# 🔱 Argus AI — Idea Proposal

## Privacy-Preserving Digital Employee Twins for Continuous Insider Threat Detection in Banking Environments

**Hackathon**: CyberShield — PSBs Hackathon Series 2026
**Problem Statement**: AI/ML-Based Identity Trust Framework
**Team**: SK8-infi

---

## 1. Executive Summary

**Argus AI** is an intelligent insider threat detection platform designed for Indian banking environments. Named after the all-seeing giant of Greek mythology, it introduces the concept of **Digital Employee Twins** — dynamic behavioral replicas that continuously monitor employee activities and detect threats through deviation analysis.

Unlike conventional identity verification systems that authenticate once at login, Argus AI treats identity trust as a **continuous, decaying signal** that must be constantly reinforced by normal behavior. When an employee's current activity deviates from their digital twin's expectations, the system dynamically adjusts their trust score and triggers appropriate responses — from silent monitoring to session suspension.

### Why Insider Threats?

While most teams will tackle Account Takeover (ATO), we focus on the **harder, less crowded, and more research-worthy** problem of insider threats:

| Aspect | Account Takeover | Insider Threats (Our Focus) |
|--------|-----------------|---------------------------|
| **Approach** | Login → Risk Score → OTP | Employee Behavior → Trust Score → Privileged Access Monitoring |
| **Novelty** | Well-trodden path | Few teams attempt this |
| **Research Value** | Incremental | Paper-worthy |
| **Technical Depth** | Moderate | High — temporal modeling, role context, behavioral profiling |
| **Judge Appeal** | Expected | Surprising + impressive |

### Key Metrics (Targets)

| Metric | Target | Description |
|--------|--------|-------------|
| **AUC-ROC** | > 0.95 | Near-perfect discrimination between normal and malicious |
| **F1 Score** | > 0.85 | Balance of precision and recall |
| **Precision** | > 0.80 | Minimal false alerts (analyst fatigue reduction) |
| **Recall** | > 0.85 | Catch majority of insider threats |
| **Alert Latency** | < 500ms | Real-time scoring |
| **False Positive Rate** | < 2% | Acceptable for banking operations |

---

## 2. Problem Analysis

### 2.1 What Are Insider Threats?

Banks inherently trust employees, contractors, and admins with access to sensitive systems and data. Insider threats occur when trusted individuals misuse their access, either maliciously or through compromised credentials.

**Real-World Insider Threat Scenarios in Banking**:

| Scenario | Description | Impact |
|----------|-------------|--------|
| **Bulk Customer Data Exfiltration** | Employee downloads unusually large amounts of customer PII | Data breach, regulatory penalty |
| **Unauthorized Account Snooping** | HR staff accessing customer financial records | Privacy violation |
| **Privilege Escalation Abuse** | IT admin using superadmin credentials on production systems | System integrity compromise |
| **Pre-Resignation Data Theft** | Employee bulk-downloading files before leaving | IP theft, competitive damage |
| **Credential Compromise** | Legitimate employee account used from two locations simultaneously | Unauthorized access |
| **Slow-Burn Reconnaissance** | Gradually expanding access scope over weeks | Undetected long-term threat |

### 2.2 Why Current Solutions Fail

| Limitation | Impact | Argus AI Solution |
|-----------|--------|-------------------|
| **Static rules** miss evolving threats | New attack patterns bypass thresholds | Continuous behavioral learning via Digital Twin |
| **One-time authentication** | Session hijacking goes undetected | Continuous trust scoring with privilege decay |
| **No role context** | Same alert for admin vs. intern | Role-Resource risk matrix with contextual scoring |
| **Individual baseline only** | Slow-burn threats normalize gradually | Peer Constellation comparison |
| **Point-in-time anomalies** | Multi-step attacks look normal step-by-step | Intent Signal Chain detection |
| **Black-box models** | Can't explain why alert was raised | Natural language explainable alerts |
| **Privacy concerns** | Can't share behavioral data across departments | Federated Learning with Differential Privacy |

### 2.3 The Research Gap We Fill

Current state-of-the-art in insider threat detection (2024-2025):

| Approach | Limitation | Our Improvement |
|----------|-----------|-----------------|
| Isolation Forest (static) | Misses temporal patterns | + LSTM Autoencoder for temporal context |
| LSTM Autoencoder (temporal) | No role context | + Privilege Context Engine |
| User Behavior Analytics (UEBA) | Self-referential only | + Peer Constellation Analysis |
| Rule-based triggers | No learning capability | + Self-improving Digital Twin |
| Binary anomaly detection | Yes/No output | + Continuous Trust Score (0-100) with decay |

---

## 3. Our Approach: Five Integrated Modules

### Module 1: Digital Employee Twin — Behavioral Genome

