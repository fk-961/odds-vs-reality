"""
Creates one artifact per CSV file to be processed.
"""

from maestro import blueprints as bp
from pathlib import Path
import pandas as pd

from src.pipelines.ingestion.steps.load_file import LoadFile
from src.pipelines.ingestion.steps.fix_columns import FixColumns
from src.pipelines.validation.core.registry import get_checks
checks = get_checks("ingestion")
from src.db.common.persist_table import PersistTable

def build_artifacts(path : Path) -> list[bp.Artifact]:
    artifacts = []
    
    csv_files = list(path.glob("*.csv"))
    for file in csv_files:
        
        df = pd.read_csv(file)
        artifacts.append(bp.Artifact(
            name = f"{file.stem}",
            builders = [
                LoadFile(file),
                FixColumns(file.stem)
            ],
            validators = [
              check(f"normalized_{file.stem}") for check in checks  
            ],
            persisters = [
              PersistTable(
                  f"normalized_{file.stem}",
                  "matches",
                  "append"
              )  
            ],
            dependencies = []
        ))
        
    return artifacts