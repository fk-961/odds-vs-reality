"""
Reads a given table into a pandas dataframe.
"""

import pandas as pd
from sqlalchemy.engine import Engine

from src.db.engine import engine

def load_table(table_name : str, engine : Engine) -> pd.DataFrame:
    query = f"""
    SELECT * FROM {table_name}
    """
    return pd.read_sql(query, engine)
    