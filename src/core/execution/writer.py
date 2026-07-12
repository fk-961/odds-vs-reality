import json
from dataclasses import asdict

from src.core.framework.orchestrator import MaestroExecutionResult
from src.config import LOGS_DIR

class ExecutionWriter:
    
    def run(
        self,
        exec_result : MaestroExecutionResult,
    ):
        self._json_writer(exec_result)
    
    def _json_writer(
        self,
        exec_result : MaestroExecutionResult,
    ):
        
        LOGS_DIR.mkdir(exist_ok = True)
        with open(LOGS_DIR/"snapshot.json", "w") as f:
            json.dump(
                asdict(exec_result),
                f,
                indent = 4,
                default = str
            )