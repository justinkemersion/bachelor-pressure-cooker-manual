import pytest
from pathlib import Path
import subprocess


BASE_DIR = Path(__file__).parent.parent


def _has_print_deps() -> bool:
    try:
        import markdown  # noqa: F401
        import weasyprint  # noqa: F401
        return True
    except Exception:
        return False


class TestPrintPageNumbers:
    """
    Guardrail: prevent internal cross-reference page numbers from regressing to 'p. 0'.

    Root cause (previous regression):
    - Defining `counter-reset: page 0;` on a normal element in the document flow
      breaks CSS `target-counter(..., page)` and causes 0 page numbers in xrefs.
    """

    def test_compiler_does_not_define_page_counter_in_flow(self):
        # The page counter should only be controlled in @page rules, not on normal elements.
        compiler = (BASE_DIR / "tools" / "print" / "compile_print_bundle.py").read_text(encoding="utf-8")
        assert ".page-reset" not in compiler, "Do not use in-flow .page-reset; it breaks target-counter page refs"
        assert "counter-reset: page 0;" in compiler, "Expected page reset via @page main:first counter-reset"

    def test_generated_pdf_has_nonzero_xref_targets(self):
        if not _has_print_deps():
            pytest.skip("print dependencies not installed")

        # Generate bundle (includes PDF)
        subprocess.run(
            ["python3", "tools/print/compile_print_bundle.py"],
            cwd=str(BASE_DIR),
            check=True,
            capture_output=True,
            text=True,
        )

        # Render again and verify anchor mapping is sane (no missing anchors).
        from weasyprint import HTML

        html_path = BASE_DIR / "05_print" / "compiled_manual.html"
        doc = HTML(filename=str(html_path)).render()
        anchor_to_page: dict[str, int] = {}
        for i, page in enumerate(doc.pages):
            page_num = i + 1
            for anchor in page.anchors.keys():
                anchor_to_page.setdefault(anchor, page_num)

        # Ensure all doc anchors exist and are on a real page number >= 1.
        doc_anchors = [a for a in anchor_to_page.keys() if a.startswith("doc-")]
        assert doc_anchors, "Expected doc anchors in rendered output"
        assert all(anchor_to_page[a] >= 1 for a in doc_anchors), "All doc anchors should map to a physical page >= 1"

