import feedparser
from datetime import datetime
import pytz

def fetch_crypto_news():
    # CoinDesk RSS feed URL
    rss_url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
    
    # Fetch and parse the RSS feed
    feed = feedparser.parse(rss_url)
    
    # List to store articles
    articles = []
    
    # Process each entry in the feed
    for entry in feed.entries:
        article = {
            'title': entry.title,
            'link': entry.link,
            'summary': entry.summary,
            'published_date': parse_date(entry.published)
        }
        articles.append(article)
    
    return articles

def parse_date(date_string):
    """Convert the feed's date string to a standardized format"""
    try:
        # Parse the date from the feed
        parsed_date = datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %z')
        # Convert to UTC and format
        utc_date = parsed_date.astimezone(pytz.UTC)
        return utc_date.strftime('%Y-%m-%d %H:%M:%S UTC')
    except Exception as e:
        return date_string  # Return original string if parsing fails

def main():
    print("Fetching crypto news articles...")
    articles = fetch_crypto_news()
    
    print("\nLatest Crypto News Headlines:")
    print("-" * 50)
    
    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"Published: {article['published_date']}")
        print(f"Link: {article['link']}")
        print("-" * 50)

if __name__ == "__main__":
    main()