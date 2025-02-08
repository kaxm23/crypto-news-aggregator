import nltk
import logging

def initialize_app():
    """Initialize application dependencies"""
    try:
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')
        print("Successfully initialized NLTK data")
        
    except Exception as e:
        logging.error(f"Error initializing application: {e}")
        raise

if __name__ == "__main__":
    initialize_app()