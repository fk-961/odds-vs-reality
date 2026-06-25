import json
from pathlib import Path

from src.validation.core.pipeline import ValidationExecutionResult

class ValidationReportBuilder:
    
    def __init__(self, snapshot_path : Path, logs_path : Path):
        self.snapshot_path = snapshot_path
        self.logs_path = logs_path
        
    def generate_json_report(self, result : ValidationExecutionResult) -> dict:
        
        return {
            "pipeline" : result.name,
            "layer" : "validation",
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
        
    def add_snapshot(self, result : ValidationExecutionResult):
        self.ensure_path(self.snapshot_path)
        with open(self.snapshot_path, "w") as f:
            json.dump(self.generate_json_report(result), f, indent=4)
            
    def add_logs(self, result : ValidationExecutionResult):
        self.ensure_path(self.logs_path)
        with open(self.logs_path, "a") as f:
            f.write(json.dumps(self.generate_json_report(result)) + "\n")