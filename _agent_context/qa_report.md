# QA Report: document-generator agent
Date: 2026-09-10
Run: 1

## Result: PASSED

## Checks
- [PASS] Review fix: AGENTS.md model routing row
- [PASS] Review fix: generate-from-example fallback behavior
- [PASS] Review fix: generate-pptx.md dead code removed
- [PASS] All 3 modes in document-generator.md
- [PASS] Events format section present
- [PASS] Hard rules section present
- [PASS] generate-pptx.md all sections present
- [PASS] Cross-file name consistency
- [PASS] Registry entry complete

## Checks — detail

### Review fix: AGENTS.md model routing row
AGENTS.md line 125 contains:
`| Document-Generator  | claude-sonnet-4-6  | generate-from-data (simple)              | Simple templated slides; no style-matching |`
Row is present and correct. Fix verified.

### Review fix: generate-from-example fallback behavior
document-generator.md Mode: generate-from-example, What to do, step 1 now reads:
"Read the example Markdown file — if it does not exist in `_factory/<task-id>/output/`:
- Log warning: `[DOC-GENERATOR] Warning: example Markdown not found. Falling back to generate-from-data.`
- Proceed as generate-from-data mode using only the new content"
Fallback is documented and matches spec.md Assumption 4. Fix verified.

### Review fix: generate-pptx.md dead code removed
The confusing intermediate code block that contained `MSO_SHAPE_TYPE.RECTANGLE if False else 1` (flagged as a NOTE in the review) has been replaced. The Images section now shows a single clean placeholder code block using `1` directly as the shape type argument, with a clear comment:
`# add_shape takes an integer shape type: 1 = rectangle (MSO_SHAPE_TYPE.RECTANGLE)`
The "Correct shape insertion" duplicate block has been eliminated. The section now has one clear example per use case. Fix verified.

### All 3 modes in document-generator.md
Modes present: generate-from-data (line 36), generate-from-example (line 71), run-script (line 108). All three have Trigger, Input, What to do, Output, and Print on finish subsections.

### Events format section present
Section "## Events format" is present (after "## Script execution rules"). Contains three event examples: start event, completion event (success), completion event (failure after retries).

### Hard rules section present
Section "## Hard rules" is present at end of file with 7 rules covering content invention, truncation, skill loading, output verification, script artifact requirement, terminal output, and source file protection.

### generate-pptx.md all required sections present
- Library setup: present (line 8)
- Creating a presentation (layouts): present (line 44) — note: layout table is the "Slide layouts" section
- Placeholders: present (line 65)
- Fonts: present (line 138)
- Colors: present (line 166)
- Images: present (line 195)
- Structure (business presentation): present (line 230)
- Saving: present (line 249)
- Pitfalls: present (line 264)
All required sections confirmed present.

### Cross-file name consistency
Agent name "Document-Generator":
- _registry.md: `AGENT: Document-Generator` (line 221) — MATCH
- AGENTS.md agents list: `document-generator.md — generates PPTX from structured data, example files, or existing scripts [Sonnet]` (line 48) — entry present
- AGENTS.md model routing table: `| Document-Generator  |` (line 125) — MATCH
- README.md agents list: `document-generator.md — generates PPTX from structured data, example files, or scripts [Sonnet]` (line 101) — entry present
- README.md model routing table: `| Document-Generator  |` (line 77) — MATCH

File path "agents/document-generator.md":
- _registry.md: `FILE: C:/PROJECTS/my_claude/agents/document-generator.md` (line 222) — consistent
- AGENTS.md agents list: `document-generator.md` (line 48) — consistent
- README.md agents list: `document-generator.md` (line 101) — consistent

Skill path "skills/generate-pptx.md":
- _registry.md: `SKILLS: [generate-pptx.md]` (line 234) — consistent
- AGENTS.md skills list: `generate-pptx.md — python-pptx patterns: slide layouts, themes, fonts, images, common pitfalls` (line 61) — present
- README.md skills list: `generate-pptx.md — python-pptx patterns: slide layouts, themes, fonts, images, pitfalls` (line 116) — present
- document-generator.md startup: `Read own skills: C:/PROJECTS/my_claude/skills/generate-pptx.md` (line 14) — consistent

Modes consistency:
- _registry.md MODES: [generate-from-data, generate-from-example, run-script] (line 227)
- document-generator.md: all three modes present as top-level sections
- MATCH confirmed.

### Registry entry completeness
All required fields present in DOCUMENT-GENERATOR entry:
- AGENT: Document-Generator
- FILE: C:/PROJECTS/my_claude/agents/document-generator.md
- MODEL: two-tier entry (default sonnet / haiku for generate-from-data simple)
- DOMAINS: [documents, generation, presentation]
- MODES: [generate-from-data, generate-from-example, run-script]
- READS: three entries listed
- WRITES: three entries listed (pptx, py script, events.jsonl)
- SKILLS: [generate-pptx.md]
- PARALLEL: YES
- DEPENDS_ON: [Document-Converter, Document-Analyst] with conditional annotation

Model routing summary table: Document-Generator row present (line 255).
Domain detection keyword row: "generate", "create presentation", "make pptx", "build slides" row present (line 276).

## Issues found
None. All checks passed. No critical bugs, no minor bugs.

## Verdict
PASSED. All SHOULD fixes from the v1 review have been applied correctly. The document-generator agent spec is complete, internally consistent, and cross-referenced correctly across all five target files. Ready for production use in pipelines.
