# 📊 Argus AI — Data Strategy

## Overview

Argus AI uses **three data sources** to build, train, and demonstrate the insider threat detection system. This document details the selection rationale, data schemas, feature engineering pipeline, and synthetic data generation methodology.

---

## Data Source 1: CERT Insider Threat Dataset (r4.2)

### Why CERT r4.2?

| Property | CERT r4.2 | CERT r6.2 | LANL |
|----------|-----------|-----------|------|
| **Employees** | ~1,000 | ~4,000 | ~11,000 |
| **Duration** | 18 months | 18 months | 58 days |
| **Insider Scenarios** | 70 (highest ratio) | ~30 | Red team only |
| **Data Modalities** | 5 (logon, email, file, device, http) | 5 | 2 (auth, flow) |
| **Research Usage** | Most cited version | Less common | Network-focused |
| **Our Choice** | ✅ **Primary** | ❌ | Supplementary |

**Decision**: r4.2 has the highest proportion of malicious insider incidents, making it ideal for a hackathon where we need clear signal.

### Dataset Files & Schema

#### `logon.csv` — Session Events
```csv
id,date,user,pc,activity
{id},{YYYY/MM/DD HH:MM:SS},{user_id},{pc_id},{Logon|Logoff}
```
- ~32M records across 18 months
- Captures when employees start/end sessions
- Key features: login times, session durations, weekend access

#### `email.csv` — Email Activity
```csv
id,date,user,pc,to,cc,bcc,from,size,attachments,content
```
- Internal and external email communications
- Key features: external email ratio, attachment sizes, unusual recipients

#### `file.csv` — File Operations
```csv
id,date,user,pc,filename,content
```
- File read/write/copy/delete events
- Key features: file access volume, sensitive file access, bulk operations

#### `device.csv` — USB/Removable Media
```csv
id,date,user,pc,activity
{id},{date},{user_id},{pc_id},{Connect|Disconnect}
```
- USB device connect/disconnect events
- Key features: USB usage frequency, new device detection, timing

#### `http.csv` — Web Browsing
```csv
id,date,user,pc,url,content
```
- Web browsing activity
- Key features: URLs visited, external uploads, job search activity

#### `psychometric.csv` — Employee Profiles
```csv
user_id,O,C,E,A,N
```
- Big Five personality traits (OCEAN model)
- Used for employee profiling context

#### `answers/` — Ground Truth Labels
- Identifies which users are insiders and their attack scenarios
- Attack types: data exfiltration, sabotage, IP theft, credential abuse

### CERT Data Processing Pipeline

```
Raw CERT CSVs (5 files, ~2-4 GB)
        │
        ▼
┌───────────────────────┐
│  1. PARSE & CLEAN     │
│  • Parse timestamps    │
│  • Standardize IDs    │
│  • Remove duplicates  │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  2. AGGREGATE         │
│  • Group by (user,    │
│    date) pairs        │
│  • Count events per   │
│    type per day       │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  3. FEATURE ENGINEER  │
│  • 47 features per    │
│    employee-day       │
│  • 8 feature groups   │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  4. SEQUENCE BUILD    │
│  • 7-day sliding      │
│    windows            │
│  • (user, 7, 47)      │
│    tensors for LSTM   │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  5. LABEL & SPLIT     │
│  • Match with answers │
│  • Train (normal only)│
│  • Val/Test (mixed)   │
└───────────────────────┘
```

---

## Data Source 2: LANL Cybersecurity Dataset

### Usage: Supplementary — Authentication Patterns Only

We use LANL specifically for its massive scale of authentication events (700M+), which gives us:
- **Baseline temporal patterns**: What "normal" login distributions look like at enterprise scale
- **Rare event statistics**: How often legitimate users access unusual machines
- **Circadian rhythm reference**: Global login hour distributions for FFT baseline

We do NOT use LANL for primary training — only as a reference distribution.

### Processing

```python
# Extract hourly login distribution from LANL
# Used as prior for circadian profile construction
lanl_hourly_dist = compute_hourly_login_distribution(lanl_auth_data)
# Output: 24-element vector (proportion of logins per hour)
```

---

## Data Source 3: Synthetic Banking Data Generator

### Why Synthetic Data?

CERT simulates a **generic enterprise** (technology company scenario). Banks have specific characteristics:

