import streamlit as st

from src.db.engine import engine
from src.utils import load_table
from src.analytics.team_history import get_team_stats

st.set_page_config(layout="wide")


# --------------------------------------------------
# Styling
# --------------------------------------------------

st.markdown("""
<style>

div.block-container {
    padding-top: 5rem;
}

/* Main title */
.main-title {
    color: #D90429;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

/* Section headers */
.section-title {
    color: #D90429;
    font-size: 1.1rem;
    font-weight: 600;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Load data
# --------------------------------------------------

standings = load_table("standings", engine)
teams = load_table("teams", engine)

seasons = sorted(standings["season"].unique())
teams = teams['team']

# --------------------------------------------------
# Page title
# --------------------------------------------------

st.markdown(
    '<div class="main-title">⚽ Ligue 1 Standings Dashboard</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1, 2])

# ==================================================
# LEFT PANEL
# ==================================================

left.markdown(
    '<div class="section-title">Season Champion</div>',
    unsafe_allow_html=True
)

season = left.selectbox(
    "Season",
    seasons
)

season_table = (
    standings.loc[
        standings["season"] == season
    ]
    .sort_values("position")
)

champion = season_table.iloc[0]["team"]

left.metric(
    label="Champion",
    value=champion
)

left.divider()

left.markdown(
    '<div class="section-title">Team History</div>',
    unsafe_allow_html=True
)

team = left.selectbox(
    "Team",
    teams
)

# --------------------------------------------------
# Position history
# --------------------------------------------------

team_positions = get_team_stats(
    standings,
    team,
    "position"
)

left.markdown(
    '<div class="section-title">League Positions</div>',
    unsafe_allow_html=True
)

left.dataframe(
    team_positions,
    hide_index=True,
    use_container_width=True
)

# --------------------------------------------------
# Points history
# --------------------------------------------------

team_points = (
    get_team_stats(
        standings,
        team,
        "points"
    )
    .rename(columns={"points": "team_points"})
)

champion_points = (
    standings.loc[
        standings["position"] == 1,
        ["season", "points"]
    ]
    .rename(columns={"points": "champion_points"})
)

comparison = team_points.merge(
    champion_points,
    on="season",
    how="left"
)

left.markdown(
    '<div class="section-title">Points vs Champion</div>',
    unsafe_allow_html=True
)

left.line_chart(
    comparison.set_index("season")
)

# ==================================================
# RIGHT PANEL
# ==================================================

right.markdown(
    f'<div class="section-title">{season} Final Standings</div>',
    unsafe_allow_html=True
)

with right.container(border=True):
    st.dataframe(
        season_table,
        hide_index=True,
        use_container_width=True
    )