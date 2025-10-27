# Contributing

This repo uses a simple, issue-driven workflow with strict branch naming.

## Branch Naming (strict)
Use one of:
- `feature/issue-<number>-short-name`
- `bugfix/issue-<number>-short-name`
- `chore/issue-<number>-short-name`

**Examples**
- `feature/issue-12-rentals-endpoint`
- `bugfix/issue-7-auth-timezone`
- `chore/issue-3-ci-setup`

## Issue → Branch → PR
1) Create an **Issue** (use the Task template).
2) Create a **branch** from that issue.
3) Open a **PR** that references the issue (add `Closes #<issue number>` in the PR body).
4) Merge when green; the issue closes automatically.

## Pull Request Checklist
- [ ] Title is clear and scoped
- [ ] Branch name follows the required pattern
- [ ] PR body includes `Closes #<issue>`
- [ ] Code is commented where clarity helps
- [ ] App runs locally without breaking existing behavior
- [ ] Tests updated/added where sensible

## Local Dev (quick start)
```bash
git checkout -b feature/issue-<num>-short-name
# make changes
git add .
git commit -m "Issue #<num>: brief description"
git push -u origin feature/issue-<num>-short-name
# open PR on GitHub
