from bs4 import BeautifulSoup
import re
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TextProcessingError(Exception):
    """Custom exception for text processing errors"""
    pass

def clean_text(
    text: str,
    preserve_numbers: bool = True,
    preserve_urls: bool = True,
    max_length: Optional[int] = None
) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text: Input text to clean
        preserve_numbers: Whether to keep numbers in text
        preserve_urls: Whether to keep URLs in text
        max_length: Maximum length of output text
        
    Returns:
        Cleaned text string
    """
    try:
        if not text:
            return ""

        # Remove HTML tags
        soup = BeautifulSoup(text, 'html.parser')
        text = soup.get_text()

        # Preserve URLs if requested
        urls = []
        if preserve_urls:
            url_pattern = r'https?://\S+'
            urls = re.findall(url_pattern, text)

        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Handle numbers
        if not preserve_numbers:
            text = re.sub(r'\d+', '', text)

        # Normalize whitespace
        text = ' '.join(text.split())

        # Reinsert URLs if preserved
        if preserve_urls and urls:
            for url in urls:
                text = text + f" {url}"

        # Truncate if maximum length specified
        if max_length and len(text) > max_length:
            text = text[:max_length].rsplit(' ', 1)[0] + '...'

        return text.strip()

    except Exception as e:
        error_msg = f"Error cleaning text: {str(e)}"
        logger.error(error_msg)
        raise TextProcessingError(error_msg)

def extract_keywords(text: str, max_keywords: int = 5) -> list:
    """Extract key words from text"""
    try:
        # Remove common words and punctuation
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'is', 'are'}
        words = text.lower().split()
        words = [w for w in words if w not in common_words and len(w) > 2]
        
        # Count word frequencies
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
            
        # Sort by frequency and return top words
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:max_keywords]]
        
    except Exception as e:
        logger.error(f"Error extracting keywords: {e}")
        return []

def summarize_text(text: str, max_sentences: int = 3) -> str:
    """Generate a brief summary of the text"""
    try:
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return text
            
        # Return first few sentences
        summary = '. '.join(sentences[:max_sentences]) + '.'
        return summary
        
    except Exception as e:
        logger.error(f"Error summarizing text: {e}")
        return text

# Test the module if run directly
if __name__ == "__main__":
    sample_text = """
    <p>Bitcoin surged to $50,000 today! The cryptocurrency market is showing strong signs of recovery. 
    Visit https://example.com for more details. This is a major milestone for digital currencies.</p>
    """
    
    try:
        cleaned = clean_text(sample_text)
        print(f"Cleaned text: {cleaned}")
        
        keywords = extract_keywords(cleaned)
        print(f"Keywords: {keywords}")
        
        summary = summarize_text(cleaned)
        print(f"Summary: {summary}")
        
    except TextProcessingError as e:
        print(f"Error: {e}")