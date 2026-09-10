# Implementation Spec: document-generator agent

Task: software-2026-09-10-document-generator-agent
Date: 2026-09-10
Author: Analyst

---

## Overview

Create a new `document-generator` agent plus `generate-pptx` skill that generates PPTX output from structured data, from an example file + new data, or by fixing/running an existing Python script. The architecture is intentionally thin: the agent holds format-agnostic orchestration logic; all format-specific knowledge lives in skill files. Future formats (docx, xlsx) require only a new skill file — the agent stays untouched.

---

## 1. agents/document-generator.md

### Full file content to create: `C:/PROJECTS/my_claude/agents/document-generator.md`

```markdown
# Document Generator Agent

## Role
Generate output documents (PPTX, and future formats) from structured content, example files, or existing scripts.
Reads content/data prepared by prior pipeline agents. Writes final output files to `_factory/<task-id>/output/`.
Never analyse or summarise content — Document-Analyst's job. Never convert source documents — Document-Converter's job.

## Startup

**Model:** claude-sonnet-4-6 (default)
**Model:** claude-haiku-4-5 (generate-from-data mode, simple presentations only — see registry)

### On launch — always do this first
1. Read own skills: `C:/PROJECTS/my_claude/skills/generate-pptx.md`
2. Read `_factory/<task-id>/brief.md` — task-id is passed by Orchestrator
3. Read `_factory/<task-id>/events.jsonl` — identify what prior agents produced (output fields)
4. If events.jsonl has Document-Converter or Document-Analyst entries: read those output files as input

### Print on start
```
[DOC-GENERATOR] Starting. Task: <task-id>. Mode: <mode>. Input: <source description>
```

### Append to events.jsonl on start
```json
{"agent":"Document-Generator","mode":"<mode>","stage":"generate","status":"in-progress","model":"<model>","ts":"<ISO timestamp>"}
```

### Append to events.jsonl on completion
```json
{"agent":"Document-Generator","mode":"<mode>","stage":"generate","status":"done","model":"<model>","summary":"Generated <filename>. Slides: N.","output":"_factory/<task-id>/output/<filename>.pptx","ts":"<ISO timestamp>"}
```

---

## Mode: generate-from-data

### Trigger
Orchestrator sets this mode when task provides structured content (Markdown analysis results, JSON data) and requests PPTX output with no style reference.

### Input
- One or more Markdown or JSON files in `_factory/<task-id>/output/` (from Document-Analyst or Analyst)
- OR content embedded directly in brief.md under a `## CONTENT` section
- brief.md `## OUTPUT` section specifying filename, slide count preference, and any thematic instructions

### What to do
1. Read all input content files identified from events.jsonl or brief.md
2. Plan slide structure:
   - Title slide (presentation title + subtitle/date)
   - Agenda / table of contents slide (if 5+ content slides)
   - Content slides — one main idea per slide
   - Summary / key takeaways slide
   - Closing / thank you slide (if appropriate)
3. Load `skills/generate-pptx.md` and apply its layout and theme conventions
4. Write a Python script to `_factory/<task-id>/output/generate_<filename>.py` using python-pptx
5. Execute the script via Bash: `python _factory/<task-id>/output/generate_<filename>.py`
6. Verify output PPTX exists and is non-zero bytes
7. If script errors: diagnose, fix script, re-run (up to 3 attempts before escalating)

### Output
- Python script: `_factory/<task-id>/output/generate_<filename>.py`
- PPTX file: `_factory/<task-id>/output/<filename>.pptx`

### Print on finish
```
[DOC-GENERATOR] Done. Output: _factory/<task-id>/output/<filename>.pptx. Slides: N
```

---

## Mode: generate-from-example

### Trigger
Orchestrator sets this mode when an example PPTX was provided (already converted to Markdown by Document-Converter), and new data must be presented in the same style.

### Input
- Example Markdown file: `_factory/<task-id>/output/<example>.md` (produced by Document-Converter pptx-to-markdown mode)
- New data/content: Markdown or JSON file(s) in output/, or brief.md `## NEW CONTENT` section
- brief.md specifying which is the example and which is new content

### What to do
1. Read the example Markdown file — extract:
   - Number of slides and their structure pattern
   - Heading hierarchy used
   - Recurring layout patterns (title-only, title+bullets, two-column, etc.)
   - Color/theme cues if extractable from conversion notes
   - Font size patterns if mentioned in conversion notes
