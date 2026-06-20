"""
"""

import pandas as pd

INFO_COLS = ['league_divison', 'season', 'team']

def get_team_stats(
    df : pd.DataFrame,
    team : str,
    stats : str
) -> pd.DataFrame:
    return (
        df.loc[
            df['team'] == team
        ]
        .sort_values("season")
        .reset_index(drop = True)
    )
