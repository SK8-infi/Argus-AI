"""
Argus AI — Enhanced Training Pipeline (Phases 3-6)
=====================================================
Combines:
  Phase 3: Synthetic augmentation (SMOTE + Tomek, conditional)
  Phase 4: Supervised models (XGBoost, LightGBM)
  Phase 5: Ensemble stacking
  Phase 6: Final evaluation

Based on BOI Hackathon methodology:
  - XGBoost Blend achieved F1=0.743 from initial F1~0.30
  - Key: class weight tuning, feature selection, threshold optimization

Usage:
    python -m argus.train_enhanced
"""

import sys
import json
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import (
    f1_score, precision_score, recall_score, roc_auc_score,
    confusion_matrix, classification_report, average_precision_score,
    precision_recall_curve,
)
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent.parent))
from argus.config import Config


def main():
    parser = argparse.ArgumentParser(description="Argus AI — Enhanced Training Pipeline")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--smote", action="store_true", default=True)
    parser.add_argument("--no-smote", dest="smote", action="store_false")
    args = parser.parse_args()

    Config.setup()
    np.random.seed(args.seed)

    proc_dir = Config.paths.PROCESSED_DATA
    models_dir = Config.paths.MODELS
    results_dir = Config.paths.RESULTS
    research_dir = Path(Config.paths.ROOT) / "research"
    models_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)
    research_dir.mkdir(parents=True, exist_ok=True)

    experiment_log = []

    # ═══════════════════════════════════════════════════════════
    #  STEP 1: Load enhanced features
    # ═══════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("STEP 1: Loading enhanced features (211 dimensions)...")
    logger.info("=" * 60)

    X_sequences = np.load(proc_dir / "X_enhanced.npy")
    y_labels = np.load(proc_dir / "y_enhanced.npy")
    feature_cols = json.load(open(proc_dir / "enhanced_feature_cols.json"))

    logger.info(f"  Sequences: {X_sequences.shape}")
    logger.info(f"  Features: {len(feature_cols)}")
    logger.info(f"  Positive: {y_labels.sum()} / {len(y_labels)} ({y_labels.mean()*100:.2f}%)")

    # Static features = last timestep of each sequence
    X_static = X_sequences[:, -1, :]  # (n_samples, 211)

    # ═══════════════════════════════════════════════════════════
    #  STEP 2: Train/Val/Test split (stratified)
    # ═══════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("STEP 2: Stratified split...")
    logger.info("=" * 60)

    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X_static, y_labels, test_size=0.15, random_state=args.seed, stratify=y_labels
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_trainval, y_trainval, test_size=0.176, random_state=args.seed, stratify=y_trainval
    )

    # Also split sequences for LSTM
    Xseq_trainval, Xseq_test, _, _ = train_test_split(
        X_sequences, y_labels, test_size=0.15, random_state=args.seed, stratify=y_labels
    )
    Xseq_train, Xseq_val, _, _ = train_test_split(
        Xseq_trainval, y_trainval, test_size=0.176, random_state=args.seed, stratify=y_trainval
    )

    logger.info(f"  Train: {X_train.shape[0]} ({y_train.sum()} pos)")
    logger.info(f"  Val:   {X_val.shape[0]} ({y_val.sum()} pos)")
    logger.info(f"  Test:  {X_test.shape[0]} ({y_test.sum()} pos)")

    imbalance_ratio = (y_train == 0).sum() / max(1, (y_train == 1).sum())
    logger.info(f"  Imbalance ratio: {imbalance_ratio:.1f}:1")

    # ═══════════════════════════════════════════════════════════
    #  STEP 3: SMOTE + Tomek (augment training set)
    # ═══════════════════════════════════════════════════════════
    if args.smote:
        logger.info("=" * 60)
        logger.info("STEP 3: Applying SMOTE + Tomek Links...")
        logger.info("=" * 60)

        from imblearn.combine import SMOTETomek
        from imblearn.over_sampling import SMOTE

        smote_tomek = SMOTETomek(
            smote=SMOTE(sampling_strategy=0.3, random_state=args.seed, k_neighbors=5),
            random_state=args.seed,
        )
        X_train_aug, y_train_aug = smote_tomek.fit_resample(X_train, y_train)
        logger.info(f"  Before SMOTE: {X_train.shape[0]} ({y_train.sum()} pos)")
        logger.info(f"  After SMOTE:  {X_train_aug.shape[0]} ({y_train_aug.sum()} pos)")
        logger.info(f"  New imbalance: {(y_train_aug==0).sum()/max(1,(y_train_aug==1).sum()):.1f}:1")

        experiment_log.append({
            "experiment": "SMOTE+Tomek",
            "before_pos": int(y_train.sum()),
            "after_pos": int(y_train_aug.sum()),
            "before_total": len(y_train),
            "after_total": len(y_train_aug),
        })
    else:
        X_train_aug, y_train_aug = X_train, y_train

    # ═══════════════════════════════════════════════════════════
    #  STEP 4a: Train LSTM Autoencoder (unsupervised)
    # ═══════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("STEP 4a: Training LSTM Autoencoder...")
    logger.info("=" * 60)

    from argus.models.lstm_autoencoder import (
        LSTMAutoencoder, train_autoencoder,
        compute_anomaly_scores, extract_twin_embeddings,
    )

    Xseq_train_normal = Xseq_train[y_train == 0]
    Xseq_val_normal = Xseq_val[y_val == 0]

    lstm_model, lstm_history = train_autoencoder(
        X_train=Xseq_train_normal,
        X_val=Xseq_val_normal,
        epochs=args.epochs,
        batch_size=32,
        lr=1e-3,
        patience=10,
        model_save_path=models_dir / "lstm_autoencoder_enhanced.pt",
        device=Config.model.DEVICE,
    )

    import torch
    ckpt = torch.load(models_dir / "lstm_autoencoder_enhanced.pt", weights_only=False)
    lstm_mean, lstm_std = ckpt["mean"], ckpt["std"]

    lstm_scores_train = compute_anomaly_scores(lstm_model, Xseq_train, lstm_mean, lstm_std, Config.model.DEVICE)
    lstm_scores_val = compute_anomaly_scores(lstm_model, Xseq_val, lstm_mean, lstm_std, Config.model.DEVICE)
    lstm_scores_test = compute_anomaly_scores(lstm_model, Xseq_test, lstm_mean, lstm_std, Config.model.DEVICE)

    logger.info(f"  LSTM — Normal mean: {lstm_scores_train[y_train==0].mean():.4f}, Insider: {lstm_scores_train[y_train==1].mean():.4f}")
    gap = lstm_scores_train[y_train==1].mean() / max(1e-8, lstm_scores_train[y_train==0].mean())
    logger.info(f"  Reconstruction error gap: {gap:.1f}x")

    # ═══════════════════════════════════════════════════════════
    #  STEP 4b: Train Isolation Forest (unsupervised)
    # ═══════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("STEP 4b: Training Isolation Forest...")
    logger.info("=" * 60)

    from argus.models.isolation_forest import train_isolation_forest, compute_if_scores

    if_model, if_scaler, if_info = train_isolation_forest(
        X_train=X_train[y_train == 0],
        feature_names=feature_cols,
        n_estimators=500,
        contamination=0.05,
        seed=args.seed,
        model_save_path=models_dir / "isolation_forest_enhanced.joblib",
    )

    if_scores_train = compute_if_scores(if_model, if_scaler, X_train)
    if_scores_val = compute_if_scores(if_model, if_scaler, X_val)
    if_scores_test = compute_if_scores(if_model, if_scaler, X_test)

    # ═══════════════════════════════════════════════════════════
    #  STEP 4c: Train XGBoost (supervised)
    # ═══════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("STEP 4c: Training XGBoost Classifier...")
    logger.info("=" * 60)

    import xgboost as xgb

    # Scale for XGBoost
    scaler_xgb = StandardScaler()
    X_train_scaled = scaler_xgb.fit_transform(X_train_aug)
    X_val_scaled = scaler_xgb.transform(X_val)
    X_test_scaled = scaler_xgb.transform(X_test)

    # XGBoost with class weight
    spw = (y_train_aug == 0).sum() / max(1, (y_train_aug == 1).sum())
    xgb_model = xgb.XGBClassifier(
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
        scale_pos_weight=spw,
        min_child_weight=3,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        eval_metric="logloss",
        random_state=args.seed,
        use_label_encoder=False,
        verbosity=0,
    )
    xgb_model.fit(
        X_train_scaled, y_train_aug,
        eval_set=[(X_val_scaled, y_val)],
        verbose=False,
    )

    xgb_probs_train = xgb_model.predict_proba(scaler_xgb.transform(X_train))[:, 1]
    xgb_probs_val = xgb_model.predict_proba(X_val_scaled)[:, 1]
    xgb_probs_test = xgb_model.predict_proba(X_test_scaled)[:, 1]

    # XGBoost standalone performance
    xgb_val_f1 = _best_f1_threshold(y_val, xgb_probs_val)
    logger.info(f"  XGBoost Val F1: {xgb_val_f1['f1']:.4f} (threshold={xgb_val_f1['threshold']:.3f})")

    # Feature importance
    importance = xgb_model.feature_importances_
    top_features = sorted(zip(feature_cols, importance), key=lambda x: x[1], reverse=True)[:20]
    logger.info(f"  Top 5 features: {[f[0] for f in top_features[:5]]}")

    joblib.dump(xgb_model, models_dir / "xgboost_enhanced.joblib")
    joblib.dump(scaler_xgb, models_dir / "scaler_xgb.joblib")

    experiment_log.append({
        "experiment": "XGBoost Standalone",
        "val_f1": round(xgb_val_f1["f1"], 4),
        "val_threshold": round(xgb_val_f1["threshold"], 3),
        "top_features": [f[0] for f in top_features[:10]],
    })

    # ═══════════════════════════════════════════════════════════
    #  STEP 4d: Train LightGBM (supervised)
    # ═══════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("STEP 4d: Training LightGBM Classifier...")
    logger.info("=" * 60)

    import lightgbm as lgb

    lgb_model = lgb.LGBMClassifier(
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
        is_unbalance=True,
        num_leaves=31,
        min_child_samples=5,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=args.seed,
        verbose=-1,
    )
    lgb_model.fit(
        X_train_aug, y_train_aug,
        eval_set=[(X_val, y_val)],
    )

    lgb_probs_train = lgb_model.predict_proba(X_train)[:, 1]
    lgb_probs_val = lgb_model.predict_proba(X_val)[:, 1]
    lgb_probs_test = lgb_model.predict_proba(X_test)[:, 1]

    lgb_val_f1 = _best_f1_threshold(y_val, lgb_probs_val)
    logger.info(f"  LightGBM Val F1: {lgb_val_f1['f1']:.4f} (threshold={lgb_val_f1['threshold']:.3f})")

    joblib.dump(lgb_model, models_dir / "lightgbm_enhanced.joblib")

    experiment_log.append({
        "experiment": "LightGBM Standalone",
        "val_f1": round(lgb_val_f1["f1"], 4),
        "val_threshold": round(lgb_val_f1["threshold"], 3),
    })

    # ═══════════════════════════════════════════════════════════
    #  STEP 5: Ensemble Stacking (Meta-Learner)
    # ═══════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("STEP 5: Building Ensemble Stack...")
    logger.info("=" * 60)

    # Stack features: [lstm_score, if_score, xgb_prob, lgb_prob]
    stack_train = np.column_stack([
        lstm_scores_train, if_scores_train, xgb_probs_train, lgb_probs_train
    ])
    stack_val = np.column_stack([
        lstm_scores_val, if_scores_val, xgb_probs_val, lgb_probs_val
    ])
    stack_test = np.column_stack([
        lstm_scores_test, if_scores_test, xgb_probs_test, lgb_probs_test
    ])

    # Meta-learner: Logistic Regression
    meta_model = LogisticRegression(
        class_weight="balanced",
        C=1.0,
        max_iter=1000,
        random_state=args.seed,
    )
    meta_model.fit(stack_train, y_train)

    meta_probs_val = meta_model.predict_proba(stack_val)[:, 1]
    meta_probs_test = meta_model.predict_proba(stack_test)[:, 1]

    meta_val_f1 = _best_f1_threshold(y_val, meta_probs_val)
    logger.info(f"  Meta-Learner Val F1: {meta_val_f1['f1']:.4f} (threshold={meta_val_f1['threshold']:.3f})")
    logger.info(f"  Meta-Learner coefficients: LSTM={meta_model.coef_[0][0]:.4f}, IF={meta_model.coef_[0][1]:.4f}, "
                f"XGB={meta_model.coef_[0][2]:.4f}, LGB={meta_model.coef_[0][3]:.4f}")

    joblib.dump(meta_model, models_dir / "meta_learner.joblib")

    # Also try simple average blend
    blend_probs_val = 0.3 * xgb_probs_val + 0.3 * lgb_probs_val + 0.2 * (lstm_scores_val / max(1e-8, lstm_scores_val.max())) + 0.2 * if_scores_val
    blend_val_f1 = _best_f1_threshold(y_val, blend_probs_val)
    logger.info(f"  Simple Blend Val F1: {blend_val_f1['f1']:.4f}")

    experiment_log.append({
        "experiment": "Meta-Learner (LR)",
        "val_f1": round(meta_val_f1["f1"], 4),
        "val_threshold": round(meta_val_f1["threshold"], 3),
    })
    experiment_log.append({
        "experiment": "Simple Blend",
        "val_f1": round(blend_val_f1["f1"], 4),
        "val_threshold": round(blend_val_f1["threshold"], 3),
    })

    # ═══════════════════════════════════════════════════════════
    #  STEP 6: Final Evaluation on Test Set
    # ═══════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("STEP 6: Final Evaluation on Test Set")
    logger.info("=" * 60)

    # Choose best model based on val F1
    models_compared = {
        "XGBoost": (xgb_probs_test, xgb_val_f1),
        "LightGBM": (lgb_probs_test, lgb_val_f1),
        "Meta-Learner": (meta_probs_test, meta_val_f1),
    }

    best_model_name = max(models_compared.keys(), key=lambda k: models_compared[k][1]["f1"])
    best_probs, best_info = models_compared[best_model_name]
    best_threshold = best_info["threshold"]

    logger.info(f"\n  🏆 Best model: {best_model_name} (Val F1={best_info['f1']:.4f})")

    # Evaluate all models on test set
    all_results = {}
    for name, (probs, vinfo) in models_compared.items():
        thresh = vinfo["threshold"]
        preds = (probs >= thresh).astype(int)
        
        test_f1 = f1_score(y_test, preds, zero_division=0)
        test_prec = precision_score(y_test, preds, zero_division=0)
        test_rec = recall_score(y_test, preds, zero_division=0)
        test_auc = roc_auc_score(y_test, probs)
        test_prauc = average_precision_score(y_test, probs)
        cm = confusion_matrix(y_test, preds)
        tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)
        fpr = fp / max(1, fp + tn)

        result = {
            "model": name,
            "threshold": float(thresh),
            "test_f1": float(test_f1),
            "test_precision": float(test_prec),
            "test_recall": float(test_rec),
            "test_auc_roc": float(test_auc),
            "test_pr_auc": float(test_prauc),
            "test_fpr": float(fpr),
            "tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn),
            "val_f1": float(vinfo["f1"]),
        }
        all_results[name] = result

        marker = " ← BEST" if name == best_model_name else ""
        logger.info(f"\n  {name}{marker}:")
        logger.info(f"    F1={test_f1:.4f}  P={test_prec:.4f}  R={test_rec:.4f}  AUC={test_auc:.4f}  PR-AUC={test_prauc:.4f}")
        logger.info(f"    TP={tp}  FP={fp}  FN={fn}  TN={tn}  FPR={fpr:.4f}")

    # Also evaluate unsupervised models alone
    logger.info("\n  --- Unsupervised Baselines ---")
    for name, scores, labels in [
        ("LSTM-AE", lstm_scores_test, y_test),
        ("IsolationForest", if_scores_test, y_test),
    ]:
        bf1 = _best_f1_threshold(y_test, scores)
        logger.info(f"  {name}: Test F1={bf1['f1']:.4f} (threshold={bf1['threshold']:.4f})")
        all_results[name] = {"model": name, "test_f1": float(bf1["f1"])}

    # ═══════════════════════════════════════════════════════════
    #  STEP 7: Save everything
    # ═══════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("STEP 7: Saving results & experiment log")
    logger.info("=" * 60)

    # Comprehensive metrics
    metrics = {
        "best_model": best_model_name,
        "all_results": all_results,
        "experiment_log": experiment_log,
        "feature_count": len(feature_cols),
        "top_features_xgb": [{"feature": f, "importance": round(float(s), 6)} for f, s in top_features[:30]],
        "meta_learner_weights": {
            "lstm": float(meta_model.coef_[0][0]),
            "isolation_forest": float(meta_model.coef_[0][1]),
            "xgboost": float(meta_model.coef_[0][2]),
            "lightgbm": float(meta_model.coef_[0][3]),
        },
        "smote_applied": args.smote,
    }

    with open(results_dir / "metrics_enhanced.json", "w") as f:
        json.dump(metrics, f, indent=2, default=str)

    # Save experiment log to research folder
    with open(research_dir / "03_experiment_log.json", "w") as f:
        json.dump(experiment_log, f, indent=2, default=str)

    # Generate experiment report
    _generate_experiment_report(all_results, top_features, experiment_log, research_dir)

    # Save twin embeddings
    embeddings = extract_twin_embeddings(lstm_model, Xseq_test, lstm_mean, lstm_std, Config.model.DEVICE)
    np.save(results_dir / "twin_embeddings_enhanced.npy", embeddings)

    logger.success(f"\n{'='*60}")
    logger.success(f"✅ Enhanced Pipeline Complete!")
    logger.success(f"{'='*60}")
    best = all_results[best_model_name]
    logger.info(f"  Best Model: {best_model_name}")
    logger.info(f"  Test F1:    {best['test_f1']:.4f}")
    logger.info(f"  Test AUC:   {best['test_auc_roc']:.4f}")
    logger.info(f"  Features:   {len(feature_cols)}")

    return metrics


