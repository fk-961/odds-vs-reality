CREATE SCHEMA IF NOT EXISTS metadata;


CREATE TABLE metadata.execution_runs (
    run_id UUID PRIMARY KEY,
    status TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    duration FLOAT NOT NULL,
    pipelines_scheduled INTEGER,
    artifacts_count INTEGER,
    artifacts_passed INTEGER,
    artifacts_failed INTEGER,
    artifacts_skipped INTEGER,
    message TEXT,
    error TEXT
);


CREATE TABLE metadata.pipeline_runs (
    id BIGSERIAL PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES metadata.execution_runs(run_id),
    name TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    duration FLOAT NOT NULL,
    status TEXT NOT NULL,
    artifacts_scheduled INTEGER NOT NULL,
    artifacts_passed INTEGER NOT NULL,
    artifacts_failed INTEGER NOT NULL,
    artifacts_skipped INTEGER NOT NULL,
    message TEXT,
    error TEXT
);


CREATE TABLE metadata.artifact_runs (
    id BIGSERIAL PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES metadata.execution_runs(run_id),
    pipeline_id BIGINT NOT NULL REFERENCES metadata.pipeline_runs(id),
    name TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    duration FLOAT NOT NULL,
    status TEXT NOT NULL,
    message TEXT,
    error TEXT
);


CREATE TABLE metadata.stage_runs (
    id BIGSERIAL PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES metadata.execution_runs(run_id),
    artifact_id BIGINT NOT NULL REFERENCES metadata.artifact_runs(id),
    stage TEXT NOT NULL,
    scheduled_steps INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    duration FLOAT NOT NULL,
    status TEXT NOT NULL,
    steps_attempted INTEGER NOT NULL,
    steps_warnings_count INTEGER NOT NULL,
    message TEXT,
    error TEXT
);


CREATE TABLE metadata.step_runs (
    id BIGSERIAL PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES metadata.execution_runs(run_id),
    stage_id BIGINT NOT NULL REFERENCES metadata.stage_runs(id),
    name TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    duration FLOAT NOT NULL,
    status TEXT NOT NULL,
    step_results JSONB,
    message TEXT,
    error TEXT
);