import os
from dotenv import load_dotenv
import requests
import config.football_keywords as football_keywords
import config.player_alias as player_alias
import re

load_dotenv()
api_key = os.getenv("news-data-api-key")
base_url = "https://gnews.io/api/v4/search?q="
player_name = player_alias.player_alias[0]

def get_news_data():
    data = set()
    url = base_url + player_name + "&apikey=" + api_key
    response = requests.get(url)

    if response.status_code == 200:
        articles = response.json().get("articles", [])
        for item in articles:
            desc = item.get("description", "").lower()
            for kw in football_keywords.football_keywords:
                if re.search(rf'\b{re.escape(kw)}\b', desc):
                    data.add(item.get("description", ""))
                    break
    else:
        print(response.status_code, response.text)

    return list(data)