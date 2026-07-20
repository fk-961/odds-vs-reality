"""
Verify that numeric values fall within reasonable ranges.
"""

from maestro import blueprints as bp
from maestro import runtime as rt
from maestro.common.types import Status

from src.mappings import (
    non_bookies_cols,
    bookies_cols,
)
from src.pipelines.validation.core.registry import register_check

@register_check("ingestion")
class ValueRanges(bp.PipelineStep):
    name = "Value Ranges"

    def run(
        self,
        ctx: rt.PipelineContext,
        etx: rt.ExecutionContext,
    ) -> bp.StepResult:

        matches = ctx.get_artifact("matches")
        if matches.empty:
            message = "matches table empty"
            etx.logger.error(message)
            return self.fail(msg=message)

        non_bookies_numeric_cols = list(
            set(non_bookies_cols.values())
            - {
                "league_division",
                "match_date",
                "kick_off",
                "home_team",
                "away_team",
                "half_time_match_result",
                "full_time_match_result",
            }
        )

        # Count negative values in non-bookmaker numeric columns
        non_bookie_violations = (
            (matches[non_bookies_numeric_cols] < 0)
            .sum()
            .astype(int)
            .rename(lambda c: f"{c}_negative_values")
            .to_dict()
        )

        # Count bookmaker odds outside [1, 100]
        odds_cols = list(bookies_cols.values())

        odds_violations = (
            ((matches[odds_cols] < 1) | (matches[odds_cols] > 100))
            .sum()
            .astype(int)
            .rename(lambda c: f"{c}_weird_values")
            .to_dict()
        )

        status = Status.PASS

        if any(v > 0 for v in non_bookie_violations.values()):
            status = Status.FAIL
        elif any(v > 0 for v in odds_violations.values()):
            status = Status.WARNING

        return bp.StepResult(
            status=status,
            step_results = {
                "non_bookie_violations": non_bookie_violations,
                "odds_violations": odds_violations,
            }
        )