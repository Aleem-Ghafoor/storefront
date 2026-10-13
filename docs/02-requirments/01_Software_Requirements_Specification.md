# Storefront — Software Requirements Specification (SRS)
**ID:** ST-REQ-01 | **Version:** 0.5 | **Status:** Draft baseline — confirmed decisions incorporated

## 1. Purpose and scope
Storefront is an internal web application for one Admin to manage products, collections, inventory, orders, completed sales, expenses, and financial reports. It is not a public e-commerce storefront in this scope.

## 2. User
- **Admin:** the sole planned application role. Separate Manager and Staff roles are out of scope.

## 3. Confirmed business rules
- **BR-01:** Admin creates orders. A completed order generates a sale; creating an order alone is not a completed sale.
- **BR-02:** Stock is deducted only when sale completion succeeds. Pending orders do not reserve stock in the initial version; stock availability is checked at completion.
- **BR-03:** Reports include revenue, product cost/COGS, expenses, gross profit, and net profit.
- **BR-04:** Initial access model has one Admin role.
- **BR-05:** All financial values are denominated in Pakistani Rupees (PKR).
- **BR-06:** Discounts are not supported in the initial scope.
- **BR-07:** Tax calculation is not supported in the initial scope.
- **BR-08:** Returns/refunds are deferred and are not part of the initial implementation. Mistaken completed sales may be handled only through an Admin-only void/correction process; exact stock and report effects must be specified before implementation.
- **BR-09:** Reports include a sale according to its **completion date**, not order creation date.
- **BR-10:** Sale completion must be atomic and idempotent: no partial updates and no duplicate deduction.
- **BR-11:** Money values use two decimal places. The precise rounding method for calculations still needs confirmation.
- **BR-12:** Expense categories use a predefined list in the initial scope.
- **BR-13:** Expense edits/deletions must leave an audit history.
- **BR-14:** Low-stock alerts are in scope; the alert threshold and whether it is global or per product remain open.
- **BR-15:** Products with historical records are archived/deactivated rather than physically deleted.

## 4. Functional requirements

### Authentication
- **FR-001:** Admin can log in with valid credentials.
- **FR-002:** Admin can log out.
- **FR-003:** Protected management pages/actions require an authenticated Admin.

### Products and collections
- **FR-010:** Admin can create, view, and update products.
- **FR-011:** Admin can create, view, and update collections.
- **FR-012:** Selling price must be valid and stock cannot be negative.
- **FR-013:** Product cost/purchase price must be recorded for profit reporting.
- **FR-014:** Historical order records must be preserved; deletion must not break them. Products with historical records must be archived/deactivated, not physically deleted.
- **FR-015:** Financial amounts must be stored and displayed in PKR. Money values use two decimal places; calculation rounding policy remains to be finalized.
- **FR-016:** Initial sales must not apply discounts or tax calculations.

### Orders and sales
- **FR-020:** Admin can create an order with one or more product line items.
- **FR-021:** Product references must exist and quantities must be positive integers.
- **FR-022:** Creating an order does not deduct or reserve stock.
- **FR-023:** Admin can view order details and status.
- **FR-024:** Admin can complete an eligible order.
- **FR-025:** Successful completion records the sale and deducts stock for its line items exactly once.
- **FR-026:** Completion is rejected if any line item has insufficient stock at the time of completion. Pending orders do not reserve stock.
- **FR-027:** Completion is atomic: all stock and sale changes succeed together or none are committed.
- **FR-028:** Repeated completion requests must not duplicate stock deduction or revenue.
- **FR-029:** Historical order lines preserve the applicable quantity, selling price, and product cost so later edits to the current product do not change past reports.
- **FR-030:** Allowed status transitions must be enforced. Returns/refunds are out of initial scope; an Admin-only void/correction path is allowed for mistaken completed sales; its stock and report effects must be defined before implementation.

### Customers
- **FR-040:** Admin can maintain customer information when needed for orders.
- **FR-041:** Customer details are optional for walk-in orders.

