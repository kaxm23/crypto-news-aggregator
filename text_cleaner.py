from bs4 import BeautifulSoup
import re

def clean_text(html_content):
    """
    Clean HTML content by removing HTML tags and non-alphabetic characters.
    
    Args:
        html_content (str): String containing HTML content
        
    Returns:
        str: Cleaned text containing only alphabetic characters and spaces
    """
    # Step 1: Remove HTML tags using BeautifulSoup
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text()
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return ""
    
    # Step 2: Remove non-alphabetic characters using regex
    # This keeps only letters and spaces, converting to lowercase
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text_content)
    
    # Step 3: Normalize spaces (remove extra whitespace)
    cleaned_text = ' '.join(cleaned_text.split())
    
    return cleaned_text.lower()

# Example usage and test cases
if __name__ == "__main__":
    # Test case 1: Simple HTML
    test_html1 = """
    <div class="article">
        <h1>Hello, World!</h1>
        <p>This is a test123... </p>
    </div>
    """
    print("Test 1 Result:")
    print(clean_text(test_html1))
    print("-" * 50)
    
    # Test case 2: More complex HTML with special characters
    test_html2 = """
    <article>
        <h2>Crypto & Trading!</h2>
        <p>Bitcoin price: $50,000 📈</p>
        <ul>
            <li>Point #1</li>
            <li>Point #2!!!</li>
        </ul>
    </article>
    """
    print("Test 2 Result:")
    print(clean_text(test_html2))