---
name: budget-cli
description: Use for the budgetApp Python CSV-based CLI bookkeeping project, including project rules, TDD workflow, QA checks, and implementation guidance.
---

# budgetApp Skill

Use this skill for work in the CSV-based accounting CLI app.

## Working rules
- Write tests before implementation.
- Keep every function typed.
- Keep functions short and under 50 lines.
- Keep cyclomatic complexity at 10 or below.
- Run `pytest` and `radon cc` during verification.
- Before any commit, route the change through `qa_engineer` review.

## Recommended workflow
1. Add or update tests first.
2. Implement the smallest change that passes them.
3. Run `pytest`.
4. Run `radon cc`.
5. Ask `qa_engineer` to inspect the diff.
6. Commit and push once one feature is complete.
