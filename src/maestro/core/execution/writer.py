import json
from dataclasses import asdict
from sqlalchemy.engine import Engine

from src.core.framework.orchestrator import MaestroExecutionResult
from src.config import LOGS_DIR
from src.db.metadata.writer import write_execution

class ExecutionWriter:
    
    def run(
        self,
        exec_result : MaestroExecutionResult,
        metadata_engine : Engine
    ):
        self._json_writer(exec_result)
        self._metadata_writer(exec_result, metadata_engine)
    
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
            
    def _metadata_writer(
        self,
        exec_result : MaestroExecutionResult,
        metadata_engine : Engine
    ):
        write_execution(exec_result, metadata_engine)