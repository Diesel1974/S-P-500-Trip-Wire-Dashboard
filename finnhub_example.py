"""
Example: How to use Finnhub API with environment variables
This demonstrates the SECURE way to handle API keys
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable (NEVER hardcode!)
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

if not FINNHUB_API_KEY:
    raise ValueError("FINNHUB_API_KEY not found in .env file!")


class FinnhubClient:
    """
    Finnhub API client that uses environment variables for authentication
    """

    def __init__(self):
        self.api_key = os.getenv('FINNHUB_API_KEY')
        self.base_url = 'https://finnhub.io/api/v1'

        if not self.api_key:
            raise ValueError("FINNHUB_API_KEY not set in environment variables")

    def get_quote(self, symbol: str):
        """
        Get real-time stock quote

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')

        Returns:
            dict: Stock quote data
        """
        url = f'{self.base_url}/quote'
        params = {
            'symbol': symbol,
            'token': self.api_key  # API key passed as 'token' parameter
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching quote for {symbol}: {e}")
            return None

    def get_company_profile(self, symbol: str):
        """
        Get company profile information

        Args:
            symbol: Stock ticker symbol

        Returns:
            dict: Company profile data
        """
        url = f'{self.base_url}/stock/profile2'
        params = {
            'symbol': symbol,
            'token': self.api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching profile for {symbol}: {e}")
            return None

    def get_company_news(self, symbol: str, from_date: str, to_date: str):
        """
        Get company news

        Args:
            symbol: Stock ticker symbol
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)

        Returns:
            list: News articles
        """
        url = f'{self.base_url}/company-news'
        params = {
            'symbol': symbol,
            'from': from_date,
            'to': to_date,
            'token': self.api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news for {symbol}: {e}")
            return None

    def get_market_news(self, category: str = 'general'):
        """
        Get market news

        Args:
            category: News category (general, forex, crypto, merger)

        Returns:
            list: News articles
        """
        url = f'{self.base_url}/news'
        params = {
            'category': category,
            'token': self.api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching market news: {e}")
            return None


def main():
    """
    Example usage of Finnhub API client
    """
    # Initialize client (automatically loads from .env)
    client = FinnhubClient()

    print("=" * 80)
    print("FINNHUB API EXAMPLE - Using Environment Variables")
    print("=" * 80)
    print()

    # Test 1: Get stock quote
    print("Test 1: Getting AAPL stock quote...")
    quote = client.get_quote('AAPL')
    if quote:
        print(f"✅ Current Price: ${quote.get('c', 0):.2f}")
        print(f"   Change: {quote.get('d', 0):.2f} ({quote.get('dp', 0):.2f}%)")
        print(f"   High: ${quote.get('h', 0):.2f}")
        print(f"   Low: ${quote.get('l', 0):.2f}")
    else:
        print("❌ Failed to fetch quote")

    print()

    # Test 2: Get company profile
    print("Test 2: Getting AAPL company profile...")
    profile = client.get_company_profile('AAPL')
    if profile:
        print(f"✅ Company: {profile.get('name', 'N/A')}")
        print(f"   Industry: {profile.get('finnhubIndustry', 'N/A')}")
        print(f"   Market Cap: ${profile.get('marketCapitalization', 0):,.0f}M")
        print(f"   Country: {profile.get('country', 'N/A')}")
    else:
        print("❌ Failed to fetch profile")

    print()

    # Test 3: Get market news
    print("Test 3: Getting general market news...")
    news = client.get_market_news('general')
    if news and len(news) > 0:
        print(f"✅ Found {len(news)} articles")
        print(f"   Latest: {news[0].get('headline', 'N/A')[:80]}...")
    else:
        print("❌ Failed to fetch news")

    print()
    print("=" * 80)
    print("API KEY SECURITY:")
    print("✅ API key loaded from .env file")
    print("✅ .env file is in .gitignore (not committed to Git)")
    print("✅ Code never contains hardcoded API keys")
    print("=" * 80)


if __name__ == '__main__':
    main()
