"""
Features added to raw table:
- Goal difference
- Result encoding
- Odds implied probabilites
"""

import pandas as pd
import numpy as np

from src.mappings import bookies, bookies_cols

def add_goal_diff(df : pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['goal_diff'] = df['home_goals'] - df['away_goals']
    
    return df

def add_result_encoding(df : pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['result_encoding'] = df['full_time_match_result'].map(
        {
            'H' : 1,
            'D' : 0,
            'A' : -1
        }
    )
    
    return df

def add_odds_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    bookmakers = [
        "bet365",
        "bet365_closing",
        "betwin",
        "betwin_closing",
        "pinnacle",
        "pinnacle_closing",
        "market_average",
        "market_average_closing",
        "market_maximum",
        "market_maximum_closing"
    ]

    for bookmaker in bookmakers:

        home_col = f"{bookmaker}_home_odds"
        draw_col = f"{bookmaker}_draw_odds"
        away_col = f"{bookmaker}_away_odds"

        # skip if bookmaker doesn't exist
        if home_col not in df.columns:
            continue

        # raw implied probabilities
        home_raw = 1 / df[home_col]
        draw_raw = 1 / df[draw_col]
        away_raw = 1 / df[away_col]

        df[f"{bookmaker}_home_raw_prob"] = home_raw
        df[f"{bookmaker}_draw_raw_prob"] = draw_raw
        df[f"{bookmaker}_away_raw_prob"] = away_raw

        # bookmaker margin
        total = home_raw + draw_raw + away_raw

        df[f"{bookmaker}_margin"] = total - 1

        # normalized probabilities
        df[f"{bookmaker}_home_normalized_prob"] = home_raw / total
        df[f"{bookmaker}_draw_normalized_prob"] = draw_raw / total
        df[f"{bookmaker}_away_normalized_prob"] = away_raw / total

    return df