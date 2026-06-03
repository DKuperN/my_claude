# Rule: Test-Driven Development

ALWAYS apply these rules. No exceptions.

- ALWAYS write tests as part of building a feature — not after
- ALWAYS cover: happy path + at least one error case + one edge case per endpoint or component
- ALWAYS run the full test suite after any change — not just the changed file's tests
- NEVER mark a task complete if tests are missing or failing
- NEVER ship a fix without re-running the full test suite
- NEVER let QA be the first to discover missing tests — that is a Developer failure

**QA classification rule:** Missing tests = CRITICAL bug. Same severity as broken core functionality.

**Test location rule:** Tests live next to the code they test (or in the pattern already used by the project).
Match existing test file location and naming — check `_agent_context/onboarding/qa_context.md` for the project's pattern.
