# Bachelor Cookbook Test Suite

## Overview

This test suite validates the cookbook's consistency, accuracy, and completeness using pytest. It ensures:
- Timing information is consistent across all files
- Recipes follow the correct format
- Cross-references are valid
- Content is complete and accurate

## Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Or install pytest directly
pip install pytest
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_timing_consistency.py

# Run specific test
pytest tests/test_timing_consistency.py::TestTimingConsistency::test_chicken_thighs_timing

# Run with coverage (if pytest-cov installed)
pytest --cov=. --cov-report=html
```

## Test Categories

### `test_timing_consistency.py`
- Validates timing information across timing charts, dictionary, and recipes
- Ensures chicken cuts have correct timing
- Verifies rice timing is consistent
- Checks that Natural Release is specified

### `test_references.py`
- Validates file references exist
- Checks abbreviations are defined
- Verifies cross-references work

### `test_content_validation.py`
- Validates content completeness
- Checks required sections exist
- Verifies formatting consistency

## Adding New Tests

When adding new content:
1. Add tests for new timing information
2. Update reference tests if adding new files
3. Add validation for new recipe sections

## Continuous Validation

Run tests before committing:
```bash
pytest
```

This ensures the cookbook maintains quality and consistency as it grows.
