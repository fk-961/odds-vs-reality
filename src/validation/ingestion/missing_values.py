"""
Checks NULL values in our database's matches table.
"""

import pandas as pd
from maestro import blueprints as bp
from maestro import runtime as rt
from maestro.common.types import Status

from src.validation.core.registry import register_check
from src.mappings import col_mapping, non_bookies_cols

@register_check("ingestion")
class MissingValues(bp.PipelineStep):
    name = "Missing Values"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        
        matches = ctx.get_artifact("matches")
        if matches.empty:
            message = "matches table empty"
            etx.logger.error(message)
            return bp.StepResult(
                status = Status.FAIL,
                message = message
            )
            
        cols = list(col_mapping.values())

        null_counts = (
            matches[cols]
            .isna()
            .sum()
        )

        null_percentages = (
            null_counts / len(matches) * 100
        ).round(2)

        results = {}
        status = Status.PASS

        for col in cols:

            count = null_counts[col]

            results[col] = {
                "nulls": int(count),
                "null_percentage": float(null_percentages[col])
            }

            if count > 0:
                if col in non_bookies_cols:
                    status = Status.FAIL
                elif status != Status.FAIL:
                    status = Status.WARNING

        return bp.StepResult(
            status=status,
            step_results={
                "total_rows": len(matches),
                "columns": results
            }
        )