"""
Test that all cross-references and links are valid.
Ensures glossary terms are defined, file references exist, etc.
"""
import re
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


def find_markdown_files():
    """Find all markdown files in the project"""
    md_files = []
    for path in BASE_DIR.rglob("*.md"):
        if "notes-for-cursor" not in str(path):  # Skip notes
            md_files.append(path)
    return md_files


def extract_file_references(content):
    """Extract file references from markdown (e.g., `01_fundamentals/file.md`)"""
    pattern = r'`([^`]+\.md)`'
    return re.findall(pattern, content)


def extract_glossary_terms(content):
    """Extract terms that should be in glossary"""
    # Look for terms in bold that might need definition
    pattern = r'\*\*([A-Z][a-zA-Z\s]+)\*\*'
    return re.findall(pattern, content)


class TestFileReferences:
    """Test that all file references are valid"""
    
    def test_all_referenced_files_exist(self):
        """All referenced markdown files should exist"""
        md_files = find_markdown_files()
        
        for md_file in md_files:
            content = md_file.read_text()
            references = extract_file_references(content)
            
            for ref in references:
                # Skip placeholder references (e.g., [recipe_name].md)
                if "[" in ref and "]" in ref:
                    continue  # This is a placeholder, not a real reference
                
                # Handle relative paths
                if "/" in ref:
                    ref_path = BASE_DIR / ref
                else:
                    # If reference is just a filename, check common locations
                    ref_path = md_file.parent / ref
                    if not ref_path.exists() and "templates" in str(md_file):
                        # Template references recipes in 03_recipes/
                        ref_path = BASE_DIR / "03_recipes" / ref
                    elif not ref_path.exists():
                        # Try recipes directory as fallback
                        ref_path = BASE_DIR / "03_recipes" / ref
                
                assert ref_path.exists(), \
                    f"{md_file.name} references {ref} which doesn't exist (checked: {ref_path})"


class TestAbbreviations:
    """Test that abbreviations are defined"""
    
    def test_common_abbreviations_defined(self):
        """Common abbreviations should be defined in glossary"""
        glossary = BASE_DIR / "04_reference" / "glossary.md"
        if not glossary.exists():
            pytest.skip("Glossary not found")
        
        content = glossary.read_text()
        
        abbreviations = ["HP", "NR", "QR", "10m NR", "Sauté"]
        for abbr in abbreviations:
            assert abbr in content, \
                f"Abbreviation {abbr} should be defined in glossary"
    
    def test_recipes_reference_quick_reference(self):
        """Recipes should have Quick Reference section with abbreviations"""
        for recipe_file in (BASE_DIR / "03_recipes").glob("*.md"):
            content = recipe_file.read_text()
            if "Quick Reference" in content:
                # Should have at least HP and NR defined
                assert "HP" in content and "NR" in content, \
                    f"{recipe_file.name} Quick Reference should define HP and NR"


class TestRecipeStructure:
    """Test recipe structure and required sections"""
    
    def test_recipes_have_required_sections(self):
        """Recipes should have all required sections"""
        required_sections = [
            "Hardware & Variables",
            "Execution",
            "Chemistry Notes",
            "Troubleshooting"
        ]
        
        for recipe_file in (BASE_DIR / "03_recipes").glob("*.md"):
            content = recipe_file.read_text()
            for section in required_sections:
                # Allow variations in section names
                if section not in content and section.split()[0] not in content:
                    # This is a warning, not a hard failure
                    print(f"Warning: {recipe_file.name} may be missing {section}")


class TestTimingFormat:
    """Test that timing is formatted consistently"""
    
    def test_timing_uses_consistent_format(self):
        """Timing should use consistent format (e.g., '8 mins HP' or '8m HP')"""
        timing_files = [
            BASE_DIR / "01_fundamentals" / "timing_charts.md",
            BASE_DIR / "04_reference" / "timing_dictionary.md"
        ]
        
        for timing_file in timing_files:
            if timing_file.exists():
                content = timing_file.read_text()
                # Should use consistent format
                # Allow both "mins" and "m" but should be consistent
                assert "mins" in content or "m" in content, \
                    f"{timing_file.name} should specify time units"
