#!/bin/bash
# Print all recipes to PDF with automatic page breaks at '---'
# Outputs to 05_print/ directory

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRINT_DIR="$SCRIPT_DIR/05_print"
RECIPES_DIR="$SCRIPT_DIR/03_recipes"

# Create print directory if it doesn't exist
mkdir -p "$PRINT_DIR"

# Check if Python script exists
if [ ! -f "$SCRIPT_DIR/tools/print/print_markdown.py" ]; then
    echo "ERROR: print_markdown.py not found"
    exit 1
fi

# Activate venv if it exists
if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
fi

echo "Converting recipes to PDF..."
echo ""

# Also create the whole-project print bundle (optional, print-friendly compilation)
if [ -f "$SCRIPT_DIR/tools/print/compile_print_bundle.py" ]; then
    echo "Compiling full cookbook print bundle..."
    python3 "$SCRIPT_DIR/tools/print/compile_print_bundle.py" || true
    echo ""
fi

# Convert each recipe
for recipe in "$RECIPES_DIR"/*.md; do
    if [ -f "$recipe" ]; then
        filename=$(basename "$recipe" .md)
        output="$PRINT_DIR/${filename}.pdf"
        echo "Processing: $filename"
        python3 "$SCRIPT_DIR/tools/print/print_markdown.py" "$recipe" "$output"
    fi
done

echo ""
echo "✓ All recipes converted to PDF in $PRINT_DIR"
echo ""
echo "To print:"
echo "  - Open PDFs in your PDF viewer"
echo "  - Print with 'Print on both sides' option"
echo "  - Or print single-sided and manually flip for back pages"
