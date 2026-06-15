# 10 — SHAP Explainability Analysis

**Date**: 2026-06-16
**Features**: 211 enhanced dimensions
**Method**: TreeExplainer (exact Shapley values for GBDT)

---

## Global Feature Importance (LightGBM)

| Rank | Feature | Mean |SHAP| |
|------|---------|------------|
| 1 | clearance_normalized | 0.609544 |
| 2 | roll_7d_max_data_volume_mb | 0.532483 |
| 3 | expanding_max_systems | 0.445666 |
| 4 | login_hour | 0.374860 |
| 5 | temporal_entropy | 0.372048 |
| 6 | expanding_max_data_volume | 0.367654 |
| 7 | zscore_dept_data_egress_volume | 0.349594 |
| 8 | roll_14d_std_files_accessed | 0.344336 |
| 9 | zscore_role_data_volume_mb | 0.332352 |
| 10 | roll_14d_sum_files_accessed | 0.321509 |
| 11 | roll_14d_mean_data_volume_mb | 0.264201 |
| 12 | roll_14d_mean_files_accessed | 0.252577 |
| 13 | roll_14d_std_data_volume_mb | 0.229092 |
| 14 | command_diversity_index | 0.220990 |
| 15 | zscore_dept_unique_systems_accessed | 0.217335 |
| 16 | roll_14d_sum_is_after_hours | 0.198782 |
| 17 | roll_14d_max_files_accessed | 0.162898 |
| 18 | is_after_hours | 0.161259 |
| 19 | zscore_role_data_egress_volume | 0.161067 |
| 20 | roll_7d_mean_data_volume_mb | 0.140123 |
| 21 | abs_delta_avg_attachment_size | 0.139693 |
| 22 | time_since_last_session | 0.138503 |
| 23 | roll_7d_std_data_volume_mb | 0.136199 |
| 24 | delta_login_hour | 0.136041 |
| 25 | zscore_dept_data_volume_mb | 0.126136 |
| 26 | roll_14d_sum_data_volume_mb | 0.125298 |
| 27 | velocity_data_egress_volume | 0.124139 |
| 28 | weekday_vs_weekend_ratio | 0.123212 |
| 29 | abs_delta_behavioral_velocity | 0.119491 |
| 30 | zscore_role_session_duration_hrs | 0.115102 |

## Global Feature Importance (XGBoost)

| Rank | Feature | Mean |SHAP| |
|------|---------|------------|
| 1 | clearance_normalized | 0.560317 |
| 2 | login_hour | 0.432248 |
| 3 | temporal_entropy | 0.423010 |
| 4 | roll_14d_std_data_volume_mb | 0.373683 |
| 5 | zscore_dept_data_egress_volume | 0.360723 |
| 6 | zscore_role_data_volume_mb | 0.344442 |
| 7 | roll_14d_sum_files_accessed | 0.333993 |
| 8 | command_diversity_index | 0.322059 |
| 9 | roll_7d_max_data_volume_mb | 0.307828 |
| 10 | expanding_max_data_volume | 0.287894 |
| 11 | roll_14d_sum_is_after_hours | 0.281842 |
| 12 | expanding_max_systems | 0.270929 |
| 13 | roll_14d_mean_data_volume_mb | 0.258534 |
| 14 | action_sequence_entropy | 0.207023 |
| 15 | zscore_dept_unique_systems_accessed | 0.201849 |
| 16 | roll_14d_std_files_accessed | 0.187168 |
| 17 | unique_recipients | 0.186163 |
| 18 | roll_14d_mean_files_accessed | 0.185656 |
| 19 | abs_delta_behavioral_velocity | 0.169877 |
| 20 | zscore_dept_data_volume_mb | 0.165930 |
| 21 | abs_delta_avg_attachment_size | 0.142734 |
| 22 | delta_login_hour | 0.139814 |
| 23 | external_email_ratio | 0.138849 |
| 24 | roll_7d_std_data_volume_mb | 0.135527 |
| 25 | time_since_last_session | 0.134736 |
| 26 | zscore_role_data_egress_volume | 0.130781 |
| 27 | roll_14d_max_files_accessed | 0.128923 |
| 28 | weekday_vs_weekend_ratio | 0.128217 |
| 29 | velocity_data_egress_volume | 0.126696 |
| 30 | session_duration_hrs | 0.108257 |

## Per-Insider Explanations (Top 10)


### Insider 1 — P(insider) = 0.9996

