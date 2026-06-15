"""
Argus AI — Enhanced Feature Engineering Pipeline (Phase 2)
============================================================
Expands from 47 → 120+ features by adding:
  - Temporal deltas (day-over-day changes)
  - Rolling window statistics (7d, 14d)
  - Velocity & acceleration features
  - Feature interactions
  - Enhanced peer z-scores
  - Cumulative risk indicators

Based on research from BOI Hackathon (delta/change features were the
strongest predictors, along with interaction features).

Usage:
    python -m argus.data.enhanced_feature_engineer
"""

import sys
import argparse
from pathlib import Path
from collections import Counter

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats
from loguru import logger
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from argus.config import Config

# ═══════════════════════════════════════════════════════════════
#  ORIGINAL 47 FEATURES
# ═══════════════════════════════════════════════════════════════

ORIGINAL_FEATURE_COLS = [
    "login_hour", "logout_hour", "session_duration_hrs", "is_weekend",
    "is_after_hours", "time_since_last_session", "login_regularity_score",
    "temporal_entropy",
    "files_accessed", "emails_sent", "emails_received", "urls_visited",
    "usb_events", "data_volume_mb", "unique_systems_accessed",
    "is_new_device", "device_count", "unique_pcs", "geo_anomaly_flag",
    "vpn_usage",
    "external_email_ratio", "avg_attachment_size", "unique_recipients",
    "cc_bcc_ratio", "email_content_sentiment", "unusual_recipient_flag",
    "file_copy_count", "usb_file_transfers", "large_download_flag",
    "sensitive_file_access", "data_egress_volume", "print_count",
    "cloud_upload_count",
    "access_to_role_ratio", "peer_deviation_score", "weekday_vs_weekend_ratio",
    "morning_vs_evening_ratio", "productive_vs_idle_ratio",
    "command_diversity_index",
    "action_sequence_entropy", "longest_unusual_chain",
    "role_boundary_crossings", "privilege_escalation_count",
    "session_action_diversity", "repeat_pattern_score",
    "novelty_score", "behavioral_velocity",
]

# Features to DROP (dead/redundant from investigation)
DROP_FEATURES = [
    "cc_bcc_ratio",           # constant zero
    "email_content_sentiment", # constant zero
    "usb_file_transfers",      # constant zero
    "unique_pcs",              # identical to device_count (r=1.0)
    "vpn_usage",               # identical to geo_anomaly_flag (r=1.0)
    "repeat_pattern_score",    # inverse of command_diversity_index (r=-1.0)
    "productive_vs_idle_ratio", # near-identical to behavioral_velocity (r=0.999)
]

# Key features for temporal delta computation
DELTA_FEATURES = [
    "data_volume_mb", "files_accessed", "unique_systems_accessed",
    "sensitive_file_access", "login_hour", "session_duration_hrs",
    "behavioral_velocity", "data_egress_volume", "novelty_score",
    "role_boundary_crossings", "access_to_role_ratio", "avg_attachment_size",
]

# Key features for rolling window statistics
ROLLING_FEATURES = [
    "data_volume_mb", "files_accessed", "sensitive_file_access",
    "usb_events", "is_after_hours", "data_egress_volume",
    "novelty_score", "role_boundary_crossings", "is_new_device",
    "access_to_role_ratio", "device_count", "large_download_flag",
]

# Interaction pairs (from investigation: best interactions)
INTERACTION_PAIRS = [
    ("access_to_role_ratio", "unique_systems_accessed"),  # +20.5% improvement
    ("role_boundary_crossings", "data_egress_volume"),     # high signal
    ("behavioral_velocity", "novelty_score"),
    ("is_after_hours", "sensitive_file_access"),
    ("usb_events", "data_volume_mb"),
    ("is_new_device", "data_volume_mb"),
    ("is_new_device", "role_boundary_crossings"),
    ("data_volume_mb", "login_regularity_score"),
    ("files_accessed", "is_after_hours"),
    ("external_email_ratio", "data_volume_mb"),
    ("sensitive_file_access", "is_after_hours"),
    ("novelty_score", "is_after_hours"),
    ("data_volume_mb", "is_weekend"),
]

# Peer z-score features
PEER_FEATURES = [
    "data_volume_mb", "files_accessed", "unique_systems_accessed",
    "login_hour", "session_duration_hrs", "data_egress_volume",
    "sensitive_file_access", "novelty_score",
]


