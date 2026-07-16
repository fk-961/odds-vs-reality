import json
from dataclasses import asdict
from pathlib import Path
from maestro import blueprints as bp

from src.db.metadata.write_execution import write_execution

class ExecutionWriter:
    
    def run(
        self,
        exec_result : bp.MaestroExecutionResult,
        metadata_engine,
        logs_path : Path
    ):
        self._json_writer(exec_result, logs_path)
        self._metadata_writer(exec_result, metadata_engine)
    
    def _json_writer(
        self,
        exec_result : bp.MaestroExecutionResult,
        logs_path : Path
    ):
        
        logs_path.mkdir(exist_ok = True)
        with open(logs_path/"snapshot.json", "w") as f:
            json.dump(
                asdict(exec_result),
                f,
                indent = 4,
                default = str
            )
            
    def _metadata_writer(
        self,
        exec_result : bp.MaestroExecutionResult,
        metadata_engine
    ):
        write_execution(exec_result, metadata_engine)