def _best_f1_threshold(y_true, probs, n_thresholds=200):
    """Find threshold that maximizes F1 score."""
    best_f1, best_t = 0, 0.5
    for t in np.linspace(0.01, 0.99, n_thresholds):
        preds = (probs >= t).astype(int)
        if preds.sum() == 0:
            continue
        f1 = f1_score(y_true, preds, zero_division=0)
        if f1 > best_f1:
            best_f1 = f1
            best_t = t
    return {"f1": best_f1, "threshold": best_t}


def _generate_experiment_report(all_results, top_features, experiment_log, research_dir):
    """Generate a markdown experiment report."""
    lines = []
    lines.append("# 03 — Model Training Experiments & Results\n")
    lines.append(f"**Generated**: 2026-06-16\n")
    lines.append("---\n")
    lines.append("## Model Comparison (Test Set)\n")
    lines.append("| Model | F1 | Precision | Recall | AUC-ROC | PR-AUC | FPR | TP | FP | FN | TN |")
    lines.append("|-------|----|-----------|--------|---------|--------|-----|----|----|----|----|")

    for name, r in all_results.items():
        if "test_precision" in r:
            lines.append(
                f"| {name} | **{r['test_f1']:.4f}** | {r['test_precision']:.4f} | "
                f"{r['test_recall']:.4f} | {r['test_auc_roc']:.4f} | {r['test_pr_auc']:.4f} | "
                f"{r['test_fpr']:.4f} | {r['tp']} | {r['fp']} | {r['fn']} | {r['tn']} |"
            )
        else:
            lines.append(f"| {name} | **{r['test_f1']:.4f}** | — | — | — | — | — | — | — | — | — |")

    lines.append("\n## Top 20 Features (XGBoost Importance)\n")
    lines.append("| Rank | Feature | Importance |")
    lines.append("|------|---------|-----------|")
    for rank, (feat, imp) in enumerate(top_features[:20], 1):
        lines.append(f"| {rank} | {feat} | {imp:.6f} |")

    lines.append("\n## Experiment Log\n")
    lines.append("```json")
    lines.append(json.dumps(experiment_log, indent=2, default=str))
    lines.append("```\n")

    report_path = research_dir / "03_experiment_results.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    logger.info(f"  Experiment report saved to: {report_path}")


if __name__ == "__main__":
    main()
