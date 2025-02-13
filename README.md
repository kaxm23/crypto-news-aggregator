# Crypto News Sentiment Analyzer

A Flask-based web application that aggregates cryptocurrency news and performs sentiment analysis.

**Last Updated:** 2025-02-13 08:00:18 UTC  
**Maintainer:** [@kaxm23](https://github.com/kaxm23)  
**Project Status:** Active  
**Language Composition:** Python (75.4%), HTML (24.6%)

## Features

- Real-time crypto news aggregation
- Sentiment analysis of news articles
- Clean, responsive web interface
- Color-coded sentiment indicators
- Article summary generation
- Authentication system
- Enhanced text processing
- Automated testing suite

## Technical Details

### News Collection
- Multi-source aggregation from top crypto news sites:
  - CoinDesk
  - CoinTelegraph
  - CryptoNews
- RSS feed parsing with `feedparser`
- Automatic content cleaning and summarization
- Rate-limiting and caching mechanisms

### Sentiment Analysis
- Powered by TextBlob for natural language processing
- Features:
  - Polarity scoring (-1.0 to 1.0)
  - Subjectivity analysis (0.0 to 1.0)
  - Custom sentiment classification
  - Confidence scoring
- Color-coded indicators:
  - Green: Positive sentiment (> 0.3)
  - Yellow: Neutral sentiment (-0.3 to 0.3)
  - Red: Negative sentiment (< -0.3)

### Text Processing
- Advanced text cleaning pipeline:
  - HTML tag removal
  - Special character handling
  - URL detection and processing
  - Cryptocurrency symbol recognition
- Summary generation with customizable length
- Multi-language support (English primary)

## System Requirements

- Python 3.8 or higher
- 512MB RAM minimum
- 1GB storage space recommended
- Internet connection for news fetching
- Modern web browser for interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kaxm23/crypto-news-aggregator.git
cd crypto-news-aggregator
