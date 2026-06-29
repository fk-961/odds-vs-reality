"""
Checks if every team played the expected number of matches
per the inverse square law 2(n-1).
"""

import pandas as pd

from src.validation.services.team_numbers import get_nb_teams
from src.validation.core.check import (
    ValidationCheck, CheckResult
)
from src.validation.core.registry import register_check
from src.validation.core.context import ValidationContext

@register_check
class MatchCount(ValidationCheck):
    
    name = "Match Count"
    
    def run(self, ctx : ValidationContext) -> CheckResult:
        total_matches_query = """
        WITH nb_matches AS (
            SELECT
                league_division,
                season,
                home_team AS team
            FROM matches

            UNION ALL

            SELECT
                league_division,
                season,
                away_team AS team
            FROM matches
        )

        SELECT
            league_division,
            season,
            team,
            COUNT(*) AS matches_played
        FROM nb_matches
        GROUP BY
            league_division,
            season,
            team
        """
        total_matches_df = pd.read_sql(total_matches_query, ctx.engine)
        
        # Get the names of leagues and corresponding seasons
        season_leagues_query = """
        SELECT
            "league_division",
            "season"
        FROM matches
        GROUP BY
            "league_division",
            "season"
        """
        season_leagues = pd.read_sql(season_leagues_query, ctx.engine).to_dict(orient = "records")
        
        status = "PASS"
        results = []
        for season in season_leagues:
            n = get_nb_teams(
                season['league_division'],
                season['season'],
                ctx.engine
            )
            
            # expected number of matches
            expected = 2*(n-1)
            
            # matches for that season
            season_df = total_matches_df[
                (total_matches_df['league_division'] == season['league_division']) &
                (total_matches_df['season'] == season['season'])
            ]
            
            # teams that played matches different from the expectd number
            issues = season_df[season_df['matches_played'] != expected]
            if len(issues) > 0:
                status = "WARNING"
                
            season_result = {
                "league_division" : season['league_division'],
                "season" : season['season'],
                "expected_matches_per_team" : expected,
                "issues" : issues.to_dict(orient = "records")
            }
            results.append(season_result)
            
        return CheckResult(
            status = status,
            result = results
        )