The core innovation. For every employee, we build a **Behavioral Genome** — a multi-dimensional compressed representation of their "normal" behavior.

**What the Twin Learns**:

```
Employee "Raj Sharma" — Relationship Manager, Mumbai Branch
──────────────────────────────────────────────────────────────
Circadian Profile:
  ├─ Typical login: 09:15 ± 12 min
  ├─ Typical logout: 18:30 ± 25 min
  ├─ Weekend logins: Never (0% historical)
  └─ Peak activity: 10:00-12:00, 14:00-16:00

Access Profile:
  ├─ Systems: CRM (daily), CBS (3x/week), Email (daily)
  ├─ Records accessed: 45 ± 15 per day
  ├─ Data volume: 2.3 ± 1.1 MB per day
  └─ External emails: 8 ± 4 per day

Device Profile:
  ├─ Primary: WS_MUM_042 (Mumbai office)
  ├─ Secondary: None
  └─ USB usage: Never (0% historical)

Behavioral Velocity: Stable (0.02 drift/week)
```

**How It Works**:
1. **Historical Training**: Build genome from 30+ days of normal activity
2. **Continuous Comparison**: Every action is scored against the twin
3. **Living Evolution**: Twin updates slowly with new normal behavior (exponential moving average)
4. **Anomaly Signal**: Large deviation from twin → elevated risk

### Module 2: Hybrid Risk Scoring Engine

Two complementary anomaly detection paths:

**Path A — LSTM Autoencoder (Temporal)**:
- Input: 7-day sliding window of 47 behavioral features
- Trained only on normal behavior
- High reconstruction error = temporal anomaly
- Catches: slow-burn threats, sequence-level deviations, gradual behavioral shifts

**Path B — Isolation Forest (Static)**:
- Input: Single day's 47 features + 6 engineered ratios
- Detects extreme outliers in feature space
- Catches: sudden spikes (15× download volume), one-off extreme events

**Ensemble Fusion**:
```
Final_Score = α × LSTM_score + (1-α) × IF_score
where α ≈ 0.65 (optimized on validation set)
```

Research shows this hybrid achieves F1 ≈ 0.89-0.92 on CERT data, vs. 0.86 (LSTM-only) and 0.71 (IF-only).

### Module 3: Privilege Context Engine

**The same action has different risk for different roles.**

Example — "Accessed 100 customer records today":
- **Call-center agent** → Risk = 1.0× (normal for their role)
- **HR employee** → Risk = 6.0× (why are they in customer data?)
- **IT admin** → Risk = 7.0× (no business reason for this)

**Privilege Decay Function**:

Trust decays exponentially when not reinforced by normal behavior:

```
T(t) = T(t-1) × e^(-λ × Δt) + reinforcement(t)
```

Where:
- λ = decay rate (higher for unused/sensitive privileges)
- Δt = time since last normal behavior
- reinforcement = +5 (normal action), 0 (idle), -20 (anomaly)

**Example Timeline**:
```
09:00 Login normally           → Trust = 95
14:00 CRM access (normal)     → Trust = 97 (reinforced)
18:30 Still logged in         → Trust = 88 (decay)
20:00 Treasury access (!role) → Trust = 42 (penalty)
20:05 USB connected           → Trust = 18 (compound risk)
→ ALERT: Step-up verification required
```

### Module 4: Explainable Alert Engine

**Three layers of explainability**:

1. **Intent Signal Chains** — detects attack narratives (sequences), not isolated events:
   ```
   Normal:   Login → CRM → Update 3 records → Logout
   Suspect:  Login → CRM → Bulk export → USB mount → File copy → Logout
   ```

2. **Natural Language Alerts**:
   ```
   🔴 HIGH RISK: Employee Raj Sharma (EMP_047)
   Trust Score: 23/100 (was 94 yesterday)
   
   Risk elevated because:
   ├─ 📍 New workstation (WS_DEL_019) — never used before
   ├─ 🕐 Access at 22:47 IST — outside normal hours (9-18)
   ├─ 📊 847 customer records accessed — 15× daily average (56)
   ├─ 💾 USB device connected — no USB history in 36 months
   └─ 🏦 Treasury database access — not in Relationship Manager scope
   
   Intent Chain Match: "Data Exfiltration" (89% confidence)
   Recommended Action: Suspend session + notify CISO
   ```

3. **Peer Constellation Comparison**:
   - "Other Retail Banking RMs access avg 52 records/day — this employee accessed 847"
   - "0 out of 47 peers accessed treasury DB in last 90 days"

### Module 5: Privacy-Preserving Cross-Department Intelligence

