"""
Checks if results are consistent throughout the data which
translates to having home goals greater than away goals if
the match result is home win for example.
"""

import pandas as pd

from src.core.step import PipelineStep, StepResult
from src.validation.core.registry import register_check
from src.validation.core.context import ValidationContext

@register_check
class MatchResults(PipelineStep):
    
    name = "Match Results"
    
    def run(self, ctx : ValidationContext) -> StepResult:
        query = """
        SELECT
            "id",
            "league_division",
            "season",
            "match_date",
            "home_team",
            "away_team",
            "full_time_match_result",
            "full_time_home_goals",
            "full_time_away_goals"
        FROM matches
        WHERE (
            (full_time_match_result = 'H') AND
            (full_time_home_goals <= full_time_away_goals)
        ) OR (
            (full_time_match_result = 'A') AND
            (full_time_away_goals <= full_time_home_goals) 
        ) OR (
            (full_time_match_result = 'D') AND
            (full_time_home_goals != full_time_away_goals)
        )
        """
        df = pd.read_sql(query, ctx.engine)
        
        status = "PASS"
        if not df.empty:
            status = "FAIL"
            
        return StepResult(
            status = status,
            result = {
                "inconsistent_match_counts" : len(df),
                "inconsistent_matches_records" : df.to_dict(orient = "records")
            }
        )