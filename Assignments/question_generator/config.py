import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY=os.getenv("MY_OPENROUTER_API_KEY")

MODEL_NAME=os.getenv(
    "MODEL_NAME",
    "deepseek/deepseek-chat-v3-0324:free"
)

UPLOAD_DIR=os.getenv("UPLOAD_DIR","uploads")
AUDIO_DIR=os.getenv("AUDIO_DIR","audio")
TRANSCRIPT_DIR=os.getenv("TRANSCRIPT_DIR","transcripts")

os.makedirs(UPLOAD_DIR,exist_ok=True)
os.makedirs(AUDIO_DIR,exist_ok=True)
os.makedirs(TRANSCRIPT_DIR,exist_ok=True)