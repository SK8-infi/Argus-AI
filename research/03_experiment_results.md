# 03 — Model Training Experiments & Results

**Generated**: 2026-06-16

---

## Model Comparison (Test Set)

| Model | F1 | Precision | Recall | AUC-ROC | PR-AUC | FPR | TP | FP | FN | TN |
|-------|----|-----------|--------|---------|--------|-----|----|----|----|----|
| XGBoost | **0.9388** | 0.9583 | 0.9200 | 0.9880 | 0.9592 | 0.0012 | 46 | 2 | 4 | 1675 |
| LightGBM | **0.9495** | 0.9592 | 0.9400 | 0.9827 | 0.9589 | 0.0012 | 47 | 2 | 3 | 1675 |
| Meta-Learner | **0.9400** | 0.9400 | 0.9400 | 0.9795 | 0.9595 | 0.0018 | 47 | 3 | 3 | 1674 |
| LSTM-AE | **0.3333** | — | — | — | — | — | — | — | — | — |
| IsolationForest | **0.3051** | — | — | — | — | — | — | — | — | — |

## Top 20 Features (XGBoost Importance)

| Rank | Feature | Importance |
|------|---------|-----------|
| 1 | roll_7d_max_data_volume_mb | 0.257237 |
| 2 | roll_14d_std_data_volume_mb | 0.067232 |
| 3 | expanding_max_systems | 0.060690 |
| 4 | roll_14d_std_novelty_score | 0.044338 |
| 5 | zscore_role_unique_systems_accessed | 0.031712 |
| 6 | roll_7d_std_novelty_score | 0.028406 |
| 7 | clearance_normalized | 0.022400 |
| 8 | roll_7d_std_data_egress_volume | 0.020071 |
| 9 | delta_novelty_score | 0.017244 |
| 10 | is_weekend | 0.016330 |
| 11 | roll_14d_max_data_volume_mb | 0.015569 |
| 12 | zscore_dept_data_egress_volume | 0.012734 |
| 13 | roll_14d_std_data_egress_volume | 0.012256 |
| 14 | is_new_device | 0.011676 |
| 15 | expanding_max_data_volume | 0.011513 |
| 16 | zscore_role_data_volume_mb | 0.011139 |
| 17 | roll_7d_mean_data_volume_mb | 0.009795 |
| 18 | roll_14d_mean_is_after_hours | 0.009620 |
| 19 | cum_7d_is_after_hours | 0.008198 |
| 20 | roll_14d_max_device_count | 0.008187 |

## Experiment Log

```json
[
  {
    "experiment": "SMOTE+Tomek",
    "before_pos": 233,
    "after_pos": 2348,
    "before_total": 8061,
    "after_total": 10176
  },
  {
    "experiment": "XGBoost Standalone",
    "val_f1": 0.9485,
    "val_threshold": 0.498,
    "top_features": [
      "roll_7d_max_data_volume_mb",
      "roll_14d_std_data_volume_mb",
      "expanding_max_systems",
      "roll_14d_std_novelty_score",
      "zscore_role_unique_systems_accessed",
      "roll_7d_std_novelty_score",
      "clearance_normalized",
      "roll_7d_std_data_egress_volume",
      "delta_novelty_score",
      "is_weekend"
    ]
  },
  {
    "experiment": "LightGBM Standalone",
    "val_f1": 0.9583,
    "val_threshold": 0.35
  },
  {
    "experiment": "Meta-Learner (LR)",
    "val_f1": 0.9485,
    "val_threshold": 0.054
  },
  {
    "experiment": "Simple Blend",
    "val_f1": 0.9485,
    "val_threshold": 0.173
  }
]
```
