"""
Check whether the number of rows we have for a specific
league and season gives us an exact number of teams.

This check accomplished 2 things:
- Checks if the number of rows corresponds to an integer number of
teams.
- Compares the calculated number of teams to the actual number of
teams extracted from our table.

Check raw_standings notebook for more info.
"""

import numpy as np
import pandas as pd
from maestro import blueprints as bp
from maestro import runtime as rt
from maestro.common.types import Status

from src.pipelines.validation.core.registry import register_check

@register_check("ingestion")
class TeamCounts(bp.PipelineStep):
    def __init__(self, file : str):
        self.file = file
        self.name = f"{file} Team Counts"
    
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
        
        
        status = Status.PASS
        results = []
        for (league, season), season_matches in matches.groupby(
            ['league_division', 'season']
        ):
            
            # n(n-1) = k, k nb of rows and n nb of teams
            k = int(season_matches.shape[0])
            n = (1 + np.sqrt(1 + 4 * k))/2
            if not np.isclose(n, round(n)):
                status = Status.WARNING
                
            # get the number of distinct teams from table
            expected_n = pd.concat(
                [
                    season_matches['home_team'],
                    season_matches['away_team']
                ]
            ).nunique()
            
            if expected_n != int(round(n)):
                status = Status.WARNING
                
            results.append({
                "league_division" : league,
                "season" : season,
                "nb_rows" : k,
                "calculated_n" : n,
                "nb_teams" : expected_n
            })
            
        return bp.StepResult(
            status = status,
            step_results = {
                "results_per_season" : results
            }
        )