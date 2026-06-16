"""
Runs all data quality checks and builds a validation report.
"""

import json
from datetime import datetime
from pathlib import Path

from src.config import (
    VALIDATION_LOGS,
    VALIDATION_SNAPSHOT,
    ROOT_DIR
)
from src.db.engine import engine

from src.validation.check_schema import check_schema
from src.validation.check_missing_values import check_missing_values
from src.validation.check_ranges import check_ranges


def run_pipeline_test(engine):
    
    results = []
    
    schema_results = check_schema(engine)
    results.append(schema_results)
    print("- Ran Schema check.")
    
    missing_values_results = check_missing_values(engine)
    results.append(missing_values_results)
    print("- Ran Missing Values check.")
    
    ranges_result = check_ranges(engine)
    results.append(ranges_result)
    print("- Ran Value Ranges check.")
    
    return results
    
def get_results(report : list) -> dict:
    # overral status of pipeline
    status = "PASS"
    warning_counts = 0
    
    for r in report:
        if r["status"] == "FAIL":
            status = "FAIL"
        elif r["status"] == "WARNING" and r["status"] != 'FAIL':
            status = "WARNING"
            warning_counts += 1
            
    return {
        "timestamp" : datetime.now().isoformat(),
        "overall_status" : status,
        "warnings" : warning_counts,
        "report" : report
    }

def ensure_path(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    
def get_snapshot(
    report : dict,
    path : Path = VALIDATION_SNAPSHOT
) -> None:
    ensure_path(path)
    with open(path, "w") as f:
        json.dump(report, f, indent=4)
        
def add_to_logs(
    report : dict,
    path : Path = VALIDATION_LOGS
) -> None:
    ensure_path(path)
    with open(path, "a") as f:
        f.write(json.dumps(report) + "\n")
        
if __name__ == "__main__":
    print("Starting Validation pipeline !")
    print("="*30)
    
    results = run_pipeline_test(engine)
    report = get_results(results)
    print(f"Completed available checks with {report['warnings']} warnings.")
    print(f"Status: {report['overall_status']}")
    
    get_snapshot(report)
    print(f"Generated report at {VALIDATION_SNAPSHOT.relative_to(ROOT_DIR.parent)}.")
    add_to_logs(report)
    print("="*30)