import streamlit as st
import pandas as pd

from src.db.engine import engine


df = pd.read_sql(
    "SELECT * FROM standings",
    engine
)

st.title("Ligue 1 Standings")

seasons = sorted(df["season"].unique())

selected_season = st.selectbox(
    "Season",
    seasons
)

season_df = (
    df[df["season"] == selected_season]
    .sort_values("position")
)

champion = season_df.iloc[0]["team"]

st.metric(
    "Champion",
    champion
)

st.dataframe(
    season_df[
        [
            "position",
            "team",
            "played",
            "wins",
            "draws",
            "losses",
            "goals_for",
            "goals_against",
            "goal_diff",
            "points"
        ]
    ],
    use_container_width=True
)