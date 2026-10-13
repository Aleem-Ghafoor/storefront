# Storefront — Scope Statement
**ID:** ST-PLN-02 | **Version:** 0.1 | **Status:** Draft

## In scope
1. Admin login/logout.
2. Product and collection management.
3. Inventory quantity tracking.
4. Sales recording.
5. Order creation and status tracking, subject to final workflow decisions.
6. Customer records where needed for sales/orders.
7. Expense records: amount, date, category, description.
8. Dashboard and reports for stock, sales, expenses, and profit estimates.
9. Validation, error handling, and data-integrity controls.
10. Tests, Git version control, documentation, and deployment preparation.

## Out of scope initially
- Public customer shopping accounts and storefront checkout.
- Online payment gateway.
- Separate Manager/Staff roles.
- Multi-branch or multi-warehouse support.
- Native mobile app.
- AI forecasting.
- External accounting integration or claims of regulatory accounting compliance.

## Clarifications
- “Complete system” means completing the agreed workflows in stages, not adding every possible retail feature.
- Profit requires reliable product cost data. The current Product model has a selling `price`; product purchase/cost price must be considered in design.
- Stock deduction and order-status rules must be defined before implementation.
- Existing models and migrations must be reviewed before structural changes.

## Scope change process
For each proposed feature, record its reason, linked objective/requirement, impact on data/code/tests/schedule, and a decision to accept, defer, or reject.
