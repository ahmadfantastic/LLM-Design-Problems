import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    DB_NAME = os.getenv("DB_NAME", "default_db")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DATABASE_URI = os.getenv("DATABASE_URI")

    if DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = DATABASE_URI
    elif all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_NAME}.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    # Switch to another LLM provider by overriding *_API_KEY and in openai_client.py
