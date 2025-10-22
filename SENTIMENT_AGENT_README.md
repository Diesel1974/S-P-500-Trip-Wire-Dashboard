# Sentiment Stock Agent

An intelligent agent that validates stocks and performs sentiment analysis on tech sectors including AI, data centers, and power generation.

## Features

### Stock Validation
- Real-time stock price validation using Yahoo Finance
- Comprehensive stock information (price, change, volume, market cap)
- Support for all major stock tickers

### Sentiment Analysis
- **Dual sentiment engines**: TextBlob and VADER
- **Multi-source news aggregation**: News API + Google News RSS
- **Sector-specific analysis**:
  - **AI**: artificial intelligence, machine learning, GPT, neural networks
  - **Data Centers**: cloud computing, hyperscale, edge computing, colocation
  - **Power Generation**: renewable energy, solar, wind, nuclear, grid infrastructure

### Web Scraping
- Google News RSS feed scraping
- News API integration for real-time articles
- Automatic sentiment scoring for all articles
- Rate limiting and caching to optimize performance

### Tech News Search
- Latest news from the past 7 days (configurable)
- Keyword-based search across multiple tech sectors
- Sentiment classification: positive, negative, neutral
- Source attribution and publication timestamps

## Installation

### 1. Clone the repository
```bash
cd S-P-500-Trip-Wire-Dashboard
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API keys
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Get your free API keys:
- **News API**: https://newsapi.org/ (100 requests/day free tier)
- **Alpha Vantage** (optional): https://www.alphavantage.co/

### 5. Download NLTK data (for TextBlob)
```python
python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"
```

## Usage

### Running the API Server

```bash
python api.py
```

The API will be available at `http://localhost:5000`

### API Endpoints

#### 1. Get API Information
```bash
GET /
```

#### 2. Health Check
```bash
GET /health
```

#### 3. Validate Stock
```bash
GET /validate/<ticker>

# Example
curl http://localhost:5000/validate/NVDA
```

Response:
```json
{
  "valid": true,
  "ticker": "NVDA",
  "name": "NVIDIA Corporation",
  "sector": "Technology",
  "current_price": 875.50,
  "change": 12.34,
  "change_pct": 1.43,
  "market_cap": 2150000000000,
  "volume": 45678900
}
```

#### 4. Get Tech News with Sentiment
```bash
GET /sentiment/news?sector=ai&days=7

# Examples
curl http://localhost:5000/sentiment/news?sector=ai&days=7
curl http://localhost:5000/sentiment/news?sector=data_centers&days=3
curl http://localhost:5000/sentiment/news?sector=all&days=14
```

Response:
```json
{
  "sector": "ai",
  "days_back": 7,
  "article_count": 25,
  "articles": [
    {
      "sector": "ai",
      "title": "NVIDIA Announces Breakthrough in AI Computing",
      "description": "New GPU architecture delivers 10x performance...",
      "url": "https://...",
      "source": "TechCrunch",
      "published_at": "2025-10-21T14:30:00Z",
      "sentiment_textblob": {
        "polarity": 0.65,
        "subjectivity": 0.42,
        "classification": "positive"
      },
      "sentiment_vader": {
        "compound": 0.72,
        "positive": 0.35,
        "negative": 0.02,
        "neutral": 0.63,
        "classification": "positive"
      },
      "overall_sentiment": "positive"
    }
  ]
}
```

#### 5. Get Sector Sentiment Summary
```bash
GET /sentiment/sector/<sector>?days=7

# Examples
curl http://localhost:5000/sentiment/sector/ai
curl http://localhost:5000/sentiment/sector/data_centers
curl http://localhost:5000/sentiment/sector/power_generation
```

Response:
```json
{
  "sector": "ai",
  "article_count": 25,
  "sentiment_summary": {
    "overall": "positive",
    "avg_vader_compound": 0.45,
    "avg_textblob_polarity": 0.38,
    "positive_count": 18,
    "negative_count": 3,
    "neutral_count": 4
  },
  "top_articles": [...],
  "last_updated": "2025-10-22T10:30:00"
}
```

#### 6. Get All Sectors Overview
```bash
GET /sentiment/overview

curl http://localhost:5000/sentiment/overview
```

#### 7. Analyze Stock with Sector Sentiment
```bash
GET /analyze/<ticker>

# Example
curl http://localhost:5000/analyze/NVDA
```

Response:
```json
{
  "stock": {
    "valid": true,
    "ticker": "NVDA",
    "name": "NVIDIA Corporation",
    "current_price": 875.50,
    "change_pct": 1.43
  },
  "relevant_sectors": ["ai"],
  "sector_sentiments": {
    "ai": {
      "sentiment_summary": {
        "overall": "positive",
        "avg_vader_compound": 0.45
      },
      "top_articles": [...]
    }
  },
  "recommendation": {
    "action": "buy",
    "confidence": "high",
    "reason": "Strong positive sentiment and upward price momentum"
  }
}
```

#### 8. Batch Analysis
```bash
POST /analyze/batch
Content-Type: application/json

{
  "tickers": ["NVDA", "MSFT", "GOOGL", "EQIX"]
}

# Example
curl -X POST http://localhost:5000/analyze/batch \
  -H "Content-Type: application/json" \
  -d '{"tickers": ["NVDA", "MSFT", "GOOGL"]}'
```

