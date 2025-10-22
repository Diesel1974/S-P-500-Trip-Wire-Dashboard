# Reddit Stock Market Sentiment Scraper

A Python application that scrapes Reddit for stock market sentiment analysis with a user-friendly GUI interface.

## Features

- **Targeted Scraping**: Focuses on stock market subreddits (r/wallstreetbets, r/stocks, r/investing, etc.)
- **Sentiment Analysis**: Uses VADER sentiment analysis to determine bullish/bearish sentiment
- **Stock Ticker Detection**: Automatically extracts stock ticker symbols from posts
- **Easy-to-Use GUI**: Simple interface with button to launch analysis
- **Real-Time Results**: Displays comprehensive summary in text window
- **Export Functionality**: Save results to text file

## Monitored Subreddits

- r/wallstreetbets
- r/stocks
- r/investing
- r/StockMarket
- r/options
- r/pennystocks
- r/SecurityAnalysis
- r/ValueInvesting

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Get Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Log in with your Reddit account
3. Scroll to the bottom and click "create another app..."
4. Fill in the form:
   - **Name**: Choose any name (e.g., "Stock Sentiment Scraper")
   - **App Type**: Select "script"
   - **Description**: Optional
   - **About URL**: Optional
   - **Redirect URI**: http://localhost:8080
5. Click "create app"
6. Note your credentials:
   - **Client ID**: The string under the app name
   - **Client Secret**: The string labeled "secret"

## Usage

### Running the GUI Application

```bash
python reddit_sentiment_gui.py
```

### Using the GUI

1. **Enter Reddit API Credentials**:
   - Paste your Client ID
   - Paste your Client Secret
   - Keep the default User Agent or customize it

2. **Configure Settings**:
   - Set the number of posts per subreddit (10-100)
   - Check "Save credentials" to remember them for next time

3. **Start Analysis**:
   - Click the "Start Analysis" button
   - Wait while the scraper collects and analyzes data
   - Progress bar will show activity

4. **View Results**:
   - Results appear in the text window
   - Shows overall market sentiment (Bullish/Bearish/Neutral)
   - Lists top 10 most mentioned stocks
   - Displays sentiment distribution
   - Provides key insights

5. **Export Results** (Optional):
   - Click "Export Results" to save to a text file

## Analysis Output

The scraper provides:

- **Total Posts Analyzed**: Number of posts scraped from all subreddits
- **Overall Market Sentiment**: Bullish, Bearish, or Neutral
- **Average Sentiment Score**: Range from -1 (very negative) to +1 (very positive)
- **Sentiment Distribution**: Percentage of positive, neutral, and negative posts
- **Top 10 Most Mentioned Stocks**: With mention count and individual sentiment
- **Key Insights**: Automated interpretation of the data

## Example Output

```
================================================================================
REDDIT STOCK MARKET SENTIMENT ANALYSIS
================================================================================

Analysis Time: 2025-10-22 14:30:45
Total Posts Analyzed: 200

Scraping completed from 8 subreddits:
  - r/wallstreetbets: 25 posts
  - r/stocks: 25 posts
  - r/investing: 25 posts
  ...

--------------------------------------------------------------------------------
OVERALL MARKET SENTIMENT
--------------------------------------------------------------------------------
Market Sentiment: BULLISH
Average Sentiment Score: 0.152 (Range: -1 to +1)

Sentiment Distribution:
  POSITIVE: 95 posts (47.5%)
  NEUTRAL:  70 posts (35.0%)
  NEGATIVE: 35 posts (17.5%)

--------------------------------------------------------------------------------
TOP 10 MOST MENTIONED STOCKS
--------------------------------------------------------------------------------
 1. $SPY   -  45 mentions - Sentiment: BULLISH  (+0.210)
 2. $TSLA  -  38 mentions - Sentiment: BULLISH  (+0.185)
 3. $AAPL  -  32 mentions - Sentiment: NEUTRAL  (+0.045)
 ...
```

## How It Works

### 1. Reddit Scraping
- Connects to Reddit API using PRAW library
- Scrapes "hot" posts from target subreddits
- Collects post titles, text, scores, and comments

### 2. Sentiment Analysis
- Uses VADER (Valence Aware Dictionary and sEntiment Reasoner)
- Analyzes combined title + text of each post
- Assigns compound sentiment score (-1 to +1)
- Classifies as Positive, Neutral, or Negative

### 3. Stock Ticker Extraction
- Uses regex patterns to find stock tickers
- Looks for $TICKER format (e.g., $AAPL)
- Also finds standalone uppercase 2-5 letter words
- Filters out common non-ticker words

### 4. Summary Generation
- Aggregates sentiment across all posts
- Calculates per-ticker sentiment averages
- Ranks stocks by mention frequency
- Generates human-readable insights

## Troubleshooting

### "Error initializing Reddit client"
- Double-check your Client ID and Client Secret
- Ensure you created a "script" type app, not "web app"
- Verify you're using the correct credentials

### "No posts were scraped"
- Check your internet connection
- Verify your Reddit account is in good standing
- Some subreddits may have rate limits

### Missing tkinter
If you get an error about tkinter not being installed:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS**: tkinter should be included with Python
- **Windows**: tkinter should be included with Python

## API Rate Limits

Reddit API has rate limits:
- Standard: 60 requests per minute
- The scraper respects these limits automatically
- Be patient when analyzing many posts

## Privacy & Security

- Credentials are stored locally in `reddit_config.json` (if enabled)
- Never share your API credentials
- The scraper only reads public posts
- No personal data is collected

## Files

- `reddit_scraper.py`: Core scraping and analysis logic
- `reddit_sentiment_gui.py`: GUI application
- `requirements.txt`: Python dependencies
- `reddit_config.json`: Saved credentials (created on first run)

## Advanced Usage

### Using the Scraper Module Directly

You can also use the scraper programmatically:

```python
from reddit_scraper import RedditStockSentimentScraper

# Initialize scraper
scraper = RedditStockSentimentScraper()

# Set up Reddit client
scraper.initialize_reddit_client(
    client_id="your_client_id",
    client_secret="your_client_secret",
    user_agent="your_user_agent"
)

# Scrape all subreddits
posts = scraper.scrape_all_subreddits(post_limit_per_sub=25)

# Generate summary
summary = scraper.generate_summary(posts)
print(summary)
```

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is provided as-is for educational and informational purposes.

## Disclaimer

This tool is for informational purposes only. The sentiment analysis is based on Reddit posts and should not be used as the sole basis for investment decisions. Always do your own research and consult with financial professionals before making investment decisions.

## Support

For issues or questions:
- Check the troubleshooting section above
- Review Reddit API documentation: https://www.reddit.com/dev/api
- PRAW documentation: https://praw.readthedocs.io/
