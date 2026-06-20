"""
Runs the transformatin pipeline.
"""

from datetime import datetime
from time import perf_counter

from src.db.engine import engine
from src.transformation.load_matches_table import load_matches_table
from src.transformation.build_standings import build_standings
from src.transformation.build_match_probs import build_match_probs
from src.transformation.create_transformed_table import create_transformed_table

if __name__ == "__main__":
    print("="*30)
    print("Starting Transformation pipeline !")
    print("="*30)
    
    start = perf_counter()
    start_time = datetime.now().isoformat()
    
    # Load raw data
    raw_matches_df = load_matches_table(engine)
    
    # Create standings table
    standings_df = build_standings(raw_matches_df)
    create_transformed_table(standings_df, "standings", engine)
    print("Created standings table")
    
    # Create match_probs table
    match_probs_df = build_match_probs(raw_matches_df)
    create_transformed_table(match_probs_df, "match_probs", engine)
    print("Created match_probs table")
    
    end = perf_counter()
    duration = round(end - start, 5)
    
    print(f"Duration: {duration} seconds")
    print("="*30)
    