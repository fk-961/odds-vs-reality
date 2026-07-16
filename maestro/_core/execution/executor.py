from ..runtime.context import ExecutionContext
from ..runtime.logger import PipelineLogger
from ..blueprints.orchestrator import Maestro
from .runners.orchestrator import MaestroRunner

class MaestroExecutor:
    
    def __init__(self, engine):
        
        self._etx = ExecutionContext(
            logger = PipelineLogger(),
            metadata_engine = engine
        )
        self._runner = MaestroRunner()
        
    def execute(
        self,
        maestro : Maestro
    ) -> None:
        
        results = self._runner.run(maestro, self._etx)