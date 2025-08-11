import google.generativeai as genai
from dotenv import load_dotenv
import os
## use llm to get player nicknames

load_dotenv()
gemini_api_key = os.getenv("gemini-api-key")
genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])
reply = chat.send_message("Hello")
print(reply)

player_alias = [
    "Justin Jefferson",
    "justin jefferson",
    "jjettas",
    "jetts",
    "j jets",
    "jjeff",
    "jefferson jr",
    "jefferson wr",
    "j. jefferson",
    "jefferson",
    "JJ"
]