"""
Checks whether the raw_table in our database is consistent with
our predefined schema.
"""

import pandas as pd

from src.mappings import col_mapping
from src.core.step import PipelineStep, StepResult
from src.validation.core.registry import register_check
from src.validation.core.context import ValidationContext

@register_check
class Schema(PipelineStep):
    
    name = "Schema"
    
    def run(self, ctx : ValidationContext) -> StepResult:
        
        query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'matches';
        """

        actual_df = pd.read_sql(query, ctx.engine)
        actual_columns = set(actual_df["column_name"])

        expected_columns = set(col_mapping.values())
        expected_columns.update(["id", "season", "league_division"])

        missing = expected_columns - actual_columns
        extra = actual_columns - expected_columns

        status = "PASS"
        if missing:
            status = "FAIL"
        elif extra:
            status = "WARNING"
            
        return StepResult(
            status = status,
            result = {
                "missing_columns" : list(missing),
                "extra_columns" : list(extra)
            }
        )
