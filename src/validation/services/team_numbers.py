"""
Returns the number of distinct teams in matches table.
"""

import pandas as pd
from sqlalchemy.engine import Engine

def get_nb_teams(
    league : str,
    season : str,
    engine : Engine
) -> pd.DataFrame:
    query = f"""
    SELECT "home_team", "away_team"
    FROM matches
    WHERE "league_division" = '{league}' AND "season" = '{season}'
    """
    teams_df = pd.read_sql(query, engine)
    return len(
        set(teams_df['home_team']) | set(teams_df['away_team'])
    )