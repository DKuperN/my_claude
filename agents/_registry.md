# Agent Registry

Single source of truth for all agents in the factory.
Orchestrator reads this file before building any execution plan.

---

## How to read this registry

Each entry has:
- **AGENT** — canonical name used in logs and event entries
- **FILE** — path to agent prompt file
- **MODEL** — Claude tier to use when invoking this agent
- **DOMAINS** — task-type tags for domain detection and filtering
- **MODES** — named invocation modes the agent supports
- **READS** — files/paths the agent expects as input
- **WRITES** — files/paths the agent produces as output
- **SKILLS** — skill files the agent self-loads (Orchestrator need not inject these)
- **PARALLEL** — YES if agent can run concurrently with others at the same pipeline stage
- **DEPENDS_ON** — agents whose WRITES this agent reads (empty = can run first)

Stack-specific skills (typescript.md, python.md, etc.) are NOT listed here —
they are injected by Orchestrator from project_context.md for Developer and Reviewer.

---

## Core infrastructure

### ORCHESTRATOR
```
AGENT:       Orchestrator
FILE:        C:/PROJECTS/my_claude/agents/orchestrator.md
MODEL:       claude-sonnet-4-6
DOMAINS:     [all]
MODES:       [factory-dispatch, onboarding, task-routing]
READS:       user task input, agents/_registry.md
WRITES:      _factory/<task-id>/brief.md
             _factory/<task-id>/plan.md
             _factory/<task-id>/events.jsonl (initializes)
SKILLS:      []
PARALLEL:    NO
DEPENDS_ON:  []
```

---

## Software development domain

### ANALYST
```
AGENT:       Analyst
FILE:        C:/PROJECTS/my_claude/agents/analyst.md
MODEL:       claude-opus-4-7
DOMAINS:     [software, analysis, planning]
MODES:       [size-assessment, spec, spec-acceptance, consultation, acceptance-review, onboarding]
READS:       _factory/<task-id>/brief.md
             _factory/<task-id>/events.jsonl
             _agent_context/onboarding/analyst_context.md (if exists)
             _agent_context/onboarding/project_context.md (if exists)
WRITES:      _agent_context/spec.md
             _agent_context/acceptance.md (LARGE tasks)
             _factory/<task-id>/events.jsonl (appends)
SKILLS:      [architecture.md]
PARALLEL:    NO
DEPENDS_ON:  []
```

### DEVELOPER
```
AGENT:       Developer
FILE:        C:/PROJECTS/my_claude/agents/developer.md
MODEL:       claude-sonnet-4-6
DOMAINS:     [software]
MODES:       [build, fix, refactor, tech-review, onboarding]
READS:       _factory/<task-id>/brief.md
             _factory/<task-id>/events.jsonl
             _agent_context/spec.md
             _agent_context/onboarding/developer_context.md (if exists)
WRITES:      source files
             _agent_context/log.md
             _agent_context/tech_review.md (LARGE only)
             _agent_context/refactor_report.md (Fix mode, if found)
             _factory/<task-id>/events.jsonl (appends)
SKILLS:      [architecture.md]
             ← stack skills (typescript.md, python.md, etc.) injected by Orchestrator
PARALLEL:    NO
DEPENDS_ON:  [Analyst]
```

### REVIEWER
```
AGENT:       Reviewer
FILE:        C:/PROJECTS/my_claude/agents/reviewer.md
MODEL:       claude-sonnet-4-6
DOMAINS:     [software]
MODES:       [internal-review, branch-review, onboarding]
READS:       _factory/<task-id>/brief.md
             _factory/<task-id>/events.jsonl
             source files (changed)
             _agent_context/spec.md
             _agent_context/onboarding/reviewer_context.md (if exists)
WRITES:      _agent_context/reviews/<name>.md
             _factory/<task-id>/events.jsonl (appends)
SKILLS:      [architecture.md]
             ← stack skills injected by Orchestrator
PARALLEL:    NO
DEPENDS_ON:  [Developer]
```

### QA
```
AGENT:       QA
FILE:        C:/PROJECTS/my_claude/agents/qa.md
MODEL:       claude-sonnet-4-6
DOMAINS:     [software]
MODES:       [testing, onboarding]
READS:       _factory/<task-id>/brief.md
             _factory/<task-id>/events.jsonl
             _agent_context/acceptance.md (if exists)
             _agent_context/onboarding/qa_context.md (if exists)
WRITES:      _agent_context/qa_report.md
             _factory/<task-id>/events.jsonl (appends)
SKILLS:      []
PARALLEL:    NO
DEPENDS_ON:  [Developer, Reviewer]
```