| Aspect | Generic Enterprise (CERT) | Banking (Our Synthetic) |
|--------|--------------------------|------------------------|
| **Systems** | Email, file servers | CBS, CRM, Treasury, Compliance |
| **Data Sensitivity** | Corporate IP | Customer PII, financial records |
| **Regulatory** | General compliance | RBI, DPDPA, FIU-IND |
| **Roles** | Engineers, managers | Tellers, RMs, IT admins, compliance |
| **Attack Vectors** | USB exfiltration | Customer data theft, unauthorized account access |

### Generation Methodology

Our synthetic data generation is grounded in established research:

| Step | Method | Research Basis |
|------|--------|---------------|
| Employee profiles | Stratified sampling by department/role | Organizational structure modeling |
| Normal activity sequences | Role-specific Markov chains | Le & Zincir-Heywood (2021) |
| Temporal distributions | Gaussian Mixture Models (GMM) | Yuan & Wu (2021) |
| Threat scenario injection | Perturbation of normal baselines | Glasser & Lindauer (2013) |
| Tabular feature preservation | CTGAN | Xu et al. (2019) |
| Noise & realism | Controlled randomization | Standard Monte Carlo methods |

### Employee Profile Distribution

```
200 Employees Total:
├── Retail Banking (60 employees)
│   ├── Relationship Managers (30)
│   ├── Tellers (20)
│   └── Branch Managers (10)
├── Treasury (25 employees)
│   ├── Traders (15)
│   └── Treasury Analysts (10)
├── IT Administration (35 employees)
│   ├── System Admins (15)
│   ├── DBA Admins (10)
│   └── Help Desk (10)
├── HR (30 employees)
│   ├── HR Generalists (15)
│   ├── Recruiters (10)
│   └── Payroll (5)
└── Compliance (50 employees)
    ├── AML Analysts (25)
    ├── Audit (15)
    └── Risk Officers (10)
```

### Normal Behavior Generation

For each role, we define a **Markov chain** of typical daily actions:

```python
# Example: Relationship Manager daily activity Markov chain
RM_TRANSITIONS = {
    "start_day": {"login": 1.0},
    "login": {"access_crm": 0.7, "read_email": 0.3},
    "access_crm": {"update_record": 0.4, "view_record": 0.3, "access_crm": 0.1, "read_email": 0.1, "break": 0.1},
    "view_record": {"access_crm": 0.5, "read_email": 0.2, "make_call": 0.2, "break": 0.1},
    "update_record": {"access_crm": 0.4, "view_record": 0.3, "read_email": 0.2, "break": 0.1},
    "read_email": {"send_email": 0.3, "access_crm": 0.3, "browse_web": 0.2, "break": 0.2},
    "send_email": {"read_email": 0.3, "access_crm": 0.4, "break": 0.3},
    "make_call": {"access_crm": 0.5, "update_record": 0.3, "break": 0.2},
    "browse_web": {"read_email": 0.3, "access_crm": 0.3, "browse_web": 0.2, "break": 0.2},
    "break": {"access_crm": 0.3, "read_email": 0.3, "browse_web": 0.2, "logout": 0.2},
    "logout": {"end_day": 1.0},
}

# Temporal parameters (GMM)
RM_TEMPORAL = {
    "login_time": GaussianMixture(means=[9.25], stds=[0.2]),  # 09:15 ± 12 min
    "logout_time": GaussianMixture(means=[18.5], stds=[0.4]), # 18:30 ± 24 min
    "session_actions": Poisson(lambda_=45),                    # ~45 actions/day
    "email_volume": Poisson(lambda_=8),                        # ~8 emails/day
    "records_accessed": Poisson(lambda_=50),                   # ~50 records/day
}
```

### Threat Scenario Injection

We inject **6 banking-specific attack scenarios** into 15-20 employees (7.5-10% insider rate):

#### Scenario 1: Bulk Customer Data Exfiltration
```
Week 1-3: Normal behavior (building baseline)
Week 4:   Increase in records accessed (2× normal)
Week 5:   Further increase (5× normal)
Week 6:   After-hours login + USB connect + 15× data volume + file copy
```

**Perturbation Parameters**:
```python
{
    "data_volume_multiplier": 15.0,
    "after_hours_probability": 0.8,
    "usb_connect_probability": 0.9,
    "ramp_up_weeks": 3,
    "attack_window_days": 3,
}
```

#### Scenario 2: Unauthorized Account Snooping
```
HR employee starts accessing customer financial records.
Gradual — 2-3 records per week initially, growing to 20/day.
No data exfiltration — just viewing/reading.
```

