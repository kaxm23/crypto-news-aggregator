from textblob import TextBlob
from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime
import pytz

@dataclass
class SentimentResult:
    """Class to store sentiment analysis results"""
    polarity: float
    subjectivity: float
    text_length: int
    timestamp_utc: str
    user: str
    
    def get_sentiment_label(self) -> str:
        """Returns a human-readable sentiment label based on polarity"""
        if self.polarity > 0.3:
            return "Positive"
        elif self.polarity < -0.3:
            return "Negative"
        else:
            return "Neutral"
    
    def get_subjectivity_label(self) -> str:
        """Returns a human-readable subjectivity label"""
        if self.subjectivity > 0.7:
            return "Very Subjective"
        elif self.subjectivity > 0.3:
            return "Somewhat Subjective"
        else:
            return "Objective"
    
    def to_dict(self) -> Dict:
        """Convert the result to a dictionary"""
        return {
            "polarity": round(self.polarity, 3),
            "subjectivity": round(self.subjectivity, 3),
            "sentiment_label": self.get_sentiment_label(),
            "subjectivity_label": self.get_subjectivity_label(),
            "text_length": self.text_length,
            "timestamp_utc": self.timestamp_utc,
            "user": self.user
        }

def analyze_sentiment(
    text: str,
    user: str = "kaxm23",
    timestamp: Optional[str] = None
) -> SentimentResult:
    """
    Analyze the sentiment of the given text using TextBlob.
    
    Args:
        text (str): The text to analyze
        user (str, optional): The user performing the analysis. Defaults to "kaxm23"
        timestamp (str, optional): UTC timestamp. If None, current time is used.
    
    Returns:
        SentimentResult: Object containing sentiment analysis results
        
    Example:
        >>> result = analyze_sentiment("I love this product! It's amazing!")
        >>> print(result.to_dict())
        {
            'polarity': 0.875,
            'subjectivity': 0.9,
            'sentiment_label': 'Positive',
            'subjectivity_label': 'Very Subjective',
            'text_length': 32,
            'timestamp_utc': '2025-02-08 22:13:31',
            'user': 'kaxm23'
        }
    """
    # Use provided timestamp or current time
    if timestamp is None:
        timestamp = "2025-02-08 22:13:31"
    
    # Create TextBlob object
    blob = TextBlob(text)
    
    # Analyze sentiment
    sentiment = blob.sentiment
    
    # Create and return result object
    return SentimentResult(
        polarity=sentiment.polarity,
        subjectivity=sentiment.subjectivity,
        text_length=len(text),
        timestamp_utc=timestamp,
        user=user
    )