### Expenses
- **FR-050:** Admin can record an expense with amount, date, category, and description.
- **FR-051:** Expense amounts must be positive and validated server-side; amounts are recorded in PKR.
- **FR-052:** Admin can view and correct expenses, while reports remain consistent. Expense categories are predefined initially, and edits/deletions must be recorded in an audit history.

### Dashboard and financial reports
- **FR-060:** Admin can request a report for a selected date range.
- **FR-061:** Revenue includes completed sales only.
- **FR-062:** Report includes cost of goods sold (COGS) for completed sales.
- **FR-063:** Report includes recorded expenses assigned to the selected reporting period.
- **FR-064:** Gross profit = revenue − COGS.
- **FR-065:** Net profit = gross profit − included operating expenses.
- **FR-066:** Reports display PKR and use sale completion date to determine which completed sales fall within the selected period.
- **FR-067:** The selected date range is displayed on the report.
- **FR-068:** Pending orders are excluded from revenue and COGS.
- **FR-069:** Report totals are calculated from stored records, not manually entered summary values.
- **FR-070:** Discounts and taxes are not added to initial sales totals.
- **FR-071:** The inventory view must identify products at or below a configured low-stock threshold; whether the threshold is global or per product remains open.

## 5. Non-functional requirements
- **NFR-001 Security:** Protected areas require authentication; secrets must not be committed to Git.
- **NFR-002 Validation:** Server-side validation is required even when client-side validation exists.
- **NFR-003 Data integrity:** Stock and sale completion remain consistent, including duplicate requests.
- **NFR-004 Maintainability:** Django code should have clear app/module responsibilities.
- **NFR-005 Testability:** Core business rules must have automated tests, including failure paths.
- **NFR-006 Usability:** Common workflows should provide clear labels and validation feedback.
- **NFR-007 Recoverability:** Setup, configuration, backup needs, and deployment steps must be documented.
- **NFR-008 Auditability:** Financial totals must be explainable from underlying sales and expense records.

## 6. Financial definitions
- **Currency:** Pakistani Rupee (PKR).
- **Revenue:** Sum of selling amounts for completed sales in the selected period, using each sale's completion date; no discounts or tax calculations in the initial scope.
- **COGS:** Recorded cost basis of products sold in completed sales.
- **Gross profit:** Revenue − COGS.
- **Operating expenses:** Expenses included for the selected period.
- **Net profit:** Gross profit − operating expenses.
- **Date inclusion:** Completed sales are filtered by completion date. Expense-date filtering uses the expense date; timezone and date-boundary details remain to be specified.
- **Returns/refunds:** Deferred; no return/refund workflow is included in the initial scope.

## 7. Remaining open decisions
1. **Money rounding:** calculation precision and the rounding method to use with two-decimal monetary values.
2. **Pending-order stock reservation:** pending orders do not deduct stock, but whether they temporarily reserve stock is undecided.
2. **Completed-sale correction details:** Admin-only void/correction is confirmed for mistaken completed sales; define eligibility, confirmation/reason, stock restoration, revenue/COGS report treatment, and audit history. Returns/refunds remain deferred.
3. **Expense audit details:** define which fields and old/new values are retained, who can view history, and whether deletion is soft-delete or another auditable approach. Categories are predefined initially.
4. **Low-stock threshold:** alerts are required; decide whether the threshold is global or per product and what default value to use.
5. **Product archive behavior:** define how archived products appear in search/inventory and whether they can be reactivated. Physical deletion is not allowed for products with historical records.
6. **Pending-order stock reservation:** decide whether pending orders reserve stock temporarily; they do not deduct stock.
7. **Expense/report date conventions:** timezone, inclusive/exclusive range boundaries, and how expenses on boundary dates are handled.
8. **Operational details:** target deployment environment, backup approach, and project deadline are not yet confirmed.

## 8. Traceability
See `02_Use_Cases.md` and `03_Acceptance_Criteria.md`. Each requirement should be linked to design, implementation, and test evidence.
