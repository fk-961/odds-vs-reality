"""
Reads the matches table into a pandas dataframe.
"""

import pandas as pd
from sqlalchemy.engine import Engine

from src.db.engine import engine

def load_matches_table(engine : Engine) -> pd.DataFrame:
    query = """
    SELECT * FROM matches
    """
    return pd.read_sql(query, engine)
    