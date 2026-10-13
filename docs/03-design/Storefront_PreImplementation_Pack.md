# Storefront — Pre-Implementation Design Pack

**Project:** Internal Store Management System  
**Architecture:** Django Modular Monolith  
**Status:** Pre-implementation design baseline  
**Scope:** Single Admin; products, inventory, orders/sales, expenses, reports and audit history.

> This pack consolidates the remaining design work before coding. It does not claim that the system is implemented or tested. Existing requirements, ERD and UML deliverables remain the source artifacts; this document aligns architecture and implementation planning with those decisions.

## 1. Scope baseline

### Included
- One Admin role using Django authentication and authorization.
- Products and collections.
- Optional customer records.
- Orders and order items.
- Stock ledger, opening stock and manual stock adjustments.
- Order completion, cancellation and completed-sale voiding.
- Expense categories, expenses, edits and voiding.
- Revenue, cost of goods sold (COGS), gross profit, net profit and low-stock reporting.
- Audit/history records for sensitive changes.
- PKR monetary amounts stored as decimals to two places.
- Asia/Karachi timezone and timezone-aware timestamps.

### Excluded from initial version
- Separate Manager/Staff roles.
- Tax and discount handling.
- Returns/refunds workflow.
- Inventory cost layers or FIFO/weighted-average costing.
- Multiple currencies.
- Online payment gateway or public customer storefront.

## 2. Business rules that must not change accidentally

1. Pending orders do not reserve stock.
2. Only a Pending order with at least one item and sufficient stock for every item can be completed.
3. Order completion validates all items before applying stock deductions.
4. Stock deductions, stock movement records, order status and status history are committed atomically.
5. A failed completion must not leave partial stock changes.
6. Completed sales can be voided only with a non-empty reason.
7. Sale void restores stock and records movements, status history and a void-specific audit record in one transaction.
8. Voided sales are excluded from revenue and COGS reports, but original order/history records remain.
9. Order status transitions: Pending → Completed, Pending → Cancelled, Completed → Voided. Cancelled and Voided are terminal.
10. Cancelled pending orders do not change stock because pending orders did not reserve stock.
11. A pending order can be edited. A product's selling and cost prices are snapshotted when an order item is added; existing snapshots do not silently change after product price edits.
12. Each product appears at most once per order; adding the same product again increments its quantity and creates required edit history.
13. Product opening stock creation and its StockMovement record are atomic.
14. Manual stock adjustment requires a reason and creates a StockMovement.
15. Stock quantity is a whole number and must never become negative.
16. Expense edits require a reason; expense voiding requires a reason and preserves history.
17. Report date ranges are inclusive and interpreted in Asia/Karachi.
18. Sale report date is the order completion date; expense report date is the user-entered expense_date.
19. Products with transaction history are archived/deactivated rather than hard-deleted.
20. Duplicate product names are allowed; SKU is optional but unique when present. Collection title is unique.
21. Removing a collection clears the product's collection relation without deleting the product.
22. Customer is optional on an order; customer name is required, phone is optional and non-unique.
23. Price/expense values use Decimal, not floating-point arithmetic. Expense amount must be greater than zero and have at most two decimal places. Product selling and cost prices must be greater than zero; selling below cost is allowed but should show a warning.
24. Product stock threshold is per product. A threshold of 5 is only a suggested default unless explicitly confirmed.
25. Order number format is ORD-000001 and must be allocated with a concurrency-safe mechanism, not by counting current orders.
26. Price changes record old/new value, price type, Admin, timestamp and mandatory reason in the same transaction as the update.
27. Expense creation uses a user-entered business date; created_at is automatic.
28. Initial expense categories: Rent, Electricity, Salaries, Transport, Supplies, Other.
29. Current product cost is a single current cost price; there are no inventory cost layers. Order item cost snapshots are used for COGS.
30. A completed order must contain at least one order item.

## 3. Architecture decision

Use a **Modular Monolith**: one Django project and one database, organized into feature apps. This avoids the operational complexity of microservices while keeping responsibilities separated.

### Layers
- **Presentation:** Django views, forms, templates and URLs.
- **Application/business logic:** explicit service functions for transactional workflows.
- **Data:** Django models, constraints, indexes and migrations.
- **Audit:** separate history/ledger records for important actions.
- **Tests:** unit and integration tests around business rules.

