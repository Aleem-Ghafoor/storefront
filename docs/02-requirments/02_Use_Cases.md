# Storefront — Use Cases
**ID:** ST-REQ-02 | **Version:** 0.4 | **Status:** Draft

## UC-01: Admin logs in
**Actor:** Admin. **Precondition:** Admin account exists.
1. Admin enters credentials.
2. System validates them.
3. On success, system creates an authenticated session and opens the dashboard.
**Alternative:** Invalid credentials show an error and do not authenticate the user.
**Postcondition:** Only valid credentials create an authenticated session.
**Requirements:** FR-001–FR-003, NFR-001.

## UC-02: Manage products and collections
**Actor:** Admin. **Precondition:** Admin is authenticated.
1. Admin opens products or collections.
2. Admin creates or edits a record.
3. System validates fields.
4. System saves valid data and confirms success.
**Alternative:** Invalid values are rejected with clear feedback. Products with historical records are archived/deactivated rather than physically deleted.
**Requirements:** FR-010–FR-014.

## UC-03: Create an order
**Actor:** Admin. **Precondition:** Admin is authenticated and products exist.
1. Admin starts an order.
2. Admin adds products and positive quantities.
3. System validates product references and quantities.
4. System saves the order as non-completed and preserves line-item values needed for history.
5. System confirms creation.
**Postcondition:** Stock is unchanged and no completed-sale revenue is recorded.
**Requirements:** FR-020–FR-023, FR-029.

## UC-04: Complete sale from an order
**Actor:** Admin. **Precondition:** Admin is authenticated; order is eligible for completion.
1. Admin opens an order and requests completion.
2. System checks order status and stock for every line.
3. System atomically deducts stock, records the sale, and updates order status.
4. System confirms completion.
**Alternatives:** Insufficient stock rejects completion without changing any line. Already-completed orders do not cause a second deduction. A transaction failure rolls back all changes.
**Postcondition:** One completed sale and one stock deduction per ordered quantity.
**Requirements:** FR-024–FR-030, NFR-003, NFR-005.

## UC-05: Record an expense
**Actor:** Admin. **Precondition:** Admin is authenticated.
1. Admin enters amount, date, category, and description.
2. System validates values.
3. System saves the expense and confirms success.
**Alternative:** Zero/negative amount is rejected. Expense edits/deletions are recorded in audit history; categories are selected from a predefined list.
**Requirements:** FR-050–FR-052.

## UC-06: View financial report
**Actor:** Admin. **Precondition:** Admin is authenticated.
1. Admin selects a date range.
2. System retrieves completed sales and included expenses.
3. System selects completed sales by sale completion date and expenses by expense date.
4. System calculates revenue, COGS, gross profit, and net profit without discount or tax calculations.
5. System displays totals in PKR and the selected date range.
**Alternative:** No records produce zero totals or a clear empty state.
**Postcondition:** Report is reproducible from stored records.
**Requirements:** FR-060–FR-069, NFR-008.

## UC-07: Access protected area without authentication
**Actor:** Unauthenticated visitor. **Precondition:** Visitor is not logged in.
1. Visitor requests a protected URL.
2. System denies access or redirects to login.
**Postcondition:** No protected information or action is exposed.
**Requirements:** FR-003, NFR-001.

## UC-08: Review inventory
**Actor:** Admin. **Precondition:** Admin is authenticated.
1. Admin opens inventory.
2. System displays persisted stock quantities.
3. Admin can identify available stock and products at/below the configured low-stock threshold.
4. Admin can archive/deactivate a product with historical records instead of deleting it.
**Requirements:** FR-012, FR-014, FR-071.

**Out of initial scope:** returns/refunds, discounts, and tax calculation. **Still open:** pending-order stock reservation; detailed effects and audit requirements for Admin-only mistaken-sale void/correction; low-stock threshold scope/default; expense audit-history fields and deletion behavior; archive/reactivation behavior; money rounding method; and report date-boundary/timezone rules.
