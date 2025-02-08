from enhanced_text_cleaner import TextCleanerConfig, CleaningLevel, clean_text
from datetime import datetime

# Test HTML content with various elements
test_cases = {
    "News Article": """
        <article class="news-item">
            <h1>Breaking News: Bitcoin Surges to $60,000!</h1>
            <p class="timestamp">Posted on February 8th, 2025</p>
            <div class="content">
                <p>The cryptocurrency market saw significant gains today as Bitcoin (BTC) 
                reached $60,000, marking a new milestone for 2025.</p>
                <ul class="highlights">
                    <li>24-hour gain: +15%</li>
                    <li>Trading volume: $25B</li>
                    <li>Market cap: $1.2T</li>
                </ul>
                <a href="https://example.com/crypto-news">Read more...</a>
            </div>
        </article>
    """,
    
    "Simple Text": """
        <div>
            <p>Hello, World! This is a simple test with numbers 123 and special chars @#$%.</p>
            <p>Visit our website: https://example.com</p>
        </div>
    """,
    
    "Mixed Content": """
        <section>
            <h2>Technical Analysis</h2>
            <p>RSI: 65.5</p>
            <p>MACD: Positive</p>
            <code>print("Hello, World!")</code>
            <pre>Some pre-formatted text</pre>
        </section>
    """
}

def run_tests():
    current_time = "2025-02-08 22:09:22"  # Using the provided timestamp
    current_user = "kaxm23"  # Using the provided user login
    
    print("=" * 80)
    print(f"Running Text Cleaner Tests at {current_time}")
    print(f"User: {current_user}")
    print("=" * 80)
    
    for test_name, html_content in test_cases.items():
        print(f"\n📌 Testing: {test_name}")
        print("-" * 40)
        
        # Test 1: Minimal Cleaning
        config = TextCleanerConfig(
            cleaning_level=CleaningLevel.MINIMAL,
            user=current_user
        )
        result = clean_text(html_content, config)
        print("\n🔍 Minimal Cleaning:")
        print(f"Text: {result.text[:100]}...")
        print(f"Metadata: {result.get_metadata_dict()}")
        
        # Test 2: Standard Cleaning with Numbers and URLs
        config = TextCleanerConfig(
            cleaning_level=CleaningLevel.STANDARD,
            preserve_numbers=True,
            preserve_urls=True,
            preserved_punctuation=".,!$%",
            user=current_user
        )
        result = clean_text(html_content, config)
        print("\n🔍 Standard Cleaning (with numbers and URLs):")
        print(f"Text: {result.text[:100]}...")
        print(f"Metadata: {result.get_metadata_dict()}")
        
        # Test 3: Strict Cleaning
        config = TextCleanerConfig(
            cleaning_level=CleaningLevel.STRICT,
            preserve_case=True,
            user=current_user
        )
        result = clean_text(html_content, config)
        print("\n🔍 Strict Cleaning:")
        print(f"Text: {result.text[:100]}...")
        print(f"Metadata: {result.get_metadata_dict()}")
        
        print("\n" + "=" * 80)

if __name__ == "__main__":
    run_tests()