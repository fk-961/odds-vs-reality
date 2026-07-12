"""
Build the matches metrics table with having match outcome,
match normalized probabilities per bookmaker, the match result
in one-hot encoding format and metrics like brier score and
log loss. Uses standings table as source of truth.
"""

import pandas as pd
import numpy as np

def build_match_metrics(df : pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    df = df[
        [
            'match_id',
            'bookmaker',
            'season',
            'league_division',
            'home_norm_prob',
            'away_norm_prob',
            'draw_norm_prob',
            'closing_home_norm_prob',
            'closing_away_norm_prob',
            'closing_draw_norm_prob',
            'opening_overround',
            'closing_overround',
            'outcome'
        ]
    ].copy()
    
    df['y_home'] = (df['outcome'] == 'H').astype(int)
    df['y_away'] = (df['outcome'] == 'A').astype(int)
    df['y_draw'] = (df['outcome'] == 'D').astype(int)
    
    
    df['brier_score_opening'] = (
        (df['home_norm_prob'] - df['y_home'])**2
        + (df['away_norm_prob'] - df['y_away'])**2
        + (df['draw_norm_prob'] - df['y_draw'])**2
    )
    
    df['brier_score_closing'] = (
        (df['closing_home_norm_prob'] - df['y_home'])**2
        + (df['closing_away_norm_prob'] - df['y_away'])**2
        + (df['closing_draw_norm_prob'] - df['y_draw'])**2
    )
    
    eps = 1e-15
    df['log_loss_opening'] = -(
        df['y_home'] * np.log(np.clip(df['home_norm_prob'], eps, 1))
        + df['y_away'] * np.log(np.clip(df['away_norm_prob'], eps, 1))
        + df['y_draw'] * np.log(np.clip(df['draw_norm_prob'], eps, 1))
    )
    
    df['log_loss_closing'] = -(
        df['y_home'] * np.log(np.clip(df['closing_home_norm_prob'], eps, 1))
        + df['y_away'] * np.log(np.clip(df['closing_away_norm_prob'], eps, 1))
        + df['y_draw'] * np.log(np.clip(df['closing_draw_norm_prob'], eps, 1))
    )
    
    return df