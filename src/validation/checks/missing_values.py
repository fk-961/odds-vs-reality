"""
Checks NULL values in our database's matches table.
"""

import pandas as pd

from src.mappings import col_mapping, non_bookies_cols
from src.core.step import PipelineStep, StepResult
from src.validation.core.registry import register_check
from src.validation.core.context import ValidationContext

@register_check
class MissingValues(PipelineStep):
    
    name = "Missing Values"
    
    def run(self, ctx : ValidationContext) -> StepResult:
        
        cols = list(col_mapping.values())
        select_check = [
            f"SUM(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END) AS {col}_null_count"
            for col in cols
        ]
        
        query = f"""
        SELECT
            COUNT(*) AS total_rows,
            {", ".join(select_check)}
        FROM matches
        """
        
        result = pd.read_sql(query, ctx.engine)
        
        # result is one row with results for each columns
        result = result.iloc[0].to_dict()
        total_rows = result['total_rows']
        
        results = {}
        status = "PASS"
        for col in cols:
            null_counts = result[f"{col}_null_count"]
            results[col] = {
                "nulls" : int(null_counts),
                "null_percentage" : round(null_counts/total_rows*100, 2)
            }
            if col in list(non_bookies_cols.values()) and null_counts > 0:
                status = "FAIL"
            elif null_counts > 0:
                status = "WARNING"
                
        return StepResult(
            status = status,
            result = results
        )
