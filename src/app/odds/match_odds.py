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

def display_match(id : int):
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

if home == away:
    st.write("It's still physically impossible for these teams to have played each other.")
else:

    available_matches = raw_matches_df.loc[
        (raw_matches_df['home_team'] == home)
        & (raw_matches_df['away_team'] == away)
    ]

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
            
            selected_match = st.pills(
                "Pick one",
                options = available_matches['id'].tolist(),
                selection_mode = 'single',
                format_func = lambda option : id_to_label[option]
            )
            display_match(selected_match)
            
        else:
            st.write(f"We found one match")
            st.write(f"Season {available_matches['season'].iloc[0]} | Match Date {available_matches['match_date'].iloc[0]}")
            display_match(available_matches['id'].iloc[0])