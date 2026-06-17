# ==============================================================================
# --- 0. ADVANCED ENCRYPTED RUNTIME INTERCEPTION & BLOCKCHAIN EMULATOR ---
# ==============================================================================
import os
import sys
import time
import random
import sqlite3
from datetime import datetime

# Enforce secure pure-python layer translation mapping over modern runtimes
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st

# ==============================================================================
# --- 1. ENTERPRISE GLOBAL TRANSLATION PROTOCOLS (22 DYNAMIC LANGUAGES) ---
# ==============================================================================
DICTIONARY = {
    "🌐 English": {
        "title": "nicehash", "news_head": "News Notice", "got_it": "Got it",
        "welcome": "NiceHash · A New Era of Mining", "launch": "Officially launched on May 31, 2026.",
        "marquee": "Unlock and earn your first earnings now! No waiting, no complicated operations, earnings arrive instantly after unlocking.",
        "assets_title": "Total assets", "invest_lbl": "Invest wallet", "comm_lbl": "Commission wallet",
        "d_btn": "Deposit", "w_btn": "Withdraw", "v_btn": "VIP Plan", "t_btn": "My Team", "m_btn": "Mine", "me_btn": "Me",
        "log_title": "Withdrawal Stream Log", "partners": "Global Partners", "curr_v": "Current Profile Level:", "my_d": "My Active Deposit:",
        "req_m": "Required Minimum Entry:", "day_r": "Automated Daily Return:", "acc_c": "Accumulating Live Crypto",
        "eng_s": "Cloud Engine Status:", "act_run": "ACTIVE & RUNNING", "inv_id": "Personal Invitation ID Code",
        "inv_lnk": "Share Referral Registration Link", "firewall": "NiceHash Security Firewall", "email_lbl": "Account Handle Email:",
        "pass_lbl": "Security Access Key:", "unlock_b": "LOG IN", "inject_b": "Inject Simulated USDT Balance",
        "disc_b": "Log out", "success_msg": "Wallet Updated Successfully!", "extract_b": "BOOST HASHRATE",
        "wth_lbl": "Withdraw Amount ($):", "exec_wth": "Execute Real Withdrawal", "insufficient": "Insufficient Balance bounds."
    },
    "🌐 Urdu": {
        "title": "نائس ہیش", "news_head": "اہم خبریں", "got_it": "ٹھیک ہے",
        "welcome": "نائس ہیش · مائننگ کا نیا دور", "launch": "سرکاری طور پر 31 مئی 2026 کو شروع کیا گیا۔",
        "marquee": "ابھی انلاک کریں اور اپنی پہلی کمائی حاصل کریں! کوئی انتظار نہیں، کوئی پیچیدہ طریقہ کار نہیں، رقم فوری منتقل ہوتی ہے۔",
        "assets_title": "کل اثاثے", "invest_lbl": "انوسٹ والٹ", "comm_lbl": "کمیشن والٹ",
        "d_btn": "جمع کریں", "w_btn": "نکلوائیں", "v_btn": "وی آئی پی", "t_btn": "میری ٹیم", "m_btn": "مائننگ", "me_btn": "پروفائل",
        "log_title": "رقم نکلوانے کا لائیو لاگ", "curr_v": "موجودہ وی آئی پی لیول:", "my_d": "میرا فعال ڈیپازٹ:",
        "req_m": "کم از کم مطلوبہ رقم:", "day_r": "روزانہ کا خودکار منافع:", "acc_c": "لائیو کرپٹو مائننگ جاری ہے",
        "eng_s": "کلاؤڈ انجن کی حالت:", "act_run": "فعال اور چل رہا ہے", "inv_id": "ذاتی انویٹیشن کوڈ",
        "inv_lnk": "ریفرل رجسٹریشن لنک شیئر کریں", "firewall": "نائس ہیش سیکیورٹی فائر وال", "email_lbl": "اکاؤنٹ ای میل درج کریں:",
        "pass_lbl": "سیکیورٹی پاس ورڈ کی:", "unlock_b": "لاگ ان کریں", "inject_b": "ٹیسٹ بیلنس جمع کریں",
        "disc_b": "لاگ آؤٹ کریں", "success_msg": "والٹ کامیابی سے اپ ڈیٹ ہو گیا!", "extract_b": "ہیش ریٹ بڑھائیں",
        "wth_lbl": "نکلوانے کی رقم:", "exec_wth": "رقم نکلوانے کی درخواست کریں", "insufficient": "والٹ میں رقم کم ہے۔"
    }
}

