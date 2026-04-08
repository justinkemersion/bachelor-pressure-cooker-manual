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


class TestPrintRendering:
    """
    Guardrail: prevent raw markdown (e.g., '### Phase', '## Instructions') from leaking into the
    generated HTML/PDF due to HTML wrappers that disable markdown parsing.
    """

    def test_compiled_html_has_no_raw_markdown_headings(self):
        if not _has_markdown_dependency():
            pytest.skip("markdown dependency not installed; print HTML not generated")

        # Generate bundle (HTML + optional PDF)
        subprocess.run(
            ["python3", "tools/print/compile_print_bundle.py"],
            cwd=str(BASE_DIR),
            check=True,
            capture_output=True,
            text=True,
        )

        html_path = BASE_DIR / "05_print" / "compiled_manual.html"
        assert html_path.exists(), "Expected 05_print/compiled_manual.html to be generated"

        html = html_path.read_text(encoding="utf-8")

        # These should never appear as literal text in rendered HTML.
        # If they appear, markdown parsing likely broke inside injected HTML wrappers.
        assert "### Phase" not in html, "Raw markdown heading leaked into compiled HTML (### Phase)"
        assert "## Instructions" not in html, "Raw markdown heading leaked into compiled HTML (## Instructions)"

