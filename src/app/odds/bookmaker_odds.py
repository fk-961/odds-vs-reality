"""
Get bookmaker's odds distribution and stats.
"""

import streamlit as st
import pandas as pd

from src.utils import load_table
from src.db.engine import engine

match_probs_df = load_table("match_probs", engine)

bookmakers = match_probs_df['bookmaker'].unique().tolist()

bookmakers_map = {
    "bet365" : "Bet365",
    "betwin" : "Bet & Win",
    "pinnacle" : "Pinnacle",
    "market_average" : "Market Avg",
    "market_maximum" : "Market Max"
}


selected_bookmaker = st.selectbox(
    "Select a bookmaker",
    options = bookmakers,
    format_func = lambda option : bookmakers_map[option]
)

bookmaker_df = match_probs_df.loc[
    match_probs_df['bookmaker'] == selected_bookmaker
]

left, right = st.columns(2, border = True)

left.scatter_chart()