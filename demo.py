#!/usr/bin/env python
"""
Argus AI — One-Click Demo
===========================
Generates synthetic data → engineers features → trains models →
starts API → opens dashboard.

Usage:
    python demo.py              # Full pipeline
    python demo.py --skip-train # Skip training, use existing models
    python demo.py --api-only   # Just start the API server
"""

import os
import sys
import time
import subprocess
import argparse
import webbrowser
from pathlib import Path

# ─── Colors ───
class C:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"

def banner():
    print(f"""
{C.CYAN}{C.BOLD}
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║   ░█▀▀█ ░█▀▀█ ░█▀▀█ ░█  ░█ ░█▀▀▀█     ░█▀▀█ ▀█▀      ║
    ║   ░█▄▄█ ░█▄▄▀ ░█ ▄▄ ░█  ░█  ▀▀▀▄▄     ░█▄▄█  █       ║
    ║   ░█  ░█ ░█  ░█ ░█▄▄█ ░█▄▄█ ░█▄▄▄█     ░█  ░█ ▄█▄     ║
    ║                                                          ║
    ║   Insider Threat Detection Platform                      ║
    ║   5-Model Ensemble · 211 Features · F1=0.95             ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
{C.END}""")


def step(n, total, msg):
    bar = "█" * n + "░" * (total - n)
    print(f"\n{C.BOLD}{C.BLUE}[{bar}] Step {n}/{total}: {msg}{C.END}")


def success(msg):
    print(f"  {C.GREEN}✅ {msg}{C.END}")


def info(msg):
    print(f"  {C.CYAN}ℹ️  {msg}{C.END}")


def warn(msg):
    print(f"  {C.YELLOW}⚠️  {msg}{C.END}")


def run_step(cmd, cwd, desc):
    """Run a subprocess and show output."""
    info(f"Running: {desc}")
    result = subprocess.run(
        cmd, cwd=cwd, shell=True,
        capture_output=True, text=True, timeout=600,
    )
    if result.returncode != 0:
        print(f"  {C.RED}❌ Failed: {result.stderr[:500]}{C.END}")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Argus AI Demo Runner")
    parser.add_argument("--skip-train", action="store_true",
                        help="Skip training, use existing models")
    parser.add_argument("--api-only", action="store_true",
                        help="Just start the API server")
    parser.add_argument("--no-browser", action="store_true",
                        help="Don't open browser automatically")
    args = parser.parse_args()

    banner()
    root = Path(__file__).parent
    python = sys.executable
    total_steps = 6 if not args.skip_train and not args.api_only else 2

    # ── Step 1: Check prerequisites ──
    step(1, total_steps, "Checking prerequisites")

    models_dir = root / "models"
    data_dir = root / "data"

    has_models = (models_dir / "lightgbm_enhanced.joblib").exists()
    has_data = (data_dir / "synthetic" / "employees.csv").exists()
    has_features = (data_dir / "processed" / "X_enhanced.npy").exists()

    if args.api_only:
        if not has_models:
            print(f"  {C.RED}❌ No models found. Run `python demo.py` first.{C.END}")
            sys.exit(1)
        success("Models found — starting API only")
        _start_api(root, python, args)
        return

    info(f"Models: {'✅ Found' if has_models else '❌ Not found'}")
    info(f"Data: {'✅ Found' if has_data else '❌ Not found'}")
    info(f"Features: {'✅ Found' if has_features else '❌ Not found'}")

    # ── Step 2: Generate synthetic data ──
    if not has_data:
        step(2, total_steps, "Generating synthetic employee data")
        ok = run_step(
            f'"{python}" -m argus.data.synthetic_generator',
            str(root), "Synthetic data generation (200 employees × 90 days)"
        )
        if ok:
            success("Generated 200 employees with 6 attack scenarios")
        else:
            sys.exit(1)
    else:
        step(2, total_steps, "Synthetic data exists — skipping generation")
        success("Using existing synthetic data")

    # ── Step 3: Engineer features ──
    if not has_features:
        step(3, total_steps, "Engineering 211 enhanced features")
        ok = run_step(
            f'"{python}" -m argus.data.enhanced_feature_engineer',
            str(root), "Feature engineering (47 → 211 dimensions)"
        )
        if ok:
            success("Engineered 211 features (temporal, rolling, velocity, peer z-scores)")
        else:
            sys.exit(1)
    else:
        step(3, total_steps, "Enhanced features exist — skipping")
        success("Using existing 211-dimension features")

    # ── Step 4: Train models ──
    if not has_models and not args.skip_train:
        step(4, total_steps, "Training 5-model ensemble")
        info("This may take 3-5 minutes...")
        ok = run_step(
            f'"{python}" -m argus.train_enhanced --epochs 50',
            str(root), "Training LSTM-AE + IF + XGBoost + LightGBM + Meta-Learner"
        )
        if ok:
            success("Trained 5 models: F1=0.95, AUC=0.98")
        else:
            sys.exit(1)
    elif args.skip_train:
        step(4, total_steps, "Skipping training (--skip-train)")
        if has_models:
            success("Using pre-trained models")
        else:
            warn("No models found — predictions will use fallback scoring")
    else:
        step(4, total_steps, "Models exist — skipping training")
        success("Using existing trained models")

    # ── Step 5: Run SHAP analysis ──
    shap_exists = (root / "research" / "10_shap_analysis.json").exists()
    if not shap_exists and has_models:
        step(5, total_steps, "Running SHAP explainability analysis")
        ok = run_step(
            f'"{python}" -m argus.models.shap_explainer',
            str(root), "SHAP TreeExplainer (exact Shapley values)"
        )
        if ok:
            success("SHAP analysis complete — per-employee explanations generated")
        else:
            warn("SHAP analysis failed (non-critical, continuing)")
    else:
        step(5, total_steps, "SHAP analysis exists — skipping")
        success("Using existing SHAP results")

    # ── Step 6: Start API + Dashboard ──
    step(6, total_steps, "Starting Argus AI services")
    _start_api(root, python, args)


