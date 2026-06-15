# Cross-Validation Results

**Date**: 2026-06-16 03:29
**Features**: 211 enhanced dimensions
**Method**: 5-Fold Stratified CV (shuffle=True, seed=42)
**Dataset**: 11510 samples, 333 positive (2.9%)

---

## LightGBM

| Metric | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | Mean ± Std |
|--------|--------|--------|--------|--------|--------|------------|
| F1 | 0.9688 | 0.9449 | 0.9365 | 0.9206 | 0.9032 | **0.9348 ± 0.0222** |
| AUC | 0.9915 | 0.9877 | 0.9890 | 0.9934 | 0.9917 | **0.9907 ± 0.0020** |
| PRECISION | 1.0000 | 0.9836 | 1.0000 | 0.9831 | 0.9825 | **0.9898 ± 0.0083** |
| RECALL | 0.9394 | 0.9091 | 0.8806 | 0.8657 | 0.8358 | **0.8861 ± 0.0356** |
| FPR | 0.0000 | 0.0004 | 0.0000 | 0.0004 | 0.0004 | **0.0003 ± 0.0002** |

## XGBoost

| Metric | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | Mean ± Std |
|--------|--------|--------|--------|--------|--------|------------|
| F1 | 0.9688 | 0.9449 | 0.9365 | 0.9291 | 0.8960 | **0.9351 ± 0.0236** |
| AUC | 0.9930 | 0.9793 | 0.9894 | 0.9953 | 0.9917 | **0.9897 ± 0.0056** |
| PRECISION | 1.0000 | 0.9836 | 1.0000 | 0.9833 | 0.9655 | **0.9865 ± 0.0128** |
| RECALL | 0.9394 | 0.9091 | 0.8806 | 0.8806 | 0.8358 | **0.8891 ± 0.0344** |
| FPR | 0.0000 | 0.0004 | 0.0000 | 0.0004 | 0.0009 | **0.0004 ± 0.0003** |

---

## Key Takeaways

- **Best model**: XGBoost (F1 = 0.9351 ± 0.0236)
- **AUC-ROC**: 0.9897 — excellent separation
- **LightGBM FPR**: 0.0003 (0.03%) — well below 2% target
- **XGBoost FPR**: 0.0004 (0.04%) — well below 2% target

> **Conclusion**: The enhanced 211-feature pipeline produces stable, high-performance
> results across all folds with low variance, indicating robust generalization.
