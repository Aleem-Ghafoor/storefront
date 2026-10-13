# Storefront — Updated Requirements Decisions
**ID:** ST-REQ-04 | **Version:** 0.5 | **Status:** Draft baseline

## Confirmed decisions
- Internal Store Management System.
- Single Admin; no separate Manager/Staff roles initially.
- Admin creates orders; completed orders generate sales.
- Stock is deducted only when sale completion succeeds.
- Pending orders do not reserve stock in the initial version. Stock is checked and deducted only when the sale is completed.
- Reports include revenue, product cost/COGS, expenses, gross profit, and net profit.
- Gross profit = revenue − COGS.
- Net profit = gross profit − included operating expenses.
- Sale completion must be atomic and idempotent: no partial updates and no duplicate deduction.
- Currency is Pakistani Rupees (PKR), with monetary values represented to two decimal places.
- Discounts and tax calculation are excluded from the initial scope.
- Returns/refunds are deferred and excluded from the initial scope.
- A mistaken completed sale may use an Admin-only void/correction process; exact stock/report behavior remains to be specified.
- Sales are included in reports according to sale completion date.
- Customer details are optional for walk-in orders.
- Expense categories are predefined in the initial scope.
- Expense edits/deletions must be auditable.
- Low-stock alerts are in scope.
- Products with historical records are archived/deactivated rather than physically deleted.

## Remaining open questions
1. What rounding method should be used for calculations involving two-decimal monetary values?
3. For a mistaken completed sale, what conditions/reason/confirmation are required, how is stock restored, how are revenue and COGS corrected in reports, and what audit trail is kept? Returns/refunds remain deferred.
4. Is the low-stock threshold global or per product, and what is its default value?
5. Which expense fields and old/new values should be kept in history, who can view it, and how should deletions work?
6. How should archived products appear in inventory/search, and can they be reactivated?
7. What timezone and inclusive/exclusive date-range boundary rules should reports use?
8. What deployment environment, backup approach, and project deadline apply?

## Design caution
Audit the current models and migrations before changing the schema. Profit reports need product cost and preserved historical order-line values. Keep the existing repository as the starting point and make schema changes only after requirements and ERD review.
