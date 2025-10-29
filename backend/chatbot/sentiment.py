from textblob import TextBlob

def analyze_sentiment(text: str) -> str:
    """Classify sentiment as Positive, Negative, or Neutral."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.2:
        return "Positive"
    elif polarity < -0.2:
        return "Negative"
    else:
        return "Neutral"