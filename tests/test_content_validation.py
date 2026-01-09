"""
Test content validation - check for common errors, missing information, etc.
"""
import re
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
            assert "cup" in content.lower() or "1.75" in content or "2 cup" in content, \
                f"{recipe_file.name} should specify liquid amount"


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
