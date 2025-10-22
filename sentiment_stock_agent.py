"""
Sentiment Stock Agent - Validates stocks and analyzes web sentiment
for tech sectors including AI, data centers, and power generation
"""

import os
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json

# Data processing
import pandas as pd
import numpy as np

# Stock data
import yfinance as yf

# Web scraping
import requests
from bs4 import BeautifulSoup

# Sentiment analysis
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# News
import feedparser
from newsapi import NewsApiClient

# Configuration
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class SentimentStockAgent:
    """
    Agent that validates stocks and performs sentiment analysis on tech sectors
    """

    def __init__(self, newsapi_key: Optional[str] = None):
        """
        Initialize the sentiment stock agent

        Args:
            newsapi_key: API key for News API (optional, will use env var if not provided)
        """
        self.newsapi_key = newsapi_key or os.getenv('NEWS_API_KEY')
        self.vader = SentimentIntensityAnalyzer()

        # Initialize news API client if key is available
        self.news_client = None
        if self.newsapi_key:
            try:
                self.news_client = NewsApiClient(api_key=self.newsapi_key)
            except Exception as e:
                logger.warning(f"Failed to initialize News API: {e}")

        # Tech sector keywords
        self.sector_keywords = {
            'ai': ['artificial intelligence', 'AI', 'machine learning', 'deep learning',
                   'neural networks', 'ChatGPT', 'GPT', 'LLM', 'generative AI'],
            'data_centers': ['data center', 'datacenter', 'cloud computing', 'server',
                            'hyperscale', 'colocation', 'edge computing'],
            'power_generation': ['power generation', 'energy', 'renewable energy',
                                'solar power', 'wind power', 'nuclear energy',
                                'electricity', 'grid', 'power infrastructure']
        }

        # S&P 500 tech stocks by sector
        self.tech_stocks = {
            'ai': ['NVDA', 'MSFT', 'GOOGL', 'META', 'AMD', 'INTC', 'ORCL', 'CRM', 'ADBE'],
            'data_centers': ['EQIX', 'DLR', 'AMT', 'CCI', 'SBAC', 'MSFT', 'GOOGL', 'AMZN'],
            'power_generation': ['NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'SRE', 'XEL']
        }

        logger.info("Sentiment Stock Agent initialized")

    def validate_stock(self, ticker: str) -> Dict:
        """
        Validate a stock ticker and get its current information

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with stock validation data
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="5d")

            if hist.empty:
                return {
                    'valid': False,
                    'ticker': ticker,
                    'error': 'No data available for this ticker'
                }

            current_price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            change = current_price - prev_price
            change_pct = (change / prev_price * 100) if prev_price != 0 else 0

            return {
                'valid': True,
                'ticker': ticker,
                'name': info.get('longName', ticker),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'current_price': round(float(current_price), 2),
                'change': round(float(change), 2),
                'change_pct': round(float(change_pct), 2),
                'market_cap': info.get('marketCap', 0),
                'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist else 0,
                'last_updated': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error validating stock {ticker}: {e}")
            return {
                'valid': False,
                'ticker': ticker,
                'error': str(e)
            }

    def analyze_sentiment_textblob(self, text: str) -> Dict:
        """
        Analyze sentiment using TextBlob

        Args:
            text: Text to analyze

        Returns:
            Dictionary with sentiment scores
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 to 1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1

        return {
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3),
            'classification': 'positive' if polarity > 0.1 else 'negative' if polarity < -0.1 else 'neutral'
        }

    def analyze_sentiment_vader(self, text: str) -> Dict:
        """
        Analyze sentiment using VADER (optimized for social media)

        Args:
            text: Text to analyze

        Returns:
            Dictionary with sentiment scores
        """
        scores = self.vader.polarity_scores(text)

        return {
            'compound': round(scores['compound'], 3),
            'positive': round(scores['pos'], 3),
            'negative': round(scores['neg'], 3),
            'neutral': round(scores['neu'], 3),
            'classification': 'positive' if scores['compound'] > 0.05 else 'negative' if scores['compound'] < -0.05 else 'neutral'
        }

    def scrape_google_news(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Scrape Google News for a query using RSS feeds

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            List of news articles
        """
        try:
            # Google News RSS feed
            url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en-US&gl=US&ceid=US:en"
            feed = feedparser.parse(url)

            articles = []
            for entry in feed.entries[:num_results]:
                articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.get('published', ''),
                    'source': entry.get('source', {}).get('title', 'Unknown'),
                    'summary': entry.get('summary', '')
                })

            return articles

        except Exception as e:
            logger.error(f"Error scraping Google News: {e}")
            return []

    def search_tech_news(self, sector: str = 'all', days_back: int = 7) -> List[Dict]:
        """
        Search for latest tech news with sentiment analysis

        Args:
            sector: Sector to search ('ai', 'data_centers', 'power_generation', or 'all')
            days_back: Number of days to search back

        Returns:
            List of news articles with sentiment scores
        """
        articles_with_sentiment = []

        # Determine which sectors to search
        sectors_to_search = [sector] if sector != 'all' else list(self.sector_keywords.keys())

        for sect in sectors_to_search:
            if sect not in self.sector_keywords:
                continue

            keywords = self.sector_keywords[sect]

            # Try News API first if available
            if self.news_client:
                try:
                    from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

                    for keyword in keywords[:3]:  # Limit API calls
                        try:
                            results = self.news_client.get_everything(
                                q=keyword,
                                from_param=from_date,
                                language='en',
                                sort_by='publishedAt',
                                page_size=5
                            )

                            if results and results.get('articles'):
                                for article in results['articles']:
                                    text = f"{article.get('title', '')} {article.get('description', '')}"

                                    sentiment_tb = self.analyze_sentiment_textblob(text)
                                    sentiment_vader = self.analyze_sentiment_vader(text)

                                    articles_with_sentiment.append({
                                        'sector': sect,
                                        'title': article.get('title', ''),
                                        'description': article.get('description', ''),
                                        'url': article.get('url', ''),
                                        'source': article.get('source', {}).get('name', 'Unknown'),
                                        'published_at': article.get('publishedAt', ''),
                                        'sentiment_textblob': sentiment_tb,
                                        'sentiment_vader': sentiment_vader,
                                        'overall_sentiment': sentiment_vader['classification']
                                    })

                            time.sleep(0.5)  # Rate limiting

                        except Exception as e:
                            logger.error(f"Error fetching news for {keyword}: {e}")
                            continue

                except Exception as e:
                    logger.error(f"Error with News API: {e}")

            # Fallback to Google News RSS
            if len(articles_with_sentiment) < 10:
                for keyword in keywords[:2]:
                    google_articles = self.scrape_google_news(keyword, num_results=5)

                    for article in google_articles:
                        text = f"{article.get('title', '')} {article.get('summary', '')}"

                        sentiment_tb = self.analyze_sentiment_textblob(text)
                        sentiment_vader = self.analyze_sentiment_vader(text)

                        articles_with_sentiment.append({
                            'sector': sect,
                            'title': article.get('title', ''),
                            'description': article.get('summary', ''),
                            'url': article.get('link', ''),
                            'source': article.get('source', 'Google News'),
                            'published_at': article.get('published', ''),
                            'sentiment_textblob': sentiment_tb,
                            'sentiment_vader': sentiment_vader,
                            'overall_sentiment': sentiment_vader['classification']
                        })

        return articles_with_sentiment

    def get_sector_sentiment_summary(self, sector: str = 'all', days_back: int = 7) -> Dict:
        """
        Get aggregated sentiment summary for a sector

        Args:
            sector: Sector to analyze
            days_back: Number of days to analyze

        Returns:
            Dictionary with sentiment summary
        """
        articles = self.search_tech_news(sector=sector, days_back=days_back)

        if not articles:
            return {
                'sector': sector,
                'article_count': 0,
                'error': 'No articles found'
            }

        # Calculate averages
        vader_compounds = [a['sentiment_vader']['compound'] for a in articles]
        tb_polarities = [a['sentiment_textblob']['polarity'] for a in articles]

        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        for article in articles:
            sentiment_counts[article['overall_sentiment']] += 1

        avg_vader = np.mean(vader_compounds) if vader_compounds else 0
        avg_textblob = np.mean(tb_polarities) if tb_polarities else 0

        overall = 'positive' if avg_vader > 0.05 else 'negative' if avg_vader < -0.05 else 'neutral'

        return {
            'sector': sector,
            'article_count': len(articles),
            'sentiment_summary': {
                'overall': overall,
                'avg_vader_compound': round(avg_vader, 3),
                'avg_textblob_polarity': round(avg_textblob, 3),
                'positive_count': sentiment_counts['positive'],
                'negative_count': sentiment_counts['negative'],
                'neutral_count': sentiment_counts['neutral']
            },
            'top_articles': articles[:5],
            'last_updated': datetime.now().isoformat()
        }

    def analyze_stock_with_sector_sentiment(self, ticker: str) -> Dict:
        """
        Analyze a stock and correlate with sector sentiment

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with stock data and correlated sentiment
        """
        # Validate stock
        stock_data = self.validate_stock(ticker)

        if not stock_data.get('valid'):
            return stock_data

        # Determine which sector(s) this stock belongs to
        relevant_sectors = []
        for sector, tickers in self.tech_stocks.items():
            if ticker in tickers:
                relevant_sectors.append(sector)

        # Get sentiment for relevant sectors
        sector_sentiments = {}
        for sector in relevant_sectors:
            sector_sentiments[sector] = self.get_sector_sentiment_summary(sector=sector, days_back=7)

        # If no specific sector match, use 'all'
        if not relevant_sectors:
            sector_sentiments['general'] = self.get_sector_sentiment_summary(sector='all', days_back=7)

        return {
            'stock': stock_data,
            'relevant_sectors': relevant_sectors,
            'sector_sentiments': sector_sentiments,
            'recommendation': self._generate_recommendation(stock_data, sector_sentiments),
            'analysis_timestamp': datetime.now().isoformat()
        }

    def _generate_recommendation(self, stock_data: Dict, sector_sentiments: Dict) -> Dict:
        """
        Generate a trading recommendation based on stock and sentiment data

        Args:
            stock_data: Stock validation data
            sector_sentiments: Sentiment analysis for relevant sectors

        Returns:
            Dictionary with recommendation
        """
        if not sector_sentiments:
            return {'action': 'hold', 'confidence': 'low', 'reason': 'Insufficient sentiment data'}

        # Calculate average sentiment across sectors
        avg_sentiments = []
        for sector, data in sector_sentiments.items():
            if 'sentiment_summary' in data:
                avg_sentiments.append(data['sentiment_summary']['avg_vader_compound'])

        if not avg_sentiments:
            return {'action': 'hold', 'confidence': 'low', 'reason': 'No sentiment data available'}

        avg_sentiment = np.mean(avg_sentiments)
        stock_change = stock_data.get('change_pct', 0)

        # Simple recommendation logic
        if avg_sentiment > 0.2 and stock_change > 0:
            return {
                'action': 'buy',
                'confidence': 'high',
                'reason': 'Strong positive sentiment and upward price momentum'
            }
        elif avg_sentiment > 0.1:
            return {
                'action': 'buy',
                'confidence': 'medium',
                'reason': 'Positive sentiment in sector'
            }
        elif avg_sentiment < -0.2 and stock_change < 0:
            return {
                'action': 'sell',
                'confidence': 'high',
                'reason': 'Strong negative sentiment and downward price momentum'
            }
        elif avg_sentiment < -0.1:
            return {
                'action': 'sell',
                'confidence': 'medium',
                'reason': 'Negative sentiment in sector'
            }
        else:
            return {
                'action': 'hold',
                'confidence': 'medium',
                'reason': 'Neutral sentiment and price action'
            }

    def get_all_tech_sectors_overview(self) -> Dict:
        """
        Get sentiment overview for all tech sectors

        Returns:
            Dictionary with all sector sentiments
        """
        overview = {
            'timestamp': datetime.now().isoformat(),
            'sectors': {}
        }

        for sector in self.sector_keywords.keys():
            logger.info(f"Analyzing sector: {sector}")
            overview['sectors'][sector] = self.get_sector_sentiment_summary(sector=sector, days_back=7)
            time.sleep(1)  # Rate limiting

        return overview


def main():
    """
    Demo function to test the agent
    """
    print("Initializing Sentiment Stock Agent...")
    agent = SentimentStockAgent()

    print("\n" + "="*80)
    print("TESTING STOCK VALIDATION")
    print("="*80)

    # Test stock validation
    test_tickers = ['NVDA', 'MSFT', 'EQIX', 'NEE']
    for ticker in test_tickers:
        result = agent.validate_stock(ticker)
        print(f"\n{ticker}: {json.dumps(result, indent=2)}")

    print("\n" + "="*80)
    print("TESTING SENTIMENT ANALYSIS")
    print("="*80)

    # Test sentiment analysis
    test_text = "NVIDIA announces breakthrough in AI chip technology, stock soars 15%"
    print(f"\nText: {test_text}")
    print(f"TextBlob: {agent.analyze_sentiment_textblob(test_text)}")
    print(f"VADER: {agent.analyze_sentiment_vader(test_text)}")

    print("\n" + "="*80)
    print("TESTING TECH NEWS SEARCH")
    print("="*80)

    # Test news search for AI sector
    print("\nSearching AI news...")
    ai_news = agent.search_tech_news(sector='ai', days_back=7)
    print(f"Found {len(ai_news)} articles")
    if ai_news:
        print(f"\nSample article:")
        print(json.dumps(ai_news[0], indent=2))

    print("\n" + "="*80)
    print("TESTING SECTOR SENTIMENT SUMMARY")
    print("="*80)

    # Test sector summary
    print("\nGetting AI sector sentiment summary...")
    ai_summary = agent.get_sector_sentiment_summary(sector='ai', days_back=7)
    print(json.dumps(ai_summary, indent=2))

    print("\n" + "="*80)
    print("TESTING STOCK WITH SECTOR SENTIMENT")
    print("="*80)

    # Test full analysis
    print("\nAnalyzing NVDA with sector sentiment...")
    full_analysis = agent.analyze_stock_with_sector_sentiment('NVDA')
    print(json.dumps(full_analysis, indent=2))


if __name__ == "__main__":
    main()
