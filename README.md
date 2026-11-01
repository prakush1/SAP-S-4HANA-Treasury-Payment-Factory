# 🏛️ SAP S/4HANA Treasury Payment Factory & In-House Banking Platform
### Architected & Developed by **Prakush Shende** — Senior SAP TRM & Corporate Treasury Solution Architect

[![SAP S/4HANA](https://img.shields.io/badge/SAP-S%2F4HANA_2026-0a6ed1?logo=sap&logoColor=white)](https://sap.com)
[![ISO 20022](https://img.shields.io/badge/ISO_20022-pain.001%20%7C%20pain.002%20%7C%20camt.053-blue)](https://www.iso20022.org)
[![SWIFT gpi](https://img.shields.io/badge/SWIFT_gpi-UETR_Tracking_RFC_4122-success)](https://www.swift.com)
[![AI Governance](https://img.shields.io/badge/AI_Governance-SOX_404_%7C_EU_AI_Act_Killswitch-red)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.54_Cloud_Ready-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)

---

## 📌 Executive Summary: The Business Challenge & The Solution

In large global enterprises, subsidiaries often operate in silos—maintaining hundreds of redundant external commercial bank accounts. This decentralization leads to:
* **Exorbitant cross-border wire transfer and FX conversion fees.**
* **Fragmented cash liquidity** trapped across global subsidiaries.
* **Insecure, manual payment approvals** vulnerable to Business Email Compromise (BEC) and invoice tampering.

### The Solution:
This platform demonstrates a **centralized S/4HANA Corporate Treasury Payment Factory**:
1. **In-House Banking (IHC/IHB):** Subsidiaries close external accounts and open virtual accounts with the central corporate headquarters.
2. **Payment-on-Behalf-Of (POBO):** Corporate Treasury settles external vendor invoices out of a central corporate bank account, eliminating cross-border banking fees.
3. **Bank Communication Management (BCM):** Enforces multi-tier digital sign-offs, payment batching, and automated approval workflows before files leave SAP.
4. **SAP Multi-Bank Connectivity (MBC):** Securely transmits ISO 20022 XML (`pain.001`) with mandatory **SWIFT UETR** tracking directly to banking networks.
5. **AI Treasury Governance & Killswitch:** An algorithmic anomaly shield that flags unauthorized IBAN changes, accompanied by an emergency **AI Killswitch** to enforce strict human control pursuant to SOX 404 and EU AI Act standards.

---

## 🗺️ Interactive End-to-End Architecture Flow

```text
┌─────────────────────────────────┐
│  1. Subsidiary Payment Run      │  • Fiori: Manage Automatic Payments (F110 / F111)
│     (Originating Company Code)  │  • Engine: SAPFPAYM | Tables: REGUH, REGUP
│                                 │  • Action: Clears Vendor AP; routes offset to IHC Clearing
└─────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  2. In-House Banking (IHC)      │  • Cockpit: In-House Banking Ledger (IHC0)
│     (Central Corporate Bank)    │  • Engine: IHC_EOD_JOB | Tables: IHC_DB_PN, IHC_DB_ACCT
│                                 │  • Action: Debits Sub virtual account; routes POBO via HQ
└─────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  3. BCM Approval Cockpit        │  • Cockpit: Manage Payment Batches (BNK_MONI)
│     (Sign-off Matrix Policy)    │  • Engine: RBNK_BATCH_CREATE | Tables: BNK_BATCH, SWWWIHEAD
│                                 │  • Action: 1-tier, 2-tier (Dual Signer), or 3-tier (CFO) release
└─────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  4. SAP MBC / SWIFT Engine      │  • Connector: Track Payments (/BSNAGT/MONITOR)
│     (ISO 20022 & SWIFT gpi)     │  • Engine: SSF Certificate Encryption | Table: /BSNAGT/MESSAGES
│                                 │  • Payload: pain.001.001.03 XML with RFC 4122 UUIDv4 UETR
└─────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  5. Bank Feedback & EBS Clear   │  • Engine: Process Electronic Bank Statements (FEB_BSPROC)
│     (Automated Reconciliation)  │  • Payloads: pain.002 (ACK/NACK) & camt.053 (End of Day Statement)
│                                 │  • Action: Automated ACDOCA Reversal if bank rejects (e.g. AC04)
└─────────────────────────────────┘
```

---

## 🌟 Interactive Features Walkthrough (Inside the Application)

### 1. 🤖 AI Treasury Anomaly Shield & Emergency Killswitch
* **Defensible Machine Learning (XGBoost / Isolation Forest):** Continuously screens payments before BCM batch release across 4 feature vectors:
  * **Vendor IBAN Change Velocity:** Checks table `LFBK` / BP master data. If an account was changed within 30 days, anomaly risk spikes.
  * **Amount $Z$-Score:** Flags payments that deviate $> 3$ standard deviations from the rolling 12-month mean.
  * **Sanctions Fuzzy-Matching Index:** Real-time screening against OFAC/EU sanctions lists.
  * **Prescriptive Liquidity Routing:** Calculates fee savings for In-House Cash POBO vs. external wires.
* **Interactive IBAN Tampering Simulation:** Click **`🚨 Simulate Vendor IBAN Tampering Attack`** to watch the Fraud Index spike to **94% (CRITICAL ALERT)** and automatically quarantine the payment in status `09`.
* **🚨 Emergency AI Killswitch:** Toggle the killswitch in the sidebar to hard-freeze autonomous operations, satisfying **SOX 404 and EU AI Act** human-in-the-loop audit requirements.

### 2. 🌐 SWIFT gpi UETR Tracking (RFC 4122 Compliant)
* Generates a 36-character **RFC 4122 Version 4 UUID** (e.g., `eb6303c1-b778-4c16-8c45-46eb610185a3`).
* Injected into ISO 20022 XML tag `<CdtTrfTxInf> -> <PmtId> -> <UETR>` and stored in SAP field `REGUH-UETR`.
* **Live 4-Hop Telemetry Timeline:** Visualizes payment progress across **Citibank NY** $\rightarrow$ **Deutsche Bank** $\rightarrow$ **Commerzbank** $\rightarrow$ **Beneficiary Account Credited** (77-second total settlement).

### 3. 🎯 7 Real-Time Enterprise Scenarios
Switch scenarios live in the sidebar to observe real-time system responses:
1. **Scenario 1: Happy Path (Standard POBO EUR 125,000):** Normal POBO execution, dual approval, and bank acceptance.
2. **Scenario 2: High-Value Flow ($1,500,000 USD):** Triggers the multi-tier sign-off policy requiring Treasury Director and CFO authorizations.
3. **Scenario 3: Bank Rejection & Auto-Rollback (`pain.002` AC04):** Simulates an external bank rejection for a closed account number. BCM marks the batch `Partially Rejected` and posts an automated reversal document in `ACDOCA` to reopen the vendor open item.
4. **Scenario 4: Insufficient Funds Exception (`pain.002` AM04):** Bank NACK triggered by liquidity shortfall.
5. **Scenario 5: Multilateral Intercompany Netting:** Internal settlement offsetting reciprocal debts across 3 subsidiaries with zero external banking fees.
6. **Scenario 6: Cross-Border FX Hedged Settlement:** Cross-currency POBO (EUR $\rightarrow$ JPY) linking to TRM FX Forward deal Product `60A` (`VTBFHA`).
7. **Scenario 7: Bank Sanctions / AML Compliance Review (`pain.002` PDNG):** Simulates a clearing house hold for compliance screening.

### 4. ⚙️ SPRO Configuration Sandbox (Dynamic Rules Editor)
* **Approval Threshold Slider:** Shift the limit from $\$10\text{k}$ to $\$1,000,000$ to watch BCM re-evaluate release rules live.
* **Release Policy Selector:** Toggle between *Single Signer*, *Dual Signer*, and *3-Tier Board Sign-off*.
* **Batch Grouping Rules:** Switch criteria (*Company Code + Currency* vs. *House Bank* vs. *Payment Method*).
* **Disbursement Engine:** Toggle between *In-House Cash (POBO)* and *Direct External House Bank Disbursal*.

### 5. 📑 Universal Journal (`ACDOCA`) Ledgers
* Displays balanced Debit/Credit postings across **Subsidiary Ledger (CoCode 2000)** and **Central Corporate Treasury (CoCode 1000)** with real SAP posting keys (`25`, `50`, `40`, `31`).
* Generates offsetting reversal journal entries upon bank rejection.
* One-click export to CSV.

### 6. 📚 Treasury Knowledge Base & Glossary
An embedded encyclopedia covering:
* **Corporate Treasury Concepts:** POBO, COBO, Multilateral Netting, Cash Pooling (ZBA vs Notional).
* **SAP Technical Objects:** `ACDOCA`, `REGUH`, `REGUP`, `BNK_BATCH`, `FEB_BSPROC`, `DMEEX`.
* **ISO 20022 Standards:** `pain.001`, `pain.002`, `camt.053`, `camt.054`, SWIFT UETR, and ISO error codes (`AC04`, `AM04`, `BE04`, `AG01`).

---

## 📂 Project Structure

```text
sap-treasury-payment-factory/
├── .streamlit/
│   └── config.toml          # Streamlit UI theme and headless server configuration
├── app.py                   # Main enterprise application and UI logic
├── test_app.py              # Automated unit and integration test suite
├── e2e_server_check.py      # E2E localhost health check script
├── requirements.txt         # Production dependencies for cloud deployment
├── .gitignore               # Excludes bytecode and temporary artifacts
└── README.md                # Enterprise solution documentation and architecture guide
```

---

## 🚀 Running Locally (100% Offline)

### Prerequisites
* Python 3.9 or higher installed

### Step-by-Step
1. Clone the repository and navigate into the project directory:
   ```bash
   git clone https://github.com/prakush1/SAP-S-4HANA-Treasury-Payment-Factory.git
   cd SAP-S-4HANA-Treasury-Payment-Factory
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the automated test suite to verify system integrity:
   ```bash
   python -m unittest test_app.py
   ```
4. Launch the application:
   ```bash
   streamlit run app.py
   ```
5. Open your browser at **`http://localhost:8501`**.

---

## ☁️ Free Cloud Deployment to Streamlit Community Cloud

Deploy this project on the web for free in under 2 minutes:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Update README and documentation"
   git push -u origin main
   ```
2. **Deploy on Streamlit Cloud:**
   * Go to **[share.streamlit.io](https://share.streamlit.io/)** and log in with GitHub.
   * Click **"New App"**.
   * Select your repository: `prakush1/SAP-S-4HANA-Treasury-Payment-Factory`, branch: `main`, file: `app.py`.
   * Click **"Deploy"**.
   * You will receive a permanent, public cloud URL (e.g., `https://sap-s-4hana-treasury-payment-factory.streamlit.app`).

---

## 🎙️ Executive Interview Pitch

> *"During our corporate treasury blueprint workshops, I architected this functional prototype to bridge the gap between business stakeholders and technical SAP teams. 
> 
> It models the complete payment lifecycle: from subsidiary POBO origination in `REGUH` and dynamic BCM sign-off matrices in `BNK_BATCH`, down to ISO 20022 `pain.001` XML generation with SWIFT UETRs and balancing lines in `ACDOCA`. 
> 
> Crucially, it demonstrates both happy-path routing and exception handling—including bank `pain.002` rejections (like `AC04` Closed Account) that automatically flip batch statuses and trigger offsetting reversal documents without manual intervention.
>
> Furthermore, it incorporates an AI Treasury Anomaly Shield and an emergency AI Killswitch to demonstrate compliance with internal audit, SOX 404, and human-in-the-loop oversight."*

---

<div align="center">
    <b>S/4HANA Treasury Payment Factory & In-House Banking Architecture Platform</b><br>
    Architected, Designed & Developed by <b>Prakush Shende</b> — Senior SAP TRM & Corporate Treasury Solution Architect<br>
    Built with SAP S/4HANA 2026 Best Practices, ISO 20022 Global Standards, BCM Frameworks & AI Governance Controls.
</div>
