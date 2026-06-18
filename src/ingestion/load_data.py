"""
Loads the data retrieved into our database.
"""

from typing import Tuple
import pandas as pd
from pathlib import Path
from sqlalchemy.engine import Engine

from src.mappings import col_mapping

def prepare_data(
    source_path : Path
) -> Tuple[list, pd.DataFrame, dict]:
    """Creates a dataframe of all the data that we have in our
    raw data folder.

    Args:
        source_path (Path): Path to our raw data folder

    Returns:
        pd.DataFrame: DataFrame containing all the data
    """
    
    data = []
    results = []
    nb_files = 0
    total_rows = 0

    for file in source_path.glob("*.csv"):
        print(f"- Found {file.stem} CSV")

        df = pd.read_csv(file)
        
        df = df[df.columns.intersection(col_mapping.keys())]
        df = df.rename(columns=col_mapping)

        df["season"] = file.stem[3:5] + "/" + file.stem[5:]
        df["league_division"] = "L1"
        
        df["match_date"] = pd.to_datetime(df["match_date"], dayfirst=True).dt.date

        data.append(df)
        results.append({
            "file" : file.stem,
            "rows" : int(df.shape[0]),
            "columns" : int(df.shape[1]),
            "status" : "PASS"
        })
        
        nb_files += 1
        total_rows += int(df.shape[0])
    
    if not data:
        print("No files found.")
        return (
            [{"status" : "FAIL"}],
            pd.DataFrame(),
            {
                "files_processed" : 0,
                "rows_loaded" : 0
            }
        )
    
    return (
        results,
        pd.concat(data, ignore_index=True),
        {
            "files_processed" : nb_files,
            "rows_loaded" : total_rows
        }
    )

def load_data(
    engine : Engine,
    source_path : Path,
    if_exists : str = "append"
) -> list:
    """Load our data into the database

    """
    results, data, metadata = prepare_data(source_path)
    if data.empty:
        return results, metadata
    
    data.to_sql(
        "matches",
        engine,
        if_exists = if_exists,
        index = False
    )
    return results, metadata
    