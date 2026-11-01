# 🏛️ S/4HANA Treasury Payment Factory & In-House Banking Architecture Platform
### Architected & Developed by **Prakush Shende** — Senior SAP TRM & Corporate Treasury Solution Architect

An interactive, enterprise-grade architecture platform modeling **SAP S/4HANA In-House Banking (IHB/IHC)**, **Bank Communication Management (BCM)**, **SAP Multi-Bank Connectivity (MBC)**, **ISO 20022 XML Messaging**, and **AI Treasury Governance**.

---

## 🌟 Architecture & Capabilities

1. **Enterprise Flow & Backend Execution Map:**
   * Visual tracking across 5 lifecycle stages: *Subsidiary AP (`F110`/`F111`) $\rightarrow$ In-House Bank (`IHC0`) $\rightarrow$ BCM Batching & Approvals (`BNK_MONI`) $\rightarrow$ Multi-Bank Connectivity & SWIFT $\rightarrow$ EBS Auto-Reconciliation (`FEB_BSPROC`)*.
   * Telemetry inspector detailing ABAP programs (`SAPFPAYM`, `RFEBKA00`), database tables (`REGUH`, `REGUP`, `BNK_BATCH`, `ACDOCA`), and interface payloads at each stage.
2. **7 Comprehensive Enterprise Scenarios:**
   * **Scenario 1:** Standard POBO Happy Path (EUR 125,000).
   * **Scenario 2:** High-Value Dual-Signoff Flow ($1,500,000 USD).
   * **Scenario 3:** Bank Rejection & Auto-Rollback (`pain.002` NACK with ISO code `AC04` Closed Account).
   * **Scenario 4:** Insufficient Funds Exception (`pain.002` NACK with code `AM04`).
   * **Scenario 5:** Multilateral Intercompany Netting (Settling 3 subsidiaries with zero external bank fees).
   * **Scenario 6:** Cross-Border FX Hedged Settlement (EUR $\rightarrow$ JPY linking to TRM FX Forward deal `60A`).
   * **Scenario 7:** Bank Sanctions / AML Compliance Review (`pain.002` `PDNG` Hold).
3. **AI Treasury Governance & Anomaly Detection (with Emergency Killswitch):**
   * Machine learning anomaly detection across 4 feature vectors: Master data changes in `LFBK`, Amount $Z$-scores, Sanctions fuzzy-matching, and Cost-optimal routing.
   * **Emergency AI Killswitch:** Hard-freezes autonomous machine routing pursuant to SOX 404 and EU AI Act regulations, enforcing strict human dual-authorization.
   * Interactive IBAN tampering simulation demonstrating automated batch quarantining.
4. **SWIFT gpi Tracking & ISO 20022 Engine:**
   * Validated RFC 4122 Version 4 UUID for SWIFT `UETR` tracking.
   * Dynamic generation of ISO 20022 `pain.001.001.03` XML and `camt.053` electronic bank statements.
   * Real-time 4-hop correspondent banking telemetry across Citibank NY, Deutsche Bank, and Commerzbank.
5. **Dynamic SPRO Configuration Sandbox:**
   * Live slider to modify the **Dual-Approval Threshold** ($10k – $1M).
   * Real-time toggles for **Sign-off Policies** (*Single Signer*, *Dual Signer*, *3-Tier Board Approval*), **Batch Grouping Keys**, and **Disbursement Routing Models**.
6. **Universal Journal (`ACDOCA`) & Reversals:**
   * Real-time balanced Debit/Credit postings across subsidiary and corporate ledgers, with automated reversal documents on bank failure.
7. **Treasury Knowledge Base (Glossary):**
   * Reference guide covering corporate treasury business concepts (POBO, COBO, Netting, ZBA), SAP architecture objects (`ACDOCA`, `REGUH`, `DMEEX`), and ISO 20022 banking standards (`pain.001`, `pain.002`, `camt.053`, SWIFT UETR).

---

## 📂 Project Structure

```text
sap-treasury-simulator/
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

```powershell
cd "C:\Users\HP\.gemini\antigravity\scratch\sap-treasury-simulator"

# 1. Run automated test suite:
python -m unittest test_app.py

# 2. Launch the app locally:
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## ☁️ Free Cloud Deployment to GitHub & Streamlit Community Cloud

### Step 1: Push to GitHub
```bash
cd "C:\Users\HP\.gemini\antigravity\scratch\sap-treasury-simulator"
git init
git add .
git commit -m "S/4HANA Treasury Simulator by Prakush Shende"
git branch -M main
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/sap-treasury-simulator.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Community Cloud (Free Forever)
1. Go to **[share.streamlit.io](https://share.streamlit.io/)** and log in with your GitHub account.
2. Click **"New App"**.
3. Fill in the deployment form:
   * **Repository:** `<YOUR_GITHUB_USERNAME>/sap-treasury-simulator`
   * **Branch:** `main`
   * **Main file path:** `app.py`
4. Click **"Deploy"**.
5. Within 90 seconds, you will receive your live, public cloud URL (e.g., `https://sap-treasury-simulator.streamlit.app`).

---

## 🎙️ Executive Interview Pitch

> *"During our corporate treasury blueprint workshops, I architected this functional prototype to bridge the gap between business stakeholders and technical SAP teams. 
> 
> It models the complete payment lifecycle: from subsidiary POBO origination in `REGUH` and dynamic BCM sign-off matrices in `BNK_BATCH`, down to ISO 20022 `pain.001` XML generation with SWIFT UETRs and balancing lines in `ACDOCA`. 
> 
> Crucially, it demonstrates both happy-path routing and exception handling—including bank `pain.002` rejections (like `AC04` Closed Account) that automatically flip batch statuses and trigger offsetting reversal documents without manual intervention.
>
> Furthermore, it incorporates an AI Treasury Anomaly Shield and an emergency AI Killswitch to demonstrate compliance with internal audit, SOX 404, and human-in-the-loop oversight."*
