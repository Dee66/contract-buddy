[⬅ Back to Section Overview](README.md)

[⬅ Back to Main Index](../../INDEX.md)

# Cost Tracking

## Local Cost Estimation
- Each experiment run logs estimated compute cost based on runtime, CPU/GPU usage, and environment (dev/prod).
- Rates are set in code (see `estimate_local_cost` in `peft_hyperparam_sweep.py`).
- Estimated cost is included in each run’s results and in experiment summaries.

## Cloud Cost Tracking
- If running on cloud, set environment variables:
  - `EC2_INSTANCE_TYPE` (or similar)
  - `CLOUD_HOURLY_RATE` (USD/hour)
- These are logged in experiment metadata.
- (Optional) Integrate with cloud billing APIs for precise cost reporting.

## Where to Find Cost Info
- Per-run and per-experiment cost is logged in:
  - `data/clean/hyperparam_sweep_results.json`
  - `data/clean/experiments.json`
- Summaries and leaderboards include cost columns.

## Visualization
- (Optional) Cost can be visualized alongside accuracy and runtime in benchmark plots.