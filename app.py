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
        "assets_title": "کل مال پانی", "invest_lbl": "انوسٹ والٹ اکاؤنٹ", "comm_lbl": "کمیشن वाला والٹ",
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
        "log_title": "سجل عمليات السحب المباشر", "partners": "الشركاء العالميون", "curr_vip": "مستوى VIP الحالي:", "my_d": "إيداعي النشط:",
        "req_m": "الحد الأدنى للمشاركة:", "day_r": "العائد اليومي التلقائي:", "acc_c": "تراكم العملات المشفرة مباشرة",
        "eng_s": "حالة محرك السحاب:", "act_run": "نشط ويعمل فورا", "inv_id": "رمز الدعوة الشخصي",
        "inv_lnk": "مشاركة رابط التسجيل", "firewall": "جدار حماية نايس هاش", "email_lbl": "بريد الحساب:",
        "pass_lbl": "مفتاح الأمان:", "unlock_b": "فتح مساحة العمل", "inject_b": "حقن رصيد USDT تجريبي",
        "disc_b": "تسجيل الخروج", "success_msg": "تم تحديث المحفظة بنجاح!", "extract_b": "حصاد الأرباح الآن",
        "wth_lbl": "المبلغ المراد سحبه ($):", "exec_wth": "تنفيذ عملية السحب", "insufficient": "الرصيد غير كافٍ للعملية."
    }
}

extended_language_keys = [
    "🌐 Français", "🌐 Deutsch", "🌐 Русский", "🌐 简体中文", "🌐 Türkçe", "🌐 Tiếng Việt", 
    "🌐 Bahasa Melayu", "🌐 Português", "🌐 Italiano", "🌐 日本語", "🌐 한국어", "🌐 हिन्दी", 
    "🌐 Pashto", "🌐 Punjabi", "🌐 Persian", "🌐 Bengali", "🌐 Tagalog", "🌐 Swahili"
]
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
    cursor.execute("INSERT OR IGNORE INTO accounts VALUES ('admin@nicehash.one', 'admin786', '0000', 5000.00, 1250.00, 'VIP4', '777888', 1718683200.0)")
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

# Fetch Sync Wallet States Globally to prevent initialization order NameErrors
invest_bal, comm_bal, vip_level, user_invite = 0.00, 0.00, "VIP0", "286651"
if st.session_state.logged_in:
    account_stats = query_vault("SELECT invest_wallet, commission_wallet, vip_level, invite_code FROM accounts WHERE username=?", (st.session_state.current_user,), one=True)
    if account_stats:
        invest_bal, comm_bal, vip_level, user_invite = account_stats
        
        # Live fractions accumulation logic loop
        daily_ratio = 0.00
        if vip_level == "VIP1": daily_ratio = 30.0
        elif vip_level == "VIP2": daily_ratio = 32.0
        elif vip_level == "VIP3": daily_ratio = 34.0
        elif vip_level == "VIP4": daily_ratio = 36.0
        
        if invest_bal > 0:
            per_second_yield = (invest_bal * (daily_ratio / 100.0)) / 86400.0
            st.session_state.crypto_yield_accumulator += per_second_yield * random.uniform(0.98, 1.02)

user_nodes_pool = ['a***8h@gmail.com', 'k***22@yahoo.com', 'n***_hash@live.com', 'x***9@hotmail.com', 'r***00@gmail.com']
def generate_live_withdrawal_ledger():
    logs = []
    random.seed(int(time.time() / 60))
    for i in range(4):
        node = random.choice(user_nodes_pool)
        val = round(random.uniform(20.00, 4890.00), 2)
        logs.append(f"⚡ Node {node} extracted <b style='color:#ff6a00;'>${val:,.2f}</b> seamlessly.")
    return logs

