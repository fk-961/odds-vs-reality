"""
Get a chosen match odds. Can filter by season or average.
"""

import streamlit as st
import pandas as pd

from src.db.engine import engine
from src.utils import load_table

raw_matches_df = load_table("matches", engine)
match_prob_df = load_table("match_probs", engine)
teams_df = load_table("teams", engine).sort_values('team')

def display_match(id : int) -> None:
    match = raw_matches_df.loc[raw_matches_df['id'] == id].iloc[0]
    
    with st.container(border = True):
        st.write(f"{match['home_team']} vs {match['away_team']}")
        st.write(f"{match['full_time_home_goals']} - {match['full_time_away_goals']}")

home = st.selectbox(
    "Choose home team",
    teams_df['team']
)
away = st.selectbox(
    "Choose away team",
    teams_df['team']
)

def get_selected_match_id(home, away):
    selected_match_id = None
    if home == away:
        st.write("It's still physically impossible for these teams to have played each other.")
    else:

        available_matches = raw_matches_df.loc[
            (raw_matches_df['home_team'] == home)
            & (raw_matches_df['away_team'] == away)
        ].sort_values('match_date')

        if available_matches.empty:
            st.write("These teams haven't played each other in our data")
        else:
            available_matches["label"] = (
                available_matches[["home_team", "away_team", "season", "match_date"]]
                .astype(str)
                .apply(
                    lambda x: f"Season {x['season']} | Match Date {x['match_date']}",
                    axis=1
                )
            )
            
            id_to_label = dict(zip(available_matches['id'], available_matches['label']))
            
            if len(available_matches) > 1:
                st.write(f"We found {len(available_matches)}")
                
                selected_match_id = st.pills(
                    "Pick one",
                    options = available_matches['id'].tolist(),
                    selection_mode = 'single',
                    format_func = lambda option : id_to_label[option]
                )
                if selected_match_id is not None:
                    display_match(selected_match_id)
                
            else:
                st.write(f"We found one match")
                st.write(f"Season {available_matches['season'].iloc[0]} | Match Date {available_matches['match_date'].iloc[0]}")
                selected_match_id = available_matches['id'].iloc[0]
                display_match(selected_match_id)
                
    return selected_match_id

selected_match_id = get_selected_match_id(home, away)
            
selected_match_odds_df = match_prob_df.loc[
    match_prob_df['match_id'] == selected_match_id
]

def display_odds(df : pd.DataFrame) -> None:
    df = df.copy()
    
    with st.container(border = True):
        st.write("Closing Odds/probabilites")
        id_to_bookmaker = dict(zip(df['match_id'], df['bookmaker']))
        bookmakers = df['bookmaker'].sort_values().tolist()
        bookmakers_map = {
            "bet365" : "Bet365",
            "betwin" : "Bet & Win",
            "pinnacle" : "Pinnacle",
            "market_average" : "Market Avg",
            "market_maximum" : "Market Max"
        }
        selected_bookmaker = st.segmented_control(
            "Pick one bookmaker",
            options = bookmakers,
            selection_mode = 'single',
            format_func = lambda option : bookmakers_map[option]
        )
        
        closing_odds = df.loc[
            df['bookmaker'] == selected_bookmaker,
            ['closing_home_odds', 'closing_away_odds', 'closing_draw_odds']
        ]
        
        if selected_bookmaker is not None:
            closing_norm_probs = df.loc[
                df['bookmaker'] == selected_bookmaker,
                ['closing_home_norm_prob', 'closing_away_norm_prob', 'closing_draw_norm_prob']
            ].map(lambda x : str(round(x*100,2))+"%")
            
            on = st.toggle("Activate to switch to normalized implied probabilities")
            
            overround = df.loc[
                df['bookmaker'] == selected_bookmaker,
                'closing_overround'
            ].iloc[0]
            st.write(f"Overround {round(overround*100, 2)}%")
            if on:
                st.dataframe(closing_norm_probs)
            else:
                st.dataframe(closing_odds)
        
            
if selected_match_id is not None:
    display_odds(selected_match_odds_df)