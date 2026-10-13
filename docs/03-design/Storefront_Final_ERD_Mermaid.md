# Storefront ERD — Mermaid Source

```mermaid
erDiagram
    COLLECTION ||--o{ PRODUCT : groups
    CUSTOMER o|--o{ ORDER : associated_with
    USER ||--o{ ORDER : creates
    ORDER ||--o{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : referenced_by
    PRODUCT ||--o{ STOCK_MOVEMENT : tracks
    ORDER o|--o{ STOCK_MOVEMENT : causes
    PRODUCT ||--o{ PRODUCT_PRICE_HISTORY : price_changes
    USER ||--o{ PRODUCT_PRICE_HISTORY : changes
    ORDER ||--o{ ORDER_EDIT_HISTORY : edits
    ORDER ||--o{ ORDER_STATUS_HISTORY : transitions
    ORDER ||--o| SALE_VOID_HISTORY : voided_by
    EXPENSE_CATEGORY ||--o{ EXPENSE : classifies
    USER ||--o{ EXPENSE : creates
    EXPENSE ||--o{ EXPENSE_CHANGE : edits
    EXPENSE ||--o| EXPENSE_VOID_HISTORY : voided_by
    USER ||--o{ ORDER_EDIT_HISTORY : records
    USER ||--o{ ORDER_STATUS_HISTORY : records
    USER ||--o{ SALE_VOID_HISTORY : performs
    USER ||--o{ EXPENSE_CHANGE : records
    USER ||--o{ EXPENSE_VOID_HISTORY : performs
```

## Core constraints
- Product.collection is nullable; deleting/removing a collection must not delete products.
- Product title is not unique; SKU is optional and unique if supplied.
- OrderItem has unique `(order_id, product_id)`.
- Customer is optional on Order.
- Stock changes and movement ledger writes are atomic.
- Price changes and price-history writes are atomic.
- Sale void and stock restoration are atomic and idempotent.
- Reports use inclusive Asia/Karachi date ranges.
