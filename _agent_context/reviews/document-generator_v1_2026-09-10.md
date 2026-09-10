# Code Review: document-generator agent
Date: 2026-09-10
Branch: feat/document-generator-agent

## Summary
APPROVED WITH NOTES

The Developer created all required files (document-generator.md, generate-pptx.md) and updated the four cross-reference files (_registry.md, AGENTS.md, README.md). The core agent spec and skill file are accurate, well-structured, and follow existing conventions. Two issues were found — neither blocks merge, but both should be addressed before the next agent is built on top of these files.

---

## Issues found

### CRITICAL (blocks merge)
None.

---

### MINOR (should fix but not blocking)

**[SHOULD] AGENTS.md model routing table missing Document-Generator row**
File: `AGENTS.md`, lines 115–124 (model routing table)
Issue: The `## Model routing` table in AGENTS.md ends at Document-Analyst. Document-Generator is absent. README.md's equivalent table was updated correctly. Anyone reading AGENTS.md for model selection guidance will not see the Document-Generator haiku override.
Fix: Add the following row to the AGENTS.md model routing table, after the Document-Analyst row:
```
| Document-Generator  | claude-sonnet-4-6  | generate-from-data (simple)              | Simple templated slides; no style-matching |
```
Note: spec.md section 4 did not explicitly call for this change, but it is required for cross-file consistency. README.md and _registry.md both include this row.

**[SHOULD] generate-from-example fallback behavior not documented in agent file**
File: `agents/document-generator.md`, Mode: generate-from-example section
Issue: spec.md Assumption 4 states: "If no Markdown exists [from Document-Converter], the agent should log a warning and fall back to generate-from-data behavior." This fallback is not mentioned anywhere in the agent's generate-from-example mode. Without it, the agent has no defined behavior when called in generate-from-example mode but the expected Markdown file is missing — it may silently error or hallucinate content.
Fix: Add a step to the "What to do" list in Mode: generate-from-example:
```
7. If example Markdown file is not found: log warning "[DOC-GENERATOR] WARNING: Example Markdown not found — falling back to generate-from-data behavior", append warning to events.jsonl, and proceed as generate-from-data.
```

---

### NOTES (observations, no action needed)

**[NOTE] generate-pptx.md Images section contains a confusing intermediate code block**
File: `skills/generate-pptx.md`, approximately lines 218–231
The first code block in the Images section uses `MSO_SHAPE_TYPE.RECTANGLE if False else 1` as the shape type argument. This is syntactically valid Python but semantically confusing — `if False else 1` always evaluates to `1`, making the `MSO_SHAPE_TYPE.RECTANGLE` branch dead code. The comment says "use freeform rectangle: MSO_CONNECTOR_TYPE = 1 is wrong; use add_shape" which adds to the confusion. The immediately following "Correct shape insertion" block gives the right pattern clearly.
Recommendation: Remove the confusing intermediate block entirely or replace it with a clean version that just shows `1` directly. The "Correct shape insertion" block is sufficient on its own.

**[NOTE] AGENTS.md does not have a "Documents pipeline" or "Domain detection" section**
File: `AGENTS.md`
spec.md section 4 instructs the Developer to update "Domain detection rules table" and "Documents pipeline description" in AGENTS.md. These sections do not exist in AGENTS.md — they exist only in README.md. The README.md updates were applied correctly. The spec appears to have confused AGENTS.md and README.md for those two sub-sections. No action needed since README.md is correct.

**[NOTE] Agent file is a verbatim copy of spec.md content**
File: `agents/document-generator.md`
The agent file content matches the spec exactly, which is correct for this task type (the spec was written as a direct "full file content to create" spec). No deviation from spec — this is positive, not a concern.

**[NOTE] Registry PARALLEL flag set to YES — verify with Orchestrator**
File: `agents/_registry.md`, DOCUMENT-GENERATOR entry
`PARALLEL: YES` means the Orchestrator may run Document-Generator concurrently with other agents at the same pipeline stage. For generate-from-example mode this is correct (it runs after Document-Converter completes). For generate-from-data mode it may run concurrently with Document-Analyst if both are in the pipeline. The Orchestrator should validate that DEPENDS_ON is respected before parallelising.

---

## Statistics
MUST: 0
SHOULD: 2
NOTES: 4

## Verdict
APPROVED WITH NOTES

No blocking issues. The agent spec is complete, technically accurate, and consistent with existing agent conventions. Two SHOULD fixes are recommended before relying on this agent in production pipelines: the AGENTS.md model routing row (consistency) and the generate-from-example fallback path (correctness under error conditions).

---

## Positive notes

- All three modes are fully specified with trigger, input, what-to-do steps, output, and print-on-finish — matching the level of detail in document-converter.md and document-analyst.md exactly.
- generate-pptx.md is technically sound: RGBColor usage, Inches for dimensions, explicit 16:9 slide size, auto-install guard, os.makedirs before save, and the pitfalls table are all correct and production-ready.
- The registry entry follows the exact same format as DOCUMENT-CONVERTER and DOCUMENT-ANALYST including field order, alignment, and the conditional DEPENDS_ON annotation.
- Hard rules section is clear and actionable (NEVER invent content, ALWAYS verify PPTX exists, max 3 retry cycles).
- Events format section includes all three event types (start, success, failure-after-retries) with concrete examples — more complete than the reference agents.
