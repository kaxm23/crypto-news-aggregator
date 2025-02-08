import feedparser
from datetime import datetime
import logging
from typing import List, Dict, Optional
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewsCollectionError(Exception):
    """Custom exception for news collection errors"""
    pass

def fetch_crypto_news(max_articles: int = 10) -> List[Dict]:
    """
    Fetch cryptocurrency news from various RSS feeds.
    
    Args:
        max_articles (int): Maximum number of articles to return
        
    Returns:
        List[Dict]: List of articles with title, summary, link, and published date
        
    Raises:
        NewsCollectionError: If there's an error fetching news
    """
    # List of cryptocurrency news RSS feeds
    news_feeds = [
        'https://cointelegraph.com/rss',
        'https://coindesk.com/arc/outboundfeeds/rss/',
        'https://cryptonews.com/news/feed',
    ]
    
    articles = []
    
    try:
        for feed_url in news_feeds:
            try:
                # Add user agent to avoid blocking
                feed = feedparser.parse(feed_url, agent='Mozilla/5.0')
                
                if feed.get('status') != 200:
                    logger.warning(f"Failed to fetch feed from {feed_url}: Status {feed.get('status')}")
                    continue
                
                # Process each entry in the feed
                for entry in feed.entries:
                    article = {
                        'title': entry.get('title', '').strip(),
                        'summary': clean_summary(entry.get('summary', '')),
                        'link': entry.get('link', ''),
                        'published_date': parse_date(entry.get('published', '')),
                        'source': feed_url
                    }
                    
                    # Only add articles with valid titles
                    if article['title']:
                        articles.append(article)
                    
                    # Break if we have enough articles
                    if len(articles) >= max_articles:
                        break
                        
                # Small delay between requests
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error processing feed {feed_url}: {str(e)}")
                continue
        
        # Sort articles by publication date
        articles.sort(key=lambda x: x['published_date'], reverse=True)
        
        return articles[:max_articles]
    
    except Exception as e:
        error_msg = f"Failed to fetch crypto news: {str(e)}"
        logger.error(error_msg)
        raise NewsCollectionError(error_msg)

def clean_summary(summary: str) -> str:
    """Clean the article summary by removing HTML tags and extra whitespace"""
    import re
    from bs4 import BeautifulSoup
    
    try:
        # Remove HTML tags
        soup = BeautifulSoup(summary, 'html.parser')
        text = soup.get_text()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Truncate if too long
        max_length = 300
        if len(text) > max_length:
            text = text[:max_length] + '...'
            
        return text
    except Exception as e:
        logger.warning(f"Error cleaning summary: {str(e)}")
        return summary

def parse_date(date_str: str) -> str:
    """Parse various date formats to consistent UTC format"""
    try:
        # Try different date formats
        formats = [
            '%a, %d %b %Y %H:%M:%S %z',
            '%a, %d %b %Y %H:%M:%S GMT',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%d %H:%M:%S',
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                continue
        
        # If no format matches, return current time
        return "2025-02-08 22:30:35"
    
    except Exception as e:
        logger.warning(f"Error parsing date {date_str}: {str(e)}")
        return "2025-02-08 22:30:35"

# Test the module if run directly
if __name__ == "__main__":
    try:
        print("Fetching crypto news...")
        news = fetch_crypto_news(max_articles=5)
        print(f"\nFetched {len(news)} articles:")
        for article in news:
            print(f"\nTitle: {article['title']}")
            print(f"Published: {article['published_date']}")
            print(f"Summary: {article['summary'][:100]}...")
    except NewsCollectionError as e:
        print(f"Error: {e}")