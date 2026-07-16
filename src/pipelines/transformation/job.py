from maestro import blueprints as bp

from src.pipelines.transformation.core.context import TransformationContext
from src.pipelines.transformation.steps.build_standings import BuildStandings
from src.pipelines.transformation.steps.build_teams import BuildTeams
from src.pipelines.transformation.steps.build_match_probs import BuildMatchProbs
from src.pipelines.transformation.steps.build_expected_points import BuildExpectedPoints
from src.pipelines.transformation.steps.build_expected_standings import BuildExpectedStandings

from src.db.common.load_table import LoadTable
from src.db.common.persist_table import PersistTable

from src.db.engine import engine

standings = bp.Artifact(
    name = "standings",
    builders = [LoadTable("matches"), BuildStandings()],
    validators = [],
    persisters = [PersistTable("standings", "standings")],
    dependencies = ["matches"]
)

teams = bp.Artifact(
    name = "teams",
    builders = [BuildTeams()],
    validators = [],
    persisters = [PersistTable("teams", "teams")],
    dependencies = ["standings"]
)

match_probs = bp.Artifact(
    name = "match_probs",
    builders = [BuildMatchProbs()],
    validators = [],
    persisters = [PersistTable("match_probs", "match_probs")],
    dependencies = ["matches"]
)

expected_points = bp.Artifact(
    name = "expected_points",
    builders = [BuildExpectedPoints()],
    validators = [],
    persisters = [PersistTable("expected_points", "expected_points")],
    dependencies = ["match_probs"]
)

expected_standings = bp.Artifact(
    name = "expected_standings",
    builders = [BuildExpectedStandings()],
    validators = [],
    persisters = [PersistTable("expected_standings", "expected_standings")],
    dependencies = ["expected_points"]
)

pipeline = bp.Pipeline(
    name = "transformation",
    artifacts = [
        standings, teams, match_probs, expected_points, expected_standings
    ]
)

context = TransformationContext(
    engine = engine
)

transformation_job = bp.PipelineExecution(
    pipeline = pipeline,
    context = context
)