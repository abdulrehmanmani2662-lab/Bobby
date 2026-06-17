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
import datetime

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
    # Default Dummy Accounts for instant validation
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
if 'show_news' not in st.session_state: st.session_state.show_news = True

# Real-time Rotating Fake Log Pools
emails_pool = ['m***7a@gmail.com', 'k***99@yahoo.com', 's***_khan@live.com', 'r***x7@hotmail.com', 'a***11@gmail.com']
phones_pool = ['+9230****891', '+9232****443', '+6281****992', '+4479****112', '+121****554']

def get_rotating_withdrawal_logs():
    logs = []
    random.seed(int(time.time() / 60))  # Consistent rotation across refreshes
    for i in range(4):
        identity = random.choice(emails_pool if i % 2 == 0 else phones_pool)
        amount = round(random.uniform(15.00, 3450.00), 2)
        logs.append(f"🎉 User {identity} successfully extracted <b style='color:#ff6a00;'>${amount:,.2f}</b> to wallet.")
    return logs

# ==============================================================================
# --- 2. EXACT ORIGINAL GRAPHIC STYLING EMBED (YOUR PREMIUM MARKS) ---
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
footer, .stDeployButton, #MainMenu, [data-testid="stStatusWidget"], [data-testid="stHeader"] { display: none !important; }

