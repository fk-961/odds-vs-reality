from maestro import blueprints as bp

from src.pipelines.analytics.core.context import AnalyticsContext
from src.pipelines.analytics.steps.build_match_metrics import BuildMatchMetrics
from src.pipelines.analytics.steps.build_bookmaker_metrics import BuildBookmakerMetrics

from src.db.common.load_table import LoadTable
from src.db.common.persist_table import PersistTable
from src.db.engine import engine

# Artifacts
match_metrics = bp.Artifact(
    name = "match_metrics",
    builders = [
        LoadTable("match_probs"), BuildMatchMetrics()
    ],
    validators = [],
    persisters = [PersistTable("match_metrics", "match_metrics")],
    dependencies = ["match_probs"]
)
bookmaker_metrics = bp.Artifact(
    name = "bookmaker_metrics",
    builders = [BuildBookmakerMetrics()],
    validators = [],
    persisters = [PersistTable("bookmaker_metrics", "bookmaker_metrics")],
    dependencies = ["match_metrics"]
)

# Job
pipeline = bp.Pipeline(
    name = "analytics",
    artifacts = [match_metrics, bookmaker_metrics]
)
context = AnalyticsContext(engine)
analytics_job = bp.PipelineExecution(
    pipeline = pipeline, context = context
)