#### Scenario 3: Privilege Escalation Abuse
```
IT admin uses superadmin credentials on production CBS.
Accesses audit logs (potential evidence tampering).
Creates new admin account (persistence).
```

#### Scenario 4: Pre-Resignation Data Theft
```
Week 1-2: Job search browsing (LinkedIn, Indeed)
Week 3:   Increased file downloads
Week 4:   Bulk email to personal address with attachments
Week 5:   Last working day
```

#### Scenario 5: Credential Compromise
```
Day 1: Normal login from Mumbai at 09:15
Day 1: Second login from Delhi at 09:47 (impossible travel)
Day 2: Rapid system switching (CBS → Treasury → Admin Console)
Day 3: Data access outside normal role scope
```

#### Scenario 6: Slow-Burn Reconnaissance
```
Month 1: Accesses 1 new system (outside normal scope)
Month 2: Accesses 3 new systems
Month 3: Accesses 5 new systems + increased data volume
Each individual action looks benign — pattern only visible over weeks.
```

### Generated Data Schema

#### `employees.csv`
```csv
emp_id,name,department,role,clearance_level,branch,tenure_months,hire_date
EMP_001,Raj Sharma,retail_banking,relationship_manager,3,mumbai_main,36,2022-06-15
```

#### `activity_log.csv`
```csv
timestamp,emp_id,action_type,system,resource,records_accessed,data_volume_mb,device_id,ip_address,is_after_hours,is_new_device,geo_location
2025-06-15T14:23:45,EMP_001,data_access,CBS,customer_records,12,2.3,WS_MUM_042,10.1.42.15,False,False,mumbai
```

#### `ground_truth.csv`
```csv
emp_id,is_insider,scenario,attack_start_date,attack_end_date,description
EMP_047,True,data_exfiltration,2025-08-01,2025-08-15,Bulk customer data download and USB exfiltration
```

### Generated Dataset Statistics (Target)

| Metric | Value |
|--------|-------|
| **Employees** | 200 |
| **Duration** | 90 days |
| **Total activity events** | ~1.8M (200 × 45 actions/day × 90 days × variance) |
| **Departments** | 5 |
| **Unique roles** | 12 |
| **Insider employees** | 15-20 (7.5-10%) |
| **Attack scenarios** | 6 types |
| **Feature vectors** | 18,000 (200 employees × 90 days) |

---

## Feature Engineering Pipeline

### 47 Features — 8 Categories

#### Category 1: Temporal Features (8)

| # | Feature | Type | Description | Source |
|---|---------|------|-------------|--------|
| 1 | `login_hour` | float | Hour of first login (0-24) | logon.csv |
| 2 | `logout_hour` | float | Hour of last logout (0-24) | logon.csv |
| 3 | `session_duration_hrs` | float | Total session time in hours | logon.csv |
| 4 | `is_weekend` | binary | 1 if Saturday/Sunday, 0 otherwise | timestamp |
| 5 | `is_after_hours` | binary | 1 if any activity outside 9:00-18:00 | logon.csv |
| 6 | `time_since_last_session` | float | Hours since previous session end | logon.csv |
| 7 | `login_regularity_score` | float | Cosine similarity of login time to historical average | computed |
| 8 | `temporal_entropy` | float | Shannon entropy of hourly event distribution | computed |

#### Category 2: Access Volume Features (7)

| # | Feature | Type | Description | Source |
|---|---------|------|-------------|--------|
| 9 | `files_accessed` | int | Number of file operations | file.csv |
| 10 | `emails_sent` | int | Emails sent | email.csv |
| 11 | `emails_received` | int | Emails received | email.csv |
| 12 | `urls_visited` | int | Web pages accessed | http.csv |
| 13 | `usb_events` | int | USB connect/disconnect count | device.csv |
| 14 | `data_volume_mb` | float | Total data transferred (MB) | computed |
| 15 | `unique_systems_accessed` | int | Distinct systems/PCs used | logon.csv |

#### Category 3: Device & Location Features (5)

| # | Feature | Type | Description | Source |
|---|---------|------|-------------|--------|
| 16 | `is_new_device` | binary | 1 if device never used before | device history |
| 17 | `device_count` | int | Number of distinct devices used today | logon.csv |
| 18 | `unique_pcs` | int | Number of unique PCs logged into | logon.csv |
| 19 | `geo_anomaly_flag` | binary | 1 if impossible travel detected | IP analysis |
| 20 | `vpn_usage` | binary | 1 if VPN connection detected | logon.csv |

