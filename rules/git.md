# Rule: Git Workflow

ALWAYS apply these rules. No exceptions.

- ALWAYS commit after each logical step — not at the end of all work
- ALWAYS use commit message format: `<ticket-id>: <short description of what was done>`
  Example: `PROJ-123: add pagination to /api/pages endpoint`
- NEVER commit with failing tests — fix first, commit after
- NEVER create or push branches — Orchestrator does this
- NEVER use --no-verify to skip hooks
- NEVER amend a pushed commit

**Who does what:**
- Developer: `git add` + `git commit` after each logical step
- Orchestrator: `git checkout -b <branch>` before work starts, `git push` after QA passes
- No other agent touches git
