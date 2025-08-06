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
player_names = [
    "justin jefferson",
    "jjettas",
    "jetts",
    "j jets",
    "jjeff",
    "jefferson jr",
    "jefferson wr",
    "j. jefferson"
]

football_keywords = [
    # Fantasy Football
    "keeper", "draft", "fantasy", "value", "rb", "wr", "adp", "target share", "snap count",
    
    # Performance & Stats
    "touchdown", "td", "yards", "targets", "receptions", "stats", "production", "volume", "ceiling", "floor",

    # Team Context
    "qb", "quarterback", "offense", "defense", "oc", "coach", "system", "scheme",

    # Injury/Status
    "injury", "hamstring", "hurt", "healthy", "status", "practice", "IR", "return", "out",

    # Game / Season Analysis
    "game", "matchup", "schedule", "bye week", "week", "season", "performance", "highlight", "catch", "win", "loss"
]
skip_words = ['ticket', 'shop', 'sponsor', 'ad', 'discount']

data = []
max_len = int(os.getenv("max-sequence-length"))


def is_relevant_post(post, player):
    if len(post.title.split()) < 8:
        return False
    if any(word in post.title.lower() for word in skip_words):
        return False
    if player.lower() not in post.title.lower() and player.lower() not in post.selftext.lower():
        return False
    combined_text = (post.title + " " + post.selftext).lower()
    if not any(keyword in combined_text for keyword in football_keywords):
        return False
    
    return True
def is_relevant_comment(comment, title):
    comment = comment.lower()
    title = title.lower()
    if len(comment) > max_len or len(comment.split()) < 8:
        return False
    # If player is mentioned in title, require a football keyword in comment
    if any(player in title for player in player_names):
        if not any(keyword in comment for keyword in football_keywords):
            return False
    else:
        # Otherwise, comment must directly mention the player
        if not any(player in comment for player in player_names):
            return False
    return True

def get_reddit_data():
    for name in player_names:
        for post in reddit.subreddit("all").search(query=name,sort="relevance",time_filter="week"):
            if not is_relevant_post(post, name):
                continue
            post_title = post.title
            if any(player in post.title for player in player_names):
                data.append(post_title)
            post.comments.replace_more(limit=None)
            for comment in post.comments.list():
                post_comment = comment.body
                if is_relevant_comment(post_comment,post_title):
                    data.append(post_comment)
    return data