2. Read the new content data
3. Map new content onto the detected slide structure pattern
4. Load `skills/generate-pptx.md` and apply its layout conventions, using example patterns as overrides where detected
5. Write Python script to `_factory/<task-id>/output/generate_<filename>.py`
6. Execute via Bash, verify output, retry up to 3 times on error

### Output
- Python script: `_factory/<task-id>/output/generate_<filename>.py`
- PPTX file: `_factory/<task-id>/output/<filename>.pptx`

### Print on finish
```
[DOC-GENERATOR] Done (example-matched). Output: _factory/<task-id>/output/<filename>.pptx. Slides: N
```

---

## Mode: run-script

### Trigger
Orchestrator sets this mode when brief.md provides an existing Python python-pptx script that needs to be fixed or executed.

### Input
- Python script path from brief.md `## SCRIPT` section
- Error description from brief.md `## ERROR` section (optional — may be empty if script just needs running)

### What to do
1. Read the script file
2. If an error was provided:
   a. Diagnose root cause (import error, API misuse, missing file, bad path, data type issue)
   b. Apply fix — load `skills/generate-pptx.md` to validate fix against known pitfalls
   c. Write fixed script back to the same path (or to `_factory/<task-id>/output/fixed_<original>.py`)
3. Execute the script via Bash
4. If execution fails: diagnose, fix, re-run (up to 3 attempts)
5. Verify output PPTX exists and is non-zero bytes
6. Report what was changed in the events.jsonl summary field

### Output
- Fixed script (if applicable): `_factory/<task-id>/output/fixed_<original>.py`
- PPTX file: as defined inside the script (report actual path in events.jsonl)

### Print on finish
```
[DOC-GENERATOR] Done. Script executed. Output: <path from script>. Changes: <what was fixed or "none">
```

---

## Output conventions

- All PPTX files written to `_factory/<task-id>/output/<filename>.pptx`
- All Python scripts written to `_factory/<task-id>/output/generate_<filename>.py`
- Output filename: use value from brief.md `## OUTPUT` section; if not specified, derive from task-id
- Never overwrite input Markdown files
- Never modify source documents in brief.md SOURCE FILES section

## Script execution rules

- Always execute via: `python <script-path>`
- Check exit code; non-zero = failure, read stderr
- On failure: read error, fix the script, re-run
- Maximum 3 fix-and-retry cycles; after 3 failures append error to events.jsonl with status "failed" and stop
- Always confirm output file exists with: `ls -la <output-path>`

## Events format

Start event:
```json
{"agent":"Document-Generator","mode":"generate-from-data","stage":"generate","status":"in-progress","model":"claude-sonnet-4-6","ts":"2026-09-10T10:00:00Z"}
```

Completion event (success):
```json
{"agent":"Document-Generator","mode":"generate-from-data","stage":"generate","status":"done","model":"claude-sonnet-4-6","summary":"Generated quarterly-review.pptx. Slides: 12.","output":"_factory/task-id/output/quarterly-review.pptx","ts":"2026-09-10T10:05:00Z"}
```

Completion event (failure after retries):
```json
{"agent":"Document-Generator","mode":"run-script","stage":"generate","status":"failed","model":"claude-sonnet-4-6","summary":"Script failed after 3 attempts. Last error: <error summary>.","output":"none","ts":"2026-09-10T10:05:00Z"}
```

## Hard rules

- NEVER invent slide content not present in input data
- NEVER silently skip slides or truncate content — if content does not fit, split across slides
- ALWAYS read `skills/generate-pptx.md` before writing any python-pptx script
- ALWAYS verify PPTX output file exists before reporting done
- ALWAYS write a runnable Python script as an intermediate artifact (not just inline code)
- Do NOT print full script content to terminal — print only path confirmation and slide count
- Do NOT modify source input files — output only to `_factory/<task-id>/output/`
```

---

## 2. skills/generate-pptx.md

### Full file content to create: `C:/PROJECTS/my_claude/skills/generate-pptx.md`

```markdown
# Skill: Generate PPTX with python-pptx

Domain knowledge for Document-Generator agent.
Read this file before writing any python-pptx script.

---

## Library setup

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.dml import MSO_THEME_COLOR
```

Install check (include at top of generated scripts):
```python
try:
    from pptx import Presentation
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-pptx"])
    from pptx import Presentation
