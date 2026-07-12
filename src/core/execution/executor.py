from src.core.execution.context import ExecutionContext
from src.core.execution.logger import PipelineLogger
from src.core.framework.orchestrator import (
    MaestroRunner, Maestro
)
from src.core.execution.writer import ExecutionWriter

class MaestroExecutor:
    
    def __init__(self):
        
        self._etx = ExecutionContext(
            logger = PipelineLogger()
        )
        self._runner = MaestroRunner()
        self._writer = ExecutionWriter()
        
    def execute(
        self,
        maestro : Maestro
    ) -> None:
        
        results = self._runner.run(maestro, self._etx)
        self._writer.run(results)