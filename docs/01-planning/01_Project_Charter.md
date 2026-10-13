# Storefront — Project Charter
**ID:** ST-PLN-01 | **Version:** 0.1 | **Status:** Draft

## Project summary
Storefront is an internal web-based Store Management System. A single Admin will manage products, collections, inventory, sales, orders, expenses, and reports. The project is also a practical learning project for Django and Software Engineering practices, following an FYP-style lifecycle.

## Problem statement
Many stores need to maintain product records, monitor stock, record sales, manage orders, and track expenses. When these activities are handled manually or through separate records, it can be difficult to maintain accurate information and understand financial performance. Storefront aims to provide one centralized application for managing these activities.

*This problem statement is proposed and has not yet been validated through research with an actual store.*

## Objectives
1. Manage products and collections.
2. Maintain inventory and stock levels.
3. Record sales and manage orders.
4. Maintain customer records where needed.
5. Record and categorize expenses.
6. Report stock, sales, expenses, and estimated profit.
7. Protect store information through Admin authentication.
8. Apply planning, requirements, design, Git, testing, deployment, and documentation practices.
9. Build incrementally to support practical learning.

## Primary user
- **Admin:** the only planned role in the initial version.

## High-level deliverables
- Planning documents
- Software Requirements Specification (SRS)
- Use cases and acceptance criteria
- Design document and diagrams
- Application source code
- Test plan, test cases, and test report
- Setup/deployment guide
- Final documentation and retrospective

## Success criteria
- Agreed in-scope workflows work correctly.
- Important business rules have test coverage.
- Requirements can be linked to implementation and tests.
- Setup instructions are sufficient to run the project.
- Developer can explain the architecture and key data flows.

## Constraints and assumptions
- Existing Django `storefront` repository is the starting point and must be audited.
- Django/Python remain the current learning stack unless the audit gives a strong reason to change.
- Single Admin; no separate Manager/Staff roles initially.
- Deadline, hosting, budget, and detailed business rules are not confirmed.
