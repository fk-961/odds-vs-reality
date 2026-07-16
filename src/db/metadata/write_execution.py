from sqlalchemy import text
from sqlalchemy.engine import Engine
import json
from maestro import blueprints as bp

from src.db.engine import engine

def write_execution(
    result: bp.MaestroExecutionResult,
    engine : Engine
):
    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO metadata.execution_runs (
                    run_id,
                    status,
                    timestamp,
                    duration,
                    pipelines_scheduled,
                    artifacts_count,
                    artifacts_passed,
                    artifacts_failed,
                    artifacts_skipped,
                    message,
                    error
                )
                VALUES (
                    :run_id,
                    :status,
                    :timestamp,
                    :duration,
                    :pipelines_scheduled,
                    :artifacts_count,
                    :artifacts_passed,
                    :artifacts_failed,
                    :artifacts_skipped,
                    :message,
                    :error
                )
            """),
            {
                "run_id": result.run_id,
                "status": result.status.value,
                "timestamp": result.timestamp,
                "duration": result.duration_seconds,
                "pipelines_scheduled": result.pipelines_scheduled,
                "artifacts_count": result.artifacts_count,
                "artifacts_passed": result.artifacts_passed,
                "artifacts_failed": result.artifacts_failed,
                "artifacts_skipped": result.artifacts_skipped,
                "message": result.message,
                "error": result.error,
            },
        )

        for pipeline in result.maestro_results or []:

            pipeline_id = conn.execute(
                text("""
                    INSERT INTO metadata.pipeline_runs (
                        run_id,
                        name,
                        timestamp,
                        duration,
                        status,
                        artifacts_scheduled,
                        artifacts_passed,
                        artifacts_failed,
                        artifacts_skipped,
                        message,
                        error
                    )
                    VALUES (
                        :run_id,
                        :name,
                        :timestamp,
                        :duration,
                        :status,
                        :artifacts_scheduled,
                        :artifacts_passed,
                        :artifacts_failed,
                        :artifacts_skipped,
                        :message,
                        :error
                    )
                    RETURNING id
                """),
                {
                    "run_id": result.run_id,
                    "name": pipeline.name,
                    "timestamp": pipeline.timestamp,
                    "duration": pipeline.duration_seconds,
                    "status": pipeline.status.value,
                    "artifacts_scheduled": pipeline.artifacts_scheduled,
                    "artifacts_passed": pipeline.artifacts_passed,
                    "artifacts_failed": pipeline.artifacts_failed,
                    "artifacts_skipped": pipeline.artifacts_skipped,
                    "message": pipeline.message,
                    "error": pipeline.error,
                },
            ).scalar_one()

            for artifact in pipeline.pipeline_results or []:

                artifact_id = conn.execute(
                    text("""
                        INSERT INTO metadata.artifact_runs (
                            run_id,
                            pipeline_id,
                            name,
                            timestamp,
                            duration,
                            status,
                            message,
                            error
                        )
                        VALUES (
                            :run_id,
                            :pipeline_id,
                            :name,
                            :timestamp,
                            :duration,
                            :status,
                            :message,
                            :error
                        )
                        RETURNING id
                    """),
                    {
                        "run_id": result.run_id,
                        "pipeline_id": pipeline_id,
                        "name": artifact.name,
                        "timestamp": artifact.timestamp,
                        "duration": artifact.duration_seconds,
                        "status": artifact.status.value,
                        "message": artifact.message,
                        "error": artifact.error,
                    },
                ).scalar_one()

                for stage in artifact.artifact_results or []:

                    stage_id = conn.execute(
                        text("""
                            INSERT INTO metadata.stage_runs (
                                run_id,
                                artifact_id,
                                stage,
                                scheduled_steps,
                                timestamp,
                                duration,
                                status,
                                steps_attempted,
                                steps_warnings_count,
                                message,
                                error
                            )
                            VALUES (
                                :run_id,
                                :artifact_id,
                                :stage,
                                :scheduled_steps,
                                :timestamp,
                                :duration,
                                :status,
                                :steps_attempted,
                                :steps_warnings_count,
                                :message,
                                :error
                            )
                            RETURNING id
                        """),
                        {
                            "run_id": result.run_id,
                            "artifact_id": artifact_id,
                            "stage": stage.stage.value,
                            "scheduled_steps": stage.scheduled_steps,
                            "timestamp": stage.timestamp,
                            "duration": stage.duration_seconds,
                            "status": stage.status.value,
                            "steps_attempted": stage.steps_attempted,
                            "steps_warnings_count": stage.steps_warnings_count,
                            "message": stage.message,
                            "error": stage.error,
                        },
                    ).scalar_one()

                    for step in stage.stage_results or []:

                        conn.execute(
                            text("""
                                INSERT INTO metadata.step_runs (
                                    run_id,
                                    stage_id,
                                    name,
                                    timestamp,
                                    duration,
                                    status,
                                    step_results,
                                    message,
                                    error
                                )
                                VALUES (
                                    :run_id,
                                    :stage_id,
                                    :name,
                                    :timestamp,
                                    :duration,
                                    :status,
                                    CAST(:step_results AS JSONB),
                                    :message,
                                    :error
                                )
                            """),
                            {
                                "run_id": result.run_id,
                                "stage_id": stage_id,
                                "name": step.name,
                                "timestamp": step.timestamp,
                                "duration": step.duration_seconds,
                                "status": step.status.value,
                                "step_results": json.dumps(step.step_results) if step.step_results else None,
                                "message": step.message,
                                "error": step.error,
                            },
                        )