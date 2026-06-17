"""
Loads the data retrieved into our database.
"""

import pandas as pd
from pathlib import Path

from src.config import ROOT_DIR, RAW_LIGUE1_DIR
from src.db.engine import engine
from src.mappings import col_mapping

def create_df(
    source_path : Path
) -> pd.DataFrame:
    """Creates a dataframe of all the data that we have in our
    raw data folder.

    Args:
        source_path (Path): Path to our raw data folder

    Returns:
        pd.DataFrame: DataFrame containing all the data
    """
    
    data = []

    print(f"Looking for data in {RAW_LIGUE1_DIR.relative_to(ROOT_DIR.parent)}")
    for file in source_path.glob("*.csv"):
        print(f"Found {file.stem} CSV")

        df = pd.read_csv(file)
        
        df = df[df.columns.intersection(col_mapping.keys())]
        df = df.rename(columns=col_mapping)

        df["season"] = file.stem[3:5] + "/" + file.stem[5:]
        df["league_division"] = "L1"
        
        df["match_date"] = pd.to_datetime(df["match_date"], dayfirst=True).dt.date

        data.append(df)
    
    if not data:
        print("No files found.")
        return pd.DataFrame()

    return pd.concat(data, ignore_index=True)

def create_raw_matches(
    if_exists : str = "append"
) -> None:
    """Load our data into the database

    """
    data = create_df(RAW_LIGUE1_DIR)
    data.to_sql(
        "matches",
        engine,
        if_exists = if_exists,
        index = False
    )
    
if __name__ == "__main__":
    create_raw_matches()