#!/bin/bash
# Launcher script for Reddit Stock Market Sentiment Scraper

echo "Reddit Stock Market Sentiment Scraper"
echo "======================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.7 or higher."
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
python3 -c "import praw" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies."
        echo "Please run: pip3 install -r requirements.txt"
        exit 1
    fi
fi

# Launch the GUI
echo "Launching GUI..."
python3 reddit_sentiment_gui.py
