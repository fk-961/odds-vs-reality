import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Useful directories path
ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_LIGUE1_DIR = ROOT_DIR/"data"/"raw"/"ligue1"
LOGS_DIR = ROOT_DIR/"logs"
VALIDATION_SNAPSHOT = LOGS_DIR/"validation"/"snapshot.json"
VALIDATION_LOGS = LOGS_DIR/"validation"/"logs.jsonl"

# DB credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# DB schema
DB_SCHEMA = ROOT_DIR/"src"/"db"/"schema.sql"