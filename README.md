# S-P-500-Trip-Wire-Dashboard

An interactive web dashboard that monitors key risk indicators for the S&P 500 index, now enhanced with an intelligent **Sentiment Stock Agent** that analyzes market sentiment across AI, data centers, and power generation sectors.

## Features

### Trip-Wire Dashboard
- Real-time monitoring of S&P 500 risk indicators
- Interactive charts and gauges
- VIX tracking, credit spreads, yield curves
- Market breadth analysis
- Dark/Light theme support
- Auto-refresh functionality

### Sentiment Stock Agent (NEW!)
- **Stock Validation**: Real-time stock data and price validation
- **Web Scraping**: Automatically scrapes news from multiple sources
- **Sentiment Analysis**: Dual-engine sentiment scoring (TextBlob + VADER)
- **Tech Sector Focus**: AI, data centers, power generation
- **News Aggregation**: Latest tech news with sentiment classification
- **Smart Recommendations**: AI-powered buy/sell/hold suggestions

### Stock GUI - Trading Terminal (NEW!)
- **Modern UI**: Sleek glassmorphism design with animated gradients
- **Real-time Charts**: Interactive price charts with hover tooltips
- **Watchlist Management**: Track multiple stocks simultaneously
- **Sentiment Gauges**: Visual sentiment indicators with circular progress
- **Live News Feed**: Latest news with sentiment classification
- **Buy/Sell/Hold Signals**: AI-powered trading recommendations
- **Sector Overview**: Quick view of AI, Data Centers, and Power sector sentiment
- **Responsive Design**: Works on desktop and mobile devices

## Quick Start

### Dashboard
Simply open `index.html` in your browser to view the trip-wire dashboard.

### Stock GUI Trading Terminal
Open `stock_gui.html` in your browser for the advanced trading interface with real-time sentiment analysis.

### With Sentiment Agent

#### Linux/Mac
```bash
./run_sentiment_agent.sh
```

#### Windows
```bash
run_sentiment_agent.bat
```

The API will be available at `http://localhost:5000`

## Documentation

- **Trip-Wire Dashboard**: Open `index.html` for S&P 500 risk monitoring
- **Stock GUI**: Open `stock_gui.html` for the advanced trading terminal
- **Sentiment Agent API**: See [SENTIMENT_AGENT_README.md](SENTIMENT_AGENT_README.md) for detailed API documentation

## Installation (Sentiment Agent)

1. **Install Python 3.8+**

2. **Set up environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure API keys**:
   ```bash
   cp .env.example .env
   # Edit .env and add your News API key from https://newsapi.org/
   ```

4. **Run the agent**:
   ```bash
   python api.py
   ```

## API Quick Examples

### Validate a Stock
```bash
curl http://localhost:5000/validate/NVDA
```

### Get AI Sector Sentiment
```bash
curl http://localhost:5000/sentiment/sector/ai
```

### Analyze Stock with Sentiment
```bash
curl http://localhost:5000/analyze/NVDA
```

### Search Tech News
```bash
curl http://localhost:5000/sentiment/news?sector=ai&days=7
```

## Monitored Sectors

- **AI**: NVDA, MSFT, GOOGL, META, AMD, INTC, ORCL, CRM, ADBE
- **Data Centers**: EQIX, DLR, AMT, CCI, SBAC, MSFT, GOOGL, AMZN
- **Power Generation**: NEE, DUK, SO, D, AEP, EXC, SRE, XEL

## Project Structure

```
S-P-500-Trip-Wire-Dashboard/
├── index.html                    # Trip-Wire Dashboard (risk monitoring)
├── stock_gui.html                # Stock GUI Trading Terminal (NEW!)
├── sentiment_stock_agent.py      # Core sentiment analysis engine
├── api.py                        # Flask REST API
├── requirements.txt              # Python dependencies
├── .env.example                  # Configuration template
├── run_sentiment_agent.sh        # Linux/Mac startup script
├── run_sentiment_agent.bat       # Windows startup script
├── README.md                     # This file
└── SENTIMENT_AGENT_README.md     # Detailed API documentation
```

## Technologies

### Frontend
- HTML5, CSS3, JavaScript
- Tailwind CSS
- Chart.js with Financial Plugin
- FontAwesome Icons

### Backend (Sentiment Agent)
- Python 3.8+
- Flask (REST API)
- yfinance (Stock data)
- BeautifulSoup4 (Web scraping)
- TextBlob & VADER (Sentiment analysis)
- NewsAPI & RSS feeds (News aggregation)
- pandas, numpy (Data processing)

## License

MIT License
