"""
"""

import pandas as pd

INFO_COLS = ['league_division', 'season', 'team']

def get_team_stats(
    df : pd.DataFrame, # standings table
    team : str,
    stats : str
) -> pd.DataFrame:
    return (
        df.loc[
            df['team'] == team,
            ['season', stats]
        ]
        .sort_values("season")
        .reset_index(drop = True)
    )
