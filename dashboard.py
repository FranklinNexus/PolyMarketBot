"""
╔══════════════════════════════════════════════════════════════════╗
║  LAPLACE VAULT — VC Pitch Demo Dashboard                        ║
║  Bloomberg-Terminal-Grade · Streamlit · Dark Mode                ║
╚══════════════════════════════════════════════════════════════════╝
Usage:
    streamlit run dashboard.py
"""

import time
import streamlit as st

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PAGE CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.set_page_config(
    page_title="Laplace Vault",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  INJECT CUSTOM CSS — Bloomberg Terminal Aesthetic
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Root overrides ─────────────────────────── */
:root {
    --bg-primary:    #0a0a0f;
    --bg-card:       #0f1018;
    --bg-card-hover: #141520;
    --border:        #1a1b2e;
    --border-glow:   #2d2f4a;
    --text-primary:  #e8e6e3;
    --text-dim:      #6b6f82;
    --text-muted:    #3d4058;
    --accent-green:  #00ff88;
    --accent-blue:   #5b7fff;
    --accent-cyan:   #00d4ff;
    --accent-amber:  #ffb800;
    --accent-red:    #ff3b5c;
    --accent-purple: #a855f7;
}

.stApp {
    background: var(--bg-primary) !important;
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header, .stDeployButton { display: none !important; }

/* ── Metric cards ───────────────────────────── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, var(--bg-card) 0%, #12131f 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    transition: all 0.3s ease;
}
div[data-testid="stMetric"]:hover {
    border-color: var(--border-glow);
    box-shadow: 0 0 20px rgba(91, 127, 255, 0.08);
}
div[data-testid="stMetric"] label {
    color: var(--text-dim) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 1.6rem !important;
}
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-family: 'JetBrains Mono', monospace !important;
}

/* ── Terminal block ─────────────────────────── */
.terminal-block {
    background: #05060c;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px 28px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.75;
    color: var(--text-dim);
    overflow-x: auto;
    min-height: 300px;
    position: relative;
}
.terminal-block::before {
    content: '●  ●  ●';
    display: block;
    color: var(--text-muted);
    font-size: 0.55rem;
    letter-spacing: 4px;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}
.t-green  { color: #00ff88; }
.t-cyan   { color: #00d4ff; }
.t-amber  { color: #ffb800; }
.t-red    { color: #ff3b5c; }
.t-purple { color: #a855f7; }
.t-blue   { color: #5b7fff; }
.t-dim    { color: #3d4058; }
.t-white  { color: #e8e6e3; font-weight: 600; }
.t-blink  { animation: blink 1s step-end infinite; }
@keyframes blink { 50% { opacity: 0; } }

/* ── Header ─────────────────────────────────── */
.vault-header {
    text-align: center;
    padding: 40px 0 10px 0;
}
.vault-header h1 {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 800;
    font-size: 2.1rem;
    background: linear-gradient(135deg, #5b7fff 0%, #00d4ff 50%, #00ff88 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
    margin-bottom: 8px;
}
.vault-oneliner {
    font-family: 'JetBrains Mono', monospace;
    color: var(--text-dim);
    font-size: 0.82rem;
    letter-spacing: 0.08em;
}

/* ── Status badges ──────────────────────────── */
.badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
}
.badge-dryrun {
    background: rgba(255, 184, 0, 0.12);
    color: #ffb800;
    border: 1px solid rgba(255, 184, 0, 0.25);
}
.badge-ok {
    background: rgba(0, 255, 136, 0.10);
    color: #00ff88;
    border: 1px solid rgba(0, 255, 136, 0.25);
}

/* ── Dividers ───────────────────────────────── */
.vault-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 28px 0;
}

/* ── Strategy card ──────────────────────────── */
.strat-card {
    background: linear-gradient(135deg, #0f1018 0%, #12131f 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 22px 26px;
}
.strat-card h4 {
    font-family: 'JetBrains Mono', monospace;
    color: var(--text-dim);
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.strat-row {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid #0d0e18;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
}
.strat-row .label { color: var(--text-muted); }
.strat-row .value { color: var(--text-primary); font-weight: 500; }
.strat-row .value.green { color: #00ff88; }

/* ── Button override ────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #1a1030 0%, #0f1028 100%) !important;
    border: 1px solid #2d1f5e !important;
    border-radius: 12px !important;
    color: #a855f7 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.06em !important;
    padding: 16px 40px !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    border-color: #a855f7 !important;
    box-shadow: 0 0 30px rgba(168, 85, 247, 0.2) !important;
    background: linear-gradient(135deg, #221540 0%, #161035 100%) !important;
}
.stButton > button:active {
    box-shadow: 0 0 50px rgba(168, 85, 247, 0.35) !important;
}
</style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HEADER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown("""
<div class="vault-header">
    <h1>◈ LAPLACE VAULT</h1>
    <p class="vault-oneliner">AI-Driven Cross-Chain Yield &nbsp;·&nbsp; Delta-Neutral &nbsp;·&nbsp; Anti-Fragile</p>
    <br>
    <span class="badge badge-dryrun">DRY-RUN MODE</span>&nbsp;&nbsp;
    <span class="badge badge-ok">ENGINE ONLINE</span>
</div>
<hr class="vault-divider">
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CORE METRICS ROW
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Target Event", "BTC > $75K", "Jun 2026")
m2.metric("Polymarket Implied", "45.0 ¢", "-2.3 ¢")
m3.metric("AI True Probability", "65.2 %", "+4.1 %")
m4.metric("Arbitrage Edge", "20.2 %", "+6.4 %")
m5.metric("Net Delta Exposure", "0.00 Δ", "Neutral ✓")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  STRATEGY OVERVIEW + CONTROL PANEL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown('<hr class="vault-divider">', unsafe_allow_html=True)

col_strat, col_spacer, col_ctrl = st.columns([5, 1, 5])

with col_strat:
    st.markdown("""
    <div class="strat-card">
        <h4>◈ Position Architecture</h4>
        <div class="strat-row"><span class="label">LEG A · LONG</span><span class="value">Polymarket YES Shares</span></div>
        <div class="strat-row"><span class="label">Chain</span><span class="value">Polygon L2</span></div>
        <div class="strat-row"><span class="label">Size</span><span class="value">100 shares @ 0.50</span></div>
        <div class="strat-row"><span class="label">LEG B · SHORT</span><span class="value">Hyperliquid BTC-PERP</span></div>
        <div class="strat-row"><span class="label">Chain</span><span class="value">Hyperliquid L1</span></div>
        <div class="strat-row"><span class="label">Size</span><span class="value">0.001 BTC @ Market</span></div>
        <div class="strat-row"><span class="label">Net Delta</span><span class="value green">≈ 0.00  (Hedged)</span></div>
    </div>
    """, unsafe_allow_html=True)

with col_ctrl:
    st.markdown("""
    <div class="strat-card">
        <h4>◈ Risk Parameters</h4>
        <div class="strat-row"><span class="label">Strategy</span><span class="value">Delta-Neutral Basis</span></div>
        <div class="strat-row"><span class="label">Max Drawdown</span><span class="value">0.5 % (capped)</span></div>
        <div class="strat-row"><span class="label">Slippage Tolerance</span><span class="value">1.00 %</span></div>
        <div class="strat-row"><span class="label">Leg-Break Protection</span><span class="value green">ACTIVE</span></div>
        <div class="strat-row"><span class="label">Execution Mode</span><span class="value">asyncio.gather</span></div>
        <div class="strat-row"><span class="label">Concurrency</span><span class="value">Atomic-like (2 legs)</span></div>
        <div class="strat-row"><span class="label">Kill Switch</span><span class="value green">DRY_RUN = True</span></div>
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  IGNITION BUTTON + TERMINAL EMULATOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown('<hr class="vault-divider">', unsafe_allow_html=True)

_, btn_col, _ = st.columns([2, 3, 2])
with btn_col:
    ignite = st.button("🔥  IGNITE HEDGE ENGINE  (DRY-RUN)", use_container_width=True)

if ignite:
    st.markdown('<br>', unsafe_allow_html=True)
    terminal = st.empty()

    # ── Simulation timeline — each step is (delay_sec, html_line) ──
    FEED: list[tuple[float, str]] = [
        (0.0, '<span class="t-dim">laplace_vault v0.1.0  ·  python 3.13  ·  dry-run mode</span>'),
        (0.3, '<span class="t-dim">───────────────────────────────────────────────────</span>'),
        (0.5, '<span class="t-cyan">◈ [AI-SIGNAL]</span>  <span class="t-white">Ingesting on-chain + off-chain feature matrix…</span>'),
        (0.8, '<span class="t-cyan">◈ [AI-SIGNAL]</span>  Bayesian posterior updated  ·  P_true(BTC>75k) = <span class="t-green">0.652</span>'),
        (0.5, '<span class="t-cyan">◈ [AI-SIGNAL]</span>  Polymarket implied = <span class="t-amber">0.450</span>  ·  Edge = <span class="t-green">+20.2%</span>'),
        (0.4, '<span class="t-cyan">◈ [AI-SIGNAL]</span>  <span class="t-green">✓ EDGE EXCEEDS THRESHOLD — TRIGGERING EXECUTION</span>'),
        (0.6, '<span class="t-dim">───────────────────────────────────────────────────</span>'),
        (0.5, '<span class="t-purple">◈ [ROUTER]</span>    <span class="t-white">Initiating cross-chain atomic hedge…</span>'),
        (0.3, '<span class="t-purple">◈ [ROUTER]</span>    asyncio.gather() → 2 concurrent legs dispatched'),
        (0.7, '<span class="t-dim">───────────────────────────────────────────────────</span>'),
        (0.4, '<span class="t-blue">◈ [POLY-L2]</span>   ClobClient initialized  ·  chain_id=137 (Polygon)'),
        (0.5, '<span class="t-blue">◈ [POLY-L2]</span>   Building order  ·  side=<span class="t-green">BUY</span>  price=0.5000  size=100.00'),
        (0.6, '<span class="t-blue">◈ [POLY-L2]</span>   GET /tick-size   → <span class="t-green">200 OK</span>  (42ms)'),
        (0.3, '<span class="t-blue">◈ [POLY-L2]</span>   GET /neg-risk    → <span class="t-green">200 OK</span>  (38ms)'),
        (0.3, '<span class="t-blue">◈ [POLY-L2]</span>   GET /fee-rate    → <span class="t-green">200 OK</span>  (41ms)'),
        (0.6, '<span class="t-blue">◈ [POLY-L2]</span>   <span class="t-green">✓ Order SIGNED</span>  ·  sig=0xf774…1b  (EIP-712)'),
        (0.4, '<span class="t-blue">◈ [POLY-L2]</span>   🏜️ DRY-RUN  ·  post_order() <span class="t-amber">INTERCEPTED</span>'),
        (0.3, '<span class="t-blue">◈ [POLY-L2]</span>   → tx_hash = <span class="t-amber">Tx_Hash_Mocked_Polymarket</span>'),
        (0.7, '<span class="t-dim">───────────────────────────────────────────────────</span>'),
        (0.4, '<span class="t-cyan">◈ [HL-L1]</span>     Exchange initialized  ·  addr=0x4728…  (mainnet)'),
        (0.5, '<span class="t-cyan">◈ [HL-L1]</span>     Preparing SHORT  ·  coin=<span class="t-red">BTC</span>  size=0.001  slip=1.00%'),
        (0.6, '<span class="t-cyan">◈ [HL-L1]</span>     🏜️ DRY-RUN  ·  market_open() <span class="t-amber">INTERCEPTED</span>'),
        (0.3, '<span class="t-cyan">◈ [HL-L1]</span>     → tx_hash = <span class="t-amber">Tx_Hash_Mocked_Hyperliquid</span>'),
        (0.7, '<span class="t-dim">───────────────────────────────────────────────────</span>'),
        (0.5, '<span class="t-purple">◈ [ROUTER]</span>    <span class="t-green">✓ BOTH LEGS EXECUTED SUCCESSFULLY</span>  ·  Δt=2,158ms'),
        (0.4, '<span class="t-purple">◈ [ROUTER]</span>    Polymarket → <span class="t-green">OK</span>  ·  Hyperliquid → <span class="t-green">OK</span>'),
        (0.5, '<span class="t-purple">◈ [RISK]</span>      Leg-Break check: <span class="t-green">PASSED</span>  ·  No naked exposure'),
        (0.4, '<span class="t-purple">◈ [DELTA]</span>     Net Δ computed: <span class="t-green">0.000</span>  ·  Position is <span class="t-green">MARKET-NEUTRAL</span>'),
        (0.6, '<span class="t-dim">───────────────────────────────────────────────────</span>'),
        (0.5, '<span class="t-green">◈ LAPLACE VAULT — HEDGE COMPLETE — ANTI-FRAGILE POSITION LOCKED 🛡️</span>'),
        (0.3, '<span class="t-dim">engine shutdown  ·  uptime 2.4s  ·  0 errors  ·  0 warnings</span>'),
    ]

    rendered_lines: list[str] = []
    for delay, line in FEED:
        time.sleep(delay)
        rendered_lines.append(line)
        html = '<div class="terminal-block">' + "<br>".join(rendered_lines)
        # add blinking cursor on the last line
        html += '<span class="t-blink"> █</span></div>'
        terminal.markdown(html, unsafe_allow_html=True)

    # Final state — remove blink cursor
    final_html = '<div class="terminal-block">' + "<br>".join(rendered_lines) + "</div>"
    terminal.markdown(final_html, unsafe_allow_html=True)

    # Success banner
    st.markdown('<br>', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    s1.success("✅  Polymarket Leg — Signed & Intercepted")
    s2.success("✅  Hyperliquid Leg — Signed & Intercepted")
    s3.success("🛡️  Delta Exposure = 0.00 · Anti-Fragile")

else:
    # Idle state terminal
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("""
    <div class="terminal-block">
        <span class="t-dim">laplace_vault v0.1.0  ·  engine idle  ·  dry-run mode</span><br>
        <span class="t-dim">awaiting ignition…</span><span class="t-blink"> █</span>
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown("""
<hr class="vault-divider">
<div style="text-align:center; padding: 10px 0 30px 0;">
    <span style="font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:#3d4058; letter-spacing:0.12em;">
        LAPLACE VAULT  ·  48H HACKATHON BUILD  ·  CROSS-CHAIN DELTA-NEUTRAL  ·  ANTI-FRAGILE BY DESIGN
    </span>
</div>
""", unsafe_allow_html=True)
