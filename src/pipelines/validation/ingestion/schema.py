"""
Checks whether the raw_table in our database is consistent with
our predefined schema.
"""

from maestro import blueprints as bp
from maestro import runtime as rt

from src.pipelines.validation.core.registry import register_check
from src.mappings import col_mapping

@register_check("ingestion")
class Schema(bp.PipelineStep):
    name = "Schema"
    
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
        
        matches_cols = set(matches.columns)
        expected_cols = set(col_mapping.values())
        expected_cols.update(['season', 'league_division'])
        
        missing = expected_cols - matches_cols
        extra = matches_cols - expected_cols
        output = {
            "missing_cols" : list(missing),
            "extra_cols" : list(extra)
        }
        
        if missing:
            return self.fail(
                msg = "Missing required columns",
                output = output
            )
            
        elif extra:
            return self.warning(
                msg = "matches contains extra columns",
                output = output
            )
            
        return self.success(output = output)