### Suggested project structure

```text
storefront/
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── apps/
│   ├── products/
│   ├── customers/
│   ├── orders/
│   ├── inventory/
│   ├── expenses/
│   ├── reports/
│   └── audit/
├── templates/
├── static/
├── tests/                 # optional shared/end-to-end tests
├── requirements.txt       # or pyproject.toml; choose one primary dependency file
└── README.md
```

Each app should contain only the files it needs, typically:
- `models.py`: persistent entities and database constraints.
- `views.py`: request/response handling; keep business logic thin.
- `forms.py`: input validation for HTML forms.
- `urls.py`: app URL routes.
- `services.py`: business workflows where useful.
- `admin.py`: Django admin registration.
- `tests.py` or a `tests/` package: automated tests.
- `apps.py`: app configuration.
- `migrations/`: schema change history.

### App responsibilities
- `products`: Product, Collection, price updates and price history entry points.
- `customers`: Customer records and deactivation.
- `orders`: Order, OrderItem, order editing, status transitions and order number allocation.
- `inventory`: stock movements, opening stock and manual adjustments.
- `expenses`: Expense, ExpenseCategory, edits and voids.
- `reports`: read-only report queries and calculations.
- `audit`: shared audit-related models or audit utilities, depending on final model ownership.

**Model ownership note:** Avoid duplicate model definitions. A history model can live in the app that owns the entity (e.g., ProductPriceHistory in products, OrderStatusHistory in orders, ExpenseChange in expenses) even if the audit app provides shared utilities. Final ownership must match the finalized ERD and imports.

## 4. Service boundaries and dependencies

### Direction of responsibility
- Views/forms validate request shape and permissions, then call services.
- `orders` owns order lifecycle and orchestrates completion/void transactions.
- `inventory` owns stock movement and stock adjustment rules.
- `products` owns product/collection and price changes.
- `expenses` owns expense changes and voiding.
- `reports` reads data and must not mutate operational records.
- Audit history is written as part of the same transaction as the action being audited.

### Important service workflows
- `complete_order(order_id, actor)`
- `cancel_pending_order(order_id, actor, reason if policy requires)`
- `void_sale(order_id, actor, reason)`
- `adjust_stock(product_id, quantity_delta, reason, actor)`
- `create_product_with_opening_stock(product_data, opening_quantity, actor)`
- `change_product_price(product_id, price_type, new_price, reason, actor)`
- `edit_expense(expense_id, changes, reason, actor)`
- `void_expense(expense_id, reason, actor)`

These are proposed service interfaces, not Django built-ins. Exact signatures may change during implementation.

### Circular-import rule
Keep dependency direction deliberate. For example, `orders` may call a public inventory service, but `inventory` should not import order service back. Shared constants/enums can be placed in a stable module when truly shared. Prefer string model references in Django relationships where helpful.

## 5. ADRs — Architecture Decision Records

### ADR-001: Modular monolith
- **Decision:** One Django project with feature-oriented apps.
- **Reason:** Easier local development, deployment, testing and transactions for a learning project.
- **Alternative rejected for now:** Microservices, because they add distributed transaction and deployment complexity without a current need.

### ADR-002: Django built-in authentication
- **Decision:** Use Django's built-in User model for the single Admin role unless a custom user requirement is discovered before the first migration.
- **Reason:** Authentication and permission primitives are provided by Django.
- **Implementation note:** Decide on any custom user model before creating initial migrations; changing later is costly.

### ADR-003: Service layer for business workflows
- **Decision:** Put complex operations in service functions rather than embedding them in views.
- **Reason:** Reusable logic and easier unit/integration testing.
- **Trade-off:** Adds a small amount of structure but prevents views becoming difficult to maintain.

### ADR-004: Atomic stock-sensitive operations
- **Decision:** Use database transactions and appropriate row locks for order completion and sale void.
- **Reason:** Prevent partial updates and concurrent stock inconsistencies.
- **Note:** Verify locking behavior on the chosen database; SQLite is not a substitute for production-grade row-lock testing.

### ADR-005: Stock ledger plus current stock
- **Decision:** Store current `stock_quantity` and append StockMovement records for every opening-stock, sale deduction, sale restoration and manual adjustment.
- **Reason:** Fast stock display with an audit trail.
- **Trade-off:** Reconciliation tests are required to detect discrepancies between current quantity and ledger history.

