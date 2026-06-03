# Rule: Context Window Management

Apply when running long tasks, working across many files, or with multiple agents.

## Hard limits
- Keep MCPs under 10 enabled at any time — each MCP tool shrinks available context
- Keep total active tools under 80 — above this, effective context window degrades significantly

## Checkpoint protocol
When a LARGE task has been running long (many files read, many agent turns):
1. Before calling the next agent, current agent writes a checkpoint to `_agent_context/log.md`:
   - Current mode and last completed step
   - Files changed and why
   - Next planned step
   - Open questions or risks
2. When PreCompact fires (context compression imminent):
   - Immediately write current state to `_agent_context/log.md`
   - Every agent must be restartable from context files alone
3. If context feels large: pause, checkpoint to log.md, restart the next agent pointing at context files

## Context file purpose
Each agent's context file is its persistent memory:
- `developer_context.md` — stack, patterns, CDK, test setup
- `qa_context.md` — test framework, commands, coverage gaps
- `reviewer_context.md` — architecture decisions, review focus areas
- `analyst_context.md` — business domain, constraints, integration rules

Keep these up to date. They are the memory that survives session compression.
