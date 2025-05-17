import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    DB_NAME = os.getenv("DB_NAME", "default_db")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", f"sqlite:///{DB_NAME}.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    # Switch to another LLM provider by overriding *_API_KEY and in openai_client.py