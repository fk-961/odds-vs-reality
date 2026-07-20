from ..runtime.context import ExecutionContext
from ..runtime.logger import PipelineLogger
from ..blueprints.orchestrator import (
    Maestro, MaestroExecutionResult
)
from .runners.orchestrator import MaestroRunner

class MaestroExecutor:
    
    def __init__(self, logger : PipelineLogger):
        
        self._etx = ExecutionContext(
            logger = logger,
        )
        self._runner = MaestroRunner()
        
    def execute(
        self,
        maestro : Maestro
    ) -> MaestroExecutionResult:
        
        return self._runner.run(maestro, self._etx)