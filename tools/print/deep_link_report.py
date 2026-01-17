#!/usr/bin/env python3
"""
Report backtick markdown references that likely should be deep links.

We support links like:
  See `02_techniques/core_techniques.md#universal-microwave-reheating-method`

This tool finds patterns like:
  See `02_techniques/core_techniques.md` (Universal Microwave Reheating Method)
and suggests adding a #fragment based on matching the hint text to a heading
inside the referenced file.

Usage:
  python3 tools/print/deep_link_report.py
  python3 tools/print/deep_link_report.py --fix-preview
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
import importlib.util
import sys


BASE_DIR = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Finding:
    src: Path
    line_no: int
    line: str
    ref: str
    hint: str
    suggestion: str | None


_REF_RE = re.compile(r"`([^`]+\.md)`")
_REF_RE_WITH_HINT = re.compile(r"`([^`]+\.md)`\s*\(([^)]+)\)")


def _slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "section"


def _iter_book_markdown_files() -> list[Path]:
    # Keep it simple: scan the main book content folders.
    roots = [
        BASE_DIR / "00_front_matter",
        BASE_DIR / "01_fundamentals",
        BASE_DIR / "02_techniques",
        BASE_DIR / "03_recipes",
        BASE_DIR / "04_reference",
    ]
    out: list[Path] = []
    for r in roots:
        if not r.exists():
            continue
        out.extend(sorted(r.rglob("*.md")))
    return out


def _load_cpb():
    cpb_path = BASE_DIR / "tools" / "print" / "compile_print_bundle.py"
    spec = importlib.util.spec_from_file_location("compile_print_bundle", cpb_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load compile_print_bundle.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _book_relpaths_set() -> set[str]:
    """
    Return the set of relpaths that are actually included in the compiled book.
    """
    cpb = _load_cpb()
    chapters = cpb._chapters()  # type: ignore[attr-defined]
    rels: set[str] = set()
    for ch in chapters:
        rels.update(ch.rel_paths)
    # Front matter is also included but we don't typically deep-link into it.
    return rels


def _resolve_ref_to_book_path(ref: str, in_book: set[str]) -> str | None:
    """
    Resolve a backtick ref to a concrete relpath in the compiled book.
    Supports refs that are either:
    - full relpaths like "02_techniques/core_techniques.md"
    - bare filenames like "simple_rice_bowl.md"
    """
    if ref in in_book:
        return ref
    name = Path(ref).name
    matches = [p for p in in_book if Path(p).name == name]
    if len(matches) == 1:
        return matches[0]
    return None


def _extract_headings(md: str) -> list[str]:
    headings: list[str] = []
    in_fence = False
    for line in md.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{2,6})\s+(.+?)\s*$", line)
        if m:
            headings.append(m.group(2).strip())
    return headings


def _best_heading_match(hint: str, headings: list[str]) -> tuple[str | None, float]:
    hint_n = re.sub(r"\s+", " ", hint.strip().lower())
    best: tuple[str | None, float] = (None, 0.0)
    for h in headings:
        h_n = re.sub(r"\s+", " ", h.strip().lower())
        # Quick wins
        if hint_n == h_n:
            return (h, 1.0)
        if hint_n in h_n or h_n in hint_n:
            score = 0.92
        else:
            score = SequenceMatcher(None, hint_n, h_n).ratio()
        if score > best[1]:
            best = (h, score)
    return best


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--fix-preview",
        action="store_true",
        help="Print a preview replacement line for each suggestion.",
    )
    args = ap.parse_args()

    findings: list[Finding] = []
    in_book = _book_relpaths_set()

    for src in _iter_book_markdown_files():
        rel_src = src.relative_to(BASE_DIR)
        content = src.read_text(encoding="utf-8")
        lines = content.splitlines()

        for i, line in enumerate(lines, start=1):
            # We only flag things that look "obviously" like a deep-link candidate:
            # - There's a parenthetical hint immediately after the ref, OR
            # - The line contains "See `...` for ..." where the "for ..." is a hint-ish phrase.
            m = _REF_RE_WITH_HINT.search(line)
            hint = ""
            ref = ""
            if m:
                ref = m.group(1)
                hint = m.group(2).strip()
            else:
                if "See `" in line and " for " in line:
                    # best-effort: pull the words after "for" as a hint
                    rm = _REF_RE.search(line)
                    if not rm:
                        continue
                    ref = rm.group(1)
                    hint = line.split(" for ", 1)[1].strip().strip(".")
                else:
                    continue

            # Skip if already deep-linked
            if "#" in ref:
                continue

            # Only suggest deep links for docs that are actually in the compiled book.
            resolved = _resolve_ref_to_book_path(ref, in_book)
            if resolved is None:
                findings.append(
                    Finding(
                        src=rel_src,
                        line_no=i,
                        line=line,
                        ref=ref,
                        hint=hint,
                        suggestion=None,
                    )
                )
                continue

            target = (BASE_DIR / resolved).resolve()
            if not target.exists():
                findings.append(
                    Finding(
                        src=rel_src,
                        line_no=i,
                        line=line,
                        ref=ref,
                        hint=hint,
                        suggestion=None,
                    )
                )
                continue

            headings = _extract_headings(target.read_text(encoding="utf-8"))
            best, score = _best_heading_match(hint, headings)
            suggestion = None
            if best and score >= 0.75:
                suggestion = f"{ref}#{_slugify(best)}"

            findings.append(
                Finding(
                    src=rel_src,
                    line_no=i,
                    line=line,
                    ref=ref,
                    hint=hint,
                    suggestion=suggestion,
                )
            )

    actionable = [f for f in findings if f.suggestion]
    missing = [f for f in findings if (f.suggestion is None)]

    print(f"Deep-link candidates found: {len(findings)}")
    print(f"  suggestions: {len(actionable)}")
    print(f"  needs review: {len(missing)}")

    def _print_one(f: Finding) -> None:
        print()
        print(f"{f.src}:{f.line_no}")
        print(f"  line: {f.line.strip()}")
        print(f"  ref: `{f.ref}`")
        print(f"  hint: {f.hint}")
        if f.suggestion:
            print(f"  suggestion: `{f.suggestion}`")
            if args.fix_preview:
                print(f"  preview: {f.line.replace(f'`{f.ref}`', f'`{f.suggestion}`').strip()}")
        else:
            print("  suggestion: (none)")

    for f in actionable:
        _print_one(f)

    if missing:
        print()
        print("-----")
        print("Needs review (no confident suggestion):")
        for f in missing[:50]:
            _print_one(f)
        if len(missing) > 50:
            print(f"\n... and {len(missing) - 50} more")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

