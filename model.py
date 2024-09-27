from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch

MODEL_PATH = 'model/model_cache'

# Determine the device (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model and tokenizer from cache
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH).to(device)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# Modified pipeline initialization
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=0 if device.type == "cuda" else -1)

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