```

---

## Creating a presentation

```python
prs = Presentation()
# Standard widescreen slide size (16:9)
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
```

Always set explicit slide dimensions. Default is 10x7.5 (4:3); use 13.333x7.5 for modern 16:9.

---

## Slide layouts

python-pptx ships with a default theme containing numbered layouts. Map by index:

| Index | Layout name         | Use for                                    |
|-------|---------------------|--------------------------------------------|
| 0     | Title Slide         | First slide — large title + subtitle       |
| 1     | Title and Content   | Standard content slide — title + body      |
| 2     | Title Only          | Slide with title, free-positioned content  |
| 5     | Blank               | Full control — no placeholders             |
| 6     | Title and Two Content | Two-column layout                        |

Access layout:
```python
slide_layout = prs.slide_layouts[1]   # Title and Content
slide = prs.slides.add_slide(slide_layout)
```

Prefer indexed layouts over named lookup — names vary between pptx themes.

---

## Placeholder access

```python
# For layout 1 (Title and Content):
title_ph   = slide.placeholders[0]   # title
content_ph = slide.placeholders[1]   # body / content

title_ph.text = "Slide Title"

# Add bulleted text to content placeholder
tf = content_ph.text_frame
tf.text = "First bullet point"         # sets first paragraph
p = tf.add_paragraph()
p.text = "Second bullet"
p.level = 0                            # 0 = top level
p2 = tf.add_paragraph()
p2.text = "Sub-bullet"
p2.level = 1                           # 1 = indented
```

---

## Title slide (layout 0)

```python
slide = prs.slides.add_slide(prs.slide_layouts[0])
title    = slide.placeholders[0]
subtitle = slide.placeholders[1]
title.text    = "Presentation Title"
subtitle.text = "Subtitle — Date"
```

---

## Blank slide with free-positioned text box

Use layout 5 (Blank) when you need full positional control:

```python
slide = prs.slides.add_slide(prs.slide_layouts[5])
left  = Inches(1)
top   = Inches(2)
width = Inches(8)
height= Inches(1.5)
txBox = slide.shapes.add_textbox(left, top, width, height)
tf    = txBox.text_frame
tf.word_wrap = True
tf.text = "Free-positioned text"
```

---

## Two-column layout

Preferred approach: use layout 6 if available in theme, otherwise simulate with two text boxes on a blank slide.

```python
# Simulation with two text boxes on blank slide
slide = prs.slides.add_slide(prs.slide_layouts[5])

# Left column
left_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(5.5), Inches(5))
left_box.text_frame.word_wrap = True
left_box.text_frame.text = "Left column content"

# Right column
right_box = slide.shapes.add_textbox(Inches(7.0), Inches(1.5), Inches(5.5), Inches(5))
right_box.text_frame.word_wrap = True
right_box.text_frame.text = "Right column content"
```

---

## Font conventions

```python
from pptx.util import Pt
from pptx.dml.color import RGBColor

run = paragraph.runs[0]          # or add_run()
run.font.name  = "Calibri"       # default body font
run.font.size  = Pt(18)
run.font.bold  = True
run.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)   # dark blue
```

Recommended sizes:
| Element            | Size  |
|--------------------|-------|
| Title (slide)      | 36–44pt |
| Slide title        | 28–32pt |
| Body / bullet L0   | 20–24pt |
| Bullet L1          | 18–20pt |
| Bullet L2          | 16–18pt |
| Caption / footnote | 12–14pt |

Standard fonts (universally safe): Calibri, Arial, Helvetica, Times New Roman.

---

## Theme color conventions (business presentations)

Default palette for generated presentations (override if example file provides cues):

| Role              | Hex       | Usage                          |
|-------------------|-----------|--------------------------------|
| Primary dark      | #1F497D   | Title text, headings           |
| Primary mid       | #2E75B6   | Accent shapes, dividers        |
| Primary light     | #BDD7EE   | Background shapes, highlights  |
| Text body         | #404040   | Body text                      |
| Background        | #FFFFFF   | Slide background               |
| Accent warm       | #ED7D31   | Call-out boxes, emphasis       |

Apply background color to title slide:
```python
from pptx.dml.color import RGBColor
from pptx.util import Emu

background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = RGBColor(0x1F, 0x49, 0x7D)   # dark blue title slide
```

For content slides: white background, colored title text.

---

## Images

```python
from pptx.util import Inches

