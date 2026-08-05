# My Claude Agent System

## How to start

**New to the system?** Run the interactive guide:
  codemie-claude
  > /guide

**Ready to work?** Use a slash command:

| Command | What it does |
|---|---|
| `/guide` | **Start here if you're new** — interactive tour with theory + commands |
| `/onboard <project-path>` | Onboard a new project (all agents run setup) |
| `/task <description or ticket-id>` | Run a development task through the full pipeline |
| `/factory <task description>` | Domain-agnostic factory dispatch (code, docs, analysis, conversion) |
| `/review-branch <branch> in project at <path>` | Code review for a team branch |
| `/analyse <what> in project at <path>` | Legacy code analysis → Wiki docs |
| `/ct-design <what> in project at <path>` | Commercetools solution design or spec validation |

**Or the full manual way:**
  codemie-claude
  > Read AGENTS.md and agents/orchestrator.md. You are the orchestrator. Task: <your task here>

**From CLI:**
  codemie-claude --task "Read C:/PROJECTS/my_claude/AGENTS.md and agents/orchestrator.md. You are the orchestrator. Task: <your task here>"

## Task size and pipelines
Orchestrator determines task size automatically via Analyst.

  SMALL  (bug / hotfix):         Developer → Code Reviewer → QA
  MEDIUM (feature):              Analyst → Developer → Code Reviewer → QA
  LARGE  (new module / service): Analyst → [CT Architect if needed] → Developer (Tech Review)
                                 → Code Reviewer → QA (up to 3 runs) → Acceptance

## Agents
- guide.md              — interactive onboarding tour for new team members (start here)
- orchestrator.md       — reads registry, detects domain, dispatches agents, handles git
- _registry.md          — agent catalog: capabilities, model tiers, contracts, parallel flags
- analyst.md            — sizes task, writes spec, consults, accepts final result [Opus]
- analyst-reverse.md    — analyses legacy code, produces Wiki documentation [Sonnet]
- architect-ct.md       — CT solution design, spec validation, migration advisory [Sonnet]
- developer.md          — writes code, tech review, fix, refactor modes [Sonnet]
- qa.md                 — tests app, reports bugs, runs test suite [Sonnet]
- reviewer.md           — reviews code quality, architecture, security, TypeScript [Sonnet]
- document-converter.md — converts PDF/PPTX/Word → clean Markdown, parallelizable [Haiku]
- document-analyst.md   — summarize, extract structure, compare, Q&A over documents [Sonnet]

## Skills (domain knowledge — self-loaded by agents)
- architecture.md       — patterns, microservices, API design, antipatterns
- typescript.md         — TypeScript rules and conventions
- javascript-node.md    — JavaScript rules and conventions
- nodejs.md             — Node.js server patterns and best practices
- python.md             — Python rules and conventions
- react.md              — React component rules and patterns
- aws-cdk.md            — AWS CDK, Lambda, API Gateway deployment
- java-hybris.md        — Java reading guide, SAP Commerce patterns, Mirakl integration
- commercetools.md      — CT platform, B2B2C patterns, migration from Hybris
- documents.md          — document processing: Markdown conventions, citations, conversion markers

Agents self-load their domain skills (declared in each agent's Startup section).
Orchestrator injects only project-specific stack skills (typescript.md, python.md, etc.)
for Developer and Reviewer during software tasks.

## Rules (always-follow standards — no exceptions)
- rules/testing.md      — test-driven mandate: tests ship with features, missing tests = CRITICAL
- rules/git.md          — commit format, who branches, who pushes, no --no-verify
- rules/code-quality.md — no console.log, no hardcode, file size limits, TypeScript strict
- rules/context.md      — MCP limits, checkpoint protocol, context file purpose

## Documenting new capabilities

When the user says **"document new capabilities"** (or any equivalent), apply this checklist.
No need to ask where — figure it out from the nature of the change:

| What changed | Where to document |
|---|---|
| New orchestrator behaviour (dispatch, modes, workflow) | `agents/orchestrator.md` (primary), `README.md` (factory overview section) |
| New core principle or philosophy shift | `SOUL.md` (Core Principles list) |
| New agent or new agent mode | `agents/_registry.md` + `AGENTS.md` (Agents list) + `README.md` (Agents table) |
| New slash command | `README.md` (slash commands table) + `AGENTS.md` (slash commands table) |
| New rule (testing / git / code quality) | `rules/<topic>.md` |
| New skill (domain knowledge) | `skills/<topic>.md` + `README.md` (Skills list) + `AGENTS.md` (Skills list) |
| User-facing behaviour change | `agents/guide.md` (relevant scenario + Scenario 8 system overview) |
| New hook or settings change | `README.md` (Hooks table) + `.claude/settings.json` |

**Always update in this order:** primary spec file first → README.md → SOUL.md if philosophical → guide.md for user-facing changes.
One rule: if a user would ask "/guide" and be surprised the feature wasn't mentioned — it belongs in guide.md.

## Permissions
Pre-approved for this folder. No confirmations needed.

## Model routing
| Agent               | Model              | Reason |
|---------------------|--------------------|--------|
| Analyst             | claude-opus-4-7    | Spec and planning require frontier reasoning |
| Developer           | claude-sonnet-4-6  | Primary code workhorse |
| Reviewer            | claude-sonnet-4-6  | Review quality |
| QA                  | claude-sonnet-4-6  | Test execution and reporting |
| CT-Architect        | claude-sonnet-4-6  | Domain knowledge + structured output |
| Reverse-Analyst     | claude-sonnet-4-6  | Deep reading of legacy code |
| Document-Converter  | claude-haiku-4-5   | Stateless parallelizable leaf task |
| Document-Analyst    | claude-sonnet-4-6  | Analysis requires reasoning |

## Project output
Each project gets its own folder:
  C:/PROJECTS/my_claude/<project-name>/
  C:/PROJECTS/my_claude/<project-name>/_factory/        ← per-task execution space
    <task-id>/
      brief.md                  <- task input (orchestrator writes)
      plan.md                   <- execution plan: agents, stages, model tiers
      events.jsonl              <- append-only event log (all agents write here)
      output/                   <- agent artifacts (converted docs, analysis results)
      agent-log.md              <- human-readable execution trace
  C:/PROJECTS/my_claude/<project-name>/_agent_context/  ← persistent project knowledge
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
      solution_<topic>_<date>.md
      validation_<topic>_<date>.md
      migration_<topic>_<date>.md
    reviews/
      <branch>_v<N>_<date>.md  <- code review files
    wiki/
      <topic>/
        overview.md
        implementation.md
        api-spec.md
        data-flow.md
        notes-for-migration.md
