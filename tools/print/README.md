# Print Tooling

This directory contains the **print compiler** tooling.

## Goal
Generate a **single print-friendly bundle** (plus optional HTML/PDF) into `05_print/` where:
- Cross-references like `04_reference/glossary.md` become **book-style references** (human title + page number).
- Page numbers are computed **automatically** at render time using CSS `target-counter()`.

## Usage

```bash
python3 tools/print/compile_print_bundle.py
```

### Output
Creates files in `05_print/`:
- `05_print/compiled_manual.md`
- `05_print/compiled_manual.html` (if `markdown` is installed)
- `05_print/compiled_manual.pdf` (if `weasyprint` is installed)

## Notes
- This does **not** replace `tools/print/print_markdown.py` (which is still useful for printing a single recipe).
- This is intended for compiling the whole cookbook into a binder-ready bundle.

