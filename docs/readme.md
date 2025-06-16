# Data Pipeline

## Overview

This module provides a modular, extensible pipeline for data ingestion, cleaning, sensitive data filtering, and versioning for Contract Buddy's AI code assistant.

## Structure

- `config.yaml` — Central configuration for sources and paths.
- `pipeline_runner.py` — Orchestrates the full pipeline.
- `data_ingestion.py` — Fetches raw data from configured sources.
- `data_cleaning.py` — Cleans and normalizes raw data.
- `sensitive_data_filter.py` — Detects and removes secrets or PII.
- `versioning.py` — Handles dataset versioning.
- `sources/` — Source-specific fetchers (e.g., GitHub, docs, Stack Overflow).
- `utils.py` — Shared utilities.
- `tests/` — Unit tests for pipeline components.

## Requirements

Before running the pipeline, install all dependencies:

```sh
pip install -r ../../requirements.txt
```

### Main dependencies

- `requests` (for HTTP requests to data sources)
- `sentence-transformers` (for embedding models)
- `numpy` (for vector operations)
- `pyyaml` (for config file parsing)
- `vectordb` (for vector database operations; swap for production DB as needed)

If you see a `ModuleNotFoundError`, install the missing package with `pip install <package>`.

## Usage

```sh
python pipeline_runner.py
```

## Running the Pipeline

```sh
python pipeline_runner.py config.yaml
```

Outputs and logs will be written to the directories specified in `config.yaml`.

## Adding a New Source

1. Create a new module in `sources/` (e.g., `my_source.py`).
2. Add configuration to `config.yaml`.
3. Update `data_ingestion.py` to call new fetcher.

## Testing

```sh
python -m unittest discover tests
```

## Best Practices

- All data is logged, versioned, and auditable.
- Sensitive data is filtered before storage.
- Modular design enables easy extension and maintenance.