html, body, .stApp { background-color: #12161a !important; color: #ffffff !important; font-family: 'Inter', sans-serif !important; }

/* Perfect Mobile Canvas Bounds */
[data-testid="stVerticalBlock"] { max-width: 440px !important; margin: 0 auto !important; padding: 12px !important; background: #1c2127 !important; border-radius: 0px !important; min-height: 100vh; box-shadow: 0 0 30px rgba(0,0,0,0.6); }

/* Exact Original Header Style */
.nh-top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; background: #1c2127; padding-bottom: 8px; border-bottom: 1px solid #2a313a; }
.nh-logo-title { font-size: 24px; font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 6px; font-style: normal; }
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
.cooling-fan-hardware { width: 140px; height: 140px; background: radial-gradient(circle, #2d3542 0%, #171c24 100%); border-radius: 50%; border: 4px solid #ff6a00; margin: 25px auto; display: flex; align-items: center; justify-content: center; position: relative; box-shadow: 0 0 20px rgba(255,106,0,0.2); }
.fan-blades-wing { width: 110px; height: 110px; background: repeating-conic-gradient(from 0deg, #ff6a00 0deg 30deg, #171c24 30deg 60deg); border-radius: 50%; animation: spinHardware 1.2s linear infinite; }
@keyframes spinHardware { 100% { transform: rotate(360deg); } }
.fan-center-core { position: absolute; width: 36px; height: 36px; background: #171c24; border: 2px solid #ffffff; border-radius: 50%; color: #ffffff; font-weight: 800; font-size: 12px; line-height: 32px; text-align: center; }

/* Custom HTML Close Button embedded inside Modal container frame */
.custom-modal-close-trigger {
    display: block; width: 100%; text-align: center; background: linear-gradient(90deg, #ff8c00 0%, #ff5500 100%);
    color: white !important; font-weight: 700; border: none; padding: 12px; border-radius: 8px;
    font-size: 14px; text-decoration: none; cursor: pointer; margin-top: 15px; box-shadow: 0 4px 12px rgba(255,85,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# Application Logo Header Execution
st.markdown("""
<div class="nh-top-bar">
    <div class="nh-logo-title"><div class="nh-logo-icon"></div>nicehash</div>
    <div style="background:#222933; padding:4px 10px; border-radius:10px; font-size:12px; font-weight:600; color:#ff6a00; border:1px solid #2d3642;">🌐 English</div>
</div>
""", unsafe_allow_html=True)

# Fetch Sync Wallet States
invest_bal, comm_bal, vip_level, user_invite = 0.00, 0.00, "VIP0", "286651"
if st.session_state.logged_in:
    u_data = query_db("SELECT invest_wallet, commission_wallet, vip_level, invite_code FROM users WHERE username=?", (st.session_state.current_user,), one=True)
    if u_data: invest_bal, comm_bal, vip_level, user_invite = u_data

# ==============================================================================
# --- 3. PREMIUM NEWS MODAL CONTROLLER (100% VISIBILITY CLOSURE INTERFACE) ---
# ==============================================================================
# Native Query parameters engine interception to flush popup without framework layout blocks
url_intercept = st.query_params
if "flush_popup" in url_intercept:
    st.session_state.show_news = False
    st.query_params.clear()
    st.rerun()

if st.session_state.show_news and st.session_state.active_tab == "Home":
    st.markdown("""
    <div style="background: rgba(0,0,0,0.85); position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 999999; display: flex; align-items: center; justify-content: center; padding: 12px;">
        <div style="background: #1c2127; max-width: 390px; width:100%; border-radius: 14px; border: 1px solid #ff6a00; padding: 18px; box-shadow: 0 10px 35px rgba(0,0,0,0.8); max-height: 85vh; overflow-y: auto;">
            <h3 style="color:#ffffff; margin:0 0 12px 0; font-weight:800; font-size:22px; text-align:center;">News</h3>
            <div style="font-size:12.5px; color:#cbd5e0; line-height:1.6;">
                🎉 <b>NiceHash · A New Era of Mining for Everyone</b><br>
                <b>Officially launched on May 31, 2026.</b><br><br>
                💡 Unlock and earn your first earnings now!<br>
                No waiting, no complicated operations, earnings arrive instantly after unlocking.<br><br>
                🔥 Here, let's explore the infinite potential of cryptocurrencies together. A new era truly begins the moment you join us.
                <hr style="border-color:rgba(255,255,255,0.08); margin:12px 0;">
                <span style="color:#ff6a00; font-weight:700; font-size:13px;">✨ VIP Mission Unlocking Plan - Enjoy Instant Recharge</span>
                <table style="width:100%; border-collapse:collapse; margin-top:10px; font-size:11px; text-align:center; color:#fff;">
                    <tr style="background:#222933; font-weight:700;">
                        <th style="padding:6px; border:1px solid #2d3642;">Grade</th>
                        <th style="padding:6px; border:1px solid #2d3642;">Investment</th>
                        <th style="padding:6px; border:1px solid #2d3642;">Daily</th>
                        <th style="padding:6px; border:1px solid #2d3642;">Yield</th>
                    </tr>
                    <tr><td style="padding:5px; border:1px solid #2d3642;">VIP1</td><td style="padding:5px; border:1px solid #2d3642;">10.00</td><td style="padding:5px; border:1px solid #2d3642;">3.00</td><td style="padding:5px; border:1px solid #2d3642; color:#00ffcc;">30%</td></tr>
                    <tr><td style="padding:5px; border:1px solid #2d3642;">VIP2</td><td style="padding:5px; border:1px solid #2d3642;">100.00</td><td style="padding:5px; border:1px solid #2d3642;">32.00</td><td style="padding:5px; border:1px solid #2d3642; color:#00ffcc;">32%</td></tr>
                    <tr><td style="padding:5px; border:1px solid #2d3642;">VIP3</td><td style="padding:5px; border:1px solid #2d3642;">1000.00</td><td style="padding:5px; border:1px solid #2d3642;">340.00</td><td style="padding:5px; border:1px solid #2d3642; color:#00ffcc;">34%</td></tr>
                    <tr><td style="padding:5px; border:1px solid #2d3642;">VIP4</td><td style="padding:5px; border:1px solid #2d3642;">5000.00</td><td style="padding:5px; border:1px solid #2d3642;">1800.00</td><td style="padding:5px; border:1px solid #2d3642; color:#00ffcc;">36%</td></tr>
                </table>
            </div>
            <a href="/?flush_popup=true" target="_self" class="custom-modal-close-trigger">Got it</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 4. VIEWS PANEL DISPATCHER ---
# ==============================================================================

# --- HOME TAB PANELS (`1000078177.jpg`) ---
if st.session_state.active_tab == "Home":
    st.markdown("""
    <div style="width:100%; height:110px; background:linear-gradient(135deg, #252b35 0%, #12161a 100%); border-radius:12px; display:flex; align-items:center; justify-content:center; border:1px solid #2d3642; margin-bottom:12px;">
        <div style="font-size:26px; font-weight:900; color:#ff6a00; letter-spacing:2px; text-shadow:0 0 10px rgba(255,106,0,0.3);">nice<span style="color:#ffffff;">hash</span></div>
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
    
    st.markdown("""
    <div class="grid-icons-container">
        <div onclick="window.location.reload()"><div class="icon-box-item">🏛️</div><div class="icon-label-item">Deposit</div></div>
        <div onclick="window.location.reload()"><div class="icon-box-item">🏧</div><div class="icon-label-item">Withdraw</div></div>
        <div onclick="window.location.reload()"><div class="icon-box-item">👑</div><div class="icon-label-item">VIP Plan</div></div>
        <div onclick="window.location.reload()"><div class="icon-box-item">👥</div><div class="icon-label-item">My Team</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='font-size:14px; font-weight:700; margin-bottom:8px; color:#ff6a00;'>Withdrawal Stream Log</div>", unsafe_allow_html=True)
    for log in get_rotating_withdrawal_logs():
        st.markdown(f"<div style='background:#171c24; padding:10px; border-radius:8px; margin-bottom:6px; font-size:12px; border:1px solid #2a313a;'>{log}</div>", unsafe_allow_html=True)

# --- VIP EXPERT TIERS PANEL (`1000078175.jpg`) ---
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

# --- HARDWARE MINING FAN SIMULATOR PANEL (`1000078174.jpg`) ---
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
    
    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    if st.button("Manual Extraction Force"):
        st.toast("Syncing blockchain matrix nodes...")

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

# --- USER PROFILE & VAULT CONFIGS (`1000078171.jpg`) ---
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
                st.error("Firewall reject: Invalid Key parameters match.")
    else:
        st.markdown(f"""
        <div style="background:#252b35; padding:15px; border-radius:12px; border:1px solid #2d3642; margin-bottom:15px;">
            <div style="font-size:12px; color:#8a99ad;">Active Session Profile:</div>
            <div style="font-size:16px; font-weight:700; color:#fff; margin-top:2px;">👤 {st.session_state.current_user}</div>
            <span style="background:#ff6a00; color:white; font-size:10px; font-weight:800; padding:2px 8px; border-radius:6px; margin-top:4px; display:inline-block;">{vip_level} Level Node</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Test Transaction Simulators
        st.markdown("<div style='font-size:13px; font-weight:700; color:#ff6a00; margin-bottom:4px;'>Simulation Controls</div>", unsafe_allow_html=True)
        deposit_input = st.number_input("Test Core Deposit Amount ($):", min_value=5.0, step=10.0)
        
        if st.button("Inject Simulated USDT Balance"):
            query_db("UPDATE users SET invest_wallet = invest_wallet + ? WHERE username=?", (deposit_input, st.session_state.current_user), commit=True)
            st.success("Database vault state balanced successfully!")
            time.sleep(0.5)
            st.rerun()
            
        st.markdown("<hr style='border-color:rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
        if st.button("Disconnect Node Terminal Session"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.rerun()

# ==============================================================================
# --- 5. PREMIUM BOTTOM NAVIGATION BAR BAR CONFIGURATION ---
# ==============================================================================
st.markdown("<div style='margin-top:45px;'></div>", unsafe_allow_html=True)
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
