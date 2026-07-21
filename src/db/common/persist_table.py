from sqlalchemy import text
from maestro import blueprints as bp
from maestro import runtime as rt

from src.db.common.utils import create_table

class PersistTable(bp.PipelineStep):
    
    def __init__(
        self,
        artifact : str,
        table_name : str,
        mode : str = "append"
    ):
        self.artifact = artifact
        self.table_name = table_name
        self.mode = mode
        
        if mode not in {"append", "replace"}:
            raise ValueError(f"Unsupported perist mode: {mode}")
        
        self.name = f"Persist table [{self.table_name}] mode = {mode}"
    
    def run(
        self,
        ctx : rt.PipelineContext,
        etx : rt.ExecutionContext
    ) -> bp.StepResult:
        
        df = ctx.get_artifact(self.artifact)
        if df.empty:
            message = f"{self.artifact} table empty"
            etx.logger.error(message)
            
            return self.fail(msg = message)
        
        etx.logger.info(
            "Persisting %d rows into %s (%s)",
            int(df.shape[0]),
            self.table_name,
            self.mode
        )
        if self.mode == "replace":
            with ctx.engine.begin() as conn:
                conn.execute(
                    text(
                        f"""
                        TRUNCATE TABLE {self.table_name}
                        RESTART IDENTITY;
                        """
                    )
                )
                
        create_table(
            df,
            self.table_name,
            ctx.engine,
            if_exists=self.mode
        )
        
        etx.logger.info("Successfully persisted !")
        
        return self.success(
            output = {
                "table" : self.table_name,
                "mode" : self.mode,
                "rows_inserted" : len(df)
            }
        )