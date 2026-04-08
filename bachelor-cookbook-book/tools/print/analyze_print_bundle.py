#!/usr/bin/env python3
"""
Analyze the compiled print bundle and report layout risks without needing a physical test print.

Checks:
- Which docs start on which physical page (and whether that page is right/left).
- For each recipe, whether its "front side" fits on ONE page:
  We compare the page where the recipe starts (doc anchor) to the page where the back-side begins
  (injected anchor at the first <!-- PAGE_BREAK -->).

Usage:
  python3 tools/print/analyze_print_bundle.py
"""

from __future__ import annotations

from pathlib import Path

from weasyprint import HTML


BASE_DIR = Path(__file__).resolve().parents[2]
PRINT_DIR = BASE_DIR / "05_print"


def _side(page_num: int) -> str:
    return "RIGHT" if page_num % 2 == 1 else "LEFT"


def _display_page_number(physical_page: int, cover_pages: int = 2) -> int | None:
    """
    In our print bundle:
    - Physical p.1 = cover (no number)
    - Physical p.2 = blank inside cover (no number)
    - Physical p.3 = Field Notes and displayed as p.1 (main page sequence starts here)

    Therefore displayed_page = physical_page - cover_pages for all main-content pages.

    Returns None for cover pages.
    """
    if physical_page <= cover_pages:
        return None
    return physical_page - cover_pages


def main() -> int:
    html_path = PRINT_DIR / "compiled_manual.html"
    if not html_path.exists():
        print("ERROR: compiled_manual.html not found. Run:")
        print("  python3 tools/print/compile_print_bundle.py")
        return 2

    doc = HTML(filename=str(html_path)).render()
    total_pages = len(doc.pages)
    print(f"Total pages (physical): {total_pages}")

    # Page-number sanity table (physical vs displayed numbering)
    print("\nSanity check: physical page vs displayed page number")
    print("(Assuming 2 unnumbered front-matter pages: cover + blank inside cover)")
    print("| Physical | Side  | Displayed |")
    print("|:--:|:--:|:--:|")
    max_show = min(total_pages, 20)
    for physical in range(1, max_show + 1):
        disp = _display_page_number(physical)
        disp_str = "—" if disp is None else f"p. {disp}"
        print(f"| {physical} | {_side(physical)} | {disp_str} |")

    anchor_to_page: dict[str, int] = {}
    for i, page in enumerate(doc.pages):
        page_num = i + 1
        for anchor in page.anchors.keys():
            # First occurrence wins (anchor should only appear once).
            anchor_to_page.setdefault(anchor, page_num)

    # Collect doc anchors in order of appearance
    doc_anchors = [(a, p) for (a, p) in anchor_to_page.items() if a.startswith("doc-")]
    doc_anchors.sort(key=lambda x: x[1])

    print("\nDoc starts (physical page / side):")
    for a, p in doc_anchors:
        disp = _display_page_number(p)
        disp_str = "—" if disp is None else f"p. {disp}"
        print(f"- {a}: physical {p} ({_side(p)}), displayed {disp_str}")

    # Parity check: in main content, displayed odd should be RIGHT and displayed even should be LEFT.
    # (If this fails, spreads/recto logic gets inverted.)
    parity_mismatches: list[str] = []
    for physical in range(3, total_pages + 1):  # main content starts at physical 3
        disp = _display_page_number(physical)
        assert disp is not None
        expected_side = "RIGHT" if disp % 2 == 1 else "LEFT"
        actual_side = _side(physical)
        if expected_side != actual_side:
            parity_mismatches.append(f"physical {physical} is {actual_side} but displayed p.{disp} expects {expected_side}")

    print("\nDisplayed parity check (main content):")
    if not parity_mismatches:
        print("- ✅ OK: displayed odd pages are RIGHT; displayed even pages are LEFT")
    else:
        print("- ❌ Parity mismatch detected (spread logic likely inverted):")
        for line in parity_mismatches[:10]:
            print(f"  - {line}")
        if len(parity_mismatches) > 10:
            print(f"  ... and {len(parity_mismatches) - 10} more")

    # Recipe front-side overflow check
    recipe_starts = [(a, p) for (a, p) in doc_anchors if a.startswith("doc-03-recipes-")]
    issues: list[str] = []

    for start_anchor, start_page in recipe_starts:
        end_anchor = f"front-end-{start_anchor}"
        back_start_page = anchor_to_page.get(end_anchor)
        if back_start_page is None:
            # Not all recipes are front/back split (e.g., initiation recipe is intentionally long).
            continue
            continue

        front_pages = back_start_page - start_page
        if front_pages <= 0:
            issues.append(f"{start_anchor}: unexpected page ordering (start={start_page}, back={back_start_page})")
        elif front_pages == 1:
            # Good: front side fits exactly one page
            pass
        else:
            issues.append(
                f"{start_anchor}: FRONT SIDE SPILLS ({front_pages} pages before back-side starts; start={start_page}, back={back_start_page})"
            )

    print("\nRecipe front-side fit check:")
    if not issues:
        print("- ✅ All recipes: front side fits on one page")
    else:
        print("- ⚠️ Needs attention:")
        for line in issues:
            print(f"  - {line}")
        print("\nTip: Trim front-side text or tighten CSS (font/spacing) for flagged recipes.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

