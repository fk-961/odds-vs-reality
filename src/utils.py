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
    if_exists : str = "replace"
) -> None:
    df.to_sql(
        table_name,
        engine,
        if_exists = if_exists,
        index = False
    )

def get_report(results : list, **metadata) -> dict:
    """Takes the results list after a single execution of a pipeline 
    to generate the dictionary report to JSON. It checks for warnings
    and fails.

    Args:
        results (list): List of results returned after running a
            pipeline.
        metadata : Information specific to a pipeline to add in the
            final report.

    Returns:
        dict: Dictionary to be converted to JSON.
    """
    status = "PASS"
    warning_counts = 0
    
    for r in results:
        if r["status"] == "FAIL":
            status = "FAIL"
        elif r["status"] == "WARNING" and status != 'FAIL':
            status = "WARNING"
            warning_counts += 1
            
    return {
        "overall_status" : status,
        "warnings" : warning_counts,
        **metadata,
        "report" : results
    }

def ensure_path(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    
def add_snapshot(
    report : dict,
    path : Path
) -> None:
    ensure_path(path)
    with open(path, "w") as f:
        json.dump(report, f, indent=4)
        
def add_to_logs(
    report : dict,
    path : Path
) -> None:
    ensure_path(path)
    with open(path, "a") as f:
        f.write(json.dumps(report) + "\n")