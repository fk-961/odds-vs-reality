import json
from pathlib import Path

from src.core.pipeline import PipelineExecutionResult

class ReportBuilder:
        
    def generate_json_report(self, result : PipelineExecutionResult) -> dict:
        
        return {
            "pipeline" : result.name,
            "layer" : result.layer,
            "timestamp" : result.timestamp,
            "status" : result.status,
            "warnings" : result.warnings,
            "fails" : result.fails,
            "duration_seconds" : result.duration_seconds,
            "checks" : [
                {
                    "name" : check.name,
                    "status" : check.status,
                    "duration" : check.duration_seconds,
                    "timestamp" : check.timestamp,
                    "result" : check.result
                }
                for check in result.result
            ]
        }
        
    def ensure_path(self, path : Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        
    def add_snapshot(
        self,
        result : PipelineExecutionResult,
        snapshot_path : Path
    ):
        self.ensure_path(snapshot_path)
        with open(snapshot_path, "w") as f:
            json.dump(self.generate_json_report(result), f, indent=4)
            
    def add_logs(
        self,
        result : PipelineExecutionResult,
        logs_path : Path
    ):
        self.ensure_path(logs_path)
        with open(logs_path, "a") as f:
            f.write(json.dumps(self.generate_json_report(result)) + "\n")