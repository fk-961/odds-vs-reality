"""
Verify that numeric values fall within reasonable ranges.
"""

import pandas as pd
from sqlalchemy.engine import Engine

from src.mappings import (
    non_bookies_cols,
    bookies_cols,
)

def check_ranges(engine : Engine) -> dict:

    non_bookies_numeric_cols = list(
        set(non_bookies_cols.values()) -
        {
            'league_division',
            'match_date',
            'kick_off',
            'home_team',
            'away_team',
            'half_time_match_result',
            'full_time_match_result'
        }
    )

    # SAFE SQL (no crashing if column issues)
    select_check = [
        f'SUM(CASE WHEN "{col}" < 0 THEN 1 ELSE 0 END) AS "{col}_negative_values"'
        for col in non_bookies_numeric_cols
    ]

    query = f"""
    SELECT {", ".join(select_check)}
    FROM matches
    """

    df = pd.read_sql(query, engine)

    if df.empty:
        raise ValueError("No data returned for non-bookie checks")

    non_bookies_df = df.iloc[0].to_dict()

    # Odds check
    select_check = [
        f'SUM(CASE WHEN "{col}" < 1 OR "{col}" > 100 THEN 1 ELSE 0 END) AS "{col}_weird_values"'
        for col in list(bookies_cols.values())
    ]

    query = f"""
    SELECT {", ".join(select_check)}
    FROM matches
    """

    df = pd.read_sql(query, engine)

    if df.empty:
        raise ValueError("No data returned for odds checks")

    odds_df = df.iloc[0].to_dict()

    # Status logic (full scan)
    status = "PASS"

    for v in non_bookies_df.values():
        if v > 0:
            status = "FAIL"
            break

    if status == "PASS":
        for v in odds_df.values():
            if v > 0:
                status = "WARNING"
                break

    return {
        "check": "value_ranges",
        "status": status,
        "non_bookie_violations": non_bookies_df,
        "odds_violations": odds_df
    }