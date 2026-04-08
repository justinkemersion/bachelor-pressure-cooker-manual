import re
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


class TestPrintListParagraphRegressions:
    """
    Guardrail: bullets/numbered steps should not get trapped inside a <p> after a label.

    We previously saw patterns like:
      <p><strong>What NOT to Do:</strong>
      - ❌ ...
      - ❌ ...</p>
    which indicates markdown list parsing failed (usually missing blank line).
    """

    def test_no_paragraph_contains_raw_list_lines_after_strong_label(self):
        subprocess.run(
            ["python3", "tools/print/compile_print_bundle.py"],
            cwd=str(BASE_DIR),
            check=True,
            capture_output=True,
            text=True,
        )

        html = (BASE_DIR / "05_print" / "compiled_manual.html").read_text(encoding="utf-8")

        # Look for a <p> containing a <strong>Label:</strong> followed by a newline and a raw markdown list line.
        bad = re.search(r"<p><strong>[^<]*:</strong>\n\s*(?:-|\d+\.)\s+", html)
        assert bad is None, f"Found raw markdown list lines trapped in a paragraph near: {html[bad.start():bad.start()+120]!r}"

