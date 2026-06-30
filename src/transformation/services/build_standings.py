"""
Extracts match standings of seasons.
"""

import numpy as np
import pandas as pd

def get_season_standings(df : pd.DataFrame) -> pd.DataFrame:

    home = pd.DataFrame({
        "team": df["home_team"],
        "played": 1,
        "wins": np.where(df["full_time_match_result"] == "H", 1, 0),
        "draws": np.where(df["full_time_match_result"] == "D", 1, 0),
        "losses": np.where(df["full_time_match_result"] == "A", 1, 0),
        "goals_for": df["full_time_home_goals"],
        "goals_against": df["full_time_away_goals"],
        "points": np.select(
            [
                df["full_time_match_result"] == "H",
                df["full_time_match_result"] == "D"
            ],
            [3, 1],
            default=0
        )
    })

    away = pd.DataFrame({
        "team": df["away_team"],
        "played": 1,
        "wins": np.where(df["full_time_match_result"] == "A", 1, 0),
        "draws": np.where(df["full_time_match_result"] == "D", 1, 0),
        "losses": np.where(df["full_time_match_result"] == "H", 1, 0),
        "goals_for": df["full_time_away_goals"],
        "goals_against": df["full_time_home_goals"],
        "points": np.select(
            [
                df["full_time_match_result"] == "A",
                df["full_time_match_result"] == "D"
            ],
            [3, 1],
            default=0
        )
    })

    standings = (
        pd.concat([home, away], ignore_index=True)
        .groupby("team", as_index=False)
        .agg(
            played=("played", "sum"),
            wins=("wins", "sum"),
            draws=("draws", "sum"),
            losses=("losses", "sum"),
            goals_for=("goals_for", "sum"),
            goals_against=("goals_against", "sum"),
            points=("points", "sum")
        )
    )

    standings["goal_diff"] = (
        standings["goals_for"] -
        standings["goals_against"]
    )

    standings = standings.sort_values(
        by=["points", "goal_diff", "goals_for"],
        ascending=False
    ).reset_index(drop=True)

    standings["position"] = standings.index + 1

    return standings

def build_standings(df : pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    all_standings = []
    
    league_season = df[['league_division', 'season']].drop_duplicates()
    
    for league, season in league_season.itertuples(index = False):
        df_season = df.loc[
            (df['league_division'] == league) &
            (df['season'] == season)
        ]
        
        season_standings = get_season_standings(df_season)
        season_standings['league_division'] = league
        season_standings['season'] = season
        
        all_standings.append(season_standings)
        
    final = pd.concat(all_standings, ignore_index=True)

    final = final[
        [
            "league_division",
            "season",
            "position",
            "team",
            "played",
            "wins",
            "draws",
            "losses",
            "goals_for",
            "goals_against",
            "goal_diff",
            "points",
        ]
    ]

    return final