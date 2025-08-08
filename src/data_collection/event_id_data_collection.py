import urllib.request
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
odds_api_key = os.getenv("odds-api-key")
print(odds_api_key)

base_url = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events?apiKey="

url = base_url + odds_api_key
response = requests.get(url)

if response.status_code == 200:
    json_data = response.json()

    file_path = "data/event_id.json"
    with open(file_path, "w") as f:
        json.dump(json_data, f, indent=4)
else:
    print("Error: " + str(response.status_code) + " " + response.reason)

