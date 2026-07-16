from src.core.framework.artifact import Artifact
from src.core.framework.pipeline import Pipeline
from src.core.framework.orchestrator import PipelineExecution

from src.analytics.core.context import AnalyticsContext
from src.analytics.steps.build_match_metrics import BuildMatchMetrics
from src.analytics.steps.build_bookmaker_metrics import BuildBookmakerMetrics
from src.core.common_steps.load_table import LoadTable
from src.core.common_steps.persist_table import PersistTable
from src.db.engine import engine

# Artifacts
match_metrics = Artifact(
    name = "match_metrics",
    builders = [
        LoadTable("match_probs"), BuildMatchMetrics()
    ],
    validators = [],
    persisters = [PersistTable("match_metrics", "match_metrics")],
    dependencies = ["match_probs"]
)
bookmaker_metrics = Artifact(
    name = "bookmaker_metrics",
    builders = [BuildBookmakerMetrics()],
    validators = [],
    persisters = [PersistTable("bookmaker_metrics", "bookmaker_metrics")],
    dependencies = ["match_metrics"]
)

# Job
pipeline = Pipeline(
    name = "analytics",
    artifacts = [match_metrics, bookmaker_metrics]
)
context = AnalyticsContext(engine)
analytics_job = PipelineExecution(
    pipeline = pipeline, context = context
)