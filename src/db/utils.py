"""
Common fonctions used accross src scripts.
"""

import json
from pathlib import Path
import pandas as pd
from sqlalchemy.engine import Engine


def load_table(table_name : str, engine : Engine) -> pd.DataFrame:
    query = f"""
    SELECT * FROM {table_name}
    """
    return pd.read_sql(query, engine)

def create_table(
    df : pd.DataFrame,
    table_name : str,
    engine : Engine,
    if_exists : str = "append"
) -> None:
    df.to_sql(
        table_name,
        engine,
        if_exists = if_exists,
        index = False
    )