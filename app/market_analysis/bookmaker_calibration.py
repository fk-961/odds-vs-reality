import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

from src.db.engine import engine
from src.db.utils import load_table

match_metrics_df = load_table("match_metrics", engine)


# select bookmaker
bookmakers_map = {
    "bet365": "Bet365",
    "betwin": "Bet & Win",
    "pinnacle": "Pinnacle",
    "market_average": "Market Avg",
    "market_maximum": "Market Max"
}

bookmakers = sorted(match_metrics_df["bookmaker"].unique().tolist())

st.header('Bookmaker Calibration probabilities')
st.divider()

# selections
right, left = st.columns(2)
selected_bookmaker = right.selectbox(
    label = 'Select bookmaker',
    options = bookmakers,
    format_func = lambda option : bookmakers_map[option]
)

outcome = left.segmented_control(
    label = 'Select outcome',
    options = ['Home', 'Draw', 'Away'],
    selection_mode = 'single',
    default = 'Home',
    required = True
)

# bookmaker calibration
def get_calibration_data(
    bookmaker : str,
    outcome : str,
    bins : np.array
) -> dict[str, tuple[pd.DataFrame, pd.DataFrame]]:
    outcome = outcome.lower()
    outcome_norm_prob = f"{outcome}_norm_prob"
    closing_outcome_norm_prob = f"closing_{outcome}_norm_prob"
    y_outcome = f"y_{outcome}"
    
    probs_df = match_metrics_df.loc[
        match_metrics_df['bookmaker'] == selected_bookmaker,
        [outcome_norm_prob, closing_outcome_norm_prob, y_outcome]
    ].copy()
    
    # binning
    probs_df['opening_bins'] = pd.cut(
        probs_df[outcome_norm_prob],
        bins = bins,
        include_lowest = True
    )
    
    probs_df['closing_bins'] = pd.cut(
        probs_df[closing_outcome_norm_prob],
        bins = bins,
        include_lowest = True
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
    
    # calibration
    opening_calibration = (
        probs_df
        .groupby('opening_bins')
        .agg(
            nb_matches = (y_outcome, 'count'),
            outcome_wins = (y_outcome, 'sum'),
            mean_pred = (outcome_norm_prob, 'mean')
        )
    )
    opening_calibration['observed_freq'] = (
        opening_calibration['outcome_wins'] / opening_calibration['nb_matches']
    )
    
    closing_calibration = (
        probs_df
        .groupby('closing_bins')
        .agg(
            nb_matches = (y_outcome, 'count'),
            outcome_wins = (y_outcome, 'sum'),
            mean_pred = (closing_outcome_norm_prob, 'mean')
        )
    )
    closing_calibration['observed_freq'] = (
        closing_calibration['outcome_wins'] / closing_calibration['nb_matches']
    )
    
    return {
        "opening" : (opening_dist, opening_calibration),
        "closing" : (closing_dist, closing_calibration)
    }
    
# ece
def compute_ece(calibration_df : pd.DataFrame) -> None:
    total_matches = calibration_df['nb_matches'].sum()
    
    return (
        (calibration_df['nb_matches'] / total_matches )
        * (calibration_df['observed_freq'] - calibration_df['mean_pred']).abs()
    ).sum()
    
 
# plots
def display_charts(
    dist_df : pd.DataFrame,
    calibration_df : pd.DataFrame
) -> None:
    
    left, right = st.columns(2)
    
    left.subheader("Probability distribution")
    
    chart = alt.Chart(dist_df).mark_bar().encode(
        x=alt.X("bins", title = "Bins", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("count", title = "Match Count")
    )
    
    left.altair_chart(chart)
    
    right.subheader(
        "Calibration Curve",
        help = """
        Points close to the diagonal indicate good calibration.

        Points below the line → bookmaker is overconfident  
        Points above the line → bookmaker is underconfident
        """
    )
    
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
        
 
# get selected calibration data
bins = np.linspace(0, 1, 11)
calibration_data = get_calibration_data(
    selected_bookmaker, outcome, bins
)
opening_dist, opening_calibration = calibration_data["opening"]
closing_dist, closing_calibration = calibration_data["closing"]

# display everything
on = st.toggle("Switch to closing calibration")

st.subheader("Calibration Summary")
st.metric(
    "ECE",
    f"{compute_ece(opening_calibration):.4f}" if not on else f"{compute_ece(closing_calibration):.4f}",
    border = True
)    
with st.expander("What is ECE?"):
    st.write("""
    Expected Calibration Error measures the weighted average difference
    between predicted probabilities and the observed frequencies across
    probability bins.
    Lower values indicate better calibration.
    """)

    st.latex(r"""
    \mathrm{ECE}
    =
    \sum_{m=1}^{M}
    \frac{n_m}{N}
    \left|
    \mathrm{acc}(B_m)-\mathrm{conf}(B_m)
    \right|
    """)
    
    st.write("""
        Where:
        - $\mathrm{acc}(B_m)$ = observed frequency in bin $m$
        - $\mathrm{conf}(B_m)$ = mean predicted probability in bin $m$
        - $n_m$ = number of samples in bin $m$
        - $N$ = total number of samples
    """)

    st.latex(r"0 \leq \mathrm{ECE} \leq 1")
    
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
    