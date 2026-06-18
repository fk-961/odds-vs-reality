"""
Runs the ingestion pipeline that creates our raw matches
table and build reports.
"""

import json
from datetime import datetime
from time import perf_counter

from src.db.engine import engine
from src.config import (
    ROOT_DIR,
    RAW_LIGUE1_DIR,
    INGESTION_SNAPSHOT,
    INGESTION_LOGS
)
from src.ingestion.create_table import create_raw_tables
from src.ingestion.load_data import load_data
from src.utils import (
    get_report,
    add_snapshot,
    add_to_logs
)

if __name__ == "__main__":
    print("="*30)
    print("Starting Ingestion pipeline !")
    print("="*30)
    
    start = perf_counter()
    start_time = datetime.now().isoformat()
    
    create_raw_tables()
    print("- Created raw table.")
    
    print(f"Looking for data in {RAW_LIGUE1_DIR.relative_to(ROOT_DIR.parent)}")
    results, metadata = load_data(engine, RAW_LIGUE1_DIR)
    print("- Loaded data into database.")
    
    end = perf_counter()
    duration = round(end - start, 5)
    
    report = get_report(
        results,
        timestamp = start_time,
        duration_seconds = duration,
        **metadata
    )
    print(f"Completed Ingestion pipeline with {report['warnings']} warnings.")
    print(f"Status: {report['overall_status']}")
    print(f"Duration: {duration} seconds")
    
    add_snapshot(report, INGESTION_SNAPSHOT)
    print(f"Generated report at {INGESTION_SNAPSHOT.relative_to(ROOT_DIR.parent)}")
    add_to_logs(report, INGESTION_LOGS)
    
    print("="*30)