# Add image from file
pic = slide.shapes.add_picture(
    image_file="path/to/image.png",
    left=Inches(1),
    top=Inches(2),
    width=Inches(4),    # omit height to auto-scale proportionally
)
```

If image file is not available (e.g., was an `![image-N: description]` placeholder):
- Insert a styled rectangle placeholder with the image description as text
- Use a light grey fill: RGBColor(0xD9, 0xD9, 0xD9)
- Add italic caption: "[ Image: <description> ]"

```python
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

ph = slide.shapes.add_shape(
    MSO_SHAPE_TYPE.RECTANGLE if False else 1,   # use freeform rectangle: MSO_CONNECTOR_TYPE = 1 is wrong; use add_shape
    Inches(1), Inches(2), Inches(4), Inches(3)
)
ph.fill.solid()
ph.fill.fore_color.rgb = RGBColor(0xD9, 0xD9, 0xD9)
ph.text_frame.text = "[ Image: description ]"
ph.text_frame.paragraphs[0].runs[0].font.italic = True
ph.text_frame.paragraphs[0].runs[0].font.size = Pt(14)
```

Correct shape insertion:
```python
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Inches

# Add a rectangle as image placeholder
slide.shapes.add_shape(
    1,               # MSO_SHAPE.RECTANGLE = 1
    Inches(1), Inches(2), Inches(4), Inches(3)
)
```

---

## Typical business presentation structure

| Slide # | Layout         | Content                                              |
|---------|----------------|------------------------------------------------------|
| 1       | Title Slide    | Title, subtitle, author, date                        |
| 2       | Title+Content  | Agenda / Table of Contents (bulleted list)           |
| 3–N-2   | Title+Content  | One main topic per slide; 4–6 bullets max per slide  |
| N-1     | Title+Content  | Key Takeaways / Summary (3–5 bullets)                |
| N       | Blank or Title | Thank you / Contact / Next Steps                     |

Rules:
- One idea per slide — do not overload
- Max 6 bullet points per content slide; split into 2 slides if more
- Max 3 levels of indentation; prefer 1–2
- Every content slide must have a title
- Agenda slide must list every section heading (not every individual slide)

---

## Saving

```python
import os
output_path = "_factory/<task-id>/output/<filename>.pptx"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
prs.save(output_path)
print(f"Saved: {output_path}")
```

Always use `os.makedirs(..., exist_ok=True)` before saving.
Always print the output path so the agent can parse it from stdout.

---

## Common pitfalls

| Pitfall                                     | Fix                                                                    |
|---------------------------------------------|------------------------------------------------------------------------|
| `KeyError` on placeholder index             | Inspect layout placeholders: `[ph.placeholder_format.idx for ph in slide.placeholders]` |
| Placeholder not found in layout             | Use layout 5 (Blank) + add_textbox() instead                           |
| Text overflows slide                        | Reduce font size or split into two slides                              |
| `AttributeError: 'NoneType'` on text_frame  | Placeholder exists but has no text_frame — use shape.text_frame directly |
| Image file not found                        | Check path; use absolute path; fall back to grey rectangle placeholder  |
| `ImportError: No module named pptx`         | Add pip install guard at script top (see Library setup section)         |
| RGBColor takes ints 0–255, not hex strings  | `RGBColor(0x1F, 0x49, 0x7D)` — pass int literals, not strings          |
| Slide dimensions not set → 4:3 output      | Always set `prs.slide_width` and `prs.slide_height` explicitly          |
| `add_shape` with wrong shape type int       | Use `1` for rectangle; import `MSO_SHAPE_TYPE` for reference            |

---

## Placeholder index inspection (debug helper)

Include this as a commented block in generated scripts for debugging:
```python
# Debug: print placeholder indices for each layout
# for i, layout in enumerate(prs.slide_layouts):
#     print(f"Layout {i}: {layout.name}")
#     for ph in layout.placeholders:
#         print(f"  idx={ph.placeholder_format.idx} name={ph.name}")
```
```

---

## 3. agents/_registry.md — new entry to add

### Location
Append the following block after the `### DOCUMENT-ANALYST` entry (after line 217), before the `---` separator that leads into the "Model routing summary" section.

### Block to insert

```
### DOCUMENT-GENERATOR
```
AGENT:       Document-Generator
FILE:        C:/PROJECTS/my_claude/agents/document-generator.md
MODEL:
  default (generate-from-example, run-script): claude-sonnet-4-6
  generate-from-data (simple):                 claude-haiku-4-5
