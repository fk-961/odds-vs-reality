"""
Creates a table of teams with their aggregate statistics.
"""

import pandas as pd

def build_teams(df : pd.DataFrame) -> pd.DataFrame:
    df = df.copy() # standings table
    
    teams_df = (
        df
        .groupby(['league_division', 'team'])
        .agg(
            matches_played = ('played', 'sum'),
            wins = ('wins', 'sum'),
            draws = ('draws', 'sum'),
            losses = ('losses', 'sum'),
            
            seasons_played = ('season', 'nunique'),
            first_season = ('season', 'min'),
            last_season = ('season', 'max'),
            
            average_position = ('position', 'mean'),
            best_position = ('position', 'min'),
            worst_position = ('position', 'max'),
            
            average_points = ('points', 'mean')
        )
        .reset_index()
        .sort_values('average_points', ascending = False)
    )
    
    return teams_df