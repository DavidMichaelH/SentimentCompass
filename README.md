# SentimentCompass
SentimentCompass is a Flask web application that analyzes the sentiment of comments on YouTube videos using the Hugging Face API. It provides a user-friendly interface for users to enter a YouTube video URL, fetches comments from that video, and then evaluates their sentiment using a pre-trained model.

# Features
- Fetch YouTube video comments using the YouTube Data API
- Sentiment analysis using Hugging Face's distilbert-base-uncased-finetuned-sst-2-english model
- Clean and responsive user interface
- Summary statistics with total comments, positive/negative comments, and sentiment score
