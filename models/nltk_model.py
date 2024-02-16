from nltk.sentiment import SentimentIntensityAnalyzer

class NltkSentimentModel:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def predict_sentiment(self, example):
        sentiment_scores = self.analyzer.polarity_scores(example)
        return {
            'compound_score': sentiment_scores['compound'],
            'positive_score': sentiment_scores['pos'],
            'negative_score': sentiment_scores['neg'],
            'neutral_score': sentiment_scores['neu']
        }
