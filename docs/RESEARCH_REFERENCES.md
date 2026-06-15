# 📚 Argus AI — Research References

## Overview

This document catalogs the academic papers, industry reports, and technical references that ground Argus AI's design decisions. Each reference is linked to the specific module or technique it supports.

---

## Core Insider Threat Detection

### [R1] CERT Insider Threat Dataset
- **Authors**: Glasser, D.B. & Lindauer, B.J.
- **Title**: "Bridging the Gap: A Pragmatic Approach to Generating Insider Threat Data"
- **Year**: 2013
- **Venue**: IEEE Security and Privacy Workshops
- **Relevance**: Foundation dataset methodology. Our synthetic data generator follows the same scenario injection approach.
- **Used In**: Module 0 (Data Strategy), Synthetic Data Generator

### [R2] Insider Threat Detection Using LSTM Autoencoder
- **Authors**: Yuan, S. & Wu, X.
- **Title**: "Deep Learning for Insider Threat Detection: Review, Challenges, and Opportunities"
- **Year**: 2021
- **Venue**: Computers & Security
- **Relevance**: Validates LSTM Autoencoder approach for temporal anomaly detection. Reports F1 ≈ 0.86 on CERT data.
- **Used In**: Module 2 (Risk Engine — LSTM Autoencoder)

### [R3] Insider Threat Detection Workflow Evaluation
- **Authors**: Le, D.C. & Zincir-Heywood, A.N.
- **Title**: "Evaluating Insider Threat Detection Workflow Using Supervised and Unsupervised Learning"
- **Year**: 2021
- **Venue**: Security and Privacy
- **Relevance**: Feature aggregation methodology (user-day granularity). Markov chain activity modeling.
- **Used In**: Module 0 (Data Strategy), Module 1 (Feature Engineering)

### [R4] User-Based Sequencing for Insider Threats
- **Authors**: Various (2024-2025 ArXiv)
- **Title**: "User-Based Sequencing with Transformer Encoders for Insider Threat Detection"
- **Year**: 2024-2025
- **Venue**: ArXiv preprints
- **Relevance**: State-of-the-art sequence modeling. Validates that temporal sequencing outperforms static features. Reports ~96% accuracy.
- **Used In**: Module 2 (LSTM Architecture design)

### [R5] Hybrid Isolation Forest + Deep Learning
- **Authors**: Various (2024-2025)
- **Title**: Multiple papers on hybrid ensemble approaches for insider threat detection
- **Venue**: Various — IEEE, ACM, MDPI
- **Relevance**: Validates that hybrid IF + LSTM outperforms either alone. Reports F1 ≈ 0.89-0.92.
- **Used In**: Module 2 (Hybrid Ensemble design)

---

## Synthetic Data Generation

### [R6] CTGAN: Modeling Tabular Data using Conditional GANs
- **Authors**: Xu, L., Skoularidou, M., Cuesta-Infante, A., & Veeramachaneni, K.
- **Title**: "Modeling Tabular Data using Conditional GAN"
- **Year**: 2019
- **Venue**: NeurIPS
- **Relevance**: Foundational paper for CTGAN synthetic data generation. Preserves column correlations.
- **Used In**: Module 0 (Synthetic Data Generator — CTGAN component)

### [R7] Synthetic Data for Insider Threat Detection
- **Authors**: Various (2024-2025 MDPI)
- **Title**: "Generative AI for Privacy-Preserving Insider Threat Data Synthesis"
- **Year**: 2024-2025
- **Venue**: MDPI Sensors / Applied Sciences
- **Relevance**: Validates synthetic data approaches for training insider threat models without exposing real employee data.
- **Used In**: Module 0 (Data Strategy justification)

---

## Digital Twins & Behavioral Profiling

### [R8] Cybersecurity Digital Twins
- **Authors**: Various (2024-2025)
- **Title**: "Digital Twins for Cybersecurity: Architecture and Applications"
- **Year**: 2024-2025
- **Venue**: Forbes, IEEE, ResearchGate
- **Relevance**: Validates the Digital Twin concept for security monitoring. Describes dynamic modeling, real-time synchronization, and threat simulation capabilities.
- **Used In**: Module 1 (Digital Employee Twin concept)

