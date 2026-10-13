# Storefront — Assumptions, Decisions, and Glossary
**ID:** ST-PLN-06 | **Version:** 0.1 | **Status:** Draft

## Confirmed decisions
- Internal Store Management System.
- Single Admin; no separate Manager/Staff roles initially.
- Main workflow: inventory, sales, orders, expenses, profit reports.
- Main goal: learn Django and Software Engineering for a future FYP.
- Develop agreed scope incrementally.
- Existing `storefront` repository is the starting point.

## Assumptions to validate
- A single Admin account is enough for the first version.
- Public shopping and online payment are not needed.
- Customer records are only needed where relevant to sales/orders.
- Product cost data will be available for profit calculations.
- Existing code can be audited and improved incrementally.
- Deadline and deployment environment are not yet known.

## Open decisions
- Are sales recorded directly, through orders, or both?
- When is stock reduced: sale completion, order creation, or order confirmation?
- Should reports show revenue/expenses only, gross profit, or gross and net profit?
- How do cancellations, returns, discounts, and unpaid sales affect stock/reports?
- Should products with historical records be archived rather than deleted?
- Which currency and date/time conventions apply?
- Where will the application be deployed?

## Glossary
- **SDLC:** Software Development Life Cycle.
- **Scope:** Features and boundaries agreed for the project.
- **Feasibility study:** Early assessment of whether the project is practical.
- **Risk register:** Tracked risks, impacts, and mitigation plans.
- **SRS:** Software Requirements Specification.
- **Acceptance criteria:** Conditions required to accept a feature.
- **ERD:** Entity-Relationship Diagram.
- **ADR:** Architecture Decision Record.
- **Traceability:** Links from requirements to design, implementation, and tests.

## Reference
ISO/IEC/IEEE 29148:2018, *Systems and software engineering — Life cycle processes — Requirements engineering*. Used as a reference point for disciplined documentation; this project does not claim formal compliance.
Official overview: https://committee.iso.org/standard/72089.html
