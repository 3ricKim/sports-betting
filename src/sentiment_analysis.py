from transformers import pipeline
import reddit_extract, news_extract

sentiment_pipeline = pipeline("sentiment-analysis",framework="pt")
reddit_data = reddit_extract.get_reddit_data()
news_data = news_extract.get_news_data()

print("REDDIT ##########")
print(reddit_data)
# print(sentiment_pipeline(reddit_data))

# print("NEWS ###########")
# print(news_data)
# print(sentiment_pipeline(news_data))
# print(sentiment_pipeline(data))
