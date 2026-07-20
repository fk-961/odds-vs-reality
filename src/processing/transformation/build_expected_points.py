"""
Creates expected_points table by using the probabilites
calculated for each bookmker.
"""

import pandas as pd

def build_expected_points(df : pd.DataFrame) -> pd.DataFrame:
    df = df.copy() # match_probs table
    
    expected_points_df = df[[
        'match_id',
        'league_division',
        'season',
        'home_team',
        'away_team',
        'bookmaker'
    ]].copy()
    
    expected_points_df['expected_opening_home_points'] = (
        3 * df['home_norm_prob'] + 1 * df['draw_norm_prob']
    )
    expected_points_df['expected_opening_away_points'] = (
        3 * df['away_norm_prob'] + 1* df['draw_norm_prob']
    )
    
    expected_points_df['expected_closing_home_points'] = (
        3 * df['closing_home_norm_prob'] + 1 * df['closing_draw_norm_prob']
    )
    expected_points_df['expected_closing_away_points'] = (
        3 * df['closing_away_norm_prob'] + 1 * df['closing_draw_norm_prob']
    )
    
    return expected_points_df