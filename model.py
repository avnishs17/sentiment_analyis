from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import os

MODEL_PATH = 'model/model_cache'

# Load model and tokenizer from cache
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def predict_sentiment(text):
    result = sentiment_pipeline(text)[0]
    
    label = result['label']
    score = result['score']
    
    if label == 'POSITIVE':
        sentiment = 2
    elif label == 'NEGATIVE':
        sentiment = 0
    else:
        sentiment = 1  # This case might never occur with the current model
    
    return sentiment, score