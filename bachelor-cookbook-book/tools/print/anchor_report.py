#!/usr/bin/env python3
"""
Print a stable "anchor map" for the compiled single-document outputs.

Why:
- EPUB/PDF are compiled into a single document, so ids must be globally unique.
- The compiler scopes heading anchors under each doc anchor:
    {doc_anchor}--{heading-slug}
- This tool helps you discover the fragment to use in source links:
    `02_techniques/core_techniques.md#vegetables-in-the-pressure-cooker-frozen-fresh`
  (or your own manual anchors like `...#veg-pressure-cooker`)

Usage:
  python3 tools/print/anchor_report.py
  python3 tools/print/anchor_report.py --filter core_techniques
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
CPB_PATH = BASE_DIR / "tools" / "print" / "compile_print_bundle.py"


def _load_cpb():
    # Important: register in sys.modules before exec_module so dataclasses doesn't crash
    # (similar to our EPUB compiler's dynamic import fix).
    spec = importlib.util.spec_from_file_location("compile_print_bundle", CPB_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load compile_print_bundle.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--filter",
        default="",
        help="Only show docs whose rel_path contains this substring (case-insensitive).",
    )
    args = ap.parse_args()

    cpb = _load_cpb()

    chapters = cpb._chapters()  # type: ignore[attr-defined]
    docs: list[dict[str, str]] = []
    for ch in chapters:
        for rel in ch.rel_paths:
            src = BASE_DIR / rel
            md = src.read_text(encoding="utf-8")
            # mirror the print compiler's doc anchor scheme
            anchor = f"doc-{cpb._slugify(rel.replace('.md', ''))}"  # type: ignore[attr-defined]
            docs.append({"rel_path": rel, "anchor": anchor})

    filt = args.filter.strip().lower()

    heading_re = re.compile(r"^(#{2,6})\s+(.+?)\s*$")
    heading_id_re = re.compile(r"\s*\{#([A-Za-z0-9_\-:.]+)\}\s*$")
    a_id_re = re.compile(r'<a\s+id="([^"]+)"')

    for d in docs:
        rel_path = d["rel_path"]
        doc_anchor = d["anchor"]

        if filt and filt not in rel_path.lower():
            continue

        src = BASE_DIR / rel_path
        md = src.read_text(encoding="utf-8")

        print()
        print(f"{rel_path}")
        print(f"  doc anchor: {doc_anchor}")
        print("  section anchors:")

        in_fence = False
        seen: set[str] = set()
        for line in md.splitlines():
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            # Manual anchors
            am = a_id_re.search(line)
            if am:
                raw = am.group(1)
                scoped = cpb._doc_scoped_id(doc_anchor, raw)  # type: ignore[attr-defined]
                if scoped not in seen:
                    seen.add(scoped)
                    print(f"    - #{raw}  ->  #{scoped}")

            hm = heading_re.match(line)
            if not hm:
                continue

            # Heading anchors
            htext = hm.group(2)
            mid = heading_id_re.search(line)
            if mid:
                raw = mid.group(1)
                scoped = cpb._doc_scoped_id(doc_anchor, raw)  # type: ignore[attr-defined]
                if scoped not in seen:
                    seen.add(scoped)
                    print(f"    - {htext}  (use #{raw})  ->  #{scoped}")
            else:
                slug = cpb._slugify(htext)  # type: ignore[attr-defined]
                scoped = cpb._doc_scoped_id(doc_anchor, slug)  # type: ignore[attr-defined]
                if scoped not in seen:
                    seen.add(scoped)
                    print(f"    - {htext}  (use #{slug})  ->  #{scoped}")

    print()
    print("Tip: In source, prefer `file.md#slug` (short) and let the compiler scope it uniquely.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

