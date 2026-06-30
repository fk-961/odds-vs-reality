"""
Checks data for duplicates which means same instance of a match
appearing multiple times.
"""

import pandas as pd

from src.core.step import PipelineStep, StepResult
from src.validation.core.registry import register_check
from src.validation.core.context import ValidationContext

@register_check
class Duplicates(PipelineStep):
    
    name = "Duplicates"
    
    
    def run(self, ctx : ValidationContext) -> StepResult:
        query = """
        SELECT
            league_division,
            season,
            match_date,
            home_team,
            away_team,
            COUNT(*) as duplicate_counts
        FROM matches
        GROUP BY
            league_division,
            season,
            match_date,
            home_team,
            away_team
        HAVING COUNT(*) > 1
        """
        
        df = pd.read_sql(query, ctx.engine)
        status = "PASS"
        if not df.empty:
            status = "FAIL"
            
        return StepResult(
            status = status,
            result = {
                "duplicates_found" : len(df),
                "duplicates_records" : df.to_dict(orient = "records")
            }
        )