### ADR-006: Price snapshots on order items
- **Decision:** Store unit selling price and unit cost price on each OrderItem at the time the item is added.
- **Reason:** Historical sales and COGS must not change when current product prices change.
- **Costing limitation:** This is a single-current-cost model, not FIFO or weighted-average inventory costing.

### ADR-007: Soft voiding and audit preservation
- **Decision:** Void completed sales and expenses instead of deleting their records.
- **Reason:** Preserve traceability and explain report changes.
- **Trade-off:** Every operational report must explicitly exclude voided records.

### ADR-008: Decimal monetary values
- **Decision:** Use DecimalField with two decimal places for PKR amounts.
- **Reason:** Avoid binary floating-point rounding errors in financial calculations.

### ADR-009: Business timezone and report dates
- **Decision:** Use Asia/Karachi with `USE_TZ=True`; interpret inclusive report date ranges in this timezone.
- **Reason:** Keep business dates consistent for local operations.

### ADR-010: Sequential order numbers
- **Decision:** Use a database-backed sequence/counter or another concurrency-safe allocator for `ORD-000001` format.
- **Reason:** Concurrent order creation must not generate duplicates.
- **Rejected approach:** Counting existing orders and adding one.

### ADR-011: Product and collection deletion
- **Decision:** Archive products with transaction history. Removing a collection clears the relation but keeps products.
- **Reason:** Preserve historical references and reports.

### ADR-012: Expense edit audit
- **Decision:** Every expense edit requires a reason and records before/after values, actor and timestamp.
- **Reason:** Expense edits affect profit reporting and need traceability.

## 6. Security and data integrity

- Require authentication for all operational pages; no public self-registration in the initial internal system.
- Restrict operational actions to the Admin permission group/role.
- Use Django CSRF protection for session-authenticated form posts.
- Never change data through GET requests.
- Use Django forms/model validation plus database constraints where applicable; application validation alone is not enough for unique/positive values.
- Use ORM parameterization; avoid raw SQL unless required and safely parameterized.
- Keep secrets and `SECRET_KEY` out of source control; use environment variables for deployment.
- Set `DEBUG=False`, `ALLOWED_HOSTS`, secure cookies and HTTPS settings appropriately in production.
- Avoid exposing detailed tracebacks or customer information in user-facing error messages.
- Validate all user-controlled IDs and confirm the actor has permission.
- Use `transaction.atomic()` for multi-record operations.
- Lock relevant rows during stock-sensitive operations; validate again inside the transaction.
- Ensure idempotent guards: a completed order cannot be completed twice, and a voided sale cannot be voided twice.
- Preserve audit records; restrict destructive admin actions for transactional data.
- Back up the database and test restoration before relying on production data.
- Do not store payment card details or unnecessary sensitive personal information.

## 7. Data constraints and validation checklist

- Unique `order_number`.
- Unique collection title.
- Optional SKU unique when not blank; normalize blank values consistently.
- Unique constraint on `(order, product)` for OrderItem.
- Product prices greater than zero; Decimal, two places.
- Expense amount greater than zero; Decimal, two places.
- Stock is integer and cannot be negative.
- Order item quantity is a positive integer.
- Required reasons for price change, manual stock adjustment, expense edit and sale/expense void.
- Order completion requires at least one item.
- Valid status transitions enforced in service logic and covered by tests.
- Foreign-key delete policies preserve historical records.
- Add indexes to frequently filtered fields after considering query patterns: order status/completed_at, expense_date/is_voided, product is_active/SKU and foreign keys.
- Ensure product stock and StockMovement ledger stay reconcilable.

## 8. Testing strategy

### Unit tests
- Price and amount validators.
- Profit formulas: gross profit = revenue − COGS; net profit = gross profit − non-voided expenses.
- Status transition rules.
- Report date-boundary behavior in Asia/Karachi.

