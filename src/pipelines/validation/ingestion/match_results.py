"""
Checks if results are consistent throughout the data which
translates to having home goals greater than away goals if
the match result is home win for example.
"""

from maestro import blueprints as bp
from maestro import runtime as rt
from maestro.common.types import Status

from src.pipelines.validation.core.registry import register_check

@register_check("ingestion")
class MatchResults(bp.PipelineStep):
    def __init__(self, file : str):
        self.file = file
        self.name = f"{file} Match Results"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        
        matches = ctx.get_artifact(self.file)
        if matches.empty:
            message = "matches table empty"
            etx.logger.error(message)
            return bp.StepResult(
                status = Status.FAIL,
                message = message
            )
            
        status = Status.PASS
        
        home_win_error = (
            (matches['full_time_match_result'] == 'H')
            & (
                matches['full_time_home_goals']
                <=
                matches['full_time_away_goals']
            )
        )
        away_win_error = (
            (matches['full_time_match_result'] == 'A')
            & (
                matches['full_time_away_goals']
                <=
                matches['full_time_home_goals']
            )
        )
        draw_error = (
            (matches['full_time_match_result'] == 'D')
            & (
                matches['full_time_home_goals']
                !=
                matches['full_time_away_goals']
            )
        )
        
        issues = (
            matches
            .loc[
                (home_win_error) | (away_win_error) | (draw_error),
                [
                    'league_division',
                    'season',
                    'match_date',
                    'home_team',
                    'away_team',
                    'full_time_match_result',
                    'full_time_home_goals',
                    'full_time_away_goals'
                ]
            ]
        )
        
        if not issues.empty:
            status = Status.FAIL
            etx.logger.error(
                "Found %d matches with inconsistent results",
                len(issues)
            )
        
        return bp.StepResult(
            status = status,
            step_results = {
                "issues_found" : len(issues),
                "inconsistent_matches" : issues.to_dict(orient = "records")
            }
        )
            