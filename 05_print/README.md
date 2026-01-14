# 05_print/

This folder is for **generated, print-ready outputs**.

## Recommended workflow

1. Compile the full cookbook bundle:

```bash
python3 tools/print/compile_print_bundle.py
```

2. Print the generated outputs:
- `compiled_manual.html` → print from browser (easy)
- `compiled_manual.pdf` → print from PDF viewer (best)

## Notes
- This repo does **not** commit generated PDFs by default.
- Cross-references inside the print bundle show **page numbers automatically** when rendered to PDF (CSS `target-counter()`).

