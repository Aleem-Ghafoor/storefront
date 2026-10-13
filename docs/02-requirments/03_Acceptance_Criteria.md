# Storefront — Acceptance Criteria
**ID:** ST-REQ-03 | **Version:** 0.4 | **Status:** Draft

## AC-01: Authentication
- Given valid Admin credentials, when login is submitted, then an authenticated session is created and the dashboard is accessible.
- Given invalid credentials, when login is submitted, then authentication fails.
- Given an unauthenticated visitor, when a protected URL is requested, then protected data/actions are unavailable.

## AC-02: Product validation and historical integrity
- Given valid selling price, cost price, and non-negative stock, when a product is saved, then it is persisted.
- Given negative stock or invalid/non-positive price, when saved, then validation rejects it.
- Given a product with historical order lines, when Admin tries to remove it from active use, then it is archived/deactivated and historical records remain intact; it is not physically deleted.

## AC-03: Order creation does not deduct stock
- Given stock is 10, when Admin creates an uncompleted order for quantity 3, then stock remains 10.
- Given a line has quantity zero, negative quantity, or an unknown product, when submitted, then it is rejected.
- Given an order is uncompleted, when reports are generated, then it contributes no completed-sale revenue or COGS.

## AC-04: Completing a sale deducts stock exactly once
- Given stock is 10 and an eligible order contains quantity 3, when sale completion succeeds, then stock becomes 7, the order becomes completed, and one sale is recorded.
- Given an order is already completed, when completion is requested again, then stock does not change and no duplicate sale/revenue is recorded.
- Given any line has insufficient stock, when completion is requested, then completion is rejected and all stock quantities remain unchanged.
- Given a failure occurs during completion, when the operation ends, then stock, sale, and order status remain as before the operation.
- Given two completion requests arrive close together, when processed, then the order is deducted/recorded at most once.

## AC-05: Expense validation
- Given a valid positive amount, date, category, and description, when saved, then the expense is stored and included in reports for the applicable period.
- Given an amount of zero or less, when saved, then validation rejects it.
- Given an expense category, when an expense is saved, then the category must come from the predefined list.
- Given an expense is edited or deleted, when the operation succeeds, then an audit record is retained.

## AC-06: Financial formulas
Test data for one reporting period:
- Completed-sale revenue = 1,000
- COGS = 600
- Included operating expenses = 150

Expected report:
- Revenue = 1,000
- COGS/product cost = 600
- Gross profit = 1,000 − 600 = 400
- Net profit = 400 − 150 = 250

Additional scenarios:
- Pending orders are excluded from revenue and COGS.
- With no completed sales and no expenses, totals are zero or a clear empty state appears.
- Editing the current product price/cost after a sale does not change historical line values or historical report totals.
- Report clearly shows its date range and currency (PKR).
- Monetary amounts are stored/displayed to two decimal places; calculation rounding follows the documented policy once finalized.
- Products at or below the configured low-stock threshold are identified in inventory.
- A completed sale is included according to its completion date, even if the order was created in an earlier reporting period.
- Discounts and tax calculations are not applied to initial sales totals.

## AC-07: Quality and traceability
- Every in-scope functional requirement links to a use case or test.
- Stock and financial rules have automated success and rejection tests.
- Setup instructions do not expose secrets.
- Tests run using documented commands.

## Remaining decisions before implementation
1. Money calculation rounding method.
2. Whether pending orders reserve stock without deducting it.
3. Detailed Admin-only mistaken-sale void/correction rules: reason/confirmation, stock restoration, revenue/COGS treatment, and audit history. Returns/refunds remain deferred.
4. Low-stock threshold: global or per product, and default value.
5. Expense audit details: fields/history visibility and deletion behavior.
6. Product archive visibility and reactivation behavior.
7. Timezone and date-range boundary rules.
8. Deployment, backup approach, and deadline.


## AC-08: Pending orders do not reserve stock (confirmed v0.5)
- Given a product has stock 10, when an order for quantity 3 is created, then stock remains 10 and no stock is reserved.
- Given pending orders exist, when a sale is completed, then the system checks current available stock at completion time.
- Given current stock is insufficient at completion time, when completion is attempted, then it is rejected and stock/revenue remain unchanged.
