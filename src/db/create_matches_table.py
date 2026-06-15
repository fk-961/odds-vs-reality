"""
Creates the raw matches table using the schema defined.
"""

from sqlalchemy import text
from src.db.engine import engine

def create_tables():
    with open("src/db/schema.sql", "r") as f:
        schema_sql = f.read()

    with engine.begin() as conn:
        conn.execute(text(schema_sql))

    print("Tables created successfully")

if __name__ == "__main__":
    create_tables()