def enhance_features(
    input_csv: str | Path | None = None,
    employees_csv: str | Path | None = None,
    ground_truth_csv: str | Path | None = None,
    output_dir: str | Path | None = None,
    sequence_length: int = 7,
) -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """
    Load the original 47-feature dataset and enhance it to 120+ features.
    
    Returns:
        (enhanced_df, X_sequences, y_labels)
    """
    data_dir = Config.paths.SYNTHETIC_DATA
    proc_dir = Config.paths.PROCESSED_DATA
    out_dir = Path(output_dir) if output_dir else proc_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    input_csv = input_csv or proc_dir / "features_47d.csv"
    employees_csv = employees_csv or data_dir / "employees.csv"
    ground_truth_csv = ground_truth_csv or data_dir / "ground_truth.csv"

    logger.info("Loading original features...")
    df = pd.read_csv(input_csv)
    employees = pd.read_csv(employees_csv)
    ground_truth = pd.read_csv(ground_truth_csv)

    # Merge employee metadata
    df = df.merge(
        employees[["emp_id", "department", "role", "clearance_level"]],
        on="emp_id", how="left"
    )

    original_cols = len([c for c in ORIGINAL_FEATURE_COLS if c in df.columns])
    logger.info(f"  Original features: {original_cols}")
    logger.info(f"  Samples: {len(df):,}")
    logger.info(f"  Positive rate: {df['label'].mean()*100:.2f}%")

    # ═══════════════════════════════════════════════════════════
    #  STEP 1: DROP DEAD FEATURES
    # ═══════════════════════════════════════════════════════════
    logger.info("Step 1/7: Dropping dead/redundant features...")
    for feat in DROP_FEATURES:
        if feat in df.columns:
            df = df.drop(columns=[feat])
    logger.info(f"  Dropped {len(DROP_FEATURES)} features → {len([c for c in ORIGINAL_FEATURE_COLS if c in df.columns])} remaining")

    # ═══════════════════════════════════════════════════════════
    #  STEP 2: TEMPORAL DELTAS (day-over-day changes)
    # ═══════════════════════════════════════════════════════════
    logger.info("Step 2/7: Computing temporal deltas...")
    df = df.sort_values(["emp_id", "day_index"])

    delta_count = 0
    for feat in DELTA_FEATURES:
        if feat not in df.columns:
            continue
        col_name = f"delta_{feat}"
        df[col_name] = df.groupby("emp_id")[feat].diff().fillna(0)
        delta_count += 1

        # Also compute absolute delta (magnitude of change)
        abs_col = f"abs_delta_{feat}"
        df[abs_col] = df[col_name].abs()
        delta_count += 1

    logger.info(f"  Added {delta_count} temporal delta features")

    # ═══════════════════════════════════════════════════════════
    #  STEP 3: ROLLING WINDOW STATISTICS (7d and 14d)
    # ═══════════════════════════════════════════════════════════
    logger.info("Step 3/7: Computing rolling window statistics...")
    rolling_count = 0
    for feat in ROLLING_FEATURES:
        if feat not in df.columns:
            continue

        for window in [7, 14]:
            # Rolling mean
            col_mean = f"roll_{window}d_mean_{feat}"
            df[col_mean] = df.groupby("emp_id")[feat].transform(
                lambda x: x.rolling(window, min_periods=1).mean()
            )
            rolling_count += 1

            # Rolling std (volatility)
            col_std = f"roll_{window}d_std_{feat}"
            df[col_std] = df.groupby("emp_id")[feat].transform(
                lambda x: x.rolling(window, min_periods=2).std()
            ).fillna(0)
            rolling_count += 1

            # Rolling max (peak detection)
            col_max = f"roll_{window}d_max_{feat}"
            df[col_max] = df.groupby("emp_id")[feat].transform(
                lambda x: x.rolling(window, min_periods=1).max()
            )
            rolling_count += 1

            # Rolling sum (cumulative activity)
            col_sum = f"roll_{window}d_sum_{feat}"
            df[col_sum] = df.groupby("emp_id")[feat].transform(
                lambda x: x.rolling(window, min_periods=1).sum()
            )
            rolling_count += 1

    logger.info(f"  Added {rolling_count} rolling window features")

    # ═══════════════════════════════════════════════════════════
    #  STEP 4: VELOCITY & ACCELERATION
    # ═══════════════════════════════════════════════════════════
    logger.info("Step 4/7: Computing velocity & acceleration features...")
    velocity_count = 0

    # Velocity = slope of 7-day rolling mean
    for feat in ["data_volume_mb", "files_accessed", "sensitive_file_access",
                 "data_egress_volume", "unique_systems_accessed"]:
        if feat not in df.columns:
            continue
        delta_col = f"delta_{feat}"
        if delta_col in df.columns:
            # Velocity: smoothed delta (7d rolling mean of deltas)
            vel_col = f"velocity_{feat}"
            df[vel_col] = df.groupby("emp_id")[delta_col].transform(
                lambda x: x.rolling(7, min_periods=1).mean()
            )
            velocity_count += 1

            # Acceleration: change in velocity (delta of delta)
            acc_col = f"accel_{feat}"
            df[acc_col] = df.groupby("emp_id")[vel_col].diff().fillna(0)
            velocity_count += 1

    logger.info(f"  Added {velocity_count} velocity/acceleration features")

    # ═══════════════════════════════════════════════════════════
    #  STEP 5: FEATURE INTERACTIONS
    # ═══════════════════════════════════════════════════════════
    logger.info("Step 5/7: Computing feature interactions...")
    interaction_count = 0
    for fa, fb in INTERACTION_PAIRS:
        if fa not in df.columns or fb not in df.columns:
            continue
        col_name = f"interact_{fa}_x_{fb}"
        df[col_name] = df[fa] * df[fb]
        interaction_count += 1

    logger.info(f"  Added {interaction_count} interaction features")

    # ═══════════════════════════════════════════════════════════
    #  STEP 6: ENHANCED PEER Z-SCORES
    # ═══════════════════════════════════════════════════════════
    logger.info("Step 6/7: Computing enhanced peer z-scores...")
    zscore_count = 0

    for feat in PEER_FEATURES:
        if feat not in df.columns:
            continue

        # Department-level z-score
        dept_mean = df.groupby(["department", "day_index"])[feat].transform("mean")
        dept_std = df.groupby(["department", "day_index"])[feat].transform("std").replace(0, 1).fillna(1)
        z_col = f"zscore_dept_{feat}"
        df[z_col] = ((df[feat] - dept_mean) / dept_std).fillna(0)
        zscore_count += 1

        # Role-level z-score (more granular)
        role_mean = df.groupby(["role", "day_index"])[feat].transform("mean")
        role_std = df.groupby(["role", "day_index"])[feat].transform("std").replace(0, 1).fillna(1)
        zr_col = f"zscore_role_{feat}"
        df[zr_col] = ((df[feat] - role_mean) / role_std).fillna(0)
        zscore_count += 1

    # Max z-score across all department z-score features (worst deviation)
    dept_z_cols = [c for c in df.columns if c.startswith("zscore_dept_")]
    if dept_z_cols:
        df["max_dept_zscore"] = df[dept_z_cols].abs().max(axis=1)
        df["mean_dept_zscore"] = df[dept_z_cols].abs().mean(axis=1)
        zscore_count += 2

    logger.info(f"  Added {zscore_count} z-score features")

    # ═══════════════════════════════════════════════════════════
    #  STEP 7: CUMULATIVE RISK INDICATORS
    # ═══════════════════════════════════════════════════════════
    logger.info("Step 7/7: Computing cumulative risk indicators...")
    cumulative_count = 0

    # Days since last anomaly (any non-zero novelty_score)
    if "novelty_score" in df.columns:
        df["is_anomalous_day"] = (df["novelty_score"] > 0).astype(int)
        df["anomaly_streak"] = df.groupby("emp_id")["is_anomalous_day"].transform(
            lambda x: x.rolling(7, min_periods=1).sum()
        )
        cumulative_count += 2

    # Expanding window: unique systems ever accessed (cumulative)
    if "unique_systems_accessed" in df.columns:
        df["expanding_max_systems"] = df.groupby("emp_id")["unique_systems_accessed"].transform(
            lambda x: x.expanding(min_periods=1).max()
        )
        cumulative_count += 1

    # Expanding window: max data volume ever (detects escalation)
    if "data_volume_mb" in df.columns:
        df["expanding_max_data_volume"] = df.groupby("emp_id")["data_volume_mb"].transform(
            lambda x: x.expanding(min_periods=1).max()
        )
        # Ratio of current day to personal max (how extreme is today?)
        df["data_volume_vs_personal_max"] = (
            df["data_volume_mb"] / df["expanding_max_data_volume"].replace(0, 1)
        )
        cumulative_count += 2

    # Cumulative 7d sum of binary flags
    for flag_feat in ["usb_events", "is_new_device", "large_download_flag",
                       "is_after_hours", "geo_anomaly_flag"]:
        if flag_feat in df.columns:
            cum_col = f"cum_7d_{flag_feat}"
            df[cum_col] = df.groupby("emp_id")[flag_feat].transform(
                lambda x: x.rolling(7, min_periods=1).sum()
            )
            cumulative_count += 1

    # Clearance level (numeric — already exists in metadata)
    if "clearance_level" in df.columns:
        df["clearance_normalized"] = df["clearance_level"] / 5.0
        cumulative_count += 1

    logger.info(f"  Added {cumulative_count} cumulative risk features")

    # ═══════════════════════════════════════════════════════════
    #  FINAL: Build feature column list & sequences
    # ═══════════════════════════════════════════════════════════
    # Drop metadata columns
    meta_cols = ["emp_id", "day_index", "date", "label", "department", "role",
                 "clearance_level", "branch", "scenario", "attack_start_day",
                 "attack_end_day", "is_anomalous_day"]
    feature_cols = [c for c in df.columns if c not in meta_cols]

    # Clean NaN/inf
    for col in feature_cols:
        df[col] = df[col].replace([np.inf, -np.inf], 0).fillna(0)

    total_features = len(feature_cols)
    logger.info(f"\n  📊 FEATURE SUMMARY:")
    logger.info(f"  Original features: {original_cols}")
    logger.info(f"  After dropping dead: {original_cols - len(DROP_FEATURES)}")
    logger.info(f"  After enhancements: {total_features}")
    logger.info(f"  New features added: {total_features - (original_cols - len(DROP_FEATURES))}")

    # Save enhanced features
    enhanced_path = out_dir / "features_enhanced.csv"
    df.to_csv(enhanced_path, index=False)
    logger.info(f"  Saved enhanced features to: {enhanced_path}")

    # Save feature column list
    feature_list_path = out_dir / "enhanced_feature_cols.json"
    import json
    with open(feature_list_path, "w") as f:
        json.dump(feature_cols, f, indent=2)

    # Build sequences for LSTM
    logger.info(f"Building {sequence_length}-day sequences...")
    X_sequences, y_labels, seq_meta = _build_sequences(df, feature_cols, sequence_length)

    np.save(out_dir / "X_enhanced.npy", X_sequences)
    np.save(out_dir / "y_enhanced.npy", y_labels)
    pd.DataFrame(seq_meta).to_csv(out_dir / "seq_meta_enhanced.csv", index=False)

    n_pos = int(y_labels.sum())
    n_total = len(y_labels)
    logger.success(f"✅ Enhanced feature engineering complete!")
    logger.info(f"   Feature vectors: {len(df):,} × {total_features} features")
    logger.info(f"   LSTM sequences: {X_sequences.shape}")
    logger.info(f"   Labels: {n_pos} positive / {n_total - n_pos} negative ({n_pos/max(1,n_total)*100:.2f}%)")

    return df, X_sequences, y_labels