### CT-ARCHITECT
```
AGENT:       CT-Architect
FILE:        C:/PROJECTS/my_claude/agents/architect-ct.md
MODEL:       claude-sonnet-4-6
DOMAINS:     [software, commercetools, migration]
MODES:       [solution-design, spec-validation, migration-advisory]
READS:       _factory/<task-id>/brief.md
             _factory/<task-id>/events.jsonl
             _agent_context/spec.md (if exists)
             _agent_context/wiki/ (if migration task)
WRITES:      _agent_context/ct_review/<topic>.md
             _factory/<task-id>/events.jsonl (appends)
SKILLS:      [commercetools.md, architecture.md]
PARALLEL:    YES
DEPENDS_ON:  [Analyst]
```

---

## Analysis domain

### REVERSE-ANALYST
```
AGENT:       Reverse-Analyst
FILE:        C:/PROJECTS/my_claude/agents/analyst-reverse.md
MODEL:       claude-sonnet-4-6
DOMAINS:     [analysis, documentation, legacy-code]
MODES:       [surface-scan, deep-analysis, documentation]
READS:       _factory/<task-id>/brief.md
             _factory/<task-id>/events.jsonl
             source code at project path
             _agent_context/reverse/scan_<topic>.md (steps 2-3)
WRITES:      _agent_context/reverse/scan_<topic>.md
             _agent_context/wiki/<topic>/
             _factory/<task-id>/events.jsonl (appends)
SKILLS:      [java-hybris.md, architecture.md]
PARALLEL:    NO
DEPENDS_ON:  []
```

---

## Document domain

### DOCUMENT-CONVERTER
```
AGENT:       Document-Converter
FILE:        C:/PROJECTS/my_claude/agents/document-converter.md
MODEL:       claude-haiku-4-5
DOMAINS:     [documents, conversion]
MODES:       [pdf-to-markdown, pptx-to-markdown, batch-convert]
READS:       _factory/<task-id>/brief.md
             _factory/<task-id>/events.jsonl
             source document file(s) listed in brief.md
WRITES:      _factory/<task-id>/output/<filename>.md
             _factory/<task-id>/events.jsonl (appends)
SKILLS:      [documents.md]
PARALLEL:    YES
DEPENDS_ON:  []
```

### DOCUMENT-ANALYST
```
AGENT:       Document-Analyst
FILE:        C:/PROJECTS/my_claude/agents/document-analyst.md
MODEL:       claude-sonnet-4-6
DOMAINS:     [documents, analysis, summarization]
MODES:       [summarize, extract-structure, compare, qa-over-content]
READS:       _factory/<task-id>/brief.md
             _factory/<task-id>/events.jsonl
             _factory/<task-id>/output/ (converter output, if conversion ran first)
WRITES:      _factory/<task-id>/output/analysis.md
             _factory/<task-id>/output/summary.md (summarize mode)
             _factory/<task-id>/output/structure.md (extract-structure mode)
             _factory/<task-id>/output/comparison.md (compare mode)
             _factory/<task-id>/output/qa-answers.md (qa-over-content mode)
             _factory/<task-id>/events.jsonl (appends)
SKILLS:      [documents.md]
PARALLEL:    YES
DEPENDS_ON:  [Document-Converter]  ← only when conversion was requested; otherwise []
```

---

## Model routing summary

| Stage / Agent       | Model               | Reason |
|---------------------|---------------------|--------|
| Analyst             | claude-opus-4-7     | Spec and planning require frontier reasoning |
| Developer           | claude-sonnet-4-6   | Primary code workhorse |
| Reviewer            | claude-sonnet-4-6   | Review quality matches Sonnet |
| QA                  | claude-sonnet-4-6   | Test execution and reporting |
| CT-Architect        | claude-sonnet-4-6   | Domain knowledge + structured output |
| Reverse-Analyst     | claude-sonnet-4-6   | Deep reading of legacy code |
| Document-Converter  | claude-haiku-4-5    | Stateless, parallelizable leaf task |
| Document-Analyst    | claude-sonnet-4-6   | Analysis requires reasoning |

**Monitoring signal:** If Opus is consuming >80% of total cost across a pipeline run,
the model router is broken — investigation needed.

---

## Domain detection rules (used by Orchestrator)

| Signal | Domain |
|--------|--------|
| File extensions .pdf, .pptx, .docx, .xlsx in task description | `documents` |
| Keywords: "analyse", "document", "legacy", "wiki", "reverse" | `analysis` |
| Keywords: "commercetools", " CT ", "hybris migration" | `software+ct` |
| Keywords: "convert", "to markdown", "extract from" + file path | `documents` |
| Default (no domain signal detected) | `software` |
