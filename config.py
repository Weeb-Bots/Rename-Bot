from os import environ, path
from dotenv import load_dotenv

if path.exists("config.env"):
  load_dotenv("config.env", override=True)

def genv(name):
  return environ.get(name, None)

class Config:
  API_ID = int(genv("API_ID")) # Required
  API_HASH = genv("API_HASH") # Required
  BOT_TOKEN = genv("BOT_TOKEN") # Required
  DF_CAP = environ.get("DF_CAP", "**⌬ Uploaded By @Anime_Pile**") # Optinal
  DF_THUMB = "https://te.legra.ph/file/0aca5455329e68aec367d.jpg" # Required Or change code in main.py
