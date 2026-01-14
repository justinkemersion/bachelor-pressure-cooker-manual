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


def _inject_front_end_anchor(md: str, anchor_id: str) -> str:
    """
    Inject an anchor right before the first PAGE_BREAK marker.
    Intended for recipes: it marks the boundary between the "front side" and the back-side notes.
    """
    marker = "<!-- PAGE_BREAK -->"
    idx = md.find(marker)
    if idx == -1:
        return md
    return md.replace(marker, f'<a id="{anchor_id}"></a>\n{marker}', 1)


def _wrap_recipe_phases(md: str) -> str:
    """
    Wrap recipe phases in a non-breaking container so a phase won't split across pages.

    We wrap sections that start with a line like:
      ### Phase 1: ...
    up to (but not including) the next '### Phase' or the first PAGE_BREAK marker.

    This is deliberately conservative and only targets recipes (called only for 03_recipes/).
    """
    lines = md.splitlines(keepends=True)
    out: list[str] = []

    in_phase = False
    for line in lines:
        # Stop phase wrapping at the recipe's front/back boundary.
        if "<!-- PAGE_BREAK -->" in line:
            if in_phase:
                out.append("</div>\n")
                in_phase = False
            out.append(line)
            continue

        # Start a new phase block.
        if line.startswith("### Phase "):
            if in_phase:
                out.append("</div>\n")
            # IMPORTANT: markdown="1" allows Python-Markdown to parse markdown inside this HTML block
            # (paired with the 'md_in_html' extension in _render_html()).
            out.append('<div class="phase" markdown="1">\n')
            in_phase = True
            out.append(line)
            continue

        out.append(line)

    if in_phase:
        out.append("</div>\n")

    return "".join(out)


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

    # md_in_html is required because the compiler injects HTML wrappers (e.g., <div class="phase">)
    # and we still want markdown headings/lists inside those wrappers to render correctly.
    md = markdown.Markdown(extensions=["extra", "attr_list", "toc", "md_in_html"])
    body = md.convert(md_text)

    css = """
@page {
  size: letter;
  margin: 0.75in;
  @bottom-right { content: "p. " counter(page); font-size: 10pt; }
  @bottom-center { content: element(continue); font-size: 9pt; color: #333; }
}
@page:first {
  @bottom-right { content: ""; }
}
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.35; color: #000; }
body { font-size: 10.5pt; }
h1 { font-size: 18pt; page-break-after: avoid; margin: 0 0 8pt 0; }
h2 { font-size: 13pt; page-break-after: avoid; margin: 12pt 0 6pt 0; }
h3 { font-size: 11pt; page-break-after: avoid; margin: 10pt 0 4pt 0; }
ul, ol { margin-top: 4pt; margin-bottom: 6pt; }
li { margin: 2pt 0; }
/* Keep checkboxes visible */
input[type="checkbox"] { width: 14px; height: 14px; }
/* Make xrefs print like a book reference (no URL), with automatic page number */
a.xref { color: #000; text-decoration: none; }
@media print {
  a.xref::after { content: " (p. " target-counter(attr(href), page) ")"; }
}
/* Hard page break marker */
.page-break { page-break-after: always; }
/* Reset visible page numbering after cover so TOC starts at p. 1 */
.page-reset { counter-reset: page 0; }
/* Ensure major docs start on a front/right (odd) page */
.section-start { break-before: right; }
/* Phase pagination: keep phases together when possible */
.phase { break-inside: avoid; }
.phase > h3 { break-after: avoid; }

/* "Continues" footer control (WeasyPrint running elements) */
.continue-note { position: running(continue); }
.continue-note.end { position: running(continue); }
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

    parts: list[str] = []

    # Cover page (no page number) — then start TOC on a right page and reset numbering so TOC shows p. 1.
    cover_path = BASE_DIR / "00_front_matter" / "cover.md"
    if cover_path.exists():
        cover_raw = _read_text(cover_path)
        parts.append(cover_raw if cover_raw.endswith("\n") else cover_raw + "\n")
        parts.append("\n<div class=\"section-start page-reset\"></div>\n\n")

    # TOC (starts at p. 1 after reset)
    toc_lines: list[str] = []
    toc_lines.append("# Table of Contents\n\n")
    for d in docs:
        toc_lines.append(f"- [{d.title}](#{d.anchor}){{.xref}}\n")
    parts.append("".join(toc_lines))
    parts.append("\n<div class=\"page-break\"></div>\n\n")

    for i, d in enumerate(docs):
        src = BASE_DIR / d.rel_path
        raw = _read_text(src)
        rewritten = _rewrite_backtick_md_refs(raw, docs_by_rel, docs_by_name)

        # Ensure each major doc starts on a front/right page (odd page).
        parts.append("\n<div class=\"section-start\"></div>\n\n")

        # Reset the running footer element at the start of each doc to avoid bleed between sections.
        parts.append('<div class="continue-note end"></div>\n')

        # For recipes, inject an anchor at the front/back boundary so we can analyze front-side overflow,
        # and wrap phases to reduce mid-phase page breaks.
        if d.rel_path.startswith("03_recipes/"):
            rewritten = _inject_front_end_anchor(rewritten, f"front-end-{d.anchor}")
            rewritten = _wrap_recipe_phases(rewritten)
            # Enable the "continues" footer for recipe pages; we'll disable at the end of the recipe.
            parts.append('<div class="continue-note">Recipe continues on next page</div>\n')

        # Add a stable anchor for cross-references.
        parts.append(f'<a id="{d.anchor}"></a>\n\n')
        parts.append(rewritten)

        # Disable the "continues" footer at the end of each recipe so the last page doesn't show it.
        if d.rel_path.startswith("03_recipes/"):
            parts.append('\n<div class="continue-note end"></div>\n')

    # Convert PAGE_BREAK markers into HTML page breaks when rendering (kept for in-recipe front/back).
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

