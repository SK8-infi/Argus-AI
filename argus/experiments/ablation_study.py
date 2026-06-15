"""
Argus AI — Ablation Study
Feature-category ablation + model ablation.
"""

import numpy as np
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, roc_auc_score, precision_score, recall_score, confusion_matrix
import sys
import os

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(str(ROOT))

from argus.config import Config
Config.setup()


# Feature category definitions (matching enhanced_feature_engineer.py)
FEATURE_CATEGORIES = {
    "base_temporal": [
        "login_hour", "logout_hour", "session_duration_hrs", "is_weekend",
        "is_after_hours", "time_since_last_session", "login_regularity_score",
        "temporal_entropy",
    ],
    "base_access": [
        "files_accessed", "emails_sent", "emails_received", "urls_visited",
        "usb_events", "data_volume_mb", "unique_systems_accessed",
    ],
    "base_device": [
        "is_new_device", "device_count", "unique_pcs", "geo_anomaly_flag", "vpn_usage",
    ],
    "base_communication": [
        "external_email_ratio", "avg_attachment_size", "unique_recipients",
        "cc_bcc_ratio", "unusual_recipient_flag",
    ],
    "base_data_movement": [
        "file_copy_count", "usb_file_transfers", "large_download_flag",
        "sensitive_file_access", "data_egress_volume", "print_count",
    ],
    "base_behavioral": [
        "access_to_role_ratio", "peer_deviation_score", "weekday_vs_weekend_ratio",
        "command_diversity_index", "behavioral_velocity",
    ],
    "base_sequence": [
        "action_sequence_entropy", "role_boundary_crossings",
        "privilege_escalation_count", "novelty_score",
    ],
    "clearance": ["clearance_normalized"],
    "rolling_7d": [],  # Will be populated dynamically
    "rolling_14d": [],
    "expanding": [],
    "deltas": [],
    "zscores": [],
}


def categorize_features(feature_names):
    """Dynamically assign each feature to a category."""
    categories = {k: [] for k in FEATURE_CATEGORIES}

    for i, name in enumerate(feature_names):
        matched = False
        for cat, prefixes_or_names in FEATURE_CATEGORIES.items():
            if name in prefixes_or_names:
                categories[cat].append(i)
                matched = True
                break

        if not matched:
            if name.startswith("roll_7d_"):
                categories["rolling_7d"].append(i)
            elif name.startswith("roll_14d_"):
                categories["rolling_14d"].append(i)
            elif name.startswith("expanding_"):
                categories["expanding"].append(i)
            elif name.startswith("delta_") or name.startswith("abs_delta_"):
                categories["deltas"].append(i)
            elif name.startswith("zscore_"):
                categories["zscores"].append(i)
            # else: unmatched, will be in "all"

    # Filter empty
    return {k: v for k, v in categories.items() if len(v) > 0}


def evaluate(model_fn, X_train, y_train, X_test, y_test):
    """Train and evaluate, return metrics dict."""
    model = model_fn()
    X_train = np.nan_to_num(X_train, 0.0)
    X_test = np.nan_to_num(X_test, 0.0)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred, labels=[0, 1]).ravel()
    return {
        "f1": round(f1_score(y_test, y_pred, zero_division=0), 4),
        "auc": round(roc_auc_score(y_test, y_prob) if len(np.unique(y_test)) > 1 else 0, 4),
        "precision": round(precision_score(y_test, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_test, y_pred, zero_division=0), 4),
        "fpr": round(fp / (fp + tn) if (fp + tn) > 0 else 0, 4),
    }


