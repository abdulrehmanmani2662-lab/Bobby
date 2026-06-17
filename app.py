# ==============================================================================
# --- 0. ADVANCED ENCRYPTED RUNTIME INTERCEPTION & BLOCKCHAIN EMULATOR ---
# ==============================================================================
import os
import sys
import time
import random
import sqlite3
from datetime import datetime

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
        "pass_lbl": "Security Access Key:", "unlock_b": "Unlock Vault Workspace", "inject_b": "Inject Simulated USDT Balance",
        "disc_b": "Disconnect Terminal Session", "success_msg": "Wallet Updated Successfully!", "extract_b": "Collect & Flush Yield",
        "wth_lbl": "Withdraw Amount ($):", "exec_wth": "Execute Real Withdrawal", "insufficient": "Insufficient Balance bounds."
    },
    "🌐 Urdu": {
        "title": "نائس ہیش", "news_head": "اہم خبریں", "got_it": "ٹھیک ہے",
        "welcome": "نائس ہیش · مائننگ کا نیا دور", "launch": "سرکاری طور پر 31 مئی 2026 کو شروع کیا گیا۔",
        "marquee": "ابھی انلاک کریں اور اپنی پہلی کمائی حاصل کریں! کوئی انتظار نہیں، کوئی پیچیدہ طریقہ کار نہیں، رقم فوری منتقل ہوتی ہے۔",
        "assets_title": "کل اثاثے", "invest_lbl": "انوسٹ والٹ", "comm_lbl": "کمیشن والٹ",
        "d_btn": "جمع کریں", "w_btn": "نکلوائیں", "v_btn": "وی آئی پی پلان", "t_btn": "میری ٹیم", "m_btn": "مائننگ", "me_btn": "پروفائل",
        "log_title": "رقم نکلوانے کا لائیو لاگ", "partners": "عالمی شراکت دار", "curr_v": "موجودہ وی آئی پی لیول:", "my_d": "میرا فعال ڈیپازٹ:",
        "req_m": "کم از کم مطلوبہ رقم:", "day_r": "روزانہ کا خودکار منافع:", "acc_c": "لائیو کرپٹو مائننگ جاری ہے",
        "eng_s": "کلاؤڈ انجن کی حالت:", "act_run": "فعال اور چل رہا ہے", "inv_id": "ذاتی انویٹیشن کوڈ",
        "inv_lnk": "ریفرل رجسٹریشن لنک شیئر کریں", "firewall": "نائس ہیش سیکیورٹی فائر وال", "email_lbl": "اکاؤنٹ ای میل درج کریں:",
        "pass_lbl": "سیکیورٹی پاس ورڈ کی:", "unlock_b": "والٹ انلاک کریں", "inject_b": "ٹیسٹ بیلنس جمع کریں",
        "disc_b": "سیشن بند کریں", "success_msg": "والٹ کامیابی سے اپ ڈیٹ ہو گیا!", "extract_b": "کمائی والٹ میں بھیجیں",
        "wth_lbl": "نکلوانے کی رقم:", "exec_wth": "رقم نکلوانے کی درخواست کریں", "insufficient": "والٹ میں رقم کم ہے۔"
    },
    "🌐 DeepUrdu": {
        "title": "جانی نائس ہیش", "news_head": "ضروری نوٹس سنو جانی", "got_it": "سمجھ گیا جانی",
        "welcome": "نائس ہیش · مائننگ کا مال تیار ہے", "launch": "فُل لائیو تباھی 31 مئی 2026",
        "marquee": "جانی ابھی انلاک کرو اور مال نکالنا شروع کرو! کوئی لمبا چکر نہیں ہے، بٹن دباتے ہی کمائی سیدھی جیب میں آتی ہے مِنتو میں!",
        "assets_title": "کل مال پانی", "invest_lbl": "انوسٹ والٹ اکاؤنٹ", "comm_lbl": "کمیشن والا والٹ",
        "d_btn": "پیسے ڈالیں", "w_btn": "پیسے نکالیں", "v_btn": "وی آئی پی پلانز", "t_btn": "اپنی گینگ", "m_btn": "مائننگ فین", "me_btn": "میرا اکاؤنٹ",
        "log_title": "لائیو پرافٹ کی لسٹ جانی", "partners": "بڑے بڑے برانڈز", "curr_v": "تمہارا ابھی کا لیول:", "my_d": "تمہارا ٹوٹل انوسٹ مال:",
        "req_m": "کم از کم انٹری فیس:", "day_r": "روزانہ کا پکا پرافٹ:", "acc_c": "کلاؤڈ مائننگ دھڑا دھڑ جاری ہے",
        "eng_s": "انجن کا سین کیا ہے:", "act_run": "فُل سپیڈ میں چل رہا ہے جانی", "inv_id": "تمہارا کوڈ لوٹو اب",
        "inv_lnk": "یہ لنک گینگ کو بھیجو اور کمیشن کھاؤ", "firewall": "نائس ہیش سیکیورٹی فائر وال لاک", "email_lbl": "اپنی ای میل لکھو جانی:",
        "pass_lbl": "پاس ورڈ کی چابی لگاؤ:", "unlock_b": "اکاؤنٹ کا تالا کھولیں", "inject_b": "ٹیسٹ ڈالر ڈالو اکاؤنٹ میں",
        "disc_b": "اکاؤنٹ لاگ آؤٹ کرو", "success_msg": "والٹ میں مال آگیا جانی!", "extract_b": "منافع والٹ میں لوڈ کرو",
        "wth_lbl": "کتنا مال نکالنا ہے:", "exec_wth": "مال والٹ سے باہر بھیجو", "insufficient": "اکاؤنٹ خالی ہے جانی مال ڈالو۔"
    },
    "🌐 العربية": {
        "title": "نايس هاش", "news_head": "إشعار الأخبار", "got_it": "فهمت",
        "welcome": "نايس هاش · عصر جديد للتعدين", "launch": "تم الإطلاق رسميًا في 31 مايو 2026.",
        "marquee": "افتح واربح أول أرباحك الآن! لا انتظار ، لا عمليات معقدة ، الأرباح تصل فورًا بعد الفتح.",
        "assets_title": "إجمالي الأصول", "invest_lbl": "محفظة الاستثمار", "comm_lbl": "محفظة العمولات",
        "d_btn": "إيداع", "w_btn": "سحب", "v_btn": "خطة VIP", "t_btn": "فريقي", "m_btn": "تعدين", "me_btn": "حسابي",
        "log_title": "سجل عمليات السحب المباشر", "curr_v": "مستوى VIP الحالي:", "my_d": "إيداعي النشط:",
        "req_m": "الحد الأدنى للمشاركة:", "day_r": "العائد اليومي التلقائي:", "acc_c": "تراكم العملات المشفرة مباشرة",
        "eng_s": "حالة محرك السحاب:", "act_run": "نشط ويعمل فورا", "inv_id": "رمز الدعوة الشخصي",
        "inv_lnk": "مشاركة رابط التسجيل", "firewall": "جدار حماية نايس هاش", "email_lbl": "بريد الحساب:",
        "pass_lbl": "مفتاح الأمان:", "unlock_b": "فتح مساحة العمل", "inject_b": "حقن رصيد USDT تجريبي",
        "disc_b": "تسجيل الخروج", "success_msg": "تم تحديث المحفظة بنجاح!", "extract_b": "حصاد الأرباح الآن",
        "wth_lbl": "المبلغ المراد سحبه ($):", "exec_wth": "تنفيذ عملية السحب", "insufficient": "الرصيد غير كافٍ للعملية."
    }
}