DOMAINS:     [documents, generation, presentation]
MODES:       [generate-from-data, generate-from-example, run-script]
READS:       _factory/<task-id>/brief.md
             _factory/<task-id>/events.jsonl
             _factory/<task-id>/output/ (converter/analyst output, if prior agents ran)
WRITES:      _factory/<task-id>/output/<filename>.pptx
             _factory/<task-id>/output/generate_<filename>.py
             _factory/<task-id>/events.jsonl (appends)
SKILLS:      [generate-pptx.md]
PARALLEL:    YES
DEPENDS_ON:  [Document-Converter, Document-Analyst]  ← only when conversion/analysis ran first; otherwise []
```
```

### Model routing table row to add

In the `## Model routing summary` table (after the Document-Analyst row), add:

```
| Document-Generator  | claude-sonnet-4-6   | generate-from-data (simple)                        |
```

### Domain detection rule to add

In `## Domain detection rules` table, add:

```
| Keywords: "generate", "create presentation", "make pptx", "build slides" | `documents` |
```

---

## 4. AGENTS.md — exact lines to add

### Agents section (after `document-analyst.md` line)

Add this line:
```
- document-generator.md — generates PPTX from structured data, example files, or existing scripts [Sonnet]
```

### Skills section (after `documents.md` line)

Add this line:
```
- generate-pptx.md      — python-pptx patterns: slide layouts, themes, fonts, images, common pitfalls
```

### Domain detection rules table (in `## How the factory works` section)

The existing bullet:
```
  .pdf / .pptx / .docx in task  →  documents pipeline
```

should remain unchanged (file extension detection already covers PPTX input). No change needed there.

Add to the keywords line (or as a new bullet if cleaner):
```
  "generate", "create presentation", "make pptx", "build slides"  →  documents pipeline
```

### Documents pipeline description update

Extend the existing Documents pipeline description to include generation:

Current:
```
  Documents pipeline:
    Convert only:   Document-Converter (parallelizable per file)
    Convert + analyse: Document-Converter → Document-Analyst
    Analyse only:   Document-Analyst (no conversion)
```

Updated (add these lines):
```
    Generate only:  Document-Generator (from data or script)
    Convert + generate: Document-Converter → Document-Generator (generate-from-example)
    Convert + analyse + generate: Document-Converter → Document-Analyst → Document-Generator
```

---

## 5. README.md — exact lines to add

### Agents section (after `document-analyst.md` line, around line 95)

Add this line:
```
- document-generator.md — generates PPTX from structured data, example files, or scripts [Sonnet]
```

### Skills section (after `documents.md` line, around line 109)

Add this line:
```
- generate-pptx.md      — python-pptx patterns: slide layouts, themes, fonts, images, pitfalls
```

### Model routing table (after Document-Analyst row, around line 72)

Add this row:
```
| Document-Generator  | claude-sonnet-4-6  | generate-from-data (simple)              |
```

### Domain detection section (in `## How the factory works`, around line 37)

Add the generation keywords to the domain detection block:
```
    "generate", "create presentation", "build slides"  →  documents pipeline
```

### Documents pipeline section (in `## How the factory works`, around line 49)

Extend to:
```
    Generate only:  Document-Generator (generate-from-data or run-script)
    Convert + generate: Document-Converter → Document-Generator (generate-from-example)
    Convert + analyse + generate: Document-Converter → Document-Analyst → Document-Generator
```

---

## Assumptions

1. python-pptx is available (or installable via pip) in the execution environment. The generated script includes an auto-install guard.
2. The Orchestrator already handles the documents pipeline domain detection. The new agent slots into an existing pipeline concept — no new pipeline type is needed.
3. "Simple generate" (haiku mode) means structured data with no style matching — straightforward templated slides. Any style-matching from an example file requires sonnet.
4. The `generate-from-example` mode always assumes Document-Converter ran first and produced a Markdown file. If no Markdown exists, the agent should log a warning and fall back to `generate-from-data` behavior.
5. No acceptance.md is required for this task (personal development, no QA agent in the pipeline).

## Risks

1. python-pptx placeholder indexing varies between themes. The skill file documents the debug helper and fallback approach (blank slide + textbox).
2. Content volume mismatch: input data may be much larger or smaller than expected slide count. Agent must enforce the 6-bullets-per-slide rule and split proactively.
3. Image placeholders from Markdown conversion will almost always be unavailable as real image files. Agent must use the grey rectangle fallback consistently.
