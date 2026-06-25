"""
Checks data for duplicates which means same instance of a match
appearing multiple times.
"""

import pandas as pd
from sqlalchemy.engine import Engine

from src.validation.core.check import (
    ValidationCheck, CheckResult
)

class Duplicates(ValidationCheck):
    
    name = "Duplicates"
    
    
    def run(self, engine : Engine) -> CheckResult:
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
        
        df = pd.read_sql(query, engine)
        status = "PASS"
        if not df.empty:
            status = "FAIL"
            
        return CheckResult(
            status = status,
            result = {
                "duplicates_found" : len(df),
                "duplicates_records" : df.to_dict(orient = "records")
            }
        )