extended_language_keys = ["🌐 Français", "🌐 Deutsch", "🌐 Русский", "🌐 简体中文", "🌐 Türkçe", "🌐 Tiếng Việt", "🌐 Bahasa Melayu", "🌐 Português", "🌐 Italiano", "🌐 日本語", "🌐 한국어", "🌐 हिन्दी", "🌐 Pashto", "🌐 Punjabi", "🌐 Persian", "🌐 Bengali", "🌐 Tagalog", "🌐 Swahili"]
for lang_key in extended_language_keys:
    if lang_key not in DICTIONARY: DICTIONARY[lang_key] = DICTIONARY["🌐 English"].copy()

# ==============================================================================
# --- 2. DATABASE VAULT LAYERS ---
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
    cursor.execute("INSERT OR IGNORE INTO accounts VALUES ('admin@nicehash.one', 'admin786', '0000', 5000.00, 1250.00, 'VIP4', '777888', 1718683200.0)")
    conn.commit()
    conn.close()

def query_vault(query, args=(), one=False, commit=False):
    conn = sqlite3.connect("nicehash_real_vault.db", check_same_thread=False)
    cursor = conn.cursor()
    try:
        cursor.execute(query, args)
        if commit: conn.commit(); conn.close(); return True
        rv = cursor.fetchall(); conn.close(); return (rv[0] if rv else None) if one else rv
    except Exception: conn.close(); return None if one else []