#### 9. Get Tracked Stocks
```bash
GET /sectors/stocks

curl http://localhost:5000/sectors/stocks
```

#### 10. Clear Cache
```bash
POST /cache/clear

curl -X POST http://localhost:5000/cache/clear
```

### Using the Agent Programmatically

```python
from sentiment_stock_agent import SentimentStockAgent

# Initialize agent
agent = SentimentStockAgent()

# Validate a stock
stock_data = agent.validate_stock('NVDA')
print(stock_data)

# Get sector sentiment
ai_sentiment = agent.get_sector_sentiment_summary(sector='ai', days_back=7)
print(ai_sentiment)

# Full analysis
analysis = agent.analyze_stock_with_sector_sentiment('NVDA')
print(analysis)

# Search tech news
news = agent.search_tech_news(sector='data_centers', days_back=7)
for article in news:
    print(f"{article['title']}: {article['overall_sentiment']}")
```

## Tracked Stocks by Sector

### AI Sector
- NVDA (NVIDIA)
- MSFT (Microsoft)
- GOOGL (Google)
- META (Meta)
- AMD (AMD)
- INTC (Intel)
- ORCL (Oracle)
- CRM (Salesforce)
- ADBE (Adobe)

### Data Centers
- EQIX (Equinix)
- DLR (Digital Realty)
- AMT (American Tower)
- CCI (Crown Castle)
- SBAC (SBA Communications)
- MSFT, GOOGL, AMZN (Hyperscalers)

### Power Generation
- NEE (NextEra Energy)
- DUK (Duke Energy)
- SO (Southern Company)
- D (Dominion Energy)
- AEP (American Electric Power)
- EXC (Exelon)
- SRE (Sempra Energy)
- XEL (Xcel Energy)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Sentiment Stock Agent                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │    Stock     │  │  Sentiment   │  │   Web        │  │
│  │  Validation  │  │   Analysis   │  │  Scraping    │  │
│  │              │  │              │  │              │  │
│  │ - Yahoo Fin  │  │ - TextBlob   │  │ - News API   │  │
│  │ - Price Data │  │ - VADER      │  │ - Google RSS │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Flask REST API                       │  │
│  │  - CORS enabled                                   │  │
│  │  - 5-minute caching                              │  │
│  │  - Rate limiting                                  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Caching

The API implements a 5-minute cache to reduce external API calls and improve performance:
- Stock validations cached for 5 minutes
- News searches cached for 5 minutes
- Sector summaries cached for 5 minutes

Clear cache manually: `POST /cache/clear`

## Rate Limiting

The agent implements automatic rate limiting:
- 0.5 second delay between News API requests
- 1 second delay between sector analyses
- Maximum 20 tickers per batch request

## Testing

Run the built-in test suite:

```bash
python sentiment_stock_agent.py
```

This will test:
- Stock validation for NVDA, MSFT, EQIX, NEE
- Sentiment analysis (TextBlob and VADER)
- Tech news search
- Sector sentiment summaries
- Full stock analysis

## Sentiment Scoring

### TextBlob
- **Polarity**: -1 (negative) to +1 (positive)
- **Subjectivity**: 0 (objective) to 1 (subjective)

### VADER (Valence Aware Dictionary and sEntiment Reasoner)
- **Compound**: -1 (negative) to +1 (positive)
- **Positive/Negative/Neutral**: Individual component scores
- Optimized for social media and news

### Classification Thresholds
- **Positive**: compound > 0.05
- **Negative**: compound < -0.05
- **Neutral**: -0.05 ≤ compound ≤ 0.05

## Recommendation Logic

The agent generates buy/sell/hold recommendations based on:

1. **Sector sentiment** (VADER compound score)
2. **Stock price momentum** (% change)

| Sentiment | Price Change | Action | Confidence |
|-----------|--------------|--------|------------|
| > 0.2     | Positive     | BUY    | High       |
| > 0.1     | Any          | BUY    | Medium     |
| < -0.2    | Negative     | SELL   | High       |
| < -0.1    | Any          | SELL   | Medium     |
| Neutral   | Any          | HOLD   | Medium     |

## Troubleshooting

### No news articles found
- Check your News API key in `.env`
- Verify your internet connection
- The free tier has a 100 requests/day limit
- Agent will fall back to Google News RSS if News API fails

### Stock validation fails
- Ensure the ticker symbol is correct
- Yahoo Finance may have rate limits
- Some international stocks may not be available

### Slow response times
- First request after startup is slower (downloads data)
- Subsequent requests use caching (5 min cache duration)
- Consider reducing `days_back` parameter for faster searches

## Future Enhancements

- [ ] Add support for Twitter/X sentiment analysis
- [ ] Implement Reddit sentiment scraping (r/wallstreetbets, r/stocks)
- [ ] Add historical sentiment tracking and trends
- [ ] Implement machine learning models for better predictions
- [ ] Add websocket support for real-time updates
- [ ] Create dashboard visualizations for sentiment data
- [ ] Add email/SMS alerts for significant sentiment changes
- [ ] Implement portfolio tracking with sentiment correlation

## License

MIT License - Feel free to use and modify for your projects

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## Support

For issues or questions, please open a GitHub issue.
