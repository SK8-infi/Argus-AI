"""
Argus AI — Global Configuration
================================
Central configuration for all paths, hyperparameters, feature definitions,
and model settings. Import this module in any script:

    from argus.config import Config
"""

import os
from pathlib import Path


class Paths:
    """File system paths."""
    ROOT = Path(__file__).parent.parent  # C:\Github\BOB Hackathon
    DATA = ROOT / "data"
    CERT_DATA = DATA / "cert_r4.2"
    SYNTHETIC_DATA = DATA / "synthetic"
    PROCESSED_DATA = DATA / "processed"
    MODELS = ROOT / "models"
    RESULTS = ROOT / "results"
    DOCS = ROOT / "docs"

    @classmethod
    def ensure_dirs(cls):
        """Create all required directories."""
        for path in [cls.DATA, cls.CERT_DATA, cls.SYNTHETIC_DATA,
                     cls.PROCESSED_DATA, cls.MODELS, cls.RESULTS]:
            path.mkdir(parents=True, exist_ok=True)


class DataConfig:
    """Data pipeline configuration."""
    # Synthetic data generation
    NUM_EMPLOYEES = 200
    NUM_DAYS = 90
    INSIDER_RATIO = 0.08  # 8% insider rate (16 insiders out of 200)
    RANDOM_SEED = 42

    # Department distribution
    DEPARTMENTS = {
        "retail_banking": {"count": 60, "roles": ["relationship_manager", "teller", "branch_manager"]},
        "treasury": {"count": 25, "roles": ["trader", "treasury_analyst"]},
        "it_admin": {"count": 35, "roles": ["system_admin", "dba_admin", "help_desk"]},
        "hr": {"count": 30, "roles": ["hr_generalist", "recruiter", "payroll"]},
        "compliance": {"count": 50, "roles": ["aml_analyst", "auditor", "risk_officer"]},
    }

    # Feature engineering
    NUM_FEATURES = 47
    SEQUENCE_LENGTH = 7  # 7-day sliding windows for LSTM
    FEATURE_CATEGORIES = [
        "temporal",        # 8 features
        "access_volume",   # 7 features
        "device_location", # 5 features
        "communication",   # 6 features
        "data_movement",   # 7 features
        "behavioral_ratio",# 6 features
        "sequence",        # 8 features
    ]


class ModelConfig:
    """Model hyperparameters."""
    # LSTM Autoencoder
    LSTM_INPUT_DIM = 47
    LSTM_HIDDEN_DIM = 32
    LSTM_LATENT_DIM = 16
    LSTM_NUM_LAYERS = 2
    LSTM_DROPOUT = 0.2
    LSTM_EPOCHS = 50
    LSTM_BATCH_SIZE = 32
    LSTM_LR = 1e-3
    LSTM_PATIENCE = 10  # Early stopping

    # Isolation Forest
    IF_N_ESTIMATORS = 500
    IF_CONTAMINATION = 0.05
    IF_MAX_FEATURES = 1.0

    # Hybrid Ensemble
    ENSEMBLE_ALPHA = 0.65  # Weight for LSTM (temporal), 1-alpha for IF (static)

    # Anomaly thresholds
    ANOMALY_PERCENTILE = 95  # 95th percentile of normal reconstruction error

    # Trust Score
    TRUST_INITIAL = 95.0
    TRUST_DECAY_RATE = 0.05
    TRUST_REINFORCEMENT = 5.0
    TRUST_PENALTY_BASE = 20.0

    # General
    RANDOM_SEED = 42
    DEVICE = "cuda"  # Will fallback to "cpu" if CUDA unavailable


class APIConfig:
    """API configuration."""
    HOST = "0.0.0.0"
    PORT = 8000
    RELOAD = True  # Hot reload for development


class DashboardConfig:
    """Dashboard configuration."""
    TRUST_LEVELS = {
        "CRITICAL": (0, 20),
        "HIGH_RISK": (20, 40),
        "MEDIUM_RISK": (40, 60),
        "LOW_RISK": (60, 80),
        "TRUSTED": (80, 100),
    }
    TRUST_COLORS = {
        "CRITICAL": "#dc2626",
        "HIGH_RISK": "#f97316",
        "MEDIUM_RISK": "#eab308",
        "LOW_RISK": "#22c55e",
        "TRUSTED": "#06b6d4",
    }


class Config:
    """Master configuration — access all sub-configs."""
    paths = Paths
    data = DataConfig
    model = ModelConfig
    api = APIConfig
    dashboard = DashboardConfig

    @classmethod
    def setup(cls):
        """Initialize project directories and validate environment."""
        cls.paths.ensure_dirs()
        print(f"[Argus AI] Project root: {cls.paths.ROOT}")
        print(f"[Argus AI] Data directory: {cls.paths.DATA}")
        print(f"[Argus AI] Models directory: {cls.paths.MODELS}")

        # Check GPU
        try:
            import torch
            if torch.cuda.is_available():
                print(f"[Argus AI] GPU: {torch.cuda.get_device_name(0)}")
                cls.model.DEVICE = "cuda"
            else:
                print("[Argus AI] GPU: Not available, using CPU")
                cls.model.DEVICE = "cpu"
        except ImportError:
            print("[Argus AI] PyTorch not installed yet")
            cls.model.DEVICE = "cpu"


if __name__ == "__main__":
    Config.setup()
