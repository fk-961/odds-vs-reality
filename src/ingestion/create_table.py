"""
Creates the raw matches table using the schema defined.
"""

from sqlalchemy import text

from src.db.engine import engine
from src.config import DB_SCHEMA

def create_raw_tables() -> None:
    with open(DB_SCHEMA, "r") as f:
        schema_sql = f.read()

    with engine.begin() as conn:
        conn.execute(text(schema_sql))
