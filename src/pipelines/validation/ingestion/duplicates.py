"""
Checks data for duplicates which means same instance of a match
appearing multiple times.
"""

from maestro import blueprints as bp
from maestro import runtime as rt

from src.pipelines.validation.core.registry import register_check

@register_check("ingestion")
class Duplicates(bp.PipelineStep):
    name = "Duplicates"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        
        matches = ctx.get_artifact("matches")
        if matches.empty:
            message = "matches table empty"
            etx.logger.error(message)
            
            return self.fail(msg = message)
            
        duplicates = (
            matches
            .groupby(
                [
                    "league_division",
                    "season",
                    "match_date",
                    "home_team",
                    "away_team"
                ]
            )
            .size()
            .reset_index(name = "duplicate_count")
        )
        
        duplicates = duplicates[
            duplicates["duplicate_count"] > 1
        ]
        
        if duplicates.empty:
            return self.success()
        
        return self.fail(
            output = {
                "duplicates_found" : len(duplicates),
                "duplicates_records" : duplicates.to_dict(
                    orient = "records"
                )
            }
        )
        