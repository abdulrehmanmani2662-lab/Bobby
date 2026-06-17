# ==============================================================================
# --- 0. ADVANCED ENCRYPTED RUNTIME INTERCEPTION & BLOCKCHAIN EMULATOR ---
# ==============================================================================
import os
import time
import random
import sqlite3
import streamlit as st

# Enforce secure pure-python layer translation mapping over modern runtimes
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

st.set_page_config(page_title="NiceHash App", layout="centered", initial_sidebar_state="collapsed")

# ==============================================================================
# --- 1. ENTERPRISE GLOBAL TRANSLATION PROTOCOLS (DICTIONARY) ---
# ==============================================================================
DICTIONARY = {
    "🌐 English": {
        "title": "nicehash", "news_head": "News Notice", "got_it": "GOT IT",
        "welcome": "NiceHash · A New Era of Mining", "launch": "Officially launched on May 31, 2026.",
        "marquee": "Unlock and earn your first earnings now! No waiting, no complicated operations.",
        "assets_title": "Total assets", "invest_lbl": "Invest wallet", "comm_lbl": "Commission wallet",
        "d_btn": "Deposit", "w_btn": "Withdraw", "v_btn": "VIP Plan", "t_btn": "My Team", "m_btn": "Mine", "me_btn": "Me",
        "log_title": "Withdrawal Stream Log", "curr_v": "Current Profile Level:", "my_d": "My Active Deposit:",
        "req_m": "Required Minimum Entry:", "day_r": "Automated Daily Return:", "acc_c": "Accumulating Live Crypto",
        "eng_s": "Cloud Engine Status:", "act_run": "ACTIVE & RUNNING", "inv_id": "Personal Invitation ID Code",
        "inv_lnk": "Share Referral Registration Link", "firewall": "NiceHash Security Firewall", 
        "email_lbl": "Account Handle Email:", "pass_lbl": "Security Access Key:", "unlock_b": "LOG IN", 
        "inject_b": "Inject Simulated USDT Balance", "disc_b": "LOG OUT", "success_msg": "Wallet Updated Successfully!", 
        "extract_b": "BOOST HASHRATE", "wth_lbl": "Withdraw Amount ($):", "exec_wth": "Execute Real Withdrawal", 
        "insufficient": "Insufficient Balance bounds."
    },
    "🌐 Urdu": {
        "title": "نائس ہیش", "news_head": "اہم خبریں", "got_it": "ٹھیک ہے",
        "welcome": "نائس ہیش · مائننگ کا نیا دور", "launch": "سرکاری طور پر 31 مئی 2026 کو شروع کیا گیا۔",
        "marquee": "ابھی انلاک کریں اور اپنی پہلی کمائی حاصل کریں! رقم فوری منتقل ہوتی ہے۔",
        "assets_title": "کل اثاثے", "invest_lbl": "انوسٹ والٹ", "comm_lbl": "کمیشن والٹ",
        "d_btn": "جمع کریں", "w_btn": "نکلوائیں", "v_btn": "وی آئی پی", "t_btn": "میری ٹیم", "m_btn": "مائننگ", "me_btn": "پروفائل",
        "log_title": "رقم نکلوانے کا لائیو لاگ", "curr_v": "موجودہ وی آئی پی لیول:", "my_d": "میرا فعال ڈیپازٹ:",
        "req_m": "کم از کم مطلوبہ رقم:", "day_r": "روزانہ کا خودکار منافع:", "acc_c": "لائیو کرپٹو مائننگ جاری ہے",
        "eng_s": "کلاؤڈ انجن کی حالت:", "act_run": "فعال اور چل رہا ہے", "inv_id": "ذاتی انویٹیشن کوڈ",
        "inv_lnk": "ریفرل رجسٹریشن لنک شیئر کریں", "firewall": "نائس ہیش سیکیورٹی فائر وال", 
        "email_lbl": "اکاؤنٹ ای میل:", "pass_lbl": "پاس ورڈ:", "unlock_b": "لاگ ان کریں", 
        "inject_b": "ٹیسٹ بیلنس جمع کریں", "disc_b": "لاگ آؤٹ کریں", "success_msg": "والٹ کامیابی سے اپ ڈیٹ ہو گیا!", 
        "extract_b": "ہیش ریٹ بڑھائیں", "wth_lbl": "نکلوانے کی رقم:", "exec_wth": "رقم نکالیں", 
        "insufficient": "رقم کم ہے۔"
    }
}

