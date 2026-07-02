# Document Processing Skills

Domain knowledge for Document-Converter and Document-Analyst agents.
Always read this file before processing any document.

---

## Markdown output conventions

### Heading hierarchy
- Use `#` for document title only
- `##` for top-level sections (chapters, major parts)
- `###` for subsections
- `####` for sub-subsections — avoid going deeper
- Never skip levels (no `##` directly under `#` if there's content between them)

### Slide decks (PPTX / Keynote)
- Each slide becomes a `##` section
- Slide title is the heading text; if no title: `## Slide N`
- Slide body content follows as bullet list or prose
- Speaker notes (if present) become a `> **Notes:** ...` blockquote immediately after the slide content
- Slide numbers are preserved in headings: `## Slide 3: Market Analysis`

### Tables
- Convert to GitHub-flavored Markdown tables
- Preserve all columns and rows
- If a cell spans multiple rows/columns: split into separate rows with repeated values and add `> CONVERSION NOTE: original cell spanned N rows`
- If a table is too wide: keep it and note width issue rather than truncating columns
- Empty cells render as blank (single space in the cell)

### Lists
- Ordered lists: use `1.` numbering
- Unordered lists: use `-`
- Preserve nesting level (indent 2 spaces per level)
- Do NOT flatten nested lists to prose

### Images and diagrams
- Replace with placeholder: `![image-N: <caption or alt text if detectable>]`
- If image contains text (screenshot, diagram with labels): extract visible text as a code block after the placeholder
- Number images sequentially within the document: image-1, image-2, …

### Code blocks
- Preserve any code snippets in fenced blocks with language hint if detectable
- Command examples: use `bash` or `shell` as language hint

### Hyperlinks
- Preserve as `[link text](url)` if URL is detectable
- If only link text visible (printed PDF): `[link text]()` with empty URL

---

## Conversion quality markers

Use these markers when something cannot be converted cleanly. Always on its own line:

```
> CONVERSION NOTE: <description of what could not be cleanly converted>
```

Use for:
- Merged/complex table cells
- Rotated or sideways text
- Embedded charts (describe what the chart shows if labels are visible)
- Decorative formatting with no semantic meaning
- Content that appears corrupt or unreadable

---

## Citation format

When Document-Analyst references source content:

Single source:
```
Source: <filename>, Section: <heading>
```

Multiple sources:
```
Sources:
- <filename>, Section: <heading>
- <filename>, Section: <heading>
```

Rule: every claim in analysis output must have a citation. Never invent content not present in source.

---

## Summary output patterns

### Executive summary
Structure:
1. **Purpose** — what this document is about (1 sentence)
2. **Key findings** — 3–5 bullet points, most important first
3. **Recommendations** (if present in source)
4. **Open questions** — unclear or missing information flagged

### Key point extraction
- Extract points that are stated as conclusions, recommendations, or decisions
- Distinguish explicit statements from implicit ones
- Flag where the document is ambiguous: `> AMBIGUITY: ...`

### Structure extraction
Map document as:
```
# Document Title
## Section 1: <heading>
   ### Subsection 1.1
   Tables: N
   Lists: N
   Images: N
## Section 2: <heading>
...
```

---

## Document comparison

When comparing 2+ documents:
- Organize by topic, not by document order
- Three categories per topic: **Shared** / **Document A only** / **Document B only**
- Flag direct contradictions: `> CONTRADICTION: Doc A says X, Doc B says Y`
- Note version or date differences if detectable

---

## Gap and ambiguity reporting

Always flag at end of output:
```
## Gaps and ambiguities
- <what was unclear or missing in the source>
```

If no gaps: `## Gaps and ambiguities\nNone detected.`

---

## Tool availability for file reading

| Format | How to read |
|--------|-------------|
| PDF    | Use `Read` tool directly — Claude Code reads PDF natively |
| PPTX   | Use `Read` tool — Claude Code reads PPTX natively |
| DOCX   | Use `Read` tool — Claude Code reads DOCX natively |
| XLSX   | Use `Read` tool — Claude Code reads XLSX natively |
| Images | Use `Read` tool — Claude Code reads images visually |

If `Read` tool fails on a binary format, fall back to Bash:
```bash
# Extract text from PDF
python -c "import pdfplumber; pdf=pdfplumber.open('file.pdf'); [print(p.extract_text()) for p in pdf.pages]"
# or
pdftotext file.pdf -
```

Always note the extraction method used in the conversion output.
