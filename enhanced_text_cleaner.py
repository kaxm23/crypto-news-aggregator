from bs4 import BeautifulSoup
import re
from typing import List, Optional, Dict
from datetime import datetime
import pytz
from dataclasses import dataclass
from enum import Enum

class CleaningLevel(Enum):
    """Enum for predefined cleaning levels"""
    MINIMAL = "minimal"  # Only remove HTML tags
    STANDARD = "standard"  # Remove HTML and basic cleaning
    STRICT = "strict"  # Remove all non-alphabetic characters

@dataclass
class CleaningMetadata:
    """Metadata for the cleaning process"""
    timestamp_utc: str
    user: str
    original_length: int
    cleaned_length: int
    removed_tags: List[str]
    cleaning_level: CleaningLevel
    processing_time_ms: float

class TextCleanerConfig:
    """Configuration class for text cleaning options"""
    def __init__(
        self,
        preserve_numbers: bool = False,
        preserve_case: bool = False,
        preserved_punctuation: str = "",
        html_parser: str = "html.parser",
        strip_newlines: bool = True,
        preserve_urls: bool = False,
        min_word_length: int = 1,
        custom_replacements: dict = None,
        extract_tags: List[str] = None,
        cleaning_level: CleaningLevel = CleaningLevel.STANDARD,
        track_metadata: bool = True,
        user: str = "kaxm23"  # Default to current user
    ):
        self.preserve_numbers = preserve_numbers
        self.preserve_case = preserve_case
        self.preserved_punctuation = preserved_punctuation
        self.html_parser = html_parser
        self.strip_newlines = strip_newlines
        self.preserve_urls = preserve_urls
        self.min_word_length = min_word_length
        self.custom_replacements = custom_replacements or {}
        self.extract_tags = extract_tags
        self.cleaning_level = cleaning_level
        self.track_metadata = track_metadata
        self.user = user

class CleaningResult:
    """Class to hold the cleaning result and metadata"""
    def __init__(self, text: str, metadata: CleaningMetadata):
        self.text = text
        self.metadata = metadata

    def __str__(self):
        return self.text

    def get_metadata_dict(self) -> Dict:
        """Return metadata as a dictionary"""
        return {
            "timestamp_utc": self.metadata.timestamp_utc,
            "user": self.metadata.user,
            "original_length": self.metadata.original_length,
            "cleaned_length": self.metadata.cleaned_length,
            "removed_tags": self.metadata.removed_tags,
            "cleaning_level": self.metadata.cleaning_level.value,
            "processing_time_ms": self.metadata.processing_time_ms
        }