### Service/integration tests
- Product creation with opening stock creates product and movement atomically.
- Stock adjustment changes current quantity and creates a movement with a reason.
- Price update creates a ProductPriceHistory record with actor/reason.
- Pending order completion deducts all item stock and records movements/history.
- Insufficient stock prevents completion and causes no partial deductions.
- Empty order cannot complete.
- Repeated completion does not deduct stock twice.
- Pending cancellation does not affect stock.
- Sale void restores stock exactly once and requires a reason.
- Voided sale is excluded from revenue and COGS.
- Expense edits require a reason and preserve before/after values.
- Expense void is excluded from expense totals.
- Inclusive report date ranges work at start/end boundaries.
- Inactive products/customers behave consistently in selection and historical views.

### Concurrency tests
- Two simultaneous attempts to complete orders competing for the same stock must not oversell.
- Concurrent order creation must not duplicate order numbers.
- Run locking/concurrency tests against the intended database engine, not only SQLite.

### UI/security tests
- Anonymous users cannot access operational pages.
- Unauthorized users cannot perform admin actions.
- Invalid forms display safe validation messages.
- CSRF-protected writes reject missing/invalid tokens.

## 9. Implementation sequence

### Stage 0 — Environment and project setup
1. Create virtual environment and install a pinned Django version.
2. Choose the database engine for development and deployment; document any difference.
3. Create project and configuration package.
4. Decide built-in vs custom User before first migration.
5. Configure timezone, static/templates, environment variables and `.gitignore`.

### Stage 1 — Foundation
1. Create Django apps.
2. Add app configuration and URLs.
3. Add base template/navigation and login/logout.
4. Configure admin permissions and initial tests.

### Stage 2 — Models and migrations
1. Implement products/collections/customers.
2. Implement order/order items and history models.
3. Implement inventory ledger.
4. Implement expenses/categories/history.
5. Implement audit entities.
6. Add constraints and indexes.
7. Review migrations before applying them to a shared/production database.

### Stage 3 — Product and inventory workflows
1. Product create/edit/archive.
2. Opening stock with movement record.
3. Price change with reason and price history.
4. Manual stock adjustment with reason.
5. Low-stock view.

### Stage 4 — Orders and sales
1. Create pending order and edit items.
2. Concurrency-safe order numbering.
3. Complete order using atomic transaction and row locking.
4. Cancel pending order.
5. Void completed sale and restore stock atomically.
6. Test every transition and failure path.

### Stage 5 — Expenses and reports
1. Expense categories and expense CRUD.
2. Expense edit history and voiding.
3. Revenue and COGS report.
4. Gross and net profit calculations.
5. Date filters and low-stock reporting.

### Stage 6 — Hardening and release
1. Run all tests and inspect coverage of critical workflows.
2. Test migrations on a clean database.
3. Review authorization, CSRF, secrets and production settings.
4. Verify backup/restore procedure.
5. Prepare README with setup, environment variables, migrations, tests and run commands.
6. Run acceptance checklist using representative sample data.

## 10. Acceptance checklist before calling the first implementation complete

- [ ] Only Admin can use operational screens.
- [ ] Products, collections and customers behave according to deletion/archive rules.
- [ ] Opening stock and manual adjustments always have movement records.
- [ ] Prices use Decimal and price edits are audited.
- [ ] Pending orders do not reserve stock.
- [ ] Completion validates all items and never oversells.
- [ ] Completion failure leaves no partial changes.
- [ ] Cancellation of pending order does not alter stock.
- [ ] Sale void restores stock once and preserves audit history.
- [ ] Voided sales are excluded from revenue and COGS.
- [ ] Expense edits and voids are auditable and reflected correctly in reports.
- [ ] Report dates use Asia/Karachi and inclusive date boundaries.
- [ ] Order numbers remain unique under concurrent creation.
- [ ] Automated tests pass against the intended database.
- [ ] Production settings, secrets, backups and README are prepared.

## 11. Decisions still requiring confirmation before coding

These are deliberately listed instead of silently assumed:
1. Development/production database engine (SQLite for simple local learning vs PostgreSQL for stronger production-like behavior).
2. Exact Django version to pin.
3. Whether the low-stock threshold should default to 5 or be required on product creation.
4. Final ownership/location of audit-history models across apps.
5. Whether all report outputs need CSV export in the initial scope (not currently included in the confirmed baseline).

## Ready-to-code gate

Start implementation only after the five decisions above are resolved or explicitly deferred. The ERD, UML and this architecture pack are design artifacts; implementation and tests must still prove the intended behavior.
