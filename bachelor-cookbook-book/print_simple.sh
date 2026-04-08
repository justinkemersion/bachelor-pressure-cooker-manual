#!/bin/bash
# Simple print script using pandoc (if available) or browser
# Converts markdown to HTML/PDF with page breaks at '---'

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_FILE="${1:-}"

if [ -z "$INPUT_FILE" ]; then
    echo "Usage: ./print_simple.sh <markdown_file>"
    echo ""
    echo "This script converts markdown to PDF with page breaks at '---'"
    echo ""
    echo "Options:"
    echo "  1. If pandoc is installed: Uses pandoc with CSS page breaks"
    echo "  2. If not: Creates HTML file you can print from browser"
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "ERROR: File not found: $INPUT_FILE"
    exit 1
fi

OUTPUT_BASE="${INPUT_FILE%.md}"
OUTPUT_HTML="${OUTPUT_BASE}.html"
OUTPUT_PDF="${OUTPUT_BASE}.pdf"

# Check if pandoc is available
if command -v pandoc &> /dev/null; then
    echo "Using pandoc to convert to PDF..."
    
    # Create temporary CSS for page breaks
    CSS_FILE=$(mktemp)
    cat > "$CSS_FILE" << 'EOF'
@page {
    size: letter;
    margin: 0.75in;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.6;
    color: #000;
}
h1 { font-size: 24pt; page-break-after: avoid; }
h2 { font-size: 18pt; page-break-after: avoid; }
h3 { font-size: 14pt; page-break-after: avoid; }
/* Page break at horizontal rules */
hr {
    page-break-after: always;
    border: none;
    margin: 0;
    height: 0;
}
EOF
    
    # Convert markdown to PDF
    # Replace '---' with HTML horizontal rule for page breaks
    sed 's/^---$/---/' "$INPUT_FILE" | \
    pandoc -f markdown -t pdf \
        --css="$CSS_FILE" \
        --standalone \
        --highlight-style=pygments \
        -o "$OUTPUT_PDF"
    
    rm "$CSS_FILE"
    echo "✓ Created: $OUTPUT_PDF"
    echo ""
    echo "To print: Open PDF and print with 'Print on both sides' option"
    
else
    echo "Pandoc not found. Creating HTML file for browser printing..."
    echo ""
    
    # Create HTML with page break CSS
    cat > "$OUTPUT_HTML" << 'EOHTML'
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Print Preview</title>
    <style>
        @media print {
            @page {
                size: letter;
                margin: 0.75in;
            }
            /* Page break at horizontal rules */
            hr {
                page-break-after: always;
                border: none;
                margin: 0;
                height: 0;
            }
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            color: #000;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 20px;
        }
        h1 { font-size: 24pt; }
        h2 { font-size: 18pt; }
        h3 { font-size: 14pt; }
        hr {
            border: none;
            border-top: 2px solid #ccc;
            margin: 20px 0;
        }
    </style>
</head>
<body>
EOHTML
    
    # Convert markdown to HTML (simple conversion)
    # Replace '---' with <hr> for visual page breaks
    sed 's/^---$/<hr>/' "$INPUT_FILE" | \
    sed 's/<!-- PAGE_BREAK -->/<hr>/' | \
    python3 -c "
import sys
import re

content = sys.stdin.read()
# Simple markdown to HTML conversion
content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
content = re.sub(r'^- \[ \] (.+)$', r'<input type=\"checkbox\"> \1<br>', content, flags=re.MULTILINE)
content = re.sub(r'^- (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
content = re.sub(r'\n\n', r'</p><p>', content)
print(content)
" >> "$OUTPUT_HTML"
    
    echo "</body></html>" >> "$OUTPUT_HTML"
    
    echo "✓ Created: $OUTPUT_HTML"
    echo ""
    echo "To print:"
    echo "  1. Open $OUTPUT_HTML in your browser"
    echo "  2. Press Ctrl+P (or Cmd+P on Mac)"
    echo "  3. In print dialog, enable 'Print on both sides' or 'Duplex'"
    echo "  4. The browser will automatically page break at '---' markers"
fi