**Risk-increasing factors:**
- ↑ `roll_7d_std_data_volume_mb`: SHAP=+2.8946 (value=11.65)
- ↑ `roll_7d_max_data_volume_mb`: SHAP=+2.7293 (value=33.22)
- ↑ `roll_14d_std_data_volume_mb`: SHAP=+2.0711 (value=8.28)
- ↑ `clearance_normalized`: SHAP=+1.6428 (value=0.60)
- ↑ `expanding_max_data_volume`: SHAP=+1.4553 (value=33.22)

**Risk-decreasing factors:**
- ↓ `expanding_max_systems`: SHAP=-0.4299 (value=4.00)
- ↓ `login_hour`: SHAP=-0.3902 (value=8.58)
- ↓ `temporal_entropy`: SHAP=-0.2209 (value=2.39)

### Insider 2 — P(insider) = 0.9999

**Risk-increasing factors:**
- ↑ `roll_7d_std_data_volume_mb`: SHAP=+3.0520 (value=12.22)
- ↑ `roll_7d_max_data_volume_mb`: SHAP=+2.6577 (value=33.22)
- ↑ `roll_14d_std_data_volume_mb`: SHAP=+2.6095 (value=9.08)
- ↑ `clearance_normalized`: SHAP=+1.7439 (value=0.60)
- ↑ `expanding_max_data_volume`: SHAP=+1.4830 (value=33.22)

**Risk-decreasing factors:**
- ↓ `expanding_max_systems`: SHAP=-0.4897 (value=4.00)
- ↓ `roll_14d_sum_files_accessed`: SHAP=-0.1740 (value=96.00)
- ↓ `delta_login_hour`: SHAP=-0.1480 (value=0.60)

### Insider 3 — P(insider) = 0.9999

**Risk-increasing factors:**
- ↑ `roll_7d_std_data_volume_mb`: SHAP=+2.9036 (value=14.69)
- ↑ `roll_14d_std_data_volume_mb`: SHAP=+2.6149 (value=11.61)
- ↑ `roll_7d_max_data_volume_mb`: SHAP=+2.5439 (value=33.35)
- ↑ `clearance_normalized`: SHAP=+1.7583 (value=0.60)
- ↑ `expanding_max_data_volume`: SHAP=+1.2747 (value=33.35)

**Risk-decreasing factors:**
- ↓ `expanding_max_systems`: SHAP=-0.4214 (value=4.00)
- ↓ `roll_14d_sum_files_accessed`: SHAP=-0.1524 (value=93.00)
- ↓ `delta_data_egress_volume`: SHAP=-0.1182 (value=0.73)

### Insider 4 — P(insider) = 0.9999

**Risk-increasing factors:**
- ↑ `roll_7d_std_data_volume_mb`: SHAP=+2.8332 (value=14.82)
- ↑ `roll_7d_max_data_volume_mb`: SHAP=+2.6402 (value=33.35)
- ↑ `roll_14d_std_data_volume_mb`: SHAP=+2.3951 (value=12.89)
- ↑ `clearance_normalized`: SHAP=+1.6858 (value=0.60)
- ↑ `expanding_max_data_volume`: SHAP=+1.3711 (value=33.35)

**Risk-decreasing factors:**
- ↓ `expanding_max_systems`: SHAP=-0.4572 (value=4.00)
- ↓ `roll_14d_sum_files_accessed`: SHAP=-0.1600 (value=97.00)
- ↓ `login_regularity_score`: SHAP=-0.1241 (value=0.00)

### Insider 5 — P(insider) = 1.0000

**Risk-increasing factors:**
- ↑ `roll_7d_max_data_volume_mb`: SHAP=+2.7431 (value=36.45)
- ↑ `roll_7d_std_data_volume_mb`: SHAP=+2.2654 (value=14.74)
- ↑ `roll_14d_std_data_volume_mb`: SHAP=+2.1281 (value=14.50)
- ↑ `expanding_max_data_volume`: SHAP=+1.1689 (value=36.45)
- ↑ `roll_7d_mean_data_volume_mb`: SHAP=+1.0661 (value=22.34)

**Risk-decreasing factors:**
- ↓ `zscore_dept_unique_systems_accessed`: SHAP=-0.1450 (value=1.18)
- ↓ `delta_login_hour`: SHAP=-0.1342 (value=0.63)
- ↓ `roll_14d_sum_files_accessed`: SHAP=-0.1302 (value=102.00)

### Insider 6 — P(insider) = 1.0000

