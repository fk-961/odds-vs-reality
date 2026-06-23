"""
Runs the analytics pipeline.
"""

from datetime import datetime
from time import perf_counter

from src.db.engine import engine
from src.utils import load_table, create_table
from src.analytics.build_match_metrics import build_match_metrics
from src.analytics.build_bookmaker_metrics import build_bookmaker_metrics

if __name__ == "__main__":
    print("="*30)
    print("Starting Analytics pipeline !")
    print("="*30)
    
    start = perf_counter()
    start_time = datetime.now().isoformat()
    
    match_probs_df = load_table("match_probs", engine)
    match_metrics_df = build_match_metrics(match_probs_df)
    create_table(match_metrics_df, "match_metrics", engine)
    print("Created match_metrics table")
    
    bookmaker_metrics_df = build_bookmaker_metrics(match_metrics_df)
    create_table(bookmaker_metrics_df, "bookmaker_metrics", engine)
    print("Created bookmaker_metrics table")
    
    end = perf_counter()
    duration = round(end - start, 5)
    
    print(f"Duration: {duration} seconds")
    print("="*30)