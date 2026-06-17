"""
Check whether the number of rows we have for a specific
league and season gives us an exact number of teams.

This check accomplished 2 things:
- Checks if the number of rows corresponds to an integer number of
teams.
- Compares the calculated number of teams to the actual number of
teams extracted from our table.

Check raw_standings notebook for more info.
"""

import pandas as pd
import numpy as np
from sqlalchemy.engine import Engine

from src.validation.utils import get_nb_teams

def check_team_counts(engine : Engine) -> dict:
    query = """
    SELECT
        "league_division",
        "season",
        COUNT(*) as "season_row_count"
    FROM matches
    GROUP BY
        "league_division",
        "season"
    """
    df = pd.read_sql(query, engine)
    
    status = "PASS"
    results = {}
    seasons_total = df.to_dict(orient = "records")
    # n(n-1) = k, k nb of rows and n nb of teams
    for season in seasons_total:
        k = season['season_row_count']
        n = (1+np.sqrt(1+4*k))/2
        if not np.isclose(n, round(n)):
            status = "WARNING"
            
        # get the number of distinct teams from table and compare
        unique_teams = get_nb_teams(
            season['league_division'],
            season['season'],
            engine
        )
        if int(round(n)) != unique_teams:
            status = "WARNING"
        results[(
            season['league_division'],
            season['season']
        )] = {
            "row_count" : k,
            "calculated_n" : n,
            "unique_teams_count" : unique_teams
        }
        
    return {
        "check" : "team_counts",
        "status" : status,
        "results" : results
    }
    