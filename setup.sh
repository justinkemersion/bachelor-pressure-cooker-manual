#!/bin/bash
# Setup script for Bachelor Cookbook test suite

echo "Setting up Bachelor Cookbook test environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements-dev.txt

# Run tests
echo ""
echo "Running test suite..."
pytest tests/ -v

echo ""
echo "Setup complete! To activate the virtual environment in the future:"
echo "  source venv/bin/activate"
echo ""
echo "To run tests:"
echo "  pytest tests/ -v"