**Risk-increasing factors:**
- ↑ `roll_7d_max_data_volume_mb`: SHAP=+2.8201 (value=36.45)
- ↑ `roll_7d_std_data_volume_mb`: SHAP=+2.1735 (value=11.91)
- ↑ `roll_14d_std_data_volume_mb`: SHAP=+2.0630 (value=14.60)
- ↑ `expanding_max_data_volume`: SHAP=+1.3179 (value=36.45)
- ↑ `roll_7d_mean_data_volume_mb`: SHAP=+1.2413 (value=25.65)

**Risk-decreasing factors:**
- ↓ `zscore_dept_unique_systems_accessed`: SHAP=-0.1906 (value=1.12)
- ↓ `temporal_entropy`: SHAP=-0.1806 (value=2.41)
- ↓ `roll_14d_sum_files_accessed`: SHAP=-0.1483 (value=104.00)

### Insider 7 — P(insider) = 1.0000

**Risk-increasing factors:**
- ↑ `roll_7d_max_data_volume_mb`: SHAP=+2.6627 (value=36.45)
- ↑ `roll_7d_std_data_volume_mb`: SHAP=+2.1907 (value=6.31)
- ↑ `roll_14d_std_data_volume_mb`: SHAP=+2.0834 (value=14.32)
- ↑ `roll_7d_mean_data_volume_mb`: SHAP=+1.2164 (value=28.68)
- ↑ `expanding_max_data_volume`: SHAP=+1.1836 (value=36.45)

**Risk-decreasing factors:**
- ↓ `login_hour`: SHAP=-0.2823 (value=8.73)
- ↓ `zscore_dept_unique_systems_accessed`: SHAP=-0.1909 (value=1.15)
- ↓ `roll_14d_sum_files_accessed`: SHAP=-0.1450 (value=106.00)

### Insider 8 — P(insider) = 1.0000

**Risk-increasing factors:**
- ↑ `roll_7d_max_data_volume_mb`: SHAP=+3.1919 (value=36.45)
- ↑ `roll_14d_std_data_volume_mb`: SHAP=+2.4459 (value=14.22)
- ↑ `roll_7d_std_data_volume_mb`: SHAP=+2.1370 (value=11.04)
- ↑ `roll_7d_mean_data_volume_mb`: SHAP=+1.5326 (value=24.42)
- ↑ `expanding_max_data_volume`: SHAP=+1.2966 (value=36.45)

**Risk-decreasing factors:**
- ↓ `roll_14d_sum_files_accessed`: SHAP=-0.1258 (value=99.00)
- ↓ `roll_14d_mean_data_egress_volume`: SHAP=-0.1023 (value=1.49)
- ↓ `delta_login_hour`: SHAP=-0.0959 (value=12.85)

### Insider 9 — P(insider) = 1.0000

**Risk-increasing factors:**
- ↑ `roll_7d_max_data_volume_mb`: SHAP=+3.2165 (value=36.45)
- ↑ `roll_14d_std_data_volume_mb`: SHAP=+2.5716 (value=14.19)
- ↑ `roll_7d_std_data_volume_mb`: SHAP=+2.2621 (value=13.76)
- ↑ `roll_7d_mean_data_volume_mb`: SHAP=+1.5109 (value=22.12)
- ↑ `expanding_max_data_volume`: SHAP=+1.3361 (value=36.45)

**Risk-decreasing factors:**
- ↓ `roll_14d_sum_files_accessed`: SHAP=-0.1361 (value=94.00)
- ↓ `abs_delta_files_accessed`: SHAP=-0.1169 (value=0.00)
- ↓ `roll_14d_mean_data_egress_volume`: SHAP=-0.1046 (value=1.54)

### Insider 10 — P(insider) = 1.0000

**Risk-increasing factors:**
- ↑ `roll_7d_max_data_volume_mb`: SHAP=+2.7814 (value=42.26)
- ↑ `roll_7d_std_data_volume_mb`: SHAP=+2.1539 (value=15.30)
- ↑ `roll_14d_std_data_volume_mb`: SHAP=+2.0867 (value=15.28)
- ↑ `expanding_max_data_volume`: SHAP=+1.1767 (value=42.26)
- ↑ `roll_7d_mean_data_volume_mb`: SHAP=+1.0901 (value=23.39)

**Risk-decreasing factors:**
- ↓ `roll_14d_sum_files_accessed`: SHAP=-0.1512 (value=88.00)
- ↓ `delta_data_egress_volume`: SHAP=-0.1331 (value=11.88)
- ↓ `zscore_dept_unique_systems_accessed`: SHAP=-0.1197 (value=2.15)