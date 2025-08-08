from transformers import pipeline
import reddit_extract

sentiment_pipeline = pipeline("sentiment-analysis",framework="pt")
data = reddit_extract.get_reddit_data()
print(data)
# print(sentiment_pipeline(data))
