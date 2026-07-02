"""
This file contains the columns mappings used to create our raw table.
For more information, check `notes.txt` file or `exploration_raw.ipynb` notebook.
"""

import pandas as pd
from src.config import RAW_LIGUE1_DIR

raw_l1_cols = {}
for file in RAW_LIGUE1_DIR.glob("*.csv"):
    raw_l1_cols[file.stem] = pd.read_csv(file).columns
    
cols_sets = [set(cols) for cols in raw_l1_cols.values()]
common_cols = set.intersection(*cols_sets)

# mandatory columns
required_cols = set(
    [
        'Div',
        'Date',
        'HomeTeam',
        'AwayTeam',
        'FTHG',
        'FTAG',
        'FTR'
    ]
)

non_bookies_cols = {
    'Div' : "league_division",
    'Date' : "match_date",
    'Time' : "kick_off",
    'HomeTeam' : "home_team",
    'AwayTeam' : "away_team",
    'FTHG' : "full_time_home_goals",
    'FTAG' : "full_time_away_goals",
    'FTR' : "full_time_match_result",
    'HTHG' : "half_time_home_goals",
    'HTAG' : "half_time_away_goals",
    'HTR' : "half_time_match_result",
    'HS' : "home_shots",
    'AS' : "away_shots",
    'HST' : "home_shots_on_target",
    'AST' : "away_shots_on_target",
    'HC' : "home_corners",
    'AC' : "away_corners",
    'HF' : "home_fouls",
    'AF' : "away_fouls",
    'HY' : "home_yellow_cards",
    'AY' : "away_yellow_cards",
    'HR' : "home_red_cards",
    'AR' : "away_red_cards",
}

# Bookmakers used for this project
bookies = {
    "Avg" : "market_average",
    "Max" : "market_maximum",
    "B365" : "bet365",
    "BW" : "betwin",
    "PS" : "pinnacle"
}

bookies_cols = {}
for col in common_cols - set(list(non_bookies_cols.keys())):
    
    for abbreviation, bookmaker in bookies.items():
        # remove all unwanted odds
        if not col.startswith(abbreviation):
            continue
        
        remainder = col[len(abbreviation):]
        name = bookmaker
        
        # check if its closing odds
        if remainder.startswith("C"):
            name += "_closing"
            remainder = remainder[1:]
            
        if remainder == "H":
            name += "_home_odds"
        elif remainder == "A":
            name += "_away_odds"
        elif remainder == "D":
            name += "_draw_odds"
        else:
            continue
        
        bookies_cols[col] = name
        
col_mapping = {
    **non_bookies_cols,
    **bookies_cols
}