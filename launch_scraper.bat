@echo off
REM Launcher script for Reddit Stock Market Sentiment Scraper (Windows)

echo Reddit Stock Market Sentiment Scraper
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.7 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import praw" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies.
        echo Please run: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

REM Launch the GUI
echo Launching GUI...
python reddit_sentiment_gui.py

pause
