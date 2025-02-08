from flask import Flask, render_template
from news_collector import fetch_crypto_news, NewsCollectionError
from text_processing import clean_text, TextProcessingError
from classification import analyze_sentiment, SentimentAnalysisError
import logging
from datetime import datetime

app = Flask(__name__)

def process_article(article):
    """Process a single article with text cleaning and sentiment analysis"""
    try:
        # Clean the article summary
        cleaned_summary = clean_text(
            article.get('summary', ''),
            preserve_numbers=True,
            preserve_urls=True,
            max_length=300
        )

        # Analyze sentiment with current timestamp
        sentiment_result = analyze_sentiment(
            cleaned_summary,
            user="kaxm23",
            timestamp="2025-02-08 22:44:10"
        )

        # Return processed article with sentiment
        return {
            'title': article.get('title', ''),
            'summary': cleaned_summary,
            'url': article.get('link', ''),
            'published_date': article.get('published_date', "2025-02-08 22:44:10"),
            'sentiment': sentiment_result.to_dict()  # This ensures sentiment is a dictionary
        }
    except (TextProcessingError, SentimentAnalysisError) as e:
        logger.error(f"Error processing article: {e}")
        return None

@app.route('/')
def index():
    try:
        # Fetch raw articles
        raw_articles = fetch_crypto_news(max_articles=10)
        
        # Process articles with sentiment analysis
        processed_articles = []
        for article in raw_articles:
            processed = process_article(article)
            if processed:
                processed_articles.append(processed)
        
        return render_template(
            'articles.html',
            articles=processed_articles,
            current_time="2025-02-08 22:44:10",
            current_user="kaxm23"
        )
    except Exception as e:
        logger.error(f"Error processing articles: {e}")
        return render_template(
            'articles.html',
            articles=[],
            error=str(e),
            current_time="2025-02-08 22:44:10",
            current_user="kaxm23"
        )

if __name__ == '__main__':
    app.run(debug=True)