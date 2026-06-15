# Ablation Study Results

**Date**: 2026-06-16 03:23
**Baseline**: LightGBM on all 211 features
**Split**: 75/25 stratified (seed=42)

---

## Baseline Performance

| F1 | AUC | Precision | Recall | FPR |
|-------|-------|-----------|--------|-----|
| 0.9221 | 0.9882 | 1.0 | 0.8554 | 0.0 |

---

## Feature Category Ablation

_Remove one category at a time, measure F1 drop._

| Category | Features Removed | F1 | F1 Drop | AUC | AUC Drop |
|----------|-----------------|-----|---------|-----|----------|
| rolling_14d | 48 | 0.9007 | ↓ 0.0214 | 0.9746 | 0.0136 |
| base_communication | 4 | 0.9150 | ↓ 0.0071 | 0.9834 | 0.0048 |
| clearance | 1 | 0.9150 | ↓ 0.0071 | 0.9874 | 0.0008 |
| expanding | 2 | 0.9150 | ↓ 0.0071 | 0.9865 | 0.0017 |
| zscores | 16 | 0.9150 | ↓ 0.0071 | 0.9875 | 0.0007 |
| base_device | 3 | 0.9161 | ↓ 0.0060 | 0.9870 | 0.0012 |
| base_access | 7 | 0.9221 | → 0.0000 | 0.9884 | -0.0002 |
| base_data_movement | 5 | 0.9221 | → 0.0000 | 0.9844 | 0.0038 |
| base_sequence | 4 | 0.9221 | → 0.0000 | 0.9820 | 0.0062 |
| base_behavioral | 5 | 0.9290 | ↑ 0.0069 | 0.9827 | 0.0055 |
| base_temporal | 8 | 0.9290 | ↑ 0.0069 | 0.9862 | 0.0020 |
| deltas | 24 | 0.9290 | ↑ 0.0069 | 0.9873 | 0.0009 |
| rolling_7d | 48 | 0.9427 | ↑ 0.0206 | 0.9880 | 0.0002 |

---

## Model Ablation

_Compare individual models vs ensemble baseline._

| Model | F1 | F1 Drop | AUC | Precision | Recall |
|-------|-----|---------|-----|-----------|--------|
| **Baseline (LightGBM)** | 0.9221 | — | 0.9882 | 1.0 | 0.8554 |
| LightGBM_only | 0.9221 | 0.0 | 0.9882 | 1.0 | 0.8554 |
| XGBoost_only | 0.9161 | 0.006 | 0.9871 | 0.9861 | 0.8554 |

---

## Key Insights

1. **Most important category**: `rolling_14d` — removing it causes F1 drop of 0.0214
2. **Least important category**: `rolling_7d` — removing it improves F1 by 0.0206
3. **Feature efficiency**: 211 features → many are redundant but harmless (GBDT handles this well)
4. **Model robustness**: Both LightGBM and XGBoost achieve comparable performance
