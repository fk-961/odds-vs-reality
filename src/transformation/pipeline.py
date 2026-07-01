import logging
from src.core.logger import PipelineLogger
from src.core.pipeline import Pipeline

from src.transformation.core.context import TransformationContext

from src.core.common_steps.load_table import LoadTable
from src.transformation.steps.build_standings import BuildStandings
from src.transformation.steps.build_teams import BuildTeams
from src.transformation.steps.build_match_probs import BuildMatchProbs
from src.transformation.steps.build_expected_points import BuildExpectedPoints
from src.transformation.steps.build_expected_standings import BuildExpectedStandings
from src.core.common_steps.persist_table import PersistTable

from src.config import TRANSFORMATION_SNAPSHOT, TRANSFORMATION_LOGS
from src.db.engine import engine

transformation_steps = [
    LoadTable("matches"),
    BuildStandings(),
    PersistTable("standings" , "standings"),
    BuildTeams(),
    PersistTable("teams", "teams"),
    BuildMatchProbs(),
    PersistTable("match_probs", "match_probs"),
    BuildExpectedPoints(),
    PersistTable("expected_points", "expected_points"),
    BuildExpectedStandings(),
    PersistTable("expected_standings", "expected_standings")
]

transformation_pipeline = Pipeline(
    "transformation",
    "data_transformation",
    steps = transformation_steps
)

transformation_context = TransformationContext(
    logger = PipelineLogger(logging.getLogger("transformation")),
    snapshot_path = TRANSFORMATION_SNAPSHOT,
    logs_path = TRANSFORMATION_LOGS,
    engine = engine
)