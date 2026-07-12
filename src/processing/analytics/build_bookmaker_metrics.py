"""
Aggregates match metrics by bookmaker using match_metrics table.
"""

import pandas as pd

def build_bookmaker_metrics(df : pd.DataFrame) -> pd.DataFrame:
    df = (
        df
        .copy()
        .groupby(
            ['league_division', 'season', 'bookmaker'],
            as_index = False
        )
        .agg(
            brier_score_opening = ('brier_score_opening', 'mean'),
            brier_score_closing = ('brier_score_closing', 'mean'),
            log_loss_opening = ('log_loss_opening', 'mean'),
            log_loss_closing = ('log_loss_closing', 'mean'),
            opening_overround = ('opening_overround', 'mean'),
            closing_overround = ('closing_overround', 'mean') 
        )
    )
    
    df['closing_vs_opening_brier'] = (
        df['brier_score_opening'] - df['brier_score_closing']
    )
    
    df['closing_vs_opening_log_loss'] = (
        df['log_loss_opening'] - df['log_loss_closing']
    )
    
    df['closing_vs_opening_overround'] = (
        df['opening_overround'] - df['closing_overround']
    )
    
    return df