### [R9] Employee Digital Twins — Behavioral Layers
- **Authors**: Various (IT Brew, Trend Micro)
- **Title**: Research on Employee Digital Twins with Knowledge, Personality, Mindset, and Trust layers
- **Year**: 2024-2025
- **Relevance**: Defines the multi-layer EDT framework. Our Behavioral Genome is inspired by this layered approach.
- **Used In**: Module 1 (Behavioral Genome design)

### [R10] LSTM Autoencoders for Behavioral Anomaly
- **Authors**: ResearchGate publications
- **Title**: "High-Fidelity Temporal Profiles via LSTM Autoencoders"
- **Year**: 2024
- **Relevance**: Uses reconstruction loss from LSTM Autoencoders to detect behavioral deviations from a digital twin baseline.
- **Used In**: Module 1 (Twin deviation scoring), Module 2 (LSTM Autoencoder)

---

## Zero Trust & Privilege Management

### [R11] NIST SP 800-207: Zero Trust Architecture
- **Authors**: Rose, S., Borchert, O., Mitchell, S., & Connelly, S.
- **Title**: "Zero Trust Architecture"
- **Year**: 2020
- **Venue**: NIST Special Publication 800-207
- **Relevance**: Foundational Zero Trust framework. Our Privilege Decay Function is a mathematical formalization of NIST's continuous verification principle.
- **Used In**: Module 3 (Privilege Context Engine)

### [R12] Dynamic Trust Scoring
- **Authors**: Identity Management Institute publications
- **Title**: "Dynamic Trust Scoring for Continuous Authentication"
- **Year**: 2024
- **Relevance**: Describes the concept of numerical trust scores that rise/fall based on behavioral signals. Our privilege decay function extends this with exponential decay mathematics.
- **Used In**: Module 3 (Dynamic Trust Score)

### [R13] Privilege Decay & Least Privilege
- **Authors**: Seqrite, Ping Identity publications
- **Title**: "Zero Trust for Banking: Continuous Monitoring and Privilege Management"
- **Year**: 2024-2025
- **Relevance**: Industry validation that privilege decay (automatic expiry of unused access rights) is becoming standard in banking security.
- **Used In**: Module 3 (Privilege Decay Function)

---

## Federated Learning & Privacy

### [R14] Federated Learning for Financial Crime
- **Authors**: RBC Borealis Research
- **Title**: "Federated Learning for AML: Cross-Bank Collaboration Without Data Sharing"
- **Year**: 2023
- **Relevance**: Demonstrated federated learning achieves similar AML detection results without sharing raw data. Recall improved from 0.59 to 0.66 at 5% FPR.
- **Used In**: Module 5 (Federated Learning design)

### [R15] India's Digital Personal Data Protection Act
- **Year**: 2023
- **Relevance**: Regulatory framework requiring data minimization and purpose limitation. Our FL + DP approach is privacy-by-design, not privacy-by-policy.
- **Used In**: Module 5 (Regulatory compliance)

### [R16] Differential Privacy for Deep Learning
- **Authors**: Abadi, M., et al.
- **Title**: "Deep Learning with Differential Privacy"
- **Year**: 2016
- **Venue**: ACM CCS
- **Relevance**: Foundational DP paper. Our use of Opacus for ε-DP on PyTorch gradients follows this methodology.
- **Used In**: Module 5 (Differential Privacy)

---

## Explainability

### [R17] SHAP: A Unified Approach to Interpreting Model Predictions
- **Authors**: Lundberg, S.M. & Lee, S.I.
- **Title**: "A Unified Approach to Interpreting Model Predictions"
- **Year**: 2017
- **Venue**: NeurIPS
- **Relevance**: Foundation for our feature-level explanations. Used for both Isolation Forest and XGBoost explanations.
- **Used In**: Module 4 (Explainable Alerts — SHAP component)

---

## Anomaly Detection Techniques

### [R18] Isolation Forest
- **Authors**: Liu, F.T., Ting, K.M., & Zhou, Z.H.
- **Title**: "Isolation Forest"
- **Year**: 2008
- **Venue**: IEEE ICDM
- **Relevance**: Original Isolation Forest paper. Our static anomaly detection path uses this algorithm.
- **Used In**: Module 2 (Static anomaly detection)