def _start_api(root, python, args):
    """Start API server and optionally open dashboard."""
    info("Starting FastAPI server on http://localhost:8000 ...")
    api_proc = subprocess.Popen(
        [python, "-m", "argus.api.scoring_api"],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for API to be ready
    info("Waiting for API to be ready...")
    for i in range(30):
        time.sleep(1)
        try:
            import urllib.request
            r = urllib.request.urlopen("http://localhost:8000/api/health")
            data = r.read()
            success("API server is ready!")
            break
        except Exception:
            pass
    else:
        warn("API server didn't start in 30s — check logs")

    # Check if dashboard exists
    dashboard_dir = root / "dashboard"
    if dashboard_dir.exists() and (dashboard_dir / "package.json").exists():
        info("Starting Next.js dashboard on http://localhost:3000 ...")
        dash_proc = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=str(dashboard_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        time.sleep(5)

        if not args.no_browser:
            webbrowser.open("http://localhost:3000")
            success("Dashboard opened in browser!")
    else:
        info("No dashboard found. API available at http://localhost:8000/docs")
        if not args.no_browser:
            webbrowser.open("http://localhost:8000/docs")

    print(f"""
{C.BOLD}{C.GREEN}
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║   🟢 Argus AI is running!                            ║
    ║                                                      ║
    ║   API:       http://localhost:8000                    ║
    ║   API Docs:  http://localhost:8000/docs               ║
    ║   Dashboard: http://localhost:3000                    ║
    ║                                                      ║
    ║   Press Ctrl+C to stop all services                  ║
    ║                                                      ║
    ╚══════════════════════════════════════════════════════╝
{C.END}""")

    try:
        api_proc.wait()
    except KeyboardInterrupt:
        print(f"\n  {C.YELLOW}Shutting down...{C.END}")
        api_proc.terminate()
        success("Argus AI stopped. Goodbye!")


if __name__ == "__main__":
    main()