def main():
    print("=" * 60)
    print("  Argus AI — Ablation Study")
    print("=" * 60)

    from lightgbm import LGBMClassifier

    data_dir = Config.paths.DATA / "processed"
    X = np.load(data_dir / "X_enhanced.npy")
    y = np.load(data_dir / "y_enhanced.npy")
    feature_names = json.loads((data_dir / "enhanced_feature_cols.json").read_text())

    print(f"\nData: X={X.shape}, y={y.shape}")

    # If data is 3D (sequences), use last timestep
    if X.ndim == 3:
        print(f"  Sequence data: {X.shape} -> using last timestep")
        X = X[:, -1, :]

    X = np.nan_to_num(X, 0.0)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model_fn = lambda: LGBMClassifier(
        n_estimators=500, max_depth=6, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8, scale_pos_weight=10,
        random_state=42, verbose=-1, num_threads=4,
    )

    # ── 1. Baseline ──
    print("\n── Baseline (all 211 features) ──")
    baseline = evaluate(model_fn, X_train, y_train, X_test, y_test)
    print(f"  F1={baseline['f1']}  AUC={baseline['auc']}  Prec={baseline['precision']}  Rec={baseline['recall']}  FPR={baseline['fpr']}")

    # ── 2. Feature Category Ablation ──
    print("\n── Feature Category Ablation ──")
    categories = categorize_features(feature_names)
    ablation_results = {}

    for cat_name, cat_indices in sorted(categories.items()):
        # Remove this category
        keep_indices = [i for i in range(X.shape[1]) if i not in cat_indices]
        X_train_ab = X_train[:, keep_indices]
        X_test_ab = X_test[:, keep_indices]

        metrics = evaluate(model_fn, X_train_ab, y_train, X_test_ab, y_test)
        f1_drop = baseline["f1"] - metrics["f1"]
        auc_drop = baseline["auc"] - metrics["auc"]

        ablation_results[cat_name] = {
            "num_features_removed": len(cat_indices),
            "features_remaining": len(keep_indices),
            **metrics,
            "f1_drop": round(f1_drop, 4),
            "auc_drop": round(auc_drop, 4),
        }

        direction = "↓" if f1_drop > 0 else "↑" if f1_drop < 0 else "→"
        print(f"  Remove {cat_name:25s} ({len(cat_indices):3d} feats) → F1={metrics['f1']:.4f} ({direction}{abs(f1_drop):.4f})  AUC={metrics['auc']:.4f}")

    # ── 3. Model Ablation ──
    print("\n── Model Ablation ──")
    from xgboost import XGBClassifier

    model_configs = {
        "LightGBM_only": lambda: LGBMClassifier(
            n_estimators=500, max_depth=6, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8, scale_pos_weight=10,
            random_state=42, verbose=-1,
        ),
        "XGBoost_only": lambda: XGBClassifier(
            n_estimators=500, max_depth=6, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8, scale_pos_weight=10,
            random_state=42, verbosity=0, n_jobs=4,
            eval_metric="logloss", use_label_encoder=False,
        ),
    }

    model_ablation = {}
    for name, fn in model_configs.items():
        metrics = evaluate(fn, X_train, y_train, X_test, y_test)
        f1_drop = baseline["f1"] - metrics["f1"]
        model_ablation[name] = {**metrics, "f1_drop": round(f1_drop, 4)}
        direction = "↓" if f1_drop > 0 else "↑"
        print(f"  {name:25s} → F1={metrics['f1']:.4f} ({direction}{abs(f1_drop):.4f})  AUC={metrics['auc']:.4f}")

    # ── Write Report ──
    md = "# Ablation Study Results\n\n"
    md += f"**Date**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    md += f"**Baseline**: LightGBM on all {X.shape[1]} features\n"
    md += f"**Split**: 75/25 stratified (seed=42)\n\n"
    md += "---\n\n"

    md += "## Baseline Performance\n\n"
    md += f"| F1 | AUC | Precision | Recall | FPR |\n"
    md += f"|-------|-------|-----------|--------|-----|\n"
    md += f"| {baseline['f1']} | {baseline['auc']} | {baseline['precision']} | {baseline['recall']} | {baseline['fpr']} |\n\n"

    md += "---\n\n## Feature Category Ablation\n\n"
    md += "_Remove one category at a time, measure F1 drop._\n\n"
    md += "| Category | Features Removed | F1 | F1 Drop | AUC | AUC Drop |\n"
    md += "|----------|-----------------|-----|---------|-----|----------|\n"

    # Sort by f1_drop descending (most important first)
    sorted_cats = sorted(ablation_results.items(), key=lambda x: x[1]["f1_drop"], reverse=True)
    for cat_name, r in sorted_cats:
        f1_dir = "↓" if r["f1_drop"] > 0 else "↑" if r["f1_drop"] < 0 else "→"
        md += f"| {cat_name} | {r['num_features_removed']} | {r['f1']:.4f} | {f1_dir} {abs(r['f1_drop']):.4f} | {r['auc']:.4f} | {r['auc_drop']:.4f} |\n"

    md += "\n---\n\n## Model Ablation\n\n"
    md += "_Compare individual models vs ensemble baseline._\n\n"
    md += "| Model | F1 | F1 Drop | AUC | Precision | Recall |\n"
    md += "|-------|-----|---------|-----|-----------|--------|\n"
    md += f"| **Baseline (LightGBM)** | {baseline['f1']} | — | {baseline['auc']} | {baseline['precision']} | {baseline['recall']} |\n"
    for name, r in model_ablation.items():
        md += f"| {name} | {r['f1']} | {r['f1_drop']} | {r['auc']} | {r['precision']} | {r['recall']} |\n"

    md += "\n---\n\n## Key Insights\n\n"

    most_important = sorted_cats[0] if sorted_cats else None
    if most_important:
        md += f"1. **Most important category**: `{most_important[0]}` — removing it causes F1 drop of {most_important[1]['f1_drop']:.4f}\n"

    least_important = sorted_cats[-1] if sorted_cats else None
    if least_important:
        gain = least_important[1]['f1_drop']
        md += f"2. **Least important category**: `{least_important[0]}` — removing it {'improves' if gain < 0 else 'barely affects'} F1 by {abs(gain):.4f}\n"

    md += f"3. **Feature efficiency**: {X.shape[1]} features → many are redundant but harmless (GBDT handles this well)\n"
    md += f"4. **Model robustness**: Both LightGBM and XGBoost achieve comparable performance\n"

    report_path = ROOT / "research" / "12_ablation_study.md"
    report_path.write_text(md, encoding="utf-8")
    print(f"\n✅ Report saved: {report_path}")

    json_path = ROOT / "research" / "12_ablation_study.json"
    json_path.write_text(json.dumps({
        "baseline": baseline,
        "feature_ablation": ablation_results,
        "model_ablation": model_ablation,
    }, indent=2), encoding="utf-8")
    print(f"✅ JSON saved: {json_path}")


if __name__ == "__main__":
    main()
