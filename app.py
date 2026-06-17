# ==============================================================================
# --- 0. FORCE COMPATIBILITY SHIELD (CRITICAL FOR PYTHON 3.14 BYPASS) ---
# ==============================================================================
import os
import sys

# Google Protobuf ke fast C++ engine ko block karke pure-python par switch karta hai
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st
import sqlite3
import random
import time
import pandas as pd
import streamlit.components.v1 as components

# ==============================================================================
# --- 1. INITIALIZATION & CORE METRICS SYSTEM ---
# ==============================================================================
st.set_page_config(
    page_title="NiceHash - Cloud Mining", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Database Initialization
def init_nicehash_db():
    conn = sqlite3.connect("nicehash_vault.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY, password TEXT, security_pin TEXT,
            invest_wallet REAL, commission_wallet REAL, vip_level TEXT, invite_code TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mining_contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, vip_level TEXT, 
            investment REAL, daily_yield REAL, status TEXT, date_activated TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, type TEXT, amount REAL, status TEXT)
    """)
    cursor.execute("INSERT OR IGNORE INTO users VALUES ('demo@gmail.com', 'demo123', '1122', 0.00, 0.00, 'VIP0', '286651')")
    conn.commit()
    conn.close()

def query_db(query, args=(), one=False, commit=False):
    conn = sqlite3.connect("nicehash_vault.db", check_same_thread=False)
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

init_nicehash_db()

# State Registry Management
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'current_user' not in st.session_state: st.session_state.current_user = ""
if 'active_tab' not in st.session_state: st.session_state.active_tab = "Home"
if 'show_news' not in st.session_state: st.session_state.show_news = True
if 'auth_mode' not in st.session_state: st.session_state.auth_mode = "Login"

# ==============================================================================
# --- 2. PREMIUM CUSTOM LOGS GENERATORS (REAL-TIME ROTATING) ---
# ==============================================================================
emails_pool = ['a***3v@yahoo.com', 'o***de@yahoo.com', 'r***s8@gmail.com', 'k***m2@gmail.com', 't***77@live.com']
phones_pool = ['+62****17', '+92****92', '+91****43', '+44****88', '+1****52']

def generate_fake_withdrawals():
    logs = []
    random.seed(int(time.time() / 100)) # Changes gradually
    for i in range(4):
        identity = random.choice(emails_pool if i % 2 == 0 else phones_pool)
        amount = round(random.uniform(1000.00, 95000.00), 2)
        logs.append(f"{identity} &nbsp; withdrew &nbsp; <span style='color:#ff6a00; font-weight:700;'>${amount}</span> ! ")
    return logs

# ==============================================================================
# --- 3. HARDLUXE NICEHASH GRAPHIC STYLING CONFIG ---
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
footer, .stDeployButton, #MainMenu, [data-testid="stStatusWidget"], [data-testid="stHeader"] { display: none !important; }

html, body, .stApp { background-color: #12161a !important; color: #ffffff !important; font-family: 'Inter', sans-serif !important; }
[data-testid="stVerticalBlock"] { max-width: 460px !important; margin: 0 auto !important; padding: 12px !important; background: #1c2127 !important; border-radius: 16px !important; border: 1px solid #2a313a !important; box-shadow: 0 12px 36px rgba(0,0,0,0.5) !important; }

/* Top Luxury Custom Header Row */
.nh-top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #2a313a; padding-bottom: 10px; }
.nh-logo-title { font-size: 22px; font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 8px; }
.nh-logo-icon { width: 34px; height: 34px; background: radial-gradient(circle, #ffaa00 0%, #ff6a00 100%); border-radius: 50%; display: inline-block; position: relative; }
.nh-logo-icon::after { content: ''; position: absolute; width: 14px; height: 14px; background: #1c2127; left: 10px; top: 10px; border-radius: 3px; }

/* Main Assets Block & Grids */
.asset-premium-card { background: linear-gradient(135deg, #7a1f1f 0%, #1e2530 60%); border-radius: 14px; padding: 20px; border: 1px solid #3d2424; position: relative; margin-bottom: 15px; }
.asset-total-title { color: #a0aec0; font-size: 14px; font-weight: 500; text-align: center; margin-top: 5px; }
.asset-total-value { font-size: 32px; font-weight: 800; color: #ffffff; text-align: center; margin: 8px 0; }
.sub-wallet-row { display: flex; justify-content: space-between; padding: 8px 5px; border-top: 1px solid rgba(255,255,255,0.06); font-size: 13px; color: #cbd5e0; }

/* Quick Action Grid Icons */
.grid-icons-container { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; text-align: center; margin-bottom: 20px; }
.icon-box-item { background: #252b34; border-radius: 50%; width: 56px; height: 56px; line-height: 56px; font-size: 20px; margin: 0 auto 6px auto; border: 1px solid #313945; color: #ff6a00; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
.icon-label-item { font-size: 12px; font-weight: 600; color: #a0aec0; }

/* Running Marquee Alert Line */
.marquee-alert-box { display: flex; align-items: center; background: #232932; border-radius: 20px; padding: 8px 15px; border: 1px solid #ff6a0044; margin-bottom: 15px; font-size: 12px; color: #cbd5e0; overflow: hidden; }
.marquee-text-flow { white-space: nowrap; animation: textScroll 14s linear infinite; padding-left: 20px; }
@keyframes textScroll { 0% { transform: translate3d(100%, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }

/* Modern Mining Cooling Fan Simulator Graphic Frame */
.fan-simulator-canvas { text-align: center; margin: 20px 0; position: relative; }
.cooling-fan-hardware { width: 140px; height: 140px; background: radial-gradient(circle, #2d3542 0%, #171c24 100%); border-radius: 24px; border: 4px solid #3a4454; margin: 0 auto; box-shadow: inset 0 0 20px rgba(0,0,0,0.8), 0 8px 20px rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; position: relative; }
.fan-blades-wing { width: 110px; height: 110px; background: repeating-conic-gradient(from 0deg, #3f4a5c 0deg 30deg, #1f252e 30deg 60deg); border-radius: 50%; animation: spinHardware 2.5s linear infinite; border: 2px solid #ff6a0022; }
@keyframes spinHardware { 100% { transform: rotate(360deg); } }
.fan-center-core { position: absolute; width: 34px; height: 34px; background: #171c24; border: 2px solid #00f0ff; border-radius: 50%; color: #00f0ff; font-weight: 800; font-size: 11px; line-height: 30px; text-align: center; box-shadow: 0 0 8px #00f0ff55; }

/* Custom Inputs Overwrites */
div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input, div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: #21272f !important; color: #ffffff !important; border: 1px solid #2e3742 !important; border-radius: 10px !important; padding: 12px !important; font-weight: 600 !important;
}
div.stButton > button {
    background: linear-gradient(90deg, #ff8c00 0%, #ff5500 100%) !important; color: #ffffff !important; font-weight: 700 !important; border-radius: 10px !important; width: 100% !important; border: none !important; text-transform: uppercase; padding: 12px !important; box-shadow: 0 4px 15px rgba(255,85,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# Top Bar Render Engine
st.markdown("""
<div class="nh-top-bar">
    <div class="nh-logo-title"><div class="nh-logo-icon"></div> NiceHash</div>
    <div style="background:#252b34; padding:5px 12px; border-radius:15px; font-size:12px; font-weight:600; color:#ff6a00; border:1px solid #313945;">🌐 English</div>
</div>
""", unsafe_allow_html=True)

# Fetch user variables
invest_bal, comm_bal, vip_level, user_invite = 0.00, 0.00, "VIP0", "286651"
if st.session_state.logged_in:
    u_data = query_db("SELECT invest_wallet, commission_wallet, vip_level, invite_code FROM users WHERE username=?", (st.session_state.current_user,), one=True)
    if u_data: invest_bal, comm_bal, vip_level, user_invite = u_data

# ==============================================================================
# --- 4. GLOBAL POPUP NEWS MODAL WINDOW (`1000078176.jpg`) ---
# ==============================================================================
if st.session_state.show_news and st.session_state.active_tab == "Home":
    st.markdown("""
    <div style="background: rgba(0,0,0,0.7); position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 999999; display: flex; align-items: center; justify-content: center; padding: 15px;">
        <div style="background: #1c2127; max-width: 400px; width:100%; border-radius: 16px; border: 2px solid #ff6a00; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); max-height: 85vh; overflow-y: auto;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                <h3 style="color:#ffffff; margin:0; font-weight:800; font-size:22px; text-align:center; width:100%;">News</h3>
            </div>
            <div style="font-size:13px; color:#cbd5e0; line-height:1.6;">
                🎉 <b>NiceHash · A New Era of Mining for Everyone</b><br>
                <b>Officially launched on May 31, 2026.</b><br>
                💡 Unlock and earn your first earnings now!<br>
                No waiting, no complicated operations, earnings arrive instantly after unlocking.<br>
                🔥 Here, let's explore the infinite potential of cryptocurrencies together.<br>
                <b>A new era truly begins the moment you join us.</b>
                <hr style="border-color:rgba(255,255,255,0.1); margin:12px 0;">
                ✨ <b>VIP Mission Unlocking Plan - Enjoy Instant Recharge</b> ✨
                <table style="width:100%; border-collapse:collapse; margin-top:10px; font-size:11px; text-align:center; color:#fff;">
                    <tr style="background:#2d3542; font-weight:700;">
                        <th style="padding:6px; border:1px solid #3a4454;">Grade</th>
                        <th style="padding:6px; border:1px solid #3a4454;">Investment (USDT)</th>
                        <th style="padding:6px; border:1px solid #3a4454;">Daily Earnings</th>
                        <th style="padding:6px; border:1px solid #3a4454;">Yield</th>
                    </tr>
                    <tr><td style="padding:5px; border:1px solid #3a4454;">VIP1</td><td style="padding:5px; border:1px solid #3a4454;">10</td><td style="padding:5px; border:1px solid #3a4454;">3</td><td style="padding:5px; border:1px solid #3a4454;">30%</td></tr>
                    <tr><td style="padding:5px; border:1px solid #3a4454;">VIP2</td><td style="padding:5px; border:1px solid #3a4454;">100</td><td style="padding:5px; border:1px solid #3a4454;">32</td><td style="padding:5px; border:1px solid #3a4454;">32%</td></tr>
                    <tr><td style="padding:5px; border:1px solid #3a4454;">VIP3</td><td style="padding:5px; border:1px solid #3a4454;">1000</td><td style="padding:5px; border:1px solid #3a4454;">340</td><td style="padding:5px; border:1px solid #3a4454;">344%</td></tr>
                    <tr><td style="padding:5px; border:1px solid #3a4454;">VIP4</td><td style="padding:5px; border:1px solid #3a4454;">5000</td><td style="padding:5px; border:1px solid #3a4454;">1800</td><td style="padding:5px; border:1px solid #3a4454;">36%</td></tr>
                </table>
            </div>
            <div style="margin-top:20px;"></div>
    """, unsafe_allow_html=True)
    if st.button("Got it", key="close_news_popup_btn"):
        st.session_state.show_news = False
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

# ==============================================================================
# --- 5. TAB VIEW SYSTEMS DIRECT DISPATCH ---
# ==============================================================================

# --- TAB 1: HOME PANEL (`1000078177.jpg`) ---
if st.session_state.active_tab == "Home":
    st.markdown("""
    <div style="width:100%; height:130px; background:linear-gradient(45deg, #0f1115 25%, #232932 25%, #232932 50%, #0f1115 50%, #0f1115 75%, #232932 75%); background-size:40px 40px; border-radius:12px; display:flex; align-items:center; justify-content:center; border:1px solid #2e3742; box-shadow:inset 0 0 20px #000;">
        <div style="font-size:26px; font-weight:900; color:#ff6a00; letter-spacing:3px; text-shadow:0 0 10px rgba(255,106,0,0.5);">nice<span style="color:#ffffff;">hash</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="marquee-alert-box">
        <span style="color:#ff6a00; font-weight:700; margin-right:5px;">📢</span>
        <div class="marquee-text-flow">Unlock and earn your first earnings now! No waiting, no complicated operations, earnings arrive instantly.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="asset-premium-card">
        <div class="asset-total-title">Total assets</div>
        <div class="asset-total-value">${(invest_bal + comm_bal):,.2f}</div>
        <div class="sub-wallet-row"><span>Invest wallet</span><span style="font-weight:700; color:#fff;">${invest_bal:,.2f}</span></div>
        <div class="sub-wallet-row" style="border:none;"><span>Commission wallet</span><span style="font-weight:700; color:#fff;">${comm_bal:,.2f}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="grid-icons-container">
        <div><div class="icon-box-item">🏛️</div><div class="icon-label-item">Deposit</div></div>
        <div><div class="icon-box-item">🏧</div><div class="icon-label-item">Withdraw</div></div>
        <div><div class="icon-box-item">👑</div><div class="icon-label-item">VIP</div></div>
        <div><div class="icon-box-item">💡</div><div class="icon-label-item">Events</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div style='background:#1e252e; border-radius:12px; padding:15px; text-align:center; border:1px solid #2b333e;'><h3 style='margin:0 0 5px 0; color:#fff; font-size:18px;'>1,949,641.00</h3><small style='color:#a0aec0;'>Total users</small></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='background:#1e252e; border-radius:12px; padding:15px; text-align:center; border:1px solid #2b333e;'><h3 style='margin:0 0 5px 0; color:#ff6a00; font-size:18px;'>$31,337,652,065</h3><small style='color:#a0aec0;'>Total output</small></div>", unsafe_allow_html=True)
        
    st.markdown("<div style='font-size:14px; font-weight:700; margin:15px 0 8px 2px; color:#ff6a00; text-transform:uppercase;'>Withdraw log</div>", unsafe_allow_html=True)
    for log_item in generate_fake_withdrawals():
        st.markdown(f"<div style='background:#212730; padding:10px 15px; border-radius:10px; margin-bottom:8px; font-size:12px; border:1px solid #2c3440; display:flex; justify-content:space-between;'>{log_item}</div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:14px; font-weight:700; margin:15px 0 8px 2px; color:#a0aec0;'>Partners</div>", unsafe_allow_html=True)
    st.markdown("<div style='background:#1e252e; border-radius:12px; padding:12px; text-align:center; font-weight:700; font-size:12px; color:#ff6a00; border:1px solid #2b333e;'>BINANCE &nbsp;&bull;&nbsp; ETHEREUM &nbsp;&bull;&nbsp; BITMAIN &nbsp;&bull;&nbsp; TRON &nbsp;&bull;&nbsp; TETHER &nbsp;&bull;&nbsp; COINBASE</div>", unsafe_allow_html=True)

# --- TAB 2: VIP PANEL ---
elif st.session_state.active_tab == "VIP":
    st.markdown(f"""
    <div style="background:#212730; padding:15px; border-radius:14px; border:1px solid #2e3642; margin-bottom:15px;">
        <div style="display:flex; justify-content:space-between; font-size:13px; color:#a0aec0;"><span>Level</span><span style="color:#00ffcc; font-weight:700;">{vip_level}</span></div>
        <div style="display:flex; justify-content:space-between; font-size:13px; color:#a0aec0; margin-top:5px;"><span>Deposit amount</span><span style="color:#ff6a00; font-weight:700;">${invest_bal:,.2f}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='background:#ff6a00; color:#fff; text-align:center; padding:12px; font-weight:700; border-radius:10px; font-size:14px; box-shadow:0 4px 12px rgba(255,106,0,0.3); margin-bottom:20px;'>DEPOSIT TO UPGRADE</div>", unsafe_allow_html=True)
    
    for i in range(1, 6):
        min_amt = [0, 10, 100, 1000, 5000, 10000][i]
        max_amt = [0, 1000, 10000, 5000, 10000, 50000][i]
        yield_pct = [0, 30, 32, 34, 36, 38][i]
        
        st.markdown(f"""
        <div style="background:#1e252e; border-radius:12px; padding:15px; border:1px solid #2c3440; margin-bottom:12px;">
            <div style="font-weight:800; font-size:16px; color:#ff6a00; margin-bottom:8px;">VIP {i}</div>
            <div style="display:flex; justify-content:space-between; font-size:12px; padding:4px 0;"><span style="color:#a0aec0;">Deposit amount</span><span style="color:#fff; font-weight:600;">{min_amt:,.2f} ~ {max_amt:,.2f}</span></div>
            <div style="display:flex; justify-content:space-between; font-size:12px; padding:4px 0;"><span style="color:#a0aec0;">Mining income</span><span style="color:#00ffcc; font-weight:700;">{yield_pct:.2f}%</span></div>
            <div style="display:flex; justify-content:space-between; font-size:12px; padding:4px 0;"><span style="color:#a0aec0;">Mining window</span><span style="color:#00ffcc; font-weight:600;">364days</span></div>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 3: MINING FAN SIMULATOR ---
elif st.session_state.active_tab == "Mining":
    st.markdown("""
    <div class="fan-simulator-canvas">
        <div class="cooling-fan-hardware">
            <div class="fan-blades-wing"></div>
            <div class="fan-center-core">⚡</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background:#212730; padding:20px; border-radius:14px; border:1px solid #2e3642; text-align:center;">
        <h2 style="margin:0; font-size:28px; font-weight:800; color:#ffffff; letter-spacing:1px;">0.000000 <span style="font-size:12px; color:#ff6a00;">USDT</span></h2>
        <div style="width:100%; background:#171c24; height:8px; border-radius:4px; margin:15px 0; overflow:hidden;">
            <div style="background:linear-gradient(90deg, #ff8c00, #ff5500); width:45%; height:100%;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:12px; padding:4px 0;"><span style="color:#a0aec0;">Level</span><span style="background:#ff6a00; color:#fff; padding:1px 6px; border-radius:4px; font-size:10px; font-weight:700;">{vip_level}</span></div>
        <div style="display:flex; justify-content:space-between; font-size:12px; padding:4px 0;"><span style="color:#a0aec0;">Hashrate</span><span style="color:#fff; font-weight:600;">0.00 GH/s</span></div>
        <div style="display:flex; justify-content:space-between; font-size:12px; padding:4px 0;"><span style="color:#a0aec0;">Daily</span><span style="color:#fff; font-weight:600;">0.00 USDT</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    if st.button("BOOST HASHRATE", key="boost_hashrate_btn_action"):
        st.toast("Boosting lines...")

# --- TAB 4: TEAM / REFERRAL MANAGEMENT ---
elif st.session_state.active_tab == "Team":
    st.markdown(f"""
    <div style="background:#212730; padding:15px; border-radius:14px; border:1px solid #2e3642; position:relative;">
        <div style="position:absolute; right:15px; top:15px; background:linear-gradient(90deg, #ff8c00, #ff5500); color:#fff; font-size:11px; padding:4px 10px; font-weight:700; border-radius:12px;">Commission detail »</div>
        <div style="font-size:12px; color:#a0aec0; margin-top:15px;">Invite code:</div>
        <div style="display:flex; gap:10px; align-items:center; margin-top:4px;">
            <span style="font-size:22px; font-weight:800; color:#fff;">{user_invite}</span>
            <span style="background:#ff6a00; color:#fff; font-size:11px; padding:2px 8px; border-radius:4px; font-weight:700;">Copy</span>
        </div>
        <div style="font-size:12px; color:#a0aec0; margin-top:15px;">Share your link & earn:</div>
        <div style="background:#171c24; padding:8px 12px; border-radius:8px; font-size:11px; color:#cbd5e0; word-break:break-all; margin-top:5px; border:1px solid #2a313a;">
            https://nicehash.one/#/reg?invite_code={user_invite}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    t_c1, t_c2 = st.columns(2)
    with t_c1:
        st.markdown("<div style='background:#1e252e; padding:12px; border-radius:10px; border:1px solid #2c3440;'><small style='color:#a0aec0;'>Team size</small><h4 style='margin:5px 0 0 0; color:#fff;'>0</h4></div>", unsafe_allow_html=True)
        st.markdown("<div style='background:#1e252e; padding:12px; border-radius:10px; border:1px solid #2c3440; margin-top:10px;'><small style='color:#a0aec0;'>Team deposits</small><h4 style='margin:5px 0 0 0; color:#fff;'>$0</h4></div>", unsafe_allow_html=True)
    with t_c2:
        st.markdown("<div style='background:#1e252e; padding:12px; border-radius:10px; border:1px solid #2c3440;'><small style='color:#a0aec0;'>Ref commissions</small><h4 style='margin:5px 0 0 0; color:#fff;'>$0</h4></div>", unsafe_allow_html=True)
        st.markdown("<div style='background:#1e252e; padding:12px; border-radius:10px; border:1px solid #2c3440; margin-top:10px;'><small style='color:#a0aec0;'>Team withdrawals</small><h4 style='margin:5px 0 0 0; color:#fff;'>$0</h4></div>", unsafe_allow_html=True)

# --- TAB 5: ME / VAULT PROFILES ---
elif st.session_state.active_tab == "Me":
    if not st.session_state.logged_in:
        st.markdown("<h4 style='text-align:center; color:#ff6a00;'>SECURE TUNNEL ACCESS</h4>", unsafe_allow_html=True)
        u_in = st.text_input("Email / Phone Account:", placeholder="Enter account handle", key="nh_auth_username_field")
        p_in = st.text_input("Password Key:", type="password", placeholder="••••••••", key="nh_auth_password_field")
        if st.button("LOG IN NOW", key="execute_nh_login_gate_btn"):
            res = query_db("SELECT username FROM users WHERE username=? AND password=?", (u_in.strip(), p_in.strip()), one=True)
            if res:
                st.session_state.logged_in = True
                st.session_state.current_user = res[0]
                st.rerun()
            else: st.error("Invalid handle credentials.")
    else:
        st.markdown(f"""
        <div style="background:#212730; padding:15px; border-radius:14px; border:1px solid #2e3642; display:flex; align-items:center; gap:12px;">
            <div style="width:52px; height:52px; background:#3a4454; border-radius:50%; font-size:24px; line-height:52px; text-align:center;">👤</div>
            <div>
                <div style="font-weight:700; font-size:14px; color:#fff;">{st.session_state.current_user[:4]}****@gmail.com</div>
                <span style="background:#ff5500; color:#fff; font-size:10px; font-weight:800; padding:2px 8px; border-radius:10px;">{vip_level}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
        f_c1, f_c2 = st.columns(2)
        with f_c1:
            amount_dep = st.number_input("Deposit Value ($):", min_value=10.0, step=10.0, key="nh_deposit_value_field_cell")
            if st.button("SUBMIT INTENT", key="nh_deposit_submit_action_gate"):
                query_db("UPDATE users SET invest_wallet = invest_wallet + ? WHERE username=?", (amount_dep, st.session_state.current_user), commit=True)
                st.success("Deposit processed.")
                st.rerun()
        with f_c2:
            amount_wit = st.number_input("Withdraw Value ($):", min_value=10.0, step=10.0, key="nh_withdraw_value_field_cell")
            if st.button("EXTRACT ASSETS", key="nh_withdraw_submit_action_gate"):
                if invest_bal >= amount_wit:
                    query_db("UPDATE users SET invest_wallet = invest_wallet - ? WHERE username=?", (amount_wit, st.session_state.current_user), commit=True)
                    st.success("Withdrawal logged.")
                    st.rerun()
                else: st.error("Insufficient balance bounds.")
                
        st.markdown("<hr style='border-color:#2a313a;'>", unsafe_allow_html=True)
        if st.button("LOG OUT ENGINE", key="nh_logout_action_forced_btn"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.rerun()

# ==============================================================================
# --- 6. PREMIUM NAV BAR RENDERING AT THE BOTTOM ---
# ==============================================================================
st.markdown("<div style='margin-top:70px;'></div>", unsafe_allow_html=True)
# Safe inline menu bar rendering engine
nav_cols = st.columns(5)
with nav_cols[0]: 
    if st.button("🏠\nHome", key="nav_home_btn"): st.session_state.active_tab = "Home"; st.rerun()
with nav_cols[1]: 
    if st.button("👑\nVIP", key="nav_vip_btn"): st.session_state.active_tab = "VIP"; st.rerun()
with nav_cols[2]: 
    if st.button("⚡\nMining", key="nav_mining_btn"): st.session_state.active_tab = "Mining"; st.rerun()
with nav_cols[3]: 
    if st.button("👥\nTeam", key="nav_team_btn"): st.session_state.active_tab = "Team"; st.rerun()
with nav_cols[4]: 
    if st.button("👤\nMe", key="nav_me_btn"): st.session_state.active_tab = "Me"; st.rerun()
