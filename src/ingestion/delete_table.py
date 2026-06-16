import argparse
from sqlalchemy import text
from src.db.engine import engine

def drop_table(table_name: str):
    query = text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;')
    with engine.connect() as conn:
        conn.execute(query)
        conn.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", required=True)
    args = parser.parse_args()

    drop_table(args.table)