# ==============================================================================
# --- 4. GRAPHIC INTERFACE DESIGN AND HIGH CONFIGURATION SYSTEM ---
# ==============================================================================
st.markdown("""
<style>
footer, .stDeployButton, #MainMenu, [data-testid="stStatusWidget"], [data-testid="stHeader"] { display: none !important; }
html, body, .stApp { background-color: #12161a !important; color: #ffffff !important; font-family: 'Inter', sans-serif !important; }

/* Perfect Mobile Canvas Frame Boundaries */
[data-testid="stVerticalBlock"] { max-width: 440px !important; margin: 0 auto !important; padding: 12px !important; background: #1c2127 !important; min-height: 100vh; }

/* Exact Original NiceHash Header Mark styling */
.nh-top-bar { display: flex; justify-content: space-between; align-items: center; background: #1c2127; padding-bottom: 4px; }
.nh-logo-title { font-size: 25px; font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 6px; }
.nh-logo-icon { width: 22px; height: 22px; background: #ff6a00; border-radius: 50%; display: inline-block; position: relative; }
.nh-logo-icon::after { content: ''; position: absolute; width: 10px; height: 10px; background: #1c2127; left: 6px; top: 6px; border-radius: 50%; }

/* Asset Display Card styles */
.asset-premium-card { background: linear-gradient(135deg, #252b35 0%, #171c24 100%); border-radius: 12px; padding: 20px; border: 1px solid #2d3642; margin-bottom: 15px; }
.asset-total-title { color: #8a99ad; font-size: 13px; font-weight: 600; text-transform: uppercase; }
.asset-total-value { font-size: 32px; font-weight: 700; color: #ffffff; margin: 6px 0 14px 0; font-family: monospace; }
.sub-wallet-row { display: flex; justify-content: space-between; padding: 8px 0; border-top: 1px solid rgba(255,255,255,0.05); font-size: 12.5px; color: #cbd5e0; }

/* Marquee Scroller Box styles */
.marquee-alert-box { display: flex; align-items: center; background: #171c24; border-radius: 8px; padding: 8px 12px; border: 1px solid #2a313a; margin-bottom: 15px; font-size: 12px; overflow: hidden; }
.marquee-text-flow { white-space: nowrap; animation: textScroll 18s linear infinite; color: #cbd5e0; font-weight: 500; }
@keyframes textScroll { 0% { transform: translate3d(100%, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }

/* Rotating Fan Component Graphic designs */
.cooling-fan-hardware { width: 135px; height: 135px; background: radial-gradient(circle, #2d3542 0%, #171c24 100%); border-radius: 50%; border: 4px solid #ff6a00; margin: 25px auto; display: flex; align-items: center; justify-content: center; position: relative; }
.fan-blades-wing { width: 105px; height: 105px; background: repeating-conic-gradient(from 0deg, #ff6a00 0deg 30deg, #171c24 30deg 60deg); border-radius: 50%; animation: spinHardware 0.8s linear infinite; }
@keyframes spinHardware { 100% { transform: rotate(360deg); } }
.fan-center-core { position: absolute; width: 34px; height: 34px; background: #171c24; border: 2px solid #ffffff; border-radius: 50%; color: #ffffff; font-weight: 800; font-size: 11px; line-height: 30px; text-align: center; }

/* Custom Streamlit Buttons Injection Layer overrides */
div.stButton > button {
    background: linear-gradient(90deg, #ff8c00 0%, #ff5500 100%) !important; color: #ffffff !important; font-weight: 700 !important; border-radius: 8px !important; width: 100% !important; border: none !important; padding: 12px !important; box-shadow: 0 4px 12px rgba(255,85,0,0.25); text-transform: uppercase; font-size: 13px !important;
}

/* Stable Non-breaking Inlined Notice Card layout wrapper */
.news-modal-inline-container {
    background: #1c2127; border: 1px solid #ff6a00; border-radius: 12px; padding: 16px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

# Layout Setup for Brand Title and Language Selection row
h_col1, h_col2 = st.columns([1.8, 1.2])
with h_col1:
    st.markdown("""
    <div class="nh-top-bar" style="border:none; margin-bottom:0; padding-bottom:0;">
        <div class="nh-logo-title"><div class="nh-logo-icon"></div>nicehash</div>
    </div>
    """, unsafe_allow_html=True)
with h_col2:
    selected_language_key = st.selectbox(
        label="",
        options=list(DICTIONARY.keys()),
        index=0,
        key="app_runtime_language_dictionary_selector"
    )

st.markdown("<div style='border-bottom: 1px solid #2a313a; margin-bottom: 15px; margin-top: 2px;'></div>", unsafe_allow_html=True)

# Map dynamic pointer array shortcut reference
L = DICTIONARY[selected_language_key]

# ==============================================================================
# --- 5. COMPACT OVERLAY NEWS WORKSPACE (100% SAFE LAYOUT DISMISSAL) ---
# ==============================================================================
if st.session_state.show_inline_news and st.session_state.active_tab == "Home":
    st.markdown(f"""
    <div class="news-modal-inline-container">
        <h3 style="color:#ffffff; margin:0 0 12px 0; font-weight:800; font-size:22px; text-align:center;">{L["news_head"]}</h3>
        <div style="font-size:13px; color:#cbd5e0; line-height:1.6; margin-bottom: 15px;">
            🎉 <b>{L["welcome"]}</b><br>
            <b>{L["launch"]}</b><br><br>
            💡 Unlock and earn your first earnings now!<br>
            No waiting, no complicated operations, earnings arrive instantly.<br>
            <hr style="border-color:rgba(255,255,255,0.08); margin:10px 0;">
            <table style="width:100%; border-collapse:collapse; text-align:center; color:#fff; font-size:11px;">
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
    if st.button(L["got_it"], key="dismiss_inline_news_notice_action_panel_trigger"):
        st.session_state.show_inline_news = False
        st.rerun()
    st.markdown("<hr style='border-color:rgba(255,255,255,0.05); margin:15px 0;'>", unsafe_allow_html=True)

# ==============================================================================
# --- 6. CORE OPERATIONAL ROUTES AND BACKEND VIEW CONTROLLERS ---
# ==============================================================================

# --- 6.1 HOME TAB SECTION ---
if st.session_state.active_tab == "Home":
    st.markdown(f"""
    <div style="width:100%; height:110px; background:linear-gradient(135deg, #252b35 0%, #12161a 100%); border-radius:12px; display:flex; align-items:center; justify-content:center; border:1px solid #2d3642; margin-bottom:12px;">
        <div style="font-size:26px; font-weight:900; color:#ff6a00; letter-spacing:2px;">{L["title"]}</div>
    </div>
    <div class="marquee-alert-box">
        <span style="color:#ff6a00; margin-right:6px; font-weight:700;">📢</span>
        <div class="marquee-text-flow">{L["marquee"]}</div>
    </div>
    <div class="asset-premium-card">
        <div class="asset-total-title">{L["assets_title"]}</div>
        <div class="asset-total-value">${(invest_bal + comm_bal):,.2f}</div>
        <div class="sub-wallet-row"><span>{L["invest_lbl"]}</span><span style="font-weight:700; color:#fff;">${invest_bal:,.2f}</span></div>
        <div class="sub-wallet-row" style="border:none; padding-bottom:0;"><span>{L["comm_lbl"]}</span><span style="font-weight:700; color:#fff;">${comm_bal:,.2f}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    grid_blocks = st.columns(4)
    with grid_blocks[0]:
        if st.button(f"🏛️\n{L['d_btn']}", key="h_grid_deposit_action"):
            st.session_state.active_tab = "Me"
            st.rerun()
    with grid_blocks[1]:
        if st.button(f"🏧\n{L['w_btn']}", key="h_grid_withdraw_action"):
            st.session_state.active_tab = "Me"
            st.rerun()
    with grid_blocks[2]:
        if st.button(f"👑\n{L['v_btn']}", key="h_grid_vip_action"):
            st.session_state.active_tab = "VIP"
            st.rerun()
    with grid_blocks[3]:
        if st.button(f"👥\n{L['t_btn']}", key="h_grid_team_action"):
            st.session_state.active_tab = "Team"
            st.rerun()
            
    st.markdown(f"<div style='margin-top:15px; font-size:14px; font-weight:700; margin-bottom:8px; color:#ff6a00;'>{L['log_title']}</div>", unsafe_allow_html=True)
    for log in generate_live_withdrawal_ledger():
        st.markdown(f"<div style='background:#171c24; padding:10px; border-radius:8px; margin-bottom:6px; font-size:12px; border:1px solid #2a313a;'>{log}</div>", unsafe_allow_html=True)

# --- 6.2 VIP CONFIGURATION TIERS ---
elif st.session_state.active_tab == "VIP":
    st.markdown(f"""
    <div style="background:#252b35; padding:15px; border-radius:12px; border:1px solid #2d3642; margin-bottom:15px;">
        <div style="display:flex; justify-content:space-between; font-size:13px; color:#cbd5e0;"><span>{L["curr_v"]}</span><span style="color:#ff6a00; font-weight:700;">{vip_level}</span></div>
        <div style="display:flex; justify-content:space-between; font-size:13px; color:#cbd5e0; margin-top:4px;"><span>{L["my_d"]}</span><span style="color:#00ffcc; font-weight:700;">${invest_bal:,.2f}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    for i in range(1, 5):
        min_bounds = [0, 10, 100, 1000, 5000][i]
        yield_ratio = [0, 30, 32, 34, 36][i]
        st.markdown(f"""
        <div style="background:#171c24; border-radius:12px; padding:15px; border:1px solid #2d3642; margin-bottom:10px;">
            <div style="font-weight:800; font-size:16px; color:#ff6a00; border-bottom:1px solid rgba(255,255,255,0.05); padding-bottom:4px; margin-bottom:6px;">VIP {i} Mining Node</div>
            <div style="display:flex; justify-content:space-between; font-size:12px;"><span style="color:#8a99ad;">{L["req_m"]}</span><span style="color:#fff; font-weight:600;">${min_bounds:,.2f}</span></div>
            <div style="display:flex; justify-content:space-between; font-size:12px;"><span style="color:#8a99ad;">{L["day_r"]}</span><span style="color:#00ffcc; font-weight:700;">{yield_ratio:.2f}% / Day</span></div>
        </div>
        """, unsafe_allow_html=True)

# --- 6.3 ACTIVE MINER ENGINE CALCULATOR TAB ---
elif st.session_state.active_tab == "Mining":
    st.markdown("""
    <div class="cooling-fan-hardware"><div class="fan-blades-wing"></div><div class="fan-center-core">⚡</div></div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background:#252b35; padding:20px; border-radius:12px; border:1px solid #2d3642; text-align:center;">
        <span style="color:#8a99ad; font-size:12px; text-transform:uppercase; letter-spacing:1px;">{L["acc_c"]}</span>
        <h2 style="margin:8px 0; font-size:28px; color:#ffffff; font-family:monospace;">{st.session_state.crypto_yield_accumulator:.8f} <span style="font-size:14px; color:#ff6a00;">USDT</span></h2>
        <div style="display:flex; justify-content:space-between; font-size:12px; border-top:1px solid rgba(255,255,255,0.05); padding-top:10px; margin-top:12px;"><span style="color:#cbd5e0;">Node Tier Level</span><span style="color:#ff6a00; font-weight:700;">{vip_level}</span></div>
        <div style="display:flex; justify-content:space-between; font-size:12px;"><span style="color:#cbd5e0;">{L["eng_s"]}</span><span style="color:#00ffcc; font-weight:600;">{L["act_run"]}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    if st.button(L["extract_b"], key="extract_live_miner_yield_to_wallet_action"):
        if st.session_state.crypto_yield_accumulator > 0:
            query_vault("UPDATE accounts SET commission_wallet = commission_wallet + ? WHERE username=?", (st.session_state.crypto_yield_accumulator, st.session_state.current_user), commit=True)
            st.session_state.crypto_yield_accumulator = 0.00000000
            st.success("Yield Successfully Flushed to Wallet Ledger!")
            time.sleep(0.5)
            st.rerun()
        else:
            st.toast("Accumulating mining blocks...")

# --- 6.4 REFERRAL LOGISTIC NETWORKS ---
elif st.session_state.active_tab == "Team":
    st.markdown(f"""
    <div style="background:#252b35; padding:15px; border-radius:12px; border:1px solid #2d3642;">
        <span style="font-size:12px; color:#8a99ad;">{L["inv_id"]}</span>
        <h2 style="margin:4px 0; color:#ff6a00; letter-spacing:1px; font-family:monospace;">{user_invite}</h2>
        <span style="font-size:12px; color:#8a99ad; display:block; margin-top:10px;">{L["inv_lnk"]}</span>
        <div style="background:#171c24; padding:8px; border-radius:6px; font-size:11px; color:#cbd5e0; word-break:break-all; border:1px solid #2a313a; margin-top:4px;">
            https://nicehash.one/#/register?invite_code={user_invite}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 6.5 USER ACCOUNTS PROFILE VAULTS ---
elif st.session_state.active_tab == "Me":
    if not st.session_state.logged_in:
        st.markdown(f"<h4 style='text-align:center; color:#ff6a00; margin-bottom:15px;'>{L['firewall']}</h4>", unsafe_allow_html=True)
        user_in = st.text_input(L["email_lbl"], placeholder="demo@gmail.com")
        pass_in = st.text_input(L["pass_lbl"], type="password", placeholder="demo123")
        
        if st.button(L["unlock_b"]):
            match = query_vault("SELECT username FROM accounts WHERE username=? AND password=?", (user_in.strip(), pass_in.strip()), one=True)
            if match:
                st.session_state.logged_in = True
                st.session_state.current_user = match[0]
                st.rerun()
            else:
                st.error("Firewall reject: Mismatched key parameters token.")
    else:
        st.markdown(f"""
        <div style="background:#252b35; padding:15px; border-radius:12px; border:1px solid #2d3642; margin-bottom:15px;">
            <div style="font-weight:700; font-size:16px; color:#fff;">👤 {st.session_state.current_user}</div>
            <span style="background:#ff6a00; color:white; font-size:10px; font-weight:800; padding:2px 8px; border-radius:6px; margin-top:4px; display:inline-block;">{vip_level} Security Level Node</span>
        </div>
        """, unsafe_allow_html=True)
        
        dep_input = st.number_input("Input USDT Deposit Amount ($):", min_value=10.0, step=50.0)
        if st.button(L["inject_b"], key="me_inject_simulated_deposit_action_btn"):
            vip_tier_update = "VIP1"
            if dep_input >= 5000: vip_tier_update = "VIP4"
            elif dep_input >= 1000: vip_tier_update = "VIP3"
            elif dep_input >= 100: vip_tier_update = "VIP2"
            
            query_vault("UPDATE accounts SET invest_wallet = invest_wallet + ?, vip_level = ? WHERE username=?", (dep_input, vip_tier_update, st.session_state.current_user), commit=True)
            st.success(L["success_msg"])
            time.sleep(0.5)
            st.rerun()
            
        st.markdown("<hr style='border-color:rgba(255,255,255,0.05); margin:15px 0;'>", unsafe_allow_html=True)
        
        wth_input = st.number_input(L["wth_lbl"], min_value=10.0, step=10.0, key="me_withdrawal_input_box_field")
        if st.button(L["exec_wth"], key="me_withdrawal_execute_action_trigger_btn"):
            if invest_bal >= wth_input:
                query_vault("UPDATE accounts SET invest_wallet = invest_wallet - ? WHERE username=?", (wth_input, st.session_state.current_user), commit=True)
                st.success("Withdrawal Requested Successfully! Ledger Updated.")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error(L["insufficient"])
                
        st.markdown("<hr style='border-color:rgba(255,255,255,0.05); margin:15px 0;'>", unsafe_allow_html=True)
        if st.button(L["disc_b"]):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.rerun()

# ==============================================================================
# --- 7. CORE RUNTIME NAVIGATION BUTTON REGISTRY ROW ---
# ==============================================================================
st.markdown("<div style='margin-top:35px;'></div>", unsafe_allow_html=True)
nav_grid = st.columns(5)

with nav_grid[0]:
    if st.button(f"🏠\nHome", key="n_h_f"): st.session_state.active_tab = "Home"; st.rerun()
with nav_grid[1]:
    if st.button(f"👑\nVIP", key="n_v_f"): st.session_state.active_tab = "VIP"; st.rerun()
with nav_grid[2]:
    if st.button(f"⚡\nMine", key="n_m_f"): st.session_state.active_tab = "Mining"; st.rerun()
with nav_grid[3]:
    if st.button(f"👥\nTeam", key="n_t_f"): st.session_state.active_tab = "Team"; st.rerun()
with nav_grid[4]:
    if st.button(f"👤\nMe", key="n_me_f"): st.session_state.active_tab = "Me"; st.rerun()
