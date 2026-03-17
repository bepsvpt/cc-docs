# Claude Code Documentation PDF Generator

This project converts the official Claude Code documentation from code.claude.com into professionally
formatted A5 PDF e-books suitable for e-readers or printing. It supports both English and Traditional
Chinese (zh-TW).

## Pipeline Overview

The pipeline has three steps, each handled by a Python script in `scripts/`:

1. **Download** (`download_md.py`) — Fetches all markdown doc pages from the Claude Code website
2. **Merge** (`merge_docs.py`) — Combines individual pages into a single structured markdown document with 13 parts
3. **Generate PDF** (`generate_pdf.py`) — Converts the merged markdown to a styled A5 PDF via Pandoc + WeasyPrint

Each script accepts `--lang en` (default) or `--lang zh-TW` and `--basedir <path>` to control where
intermediate and output files are stored.

## How to Use

### Setup

Fonts are bundled in `assets/fonts/` and referenced directly — no font installation needed.

The `generate_pdf.py` script checks for required dependencies (`pandoc`, `weasyprint`, `pypdf`)
on startup and prints exact install commands if anything is missing. If it fails, just run
the printed command and retry.

### Generate PDFs

From the project root, using `make`:

```bash
make                # Build both languages
make LANG=en        # Build English only
make LANG=zh-TW     # Build Traditional Chinese only
make clean          # Remove all build artifacts
```

Individual pipeline steps (same `LANG` parameter):

```bash
make download       # Fetch docs from code.claude.com
make merge          # Combine into single markdown
make pdf            # Generate PDF from merged markdown
```

Or run the scripts directly:

```bash
python3 scripts/download_md.py --basedir .
python3 scripts/merge_docs.py --basedir .
python3 scripts/generate_pdf.py --basedir .
# Add --lang zh-TW for Traditional Chinese
```

### Output Files

- `claude_code_documentation.pdf` — English version (~795 pages, ~5 MB, A5)
- `claude_code_documentation_zh_tw.pdf` — Traditional Chinese version (~682 pages, ~5 MB, A5)

Output PDFs are saved to `output/` by default.

### Refresh Docs

To update when docs change, simply re-run the pipeline. The download script skips files that already
exist unless you pass `--force` to re-download everything.

## Architecture Details

### Download (`download_md.py`)
- Fetches from `https://code.claude.com/docs/{lang}/{slug}.md`
- Supports 12 languages: de, en, es, fr, id, it, ja, ko, pt, ru, zh-CN, zh-TW
- 64 English pages, 59 pages per translated language (5 English-only: commands, tools-reference, env-vars, authentication, changelog)
- Also downloads images referenced in docs to `docs/images/`

### Merge (`merge_docs.py`)
- Organizes docs into 13 thematic parts (Getting Started, Core Usage, Commands & Reference, etc.)
- Handles Mintlify/MDX components: `<Steps>`, `<Tab>`, `<Card>`, `<Note>`, `<Warning>`, etc.
- Strips JSX components and injects static MCP servers table for the `mcp.md` page
- Resolves internal doc links to PDF anchors
- Manages code block deindenting from nested MDX

### Generate PDF (`generate_pdf.py`)
- Splits merged markdown into sections, converts each to HTML via Pandoc (avoids OOM)
- Assembles full HTML with CSS styling and cover page
- Renders to PDF with WeasyPrint
- Key styling features:
  - A5 page size with 15mm/12mm/18mm/12mm margins
  - Amber (#D97706) accent color for headings and borders
  - Tango syntax highlighting for code blocks
  - Callout boxes for Note/Info/Tip/Warning
  - Emoji support via `@font-face` with `unicode-range` restriction
  - CJK font (Noto Sans CJK TC, regular + bold) for zh-TW
  - JetBrains Mono (regular + bold) bundled via `@font-face` — required to prevent WeasyPrint tofu in code blocks when CJK `@font-face` is combined with `@page { size: ... }`
  - Fixed-width table columns for 3/4/5-column tables
  - Image max-height constraint (180mm) to prevent page overflow

### Transform pipeline ordering (`md_transforms.py`)
- Image validation (`handle_md_img`) MUST run before `resolve_links` — the link regex also matches image syntax
- Code spans (inline backticks + fenced blocks) are extracted into NUL-byte placeholders before JSX/HTML/link transforms, then restored before `dedent_blocks` — prevents `<tag>` patterns inside code from being stripped
- Pipeline: `strip_metadata` → `protect_code_spans` → `convert_jsx_components` → `clean_html_tags` → `resolve_links` → `restore_code_spans` → `dedent_blocks` → `finalize`
