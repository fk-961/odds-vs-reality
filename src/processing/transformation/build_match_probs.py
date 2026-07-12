"""
Creates the match_probs table that has odds and
probabilites columns for every match with given bookmaker
and add the bookmaker's margin column
"""

import pandas as pd

from src.mappings import bookies

def build_match_probs(df : pd.DataFrame) -> pd.DataFrame:
    df = df.copy() # raw table
    
    match_probs = []
    
    bookmakers = list(bookies.values())
    for bookmaker in bookmakers:
        
        # opening odds
        home_odds_col = f"{bookmaker}_home_odds"
        away_odds_col = f"{bookmaker}_away_odds"
        draw_odds_col = f"{bookmaker}_draw_odds"
        
        # closing odds
        closing_home_odds = f"{bookmaker}_closing_home_odds"
        closing_away_odds = f"{bookmaker}_closing_away_odds"
        closing_draw_odds = f"{bookmaker}_closing_draw_odds"
        
        # check if bookmaker data is available
        required_cols = [
            home_odds_col,
            away_odds_col,
            draw_odds_col,
            closing_home_odds,
            closing_away_odds,
            closing_draw_odds
        ]
        if not all(col in df.columns for col in required_cols):
            print(f"Skipping {bookmaker}, reason : missing columns")
            continue
        
        cols = ['id', 'full_time_match_result'] + required_cols + [
            'home_team',
            'away_team',
            'league_division',
            'season'
        ]
        bookmaker_odds_df = df[cols].rename(
            columns = {
                'id' : "match_id",
                'full_time_match_result' : 'outcome',
                home_odds_col : "home_odds",
                away_odds_col : "away_odds",
                draw_odds_col : "draw_odds",
                closing_home_odds : "closing_home_odds",
                closing_away_odds : "closing_away_odds",
                closing_draw_odds : "closing_draw_odds"
            }
        ).copy()
        
        bookmaker_odds_df['bookmaker'] = bookmaker
        
        # calculate raw probs
        home_raw_probs = 1/bookmaker_odds_df['home_odds']
        away_raw_probs = 1/bookmaker_odds_df['away_odds']
        draw_raw_probs = 1/bookmaker_odds_df['draw_odds']
        
        closing_home_raw_probs = 1/bookmaker_odds_df['closing_home_odds']
        closing_away_raw_probs = 1/bookmaker_odds_df['closing_away_odds']
        closing_draw_raw_probs = 1/bookmaker_odds_df['closing_draw_odds']
        
        bookmaker_odds_df['home_raw_prob'] = home_raw_probs
        bookmaker_odds_df['away_raw_prob'] = away_raw_probs
        bookmaker_odds_df['draw_raw_prob'] = draw_raw_probs
        
        bookmaker_odds_df['closing_home_raw_prob'] = closing_home_raw_probs
        bookmaker_odds_df['closing_away_raw_prob'] = closing_away_raw_probs
        bookmaker_odds_df['closing_draw_raw_prob'] = closing_draw_raw_probs
        
        # normalized probabilites
        total = home_raw_probs + away_raw_probs + draw_raw_probs
        closing_total = closing_home_raw_probs + closing_away_raw_probs + closing_draw_raw_probs
        
        bookmaker_odds_df['opening_overround'] = total - 1
        bookmaker_odds_df['closing_overround'] = closing_total - 1
        
        
        bookmaker_odds_df['home_norm_prob'] = home_raw_probs / total
        bookmaker_odds_df['away_norm_prob'] = away_raw_probs / total
        bookmaker_odds_df['draw_norm_prob'] = draw_raw_probs / total
        
        bookmaker_odds_df['closing_home_norm_prob'] = closing_home_raw_probs / closing_total
        bookmaker_odds_df['closing_away_norm_prob'] = closing_away_raw_probs / closing_total
        bookmaker_odds_df['closing_draw_norm_prob'] = closing_draw_raw_probs / closing_total
        
        match_probs.append(bookmaker_odds_df)
        
    if not match_probs:
        return pd.DataFrame()
    
    final = pd.concat(match_probs, ignore_index = True)
    
    return final[[
        'match_id',
        'league_division',
        'season',
        'home_team',
        'away_team',
        'outcome',
        'bookmaker',
        'home_odds',
        'away_odds',
        'draw_odds',
        'closing_home_odds',
        'closing_away_odds',
        'closing_draw_odds',
        'home_raw_prob',
        'away_raw_prob',
        'draw_raw_prob',
        'closing_home_raw_prob',
        'closing_away_raw_prob',
        'closing_draw_raw_prob',
        'home_norm_prob',
        'away_norm_prob',
        'draw_norm_prob',
        'closing_home_norm_prob',
        'closing_away_norm_prob',
        'closing_draw_norm_prob',
        'opening_overround',
        'closing_overround'
    ]]
        