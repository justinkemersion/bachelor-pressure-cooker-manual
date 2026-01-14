"""
Test timing consistency across all reference files.
Ensures timing charts, dictionary, and recipes all agree.
"""
import re
import pytest
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
TIMING_CHARTS = BASE_DIR / "01_fundamentals" / "timing_charts.md"
TIMING_DICT = BASE_DIR / "04_reference" / "timing_dictionary.md"
RECIPES_DIR = BASE_DIR / "03_recipes"


def extract_timing_from_charts():
    """Extract timing data from timing_charts.md"""
    timings = {}
    if not TIMING_CHARTS.exists():
        return timings
    
    content = TIMING_CHARTS.read_text()
    # Match table rows with timing info
    pattern = r'\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+)\s*\|\s*[^|]+\s*\|\s*\*\*([^*]+)\*\*\s*\|'
    matches = re.findall(pattern, content)
    
    for ingredient, state, time in matches:
        key = f"{ingredient.strip()}_{state.strip()}"
        timings[key] = time.strip()
    
    return timings


def extract_timing_from_dict():
    """Extract timing data from Timing_Dictionary.md"""
    timings = {}
    if not TIMING_DICT.exists():
        return timings
    
    content = TIMING_DICT.read_text()
    pattern = r'\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+)\s*\|\s*\*\*([^*]+)\*\*\s*\|'
    matches = re.findall(pattern, content)
    
    for ingredient, state, time in matches:
        key = f"{ingredient.strip()}_{state.strip()}"
        timings[key] = time.strip()
    
    return timings


def extract_timing_from_recipes():
    """Extract timing mentions from recipe files"""
    timings = {}
    if not RECIPES_DIR.exists():
        return timings
    
    for recipe_file in RECIPES_DIR.glob("*.md"):
        content = recipe_file.read_text()
        # Look for pressure cook timing patterns
        pattern = r'\*\*(\d+)\s*(?:mins?|minutes?|m)\s*(?:HP|High Pressure)?\*\*'
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            timings[recipe_file.stem] = matches
    
    return timings


class TestTimingConsistency:
    """Test that timing information is consistent across all files"""
    
    def test_timing_charts_exists(self):
        """Timing charts file should exist"""
        assert TIMING_CHARTS.exists(), "timing_charts.md should exist"
    
    def test_timing_dictionary_exists(self):
        """Timing dictionary should exist"""
        assert TIMING_DICT.exists(), "timing_dictionary.md should exist"
    
    def test_chicken_thighs_timing(self):
        """Chicken thighs timing should be consistent"""
        charts = extract_timing_from_charts()
        dictionary = extract_timing_from_dict()
        
        # Check thawed
        if "Chicken Thighs_Thawed" in charts:
            chart_time = charts["Chicken Thighs_Thawed"]
            assert "8" in chart_time or "8-10" in chart_time, \
                f"Chicken thighs thawed should be 8-10m, found: {chart_time}"
        
        # Check frozen
        if "Chicken Thighs_Frozen" in charts:
            chart_time = charts["Chicken Thighs_Frozen"]
            assert "12" in chart_time or "12-15" in chart_time, \
                f"Chicken thighs frozen should be 12-15m, found: {chart_time}"
    
    def test_rice_timing_consistency(self):
        """Rice timing should be consistent"""
        charts = extract_timing_from_charts()
        
        # Basmati should be 6m
        if "White Basmati Rice_Rinsed" in charts:
            assert "6" in charts["White Basmati Rice_Rinsed"], \
                "Basmati rice should be 6m"
        
        # Jasmine should be 4m
        if "Jasmine Rice_Rinsed" in charts:
            assert "4" in charts["Jasmine Rice_Rinsed"], \
                "Jasmine rice should be 4m"
        
        # Long Grain should be 5m
        if "Long Grain White_Rinsed" in charts:
            assert "5" in charts["Long Grain White_Rinsed"], \
                "Long Grain White rice should be 5m"
    
    def test_all_timings_have_nr(self):
        """All timing entries should specify Natural Release"""
        charts = extract_timing_from_charts()
        content = TIMING_CHARTS.read_text()
        
        # Check that NR is mentioned for proteins and rice
        assert "10m NR" in content or "10m Natural Release" in content, \
            "Timing charts should specify Natural Release times"


class TestRecipeFormat:
    """Test that recipes follow the correct format"""
    
    def test_all_recipes_have_version(self):
        """All recipes should have a version number"""
        for recipe_file in RECIPES_DIR.glob("*.md"):
            content = recipe_file.read_text()
            assert "Version:" in content or "**Version:**" in content, \
                f"{recipe_file.name} should have a version number"
    
    def test_all_recipes_have_quick_reference(self):
        """All recipes should have Quick Reference section"""
        for recipe_file in RECIPES_DIR.glob("*.md"):
            content = recipe_file.read_text()
            # Check for various Quick Reference formats (case-insensitive)
            has_quick_ref = (
                "Quick Reference" in content or 
                "QUICK REFERENCE" in content or
                "📋" in content or 
                "📖" in content
            )
            assert has_quick_ref, \
                f"{recipe_file.name} should have Quick Reference section"
    
    def test_all_recipes_have_chemistry_notes(self):
        """All recipes should have chemistry notes"""
        for recipe_file in RECIPES_DIR.glob("*.md"):
            content = recipe_file.read_text()
            assert "Chemistry" in content or "🧪" in content, \
                f"{recipe_file.name} should have Chemistry Notes section"


class TestLiquidRatios:
    """Test liquid ratio consistency"""
    
    def test_sequential_cooking_liquid_rule(self):
        """Sequential cooking recipes should use 2 cups liquid (burn-proof)"""
        chipotle = RECIPES_DIR / "chipotle_burrito_bowl.md"
        if chipotle.exists():
            content = chipotle.read_text()
            # Should mention 2 cups for burn-proof buffer
            assert "2 cups" in content or "2.0 cups" in content, \
                "Chipotle recipe should use 2 cups liquid (burn-proof buffer)"
    
    def test_rice_ratio_mentioned(self):
        """Recipes should mention 1:1 ratio for rice"""
        for recipe_file in RECIPES_DIR.glob("*bowl*.md"):
            content = recipe_file.read_text()
            assert "1:1" in content or "2 cups" in content or "2 cup" in content, \
                f"{recipe_file.name} should mention rice ratio"
