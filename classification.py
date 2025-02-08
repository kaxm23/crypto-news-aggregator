from textblob import TextBlob
import logging
from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class SentimentResult:
    """Class to hold sentiment analysis results"""
    polarity: float
    subjectivity: float
    sentiment_label: str
    subjectivity_label: str
    timestamp: str
    user: str

    def to_dict(self) -> Dict:
        """Convert result to dictionary"""
        return {
            'polarity': self.polarity,
            'subjectivity': self.subjectivity,
            'sentiment_label': self.sentiment_label,
            'subjectivity_label': self.subjectivity_label,
            'timestamp': self.timestamp,
            'user': self.user
        }

class SentimentAnalysisError(Exception):
    """Custom exception for sentiment analysis errors"""
    pass

def analyze_sentiment(
    text: str,
    user: str = "kaxm23",
    timestamp: str = "2025-02-08 22:38:46"
) -> SentimentResult:
    """
    Analyze sentiment of text using TextBlob.
    
    Args:
        text: Input text to analyze
        user: Username performing the analysis
        timestamp: Timestamp of analysis
        
    Returns:
        SentimentResult object with analysis results
    """
    try:
        if not text:
            return SentimentResult(
                polarity=0.0,
                subjectivity=0.0,
                sentiment_label="Neutral",
                subjectivity_label="Objective",
                timestamp=timestamp,
                user=user
            )

        # Perform sentiment analysis
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity

        # Determine sentiment label
        if polarity > 0.3:
            sentiment_label = "Positive"
        elif polarity < -0.3:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        # Determine subjectivity label
        if subjectivity > 0.7:
            subjectivity_label = "Very Subjective"
        elif subjectivity > 0.3:
            subjectivity_label = "Somewhat Subjective"
        else:
            subjectivity_label = "Objective"

        return SentimentResult(
            polarity=polarity,
            subjectivity=subjectivity,
            sentiment_label=sentiment_label,
            subjectivity_label=subjectivity_label,
            timestamp=timestamp,
            user=user
        )

    except Exception as e:
        error_msg = f"Error analyzing sentiment: {str(e)}"
        logger.error(error_msg)
        raise SentimentAnalysisError(error_msg)

# Test the module if run directly
if __name__ == "__main__":
    sample_texts = [
        "Bitcoin reaches new all-time high as institutional investors pour in!",
        "Cryptocurrency market crashes, investors lose millions in devastating sell-off.",
        "Market analysts predict stable trading range for major cryptocurrencies."
    ]
    
    try:
        for text in sample_texts:
            result = analyze_sentiment(text)
            print(f"\nText: {text}")
            print(f"Sentiment: {result.sentiment_label} (Polarity: {result.polarity:.2f})")
            print(f"Subjectivity: {result.subjectivity_label} (Score: {result.subjectivity:.2f})")
            
    except SentimentAnalysisError as e:
        print(f"Error: {e}")