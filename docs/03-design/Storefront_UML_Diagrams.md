# Storefront — UML Diagrams

These are design drafts aligned to the agreed Storefront requirements. They describe intended behavior, not implemented code.

## Shared rules
- One Admin role in the initial version.
- Pending orders do not reserve stock.
- Order completion validates all items before stock deduction.
- Sale void requires a reason, restores stock, and preserves audit history.
- Use atomic database transactions for completion and void operations.
- Voided sales are excluded from revenue and COGS reports.
- `OrderService` is a proposed application service, not a Django built-in.

## 1. Use Case Diagram

Admin manages products, collections, stock, orders, customers and expenses, and can view reports and audit history.

```mermaid
flowchart LR
    Admin([Admin])
    Admin --- P1[Manage Products]
    Admin --- P2[Manage Collections]
    Admin --- P3[Manage Stock]
    Admin --- P4[Manage Orders]
    Admin --- P5[Manage Customers]
    Admin --- P6[Manage Expenses]
    Admin --- P7[View Reports]
    Admin --- P8[View Audit History]
```

## 2. Class Diagram

The class diagram is a conceptual model. Django field definitions, delete policies and service classes will be finalized during implementation.

```mermaid
classDiagram
    class User {
      +id
      +username
      +is_active
    }
    class Collection {
      +id
      +title
      +is_active
    }
    class Product {
      +id
      +title
      +sku
      +selling_price
      +cost_price
      +stock_quantity
      +low_stock_threshold
      +is_active
    }
    class Customer {
      +id
      +name
      +phone
      +is_active
    }
    class Order {
      +id
      +order_number
      +status
      +created_at
      +completed_at
    }
    class OrderItem {
      +id
      +quantity
      +unit_selling_price
      +unit_cost_price
    }
    class StockMovement {
      +id
      +movement_type
      +quantity_delta
      +reason
      +created_at
    }
    class ExpenseCategory {
      +id
      +name
      +is_active
    }
    class Expense {
      +id
      +amount
      +expense_date
      +is_voided
    }
    class ProductPriceHistory {
      +price_type
      +old_price
      +new_price
      +reason
      +changed_at
    }
    class OrderEditHistory {
      +field_name
      +old_value
      +new_value
      +reason
    }
    class OrderStatusHistory {
      +old_status
      +new_status
      +changed_at
    }
    class SaleVoidHistory {
      +reason
      +voided_at
    }
    class ExpenseChange {
      +field_name
      +old_value
      +new_value
      +reason
    }
    class ExpenseVoidHistory {
      +reason
      +voided_at
    }

    Collection "0..1" --> "0..*" Product : groups
    Customer "0..1" --> "0..*" Order : optional customer
    User "1" --> "0..*" Order : created by
    Order "1" *-- "1..*" OrderItem : contains
    Product "1" --> "0..*" OrderItem : referenced by
    Product "1" --> "0..*" StockMovement : movement ledger
    Order "0..1" --> "0..*" StockMovement : sale movement
    Product "1" --> "0..*" ProductPriceHistory : price audit
    Order "1" --> "0..*" OrderEditHistory : edit audit
    Order "1" --> "0..*" OrderStatusHistory : status audit
    Order "1" --> "0..1" SaleVoidHistory : void record
    ExpenseCategory "1" --> "0..*" Expense : categorizes
    Expense "1" --> "0..*" ExpenseChange : edit audit
    Expense "1" --> "0..1" ExpenseVoidHistory : void record
```

## 3. Activity Diagram — Order Completion

The system validates every line before committing any deduction. If stock is insufficient, no partial update should remain.

```mermaid
flowchart TD
    A([Start]) --> B[Admin selects an order]
    B --> C[Click Complete Order]
    C --> D{Order is Pending?}
    D -- No --> E[Reject completion]
    E --> Z([End])
    D -- Yes --> F{Order has at least one item?}
    F -- No --> G[Show validation error]
    G --> Z
    F -- Yes --> H[Begin database transaction]
    H --> I[Lock order and product rows]
    I --> J[Check stock for every item]
    J --> K{Enough stock for all items?}
    K -- No --> L[Rollback transaction]
    L --> M[Show insufficient stock error]
    M --> Z
    K -- Yes --> N[Deduct stock for each product]
    N --> O[Create StockMovement records]
    O --> P[Set status Completed and completed_at]
    P --> Q[Create OrderStatusHistory]
    Q --> R[Commit transaction]
    R --> S[Show success]
    S --> Z
```

## 4. Activity Diagram — Sale Void

Voiding preserves the original order and its history. The reason is mandatory, and restoration plus status changes are atomic.

```mermaid
flowchart TD
    A([Start]) --> B[Admin selects completed order]
    B --> C[Enter void reason]
    C --> D{Reason provided?}
    D -- No --> E[Show validation error]
    E --> Z([End])
    D -- Yes --> F{Order status is Completed?}
    F -- No --> G[Reject void request]
    G --> Z
    F -- Yes --> H[Begin database transaction]
    H --> I[Lock order and affected products]
    I --> J[Restore stock quantities]
    J --> K[Create StockMovement records]
    K --> L[Set order status Voided]
    L --> M[Create OrderStatusHistory]
    M --> N[Create SaleVoidHistory]
    N --> O[Commit transaction]
    O --> P[Exclude sale from reports]
    P --> Q[Show success]
    Q --> Z
```

## 5. Sequence Diagram — Order Completion

OrderService is a proposed project service layer, not a built-in Django class.

```mermaid
sequenceDiagram
    actor Admin
    participant UI as Django UI
    participant Service as OrderService
    participant DB as Database

    Admin->>UI: Click Complete Order
    UI->>Service: complete_order(order_id)
    Service->>DB: Begin transaction
    Service->>DB: Lock order and product rows
    DB-->>Service: Return order and stock data
    Service->>Service: Validate status, items and stock

    alt Invalid order or insufficient stock
        Service->>DB: Rollback transaction
        Service-->>UI: Return validation error
        UI-->>Admin: Show error
    else All checks pass
        Service->>DB: Deduct stock
        Service->>DB: Create StockMovement records
        Service->>DB: Set Completed and completed_at
        Service->>DB: Create OrderStatusHistory
        Service->>DB: Commit transaction
        Service-->>UI: Return success
        UI-->>Admin: Show completion confirmation
    end
```

## 6. Sequence Diagram — Sale Void

The sale is excluded from revenue and COGS reports after voiding.

```mermaid
sequenceDiagram
    actor Admin
    participant UI as Django UI
    participant Service as OrderService
    participant DB as Database

    Admin->>UI: Select completed order
    Admin->>UI: Enter void reason
    UI->>Service: void_sale(order_id, reason)
    Service->>DB: Begin transaction
    Service->>DB: Lock order and affected products
    DB-->>Service: Return current order and stock
    Service->>Service: Validate status and reason

    alt Invalid status or missing reason
        Service->>DB: Rollback transaction
        Service-->>UI: Return validation error
        UI-->>Admin: Display error
    else Validation successful
        Service->>DB: Restore product stock
        Service->>DB: Create StockMovement records
        Service->>DB: Set order status Voided
        Service->>DB: Create OrderStatusHistory
        Service->>DB: Create SaleVoidHistory
        Service->>DB: Commit transaction
        Service-->>UI: Return success
        UI-->>Admin: Display void confirmation
    end
```
