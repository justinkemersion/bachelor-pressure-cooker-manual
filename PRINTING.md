# Printing Your Cookbook

## Quick Answer: Print with Page Breaks at `---`

**The simplest method:** Use your browser's print function with CSS page breaks.

### Browser Print Method (No Software Needed)

1. **Open your markdown file** in a markdown viewer (VS Code preview, GitHub, or any markdown viewer)
2. **Print to PDF** (Ctrl+P / Cmd+P)
3. **In print settings:** Enable "Print on both sides" or "Duplex"
4. **The `---` separators** will naturally create page breaks when printing

**Note:** Most markdown viewers treat `---` as horizontal rules, which browsers automatically page-break at when printing.

---

## Automated Solutions

### Option 1: Simple Script (Pandoc or Browser)

```bash
./print_simple.sh 03_recipes/chipotle_burrito_bowl.md
```

**What it does:**
- If you have `pandoc`: Converts directly to PDF with page breaks at `---`
- If not: Creates an HTML file you can print from your browser

**Install pandoc (optional):**
```bash
# Arch Linux
sudo pacman -S pandoc

# Ubuntu/Debian
sudo apt install pandoc

# macOS
brew install pandoc
```

### Option 2: Python Script (More Control)

```bash
# Install dependencies first
pip install markdown weasyprint

# Convert single file
python tools/print/print_markdown.py 03_recipes/chipotle_burrito_bowl.md

# Or convert all recipes
./print_all.sh
```

**Output:** PDFs in `05_print/` directory

---

## Whole-Project Print Bundle (Recommended)

If you want a **binder-ready compilation** (with cross-references that show **page numbers** like a real book), use:

```bash
python3 tools/print/compile_print_bundle.py
```

**What it does:**
- Combines the cookbook into a single bundle in `05_print/`
- Rewrites repo-style references like `04_reference/glossary.md` into internal links
- When printed to PDF, links automatically display **(p. X)** using CSS `target-counter()`

**Outputs:**
- `05_print/compiled_manual.md`
- `05_print/compiled_manual.html` (if `markdown` is installed)
- `05_print/compiled_manual.pdf` (if `weasyprint` is installed)

---

## Print Settings for Spiral Binding

### Recommended Settings:
- **Paper Size:** Letter (8.5" x 11")
- **Print on Both Sides:** Yes (Duplex)
- **Margins:** 0.75" (for spiral binding)
- **Orientation:** Portrait

### Double-Sided Printing Strategy:
1. **Print odd pages first** (1, 3, 5, 7...)
2. **Flip stack, reinsert**
3. **Print even pages** (2, 4, 6, 8...)

**Or use your printer's "Print on both sides" feature** - it handles this automatically.

---

## Page Break Markers

Your markdown files use two types of page break markers:

1. **`---`** (three dashes) - Treated as page break when printing
2. **`<!-- PAGE_BREAK -->`** - Also treated as page break

Both work the same way - they tell the printer to start a new page.

---

## Troubleshooting

### "Page breaks not working"
- Make sure you're using `---` on its own line (not `---` in the middle of text)
- Try the browser print method first (simplest)
- Check that your PDF viewer respects page breaks

### "Text too small"
- Adjust browser zoom before printing (Ctrl/Cmd + Plus)
- Or edit the CSS in `print_simple.sh` to increase font sizes

### "Margins wrong for spiral binding"
- Most printers default to 0.5" margins
- You may need to set custom margins: 0.75" all around
- Check your printer's "Advanced" or "Layout" settings

---

## Quick Reference

| Method | Ease | Requirements | Best For |
| :--- | :--- | :--- | :--- |
| **Browser Print** | ⭐⭐⭐⭐⭐ | None | Quick single-file prints |
| **print_simple.sh** | ⭐⭐⭐⭐ | Pandoc (optional) | Automated conversion |
| **tools/print/print_markdown.py** | ⭐⭐⭐ | Python + weasyprint | Batch processing |

---

**Pro Tip:** For the best results, print a test page first to check margins and page breaks before printing the whole cookbook.