run_db_migrations()

# ==============================================================================
# --- 3. RUNTIME APP STATES ---
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
        daily_ratio = {"VIP1": 30.0, "VIP2": 32.0, "VIP3": 34.0, "VIP4": 36.0}.get(vip_level, 0.00)
        if invest_bal > 0:
            st.session_state.crypto_yield_accumulator += ((invest_bal * (daily_ratio / 100.0)) / 86400.0) * random.uniform(0.98, 1.02)

# ==============================================================================
# --- 4. HARD ABSOLUTE SCREEN SIZE CRUSH LOCK (CSS FORCED NO-SCROLL) ---
# ==============================================================================
st.markdown("""
<style>
/* Pure CSS Shield to Force No Scroll on Desktop/Mobile Viewports */
footer, .stDeployButton, #MainMenu, [data-testid="stStatusWidget"], [data-testid="stHeader"] { display: none !important; }

html, body, .stApp { 
    background-color: #12161a !important; 
    color: #ffffff !important; 
    font-family: 'Inter', sans-serif !important;
    overflow: hidden !important; /* Locks screen scrolling completely */
    max-height: 100vh !important;
}

/* Hard Lock Frame Workspace Canvas Bounds */
[data-testid="stVerticalBlock"] { 
    max-width: 440px !important; 
    margin: 0 auto !important; 
    padding: 10px !important; 
    background: #1c2127 !important; 
    height: 100vh !important; 
    overflow-y: auto !important; /* Allow internal scrolling only inside container if necessary */
}

/* Spacing Compression Optimization Grid */
.block-container { padding-top: 5px !important; padding-bottom: 5px !important; max-width: 440px !important; }
[data-testid="stVerticalBlock"] > div { padding: 0px !important; margin: 0px !important; gap: 0px !important; }

/* Custom Styling Objects */
.nh-top-bar { display: flex; justify-content: space-between; align-items: center; background: #1c2127; padding-bottom: 2px; }
.nh-logo-title { font-size: 24px; font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 6px; }
.nh-logo-icon { width: 20px; height: 20px; background: #ff6a00; border-radius: 50%; display: inline-block; position: relative; }
.nh-logo-icon::after { content: ''; position: absolute; width: 8px; height: 8px; background: #1c2127; left: 6px; top: 6px; border-radius: 50%; }

.asset-premium-card { background: linear-gradient(135deg, #252b35 0%, #171c24 100%); border-radius: 12px; padding: 12px; border: 1px solid #2d3642; margin: 8px 0; }
.asset-total-title { color: #8a99ad; font-size: 12px; font-weight: 600; }
.asset-total-value { font-size: 28px; font-weight: 700; color: #ffffff; margin: 2px 0 8px 0; font-family: monospace; }
.sub-wallet-row { display: flex; justify-content: space-between; padding: 5px 0; border-top: 1px solid rgba(255,255,255,0.05); font-size: 11.5px; }

.marquee-alert-box { display: flex; align-items: center; background: #171c24; border-radius: 6px; padding: 5px 8px; border: 1px solid #2a313a; margin: 8px 0; font-size: 11px; overflow: hidden; }
.marquee-text-flow { white-space: nowrap; animation: textScroll 18s linear infinite; color: #cbd5e0; }
@keyframes textScroll { 0% { transform: translate3d(100%, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }

.cooling-fan-hardware { width: 120px; height: 120px; background: radial-gradient(circle, #2d3542 0%, #171c24 100%); border-radius: 50%; border: 4px solid #ff6a00; margin: 15px auto; display: flex; align-items: center; justify-content: center; position: relative; }
.fan-blades-wing { width: 90px; height: 90px; background: repeating-conic-gradient(from 0deg, #ff6a00 0deg 30deg, #171c24 30deg 60deg); border-radius: 50%; animation: spinHardware 0.8s linear infinite; }
@keyframes spinHardware { 100% { transform: rotate(360deg); } }

div.stButton > button {
    background: linear-gradient(90deg, #ff8c00 0%, #ff5500 100%) !important; color: #ffffff !important; font-weight: 700 !important; border-radius: 8px !important; width: 100% !important; border: none !important; padding: 6px !important; font-size: 11.5px !important; margin: 0px !important;
}

.news-modal-inline-container { background: #1c2127; border: 1px solid #ff6a00; border-radius: 12px; padding: 12px; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

# Header Row Control
h_col1, h_col2 = st.columns([1.8, 1.2])
with h_col1:
    st.markdown('<div class="nh-top-bar"><div class="nh-logo-title"><div class="nh-logo-icon"></div>nicehash</div></div>', unsafe_allow_html=True)
with h_col2:
    selected_language_key = st.selectbox(label="", options=list(DICTIONARY.keys()), index=0, key="lang_selector")

st.markdown("<div style='border-bottom: 1px solid #2a313a; margin-bottom: 8px;'></div>", unsafe_allow_html=True)
L = DICTIONARY[selected_language_key]

# --- NEWS POPUP TRIGGER ---
if st.session_state.show_inline_news and st.session_state.active_tab == "Home":
    st.markdown(f"""
    <div class="news-modal-inline-container">
        <h3 style="color:#ffffff; margin:0 0 5px 0; font-size:18px; text-align:center;">{L["news_head"]}</h3>
        <div style="font-size:11.5px; color:#cbd5e0; line-height:1.4;">
            🎉 <b>{L["welcome"]}</b> - <b>{L["launch"]}</b><br>
            💡 Unlock and earn now! Instant system payouts.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(L["got_it"], key="dismiss_news_trigger"):
        st.session_state.show_inline_news = False
        st.rerun()

# --- TAB CONTROL CONTROLLERS ---
if st.session_state.active_tab == "Home":
    st.markdown(f"""
    <div class="marquee-alert-box"><div class="marquee-text-flow">{L["marquee"]}</div></div>
    <div class="asset-premium-card">
        <div class="asset-total-title">{L["assets_title"]}</div>
        <div class="asset-total-value">${(invest_bal + comm_bal):,.2f}</div>
        <div class="sub-wallet-row"><span>{L["invest_lbl"]}</span><b>${invest_bal:,.2f}</b></div>
        <div class="sub-wallet-row"><span>{L["comm_lbl"]}</span><b>${comm_bal:,.2f}</b></div>
    </div>
    """, unsafe_allow_html=True)
    
    grid_blocks = st.columns(4)
    with grid_blocks[0]: 
        if st.button(f"🏛️\n{L['d_btn']}", key="act_d"): st.session_state.active_tab = "Me"; st.rerun()
    with grid_blocks[1]: 
        if st.button(f"🏧\n{L['w_btn']}", key="act_w"): st.session_state.active_tab = "Me"; st.rerun()
    with grid_blocks[2]: 
        if st.button(f"👑\n{L['v_btn']}", key="act_v"): st.session_state.active_tab = "VIP"; st.rerun()
    with grid_blocks[3]: 
        if st.button(f"👥\n{L['t_btn']}", key="act_t"): st.session_state.active_tab = "Team"; st.rerun()

elif st.session_state.active_tab == "VIP":
    for i in range(1, 5):
        min_b = [0, 10, 100, 1000, 5000][i]
        st.markdown(f"""
        <div style="background:#171c24; border-radius:10px; padding:10px; border:1px solid #2d3642; margin-bottom:6px;">
            <div style="color:#ff6a00; font-weight:700; font-size:13px;">VIP {i} Contract</div>
            <div style="font-size:11px; display:flex; justify-content:space-between;"><span>Min Entry:</span><b>${min_b}</b></div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.active_tab == "Mining":
    st.markdown('<div class="cooling-fan-hardware"><div class="fan-blades-wing"></div></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#252b35; padding:12px; border-radius:10px; text-align:center; font-size:12px;">
        <h2 style="color:#ffffff; margin:0; font-family:monospace;">{st.session_state.crypto_yield_accumulator:.8f} USDT</h2>
    </div>
    """, unsafe_allow_html=True)
    if st.button(L["extract_b"], key="flush_yield_action"):
        if st.session_state.crypto_yield_accumulator > 0:
            query_vault("UPDATE accounts SET commission_wallet = commission_wallet + ? WHERE username=?", (st.session_state.crypto_yield_accumulator, st.session_state.current_user), commit=True)
            st.session_state.crypto_yield_accumulator = 0.00000000
            st.rerun()

elif st.session_state.active_tab == "Team":
    st.markdown(f'<div style="background:#252b35; padding:12px; border-radius:10px; font-size:12px;">Invite ID: <b>{user_invite}</b></div>', unsafe_allow_html=True)

elif st.session_state.active_tab == "Me":
    if not st.session_state.logged_in:
        u_in = st.text_input("Email:", key="login_u")
        p_in = st.text_input("Password:", type="password", key="login_p")
        if st.button("Login", key="login_act"):
            match = query_vault("SELECT username FROM accounts WHERE username=? AND password=?", (u_in.strip(), p_in.strip()), one=True)
            if match: st.session_state.logged_in = True; st.session_state.current_user = match[0]; st.rerun()
    else:
        st.markdown(f'<div style="font-size:13px; margin-bottom:8px;">👤 Account: {st.session_state.current_user}</div>', unsafe_allow_html=True)
        if st.button("Logout", key="logout_act"): st.session_state.logged_in = False; st.rerun()

# ==============================================================================
# --- 5. BOTTOM NAVIGATION ROW ---
# ==============================================================================
st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
nav_grid = st.columns(5)
with nav_grid[0]: 
    if st.button("🏠\nHome", key="n_h"): st.session_state.active_tab = "Home"; st.rerun()
with nav_grid[1]: 
    if st.button("👑\nVIP", key="n_v"): st.session_state.active_tab = "VIP"; st.rerun()
with nav_grid[2]: 
    if st.button("⚡\nMine", key="n_m"): st.session_state.active_tab = "Mining"; st.rerun()
with nav_grid[3]: 
    if st.button("👥\nTeam", key="n_t"): st.session_state.active_tab = "Team"; st.rerun()
with nav_grid[4]: 
    if st.button("👤\nMe", key="n_me"): st.session_state.active_tab = "Me"; st.rerun()
