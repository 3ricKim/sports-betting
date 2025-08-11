from dotenv import load_dotenv
import os
import google.generativeai as genai
from google.generativeai import types

## use llm to get player nicknames
load_dotenv()
genai.configure(api_key=os.getenv("gemini-api-key"))

model = genai.GenerativeModel(model_name="gemini-2.5-flash",
                              system_instruction='''You will be provided with an athlete's name. You need to only the most common nicknames the player may have, but don't include vague names. Also include any abbreviations of the name,
                              The response type must be a python list.
                              The first element in the list must be the player's full name.
                              For example, if the user provides Justin Jefferson, a good answer is [
    "Justin Jefferson",
    "jjettas",
    "jetts",
    "j jets",
    "jjeff",
    "jefferson jr",
    "jefferson wr",
    "j. jefferson",
] Notice how Justin or Jefferson is not included because it may be confused with other people.
Do not add any quotation around your answer so the response can be saved directly as a variable''')
response = model.generate_content(
    "Calvin Johnson",
)

player_alias = response.text
