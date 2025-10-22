import praw
import re
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import defaultdict

class RedditStockSentimentScraper:
    """
    Scrapes Reddit for stock market sentiment analysis.
    Focuses on stock market related subreddits and analyzes sentiment.
    """

    def __init__(self):
        # Initialize VADER sentiment analyzer
        self.analyzer = SentimentIntensityAnalyzer()

        # Stock market focused subreddits
        self.target_subreddits = [
            'wallstreetbets',
            'stocks',
            'investing',
            'StockMarket',
            'options',
            'pennystocks',
            'SecurityAnalysis',
            'ValueInvesting'
        ]

        # Reddit API configuration
        # Users will need to set up their own Reddit API credentials
        self.reddit = None

    def initialize_reddit_client(self, client_id, client_secret, user_agent):
        """
        Initialize the Reddit API client with user credentials.

        Args:
            client_id: Reddit API client ID
            client_secret: Reddit API client secret
            user_agent: User agent string
        """
        try:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
            return True, "Reddit client initialized successfully"
        except Exception as e:
            return False, f"Error initializing Reddit client: {str(e)}"

    def extract_stock_tickers(self, text):
        """
        Extract stock ticker symbols from text.
        Looks for $TICKER or uppercase words that might be tickers.

        Args:
            text: Text to search for tickers

        Returns:
            List of potential stock tickers
        """
        # Pattern for $TICKER format
        dollar_tickers = re.findall(r'\$([A-Z]{1,5})\b', text)

        # Pattern for standalone uppercase words (potential tickers)
        # Filter out common words that aren't tickers
        common_words = {'I', 'A', 'CEO', 'IPO', 'ETF', 'ATH', 'DD', 'YOLO', 'FD', 'WSB', 'IMO', 'FOMO', 'PM', 'AH'}
        word_tickers = [word for word in re.findall(r'\b[A-Z]{2,5}\b', text)
                       if word not in common_words]

        all_tickers = list(set(dollar_tickers + word_tickers))
        return all_tickers

    def analyze_sentiment(self, text):
        """
        Analyze sentiment of text using VADER.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with sentiment scores
        """
        scores = self.analyzer.polarity_scores(text)

        # Classify overall sentiment
        if scores['compound'] >= 0.05:
            sentiment = 'POSITIVE'
        elif scores['compound'] <= -0.05:
            sentiment = 'NEGATIVE'
        else:
            sentiment = 'NEUTRAL'

        return {
            'compound': scores['compound'],
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'sentiment': sentiment
        }

    def scrape_subreddit(self, subreddit_name, post_limit=50, time_filter='day'):
        """
        Scrape posts from a specific subreddit.

        Args:
            subreddit_name: Name of subreddit to scrape
            post_limit: Number of posts to retrieve
            time_filter: Time filter ('hour', 'day', 'week', 'month', 'year', 'all')

        Returns:
            List of posts with sentiment analysis
        """
        if not self.reddit:
            return []

        posts_data = []

        try:
            subreddit = self.reddit.subreddit(subreddit_name)

            # Get hot posts from the subreddit
            for post in subreddit.hot(limit=post_limit):
                # Combine title and selftext for analysis
                full_text = f"{post.title} {post.selftext}"

                # Analyze sentiment
                sentiment = self.analyze_sentiment(full_text)

                # Extract tickers
                tickers = self.extract_stock_tickers(full_text)

                post_data = {
                    'subreddit': subreddit_name,
                    'title': post.title,
                    'text': post.selftext[:200] if post.selftext else '',  # Limit text length
                    'score': post.score,
                    'num_comments': post.num_comments,
                    'created_utc': datetime.fromtimestamp(post.created_utc),
                    'url': post.url,
                    'tickers': tickers,
                    'sentiment': sentiment
                }

                posts_data.append(post_data)

        except Exception as e:
            print(f"Error scraping r/{subreddit_name}: {str(e)}")

        return posts_data

    def scrape_all_subreddits(self, post_limit_per_sub=25):
        """
        Scrape all target subreddits.

        Args:
            post_limit_per_sub: Number of posts to retrieve per subreddit

        Returns:
            List of all posts from all subreddits
        """
        all_posts = []

        for subreddit_name in self.target_subreddits:
            posts = self.scrape_subreddit(subreddit_name, post_limit=post_limit_per_sub)
            all_posts.extend(posts)

        return all_posts

    def generate_summary(self, posts):
        """
        Generate a comprehensive summary of scraped posts.

        Args:
            posts: List of post data

        Returns:
            Summary string
        """
        if not posts:
            return "No posts were scraped. Please check your Reddit API credentials."

        # Calculate statistics
        total_posts = len(posts)

        # Sentiment distribution
        sentiment_counts = defaultdict(int)
        total_sentiment_score = 0

        # Ticker mentions
        ticker_mentions = defaultdict(int)
        ticker_sentiments = defaultdict(list)

        # Subreddit stats
        subreddit_counts = defaultdict(int)

        for post in posts:
            # Count sentiments
            sentiment_counts[post['sentiment']['sentiment']] += 1
            total_sentiment_score += post['sentiment']['compound']

            # Count ticker mentions
            for ticker in post['tickers']:
                ticker_mentions[ticker] += 1
                ticker_sentiments[ticker].append(post['sentiment']['compound'])

            # Count subreddit posts
            subreddit_counts[post['subreddit']] += 1

        # Calculate average sentiment
        avg_sentiment = total_sentiment_score / total_posts if total_posts > 0 else 0

        # Overall market sentiment
        if avg_sentiment >= 0.05:
            overall_sentiment = "BULLISH"
        elif avg_sentiment <= -0.05:
            overall_sentiment = "BEARISH"
        else:
            overall_sentiment = "NEUTRAL"

        # Top mentioned tickers
        top_tickers = sorted(ticker_mentions.items(), key=lambda x: x[1], reverse=True)[:10]

        # Build summary string
        summary = []
        summary.append("=" * 80)
        summary.append("REDDIT STOCK MARKET SENTIMENT ANALYSIS")
        summary.append("=" * 80)
        summary.append(f"\nAnalysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary.append(f"Total Posts Analyzed: {total_posts}")
        summary.append(f"\nScraping completed from {len(self.target_subreddits)} subreddits:")
        for sub in self.target_subreddits:
            count = subreddit_counts.get(sub, 0)
            summary.append(f"  - r/{sub}: {count} posts")

        summary.append(f"\n{'-' * 80}")
        summary.append("OVERALL MARKET SENTIMENT")
        summary.append(f"{'-' * 80}")
        summary.append(f"Market Sentiment: {overall_sentiment}")
        summary.append(f"Average Sentiment Score: {avg_sentiment:.3f} (Range: -1 to +1)")

        summary.append(f"\nSentiment Distribution:")
        summary.append(f"  POSITIVE: {sentiment_counts['POSITIVE']} posts ({sentiment_counts['POSITIVE']/total_posts*100:.1f}%)")
        summary.append(f"  NEUTRAL:  {sentiment_counts['NEUTRAL']} posts ({sentiment_counts['NEUTRAL']/total_posts*100:.1f}%)")
        summary.append(f"  NEGATIVE: {sentiment_counts['NEGATIVE']} posts ({sentiment_counts['NEGATIVE']/total_posts*100:.1f}%)")

        summary.append(f"\n{'-' * 80}")
        summary.append("TOP 10 MOST MENTIONED STOCKS")
        summary.append(f"{'-' * 80}")

        if top_tickers:
            for i, (ticker, count) in enumerate(top_tickers, 1):
                # Calculate average sentiment for this ticker
                avg_ticker_sentiment = sum(ticker_sentiments[ticker]) / len(ticker_sentiments[ticker])

                if avg_ticker_sentiment >= 0.05:
                    ticker_sentiment = "BULLISH"
                elif avg_ticker_sentiment <= -0.05:
                    ticker_sentiment = "BEARISH"
                else:
                    ticker_sentiment = "NEUTRAL"

                summary.append(f"{i:2d}. ${ticker:5s} - {count:3d} mentions - Sentiment: {ticker_sentiment:8s} ({avg_ticker_sentiment:+.3f})")
        else:
            summary.append("No stock tickers detected in the analyzed posts.")

        summary.append(f"\n{'-' * 80}")
        summary.append("KEY INSIGHTS")
        summary.append(f"{'-' * 80}")

        # Generate insights
        positive_pct = sentiment_counts['POSITIVE'] / total_posts * 100
        negative_pct = sentiment_counts['NEGATIVE'] / total_posts * 100

        if positive_pct > 60:
            summary.append("- Reddit sentiment is strongly BULLISH with high positive sentiment")
        elif positive_pct > 45:
            summary.append("- Reddit sentiment leans BULLISH with moderate positive sentiment")
        elif negative_pct > 60:
            summary.append("- Reddit sentiment is strongly BEARISH with high negative sentiment")
        elif negative_pct > 45:
            summary.append("- Reddit sentiment leans BEARISH with moderate negative sentiment")
        else:
            summary.append("- Reddit sentiment is MIXED with no clear directional bias")

        if top_tickers:
            summary.append(f"- Most discussed stock: ${top_tickers[0][0]} with {top_tickers[0][1]} mentions")

        summary.append("\n" + "=" * 80)
        summary.append("End of Analysis")
        summary.append("=" * 80)

        return "\n".join(summary)
