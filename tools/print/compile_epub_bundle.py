#!/usr/bin/env python3
"""
Compile the cookbook into a Kindle-friendly EPUB in 05_print/.

Design goals:
- Single-file reading experience (one XHTML spine item) for max compatibility.
- Clickable TOC + internal links for references (no page numbers, unlike PDF).
- Reuse the same chapter ordering + reference rewrite logic as the print bundle.

Output:
- 05_print/compiled_manual.epub

Usage:
  python3 tools/print/compile_epub_bundle.py
"""

from __future__ import annotations

import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
PRINT_DIR = BASE_DIR / "05_print"

BOOK_TITLE = "The Bachelor's Pressure Cooker Cookbook"
BOOK_ID = "bachelor-pressure-cooker-cookbook"
LANG = "en"


def _require_markdown() -> None:
    try:
        import markdown  # noqa: F401
    except Exception:
        print(
            "ERROR: Missing dependency 'markdown'. Install it in your venv:\n"
            "  pip install markdown\n",
            file=sys.stderr,
        )
        raise


def _escape_xml(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "doc"


def _render_xhtml(md_text: str) -> str:
    import markdown  # type: ignore

    # Keep extensions aligned with print compiler so our injected HTML wrappers render correctly.
    md = markdown.Markdown(extensions=["extra", "attr_list", "toc", "md_in_html"])
    body = md.convert(md_text)

    css = """
body { font-family: serif; line-height: 1.4; }
h1, h2, h3 { font-family: sans-serif; }
code, pre { font-family: monospace; }
pre { white-space: pre-wrap; }
.task-list ul { list-style: none; padding-left: 0; }
.task-list li { margin: 0.2em 0; }
blockquote { border-left: 3px solid #ddd; margin-left: 0; padding-left: 1em; color: #333; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ccc; padding: 6px 8px; vertical-align: top; }
th { background: #f3f3f3; }
"""

    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{LANG}" lang="{LANG}">
  <head>
    <title>{_escape_xml(BOOK_TITLE)}</title>
    <meta charset="utf-8" />
    <style>{css}</style>
  </head>
  <body>
{body}
  </body>
</html>
"""


_EPUB_EMOJI_RE = re.compile(
    "["  # keep as a plain character class
    "\U0001F000-\U0001FAFF"  # most emoji blocks
    "\U0001F1E6-\U0001F1FF"  # flags
    "\u2600-\u26FF"          # misc symbols (includes ⚠)
    "\u2700-\u27BF"          # dingbats (includes ✅)
    "\u2B00-\u2BFF"          # misc symbols/arrows (includes ⭐)
    "]"
)


def _sanitize_for_epub(md: str) -> str:
    """
    Kindle often renders emoji as empty rectangles (tofu).
    Strip emoji-ish glyphs for EPUB output only, keeping the print sources unchanged.
    """
    # Remove emoji presentation selectors / joiners.
    md = md.replace("\uFE0F", "").replace("\uFE0E", "").replace("\u200D", "")

    # Target the known offenders we actually use as section markers.
    md = md.replace("📋", "")
    md = md.replace("⚠", "")
    md = md.replace("✅", "")
    md = md.replace("⭐", "")

    # Remove any remaining emoji-ish symbols.
    md = _EPUB_EMOJI_RE.sub("", md)

    # Clean up spacing caused by removing leading icons in headings/lists.
    md = re.sub(r"(?m)^(#+)\s{2,}", r"\1 ", md)
    md = re.sub(r"(?m)^(\s*[-*+]\s)\s+", r"\1", md)
    return md


def _build_nav_xhtml(chapters: list[dict]) -> str:
    # chapters: [{id, title, docs:[{title, anchor}]}]
    items: list[str] = []
    for ch in chapters:
        items.append(f'<li><a href="content.xhtml#chapter-{_escape_xml(ch["id"])}">{_escape_xml(ch["id"])} — {_escape_xml(ch["title"])}</a>')
        items.append("<ol>")
        for d in ch["docs"]:
            items.append(f'<li><a href="content.xhtml#{_escape_xml(d["anchor"])}">{_escape_xml(d["title"])}</a></li>')
        items.append("</ol></li>")

    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{LANG}" lang="{LANG}">
  <head>
    <title>Table of Contents</title>
    <meta charset="utf-8" />
  </head>
  <body>
    <nav xmlns:epub="http://www.idpf.org/2007/ops" epub:type="toc" id="toc">
      <h1>Table of Contents</h1>
      <ol>
        {''.join(items)}
      </ol>
    </nav>
  </body>
</html>
"""


def _build_toc_ncx(chapters: list[dict]) -> str:
    # Legacy TOC for older readers.
    play_order = 1
    nav_points: list[str] = []

    for ch in chapters:
        ch_order = play_order
        play_order += 1
        doc_points: list[str] = []
        for d in ch["docs"]:
            d_order = play_order
            play_order += 1
            doc_points.append(
                f"""
      <navPoint id="nav-{d_order}" playOrder="{d_order}">
        <navLabel><text>{_escape_xml(d["title"])}</text></navLabel>
        <content src="content.xhtml#{_escape_xml(d["anchor"])}" />
      </navPoint>""".rstrip()
            )

        nav_points.append(
            f"""
    <navPoint id="nav-{ch_order}" playOrder="{ch_order}">
      <navLabel><text>{_escape_xml(ch["id"])} — {_escape_xml(ch["title"])}</text></navLabel>
      <content src="content.xhtml#chapter-{_escape_xml(ch["id"])}" />
      {''.join(doc_points)}
    </navPoint>""".rstrip()
        )

    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
  "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="{_escape_xml(BOOK_ID)}" />
    <meta name="dtb:depth" content="2" />
    <meta name="dtb:totalPageCount" content="0" />
    <meta name="dtb:maxPageNumber" content="0" />
  </head>
  <docTitle><text>{_escape_xml(BOOK_TITLE)}</text></docTitle>
  <navMap>
{''.join(nav_points)}
  </navMap>
</ncx>
"""


def _build_opf(modified_iso: str) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="3.0" xml:lang="{LANG}">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="BookId">{_escape_xml(BOOK_ID)}</dc:identifier>
    <dc:title>{_escape_xml(BOOK_TITLE)}</dc:title>
    <dc:language>{_escape_xml(LANG)}</dc:language>
    <meta property="dcterms:modified">{_escape_xml(modified_iso)}</meta>
  </metadata>
  <manifest>
    <item id="content" href="content.xhtml" media-type="application/xhtml+xml" />
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav" />
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml" />
  </manifest>
  <spine toc="ncx">
    <itemref idref="content" />
  </spine>
</package>
"""


def _container_xml() -> str:
    return """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""


def main() -> int:
    _require_markdown()
    PRINT_DIR.mkdir(parents=True, exist_ok=True)

    # Reuse chapter structure + ref rewriting from the print compiler.
    import importlib.util
    import sys as _sys

    # NOTE: We deliberately load by file path (no package import requirement). On Python 3.13,
    # dataclasses expects the module to exist in sys.modules while the module body is executing.
    spec = importlib.util.spec_from_file_location(
        "tools.print.compile_print_bundle", str(BASE_DIR / "tools" / "print" / "compile_print_bundle.py")
    )
    assert spec and spec.loader
    cpb = importlib.util.module_from_spec(spec)
    _sys.modules[spec.name] = cpb
    spec.loader.exec_module(cpb)  # type: ignore

    chapters_obj = cpb._chapters()  # type: ignore[attr-defined]
    docs: list[cpb.Doc] = []  # type: ignore[attr-defined]
    raw_by_rel: dict[str, str] = {}
    tags_by_rel: dict[str, dict[str, object]] = {}

    for ch in chapters_obj:
        for rel in ch.rel_paths:
            path = BASE_DIR / rel
            if not path.exists():
                print(f"ERROR: Missing file in EPUB order: {rel}", file=sys.stderr)
                return 2
            raw = cpb._read_text(path)  # type: ignore[attr-defined]
            raw_by_rel[rel] = raw
            if rel.startswith("03_recipes/"):
                tags_by_rel[rel] = cpb._parse_recipe_tags(raw)  # type: ignore[attr-defined]
            title_raw = cpb._extract_title(raw, fallback=Path(rel).stem)  # type: ignore[attr-defined]
            title = cpb._normalize_title_for_print(title_raw)  # type: ignore[attr-defined]
            anchor = f"doc-{_slugify(rel.replace('.md', ''))}"
            docs.append(
                cpb.Doc(  # type: ignore[attr-defined]
                    rel_path=rel,
                    title=title,
                    anchor=anchor,
                    chapter_id=ch.id,
                    chapter_title=ch.title,
                )
            )

    docs_by_rel = {d.rel_path: d for d in docs}
    docs_by_name = {Path(d.rel_path).name: d for d in docs}

    # Build chapter+doc metadata for nav/toc.
    nav_chapters: list[dict] = []
    for ch in chapters_obj:
        ch_docs = [docs_by_rel[rel] for rel in ch.rel_paths]
        if ch.id == "03":
            # Insert a browsable index entry at the top of the Recipes chapter nav.
            ch_docs = [
                cpb.Doc(  # type: ignore[attr-defined]
                    rel_path="__recipe_index__",
                    title="Recipe Index",
                    anchor="recipe-index",
                    chapter_id=ch.id,
                    chapter_title=ch.title,
                )
            ] + ch_docs
        nav_chapters.append(
            {
                "id": ch.id,
                "title": ch.title,
                "docs": [{"title": d.title, "anchor": d.anchor} for d in ch_docs],
            }
        )

    parts: list[str] = []

    # Title/cover content (as markdown) if present
    cover_path = BASE_DIR / "00_front_matter" / "cover.md"
    if cover_path.exists():
        parts.append(cpb._read_text(cover_path))  # type: ignore[attr-defined]
        parts.append("\n---\n\n")

    # Field notes (fine in ebooks; acts as a notes page)
    inside_cover = BASE_DIR / "00_front_matter" / "inside_cover_field_notes.md"
    if inside_cover.exists():
        parts.append(cpb._read_text(inside_cover))  # type: ignore[attr-defined]
        parts.append("\n---\n\n")

    # In-book TOC (for any reader that doesn't use EPUB nav)
    parts.append("# Table of Contents\n\n")
    # Use raw HTML to guarantee nesting (some markdown normalizers flatten nested lists).
    parts.append("<ul>\n")
    for ch in nav_chapters:
        parts.append(f'  <li><a href="#chapter-{_escape_xml(ch["id"])}">{_escape_xml(ch["id"])} — {_escape_xml(ch["title"])}</a>\n')
        parts.append("    <ul>\n")
        for d in ch["docs"]:
            parts.append(f'      <li><a href="#{_escape_xml(d["anchor"])}">{_escape_xml(d["title"])}</a></li>\n')
        parts.append("    </ul>\n")
        parts.append("  </li>\n")
    parts.append("</ul>\n\n---\n\n")

    # Chapters + docs
    for ch in chapters_obj:
        parts.append(f'<a id="chapter-{ch.id}"></a>\n\n')
        parts.append(f"# {ch.id} — {ch.title}\n\n")
        parts.append(f"**{ch.subtitle}**\n\n")
        parts.append("\n---\n\n")

        if ch.id == "03":
            recipe_docs = [docs_by_rel[rel] for rel in ch.rel_paths if rel.startswith("03_recipes/")]
            parts.append('<a id="recipe-index"></a>\n\n')
            parts.append(cpb._build_recipe_index_md(recipe_docs, raw_by_rel, tags_by_rel))  # type: ignore[attr-defined]
            parts.append("\n---\n\n")

        for rel in ch.rel_paths:
            d = docs_by_rel[rel]
            src = BASE_DIR / d.rel_path
            raw = raw_by_rel.get(d.rel_path) or cpb._read_text(src)  # type: ignore[attr-defined]
            rewritten = cpb._rewrite_backtick_md_refs(raw, docs_by_rel, docs_by_name)  # type: ignore[attr-defined]
            rewritten = cpb._rewrite_first_h1(rewritten, d.title)  # type: ignore[attr-defined]
            rewritten = cpb._inject_doc_scoped_anchors(rewritten, d.anchor)  # type: ignore[attr-defined]

            # Ensure doc anchor exists.
            parts.append(f'<a id="{d.anchor}"></a>\n\n')
            parts.append(rewritten if rewritten.endswith("\n") else rewritten + "\n")
            parts.append("\n---\n\n")

    compiled_md = "".join(parts)
    compiled_md = cpb._normalize_markdown_lists(compiled_md)  # type: ignore[attr-defined]
    compiled_md = cpb._normalize_task_list_checkboxes(compiled_md)  # type: ignore[attr-defined]

    # PAGE_BREAK is a print concept; render as a simple divider in ebooks.
    compiled_md = compiled_md.replace("<!-- PAGE_BREAK -->", "\n---\n")
    compiled_md = _sanitize_for_epub(compiled_md)

    # Convert to XHTML
    content_xhtml = _render_xhtml(compiled_md)
    nav_xhtml = _build_nav_xhtml(nav_chapters)
    toc_ncx = _build_toc_ncx(nav_chapters)

    modified_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    opf = _build_opf(modified_iso)

    epub_path = PRINT_DIR / "compiled_manual.epub"

    # Write EPUB (a zip with required structure)
    with zipfile.ZipFile(epub_path, "w") as zf:
        # Per spec: mimetype must be first and uncompressed
        zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        zf.writestr("META-INF/container.xml", _container_xml(), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/content.xhtml", content_xhtml, compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/nav.xhtml", nav_xhtml, compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/toc.ncx", toc_ncx, compress_type=zipfile.ZIP_DEFLATED)

    print(f"✓ Wrote {epub_path.relative_to(BASE_DIR)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

