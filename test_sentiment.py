from sentiment_analyzer import analyze_sentiment

def run_sentiment_tests():
    # Test cases with various types of text
    test_cases = {
        "Positive": "I absolutely love this product! It's amazing and works perfectly.",
        "Negative": "This is terrible. I hate how poorly it performs and it's completely useless.",
        "Neutral": "The product has 5 buttons and weighs 100 grams.",
        "Mixed": "While the interface is great, the performance could be better.",
        "Highly Subjective": "This is the most incredible, amazing, fantastic product ever!!!",
        "Objective": "The temperature is 20 degrees Celsius and humidity is 45%.",
    }
    
    print("=" * 80)
    print("Running Sentiment Analysis Tests")
    print(f"Timestamp: 2025-02-08 22:13:31")
    print(f"User: kaxm23")
    print("=" * 80)
    
    for test_name, text in test_cases.items():
        print(f"\n📝 Testing: {test_name}")
        print(f"Text: {text}")
        
        # Analyze sentiment
        result = analyze_sentiment(text)
        
        # Get results dictionary
        analysis = result.to_dict()
        
        print("\n📊 Results:")
        print(f"Sentiment: {analysis['sentiment_label']} (Polarity: {analysis['polarity']})")
        print(f"Subjectivity: {analysis['subjectivity_label']} (Score: {analysis['subjectivity']})")
        print(f"Text Length: {analysis['text_length']} characters")
        print("-" * 40)

if __name__ == "__main__":
    run_sentiment_tests()