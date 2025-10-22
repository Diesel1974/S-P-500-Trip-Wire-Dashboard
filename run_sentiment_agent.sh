#!/bin/bash

# Sentiment Stock Agent Startup Script

echo "========================================="
echo "  Sentiment Stock Agent Startup"
echo "========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/installed.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt

    # Download NLTK data for TextBlob
    echo "Downloading NLTK data..."
    python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"

    touch venv/installed.txt
    echo "Installation complete!"
else
    echo "Requirements already installed."
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo ""
    echo "Please edit .env and add your API keys:"
    echo "  - NEWS_API_KEY (get from https://newsapi.org/)"
    echo ""
    read -p "Press Enter to continue (the agent will work with limited functionality)..."
fi

# Start the API server
echo ""
echo "========================================="
echo "  Starting Sentiment Stock Agent API"
echo "========================================="
echo ""
echo "API will be available at: http://localhost:5000"
echo "API Documentation: http://localhost:5000/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python api.py
