"""
Flask API for Sentiment Stock Agent
Provides endpoints for stock validation and sentiment analysis
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime

from sentiment_stock_agent import SentimentStockAgent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize sentiment agent
agent = SentimentStockAgent()

# Cache for reducing API calls
cache = {}
CACHE_DURATION = 300  # 5 minutes


def get_cached_or_fetch(cache_key: str, fetch_func, *args, **kwargs):
    """
    Get data from cache or fetch if expired

    Args:
        cache_key: Unique key for this data
        fetch_func: Function to call if cache miss
        *args, **kwargs: Arguments to pass to fetch_func

    Returns:
        Cached or freshly fetched data
    """
    now = datetime.now().timestamp()

    if cache_key in cache:
        cached_data, cached_time = cache[cache_key]
        if now - cached_time < CACHE_DURATION:
            logger.info(f"Cache hit for {cache_key}")
            return cached_data

    logger.info(f"Cache miss for {cache_key}, fetching fresh data")
    data = fetch_func(*args, **kwargs)
    cache[cache_key] = (data, now)
    return data


@app.route('/')
def home():
    """Home endpoint with API information"""
    return jsonify({
        'name': 'Sentiment Stock Agent API',
        'version': '1.0.0',
        'description': 'Stock validation and sentiment analysis for tech sectors',
        'endpoints': {
            'GET /': 'API information',
            'GET /health': 'Health check',
            'GET /validate/<ticker>': 'Validate a stock ticker',
            'GET /sentiment/news': 'Get tech news with sentiment analysis',
            'GET /sentiment/sector/<sector>': 'Get sector sentiment summary',
            'GET /sentiment/overview': 'Get all sectors sentiment overview',
            'GET /analyze/<ticker>': 'Full analysis: stock + sector sentiment',
            'POST /analyze/batch': 'Batch analysis for multiple tickers'
        },
        'sectors': ['ai', 'data_centers', 'power_generation', 'all']
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'agent_initialized': agent is not None
    })


@app.route('/validate/<ticker>')
def validate_stock(ticker):
    """
    Validate a stock ticker

    Args:
        ticker: Stock ticker symbol

    Returns:
        JSON with stock validation data
    """
    ticker = ticker.upper()
    cache_key = f"validate_{ticker}"

    try:
        result = get_cached_or_fetch(cache_key, agent.validate_stock, ticker)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error validating stock {ticker}: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/sentiment/news')
def get_news():
    """
    Get tech news with sentiment analysis

    Query params:
        sector: Sector to search (default: 'all')
        days: Days back to search (default: 7)

    Returns:
        JSON with news articles and sentiment
    """
    sector = request.args.get('sector', 'all')
    days = int(request.args.get('days', 7))

    cache_key = f"news_{sector}_{days}"

    try:
        result = get_cached_or_fetch(
            cache_key,
            agent.search_tech_news,
            sector=sector,
            days_back=days
        )
        return jsonify({
            'sector': sector,
            'days_back': days,
            'article_count': len(result),
            'articles': result
        })
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/sentiment/sector/<sector>')
def get_sector_sentiment(sector):
    """
    Get sentiment summary for a sector

    Args:
        sector: Sector name (ai, data_centers, power_generation, all)

    Query params:
        days: Days back to analyze (default: 7)

    Returns:
        JSON with sector sentiment summary
    """
    days = int(request.args.get('days', 7))
    cache_key = f"sector_{sector}_{days}"

    valid_sectors = ['ai', 'data_centers', 'power_generation', 'all']
    if sector not in valid_sectors:
        return jsonify({
            'error': f'Invalid sector. Must be one of: {valid_sectors}'
        }), 400

    try:
        result = get_cached_or_fetch(
            cache_key,
            agent.get_sector_sentiment_summary,
            sector=sector,
            days_back=days
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting sector sentiment: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/sentiment/overview')
def get_sentiment_overview():
    """
    Get sentiment overview for all tech sectors

    Returns:
        JSON with all sector sentiments
    """
    cache_key = "overview_all"

    try:
        result = get_cached_or_fetch(
            cache_key,
            agent.get_all_tech_sectors_overview
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting sentiment overview: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/analyze/<ticker>')
def analyze_stock(ticker):
    """
    Full analysis: stock validation + sector sentiment

    Args:
        ticker: Stock ticker symbol

    Returns:
        JSON with complete analysis
    """
    ticker = ticker.upper()
    cache_key = f"analyze_{ticker}"

    try:
        result = get_cached_or_fetch(
            cache_key,
            agent.analyze_stock_with_sector_sentiment,
            ticker
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error analyzing stock {ticker}: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/analyze/batch', methods=['POST'])
def analyze_batch():
    """
    Batch analysis for multiple tickers

    Request body:
        {
            "tickers": ["NVDA", "MSFT", "GOOGL"]
        }

    Returns:
        JSON with analysis for each ticker
    """
    try:
        data = request.get_json()
        tickers = data.get('tickers', [])

        if not tickers:
            return jsonify({'error': 'No tickers provided'}), 400

        if len(tickers) > 20:
            return jsonify({'error': 'Maximum 20 tickers allowed'}), 400

        results = {}
        for ticker in tickers:
            ticker = ticker.upper()
            cache_key = f"analyze_{ticker}"
            try:
                results[ticker] = get_cached_or_fetch(
                    cache_key,
                    agent.analyze_stock_with_sector_sentiment,
                    ticker
                )
            except Exception as e:
                results[ticker] = {'error': str(e)}

        return jsonify({
            'ticker_count': len(tickers),
            'results': results,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error in batch analysis: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/sectors/stocks')
def get_sector_stocks():
    """
    Get the list of tracked stocks by sector

    Returns:
        JSON with stocks organized by sector
    """
    return jsonify({
        'sectors': agent.tech_stocks,
        'sector_keywords': agent.sector_keywords
    })


@app.route('/cache/clear', methods=['POST'])
def clear_cache():
    """
    Clear the API cache

    Returns:
        JSON with success message
    """
    global cache
    cache = {}
    return jsonify({
        'message': 'Cache cleared successfully',
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'Please check the API documentation at /'
    }), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': str(e)
    }), 500


if __name__ == '__main__':
    logger.info("Starting Sentiment Stock Agent API...")
    logger.info("API will be available at http://localhost:5000")
    logger.info("Visit http://localhost:5000 for API documentation")

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