def _build_sequences(
    features_df: pd.DataFrame,
    feature_cols: list[str],
    seq_len: int,
) -> tuple[np.ndarray, np.ndarray, list[dict]]:
    """Build sliding-window sequences for LSTM input."""
    sequences = []
    labels = []
    meta = []

    for emp_id, emp_data in features_df.groupby("emp_id"):
        emp_data = emp_data.sort_values("day_index")
        values = emp_data[feature_cols].values.astype(np.float32)
        day_labels = emp_data["label"].values

        values = np.nan_to_num(values, nan=0.0, posinf=0.0, neginf=0.0)

        if len(values) < seq_len:
            continue

        for i in range(len(values) - seq_len + 1):
            seq = values[i:i + seq_len]
            lbl = int(day_labels[i:i + seq_len].max())
            sequences.append(seq)
            labels.append(lbl)
            meta.append({
                "emp_id": emp_id,
                "start_day": int(emp_data.iloc[i]["day_index"]),
                "end_day": int(emp_data.iloc[i + seq_len - 1]["day_index"]),
                "label": lbl,
            })

    X = np.array(sequences, dtype=np.float32)
    y = np.array(labels, dtype=np.int32)

    return X, y, meta


def main():
    parser = argparse.ArgumentParser(description="Argus AI — Enhanced Feature Engineering")
    parser.add_argument("--sequence-length", type=int, default=7)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    Config.setup()
    enhance_features(
        sequence_length=args.sequence_length,
        output_dir=args.output,
    )


if __name__ == "__main__":
    main()
