import os
from dotenv import load_dotenv

load_dotenv()

HF_AUTH_TOKEN = os.getenv('HF_AUTH_TOKEN')
if not HF_AUTH_TOKEN:
    raise ValueError("HF_AUTH_TOKEN is not set in the environment variables.")

WHISPER_MODEL = "large"  # Fixed model, change here if needed