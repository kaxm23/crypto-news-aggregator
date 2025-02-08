"""Configuration settings for the crypto news aggregator"""

class Config:
    # Flask settings
    SECRET_KEY = 'your-secret-key-here'  # Change this in production!
    DEBUG = False
    
    # News collection settings
    MAX_ARTICLES = 20
    NEWS_UPDATE_INTERVAL = 300  # 5 minutes
    
    # Text processing settings
    MAX_SUMMARY_LENGTH = 300
    PRESERVE_NUMBERS = True
    PRESERVE_URLS = True
    
    # Sentiment analysis settings
    SENTIMENT_THRESHOLD = 0.3
    SUBJECTIVITY_THRESHOLD = 0.3

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    # Add production-specific settings here

# Set the active configuration
config = DevelopmentConfig()