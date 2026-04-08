import pytest
from pathlib import Path
import subprocess


BASE_DIR = Path(__file__).parent.parent


def _has_markdown_dependency() -> bool:
    try:
        import markdown  # noqa: F401
        return True
    except Exception:
        return False


class TestPrintTaskLists:
    """
    Guardrail: ensure task-list checkboxes render as proper checkbox inputs, not literal '[ ]'
    and not as run-on text.
    """

    def test_tasklists_render_as_checkboxes(self):
        if not _has_markdown_dependency():
            pytest.skip("markdown dependency not installed; print HTML not generated")

        subprocess.run(
            ["python3", "tools/print/compile_print_bundle.py"],
            cwd=str(BASE_DIR),
            check=True,
            capture_output=True,
            text=True,
        )

        html_path = BASE_DIR / "05_print" / "compiled_manual.html"
        html = html_path.read_text(encoding="utf-8")

        assert "<li>[ ]" not in html, "Checkboxes should not render as literal '[ ]' inside list items"
        assert "<li>☐" in html or "<li>☑" in html, "Expected print-friendly checkbox glyphs (☐/☑) in compiled HTML"
        assert 'input type="checkbox"' not in html, "We should not emit HTML form checkboxes (WeasyPrint renders them poorly)"

