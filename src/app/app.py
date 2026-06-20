import streamlit as st
import pandas as pd

from src.db.engine import engine
from src.utils import load_table

st.set_page_config(layout = "wide")

standings = load_table("standings", engine)

seasons = sorted(standings['season'].unique())
teams = standings['team'].unique()

st.title("Ligue 1 standings")

left, right = st.columns([1,2], border = True)

left.header("Season Champion")

season = right.selectbox(
    "Season",
    seasons,
    width = 100
)

champion = standings.loc[
    standings['season'] == season, 'team'
].iloc[0]

left.write(champion)

right.dataframe(
    standings.loc[standings['season'] == season],
    width = "content",
    height = "content",
    hide_index = True
)
