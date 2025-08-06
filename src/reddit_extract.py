import praw
# from pmaw import PushshiftAPI
import os
from dotenv import load_dotenv

load_dotenv()
reddit = praw.Reddit(client_id = os.getenv("reddit-client-id"),
                     client_secret = os.getenv("reddit-secret"),
                     username = os.getenv("reddit-username"),
                     password = os.getenv("reddit-password"),
                     user_agent = os.getenv("reddit-useragent"))
subreddit = reddit.subreddit("fantasyfootball")

## use llm to get player nicknames
player_names = ["Justin Jefferson", "Jettas"]
data = []

def is_relevant_post(post, player):
    skip_words = ['ticket', 'shop', 'sponsor', 'ad', 'discount']
    if any(word in post.title.lower() for word in skip_words):
        return False
    if player.lower() not in post.title.lower() and player.lower() not in post.selftext.lower():
        return False
    return True

def get_reddit_data():
    for name in player_names:
        for post in reddit.subreddit("all").search(query=name,sort="relevance",time_filter="week"):
            if not is_relevant_post(post, name):
                continue
            max_len = int(os.getenv("max-sequence-length"))
            post_title = post.title
            if len(post.title) < max_len:
                data.append(post_title)
            post.comments.replace_more(limit=None)
            for comment in post.comments.list():
                post_comment = comment.body
                if len(post_comment) < max_len:
                    data.append(post_comment)
                # print(comment.body)
    return data
