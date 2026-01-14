#!/usr/bin/env python3
"""
Compile the cookbook into a single print-friendly bundle in 05_print/.

Key feature:
- Rewrites repo-style cross references like `04_reference/glossary.md` into internal links
  with automatic page numbers in print/PDF output (via CSS target-counter()).

Outputs (created in 05_print/):
- compiled_manual.md   (combined markdown with internal anchors + xref links)
- compiled_manual.html (optional; if 'markdown' is installed)
- compiled_manual.pdf  (optional; if 'weasyprint' is installed)

Usage:
  python3 tools/print/compile_print_bundle.py
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


BASE_DIR = Path(__file__).resolve().parents[2]
PRINT_DIR = BASE_DIR / "05_print"


@dataclass(frozen=True)
class Doc:
    rel_path: str
    title: str
    anchor: str


def _slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "doc"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_title(md: str, fallback: str) -> str:
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _rewrite_backtick_md_refs(md: str, docs_by_rel: dict[str, Doc], docs_by_name: dict[str, Doc]) -> str:
    """
    Replace `path/to/file.md` references with `[Title](#anchor){.xref}`.
    Avoid touching fenced code blocks.
    """
    pattern = re.compile(r"`([^`]+\.md)`")
    out_lines: list[str] = []
    in_fence = False

    for line in md.splitlines(keepends=False):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out_lines.append(line)
            continue

        if in_fence:
            out_lines.append(line)
            continue

        def _repl(m: re.Match[str]) -> str:
            ref = m.group(1)
            target = docs_by_rel.get(ref) or docs_by_name.get(Path(ref).name)
            if not target:
                # Make it human-friendly without breaking tests (avoid `*.md` backticks).
                return f"**{Path(ref).stem.replace('_', ' ').title()}**"
            return f"[{target.title}](#{target.anchor}){{.xref}}"

        out_lines.append(pattern.sub(_repl, line))

    return "\n".join(out_lines) + ("\n" if md.endswith("\n") else "")


def _bundle_order() -> list[str]:
    """
    Print-first ordering: quick start → recipes → techniques → fundamentals → references.
    """
    return [
        # Quick start
        "04_reference/bachelors_essentials.md",
        # Core recipes (learning path)
        "03_recipes/chipotle_burrito_bowl.md",
        "03_recipes/chipotle_burrito_bowl_fond_method.md",
        "03_recipes/balsamic_chicken_bowl.md",
        "03_recipes/buffalo_chicken_wing_bowl.md",
        "03_recipes/honey_garlic_chicken_bowl.md",
        "03_recipes/teriyaki_chicken_bowl.md",
        "03_recipes/pulled_chicken_taco_bowl.md",
        "03_recipes/sofritas_protocol.md",
        "03_recipes/simple_rice_bowl.md",
        # Techniques / Systems
        "02_techniques/core_techniques.md",
        "02_techniques/meal_prep_storage.md",
        "02_techniques/marinades.md",
        # Fundamentals
        "01_fundamentals/spices_and_flavor.md",
        "01_fundamentals/bachelor_hacks.md",
        "01_fundamentals/timing_charts.md",
        # Quick-reference appendix
        "04_reference/timing_dictionary.md",
        "04_reference/universal_troubleshooting.md",
        "04_reference/safety_check.md",
        "04_reference/glossary.md",
    ]


def _render_html(md_text: str) -> str | None:
    try:
        import markdown  # type: ignore
    except Exception:
        return None

    md = markdown.Markdown(extensions=["extra", "attr_list", "toc"])
    body = md.convert(md_text)

    css = """
@page {
  size: letter;
  margin: 0.75in;
  @bottom-right { content: "p. " counter(page); font-size: 10pt; }
}
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.35; color: #000; }
h1 { font-size: 22pt; page-break-after: avoid; }
h2 { font-size: 16pt; page-break-after: avoid; }
h3 { font-size: 13pt; page-break-after: avoid; }
/* Keep checkboxes visible */
input[type="checkbox"] { width: 14px; height: 14px; }
/* Make xrefs print like a book reference (no URL), with automatic page number */
a.xref { color: #000; text-decoration: none; }
@media print {
  a.xref::after { content: " (p. " target-counter(attr(href), page) ")"; }
}
/* Hard page break marker */
.page-break { page-break-after: always; }
"""

    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Bachelor Cookbook - Print Bundle</title>
  <style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""


def _write_pdf(html: str, out_pdf: Path) -> bool:
    try:
        from weasyprint import HTML  # type: ignore
    except Exception:
        return False

    HTML(string=html, base_url=str(BASE_DIR)).write_pdf(str(out_pdf))
    return True


def main() -> int:
    PRINT_DIR.mkdir(parents=True, exist_ok=True)

    ordered = _bundle_order()
    docs: list[Doc] = []

    for rel in ordered:
        path = BASE_DIR / rel
        if not path.exists():
            print(f"ERROR: Missing file in bundle order: {rel}", file=sys.stderr)
            return 2
        raw = _read_text(path)
        title = _extract_title(raw, fallback=Path(rel).stem)
        anchor = f"doc-{_slugify(rel.replace('.md', ''))}"
        docs.append(Doc(rel_path=rel, title=title, anchor=anchor))

    docs_by_rel = {d.rel_path: d for d in docs}
    docs_by_name = {Path(d.rel_path).name: d for d in docs}

    # Build a simple TOC up front with xref links that will auto-page-number in PDF.
    toc_lines: list[str] = []
    toc_lines.append("# Bachelor Cookbook: Print Bundle\n")
    toc_lines.append("## Table of Contents\n")
    for d in docs:
        toc_lines.append(f"- [{d.title}](#{d.anchor}){{.xref}}\n")
    toc_lines.append("\n<!-- PAGE_BREAK -->\n")

    parts: list[str] = ["".join(toc_lines)]

    for i, d in enumerate(docs):
        src = BASE_DIR / d.rel_path
        raw = _read_text(src)
        rewritten = _rewrite_backtick_md_refs(raw, docs_by_rel, docs_by_name)

        # Ensure each doc starts on a new page (after TOC and after previous docs).
        if i > 0:
            parts.append("\n<!-- PAGE_BREAK -->\n\n")

        # Add a stable anchor for cross-references.
        parts.append(f'<a id="{d.anchor}"></a>\n\n')
        parts.append(rewritten)

    # Convert PAGE_BREAK markers into HTML page breaks when rendering.
    compiled_md = "".join(parts)
    compiled_md = compiled_md.replace("<!-- PAGE_BREAK -->", '<div class="page-break"></div>')

    out_md = PRINT_DIR / "compiled_manual.md"
    out_md.write_text(compiled_md, encoding="utf-8")
    print(f"✓ Wrote {out_md.relative_to(BASE_DIR)}")

    html = _render_html(compiled_md)
    if html is None:
        print("ℹ️ Skipped HTML/PDF generation (missing dependency: markdown).")
        return 0

    out_html = PRINT_DIR / "compiled_manual.html"
    out_html.write_text(html, encoding="utf-8")
    print(f"✓ Wrote {out_html.relative_to(BASE_DIR)}")

    out_pdf = PRINT_DIR / "compiled_manual.pdf"
    if _write_pdf(html, out_pdf):
        print(f"✓ Wrote {out_pdf.relative_to(BASE_DIR)}")
    else:
        print("ℹ️ Skipped PDF generation (missing dependency: weasyprint).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

