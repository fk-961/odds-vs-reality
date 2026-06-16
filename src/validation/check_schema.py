"""
Checks whether the raw_table in our database is consistent with
our predefined schema.
"""

import pandas as pd
from src.mappings import col_mapping

def check_schema(engine):
    query = """
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = 'matches';
    """

    actual_df = pd.read_sql(query, engine)
    actual_columns = set(actual_df["column_name"])

    expected_columns = set(col_mapping.values())
    expected_columns.update(["id", "season", "league_division"])

    missing = expected_columns - actual_columns
    extra = actual_columns - expected_columns

    status = "PASS"
    if missing:
        status = "FAIL"
    elif extra:
        status = "WARNING"

    return {
        "check": "schema_validation",
        "status": status,
        "missing_columns": list(missing),
        "extra_columns": list(extra)
    }