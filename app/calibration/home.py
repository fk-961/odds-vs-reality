import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

from src.db.engine import engine
from src.utils import load_table

match_metrics_df = load_table("match_metrics", engine)


# select bookmaker
bookmakers_map = {
    "bet365": "Bet365",
    "betwin": "Bet & Win",
    "pinnacle": "Pinnacle",
    "market_average": "Market Avg",
    "market_maximum": "Market Max"
}

bookmakers = match_metrics_df["bookmaker"].unique().tolist()

st.header('Bookmaker Calibration by Home Wins probabilities')
st.divider()

selected_bookmaker = st.segmented_control(
    label = '',
    default = "bet365",
    required = True,
    width = "stretch",
    options = bookmakers,
    selection_mode = 'single',
    format_func = lambda option : bookmakers_map[option]
)

probs_df = match_metrics_df.loc[
    match_metrics_df['bookmaker'] == selected_bookmaker,
    ['home_norm_prob', 'closing_home_norm_prob', 'y_home']
]

# bookmaker calibration
bins = np.linspace(0, 1, 11)

probs_df['opening_bins'] = pd.cut(
    match_metrics_df['home_norm_prob'],
    bins = bins,
    include_lowest = True
)

probs_df['closing_bins'] = pd.cut(
    match_metrics_df['closing_home_norm_prob'],
    bins = bins,
    include_lowest = True
)

opening_calibration = (
    probs_df
    .groupby('opening_bins')
    .agg(
        nb_matches = ('y_home', 'count'),
        home_wins = ('y_home', 'sum'),
        mean_pred = ('home_norm_prob', 'mean')
    )
)

opening_calibration['observed_freq'] = (
    opening_calibration['home_wins'] / opening_calibration['nb_matches']
)

closing_calibration = (
    probs_df
    .groupby('closing_bins')
    .agg(
        nb_matches = ('y_home', 'count'),
        home_wins = ('y_home', 'sum'),
        mean_pred = ('closing_home_norm_prob', 'mean')
    )
)
closing_calibration['observed_freq'] = (
    closing_calibration['home_wins'] / closing_calibration['nb_matches']
)

# bookmaker probability distribution
opening_dist = (
    probs_df['opening_bins']
    .value_counts()
    .sort_index()
    .rename_axis('bins')
    .rename(index = str)
    .reset_index(name = 'count')
)

closing_dist = (
    probs_df['closing_bins']
    .value_counts()
    .sort_index()
    .rename_axis('bins')
    .rename(index = str)
    .reset_index(name = 'count')
)

on = st.toggle("Switch to closing calibration")

# plots
left, right = st.columns(2)


def display_charts(
    dist_df : pd.DataFrame,
    calibration_df : pd.DataFrame
) -> None:
    
    chart = alt.Chart(dist_df).mark_bar().encode(
        x=alt.X("bins", title = "Bins", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("count", title = "Match Count")
    )
    
    left.altair_chart(chart)
    
    chart = alt.Chart(calibration_df).mark_circle(size=80).encode(
        x=alt.X("mean_pred", title="Predicted Probability per bin"),
        y=alt.Y("observed_freq", title="Observed Frequency per bin"),
        size=alt.Size("nb_matches", title = "Number of matches", scale=alt.Scale(range=[30, 400])),
        tooltip=[
            alt.Tooltip("mean_pred", title="Predicted"),
            alt.Tooltip("observed_freq", title="Observed"),
            alt.Tooltip("nb_matches", title="Matches")
        ]
    )

    line = alt.Chart(pd.DataFrame({"x": [0, 1], "y": [0, 1]})).mark_line(
        strokeDash=[5,5],
        color="red"
    ).encode(
        x=alt.X("x:Q"),
        y=alt.Y("y:Q")
    )

    right.altair_chart(chart + line)
        

left.subheader("Probability distribution")


right.subheader(
    "Calibration Curve",
    help = """
    Points close to the diagonal indicate good calibration.

    Points below the line → bookmaker is overconfident  
    Points above the line → bookmaker is underconfident
    """
)

if on:
    display_charts(
        closing_dist,
        closing_calibration
    )
else:
    display_charts(
        opening_dist,
        opening_calibration
    )