#### Category 4: Communication Features (6)

| # | Feature | Type | Description | Source |
|---|---------|------|-------------|--------|
| 21 | `external_email_ratio` | float | External emails / total emails | email.csv |
| 22 | `avg_attachment_size` | float | Average attachment size (KB) | email.csv |
| 23 | `unique_recipients` | int | Distinct email recipients | email.csv |
| 24 | `cc_bcc_ratio` | float | CC+BCC recipients / total recipients | email.csv |
| 25 | `email_content_sentiment` | float | Sentiment score of email content (-1 to 1) | NLP analysis |
| 26 | `unusual_recipient_flag` | binary | 1 if new external recipient | email history |

#### Category 5: Data Movement Features (7)

| # | Feature | Type | Description | Source |
|---|---------|------|-------------|--------|
| 27 | `file_copy_count` | int | File copy operations | file.csv |
| 28 | `usb_file_transfers` | int | Files transferred to USB | device+file |
| 29 | `large_download_flag` | binary | 1 if any download > threshold | computed |
| 30 | `sensitive_file_access` | int | Access to sensitive/classified files | file.csv |
| 31 | `data_egress_volume` | float | Outbound data transfer (MB) | computed |
| 32 | `print_count` | int | Print jobs submitted | computed |
| 33 | `cloud_upload_count` | int | Cloud storage uploads | http.csv |

#### Category 6: Behavioral Ratio Features (6)

| # | Feature | Type | Description | Source |
|---|---------|------|-------------|--------|
| 34 | `access_to_role_ratio` | float | Actual access / expected for role | role baseline |
| 35 | `peer_deviation_score` | float | Z-score vs. peer group average | peer analysis |
| 36 | `weekday_vs_weekend_ratio` | float | Weekday activity / weekend activity | temporal |
| 37 | `morning_vs_evening_ratio` | float | AM events / PM events | temporal |
| 38 | `productive_vs_idle_ratio` | float | Active time / session time | computed |
| 39 | `command_diversity_index` | float | Shannon entropy of action types | computed |

#### Category 7: Sequence Features (8)

| # | Feature | Type | Description | Source |
|---|---------|------|-------------|--------|
| 40 | `action_sequence_entropy` | float | Entropy of the action type sequence | computed |
| 41 | `longest_unusual_chain` | int | Longest subsequence of unusual actions | computed |
| 42 | `role_boundary_crossings` | int | Count of cross-role resource accesses | role matrix |
| 43 | `privilege_escalation_count` | int | Privilege level increases | access logs |
| 44 | `session_action_diversity` | float | Unique action types / total actions | computed |
| 45 | `repeat_pattern_score` | float | Autocorrelation of action sequence | computed |
| 46 | `novelty_score` | float | Fraction of never-before-seen actions | history |
| 47 | `behavioral_velocity` | float | Rate of change in rolling feature means | computed |

---

## Train/Validation/Test Split Strategy

### For CERT Data

```
Timeline split (respects temporal ordering):
├── Train:  Months 1-12  (normal employees ONLY — no insiders)
├── Val:    Months 13-15 (mixed — for threshold tuning)
└── Test:   Months 16-18 (mixed — final evaluation)
```

### For Synthetic Banking Data

```
Timeline split:
├── Train:  Days 1-60  (normal employees ONLY)
├── Val:    Days 61-75 (mixed — includes ramp-up of some threats)
└── Test:   Days 76-90 (mixed — includes active threat scenarios)
```

### Class Balance

| Split | Normal Employee-Days | Insider Employee-Days | Ratio |
|-------|---------------------|----------------------|-------|
| Train | ~10,800 | 0 (excluded) | N/A — one-class learning |
| Val | ~2,700 | ~225 | 12:1 |
| Test | ~2,700 | ~225 | 12:1 |

---

## Data Quality Checks

Before training, we validate:

1. **No future leakage**: Features only use past/current data, never future
2. **No label leakage**: No features that directly encode the insider label
3. **Temporal consistency**: All timestamps are monotonically increasing per user
4. **Feature distributions**: No NaN, no infinite values, reasonable ranges
5. **Ground truth alignment**: Insider labels match expected scenario timelines
6. **Class balance verification**: Insider ratio matches expected 7.5-10%
