"""
Get bookmaker odds distribution and statistics.
"""

import streamlit as st
import pandas as pd

from src.utils import load_table
from src.db.engine import engine

bookmaker_metrics_df = load_table("bookmaker_metrics", engine)

bookmakers_map = {
    "bet365": "Bet365",
    "betwin": "Bet & Win",
    "pinnacle": "Pinnacle",
    "market_average": "Market Avg",
    "market_maximum": "Market Max"
}

bookmakers = bookmaker_metrics_df["bookmaker"].unique().tolist()

selected_bookmaker = st.selectbox(
    "Select a bookmaker",
    options=bookmakers,
    format_func=lambda option: bookmakers_map.get(option, option)
)

seasons = sorted(
    bookmaker_metrics_df["season"].unique(),
    reverse=True
)

current_season = seasons[0]
last_season = seasons[1]


bookmaker_df = bookmaker_metrics_df.loc[
    bookmaker_metrics_df["bookmaker"] == selected_bookmaker
]

global_metrics = (
    bookmaker_df
    .groupby("bookmaker", as_index=False)
    .agg(
        brier_score_opening=("brier_score_opening", "mean"),
        brier_score_closing=("brier_score_closing", "mean"),
        log_loss_opening=("log_loss_opening", "mean"),
        log_loss_closing=("log_loss_closing", "mean"),
        opening_overround=("opening_overround", "mean"),
        closing_overround=("closing_overround", "mean")
    )
    )

current_metrics = (
    bookmaker_df.loc[
        bookmaker_df["season"] == current_season
    ]
        .groupby("bookmaker", as_index=False)
        .agg(
            brier_score_opening=("brier_score_opening", "mean"),
            brier_score_closing=("brier_score_closing", "mean"),
            log_loss_opening=("log_loss_opening", "mean"),
            log_loss_closing=("log_loss_closing", "mean"),
            opening_overround=("opening_overround", "mean"),
            closing_overround=("closing_overround", "mean")
        )
)

last_metrics = (
    bookmaker_df.loc[
            bookmaker_df["season"] == last_season
        ]
        .groupby("bookmaker", as_index=False)
        .agg(
            brier_score_opening=("brier_score_opening", "mean"),
            brier_score_closing=("brier_score_closing", "mean"),
            log_loss_opening=("log_loss_opening", "mean"),
            log_loss_closing=("log_loss_closing", "mean"),
            opening_overround=("opening_overround", "mean"),
            closing_overround=("closing_overround", "mean")
        )
    )


def display_metric_card(
    container,
    label: str,
    metric_col: str,
    delta_color: str = "normal"
):
    current_value = current_metrics[metric_col].iloc[0]
    last_value = last_metrics[metric_col].iloc[0]
    global_value = global_metrics[metric_col].iloc[0]

    evolution = (
        bookmaker_df
        .groupby("season")[metric_col]
        .mean()
        .sort_index()
    )

    container.metric(
        label=f"Current {label}",
        value=round(current_value, 3),
        delta=round(current_value - last_value, 3),
        delta_color=delta_color,
        border=True,
        chart_data=evolution,
        chart_type="area"
    )

    container.metric(
        label=f"Global {label}",
        value=round(global_value, 3),
        border=True
    )

with st.container():
    on = st.toggle("Switch to closing metrics")
    
    left, middle, right = st.columns(3)
    
    if on:
        display_metric_card(
            left,
            label="Brier",
            metric_col="brier_score_closing",
            delta_color="inverse"
        )
        
        display_metric_card(
            middle,
            label="Log Loss",
            metric_col="log_loss_closing",
            delta_color="inverse"
        )
        
        display_metric_card(
            right,
            label="Overround",
            metric_col="closing_overround",
            delta_color="inverse"
        )
        
    else:

        display_metric_card(
            left,
            label="Brier",
            metric_col="brier_score_opening",
            delta_color="inverse"
        )

        display_metric_card(
            middle,
            label="Log Loss",
            metric_col="log_loss_opening",
            delta_color="inverse"
        )

        display_metric_card(
            right,
            label="Overround",
            metric_col="opening_overround",
            delta_color="inverse"
        )