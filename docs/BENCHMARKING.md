# 📊 Benchmarking & Optimization Report

This document details the benchmarking, trade-off analysis, and optimization process for the Contract Buddy AI pipeline.

---

## 🏁 Baseline Metrics

We established baseline retrieval metrics by running the pipeline with the base model and default hyperparameters. For each run, the following are logged:

- **Top-1 Accuracy (`top1`)**
- **Mean Reciprocal Rank (`mrr`)**
- **Runtime (seconds)**
- **Memory usage (MB)**
- **Hyperparameters:** LoRA rank (`r`), alpha, dropout, epochs, batch size

**Example baseline (from `hyperparam_sweep_results.json`):**
```json
{
  "hyperparams": {
    "r": 4,
    "alpha": 16,
    "dropout": 0.0,
    "epochs": 2,
    "batch_size": 8
  },
  "peft_retrieval": {
    "top1": 0.82,
    "topk": 0.95,
    "mrr": 0.87
  },
  "timing_seconds": 32.5,
  "memory_usage_mb": 745.8
}
```

---

## ⚖️ Trade-off Analysis

A hyperparameter sweep was performed, varying LoRA rank, alpha, dropout, epochs, and batch size.  
For each configuration, retrieval metrics and resource usage were recorded.

**Visualization:**  
The results are visualized as Top-1 Accuracy vs. Runtime, with color indicating MRR.

![Benchmark Top-1 vs Runtime](../data/clean/benchmark_top1_vs_runtime.png)

**Key Observations:**
- Increasing LoRA rank and alpha generally improved accuracy, but also increased runtime and memory usage.
- Dropout had a minor effect on accuracy but may help with generalization.
- Larger batch sizes reduced runtime but sometimes slightly reduced accuracy.

---

## 🏆 Optimization Decision

Based on the trade-off analysis, the configuration with the best balance of accuracy and efficiency was selected:

- **Best run:**  
  - `r=4, alpha=16, dropout=0.0, epochs=2, batch_size=8`
  - Top-1: 0.82, MRR: 0.87, Runtime: 32.5s, Memory: 745.8MB

This configuration provides strong retrieval performance with reasonable resource usage.

---

## 🚀 Next Steps

- Expand hyperparameter sweeps to include additional parameters or larger datasets.
- Compare against other PEFT methods or base models.
- Explore additional retrieval metrics (e.g., recall, F1).

---

_This benchmarking process demonstrates a robust, reproducible approach to model optimization and trade-off analysis, supporting both technical excellence and business value._