# Storefront — Proposed ERD (Draft)
**Version:** 0.1 | **Status:** Conceptual proposal; validate against existing models and migrations before implementation.

```mermaid
erDiagram
    CUSTOMER o|--o{ ORDER : associated_with
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : referenced_by
    COLLECTION o|--o{ PRODUCT : groups
    ORDER ||--o| SALE : completes_as
    SALE ||--|{ SALE_LINE : snapshots
    PRODUCT ||--o{ SALE_LINE : historical_product
    EXPENSE_CATEGORY ||--o{ EXPENSE : categorizes
    EXPENSE ||--o{ EXPENSE_AUDIT : change_history
    PRODUCT ||--o{ PRODUCT_AUDIT : change_history

    CUSTOMER {
      int id PK
      string name
      string phone
    }
    ORDER {
      int id PK
      int customer_id FK "nullable for walk-in"
      string status
      datetime created_at
    }
    ORDER_ITEM {
      int id PK
      int order_id FK
      int product_id FK
      int quantity
      decimal selling_price_snapshot
      decimal cost_price_snapshot
    }
    PRODUCT {
      int id PK
      string name
      decimal selling_price
      decimal cost_price
      int stock_quantity
      int low_stock_threshold
      bool is_active
      int collection_id FK
    }
    COLLECTION {
      int id PK
      string name
    }
    SALE {
      int id PK
      int order_id FK
      datetime completed_at
      string status
      decimal revenue_total
      decimal cogs_total
    }
    SALE_LINE {
      int id PK
      int sale_id FK
      int product_id FK
      int quantity
      decimal selling_price_snapshot
      decimal cost_price_snapshot
    }
    EXPENSE_CATEGORY {
      int id PK
      string name
      bool is_active
    }
    EXPENSE {
      int id PK
      int category_id FK
      decimal amount
      date expense_date
      string description
    }
    EXPENSE_AUDIT {
      int id PK
      int expense_id FK
      string action
      text old_values
      text new_values
      datetime changed_at
    }
    PRODUCT_AUDIT {
      int id PK
      int product_id FK
      string action
      text old_values
      text new_values
      datetime changed_at
    }
```

## Important design notes
- This ERD is a proposal, not a confirmed schema. The current project already has `Customer`, `Product`, `Collection`, `Order`, `OrderItem`, `Cart`, `CartItem`, and `Tag`; inspect their actual fields and migrations before deciding what to keep or change.
- A separate `SALE`/`SALE_LINE` may be unnecessary if `Order` and `OrderItem` can represent completed sales safely. Choose after repository audit to avoid duplicate sources of truth.
- Historical price and cost snapshots are required for reliable past COGS/profit reports.
- Product archive/deactivation should preserve references from historical order/sale lines.
- Pending orders do not reserve stock. Check current stock when completing a sale.
- Admin-only void/correction requires a reason and audit trail; stock restoration and report treatment remain open design decisions.
- Returns/refunds, discounts and tax calculation remain outside the initial scope.
- Monetary fields use a decimal type with two decimal places in PKR; calculation rounding policy remains open.
