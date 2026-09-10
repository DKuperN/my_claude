# Skill: Generate PPTX with python-pptx

Domain knowledge for Document-Generator agent.
Read this file before writing any python-pptx script.

---

## Library setup

Core imports (include in every generated script):
```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
```

Optional imports (add only when needed):
```python
from pptx.util import Emu            # when working with EMU units directly
from pptx.enum.text import PP_ALIGN  # when setting paragraph alignment
from pptx.enum.dml import MSO_THEME_COLOR  # when referencing theme colors by name
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

# add_shape takes an integer shape type: 1 = rectangle (MSO_SHAPE_TYPE.RECTANGLE)
ph = slide.shapes.add_shape(
    1,
    Inches(1), Inches(2), Inches(4), Inches(3)
)
ph.fill.solid()
ph.fill.fore_color.rgb = RGBColor(0xD9, 0xD9, 0xD9)
ph.text_frame.text = "[ Image: description ]"
ph.text_frame.paragraphs[0].runs[0].font.italic = True
ph.text_frame.paragraphs[0].runs[0].font.size = Pt(14)
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
