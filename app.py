import streamlit as st
import pandas as pd
import uuid
import time
from datetime import datetime
import io

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="SAP S/4HANA Treasury Platform | Prakush Shende",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# HIGH-END CSS: GLOWS, PULSES & ANIMATIONS
# ==========================================
st.markdown("""
<style>
    @keyframes pulse-green {
        0% { box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.6); }
        70% { box-shadow: 0 0 0 10px rgba(40, 167, 69, 0); }
        100% { box-shadow: 0 0 0 0 rgba(40, 167, 69, 0); }
    }
    @keyframes pulse-red {
        0% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.7); }
        70% { box-shadow: 0 0 0 12px rgba(220, 53, 69, 0); }
        100% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0); }
    }
    .hero-banner {
        background: radial-gradient(circle at 10% 20%, #0d1b2a, #1b263b 90%);
        border: 2px solid #00b4d8;
        border-radius: 14px;
        padding: 24px 32px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0, 180, 216, 0.15);
    }
    .author-highlight {
        background: linear-gradient(90deg, #ffd166, #06d6a0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 28px;
        font-weight: 900;
        letter-spacing: 0.5px;
        display: inline-block;
    }
    .architect-badge {
        background: rgba(0, 180, 216, 0.18);
        border: 1px solid #00b4d8;
        color: #90e0ef;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
        margin-bottom: 8px;
    }
    .ai-killswitch-active {
        background: linear-gradient(135deg, #49111c, #7f1d1d);
        border: 2px solid #ef4444;
        color: #fecaca;
        padding: 16px 20px;
        border-radius: 10px;
        animation: pulse-red 2s infinite;
        margin-bottom: 16px;
    }
    .ai-copilot-normal {
        background: linear-gradient(135deg, #0b2545, #134074);
        border: 1px solid #00b4d8;
        color: #e0fbfc;
        padding: 16px 20px;
        border-radius: 10px;
        margin-bottom: 16px;
    }
    .sap-status-pill {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .pill-approved { background-color: #10b981; color: white; animation: pulse-green 2.5s infinite; }
    .pill-pending { background-color: #f59e0b; color: white; }
    .pill-rejected { background-color: #ef4444; color: white; animation: pulse-red 2s infinite; }
    .pill-hold { background-color: #6b7280; color: white; }
    div[data-testid="stMetricValue"] {
        font-size: 22px !important;
        font-weight: 800 !important;
        color: #0077b6 !important;
    }
    .stButton>button {
        transition: all 0.25s ease-in-out;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE & AI CO-PILOT MANAGEMENT
# ==========================================
def sync_scenario():
    sc = st.session_state.current_scenario
    st.session_state.uetr = str(uuid.uuid4())
    st.session_state.reversal_posted = False
    
    if "Happy Path" in sc:
        st.session_state.batch_status = "04 (Fully Approved)"
        st.session_state.signer1_approved = True
        st.session_state.signer2_approved = True
        st.session_state.signer3_approved = False
        st.session_state.bank_response = "ACCP (Accepted by Bank)"
        st.session_state.ai_fraud_score = 3
    elif "High-Value" in sc:
        st.session_state.batch_status = "02 (In Approval - Step 2)"
        st.session_state.signer1_approved = True
        st.session_state.signer2_approved = False
        st.session_state.signer3_approved = False
        st.session_state.bank_response = "Pending Approval"
        st.session_state.ai_fraud_score = 12
    elif "AC04" in sc:
        st.session_state.batch_status = "08 (Partially Rejected)"
        st.session_state.signer1_approved = True
        st.session_state.signer2_approved = True
        st.session_state.bank_response = "RJCT (Rejected: AC04 Closed Account)"
        st.session_state.reversal_posted = True
        st.session_state.ai_fraud_score = 88
    elif "AM04" in sc:
        st.session_state.batch_status = "08 (Partially Rejected)"
        st.session_state.signer1_approved = True
        st.session_state.signer2_approved = True
        st.session_state.bank_response = "RJCT (Rejected: AM04 Insufficient Funds)"
        st.session_state.reversal_posted = True
        st.session_state.ai_fraud_score = 45
    elif "Netting" in sc:
        st.session_state.batch_status = "04 (Netting Settled Internally)"
        st.session_state.signer1_approved = True
        st.session_state.signer2_approved = True
        st.session_state.bank_response = "N/A (Zero External Bank Flow)"
        st.session_state.ai_fraud_score = 1
    elif "FX Hedged" in sc:
        st.session_state.batch_status = "04 (Fully Approved - Hedged)"
        st.session_state.signer1_approved = True
        st.session_state.signer2_approved = True
        st.session_state.bank_response = "ACCP (Settled via FX Deal 60A)"
        st.session_state.ai_fraud_score = 5
    elif "PDNG" in sc:
        st.session_state.batch_status = "07 (Transmitted to Bank)"
        st.session_state.signer1_approved = True
        st.session_state.signer2_approved = True
        st.session_state.bank_response = "PDNG (Pending: Bank AML Review)"
        st.session_state.ai_fraud_score = 76

# Defaults
if "current_scenario" not in st.session_state:
    st.session_state.current_scenario = "Scenario 1: Happy Path (Standard POBO EUR 125k)"
if "batch_status" not in st.session_state:
    st.session_state.batch_status = "04 (Fully Approved)"
if "signer1_approved" not in st.session_state:
    st.session_state.signer1_approved = True
if "signer2_approved" not in st.session_state:
    st.session_state.signer2_approved = True
if "signer3_approved" not in st.session_state:
    st.session_state.signer3_approved = False
if "bank_response" not in st.session_state:
    st.session_state.bank_response = "ACCP (Accepted by Bank)"
if "uetr" not in st.session_state:
    st.session_state.uetr = str(uuid.uuid4())
if "reversal_posted" not in st.session_state:
    st.session_state.reversal_posted = False

# AI Killswitch & Anomaly Variables
if "ai_killswitch_active" not in st.session_state:
    st.session_state.ai_killswitch_active = False
if "ai_fraud_score" not in st.session_state:
    st.session_state.ai_fraud_score = 4
if "iban_tampered" not in st.session_state:
    st.session_state.iban_tampered = False
if "cfg_threshold" not in st.session_state:
    st.session_state.cfg_threshold = 100000.0
if "cfg_policy" not in st.session_state:
    st.session_state.cfg_policy = "Dual Signer (Analyst + Director)"
if "cfg_grouping" not in st.session_state:
    st.session_state.cfg_grouping = "Company Code + Currency"
if "cfg_routing" not in st.session_state:
    st.session_state.cfg_routing = "In-House Cash (POBO)"

# ==========================================
# SIDEBAR CONTROLS & ARCHITECT CARD
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/sap.png", width=64)
    
    # UNMISSABLE BRANDING IN SIDEBAR
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0d1b2a, #1e3a8a); border: 2px solid #38bdf8; border-radius: 12px; padding: 18px; color:white; margin-bottom: 20px;">
        <div style="font-size:11px; text-transform:uppercase; letter-spacing:1px; color:#7dd3fc; font-weight:700;">Chief Architect & Author</div>
        <div style="font-size:20px; font-weight:900; color:#facc15; margin: 4px 0;">PRAKUSH SHENDE</div>
        <div style="font-size:12px; color:#e0e7ff; line-height:1.4;">Lead Enterprise Architect — SAP TRM, Payment Factory & Bank Integration</div>
        <hr style="border-color: rgba(255,255,255,0.2); margin: 10px 0;">
        <div style="font-size:11px; color:#bae6fd;">
            ✔ S/4HANA Treasury Subledger<br>
            ✔ In-House Banking & Netting<br>
            ✔ BCM Multi-Tier Sign-off<br>
            ✔ ISO 20022 & SWIFT gpi Architect<br>
            ✔ AI Treasury Governance & Control
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🎯 Enterprise Scenarios")
    all_scenarios = [
        "Scenario 1: Happy Path (Standard POBO EUR 125k)",
        "Scenario 2: High-Value Flow ($1.5M USD Dual-Signoff)",
        "Scenario 3: Bank Rejection & Auto-Rollback (pain.002 AC04)",
        "Scenario 4: Insufficient Funds Exception (pain.002 AM04)",
        "Scenario 5: Multilateral Intercompany Netting (Zero External Fee)",
        "Scenario 6: Cross-Border FX Hedged Settlement (EUR -> JPY)",
        "Scenario 7: Bank Sanctions / AML Compliance Hold (pain.002 PDNG)"
    ]
    
    scenario = st.selectbox(
        "Select Active Business Scenario",
        all_scenarios,
        key="current_scenario",
        on_change=sync_scenario
    )

    st.markdown("---")
    st.subheader("🤖 AI Treasury Governance")
    
    # AI KILLSWITCH TOGGLE
    killswitch = st.toggle(
        "🚨 ENGAGE AI KILLSWITCH",
        value=st.session_state.ai_killswitch_active,
        help="Emergency Governance Override: Immediately freezes all autonomous AI auto-approvals, revokes machine routing, and forces strict 4-eyes manual audit."
    )
    if killswitch != st.session_state.ai_killswitch_active:
        st.session_state.ai_killswitch_active = killswitch
        if killswitch:
            st.toast("🚨 EMERGENCY AI KILLSWITCH ENGAGED! Autonomous approvals revoked.", icon="🛑")
        else:
            st.toast("✅ AI Autonomous Pilot Restored under SOX controls.", icon="🤖")
        st.rerun()

    st.markdown("---")
    st.caption("Platform Version: S/4HANA 2026.4 Enterprise | ISO 20022 Release 2026")
    if st.button("🔄 Reset Entire Workspace"):
        st.session_state.signer1_approved = False
        st.session_state.signer2_approved = False
        st.session_state.signer3_approved = False
        st.session_state.batch_status = "02 (In Approval)"
        st.session_state.bank_response = "Pending Transmission"
        st.session_state.uetr = str(uuid.uuid4())
        st.session_state.reversal_posted = False
        st.session_state.ai_killswitch_active = False
        st.session_state.ai_fraud_score = 4
        st.rerun()

# ==========================================
# UNMISSABLE EXECUTIVE HERO BANNER
# ==========================================
st.markdown("""
<div class="hero-banner">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
        <div>
            <span class="architect-badge">⚡ S/4HANA 2026 Enterprise Architecture Showcase</span>
            <div style="margin: 4px 0;">
                <span style="font-size:16px; color:#e0e7ff; font-weight:600;">DESIGNED, ARCHITECTED & DEVELOPED BY</span><br>
                <span class="author-highlight">PRAKUSH SHENDE</span>
            </div>
            <div style="font-size:14px; color:#bae6fd; font-weight:500;">
                Senior SAP S/4HANA TRM & Corporate Treasury Solution Architect
            </div>
        </div>
        <div style="background: rgba(0,0,0,0.35); border: 1px solid rgba(255,255,255,0.2); padding: 12px 20px; border-radius: 10px; text-align:right;">
            <div style="font-size:11px; text-transform:uppercase; color:#94a3b8; letter-spacing:1px;">Architecture Scope</div>
            <div style="font-size:13px; color:#ffffff; font-weight:700; margin-top:2px;">In-House Banking • BCM • MBC • ISO 20022 • AI Governance</div>
            <div style="font-size:11px; color:#38bdf8; margin-top:4px;">Validated Against SAP S/4HANA 2026 Subledger Standards</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# AI KILLSWITCH & COPILOT ENGINE DISPLAY
# ==========================================
if st.session_state.ai_killswitch_active:
    st.markdown("""
    <div class="ai-killswitch-active">
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">
            <div>
                <strong style="font-size:17px;">🚨 EMERGENCY AI KILLSWITCH ACTIVE — STRICT HUMAN GOVERNANCE OVERRIDE</strong><br>
                <span style="font-size:13px;">
                    All autonomous machine decisions, auto-approvals, and heuristic batch routing are <b>HARD FROZEN</b> pursuant to SOX 404 & EU AI Act regulations.
                    Dual-authorization sign-off matrix is strictly enforced via manual digital signatures under corporate policy.
                </span>
            </div>
            <div style="background: #991b1b; padding: 6px 14px; border-radius: 6px; font-weight:800; font-size:12px; letter-spacing:1px;">
                HUMAN CONTROL ONLY
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    fraud_score = 94 if st.session_state.iban_tampered else st.session_state.ai_fraud_score
    st.markdown(f"""
    <div class="ai-copilot-normal">
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
            <div>
                <strong style="font-size:16px; color:#38bdf8;">🤖 S/4HANA AI Treasury Co-Pilot: Anomaly & Fraud Engine (ML: XGBoost / Isolation Forest)</strong>
                <span style="font-size:11px; margin-left:10px; background:#0284c7; color:white; padding:3px 8px; border-radius:12px;">Pre-Release Payment Screener</span><br>
                <span style="font-size:13px; color:#e2e8f0;">
                    Autonomous validation across 4 feature vectors: Master data changes, Amount Z-scores, Sanctions fuzzy-matching, and Bank fee optimization.
                </span>
            </div>
            <div style="display:flex; gap:16px; align-items:center;">
                <div>
                    <span style="font-size:11px; color:#94a3b8;">Fraud Anomaly Index:</span><br>
                    <b style="font-size:18px; color:{'#10b981' if fraud_score < 25 else ('#f59e0b' if fraud_score < 60 else '#ef4444')};">
                        {fraud_score}% {'(Clean)' if fraud_score < 25 else ('(Suspicious)' if fraud_score < 60 else '(CRITICAL FRAUD ALERT)')}
                    </b>
                </div>
                <div style="border-left:1px solid rgba(255,255,255,0.2); padding-left:14px;">
                    <span style="font-size:11px; color:#94a3b8;">Liquidity Forecast:</span><br>
                    <b style="font-size:15px; color:#38bdf8;">Optimal (€14.2M HQ Buffer)</b>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Defensible AI Feature Vectors Breakdown Expander
    with st.expander("🔬 Inspect AI Machine Learning Feature Vectors & Anomaly Telemetry", expanded=st.session_state.iban_tampered):
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            st.markdown("**1. Vendor IBAN Velocity**")
            if st.session_state.iban_tampered:
                st.error("⚠️ Changed 2 days ago (High Risk)")
                st.caption("Table LFBK / BP Bank ID")
            else:
                st.success("✔ Verified 2 Years Ago")
                st.caption("Table LFBK: Zero recent changes")
        with col_f2:
            st.markdown("**2. Amount Z-Score**")
            st.info("✔ Z = +0.38 (Normal)")
            st.caption("Within 12-month rolling mean")
        with col_f3:
            st.markdown("**3. Sanctions Fuzzy Index**")
            st.success("✔ 0.00% (Clean)")
            st.caption("OFAC / EU Sanctions List")
        with col_f4:
            st.markdown("**4. Prescriptive Routing**")
            st.success("✔ In-House Cash POBO")
            st.caption("Saved €45 vs SWIFT wire")

        st.markdown("---")
        col_sim1, col_sim2 = st.columns([2, 3])
        with col_sim1:
            if not st.session_state.iban_tampered:
                if st.button("🚨 Simulate Vendor IBAN Tampering Attack", type="secondary"):
                    st.session_state.iban_tampered = True
                    st.session_state.batch_status = "09 (Quarantined by AI Shield)"
                    st.toast("AI Detected Unauthorized Bank Account Change! Batch Quarantined.", icon="🚨")
                    st.rerun()
            else:
                if st.button("✅ Restore Verified Vendor Master Data"):
                    st.session_state.iban_tampered = False
                    st.session_state.batch_status = "04 (Fully Approved)"
                    st.toast("Vendor Master Details Restored. Fraud Risk: 4%", icon="✅")
                    st.rerun()
        with col_sim2:
            st.caption("""
**How to defend this in an interview:**
"Our AI doesn't execute financial settlements arbitrarily. It acts as an **algorithmic gatekeeper** in S/4HANA. 
If an employee or hacker alters a vendor IBAN in master data, the machine learning model detects the change velocity, 
flags the anomaly, quarantines the payment in `BNK_MONI`, and logs the event for internal audit."
            """)

# Top Metric Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Current Scenario", st.session_state.current_scenario.split(":")[0])
with kpi2:
    status_class = "pill-approved" if "04" in st.session_state.batch_status else ("pill-rejected" if "08" in st.session_state.batch_status else "pill-pending")
    st.markdown(f"**BCM Batch Status**<br><span class='sap-status-pill {status_class}'>{st.session_state.batch_status}</span>", unsafe_allow_html=True)
with kpi3:
    resp_class = "pill-approved" if "ACCP" in st.session_state.bank_response else ("pill-rejected" if "RJCT" in st.session_state.bank_response else ("pill-hold" if "PDNG" in st.session_state.bank_response else "pill-pending"))
    st.markdown(f"**Bank Feedback (pain.002)**<br><span class='sap-status-pill {resp_class}'>{st.session_state.bank_response}</span>", unsafe_allow_html=True)
with kpi4:
    st.metric("Mandatory SWIFT UETR", st.session_state.uetr[:12] + "...")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# WORKSPACE TABS
# ==========================================
tab_map, tab_orig, tab_bcm, tab_iso, tab_gl, tab_sandbox, tab_kb, tab_dict = st.tabs([
    "🗺️ End-to-End Flow & Backend Map",
    "💳 1. Payment Origination (F110/IHC)",
    "📋 2. BCM Approval Cockpit (BNK_MONI)",
    "📡 3. ISO 20022 & MBC Engine",
    "📑 4. Universal Journal (ACDOCA)",
    "⚙️ 5. SPRO Configuration Sandbox",
    "📚 6. Treasury Knowledge Base (Glossary)",
    "🔍 7. SAP Data Dictionary Reference"
])

# ----------------------------------------------------
# TAB: PROCESS FLOW & BACKEND ARCHITECTURE MAP
# ----------------------------------------------------
with tab_map:
    st.subheader("🗺️ Enterprise Process Roadmap: Front-End Flow to ABAP Backend")
    st.caption("Visualizing the transaction flow across organizational units, batch jobs, database tables, and interface payloads.")

    st.markdown("""
    ```
    ┌─────────────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
    │  1. Subsidiary AP       │ ───▶ │  2. In-House Bank (IHC) │ ───▶ │  3. BCM Approval Batch  │
    │  F110 / F111            │      │  IHC0 / Virtual Ledger  │      │  BNK_MONI Cockpit       │
    └─────────────────────────┘      └─────────────────────────┘      └─────────────────────────┘
                                                                                   │
                                                                                   ▼
    ┌─────────────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
    │  5. EBS Auto-Clearing   │ ◀─── │  4. Bank Processing     │ ◀─── │  4. SAP MBC / SWIFT     │
    │  camt.053 / FEB_BSPROC  │      │  pain.002 Status Report │      │  pain.001 XML + UETR    │
    └─────────────────────────┘      └─────────────────────────┘      └─────────────────────────┘
    ```
    """)

    steps = [
        {
            "stage": "Stage 1: Subsidiary Payment Run",
            "tcode": "Manage Automatic Payments / F110 / F111",
            "engine": "SAPFPAYM / SAPF110V",
            "tables": "REGUH (Payment header), REGUP (Invoice line items)",
            "output": "Payment Order / IDoc PAYEXT to In-House Cash",
            "detail": "The subsidiary creates a payment proposal. Instead of triggering an external wire, it uses Payment Method 'I'. The vendor invoice is cleared against an In-House Cash Clearing Account."
        },
        {
            "stage": "Stage 2: In-House Banking Core Processing",
            "tcode": "In-House Banking Cockpit / IHC0",
            "engine": "RFEBKA00 / IHC_EOD_JOB",
            "tables": "IHC_DB_PN (Payment Order), IHC_DB_ACCT (Virtual Current Account)",
            "output": "Internal Current Account Debit & POBO Request",
            "detail": "Central Treasury validates the subsidiary's virtual account balance and internal credit line. Headquarters decides POBO routing (paying externally via Citibank NY)."
        },
        {
            "stage": "Stage 3: BCM Batching & Digital Sign-off",
            "tcode": "Manage Payment Batches / BNK_MONI",
            "engine": "RBNK_BATCH_CREATE / SAPLBNK_API",
            "tables": "BNK_BATCH (Batch Master), BNK_PAYMENT (Items), SWWWIHEAD (Workflow)",
            "output": "Approved Payment Batch Container",
            "detail": "Payments are grouped into batches by Currency and CoCode. The SPRO sign-off matrix requires 1, 2, or 3 digital signatures before releasing payment media."
        },
        {
            "stage": "Stage 4: Multi-Bank Connectivity (MBC) & SWIFT",
            "tcode": "Track Payments / /BSNAGT/MONITOR",
            "engine": "/BSNAGT/R_MSG_OUTBOUND / SSF Encryption",
            "tables": "/BSNAGT/MESSAGES, /BSNAGT/MSG_LOG",
            "output": "ISO 20022 pain.001.001.03 XML Payload with SWIFT UETR",
            "detail": "S/4HANA generates the XML payload, injects a mandatory 36-character UUID SWIFT UETR, encrypts it via digital certificates, and pushes it directly to SWIFT/Citibank."
        },
        {
            "stage": "Stage 5: Bank Feedback & EBS Auto-Reconciliation",
            "tcode": "Process Electronic Bank Statement / FEB_BSPROC",
            "engine": "RFEBKA00 / FEB_FILE_HANDLING",
            "tables": "FEBEP (Statement items), FEBKO (Header), ACDOCA (Journal)",
            "output": "pain.002 ACK/NACK + camt.053 Statement",
            "detail": "Bank sends back pain.002. If rejected (e.g. AC04), an automated reversal document is posted in ACDOCA to reopen vendor liability. At day end, camt.053 clears transit accounts."
        }
    ]

    for s in steps:
        with st.expander(f"🔍 {s['stage']} — `{s['tcode']}`", expanded=False):
            c1, c2 = st.columns([3, 2])
            with c1:
                st.write(s['detail'])
                st.markdown(f"**Interface Payload:** `{s['output']}`")
            with c2:
                st.markdown(f"**ABAP Background Job:** `{s['engine']}`")
                st.markdown(f"**Database Tables Impacted:** `{s['tables']}`")

# ----------------------------------------------------
# TAB 1: PAYMENT ORIGINATION
# ----------------------------------------------------
with tab_orig:
    st.subheader("1. Subsidiary Payment Proposal (Simulating F110 / F111)")
    st.caption("Subsidiaries trigger vendor payments using Payment Method 'I' (In-House Cash) instead of expensive cross-border wires.")

    if "Netting" in st.session_state.current_scenario:
        default_amt = 450000.0
        default_curr = "EUR"
        default_vendor = "US01 Intercompany Entity"
    elif "FX Hedged" in st.session_state.current_scenario:
        default_amt = 15000000.0
        default_curr = "JPY"
        default_vendor = "Tokyo Heavy Industries Ltd"
    elif "High-Value" in st.session_state.current_scenario:
        default_amt = 1500000.0
        default_curr = "USD"
        default_vendor = "Global Turbine Systems Inc"
    else:
        default_amt = 125000.0
        default_curr = "EUR"
        default_vendor = "Siemens Energy AG"

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        sub_code = st.selectbox("Originating Company Code (Subsidiary)", ["2000 (US Subsidiary)", "3000 (Germany GmbH)", "4000 (Singapore Pte)"])
        vendor_name = st.text_input("External Vendor (Creditor)", default_vendor)
        vendor_iban = st.text_input("Vendor IBAN / Account", "DE89370400440532013000" if default_curr == "EUR" else "US33CITI000192837465")
    with col_b:
        amount = st.number_input("Invoice Amount", min_value=100.0, value=default_amt, step=5000.0)
        curr = st.selectbox("Currency", ["EUR", "USD", "GBP", "JPY"], index=["EUR", "USD", "GBP", "JPY"].index(default_curr))
        pmt_method = st.text_input("Payment Method", f"I ({st.session_state.cfg_routing})", disabled=True)
    with col_c:
        st.info(f"ℹ️ Active Routing: **{st.session_state.cfg_routing}**")
        st.write("• Internal Account: `IHC_US01_EUR`")
        st.write("• Central House Bank: `CITI1 / Account: EUR-01`")
        st.write(f"• Active Grouping Rule: `{st.session_state.cfg_grouping}`")

    # ANIMATED EXECUTION BUTTON WITH PROGRESS STEPPER
    if st.button("🚀 Execute Payment Run with Real-Time Pipeline (Simulate F111)", type="primary"):
        progress_bar = st.progress(0, text="Initializing Payment Program SAPF110V...")
        time.sleep(0.3)
        progress_bar.progress(25, text="Validating In-House Bank Virtual Credit Line...")
        time.sleep(0.3)
        progress_bar.progress(50, text="Generating Settlement Line Items in Table REGUH / REGUP...")
        time.sleep(0.3)
        progress_bar.progress(75, text="Applying SPRO BCM Batch Grouping Rules...")
        time.sleep(0.3)
        progress_bar.progress(100, text="Payment Proposal Complete!")
        time.sleep(0.2)
        progress_bar.empty()
        
        st.success(f"✅ Payment Run completed successfully! Generated Payment Document `2000000189` in CoCode {sub_code[:4]}. Forwarded to BCM Cockpit.")
        st.toast(f"Payment Document 2000000189 Created for {sub_code[:4]}!", icon="💳")

# ----------------------------------------------------
# TAB 2: BCM APPROVAL COCKPIT
# ----------------------------------------------------
with tab_bcm:
    st.subheader("2. Manage Payment Batches (Simulating BNK_MONI / Fiori)")
    st.caption("Corporate Treasury controls multi-tier digital sign-offs based on amount thresholds configured in SPRO.")

    threshold = st.session_state.cfg_threshold
    policy = st.session_state.cfg_policy

    b1, b2 = st.columns([2, 1])
    with b1:
        st.write("### Active Batch Overview")
        batch_summary = pd.DataFrame({
            "Batch Number": ["BAT-2026-00091"],
            "Company Code": [sub_code[:4]],
            "Grouping Rule": [f"RULE_{st.session_state.cfg_grouping.replace(' ', '_')}"],
            "Batch Amount": [f"{amount:,.2f} {curr}"],
            "Threshold Limit": [f"${threshold:,.0f}"],
            "Active Policy": [policy],
            "Current Status": [st.session_state.batch_status]
        })
        st.table(batch_summary)

        st.write("### Sign-off Matrix Actions")
        c_app1, c_app2, c_app3 = st.columns(3)
        
        with c_app1:
            st.markdown("**Step 1: Treasury Analyst**")
            if st.button("✍️ Signer 1: Analyst", disabled=st.session_state.signer1_approved):
                st.session_state.signer1_approved = True
                if amount < threshold or "Single" in policy:
                    st.session_state.batch_status = "04 (Fully Approved)"
                    st.balloons()
                else:
                    st.session_state.batch_status = "02 (In Approval - Step 2)"
                st.toast("Analyst Approval Registered in BNK_BATCH", icon="✍️")
                st.rerun()
            if st.session_state.signer1_approved:
                st.success("✅ Analyst Signed (`USR_ANALYST`)")

        with c_app2:
            st.markdown(r"**Step 2: Director** ($\ge \text{Threshold}$)")
            needs_dir = (amount >= threshold) and ("Dual" in policy or "3-Tier" in policy)
            dir_disabled = not st.session_state.signer1_approved or st.session_state.signer2_approved or not needs_dir
            if st.button("✍️ Signer 2: Director", disabled=dir_disabled):
                st.session_state.signer2_approved = True
                if "3-Tier" in policy:
                    st.session_state.batch_status = "02 (In Approval - Step 3 CFO)"
                else:
                    st.session_state.batch_status = "04 (Fully Approved)"
                    st.balloons()
                st.toast("Director Approval Registered in BNK_BATCH", icon="✍️")
                st.rerun()
            if st.session_state.signer2_approved:
                st.success("✅ Director Signed (`USR_DIR_TREAS`)")

        with c_app3:
            st.markdown("**Step 3: CFO** (3-Tier Policy)")
            needs_cfo = "3-Tier" in policy and amount >= threshold
            cfo_disabled = not st.session_state.signer2_approved or st.session_state.signer3_approved or not needs_cfo
            if st.button("✍️ Signer 3: CFO", disabled=cfo_disabled):
                st.session_state.signer3_approved = True
                st.session_state.batch_status = "04 (Fully Approved - Board)"
                st.balloons()
                st.toast("CFO Final Sign-off Registered!", icon="🎉")
                st.rerun()
            if st.session_state.signer3_approved:
                st.success("✅ CFO Signed (`USR_CFO`)")

    with b2:
        st.markdown("#### BCM Release Strategy Audit Trail")
        st.code(f"""
[AUDIT LOG: BATCH BAT-2026-00091]
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Batch Amount: {amount:,.2f} {curr}
Threshold Trigger: {'YES (> Limit)' if amount >= threshold else 'NO (< Limit)'}
Signer 1 (Analyst): {'APPROVED' if st.session_state.signer1_approved else 'PENDING'}
Signer 2 (Director): {'APPROVED' if st.session_state.signer2_approved else ('REQUIRED' if needs_dir else 'NOT REQUIRED')}
Signer 3 (CFO): {'APPROVED' if st.session_state.signer3_approved else ('REQUIRED' if needs_cfo else 'NOT REQUIRED')}
Final Batch State: {st.session_state.batch_status}
        """, language="yaml")

# ----------------------------------------------------
# TAB 3: ISO 20022 & BANK CONNECTIVITY
# ----------------------------------------------------
with tab_iso:
    st.subheader("3. Bank Connectivity Engine & ISO 20022 Payloads (SAP MBC)")
    st.caption("Secure Store & Forward (SSF) transmission via Multi-Bank Connectivity with full ISO 20022 schema validation.")

    # SWIFT UETR Standards Compliance Card
    st.markdown(f"""
    <div style="background:#0f172a; border: 1px solid #38bdf8; border-radius: 8px; padding: 14px; margin-bottom: 16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
            <div>
                <span style="font-size:11px; text-transform:uppercase; letter-spacing:1px; color:#94a3b8;">Global Tracking Standard</span><br>
                <strong style="font-size:15px; color:#f8fafc;">SWIFT Unique End-to-End Transaction Reference (UETR)</strong>
            </div>
            <div style="background:#0369a1; padding:4px 10px; border-radius:12px; color:white; font-size:12px; font-weight:700;">
                ✔ RFC 4122 Version 4 UUID Validated
            </div>
        </div>
        <div style="margin-top:8px; font-family:monospace; font-size:14px; color:#38bdf8; background:#1e293b; padding:8px 12px; border-radius:6px;">
            {st.session_state.uetr}
        </div>
        <div style="margin-top:6px; font-size:11px; color:#94a3b8;">
            <b>SAP Mapping:</b> Stored in Table Field <code>REGUH-UETR</code> | <b>ISO Mapping:</b> <code>&lt;CdtTrfTxInf&gt; &gt; &lt;PmtId&gt; &gt; &lt;UETR&gt;</code>
        </div>
    </div>
    """, unsafe_allow_html=True)

    sub_t1, sub_t2, sub_t3, sub_t4 = st.tabs([
        "Outgoing: pain.001 XML", 
        "Incoming: pain.002 Status Report", 
        "SWIFT gpi Live Tracker (Hops)",
        "Electronic Bank Statement (camt.053)"
    ])

    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.03">
  <CstmrCdtTrfInitn>
    <GrpHdr>
      <MsgId>MSG-{datetime.now().strftime('%Y%m%d%H%M%S')}-HQ</MsgId>
      <CreDtTm>{datetime.now().isoformat()}Z</CreDtTm>
      <NbOfTxs>1</NbOfTxs>
      <CtrlSum>{amount:.2f}</CtrlSum>
      <InitgPty>
        <Nm>GLOBAL CENTRAL TREASURY CORP (HQ01)</Nm>
        <Id><OrgId><Othr><Id>TREAS-HQ01-FRK</Id></Othr></OrgId></Id>
      </InitgPty>
    </GrpHdr>
    <PmtInf>
      <PmtInfId>BAT-2026-00091</PmtInfId>
      <PmtMtd>TRF</PmtMtd>
      <ReqdExctnDt>{datetime.now().strftime('%Y-%m-%d')}</ReqdExctnDt>
      <Dbtr>
        <Nm>{sub_code}</Nm>
      </Dbtr>
      <DbtrAcct>
        <Id><IBAN>DE44500105175409320111</IBAN></Id>
      </DbtrAcct>
      <DbtrAgt>
        <FinInstnId><BIC>CITIUS33XXX</BIC></FinInstnId>
      </DbtrAgt>
      <CdtTrfTxInf>
        <PmtId>
          <EndToEndId>E2E-{sub_code[:4]}-00452</EndToEndId>
          <!-- SWIFT gpi UETR Mandatory in 2026 -->
          <UETR>{st.session_state.uetr}</UETR>
        </PmtId>
        <Amt>
          <InstdAmt Ccy="{curr}">{amount:.2f}</InstdAmt>
        </Amt>
        <Cdtr>
          <Nm>{vendor_name}</Nm>
        </Cdtr>
        <CdtrAcct>
          <Id><IBAN>{vendor_iban}</IBAN></Id>
        </CdtrAcct>
      </CdtTrfTxInf>
    </PmtInf>
  </CstmrCdtTrfInitn>
</Document>"""

    with sub_t1:
        st.markdown("**Generated ISO 20022 Customer Credit Transfer (`pain.001.001.03`)**")
        st.code(xml_content, language="xml")
        
        # Download XML Utility
        st.download_button(
            label="💾 Download Generated pain.001.xml",
            data=xml_content,
            file_name=f"pain_001_{st.session_state.uetr[:8]}.xml",
            mime="application/xml"
        )

    with sub_t2:
        st.markdown("**Simulated Incoming Payment Status Report (`pain.002.001.03`)**")
        st.caption("Toggle bank responses to verify automated status propagation and exception routing.")

        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            if st.button("Simulate ACCP (Accepted)"):
                st.session_state.bank_response = "ACCP (Accepted by Bank)"
                st.session_state.batch_status = "04 (Settled by Bank)"
                st.session_state.reversal_posted = False
                st.toast("Bank ACCP Ingested! Settlement Complete.", icon="✅")
                st.rerun()
        with col_p2:
            if st.button("Simulate RJCT AC04 (Closed Account)"):
                st.session_state.bank_response = "RJCT (Rejected: AC04 Closed Account)"
                st.session_state.batch_status = "08 (Partially Rejected)"
                st.session_state.reversal_posted = True
                st.toast("Bank RJCT Received! Automated Reversal Triggered.", icon="🛑")
                st.rerun()
        with col_p3:
            if st.button("Simulate PDNG (Sanctions Review)"):
                st.session_state.bank_response = "PDNG (Pending: Bank AML Review)"
                st.session_state.batch_status = "07 (Transmitted to Bank)"
                st.session_state.reversal_posted = False
                st.toast("Payment Placed on Sanctions Screening Hold.", icon="⏳")
                st.rerun()

        if "RJCT" in st.session_state.bank_response:
            st.error(f"""
⚠️ **BANK NACK RECEIVED:**
- Original Message ID: `BAT-2026-00091`
- Target UETR: `{st.session_state.uetr}`
- Status: **RJCT (Rejected)**
- Reason: **AC04 (Closed Account Number)**
- Action in SAP: BCM Status marked 'Partially Rejected'. Automated ACDOCA Reversal posted to reopen vendor payable.
            """)
        elif "PDNG" in st.session_state.bank_response:
            st.warning(f"""
⏳ **BANK STATUS: PENDING INVESTIGATION (PDNG):**
- Target UETR: `{st.session_state.uetr}`
- Reason: Compliance / AML Sanctions screening in clearing house.
- Action in SAP: Payment remains in status 07; automated follow-up scheduled.
            """)
        else:
            st.success(f"""
✅ **BANK ACK RECEIVED:**
- Target UETR: `{st.session_state.uetr}`
- Status: **ACCP (Accepted by Clearing House)**
- Funds cleared through Citibank NY.
            """)

    with sub_t3:
        st.markdown("**SWIFT gpi Tracker: Real-Time Payment Hop Telemetry**")
        st.caption(f"Tracing UETR `{st.session_state.uetr}` across correspondent banking networks via SWIFT Tracker API.")
        
        hops_data = [
            {"Hop": "1. Debtors Bank", "Entity": "Citibank N.A. (CITIUS33XXX)", "Role": "Instructing Agent", "Status": "ACCP / DEBITED", "Timestamp": f"{datetime.now().strftime('%Y-%m-%d')} 10:14:02 UTC", "Fee Deducted": "$0.00"},
            {"Hop": "2. Intermediary 1", "Entity": "Deutsche Bank AG (DEUTDEDDFXX)", "Role": "Correspondent Clearing", "Status": "ACSP / PROCESSED", "Timestamp": f"{datetime.now().strftime('%Y-%m-%d')} 10:14:38 UTC", "Fee Deducted": "€0.00"},
            {"Hop": "3. Creditors Bank", "Entity": "Commerzbank AG (COBADEFFXXX)", "Role": "Beneficiary Agent", "Status": "ACSP / RECEIVED", "Timestamp": f"{datetime.now().strftime('%Y-%m-%d')} 10:15:12 UTC", "Fee Deducted": "€0.00"},
            {"Hop": "4. Final Beneficiary", "Entity": f"{vendor_name}", "Role": "Creditor Account", "Status": "CRED / FUNDS_AVAILABLE", "Timestamp": f"{datetime.now().strftime('%Y-%m-%d')} 10:15:19 UTC", "Fee Deducted": "None (Full Value)"}
        ]
        st.dataframe(pd.DataFrame(hops_data), width="stretch")
        st.info("⏱️ **Total Elapsed Settlement Time:** 77 seconds | **Charge Type:** OUR (Zero deduction from principal)")

    with sub_t4:
        st.markdown("**End-of-Day Electronic Bank Statement (`camt.053` Summary)**")
        camt_text = f"""[CAMT.053 BANK STATEMENT DATED {datetime.now().strftime('%Y-%m-%d')}]
Account: Citibank Corporate EUR-01 (HQ01)
Transaction: POBO Wire Settlement to {vendor_name}
Reference: UETR {st.session_state.uetr}
Debit: -{amount:,.2f} {curr}
Posting Rule: CIT1 (Dr Intercompany Clearing / Cr Main Bank)
Status: POSTED & CLEARED VIA FEB_BSPROC"""
        st.code(camt_text, language="yaml")
        st.download_button(
            label="💾 Download camt.053 Statement",
            data=camt_text,
            file_name="camt_053_statement.txt",
            mime="text/plain"
        )

# ----------------------------------------------------
# TAB 4: UNIVERSAL JOURNAL (ACDOCA)
# ----------------------------------------------------
with tab_gl:
    st.subheader("4. Universal Journal Accounting Ledgers (Table ACDOCA)")
    st.caption("Demonstrating real-time balanced debits and credits across multiple legal entities and internal virtual accounts.")

    st.markdown("#### A. Originating Subsidiary Ledger (Company Code 2000)")
    sub_df = pd.DataFrame([
        {"Doc Number": "1900000120", "Posting Key": "25 (Vendor Dr)", "G/L Account": "210000 (Trade AP)", "Account Text": "Vendor Invoice Cleared", "Amount": f"+{amount:,.2f} {curr}"},
        {"Doc Number": "1900000120", "Posting Key": "50 (Credit)", "G/L Account": "113190 (IHC Clearing)", "Account Text": "Liability to Central In-House Bank", "Amount": f"-{amount:,.2f} {curr}"}
    ])
    st.dataframe(sub_df, width="stretch")

    st.markdown("#### B. Central Corporate Treasury Ledger (Company Code 1000 - HQ)")
    hq_df = pd.DataFrame([
        {"Doc Number": "1000000845", "Posting Key": "40 (Debit)", "G/L Account": "113195 (IC Receivable - Sub 2000)", "Account Text": "In-House Cash Current Account", "Amount": f"+{amount:,.2f} {curr}"},
        {"Doc Number": "1000000845", "Posting Key": "50 (Credit)", "G/L Account": "113100 (Citibank Main Bank)", "Account Text": "External Outgoing Wire Settlement", "Amount": f"-{amount:,.2f} {curr}"}
    ])
    st.dataframe(hq_df, width="stretch")

    if st.session_state.reversal_posted:
        st.markdown("---")
        st.error("#### ⚠️ Automated Reversal Document Triggered (Bank Rejection)")
        st.caption("Reversal document created via FBU3 / FB08 logic restoring vendor liability.")
        rev_df = pd.DataFrame([
            {"Reversal Doc": "1900000121", "Ref Doc": "1900000120", "Posting Key": "40 (Debit)", "G/L Account": "113190 (IHC Clearing)", "Amount": f"+{amount:,.2f} {curr}", "Reason": "Bank NACK Reversal"},
            {"Reversal Doc": "1900000121", "Ref Doc": "1900000120", "Posting Key": "31 (Vendor Cr)", "G/L Account": "210000 (Vendor Account)", "Amount": f"-{amount:,.2f} {curr}", "Reason": "Vendor Item Re-Opened"}
        ])
        st.dataframe(rev_df, width="stretch")

    # CSV Export
    combined_export = pd.concat([sub_df, hq_df], ignore_index=True)
    csv_buffer = io.StringIO()
    combined_export.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📊 Export ACDOCA Postings to CSV",
        data=csv_buffer.getvalue(),
        file_name="ACDOCA_Universal_Journal_Postings.csv",
        mime="text/csv"
    )

# ----------------------------------------------------
# TAB 5: SPRO CONFIGURATION SANDBOX
# ----------------------------------------------------
with tab_sandbox:
    st.subheader("⚙️ SPRO Configuration Sandbox (Dynamic Rules Editor)")
    st.caption("Adjust system parameters below and watch the approval workflow, threshold policies, and routing logic adapt live.")

    cfg_c1, cfg_c2 = st.columns(2)
    with cfg_c1:
        st.markdown("#### 1. BCM Approval Threshold Policy")
        new_thresh = st.slider(
            "Dual-Approval Amount Threshold ($)",
            min_value=10000.0,
            max_value=1000000.0,
            value=float(st.session_state.cfg_threshold),
            step=25000.0,
            help="Payments below this limit need only 1 approval; payments above require 2 or 3 approvals."
        )
        if new_thresh != st.session_state.cfg_threshold:
            st.session_state.cfg_threshold = new_thresh
            st.toast(f"SPRO Threshold updated to ${new_thresh:,.0f}!", icon="⚙️")
            st.rerun()

        new_policy = st.selectbox(
            "Release Strategy Sign-off Policy",
            [
                "Dual Signer (Analyst + Director)",
                "Single Signer (< Threshold only)",
                "3-Tier Board Sign-off (Analyst + Director + CFO)"
            ],
            index=["Dual Signer (Analyst + Director)", "Single Signer (< Threshold only)", "3-Tier Board Sign-off (Analyst + Director + CFO)"].index(st.session_state.cfg_policy)
        )
        if new_policy != st.session_state.cfg_policy:
            st.session_state.cfg_policy = new_policy
            st.toast(f"Sign-off Policy changed to {new_policy.split(' ')[0]}", icon="⚙️")
            st.rerun()

    with cfg_c2:
        st.markdown("#### 2. Payment Routing & Grouping")
        new_grouping = st.selectbox(
            "Payment Batch Grouping Criteria",
            [
                "Company Code + Currency",
                "Company Code + Currency + House Bank",
                "Company Code + Currency + Payment Method"
            ],
            index=["Company Code + Currency", "Company Code + Currency + House Bank", "Company Code + Currency + Payment Method"].index(st.session_state.cfg_grouping)
        )
        if new_grouping != st.session_state.cfg_grouping:
            st.session_state.cfg_grouping = new_grouping
            st.rerun()

        new_routing = st.radio(
            "Disbursement Engine",
            ["In-House Cash (POBO)", "Direct External House Bank Disbursal"],
            index=0 if "POBO" in st.session_state.cfg_routing else 1
        )
        if new_routing != st.session_state.cfg_routing:
            st.session_state.cfg_routing = new_routing
            st.toast(f"Routing Model set to {new_routing}", icon="⚙️")
            st.rerun()

    st.markdown("---")
    st.info("""
💡 **Why this sandbox is valuable in an interview:**
When an interviewer asks, *"How does your design handle a subsidiary whose threshold is €500k instead of €100k?"*, 
you can adjust the threshold slider live on screen to demonstrate how BCM re-evaluates the rule resolution matrix dynamically.
    """)

# ----------------------------------------------------
# TAB 6: TREASURY KNOWLEDGE BASE & GLOSSARY
# ----------------------------------------------------
with tab_kb:
    st.subheader("📚 Treasury & SAP Knowledge Base (Glossary)")
    st.caption("A reference guide covering core business terminology, SAP technical objects, and ISO banking standards.")

    g_tab1, g_tab2, g_tab3 = st.tabs(["Business Concepts", "SAP Technical Objects", "ISO 20022 & Banking Standards"])

    with g_tab1:
        st.markdown("""
### 🏢 Corporate Treasury Concepts
* **POBO (Payment on Behalf Of):** A centralized treasury practice where the corporate parent company executes payments to external suppliers on behalf of its subsidiaries through a central bank account, eliminating cross-border bank charges.
* **COBO (Collection on Behalf Of):** Centralized receivables where customer payments are collected into a central treasury account and credited to subsidiaries' internal accounts.
* **In-House Cash (IHC) / In-House Banking (IHB):** Operating a virtual corporate bank inside SAP. Subsidiaries hold virtual current accounts with the headquarters, enabling internal netting and automated intercompany interest calculation.
* **Multilateral Intercompany Netting:** An internal settlement mechanism where reciprocal debts between three or more subsidiaries are offset and consolidated, with only the net difference transferred.
* **Cash Pooling (Physical vs. Notional):**
  * *Physical (Zero-Balance Accounts - ZBA):* Funds are physically swept daily from subsidiary accounts to a master account.
  * *Notional Pooling:* Balances are offset for interest calculation without physically moving funds.
        """)

    with g_tab2:
        st.markdown("""
### ⚙️ SAP Technical & Architecture Objects
* **`ACDOCA` (Universal Journal):** The single source of truth in S/4HANA combining General Ledger, Asset Accounting, Controlling, and Material Ledger into one unified line-item table.
* **`REGUH` & `REGUP`:** Core tables populated by the Payment Program (`F110`/`F111`). `REGUH` contains payment settlement header records; `REGUP` stores cleared invoice line items.
* **`BNK_BATCH`:** Table storing Bank Communication Management batch metadata, batch amounts, grouping rule IDs, and approval status codes.
* **`FEB_BSPROC` / `FEBAN`:** S/4HANA Fiori and GUI engines for processing Electronic Bank Statements (`camt.053`/`MT940`), performing automated rule-based clearing.
* **`DMEE` / `DMEEX`:** Data Medium Exchange Engine used to configure mapping trees between SAP fields and bank file formats (such as ISO 20022 XML format `CGI_XML_CT`).
* **`IHC0`:** Transaction to manage In-House Cash accounts, view daily ledger balances, and configure internal credit limits.
        """)

    with g_tab3:
        st.markdown("""
### 🌐 ISO 20022 & Banking Standards
* **`pain.001` (Customer Credit Transfer Initiation):** The global ISO 20022 XML standard sent from an enterprise to a bank to initiate single or batched payments.
* **`pain.002` (Payment Status Report):** The ACK/NACK message returned by a bank detailing acceptance (`ACCP`), pending status (`PDNG`), or rejection (`RJCT`) with specific ISO error codes.
* **`camt.053` (Bank-to-Customer Statement):** The end-of-day ISO 20022 XML bank statement replacing the legacy SWIFT `MT940` format.
* **`camt.054` (Debit/Credit Notification):** Real-time notification for single incoming or outgoing transaction movements.
* **SWIFT UETR (Unique End-to-End Transaction Reference):** A mandatory 36-character UUID string (e.g., `eb6303c1-b778-4c16-8c45-46eb610185a3`) included in every payment to track it globally via SWIFT gpi.
* **ISO Rejection Codes:**
  * `AC04`: Closed Account Number
  * `AM04`: Insufficient Funds / Liquidity
  * `BE04`: Missing Creditor Address
  * `AG01`: Transaction Forbidden in Clearing System
        """)

# ----------------------------------------------------
# TAB 7: SAP DATA DICTIONARY REFERENCE
# ----------------------------------------------------
with tab_dict:
    st.subheader("🔍 SAP Data Dictionary & SPRO Architecture Reference")
    st.caption("Use these technical tables, fields, and paths to prove hands-on implementation expertise in technical interviews.")

    t1, t2 = st.columns(2)
    with t1:
        st.markdown("#### 📂 Core Database Tables & Fields")
        tables_df = pd.DataFrame({
            "SAP Table": ["REGUH", "BNK_BATCH", "ACDOCA", "IHC_DB_PN"],
            "Description": ["Payment Run Settlement Data", "BCM Payment Batches", "Universal Journal", "IHC Payment Orders"],
            "Critical Fields": ["LAUFD, LAUFI, VBLNR, UETR", "BATCH_NO, RULE_ID, STATUS", "RBUKRS, BSCHL, RACCT, WSL", "BANK_AREA, ACC_NO, EXT_KEY"]
        })
        st.table(tables_df)

        st.markdown("#### ⚙️ Key SPRO Configuration Paths")
        st.code("""
1. Bank Communication Management:
   SPRO -> FSCM -> Bank Communication Management
   -> Payment Grouping -> Define Grouping Rules
   -> Release Strategy -> Define Release Steps

2. In-House Cash / Banking:
   SPRO -> FSCM -> In-House Cash
   -> Define Bank Areas and Virtual Accounts
   -> Account Determination for IHC Clearing

3. Multi-Bank Connectivity (MBC):
   SPRO -> Multi-Bank Connectivity Connector
   -> Maintain Secure Store and Forward (SSF)
   -> Maintain Inbound/Outbound Message Routing
        """, language="yaml")

    with t2:
        st.markdown("#### 🎙️ Professional Architect Pitch Script")
        st.info("""
**When the interviewer asks about your role:**
"I architected the Treasury Payment Factory integrating In-House Banking (IHC) with BCM and Multi-Bank Connectivity (MBC). 

To ensure business alignment during design workshops, I built this functional PoC modeling the exact ISO 20022 `pain.001` XML generation with SWIFT UETR tracking, dual-approval release matrices in `BNK_BATCH`, and intercompany balancing lines in `ACDOCA`. 

Crucially, we tested both the happy path and exception handling: simulating bank `pain.002` rejections (e.g., `AC04` closed accounts) to prove how SAP reverses clearing documents and re-opens vendor payables without manual intervention.

Additionally, to demonstrate AI governance, I implemented an AI Treasury Co-Pilot risk analyzer with an emergency AI Killswitch to demonstrate compliance with internal audit, SOX, and human-in-the-loop oversight."
        """)

st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#94a3b8; font-size:13px; padding: 12px 0;">
    <strong style="color:#0077b6;">S/4HANA Treasury Payment Factory & In-House Banking Architecture Platform</strong><br>
    Architected, Designed & Developed by <strong style="color:#f59e0b;">PRAKUSH SHENDE</strong> — Senior SAP TRM & Corporate Treasury Solution Architect<br>
    Built with SAP S/4HANA 2026 Enterprise Best Practices, ISO 20022 Global Standards, BCM Frameworks & AI Governance Controls.
</div>
""", unsafe_allow_html=True)
