import praw
import os
from dotenv import load_dotenv
import config.football_keywords as football_keywords
import config.player_alias as player_alias

load_dotenv()
reddit = praw.Reddit(client_id = os.getenv("reddit-client-id"),
                     client_secret = os.getenv("reddit-secret"),
                     username = os.getenv("reddit-username"),
                     password = os.getenv("reddit-password"),
                     user_agent = os.getenv("reddit-useragent"))
subreddit = reddit.subreddit("fantasyfootball")

skip_words = ['ticket', 'shop', 'sponsor', 'ad', 'discount']

data = []
max_len = int(os.getenv("max-sequence-length"))


def is_relevant_post(post, player):
    if len(post.title.split()) < 8:
        return False
    if any(word in post.title.lower() for word in skip_words):
        return False
    if player.lower() not in post.title.lower():
        return False
    combined_text = (post.title + " " + post.selftext).lower()
    if not any(keyword in combined_text for keyword in football_keywords.football_keywords):
        return False
    print("################",post.title)
    
    return True
def is_relevant_comment(comment, title):
    comment = comment.lower()
    title = title.lower()
    if len(comment) > max_len or len(comment.split()) < 8:
        return False
    if not any(player in comment for player in player_alias.player_alias) or not any(keyword in comment for keyword in football_keywords.football_keywords):
        return False
    return True

def get_reddit_data():
    name = player_alias.player_alias[0]
    for post in reddit.subreddit("all").search(query=name, sort="relevance", time_filter="week"):
        if not is_relevant_post(post, name):
            continue
        post_title = post.title
        if any(player in post.title for player in player_alias.player_alias):
            data.append(post_title)
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            post_comment = comment.body
            if is_relevant_comment(post_comment, post_title):
                data.append(post_comment)
    return data