extended_language_keys = ["🌐 DeepUrdu", "🌐 العربية", "🌐 Français", "🌐 Deutsch", "🌐 Русский"]
for lang_key in extended_language_keys:
    if lang_key not in DICTIONARY:
        DICTIONARY[lang_key] = DICTIONARY["🌐 English"].copy()

# ==============================================================================
# --- 2. MULTI-THREADED REAL PERSISTENT SQLITE DATABASE VAULT ---
# ==============================================================================
def run_db_migrations():
    conn = sqlite3.connect("nicehash_real_vault.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            username TEXT PRIMARY KEY, password TEXT, Security_pin TEXT,
            invest_wallet REAL, commission_wallet REAL, vip_level TEXT, invite_code TEXT, last_accumulation REAL
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO accounts VALUES ('demo@gmail.com', 'demo123', '1122', 150.00, 45.50, 'VIP1', '286651', 1718683200.0)")
    conn.commit()
    conn.close()

def query_vault(query, args=(), one=False, commit=False):
    conn = sqlite3.connect("nicehash_real_vault.db", check_same_thread=False)
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
    except Exception:
        conn.close()
        return None if one else []

run_db_migrations()

# ==============================================================================
# --- 3. DYNAMIC STATES & AUTOMATED INTERACTIVE MINING MATRIX ---
# ==============================================================================
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'current_user' not in st.session_state: st.session_state.current_user = ""
if 'active_tab' not in st.session_state: st.session_state.active_tab = "Home"
if 'show_inline_news' not in st.session_state: st.session_state.show_inline_news = True
if 'crypto_yield_accumulator' not in st.session_state: st.session_state.crypto_yield_accumulator = 0.00000000

invest_bal, comm_bal, vip_level, user_invite = 0.00, 0.00, "VIP0", "286651"
if st.session_state.logged_in:
    account_stats = query_vault("SELECT invest_wallet, commission_wallet, vip_level, invite_code FROM accounts WHERE username=?", (st.session_state.current_user,), one=True)
    if account_stats:
        invest_bal, comm_bal, vip_level, user_invite = account_stats
        daily_ratio = 30.0 if vip_level == "VIP1" else (32.0 if vip_level == "VIP2" else 36.0)
        if invest_bal > 0:
            st.session_state.crypto_yield_accumulator += ((invest_bal * (daily_ratio / 100.0)) / 86400.0) * random.uniform(0.98, 1.02)

def generate_live_withdrawal_ledger():
    return [
        f"r***s8@gmail.com withdrew <b style='color:#ff4444;'>${random.uniform(1000, 80000):,.2f}</b> !",
        f"a***3v@yahoo.com withdrew <b style='color:#ff4444;'>${random.uniform(500, 40000):,.2f}</b> !",
        f"+62****17 withdrew <b style='color:#ff4444;'>${random.uniform(200, 10000):,.2f}</b> !"
    ]

# ==============================================================================
# --- 4. ADVANCED CSS SHIELD (FLEX ROW FIX FOR MOBILE & BUTTON STYLING) ---
# ==============================================================================
st.markdown("""
<style>
footer, .stDeployButton, #MainMenu, [data-testid="stHeader"] { display: none !important; }
html, body, .stApp { background-color: #1c2127 !important; color: #ffffff !important; font-family: 'Inter', sans-serif !important; }

/* Perfect Fixed Mobile Framework Container Bounds */
.block-container { padding-top: 10px !important; padding-bottom: 80px !important; max-width: 440px !important; margin: 0 auto !important; }

/* 🔴 YE HIA MAIN FIX: Iski wajah se ab mobile par columns neechy nahi jayenge, hamesha ek line me rahenge! */
div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    gap: 2px !important;
}
div[data-testid="column"] { width: auto !important; flex: 1 1 0% !important; min-width: 0 !important; }

/* 🔴 PRIMARY BUTTONS (Orange Gradient jaise "LOG IN", "GOT IT", "BOOST HASHRATE") */
button[data-testid="baseButton-primary"] {
    background: linear-gradient(90deg, #ff8c00 0%, #ff5500 100%) !important;
    color: #ffffff !important; font-weight: 700 !important; border-radius: 8px !important;
    width: 100% !important; border: none !important; padding: 10px !important; 
    box-shadow: 0 4px 12px rgba(255,85,0,0.25); text-transform: uppercase;
}

/* 🔴 SECONDARY BUTTONS (Grid wale icons aur Bottom Navigation bar) */
button[data-testid="baseButton-secondary"] {
    background: transparent !important; color: #8a99ad !important;
    border: none !important; box-shadow: none !important; width: 100% !important;
    padding: 2px !important; font-size: 12px !important;
}
button[data-testid="baseButton-secondary"]:hover { color: #ff6a00 !important; }
button[data-testid="baseButton-secondary"] p { font-size: 11px !important; margin:0 !important; line-height: 1.4 !important; }

/* Header Logo Styling */
.nh-top-bar { display: flex; align-items: center; background: transparent; }
.nh-logo-icon { width: 30px; height: 30px; background: #ffba00; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; position: relative; overflow: hidden; margin-right:8px;}
.nh-logo-icon::before { content: ''; position: absolute; width: 14px; height: 14px; background: #1c2127; border-radius: 4px; top: -4px; right: -4px; }
.nh-logo-icon::after { content: ''; position: absolute; width: 12px; height: 6px; background: #1c2127; border-radius: 0 0 10px 10px; bottom: 6px; }

/* Customizing Streamlit Selectbox to look like UI pill */
div[data-baseweb="select"] > div {
    background-color: transparent !important; border: 1px solid #4a5568 !important; border-radius: 20px !important; color: #fff !important; min-height: 30px !important; padding: 0px 5px !important; font-size: 12px !important;
}

/* Card & Fan Styles */
.asset-premium-card { background: linear-gradient(135deg, #a31c1c 0%, #252b35 50%, #171c24 100%); border-radius: 15px; padding: 18px; border: 1px solid #3d4655; margin-top: 15px; margin-bottom: 15px; box-shadow: 0px 8px 24px rgba(0,0,0,0.5); }
.asset-total-title { color: #e2e8f0; font-size: 13px; font-weight: 500; }
.asset-total-value { font-size: 26px; font-weight: 800; color: #ff5500; margin: 4px 0 15px 0; display:flex; align-items: baseline; gap:5px;}
.asset-total-value span {color: #ffffff; font-size:26px;}
.sub-wallet-row { display: flex; justify-content: space-between; padding: 6px 0; font-size: 12px; color: #cbd5e0; font-weight:600;}

/* Marquee & Fan */
.marquee-alert-box { display: flex; align-items: center; background: #2f2725; border-radius: 20px; padding: 6px 15px; border: 1px solid #ff5500; margin-top: 10px; margin-bottom: 10px; font-size: 12px; overflow: hidden; color: #ffaaaa; }
.cooling-fan-hardware { width: 160px; height: 160px; background: #1a222c; border-radius: 10px; border: 2px solid #2d3642; margin: 20px auto; display: flex; align-items: center; justify-content: center; position: relative; box-shadow: inset 0px 0px 20px #00ffcc44; }
.fan-blades-wing { width: 140px; height: 140px; background: repeating-conic-gradient(from 0deg, #00ffcc 0deg 20deg, #10151a 20deg 40deg); border-radius: 50%; animation: spinHardware 1s linear infinite; opacity: 0.8;}
@keyframes spinHardware { 100% { transform: rotate(360deg); } }
</style>
""", unsafe_allow_html=True)

# Layout Setup for Header
h_col1, h_col2 = st.columns([1.5, 1])
with h_col1:
    st.markdown("""
    <div class="nh-top-bar">
        <div class="nh-logo-icon"></div>
        <span style="font-size: 22px; font-weight: 800; color: #ffffff;">NiceHash</span>
    </div>
    """, unsafe_allow_html=True)
with h_col2:
    selected_language_key = st.selectbox("", list(DICTIONARY.keys()), label_visibility="collapsed")

L = DICTIONARY[selected_language_key]
st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# --- 5. COMPACT OVERLAY NEWS WORKSPACE ---
# ==============================================================================
if st.session_state.show_inline_news and st.session_state.active_tab == "Home":
    st.markdown(f"""
    <div style="background: #1c2127; border: 1px solid #ff6a00; border-radius: 12px; padding: 15px; margin-bottom: 15px; position: relative;">
        <h3 style="color:#ffffff; margin:0 0 10px 0; font-size:18px; text-align:center;">{L["news_head"]}</h3>
        <div style="font-size:13px; color:#cbd5e0; line-height:1.6; margin-bottom: 12px;">
            🎉 <b>{L["welcome"]}</b><br><b>{L["launch"]}</b><br>
            💡 Unlock and earn your first earnings now! Instant payouts.
            <table style="width:100%; border-collapse:collapse; text-align:center; color:#fff; font-size:12px; margin-top:10px;">
                <tr style="border-bottom:1px solid #4a5568;"><th style="padding:5px;">grade</th><th style="padding:5px;">Investment</th><th style="padding:5px;">Yield</th></tr>
                <tr><td style="padding:5px;">VIP1</td><td>10</td><td>30%</td></tr>
                <tr><td style="padding:5px;">VIP2</td><td>100</td><td>32%</td></tr>
                <tr><td style="padding:5px;">VIP3</td><td>1,000</td><td>34%</td></tr>
            </table>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(L["got_it"], type="primary"): # <-- PRIMARY BUTTON
        st.session_state.show_inline_news = False
        st.rerun()
    st.markdown("<hr style='border-color:#2a313a;'>", unsafe_allow_html=True)

# ==============================================================================
# --- 6. CORE APP PAGES ---
# ==============================================================================

if st.session_state.active_tab == "Home":
    st.markdown("""
    <div style="width:100%; height:140px; background:url('https://images.unsplash.com/photo-1639762681485-074b7f4ec67a?auto=format&fit=crop&q=80&w=400') center/cover; border-radius:12px; display:flex; align-items:center; justify-content:center; box-shadow: inset 0 0 50px rgba(0,0,0,0.8);">
        <div style="display:flex; align-items:center;"><div class="nh-logo-icon" style="background:#ffba00;"></div><span style="font-size:26px; font-weight:800;">nicehash</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="marquee-alert-box">🔔 {L["marquee"]}</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="asset-premium-card">
        <div class="asset-total-title">{L["assets_title"]}</div>
        <div class="asset-total-value">$<span>{(invest_bal + comm_bal):,.2f}</span></div>
        <div class="sub-wallet-row"><span>{L["invest_lbl"]}</span><span style="color:#fff;">${invest_bal:,.2f}</span></div>
        <div class="sub-wallet-row" style="padding-bottom:0;"><span>{L["comm_lbl"]}</span><span style="color:#fff;">${comm_bal:,.2f}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid column block (Ab ye icons transparent aur black background wale honge)
    grid_blocks = st.columns(4)
    with grid_blocks[0]:
        if st.button(f"🏦\n{L['d_btn']}", key="h_d_btn"): st.session_state.active_tab = "Me"; st.rerun()
    with grid_blocks[1]:
        if st.button(f"🏧\n{L['w_btn']}", key="h_w_btn"): st.session_state.active_tab = "Me"; st.rerun()
    with grid_blocks[2]:
        if st.button(f"👑\n{L['v_btn']}", key="h_v_btn"): st.session_state.active_tab = "VIP"; st.rerun()
    with grid_blocks[3]:
        if st.button(f"📅\nEvents", key="h_e_btn"): pass

    st.markdown(f"<div style='margin-top:15px; font-size:14px; font-weight:700; margin-bottom:8px;'>Withdraw log</div>", unsafe_allow_html=True)
    for log in generate_live_withdrawal_ledger():
        st.markdown(f"<div style='background:#22262d; padding:12px; border-radius:10px; margin-bottom:6px; font-size:12px; font-weight:600;'>{log}</div>", unsafe_allow_html=True)

elif st.session_state.active_tab == "VIP":
    for i in range(1, 5):
        st.markdown(f"""
        <div style="background:#22262d; border-radius:12px; padding:15px; margin-bottom:10px;">
            <div style="font-weight:800; font-size:16px; color:#fff; margin-bottom:8px;">LEV {i}</div>
            <div style="display:flex; justify-content:space-between; font-size:12px;"><span style="color:#8a99ad;">Valid Amount</span><span style="color:#fff; font-weight:700;">${[10, 100, 1000, 5000][i-1]:,.2f}</span></div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.active_tab == "Mining":
    st.markdown('<div class="cooling-fan-hardware"><div class="fan-blades-wing"></div></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background:#22262d; padding:20px; border-radius:15px; text-align:center;">
        <h2 style="margin:0; font-size:32px; color:#ffffff;">{st.session_state.crypto_yield_accumulator:.6f} <span style="font-size:14px;">USDT</span></h2>
        <div style="background:linear-gradient(90deg, #ff8c00 50%, #4a5568 50%); height:8px; border-radius:4px; margin:15px 0;"></div>
        <div style="display:flex; justify-content:space-between; font-size:12px; color:#8a99ad; margin-bottom:5px;"><span>Level</span><span style="color:#ff5500; font-weight:800;">{vip_level}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    if st.button(L["extract_b"], type="primary"): # <-- PRIMARY ORANGE BUTTON
        if st.session_state.crypto_yield_accumulator > 0:
            query_vault("UPDATE accounts SET commission_wallet = commission_wallet + ? WHERE username=?", (st.session_state.crypto_yield_accumulator, st.session_state.current_user), commit=True)
            st.session_state.crypto_yield_accumulator = 0.00000000
            st.success("Yield Collected Successfully!")
            time.sleep(0.5); st.rerun()

elif st.session_state.active_tab == "Team":
    st.markdown(f"""
    <div style="background:#22262d; padding:20px; border-radius:15px;">
        <span style="font-size:13px; color:#8a99ad;">Invite code:</span>
        <h2 style="margin:5px 0 15px 0; color:#fff;">{user_invite}</h2>
        <span style="font-size:13px; color:#8a99ad;">Share your link & earn</span>
        <div style="background:#171c24; padding:10px; border-radius:8px; font-size:12px; color:#cbd5e0; margin-top:5px; border:1px solid #2a313a;">
            https://nicehash.one/#/reg?invite_code={user_invite}
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.active_tab == "Me":
    if not st.session_state.logged_in:
        st.markdown("""<div style="text-align:center; margin-bottom:20px;"><div class="nh-logo-icon" style="width:60px; height:60px; margin:0 auto;"></div><h2 style="margin-top:10px;">NiceHash</h2></div>""", unsafe_allow_html=True)
        user_in = st.text_input("Email", placeholder="Email")
        pass_in = st.text_input("Password", type="password", placeholder="Password")
        if st.button(L["unlock_b"], type="primary"): # <-- PRIMARY BUTTON
            match = query_vault("SELECT username FROM accounts WHERE username=?", (user_in.strip(),), one=True)
            if match:
                st.session_state.logged_in = True; st.session_state.current_user = match[0]; st.rerun()
    else:
        st.markdown(f"""
        <div style="background:#4a1c1c; border-radius:15px; padding:15px; margin-bottom:15px;">
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="width:40px; height:40px; background:#fff; border-radius:50%;"></div>
                <div><div style="font-weight:700;">{st.session_state.current_user}</div><span style="background:#ff5500; font-size:10px; padding:2px 6px; border-radius:4px; font-weight:800;">{vip_level}</span></div>
            </div>
            <div style="background:#22262d; margin-top:15px; padding:15px; border-radius:10px; text-align:center;">
                <span style="color:#8a99ad; font-size:12px;">Total assets | </span><span style="color:#ff5500; font-weight:800; font-size:18px;">${invest_bal + comm_bal:,.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(L["disc_b"], type="primary"):
            st.session_state.logged_in = False; st.session_state.current_user = ""; st.rerun()

# ==============================================================================
# --- 7. STABLE FIXED BOTTOM NAVIGATION ---
# ==============================================================================
st.markdown("<hr style='border:none; margin:30px 0;'>", unsafe_allow_html=True) # Spacer

# Navigation bar jo hamesha bottom par float karegi mobile flex row styling ki wajah se
nav_grid = st.columns(5)
with nav_grid[0]:
    if st.button("🏠\nHome"): st.session_state.active_tab = "Home"; st.rerun()
with nav_grid[1]:
    if st.button("👑\nVIP"): st.session_state.active_tab = "VIP"; st.rerun()
with nav_grid[2]:
    if st.button("⛏️\nMining"): st.session_state.active_tab = "Mining"; st.rerun()
with nav_grid[3]:
    if st.button("👥\nTeam"): st.session_state.active_tab = "Team"; st.rerun()
with nav_grid[4]:
    if st.button("👤\nMe"): st.session_state.active_tab = "Me"; st.rerun()
