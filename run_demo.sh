#!/bin/bash
# Quick demo script for the technical interview

echo "🧠 AI Therapy Evaluation System Demo"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Run a quick 3-conversation demo with verbose output
echo ""
echo "Running evaluation with 3 conversations..."
echo ""
python -m src.main --conversations 3 --verbose

# Show a specific transcript
echo ""
echo "Showing detailed transcript for conversation 1..."
echo ""
python -m src.main --conversations 3 --show-transcript 1

echo ""
echo "Demo complete! Check data/results/ for saved evaluation data."