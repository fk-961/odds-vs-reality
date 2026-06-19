"""
Creates a table in our database given a processed dataframe.
"""

import pandas as pd
from sqlalchemy.engine import Engine

from src.db.engine import engine

def create_transformed_table(
    df : pd.DataFrame,
    table_name : str,
    engine : Engine,
    if_exists : str = "replace"
) -> None:
    df.to_sql(
        table_name,
        engine,
        if_exists = if_exists,
        index = False
    )