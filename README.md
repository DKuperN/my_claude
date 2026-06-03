# my_claude — Quick Reference

## Normal Claude Code session
cd C:/PROJECTS/my_claude
codemie-claude

## Agent mode — interactive
cd C:/PROJECTS/my_claude
codemie-claude
> Read AGENTS.md and agents/orchestrator.md. You are the orchestrator. Task: <your task here>

## Agent mode — slash commands (fastest)
Once inside a session, use slash commands instead of typing the full boilerplate:

| Command | What it does |
|---|---|
| `/guide` | **Start here if you're new** — interactive tour with theory + commands |
| `/onboard <project-path>` | Onboard a new project (all agents run setup) |
| `/task <description or ticket-id>` | Run a development task through the full pipeline |
| `/review-branch <branch> in project at <path>` | Code review for a team branch |
| `/analyse <what> in project at <path>` | Legacy code analysis → Wiki docs |
| `/ct-design <what> in project at <path>` | Commercetools solution design or spec validation |

## Agent mode — direct task (CLI)
codemie-claude --task "Read C:/PROJECTS/my_claude/AGENTS.md and agents/orchestrator.md. You are the orchestrator. Task: <your task here>"

## Agent mode — task from file
codemie-claude --task "Read C:/PROJECTS/my_claude/AGENTS.md and agents/orchestrator.md. You are the orchestrator. Task is in file C:/PROJECTS/my_claude/tasks/<filename>.md"

## Task size and pipelines
Orchestrator determines task size automatically via Analyst.

SMALL  (bug / hotfix):         Developer → Code Reviewer → QA
MEDIUM (feature):              Analyst → Developer → Code Reviewer → QA
LARGE  (new module / service): Analyst → [CT Architect if needed] → Developer (Tech Review)
                               → Code Reviewer → QA (up to 3 runs) → Acceptance

## Legacy analysis pipeline
ReverseAnalyst (surface scan)
  → Analyst (confirm scope)
  → ReverseAnalyst (deep analysis + docs)
  → [CT Architect if migration] → Analyst
  → _agent_context/wiki/<topic>/

## CT solution pipeline
Analyst (spec) → CT Architect (validate/design) → Analyst (final spec)

## Git workflow
Orchestrator asks at task start:
1. Solo or team mode?
2. Ticket ID? (becomes branch name e.g. PROJ-123)

Before work:  git pull origin main → git checkout -b <branch-name>
During work:  Developer commits after each logical step
After QA:
  Solo:  branch stays local, terminal message with branch name
  Team:  git push origin <branch-name>, terminal message to team

## Agents
- guide.md              — interactive onboarding tour for new team members (start here)
- orchestrator.md       — receives task, manages all agents, selects pipeline, handles git
- analyst.md            — sizes task, writes spec, consults, accepts final result
- analyst-reverse.md    — analyses legacy code, produces Wiki documentation
- architect-ct.md       — CT solution design, spec validation, migration advisory
- developer.md          — writes code, tech review, fix, refactor modes
- qa.md                 — tests app, reports bugs, runs test suite
- reviewer.md           — reviews code quality, architecture, security, TypeScript

See SOUL.md for the core principles and philosophy behind the agent system.

## Skills (domain knowledge — injected per project stack)
- architecture.md       — patterns, microservices, API design, antipatterns
- typescript.md         — TypeScript rules and conventions
- javascript-node.md    — JavaScript rules and conventions
- nodejs.md             — Node.js server patterns and best practices
- python.md             — Python rules and conventions
- react.md              — React component rules and patterns
- aws-cdk.md            — AWS CDK, Lambda, API Gateway deployment
- java-hybris.md        — Java reading guide, SAP Commerce patterns, Mirakl integration
- commercetools.md      — CT platform, B2B2C patterns, migration from Hybris

Skills are auto-assigned by Orchestrator during onboarding based on detected stack.
architecture.md is always included.

## Rules (always-follow standards — no exceptions)
- rules/testing.md      — test-driven mandate: tests ship with features, missing tests = CRITICAL
- rules/git.md          — commit format, who branches, who pushes, no --no-verify
- rules/code-quality.md — no console.log, no hardcode, file size limits, TypeScript strict
- rules/context.md      — MCP limits, checkpoint protocol, context file purpose

Rules differ from Skills: Skills are reference knowledge; Rules are hard constraints every agent follows.

## Hooks (automated on file save)
Configured in .claude/settings.json:

| Hook | Trigger | Action |
|---|---|---|
| PostToolUse Write | Any .ts/.tsx/.js/.jsx file written | Runs `npm run lint` in nearest package.json directory |
| PreCompact | Context compression imminent | Prints checkpoint reminder to agents |

Hook script: scripts/post-write-lint.py

## Project output
Each project creates its own folder:
C:/PROJECTS/my_claude/<project-name>/
C:/PROJECTS/my_claude/<project-name>/_agent_context/
  onboarding/
    project_context.md       <- overall project context
    analyst_context.md       <- business domain, rules, integrations
    developer_context.md     <- stack, patterns, CDK, test setup
    qa_context.md            <- test framework, coverage, commands
    reviewer_context.md      <- architecture, code style, review focus
  spec.md                    <- task specification
  acceptance.md              <- acceptance criteria (LARGE tasks)
  log.md                     <- full activity log + checkpoints
  qa_report.md               <- latest QA report
  tech_review.md             <- developer tech review (LARGE tasks)
  refactor_report.md         <- refactoring opportunities if found
  ct_review/
    solution_<topic>_<date>.md    <- CT solution designs
    validation_<topic>_<date>.md  <- CT spec validations
    migration_<topic>_<date>.md   <- CT migration advisories
  reviews/
    <branch>_v<N>_<date>.md  <- code review files
  wiki/
    <topic>/
      overview.md
      implementation.md
      api-spec.md
      data-flow.md
      notes-for-migration.md
