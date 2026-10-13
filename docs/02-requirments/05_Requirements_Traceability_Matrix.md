# Storefront — Requirements Traceability Matrix
**Version:** 0.1 | **Status:** Draft for design review

| Requirement(s) | Use case / workflow | Acceptance/test coverage | Design area |
|---|---|---|---|
| FR-001–003, NFR-001 | UC-01 Login; UC-07 Protected access | Valid login, invalid login, unauthenticated access denied | Authentication/session and access control |
| FR-010–016 | UC-02 Product/collection management; UC-08 Inventory review | Product validation, non-negative stock, cost price, archive instead of delete, PKR precision, no discounts/taxes | Product, Collection, inventory |
| FR-020–030; BR-01, BR-02, BR-10 | UC-03 Create order; UC-04 Complete sale | Order creation leaves stock unchanged; stock checked at completion; insufficient stock rejected; atomic/idempotent completion; historical price/cost preserved | Order, OrderItem, sale completion transaction |
| FR-040–041 | UC-03 Create order | Walk-in order can omit customer; customer may be linked when known | Customer optional relationship |
| FR-050–052; BR-12–13 | UC-05 Expense management | Positive amount validation; predefined category; edit/delete audit history | Expense, ExpenseAudit |
| FR-060–071; BR-03, BR-05, BR-09, BR-11, BR-14 | UC-06 Reports; UC-08 Inventory review | Completion-date filtering; revenue/COGS/expenses/gross/net formulas; pending orders excluded; low-stock detection; two-decimal PKR | Reporting queries, stored historical line values, threshold |
| NFR-002–NFR-008 | All use cases | Server-side validation, test coverage, maintainability, recoverability, auditability | Cross-cutting architecture and tests |

## Notes
- Verify exact NFR IDs against the latest SRS before marking this matrix final.
- Every requirement should eventually link to at least one automated test or a documented manual verification.
- The current Django models/migrations must be audited before the proposed data model is adopted.
