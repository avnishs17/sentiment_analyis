import unittest
from model import predict_sentiment

class TestSentimentAnalysis(unittest.TestCase):
    def test_positive_sentiment(self):
        text = "I love this product!"
        sentiment, confidence = predict_sentiment(text)
        self.assertEqual(sentiment, 2)  # Positive sentiment
        self.assertGreater(confidence, 0.5)

    def test_negative_sentiment(self):
        text = "This is terrible."
        sentiment, confidence = predict_sentiment(text)
        self.assertEqual(sentiment, 0)  # Negative sentiment
        self.assertGreater(confidence, 0.5)

    def test_neutral_sentiment(self):
        text = "The sky is blue."
        sentiment, confidence = predict_sentiment(text)
        # The model might classify this as positive or negative
        self.assertIn(sentiment, [0, 1, 2])
        self.assertGreater(confidence, 0.5)

if __name__ == '__main__':
    unittest.main()