from src.core.framework.artifact import Artifact
from src.core.framework.pipeline import Pipeline
from src.transformation.core.context import TransformationContext
from src.core.framework.orchestrator import PipelineExecution

from src.transformation.steps.build_standings import BuildStandings
from src.transformation.steps.build_teams import BuildTeams
from src.transformation.steps.build_match_probs import BuildMatchProbs
from src.transformation.steps.build_expected_points import BuildExpectedPoints
from src.transformation.steps.build_expected_standings import BuildExpectedStandings

from src.core.common_steps.load_table import LoadTable
from src.core.common_steps.persist_table import PersistTable

from src.db.engine import engine

standings = Artifact(
    name = "standings",
    builders = [LoadTable("matches"), BuildStandings()],
    validators = [],
    persisters = [PersistTable("standings", "standings")],
    dependencies = ["matches"]
)

teams = Artifact(
    name = "teams",
    builders = [BuildTeams()],
    validators = [],
    persisters = [PersistTable("teams", "teams")],
    dependencies = ["standings"]
)

match_probs = Artifact(
    name = "match_probs",
    builders = [BuildMatchProbs()],
    validators = [],
    persisters = [PersistTable("match_probs", "match_probs")],
    dependencies = ["matches"]
)

expected_points = Artifact(
    name = "expected_points",
    builders = [BuildExpectedPoints()],
    validators = [],
    persisters = [PersistTable("expected_points", "expected_points")],
    dependencies = ["match_probs"]
)

expected_standings = Artifact(
    name = "expected_standings",
    builders = [BuildExpectedStandings()],
    validators = [],
    persisters = [PersistTable("expected_standings", "expected_standings")],
    dependencies = ["expected_points"]
)

pipeline = Pipeline(
    name = "transformation",
    artifacts = [
        standings, teams, match_probs, expected_points, expected_standings
    ]
)

context = TransformationContext(
    engine = engine
)

transformation_job = PipelineExecution(
    pipeline = pipeline,
    context = context
)