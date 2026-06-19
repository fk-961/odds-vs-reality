"""
Runs all data quality checks and builds a validation report.
"""

import json
from datetime import datetime
from time import perf_counter
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
from src.validation.check_duplicates import check_duplicates
from src.validation.check_team_counts import check_team_counts
from src.validation.check_matches_count import check_matches_count
from src.validation.check_match_results import check_match_results
from src.utils import (
    get_report,
    add_snapshot,
    add_to_logs
)


def run_validation_checks(engine):
    
    results = []
    
    schema_results = check_schema(engine)
    results.append(schema_results)
    print(f"- Ran Schema check -> status : {schema_results['status']}.")
    
    missing_values_results = check_missing_values(engine)
    results.append(missing_values_results)
    print(f"- Ran Missing Values check -> status : {missing_values_results['status']}.")
    
    ranges_result = check_ranges(engine)
    results.append(ranges_result)
    print(f"- Ran Value Ranges check -> status : {ranges_result['status']}.")
    
    duplicates_result = check_duplicates(engine)
    results.append(duplicates_result)
    print(f"- Ran Duplicates check -> status : {duplicates_result['status']}.")
    
    team_counts_result = check_team_counts(engine)
    results.append(team_counts_result)
    print(f"- Ran Team Counts check -> status : {team_counts_result['status']}.")
    
    matches_count_result = check_matches_count(engine)
    results.append(matches_count_result)
    print(f"- Ran Matches Counts check -> status : {matches_count_result['status']}.")
    
    matches_results = check_match_results(engine)
    results.append(matches_results)
    print(f"= Ran Matches Results check -> status : {matches_results['status']}.")
    
    return results
        
if __name__ == "__main__":
    print("="*30)
    print("Starting Validation pipeline !")
    print("="*30)
    
    start = perf_counter()
    start_time = datetime.now().isoformat()
    
    results = run_validation_checks(engine)
    
    end = perf_counter()
    duration = round(end - start, 5)
    
    report = get_report(
        results,
        timestamp = start_time,
        duration_seconds = duration
    )
    print(f"Completed available checks with {report['warnings']} warnings.")
    print(f"Status: {report['overall_status']}")
    print(f"Duration: {duration} seconds")
    
    add_snapshot(report, VALIDATION_SNAPSHOT)
    print(f"Generated report at {VALIDATION_SNAPSHOT.relative_to(ROOT_DIR.parent)}.")
    add_to_logs(report, VALIDATION_LOGS)
    print("="*30)