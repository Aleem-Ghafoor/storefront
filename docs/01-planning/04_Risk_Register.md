# Storefront — Initial Risk Register
**ID:** ST-PLN-04 | **Version:** 0.1 | **Status:** Draft

Probability/impact are preliminary qualitative estimates.

| ID | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| R-01 | Coding starts before requirements are clear | Medium | High | Define requirements and acceptance criteria before each feature |
| R-02 | User model is changed after migrations | Medium | High | Audit auth configuration and decide user-model approach early |
| R-03 | Stock becomes inaccurate after sales/orders | Medium | High | Define stock rules and test success, failure, and cancellation cases |
| R-04 | Profit reports are inaccurate due to missing cost data | High | High | Define product cost and financial formulas before implementation |
| R-05 | Existing code/migrations break during refactoring | Medium | High | Audit first, use Git commits/branches, test migrations |
| R-06 | Scope grows beyond available time | Medium | Medium | Prioritize agreed workflows and log scope changes |
| R-07 | Testing is delayed until the end | Medium | High | Write tests alongside features |
| R-08 | Secrets are committed to Git | Low/Medium | High | Use environment configuration and review `.gitignore` |
| R-09 | Documentation becomes outdated | Medium | Medium | Update docs when requirements or behavior changes |
| R-10 | Backup/deployment process is unknown | Medium | Medium | Document setup, environment variables, backup, and deployment |

Review the risk register at the end of each major phase and when important requirements or design decisions change.
