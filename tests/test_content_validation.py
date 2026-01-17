"""
Test content validation - check for common errors, missing information, etc.
"""
import re
import os
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class TestContentCompleteness:
    """Test that content is complete and not missing critical information"""
    
    def test_timing_charts_have_chicken_cuts(self):
        """Timing charts should have all common chicken cuts"""
        timing_charts = BASE_DIR / "01_fundamentals" / "timing_charts.md"
        if not timing_charts.exists():
            pytest.skip("Timing charts not found")
        
        content = timing_charts.read_text()
        required_cuts = ["Thighs", "Breast", "Cutlets"]
        
        for cut in required_cuts:
            assert cut in content, \
                f"Timing charts should include {cut}"
    
    def test_timing_charts_have_rice_types(self):
        """Timing charts should have all rice types"""
        timing_charts = BASE_DIR / "01_fundamentals" / "timing_charts.md"
        if not timing_charts.exists():
            pytest.skip("Timing charts not found")
        
        content = timing_charts.read_text()
        required_rice = ["Basmati", "Jasmine", "Long Grain"]
        
        for rice in required_rice:
            assert rice in content, \
                f"Timing charts should include {rice} rice"
    
    def test_glossary_has_critical_terms(self):
        """Glossary should have critical cooking terms"""
        glossary = BASE_DIR / "04_reference" / "glossary.md"
        if not glossary.exists():
            pytest.skip("Glossary not found")
        
        content = glossary.read_text()
        critical_terms = ["Natural Release", "High Pressure", "Sauté"]
        
        for term in critical_terms:
            assert term in content, \
                f"Glossary should define {term}"


class TestRecipeConsistency:
    """Test that recipes are consistent with each other"""
    
    def test_all_bowl_recipes_have_meal_prep(self):
        """All bowl recipes should have meal prep section"""
        for recipe_file in (BASE_DIR / "03_recipes").glob("*bowl*.md"):
            content = recipe_file.read_text()
            assert "Meal Prep" in content or "Reheating" in content, \
                f"{recipe_file.name} should have meal prep/reheating section"
    
    def test_recipes_mention_liquid_amount(self):
        """Recipes should specify liquid amounts"""
        for recipe_file in (BASE_DIR / "03_recipes").glob("*.md"):
            content = recipe_file.read_text()
            # Should mention cups of liquid
            assert "cup" in content.lower(), \
                f"{recipe_file.name} should specify liquid amount"

    def test_frozen_veg_mentions_include_pressure_cooker_guidance(self):
        """
        If a recipe mentions frozen veg, it must either:
        - link to the universal pressure-cooker veg method, OR
        - provide explicit pressure-cooker instructions.
        """
        for recipe_file in (BASE_DIR / "03_recipes").glob("*.md"):
            content = recipe_file.read_text()
            if re.search(r"\bfrozen veg|\bfrozen veggie|\bfrozen veggies", content, flags=re.IGNORECASE):
                assert (
                    "See `02_techniques/core_techniques.md`" in content
                    or "Pressure cook" in content
                    or "Quick Release" in content
                ), f"{recipe_file.name} mentions frozen veg but doesn't explain how to cook them in the pressure cooker or link to core techniques."

    def test_obvious_section_refs_should_be_deep_links_when_strict(self):
        """
        Optional strict mode: fail if we have an "obvious" section reference that should be a deep link.

        Rationale:
        - In the EPUB, a plain `file.md` ref jumps to the top of that doc, which is often not what the reader wants.
        - When the source text already includes a clear section name in parentheses, we should encode it as `file.md#fragment`.

        Enable with:
          STRICT_DEEP_LINKS=1 pytest -q
        """
        if os.environ.get("STRICT_DEEP_LINKS") != "1":
            pytest.skip("STRICT_DEEP_LINKS not enabled")

        # Flag patterns like:
        #   See `02_techniques/core_techniques.md` (Universal Microwave Reheating Method)
        # but ignore ones that are already deep links.
        pat = re.compile(r"`([^`]+\.md)`\s*\(([^)]+)\)")

        roots = [
            BASE_DIR / "00_front_matter",
            BASE_DIR / "01_fundamentals",
            BASE_DIR / "02_techniques",
            BASE_DIR / "03_recipes",
            BASE_DIR / "04_reference",
        ]

        offenders: list[str] = []
        for root in roots:
            if not root.exists():
                continue
            for p in root.rglob("*.md"):
                content = p.read_text()
                for m in pat.finditer(content):
                    ref = m.group(1)
                    if "#" in ref:
                        continue
                    # This is an "obvious" section reference; in strict mode we require a fragment.
                    offenders.append(f"{p.relative_to(BASE_DIR)}: `{ref}` ({m.group(2).strip()})")

        assert not offenders, "Found obvious section refs that should be deep links:\n" + "\n".join(offenders)


class TestFormatting:
    """Test markdown formatting consistency"""
    
    def test_checkboxes_used_for_ingredients(self):
        """Ingredients should use checkboxes format"""
        for recipe_file in (BASE_DIR / "03_recipes").glob("*.md"):
            content = recipe_file.read_text()
            # Should have checkbox format in ingredients section
            if "Hardware & Variables" in content or "Ingredients" in content:
                assert "- [ ]" in content, \
                    f"{recipe_file.name} should use checkbox format for ingredients"
    
    def test_bold_used_for_timings(self):
        """Timings should be bolded"""
        for recipe_file in (BASE_DIR / "03_recipes").glob("*.md"):
            content = recipe_file.read_text()
            # Look for timing patterns
            timing_pattern = r'\d+\s*(?:mins?|minutes?|m)'
            if re.search(timing_pattern, content):
                # Should have some bold timings
                assert "**" in content, \
                    f"{recipe_file.name} should bold timings"
