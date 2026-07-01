import logging
from src.core.pipeline import Pipeline
from src.core.logger import PipelineLogger

from src.core.common_steps.load_table import LoadTable
from src.core.common_steps.persist_table import PersistTable
from src.analytics.steps.build_match_metrics import BuildMatchMetrics
from src.analytics.steps.build_bookmaker_metrics import BuildBookmakerMetrics

from src.analytics.core.context import AnalyticsContext

from src.config import ANALYTICS_SNAPSHOT, ANALYTICS_LOGS
from src.db.engine import engine

analytics_steps = [
    LoadTable("match_probs"),
    BuildMatchMetrics(),
    PersistTable("match_metrics", "match_metrics"),
    BuildBookmakerMetrics(),
    PersistTable("bookmaker_metrics", "bookmaker_metrics")
]

analytics_pipeline = Pipeline(
    name = "analytics",
    layer = "data_analysis",
    steps = analytics_steps
)

analytics_context = AnalyticsContext(
    logger = PipelineLogger(logging.getLogger("analytics")),
    snapshot_path = ANALYTICS_SNAPSHOT,
    logs_path = ANALYTICS_LOGS,
    engine = engine
)