"""
Creates standings based on bookmaker predictions meaning we
are going to use our expected_points as match results.
"""

import pandas as pd

def build_expected_standings(df : pd.DataFrame) -> pd.DataFrame:
    df = df.copy() # expected_points table
    
    home_team = pd.DataFrame(
        {
            "team" : df['home_team'],
            "bookmaker" : df['bookmaker'],
            "league_division" : df['league_division'],
            "season" : df['season'],
            "expected_opening_points" : df['expected_opening_home_points'],
            "expected_closing_points" : df['expected_closing_home_points']
        }
    )
    
    away_team = pd.DataFrame(
        {
            "team" : df['away_team'],
            "bookmaker" : df['bookmaker'],
            "league_division" : df['league_division'],
            "season" : df['season'],
            "expected_opening_points" : df['expected_opening_away_points'],
            "expected_closing_points" : df['expected_closing_away_points']
        }
    )
    
    expected_standings = (
        pd.concat([home_team, away_team], ignore_index = True)
        .groupby(
            by = [
                'league_division',
                'season',
                'team',
                'bookmaker'
            ],
            as_index = False
        )
        .agg(
            expected_opening_points = (
                "expected_opening_points", "sum"
            ),
            expected_closing_points = (
                "expected_closing_points", "sum"
            )
        )
    )
    
    expected_standings["position"] = (
        expected_standings
        .groupby(["league_division", "season", "bookmaker"])
        ["expected_closing_points"]
        .rank(ascending=False, method="first")
    ).astype(int)
    
    return expected_standings