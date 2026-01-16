import subprocess
import zipfile
from pathlib import Path

import pytest


BASE_DIR = Path(__file__).parent.parent


def _has_markdown_dependency() -> bool:
    try:
        import markdown  # noqa: F401

        return True
    except Exception:
        return False


class TestEpubBuild:
    def test_compile_epub_bundle_creates_epub(self):
        if not _has_markdown_dependency():
            pytest.skip("markdown dependency not installed; epub not generated")

        subprocess.run(
            ["python3", "tools/print/compile_epub_bundle.py"],
            cwd=str(BASE_DIR),
            check=True,
            capture_output=True,
            text=True,
        )

        epub_path = BASE_DIR / "05_print" / "compiled_manual.epub"
        assert epub_path.exists(), "Expected 05_print/compiled_manual.epub to be generated"

        with zipfile.ZipFile(epub_path) as zf:
            names = set(zf.namelist())
            assert "mimetype" in names
            assert zf.read("mimetype") == b"application/epub+zip"

            assert "OEBPS/content.xhtml" in names
            assert "OEBPS/nav.xhtml" in names
            assert "OEBPS/content.opf" in names

            nav = zf.read("OEBPS/nav.xhtml").decode("utf-8")
            # Ensure at least one known anchor makes it into the TOC for clickability
            assert "doc-03-recipes-beef-tenderloin-steak-dinner" in nav
            assert "content.xhtml#doc-03-recipes-beef-tenderloin-steak-dinner" in nav

