"""
Checks if every team played the expected number of matches
per the inverse square law 2(n-1).
"""

import pandas as pd
from maestro import blueprints as bp
from maestro import runtime as rt
from maestro.common.types import Status

from src.pipelines.validation.core.registry import register_check

@register_check("ingestion")
class MatchCount(bp.PipelineStep):
    def __init__(self, file : str):
        self.file = file
        self.name = f"{file} Match Count"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        
        matches = ctx.get_artifact(self.file)
        if matches.empty:
            message = "matches table empty"
            etx.logger.error(message)
            
            return self.fail(msg = message)
            
        results = []
        overall_status = Status.PASS

        for (division, season), season_matches in matches.groupby(
            ['league_division', 'season']
        ):

            n = pd.concat(
                [
                    season_matches['home_team'],
                    season_matches['away_team']
                ]
            ).nunique()

            expected = 2 * (n - 1)

            matches_played = (
                season_matches['home_team']
                .value_counts()
                .add(
                    season_matches['away_team'].value_counts(),
                    fill_value=0
                )
                .astype(int)
            )

            issues = matches_played[matches_played != expected]

            max_deviation = 0
            season_status = Status.PASS

            if not issues.empty:
                etx.logger.info(
                    "%s %s: %d teams played an unexpected number of matches",
                    division,
                    season,
                    len(issues)
                )

                affected_ratio = len(issues) / n
                max_deviation = (issues - expected).abs().max()

                if affected_ratio > 0.15 or max_deviation > 3:
                    season_status = Status.FAIL

                else:
                    season_status = Status.WARNING

                if season_status == Status.FAIL:
                    overall_status = Status.FAIL
                elif overall_status == Status.PASS:
                    overall_status = Status.WARNING


            results.append({
                "league_division": division,
                "season": season,
                "expected_nb_matches": expected,
                "affected_teams": len(issues),
                "max_deviation": int(max_deviation),
                "issues": issues.to_dict(),
                "status": season_status.value
            })


        return bp.StepResult(
            status=overall_status,
            step_results={
                "seasons": results
            }
        )