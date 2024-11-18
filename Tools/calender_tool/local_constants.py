from dotenv import load_dotenv
import os

load_dotenv()

AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_API_VERSION = "2024-02-15-preview"

MODEL_TEMPERATURE = 0.00
MODEL_NAME = "gpt-4o-mini"
CREDENTIAL_PATH = os.path.abspath("Tools/calender_tool/credentials.json")
CALENDAR_EMAIL = "paranjoygupta@gmail.com"