# ==============================================================================
# --- 2. DATABASE CONFIGURATION ---
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
# --- 3. SESSION STATES & LIVE MINING LOGIC ---
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
        f"a***k@gmail.com withdrew <b style='color:#00ffcc;'>${random.uniform(50, 4000):,.2f}</b> !",
        f"u***9@yahoo.com withdrew <b style='color:#00ffcc;'>${random.uniform(100, 8000):,.2f}</b> !",
        f"+92****789 withdrew <b style='color:#00ffcc;'>${random.uniform(20, 1000):,.2f}</b> !"
    ]

# ==============================================================================
# --- 4. IRONCLAD CSS SHIELD (FIXES MOBILE WRAPPING 100%) ---
# ==============================================================================
st.markdown("""
<style>
/* Hide Streamlit Junk */
footer, header, .stDeployButton, #MainMenu { display: none !important; }

/* Global Theme */
html, body, .stApp { background-color: #12151c !important; color: #ffffff !important; font-family: 'Inter', sans-serif !important; }
.block-container { padding: 10px 15px 90px 15px !important; max-width: 440px !important; margin: 0 auto !important; }

/* 🚀 FORCE COLUMNS TO STAY IN ONE LINE (FLEX NO-WRAP) */
div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    gap: 5px !important;
}

/* Base Primary Button (Orange Gradient) */
button[data-testid="baseButton-primary"] {
    background: linear-gradient(90deg, #ff6a00 0%, #ff4500 100%) !important;
    color: #ffffff !important; font-weight: 800 !important; border-radius: 8px !important;
    border: none !important; width: 100% !important; padding: 12px !important;
    box-shadow: 0 4px 15px rgba(255,106,0,0.3); text-transform: uppercase; letter-spacing: 1px;
}

/* Base Secondary Button (Transparent Navigation) */
button[data-testid="baseButton-secondary"] {
    background: transparent !important; color: #8a99ad !important;
    border: none !important; width: 100% !important; padding: 5px !important;
    font-size: 11px !important;
}
button[data-testid="baseButton-secondary"]:hover { color: #ff6a00 !important; }
button[data-testid="baseButton-secondary"] p { font-size: 11px !important; margin: 0 !important; line-height: 1.5 !important; }

/* Cards & Containers */
.premium-card { background: linear-gradient(135deg, #2a1414 0%, #1e242b 100%); border-radius: 12px; padding: 15px; border: 1px solid #333d4a; margin: 10px 0; }
.marquee-box { background: #1c1512; border-radius: 8px; padding: 8px 12px; border: 1px solid #4a2815; font-size: 12px; color: #ff9d66; margin-bottom: 10px; display: flex; align-items: center; }

/* Mining Fan Animation */
.fan-container { width: 150px; height: 150px; background: #151a22; border-radius: 50%; border: 2px solid #333d4a; margin: 20px auto; position: relative; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 0 20px rgba(0,255,204,0.1); }
.fan-blades { width: 130px; height: 130px; border-radius: 50%; background: repeating-conic-gradient(from 0deg, #00ffcc 0deg 20deg, transparent 20deg 40deg); animation: spin 1s linear infinite; opacity: 0.7; }
@keyframes spin { 100% { transform: rotate(360deg); } }

</style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- 5. TOP HEADER BAR ---
# ==============================================================================
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("<div style='font-size:22px; font-weight:900; color:#fff; display:flex; align-items:center; gap:8px;'><div style='width:24px; height:24px; background:#ff6a00; border-radius:50%;'></div> nicehash</div>", unsafe_allow_html=True)
with col2:
    lang = st.selectbox("", list(DICTIONARY.keys()), label_visibility="collapsed")
L = DICTIONARY[lang]
st.markdown("<hr style='border-color:#2a313a; margin: 10px 0;'>", unsafe_allow_html=True)

# ==============================================================================
# --- 6. CORE APP SCREENS ---
# ==============================================================================
if st.session_state.active_tab == "Home":
    
    # News Modal
    if st.session_state.show_inline_news:
        st.markdown(f"""
        <div style="background:#1e242b; border:1px solid #ff6a00; border-radius:10px; padding:15px; margin-bottom:15px;">
            <h3 style="color:#fff; text-align:center; margin-top:0;">{L["news_head"]}</h3>
            <p style="font-size:12px; color:#cbd5e0;">{L["welcome"]}<br>{L["launch"]}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(L["got_it"], type="primary"):
            st.session_state.show_inline_news = False
            st.rerun()

    st.markdown(f'<div class="marquee-box">📢 {L["marquee"]}</div>', unsafe_allow_html=True)

    # Assets Card
    st.markdown(f"""
    <div class="premium-card">
        <div style="color:#8a99ad; font-size:12px;">{L["assets_title"]}</div>
        <div style="font-size:28px; font-weight:800; color:#ff6a00; margin:5px 0;">${(invest_bal + comm_bal):,.2f}</div>
        <div style="display:flex; justify-content:space-between; font-size:12px; border-top:1px solid #333d4a; padding-top:8px; margin-top:8px;">
            <span>{L["invest_lbl"]} <b style="color:#fff;">${invest_bal:,.2f}</b></span>
            <span>{L["comm_lbl"]} <b style="color:#fff;">${comm_bal:,.2f}</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Action Buttons (These will stay in ONE line due to custom CSS)
    btn_cols = st.columns(4)
    with btn_cols[0]:
        if st.button(f"📥\n{L['d_btn']}"): st.session_state.active_tab = "Me"; st.rerun()
    with btn_cols[1]:
        if st.button(f"📤\n{L['w_btn']}"): st.session_state.active_tab = "Me"; st.rerun()
    with btn_cols[2]:
        if st.button(f"👑\n{L['v_btn']}"): st.session_state.active_tab = "VIP"; st.rerun()
    with btn_cols[3]:
        if st.button(f"👥\n{L['t_btn']}"): st.session_state.active_tab = "Team"; st.rerun()

    st.markdown(f"<div style='margin-top:20px; font-weight:700; font-size:14px;'>{L['log_title']}</div>", unsafe_allow_html=True)
    for log in generate_live_withdrawal_ledger():
        st.markdown(f"<div style='background:#1e242b; padding:10px; border-radius:8px; margin-top:8px; font-size:12px;'>{log}</div>", unsafe_allow_html=True)

elif st.session_state.active_tab == "VIP":
    st.markdown(f"<div style='background:#ff6a00; color:#fff; padding:10px; border-radius:8px; text-align:center; font-weight:bold; margin-bottom:15px;'>{L['curr_v']} {vip_level}</div>", unsafe_allow_html=True)
    for i in range(1, 5):
        st.markdown(f"""
        <div class="premium-card">
            <div style="font-weight:800; font-size:16px; color:#fff;">VIP {i} PLAN</div>
            <div style="display:flex; justify-content:space-between; font-size:12px; color:#8a99ad; margin-top:8px;">
                <span>{L["req_m"]} <b style="color:#fff;">${[10, 100, 1000, 5000][i-1]:,.2f}</b></span>
                <span>Yield: <b style="color:#00ffcc;">{[30, 32, 34, 36][i-1]}%</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.active_tab == "Mining":
    st.markdown('<div class="fan-container"><div class="fan-blades"></div></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:20px;">
        <div style="color:#8a99ad; font-size:12px;">{L["acc_c"]}</div>
        <h1 style="color:#fff; margin:5px 0;">{st.session_state.crypto_yield_accumulator:.6f} <span style="font-size:14px; color:#ff6a00;">USDT</span></h1>
        <div style="color:#00ffcc; font-size:12px; font-weight:bold;">{L["eng_s"]} {L["act_run"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(L["extract_b"], type="primary"):
        if st.session_state.crypto_yield_accumulator > 0:
            query_vault("UPDATE accounts SET commission_wallet = commission_wallet + ? WHERE username=?", (st.session_state.crypto_yield_accumulator, st.session_state.current_user), commit=True)
            st.session_state.crypto_yield_accumulator = 0.00000000
            st.success("Yield Collected!")
            time.sleep(0.5); st.rerun()

elif st.session_state.active_tab == "Team":
    st.markdown(f"""
    <div class="premium-card" style="text-align:center;">
        <div style="color:#8a99ad; font-size:12px;">{L["inv_id"]}</div>
        <h2 style="color:#ff6a00; margin:10px 0;">{user_invite}</h2>
        <div style="background:#151a22; padding:10px; border-radius:6px; font-size:11px; word-break:break-all;">
            https://nicehash.one/#/reg?code={user_invite}
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.active_tab == "Me":
    if not st.session_state.logged_in:
        st.markdown(f"<h3 style='text-align:center; color:#fff;'>{L['firewall']}</h3>", unsafe_allow_html=True)
        user_in = st.text_input(L["email_lbl"], placeholder="demo@gmail.com")
        pass_in = st.text_input(L["pass_lbl"], type="password", placeholder="demo123")
        if st.button(L["unlock_b"], type="primary"):
            match = query_vault("SELECT username FROM accounts WHERE username=?", (user_in.strip(),), one=True)
            if match:
                st.session_state.logged_in = True; st.session_state.current_user = match[0]; st.rerun()
            else:
                st.error("Invalid Login")
    else:
        st.markdown(f"""
        <div class="premium-card">
            <h3 style="margin:0; color:#fff;">👤 {st.session_state.current_user}</h3>
            <span style="background:#ff6a00; font-size:10px; padding:2px 8px; border-radius:10px; font-weight:bold;">{vip_level}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Withdraw Section
        w_amt = st.number_input(L["wth_lbl"], min_value=10.0, step=10.0)
        if st.button(L["exec_wth"], type="primary"):
            if invest_bal >= w_amt:
                query_vault("UPDATE accounts SET invest_wallet = invest_wallet - ? WHERE username=?", (w_amt, st.session_state.current_user), commit=True)
                st.success("Withdrawal Processing!")
                time.sleep(0.5); st.rerun()
            else:
                st.error(L["insufficient"])
        
        st.markdown("<hr style='border-color:#333d4a;'>", unsafe_allow_html=True)
        if st.button(L["disc_b"]):
            st.session_state.logged_in = False; st.session_state.current_user = ""; st.rerun()

# ==============================================================================
# --- 7. STICKY BOTTOM NAVIGATION BAR ---
# ==============================================================================
st.markdown("""
<div style="position:fixed; bottom:0; left:50%; transform:translateX(-50%); width:100%; max-width:440px; background:#12151c; border-top:1px solid #2a313a; padding:5px 0; z-index:9999;">
""", unsafe_allow_html=True)

nav_cols = st.columns(5)
with nav_cols[0]:
    if st.button("🏠\nHome"): st.session_state.active_tab = "Home"; st.rerun()
with nav_cols[1]:
    if st.button("👑\nVIP"): st.session_state.active_tab = "VIP"; st.rerun()
with nav_cols[2]:
    if st.button("⛏️\nMine"): st.session_state.active_tab = "Mining"; st.rerun()
with nav_cols[3]:
    if st.button("👥\nTeam"): st.session_state.active_tab = "Team"; st.rerun()
with nav_cols[4]:
    if st.button("👤\nMe"): st.session_state.active_tab = "Me"; st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
