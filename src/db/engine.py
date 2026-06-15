"""
Creates our postgres database
"""

from sqlalchemy import create_engine
from src.config import DB_URL

engine = create_engine(DB_URL)