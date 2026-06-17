# ==============================================================================
# --- 0. FORCE COMPATIBILITY SHIELD (CRITICAL FOR PYTHON 3.14 BYPASS) ---
# ==============================================================================
import os
import sys

# Google Protobuf engine layer synchronization
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st
import sqlite3
import random
import time

# ==============================================================================
# --- 1. APP ARCHITECTURE & INITIAL SETUP ---
# ==============================================================================
st.set_page_config(
    page_title="NiceHash", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Database Backend Setup
def init_nicehash_database():
    conn = sqlite3.connect("nicehash_core_vault.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY, password TEXT, security_pin TEXT,
            invest_wallet REAL, commission_wallet REAL, vip_level TEXT, invite_code TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, vip_level TEXT, 
            investment REAL, daily_yield REAL, accumulated REAL, last_update TEXT
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO users VALUES ('demo@gmail.com', 'demo123', '1122', 150.00, 45.50, 'VIP1', '286651')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES ('admin@nicehash.one', 'admin786', '0000', 5000.00, 1250.00, 'VIP4', '777888')")
    conn.commit()
    conn.close()

def query_db(query, args=(), one=False, commit=False):
    conn = sqlite3.connect("nicehash_core_vault.db", check_same_thread=False)
    cursor = conn.cursor()
    try:
        cursor.execute(query, args)
        if commit:
            conn.commit()
            conn.close()
            return True
        rv = cursor.fetchall()
        conn.close()
        return (rv[0] if rv else None) if one else rv
    except Exception as e:
        conn.close()
        return None if one else []

init_nicehash_database()

# Session States Handling
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'current_user' not in st.session_state: st.session_state.current_user = ""
if 'active_tab' not in st.session_state: st.session_state.active_tab = "Home"
if 'show_news_announcement' not in st.session_state: st.session_state.show_news_announcement = True

# Real-time Rotating Fake Log Pools
emails_pool = ['m***7a@gmail.com', 'k***99@yahoo.com', 's***_khan@live.com', 'r***x7@hotmail.com', 'a***11@gmail.com']
phones_pool = ['+9230****891', '+9232****443', '+6281****992', '+4479****112', '+121****554']

def get_rotating_withdrawal_logs():
    logs = []
    random.seed(int(time.time() / 60))
    for i in range(4):
        identity = random.choice(emails_pool if i % 2 == 0 else phones_pool)
        amount = round(random.uniform(15.00, 3450.00), 2)
        logs.append(f"🎉 User {identity} successfully extracted <b style='color:#ff6a00;'>${amount:,.2f}</b> to wallet.")
    return logs

# ==============================================================================
# --- 2. PREMIUM APP STYLING (CLEAN SPACING CONSTRAINTS) ---
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
footer, .stDeployButton, #MainMenu, [data-testid="stStatusWidget"], [data-testid="stHeader"] { display: none !important; }

html, body, .stApp { background-color: #12161a !important; color: #ffffff !important; font-family: 'Inter', sans-serif !important; }

/* Perfect Mobile Canvas Bounds Without Empty Spaces */
[data-testid="stVerticalBlock"] { max-width: 440px !important; margin: 0 auto !important; padding: 12px !important; background: #1c2127 !important; border-radius: 0px !important; min-height: 100vh; }

/* Exact Original Header Style */
.nh-top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; background: #1c2127; padding-bottom: 8px; border-bottom: 1px solid #2a313a; }
.nh-logo-title { font-size: 24px; font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 6px; }
.nh-logo-icon { width: 24px; height: 24px; background: #ff6a00; border-radius: 50%; display: inline-block; position: relative; }
.nh-logo-icon::after { content: ''; position: absolute; width: 10px; height: 10px; background: #1c2127; left: 7px; top: 7px; border-radius: 50%; }

/* Asset Display Frame */
.asset-premium-card { background: linear-gradient(135deg, #252b35 0%, #171c24 100%); border-radius: 12px; padding: 18px; border: 1px solid #2d3642; margin-bottom: 15px; }
.asset-total-title { color: #8a99ad; font-size: 13px; font-weight: 500; }
.asset-total-value { font-size: 30px; font-weight: 700; color: #ffffff; margin: 4px 0 12px 0; font-family: monospace; }
.sub-wallet-row { display: flex; justify-content: space-between; padding: 6px 0; border-top: 1px solid rgba(255,255,255,0.05); font-size: 12px; color: #cbd5e0; }

/* Grid Quick Icons Actions */
.grid-icons-container { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; text-align: center; margin-bottom: 18px; }
.icon-box-item { background: #222933; border-radius: 12px; width: 50px; height: 50px; line-height: 50px; font-size: 20px; margin: 0 auto 4px auto; border: 1px solid #2d3642; color: #ff6a00; cursor: pointer; }
.icon-label-item { font-size: 11px; font-weight: 500; color: #cbd5e0; }

/* Marquee Scrolling Box */
.marquee-alert-box { display: flex; align-items: center; background: #171c24; border-radius: 6px; padding: 6px 10px; border: 1px solid #2a313a; margin-bottom: 15px; font-size: 12px; overflow: hidden; }
.marquee-text-flow { white-space: nowrap; animation: textScroll 16s linear infinite; color: #cbd5e0; }
@keyframes textScroll { 0% { transform: translate3d(100%, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }

/* Rotating Fan Component Graphic */
.cooling-fan-hardware { width: 140px; height: 140px; background: radial-gradient(circle, #2d3542 0%, #171c24 100%); border-radius: 50%; border: 4px solid #ff6a00; margin: 25px auto; display: flex; align-items: center; justify-content: center; position: relative; }
.fan-blades-wing { width: 110px; height: 110px; background: repeating-conic-gradient(from 0deg, #ff6a00 0deg 30deg, #171c24 30deg 60deg); border-radius: 50%; animation: spinHardware 1.2s linear infinite; }
@keyframes spinHardware { 100% { transform: rotate(360deg); } }
.fan-center-core { position: absolute; width: 36px; height: 36px; background: #171c24; border: 2px solid #ffffff; border-radius: 50%; color: #ffffff; font-weight: 800; font-size: 12px; line-height: 32px; text-align: center; }

/* Custom Streamlit Buttons Global Modification */
div.stButton > button {
    background: linear-gradient(90deg, #ff8c00 0%, #ff5500 100%) !important; color: #ffffff !important; font-weight: 700 !important; border-radius: 8px !important; width: 100% !important; border: none !important; padding: 12px !important; box-shadow: 0 4px 12px rgba(255,85,0,0.3);
}

/* Stable Inlined Overlay News Card Container */
.news-modal-inline-container {
    background: #1c2127; border: 1px solid #ff6a00; border-radius: 14px; padding: 18px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)

# Layout Setup for Title and 20+ Dynamic Languages Component
header_col1, header_col2 = st.columns([2, 1.2])
with header_col1:
    st.markdown("""
    <div class="nh-top-bar" style="border:none; margin-bottom:0; padding-bottom:0;">
        <div class="nh-logo-title"><div class="nh-logo-icon"></div>nicehash</div>
    </div>
    """, unsafe_allow_html=True)
with header_col2:
    selected_lang = st.selectbox(
        label="",
        options=[
            "🌐 English", "🌐 Urdu", "🌐 العربية", "🌐 Français", "🌐 Español", 
            "🌐 Deutsch", "🌐 Русский", "🌐 简体中文", "🌐 Türkçe", "🌐 Tiếng Việt", 
            "🌐 Bahasa Melayu", "🌐 Português", "🌐 Italiano", "🌐 日本語", "🌐 한국어",
            "🌐 हिन्दी", "🌐 DeepUrdu", "🌐 Pashto", "🌐 Punjabi", "🌐 Persian", "🌐 Bengali"
        ],
        index=0,
        key="global_language_selector_panel"
    )

st.markdown("<div style='border-bottom: 1px solid #2a313a; margin-bottom: 15px; margin-top: 5px;'></div>", unsafe_allow_html=True)

# Fetch Sync Wallet States
invest_bal, comm_bal, vip_level, user_invite = 0.00, 0.00, "VIP0", "286651"
if st.session_state.logged_in:
    u_data = query_db("SELECT invest_wallet, commission_wallet, vip_level, invite_code FROM users WHERE username=?", (st.session_state.current_user,), one=True)
    if u_data: invest_bal, comm_bal, vip_level, user_invite = u_data

# ==============================================================================
# --- 3. COHESIVE NON-BLOCKING INLINE POPUP WINDOW (100% FIXED) ---
# ==============================================================================
if st.session_state.show_news_announcement and st.session_state.active_tab == "Home":
    st.markdown("""
    <div class="news-modal-inline-container">
        <h3 style="color:#ffffff; margin:0 0 12px 0; font-weight:800; font-size:22px; text-align:center;">News Notice</h3>
        <div style="font-size:13px; color:#cbd5e0; line-height:1.6; margin-bottom: 15px;">
            🎉 <b>NiceHash · A New Era of Mining for Everyone</b><br>
            <b>Officially launched on May 31, 2026.</b><br><br>
            💡 Unlock and earn your first earnings now!<br>
            No waiting, no complicated operations, earnings arrive instantly.<br><br>
            🔥 Let's explore the infinite potential of cryptocurrencies together.
            <hr style="border-color:rgba(255,255,255,0.08); margin:12px 0;">
            <span style="color:#ff6a00; font-weight:700; font-size:13px;">✨ VIP Mission Unlocking Plan</span>
            <table style="width:100%; border-collapse:collapse; margin-top:10px; font-size:11px; text-align:center; color:#fff;">
                <tr style="background:#222933; font-weight:700;">
                    <th style="padding:6px; border:1px solid #2d3642;">Grade</th>
                    <th style="padding:6px; border:1px solid #2d3642;">Investment</th>
                    <th style="padding:6px; border:1px solid #2d3642;">Daily</th>
                    <th style="padding:6px; border:1px solid #2d3642;">Yield</th>
                </tr>
                <tr><td>VIP1</td><td>10.00</td><td>3.00</td><td style="color:#00ffcc;">30%</td></tr>
                <tr><td>VIP2</td><td>100.00</td><td>32.00</td><td style="color:#00ffcc;">32%</td></tr>
                <tr><td>VIP3</td><td>1000.00</td><td>340.00</td><td style="color:#00ffcc;">34%</td></tr>
                <tr><td>VIP4</td><td>5000.00</td><td>1800.00</td><td style="color:#00ffcc;">36%</td></tr>
            </table>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Fully working clean action trigger dismiss click
    if st.button("Got it", key="dismiss_inline_news_notice_action_panel"):
        st.session_state.show_news_announcement = False
        st.rerun()
    st.markdown("<hr style='border-color:rgba(255,255,255,0.05); margin:15px 0;'>", unsafe_allow_html=True)

# ==============================================================================
# --- 4. VIEWS PANEL DISPATCHER ---
# ==============================================================================

# --- HOME TAB PANELS ---
if st.session_state.active_tab == "Home":
    st.markdown("""
    <div style="width:100%; height:110px; background:linear-gradient(135deg, #252b35 0%, #12161a 100%); border-radius:12px; display:flex; align-items:center; justify-content:center; border:1px solid #2d3642; margin-bottom:12px;">
        <div style="font-size:26px; font-weight:900; color:#ff6a00; letter-spacing:2px;">nice<span style="color:#ffffff;">hash</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="marquee-alert-box">
        <span style="color:#ff6a00; margin-right:6px; font-weight:700;">📢</span>
        <div class="marquee-text-flow">Unlock and earn your first earnings now! No waiting, no complicated operations, earnings arrive instantly.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="asset-premium-card">
        <div class="asset-total-title">Total assets</div>
        <div class="asset-total-value">${(invest_bal + comm_bal):,.2f}</div>
        <div class="sub-wallet-row"><span>Invest wallet</span><span style="font-weight:700; color:#fff;">${invest_bal:,.2f}</span></div>
        <div class="sub-wallet-row" style="border:none; padding-bottom:0;"><span>Commission wallet</span><span style="font-weight:700; color:#fff;">${comm_bal:,.2f}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # BACKEND CONNECTION FOR QUICK HOME GRID ACTIONS
    grid_cols = st.columns(4)
    with grid_cols[0]:
        if st.button("🏛️\nDep", key="home_action_dep_btn"):
            st.session_state.active_tab = "Me"
            st.rerun()
    with grid_cols[1]:
        if st.button("🏧\nWth", key="home_action_wth_btn"):
            st.session_state.active_tab = "Me"
            st.rerun()
    with grid_cols[2]:
        if st.button("👑\nVIP", key="home_action_vip_btn"):
            st.session_state.active_tab = "VIP"
            st.rerun()
    with grid_cols[3]:
        if st.button("👥\nTeam", key="home_action_team_btn"):
            st.session_state.active_tab = "Team"
            st.rerun()
            
    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:14px; font-weight:700; margin-bottom:8px; color:#ff6a00;'>Withdrawal Stream Log</div>", unsafe_allow_html=True)
    for log in get_rotating_withdrawal_logs():
        st.markdown(f"<div style='background:#171c24; padding:10px; border-radius:8px; margin-bottom:6px; font-size:12px; border:1px solid #2a313a;'>{log}</div>", unsafe_allow_html=True)

# --- VIP TIERS PANEL ---
elif st.session_state.active_tab == "VIP":
    st.markdown(f"""
    <div style="background:#252b35; padding:15px; border-radius:12px; border:1px solid #2d3642; margin-bottom:15px;">
        <div style="display:flex; justify-content:space-between; font-size:13px; color:#cbd5e0;"><span>Current Profile Level:</span><span style="color:#ff6a00; font-weight:700;">{vip_level}</span></div>
        <div style="display:flex; justify-content:space-between; font-size:13px; color:#cbd5e0; margin-top:4px;"><span>My Active Deposit:</span><span style="color:#00ffcc; font-weight:700;">${invest_bal:,.2f}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    for i in range(1, 5):
        bounds = [0, 10, 100, 1000, 5000][i]
        profit = [0, 30, 32, 34, 36][i]
        st.markdown(f"""
        <div style="background:#171c24; border-radius:12px; padding:15px; border:1px solid #2d3642; margin-bottom:10px;">
            <div style="font-weight:800; font-size:16px; color:#ff6a00; border-bottom:1px solid rgba(255,255,255,0.05); padding-bottom:4px; margin-bottom:6px;">VIP {i} Contract Plan</div>
            <div style="display:flex; justify-content:space-between; font-size:12px;"><span style="color:#8a99ad;">Required Minimum Entry</span><span style="color:#fff; font-weight:600;">${bounds:,.2f}</span></div>
            <div style="display:flex; justify-content:space-between; font-size:12px;"><span style="color:#8a99ad;">Automated Daily Return</span><span style="color:#00ffcc; font-weight:700;">{profit:.2f}% / Day</span></div>
        </div>
        """, unsafe_allow_html=True)

# --- HARDWARE MINING FAN SIMULATOR PANEL ---
elif st.session_state.active_tab == "Mining":
    st.markdown("""
    <div class="cooling-fan-hardware"><div class="fan-blades-wing"></div><div class="fan-center-core">⚡</div></div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background:#252b35; padding:20px; border-radius:12px; border:1px solid #2d3642; text-align:center;">
        <span style="color:#8a99ad; font-size:12px; text-transform:uppercase; letter-spacing:1px;">Accumulating Live Crypto</span>
        <h2 style="margin:8px 0; font-size:28px; color:#ffffff; font-family:monospace;">0.000000 <span style="font-size:14px; color:#ff6a00;">USDT</span></h2>
        <div style="display:flex; justify-content:space-between; font-size:12px; border-top:1px solid rgba(255,255,255,0.05); padding-top:10px; margin-top:12px;"><span style="color:#cbd5e0;">Node Tier Level</span><span style="color:#ff6a00; font-weight:700;">{vip_level}</span></div>
        <div style="display:flex; justify-content:space-between; font-size:12px;"><span style="color:#cbd5e0;">Cloud Engine Status</span><span style="color:#00ffcc; font-weight:600;">ACTIVE & RUNNING</span></div>
    </div>
    """, unsafe_allow_html=True)

# --- REFERRAL LOGISTIC NETWORK PANEL ---
elif st.session_state.active_tab == "Team":
    st.markdown(f"""
    <div style="background:#252b35; padding:15px; border-radius:12px; border:1px solid #2d3642;">
        <span style="font-size:12px; color:#8a99ad;">Personal Invitation ID Code</span>
        <h2 style="margin:4px 0; color:#ff6a00; letter-spacing:1px; font-family:monospace;">{user_invite}</h2>
        <div style="background:#171c24; padding:8px; border-radius:6px; font-size:11px; color:#cbd5e0; word-break:break-all; border:1px solid #2a313a; margin-top:8px;">
            https://nicehash.one/#/register?invite_code={user_invite}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- USER PROFILE & VAULT CONFIGS ---
elif st.session_state.active_tab == "Me":
    if not st.session_state.logged_in:
        st.markdown("<h4 style='text-align:center; color:#ff6a00; margin-bottom:15px;'>NiceHash Security Firewall</h4>", unsafe_allow_html=True)
        user_input = st.text_input("Account Handle Email:", placeholder="demo@gmail.com")
        pass_input = st.text_input("Security Access Key:", type="password", placeholder="demo123")
        
        if st.button("Unlock Vault Workspace"):
            if user_input.strip() == "demo@gmail.com" and pass_input.strip() == "demo123":
                st.session_state.logged_in = True
                st.session_state.current_user = "demo@gmail.com"
                st.rerun()
            elif user_input.strip() == "admin@nicehash.one" and pass_input.strip() == "admin786":
                st.session_state.logged_in = True
                st.session_state.current_user = "admin@nicehash.one"
                st.rerun()
            else:
                st.error("Firewall reject: Invalid Key match.")
    else:
        st.markdown(f"""
        <div style="background:#252b35; padding:15px; border-radius:12px; border:1px solid #2d3642; margin-bottom:15px;">
            <div style="font-size:12px; color:#8a99ad;">Active Session Profile:</div>
            <div style="font-size:16px; font-weight:700; color:#fff; margin-top:2px;">👤 {st.session_state.current_user}</div>
            <span style="background:#ff6a00; color:white; font-size:10px; font-weight:800; padding:2px 8px; border-radius:6px; margin-top:4px; display:inline-block;">{vip_level} Level Node</span>
        </div>
        """, unsafe_allow_html=True)
        
        deposit_input = st.number_input("Test Core Deposit Amount ($):", min_value=5.0, step=10.0)
        if st.button("Inject Simulated USDT Balance"):
            query_db("UPDATE users SET invest_wallet = invest_wallet + ? WHERE username=?", (deposit_input, st.session_state.current_user), commit=True)
            st.success("Database vault state balanced successfully!")
            time.sleep(0.5)
            st.rerun()
            
        st.markdown("<hr style='border-color:rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
        if st.button("Disconnect Terminal Session"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.rerun()

# ==============================================================================
# --- 5. PREMIUM BOTTOM NAVIGATION BAR BAR CONFIGURATION ---
# ==============================================================================
st.markdown("<div style='margin-top:25px;'></div>", unsafe_allow_html=True)
bottom_navigation_grid = st.columns(5)

with bottom_navigation_grid[0]:
    if st.button("🏠\nHome", key="nav_h_core"): st.session_state.active_tab = "Home"; st.rerun()
with bottom_navigation_grid[1]:
    if st.button("👑\nVIP", key="nav_v_core"): st.session_state.active_tab = "VIP"; st.rerun()
with bottom_navigation_grid[2]:
    if st.button("⚡\nMine", key="nav_m_core"): st.session_state.active_tab = "Mining"; st.rerun()
with bottom_navigation_grid[3]:
    if st.button("👥\nTeam", key="nav_t_core"): st.session_state.active_tab = "Team"; st.rerun()
with bottom_navigation_grid[4]:
    if st.button("👤\nMe", key="nav_me_core"): st.session_state.active_tab = "Me"; st.rerun()