def clean_text(
    html_content: str,
    config: Optional[TextCleanerConfig] = None
) -> CleaningResult:
    """
    Enhanced function to clean HTML content with configurable options and metadata tracking.
    
    Args:
        html_content (str): String containing HTML content
        config (TextCleanerConfig, optional): Configuration options for text cleaning
        
    Returns:
        CleaningResult: Object containing cleaned text and metadata
    """
    import time
    start_time = time.time()

    if config is None:
        config = TextCleanerConfig()

    original_length = len(html_content)
    removed_tags = []

    # Step 1: Handle HTML content
    try:
        soup = BeautifulSoup(html_content, config.html_parser)
        
        # Track removed tags
        if config.track_metadata:
            removed_tags = [tag.name for tag in soup.find_all()]
        
        # Apply cleaning based on cleaning level
        if config.cleaning_level == CleaningLevel.MINIMAL:
            text_content = soup.get_text(strip=True)
        else:
            # If specific tags are requested, only extract those
            if config.extract_tags:
                text_content = ' '.join(
                    element.get_text(strip=True)
                    for tag in config.extract_tags
                    for element in soup.find_all(tag)
                )
            else:
                text_content = soup.get_text(strip=True)
            
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return CleaningResult("", CleaningMetadata(
            timestamp_utc="2025-02-08 22:06:34",
            user=config.user,
            original_length=0,
            cleaned_length=0,
            removed_tags=[],
            cleaning_level=config.cleaning_level,
            processing_time_ms=0
        ))

    # Only proceed with additional cleaning if not minimal level
    if config.cleaning_level != CleaningLevel.MINIMAL:
        # Step 2: Apply custom replacements if any
        for old, new in config.custom_replacements.items():
            text_content = text_content.replace(old, new)

        # Step 3: Handle URLs if preservation is requested
        urls = []
        if config.preserve_urls:
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text_content)
            for i, url in enumerate(urls):
                text_content = text_content.replace(url, f"__URL_{i}__")

        # Step 4: Clean the text based on configuration
        pattern_parts = []
        
        # Always keep letters
        pattern_parts.append(r'a-zA-Z')
        
        # Keep numbers if requested or if not in strict mode
        if config.preserve_numbers or config.cleaning_level != CleaningLevel.STRICT:
            pattern_parts.append(r'0-9')
        
        # Keep specified punctuation if not in strict mode
        if config.preserved_punctuation and config.cleaning_level != CleaningLevel.STRICT:
            escaped_punct = re.escape(config.preserved_punctuation)
            pattern_parts.append(escaped_punct)
        
        # Always preserve spaces
        pattern_parts.append(r'\s')
        
        # Build and apply the pattern
        pattern = f'[^{"".join(pattern_parts)}]'
        cleaned_text = re.sub(pattern, ' ', text_content)
        
        # Step 5: Handle case
        if not config.preserve_case:
            cleaned_text = cleaned_text.lower()
        
        # Step 6: Normalize spaces
        cleaned_text = ' '.join(
            word for word in cleaned_text.split()
            if len(word) >= config.min_word_length
        )
        
        # Step 7: Restore URLs if they were preserved
        if config.preserve_urls:
            for i, url in enumerate(urls):
                cleaned_text = cleaned_text.replace(f"__URL_{i}__", url)
    else:
        cleaned_text = text_content

    # Calculate processing time
    processing_time_ms = (time.time() - start_time) * 1000

    # Create metadata
    metadata = CleaningMetadata(
        timestamp_utc="2025-02-08 22:06:34",
        user=config.user,
        original_length=original_length,
        cleaned_length=len(cleaned_text),
        removed_tags=removed_tags,
        cleaning_level=config.cleaning_level,
        processing_time_ms=processing_time_ms
    )

    return CleaningResult(cleaned_text, metadata)

# Example usage and test cases
if __name__ == "__main__":
    # Test HTML content
    test_html = """
    <article class="news-item">
        <h1>Bitcoin Reaches $50,000!</h1>
        <p>The cryptocurrency Bitcoin (BTC) has reached $50,000 on February 8th, 2025.</p>
        <ul>
            <li>24-hour change: +5.3%</li>
            <li>Trading volume: $1.2B</li>
        </ul>
        <a href="https://example.com">Read more...</a>
    </article>
    """
    
    print("Test 1: Minimal cleaning")
    config = TextCleanerConfig(cleaning_level=CleaningLevel.MINIMAL)
    result = clean_text(test_html, config)
    print(f"Cleaned text: {result.text}")
    print("Metadata:", result.get_metadata_dict())
    print("-" * 50)
    
    print("Test 2: Standard cleaning with numbers and punctuation")
    config = TextCleanerConfig(
        preserve_numbers=True,
        preserved_punctuation=".,!$%",
        preserve_case=False,
        cleaning_level=CleaningLevel.STANDARD
    )
    result = clean_text(test_html, config)
    print(f"Cleaned text: {result.text}")
    print("Metadata:", result.get_metadata_dict())
    print("-" * 50)
    
    print("Test 3: Strict cleaning")
    config = TextCleanerConfig(
        cleaning_level=CleaningLevel.STRICT,
        preserve_case=True,
        extract_tags=['h1', 'p']
    )
    result = clean_text(test_html, config)
    print(f"Cleaned text: {result.text}")
    print("Metadata:", result.get_metadata_dict())