@echo off
REM Sentiment Stock Agent Startup Script for Windows

echo =========================================
echo   Sentiment Stock Agent Startup
echo =========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist "venv\installed.txt" (
    echo Installing requirements...
    pip install -r requirements.txt

    REM Download NLTK data for TextBlob
    echo Downloading NLTK data...
    python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"

    echo. > venv\installed.txt
    echo Installation complete!
) else (
    echo Requirements already installed.
)

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Copying .env.example to .env...
    copy .env.example .env
    echo.
    echo Please edit .env and add your API keys:
    echo   - NEWS_API_KEY (get from https://newsapi.org/)
    echo.
    pause
)

REM Start the API server
echo.
echo =========================================
echo   Starting Sentiment Stock Agent API
echo =========================================
echo.
echo API will be available at: http://localhost:5000
echo API Documentation: http://localhost:5000/
echo.
echo Press Ctrl+C to stop the server
echo.

python api.py
