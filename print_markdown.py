#!/usr/bin/env python3
"""
Simple Markdown to PDF converter with automatic page breaks at '---'

Usage:
    python print_markdown.py input.md output.pdf
    python print_markdown.py input.md  # Creates input.pdf in same directory

This script converts markdown to PDF, treating '---' as page breaks.
Perfect for printing front/back pages for spiral-bound cookbook.
"""

import sys
import os
from pathlib import Path

try:
    import markdown
    from weasyprint import HTML, CSS
except ImportError:
    print("ERROR: Missing dependencies. Install with:")
    print("  pip install markdown weasyprint")
    sys.exit(1)


def markdown_to_pdf(input_file, output_file=None):
    """Convert markdown to PDF with page breaks at '---'"""
    
    # Read markdown file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace '---' with page break marker
    # We'll use a special HTML comment that weasyprint can handle
    content = content.replace('\n---\n', '\n<div style="page-break-after: always;"></div>\n')
    content = content.replace('\n---', '\n<div style="page-break-after: always;"></div>\n')
    
    # Also handle <!-- PAGE_BREAK --> if present
    content = content.replace('<!-- PAGE_BREAK -->', '<div style="page-break-after: always;"></div>')
    
    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['extra', 'codehilite'])
    html_content = md.convert(content)
    
    # Add basic styling for print
    html_document = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{
                size: letter;
                margin: 0.75in;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                line-height: 1.6;
                color: #000;
            }}
            h1 {{
                font-size: 24pt;
                margin-top: 0;
                page-break-after: avoid;
            }}
            h2 {{
                font-size: 18pt;
                page-break-after: avoid;
            }}
            h3 {{
                font-size: 14pt;
                page-break-after: avoid;
            }}
            /* Prevent orphaned lines */
            p, li {{
                orphans: 3;
                widows: 3;
            }}
            /* Keep checkboxes visible */
            input[type="checkbox"] {{
                width: 16px;
                height: 16px;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Convert to PDF
    HTML(string=html_document).write_pdf(output_file)
    print(f"✓ Created: {output_file}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"ERROR: File not found: {input_file}")
        sys.exit(1)
    
    # Determine output file
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        # Use same name as input, but with .pdf extension
        output_file = str(Path(input_file).with_suffix('.pdf'))
    
    markdown_to_pdf(input_file, output_file)


if __name__ == '__main__':
    main()