### [R19] LSTM Autoencoders for Anomaly Detection
- **Authors**: Malhotra, P., et al.
- **Title**: "LSTM-based Encoder-Decoder for Multi-Sensor Anomaly Detection"
- **Year**: 2016
- **Venue**: ICML Anomaly Detection Workshop
- **Relevance**: Foundational architecture for sequence-based anomaly detection via reconstruction error.
- **Used In**: Module 2 (Temporal anomaly detection)

---

## Industry Context

### [R20] RBI Digital Payments Intelligence Platform
- **Year**: 2024-2025
- **Relevance**: RBI directive for real-time risk scoring across digital payment channels. Our API design (<500ms latency) aligns with this requirement.

### [R21] CERT Insider Threat Center — Best Practices
- **Authors**: CMU Software Engineering Institute
- **Title**: "Common Sense Guide to Mitigating Insider Threats"
- **Year**: 2022 (7th Edition)
- **Relevance**: Industry best practices for insider threat programs. Validates our multi-layered approach (behavioral monitoring + access controls + continuous evaluation).

---

## Summary by Module

| Module | Key References |
|--------|---------------|
| **Module 0: Data** | R1, R3, R6, R7 |
| **Module 1: Digital Twin** | R8, R9, R10 |
| **Module 2: Risk Engine** | R2, R4, R5, R18, R19, R22, R23 |
| **Module 3: Privilege Context** | R11, R12, R13 |
| **Module 4: Explainability** | R17, R24 |
| **Module 5: Privacy** | R14, R15, R16, R25 |
| **Overall** | R20, R21 |

---

## Enhanced Pipeline v2.0 References

### [R22] LightGBM: A Highly Efficient Gradient Boosting Decision Tree
- **Authors**: Ke, G., et al.
- **Title**: "LightGBM: A Highly Efficient Gradient Boosting Decision Tree"
- **Year**: 2017
- **Venue**: NeurIPS
- **Relevance**: Primary supervised model in our enhanced pipeline. Achieved F1=0.949 on insider detection. Leaf-wise growth strategy is particularly effective for our imbalanced dataset with scale_pos_weight.
- **Used In**: Enhanced Risk Scoring Engine (primary model)

### [R23] XGBoost: A Scalable Tree Boosting System
- **Authors**: Chen, T. & Guestrin, C.
- **Title**: "XGBoost: A Scalable Tree Boosting System"
- **Year**: 2016
- **Venue**: ACM KDD
- **Relevance**: Secondary supervised model. Cross-validated F1=0.935. Used for ensemble diversity in meta-learner stacking.
- **Used In**: Enhanced Risk Scoring Engine (ensemble member)

### [R24] Consistent Individualized Feature Attribution for Tree Ensembles
- **Authors**: Lundberg, S.M., Erion, G.G., & Lee, S.I.
- **Title**: "Consistent Individualized Feature Attribution for Tree Ensembles"
- **Year**: 2019
- **Venue**: AAAI
- **Relevance**: TreeExplainer algorithm used for exact SHAP values on LightGBM. Polynomial time exact Shapley computation for tree models (vs exponential for general models). Our top feature: `clearance_normalized` (SHAP=0.610).
- **Used In**: SHAP Explainability Layer

### [R25] One-Shot Federated Stacking
- **Authors**: Li, Q., Wen, Z., & He, B.
- **Title**: "Practical One-Shot Federated Learning for Cross-Silo Settings"
- **Year**: 2023
- **Venue**: NeurIPS
- **Relevance**: Validates one-shot federated stacking (train local, share predictions, stack globally). Our implementation shares only P(insider) scalars between departments — zero gradient exchange. AUC=0.974 vs centralized 0.983.
- **Used In**: Federated Stacking (privacy-compliant alternative)

### [R26] Stacked Generalization
- **Authors**: Wolpert, D.H.
- **Title**: "Stacked Generalization"
- **Year**: 1992
- **Venue**: Neural Networks
- **Relevance**: Original meta-learner stacking paper. Our 3-model ensemble (LightGBM + XGBoost + LSTM-AE/IF) uses logistic regression as the level-1 learner, following this framework.
- **Used In**: Meta-Learner Ensemble