- **Federated Learning**: Each department trains local behavioral models; only model gradients are shared
- **Differential Privacy**: ε-DP (ε = 1.0) ensures gradients can't reconstruct individual behavior
- **Cross-Department Detection**: Catches coordinated attacks spanning multiple departments
- **Compliance**: Aligned with India's Digital Personal Data Protection Act (DPDPA)

---

## 4. Data Strategy

### Primary Dataset: CERT Insider Threat (r4.2)

| Property | Value |
|----------|-------|
| **Source** | CMU Software Engineering Institute |
| **Employees** | ~1,000 simulated users |
| **Duration** | 18 months of activity |
| **Events** | ~32 million across 5 log types |
| **Threat Scenarios** | 70 insider incidents (5 attack types) |
| **Files** | logon.csv, email.csv, file.csv, device.csv, http.csv |

### Supplementary Dataset: LANL Cybersecurity

- 700M+ authentication events from Los Alamos National Laboratory
- Used specifically for temporal login pattern baselines

### Novel: Synthetic Banking Data Generator

Since CERT simulates a generic enterprise (not a bank), we generate a **banking-specific synthetic dataset** using research-grounded methods:

| Method | Research Basis | What It Generates |
|--------|---------------|-------------------|
| Markov Chain Models | Le & Zincir-Heywood (2021) | Normal daily activity sequences per role |
| Gaussian Mixture Models | Yuan & Wu (2021) | Realistic temporal distributions |
| Scenario Injection | CERT methodology (Glasser & Lindauer, 2013) | 6 banking-specific attack scenarios |
| CTGAN | Xu et al. (2019) | Synthetic tabular features preserving correlations |

**Generated Dataset**:
- 200 employees across 5 departments (Retail Banking, Treasury, IT Admin, HR, Compliance)
- 90 days of activity
- 15-20 insider threat scenarios (7.5-10% — realistic ratio)
- 6 distinct banking-specific attack types

---

## 5. What Makes Argus AI Stand Out

| Innovation | Description | Why Judges Will Care |
|-----------|-------------|---------------------|
| **Digital Employee Twin** | Living behavioral model per employee | Far more sophisticated than "we trained XGBoost on fraud data" |
| **Privilege Decay** | Mathematical formalization of Zero Trust | Research-worthy contribution |
| **Intent Signal Chains** | Attack narrative detection | Catches sophisticated multi-step attacks |
| **Peer Constellation** | Social comparison-based anomaly detection | Solves the slow-burn normalization problem |
| **Hybrid LSTM + IF** | Best of temporal + static detection | Grounded in 2024 SOTA research |
| **Explainable Alerts** | "Why" not just "what" | Immediately actionable for security analysts |
| **Banking Synthetic Data** | Domain-specific data generation | Shows research methodology + domain understanding |

---

## 6. Expected Outcomes (Aligned with Problem Statement)

| Expected Outcome | How Argus AI Achieves It |
|-----------------|-------------------------|
| **Reduction in insider misuse** | Continuous monitoring + privilege decay + real-time alerts |
| **Secure, compliant digital access** | Federated Learning + Differential Privacy + DPDPA alignment |
| **Friction-optimized access** | Risk-based verification — challenges ONLY when trust drops |
| **Scalable across channels** | Modular architecture with REST API + department-agnostic design |
| **Detect anomalous behavior** | LSTM Autoencoder + Digital Twin deviation scoring |
| **Detect new device usage** | Device profile tracking in Behavioral Genome |
| **Detect privileged access misuse** | Role-Resource matrix + Privilege Decay Function |
| **Real-time verification** | FastAPI scoring endpoint (<500ms) + dynamic trust thresholds |

---

## 7. Potential Research Paper

> **"Argus AI: Privacy-Preserving Digital Employee Twins with Privilege Decay and Intent Chain Detection for Continuous Insider Threat Monitoring in Banking Environments"**

**Publishable novel contributions**:
1. Behavioral Genome construction methodology
2. Privilege Decay Function mathematical formulation
3. Intent Signal Chain detection algorithm
4. Peer Constellation anomaly detection
5. Banking-specific synthetic data generation methodology
6. Empirical comparison of hybrid LSTM+IF vs. individual models on banking insider threat data

---

## 8. Summary

Argus AI transforms insider threat detection from a reactive, rule-based process into a **proactive, continuous, privacy-preserving intelligence system**. By creating Digital Employee Twins and continuously measuring behavioral deviation, we catch threats that traditional systems miss — from sudden data exfiltration to slow-burn reconnaissance campaigns.

The system is designed to be **impressive in a demo** (real-time trust score changes, visual attack narrative detection, natural language alerts) while being **academically rigorous** (grounded in CERT dataset research, multiple novel contributions, publishable methodology).

**This is not "another login risk scorer." This is a behavioral intelligence platform.**

---

*🔱 Argus — The All-Seeing Guardian of Banking Identity Trust*
