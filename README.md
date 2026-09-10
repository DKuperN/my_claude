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
| `/factory <task description>` | Domain-agnostic factory: code, docs, PDF/PPT conversion, analysis |
| `/review-branch <branch> in project at <path>` | Code review for a team branch |
| `/analyse <what> in project at <path>` | Legacy code analysis → Wiki docs |
| `/ct-design <what> in project at <path>` | Commercetools solution design or spec validation |

## Agent mode — direct task (CLI)
codemie-claude --task "Read C:/PROJECTS/my_claude/AGENTS.md and agents/orchestrator.md. You are the orchestrator. Task: <your task here>"

## Agent mode — task from file
codemie-claude --task "Read C:/PROJECTS/my_claude/AGENTS.md and agents/orchestrator.md. You are the orchestrator. Task is in file C:/PROJECTS/my_claude/tasks/<filename>.md"

## How the factory works
Orchestrator reads `agents/_registry.md`, detects the task domain, picks agents and model tiers, then dispatches.
All agents run in the background — the Orchestrator never blocks. After each spawn it prints a status line
and stays free to receive your instructions. When an agent finishes you see a completion message; the next
stage starts automatically. You can type `status`, `pause`, `abort`, or `skip <step>` at any point.

  Domain detection:
    .pdf / .pptx / .docx in task  →  documents pipeline
    "analyse", "legacy", "wiki"   →  analysis pipeline
    "commercetools", "CT"         →  software + CT pipeline
    "generate", "create presentation", "build slides"  →  documents pipeline
    default                       →  software pipeline

  Software pipelines (sized by Analyst):
    SMALL  (bug / hotfix):         Developer → Reviewer → QA
    MEDIUM (feature):              Analyst → Developer → Reviewer → QA
    LARGE  (new module / service): Analyst → Developer (Tech Review) → Reviewer → QA×3 → Acceptance

  Documents pipeline:
    Convert only:   Document-Converter (parallelizable per file)
    Convert + analyse: Document-Converter → Document-Analyst
    Analyse only:   Document-Analyst (no conversion)
    Generate only:  Document-Generator (generate-from-data or run-script)
    Convert + generate: Document-Converter → Document-Generator (generate-from-example)
    Convert + analyse + generate: Document-Converter → Document-Analyst → Document-Generator

  Analysis pipeline (legacy code):
    Reverse-Analyst (surface scan) → Analyst (confirm scope) → Reverse-Analyst (deep docs)

  CT solution pipeline:
    Analyst (spec) → CT Architect (validate/design) → Analyst (final spec)

## Model routing
Model selection is mode-aware: some agents use a cheaper model for simpler modes.
Orchestrator reads the mode-to-model table from `_registry.md` and passes the resolved model at spawn time.

| Agent               | Default model      | Cheaper mode (haiku)                     |
|---------------------|--------------------|------------------------------------------|
| Analyst             | claude-opus-5      | —                                        |
| Developer           | claude-sonnet-5    | —                                        |
| Reviewer            | claude-sonnet-5    | —                                        |
| QA                  | claude-sonnet-5    | testing, SMALL task                      |
| CT-Architect        | claude-sonnet-5    | spec-validation                          |
| Reverse-Analyst     | claude-sonnet-5    | surface-scan                             |
| Document-Converter  | claude-haiku-4-5-20251001 | — (always haiku)                   |
| Document-Analyst    | claude-sonnet-5    | summarize                                |
| Document-Generator  | claude-sonnet-5    | generate-from-data (simple)              |

## Git workflow
Orchestrator creates a branch at task start (solo mode by default):

  Ticket ID provided: branch name = ticket ID (e.g. PROJ-123)
  No ticket: Orchestrator asks for a branch name

  Before work:  git pull origin main → git checkout -b <branch-name>
  During work:  Developer commits after each logical step
  After QA:     branch stays local — terminal message with branch name

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
- document-generator.md — generates PPTX from structured data, example files, or scripts [Sonnet]

See SOUL.md for the core principles and philosophy behind the agent system.

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
- generate-pptx.md      — python-pptx patterns: slide layouts, themes, fonts, images, pitfalls
- patents-google.md     — Google Patents search via WebFetch xhr endpoint, minimal-cost fetch pattern

Agents self-load their own domain skills. Orchestrator only injects stack skills
(typescript.md, python.md, etc.) for Developer and Reviewer on software tasks.

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

  _factory/<task-id>/               ← per-task execution space
    brief.md                        <- task input
    plan.md                         <- execution plan: agents, stages, model tiers
    events.jsonl                    <- append-only event log (all agents write here)
    output/                         <- agent artifacts (converted docs, analysis results)

  _agent_context/                   ← persistent project knowledge (software projects)
    onboarding/
      project_context.md            <- overall project context
      analyst_context.md            <- business domain, rules, integrations
      developer_context.md          <- stack, patterns, CDK, test setup
      qa_context.md                 <- test framework, coverage, commands
      reviewer_context.md           <- architecture, code style, review focus
    spec.md                         <- task specification
    acceptance.md                   <- acceptance criteria (LARGE tasks)
    log.md                          <- full activity log + checkpoints
    qa_report.md                    <- latest QA report
    tech_review.md                  <- developer tech review (LARGE tasks)
    refactor_report.md              <- refactoring opportunities if found
    ct_review/
      solution_<topic>_<date>.md
      validation_<topic>_<date>.md
      migration_<topic>_<date>.md
    reviews/
      <branch>_v<N>_<date>.md
    wiki/
      <topic>/
        overview.md
        implementation.md
        api-spec.md
        data-flow.md
        notes-for-migration.md
