import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="AgriCast - SIH26074 Weather Intelligence",
    page_icon="🌾",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1e3d59; }
    .sub-text { color: #2c3e50; font-size: 15px; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'panchayat' not in st.session_state:
    st.session_state['panchayat'] = "Sadar Panchayat"
if 'pred_temp' not in st.session_state:
    st.session_state['pred_temp'] = 36.5
if 'pred_rain' not in st.session_state:
    st.session_state['pred_rain'] = 45.0

# --- LANGUAGE & SIDEBAR ---
st.sidebar.title("⚙️ AgriCast Controls")
lang = st.sidebar.selectbox("Language / भाषा", ["English", "हिंदी"])

# Dictionary for translations
t = {
    "English": {
        "nav_home": "🏠 Login & Location",
        "nav_weather": "🌦️ Weather Downscaling",
        "nav_advisory": "🚜 Smart Agro-Advisory",
        "title": "AgriCast - Panchayat Weather & Crop Intelligence",
        "login_title": "Farmer / Officer Login & Location Setup",
        "login_btn": "Enter Dashboard",
        "success_msg": "Login successful! Redirecting to Weather Downscaling...",
    },
    "हिंदी": {
        "nav_home": "🏠 लॉगिन और क्षेत्र चयन",
        "nav_weather": "🌦️ मौसम डाउनस्केलिंग",
        "nav_advisory": "🚜 स्मार्ट कृषि सलाह",
        "title": "एग्रीकास्ट - पंचायत-स्तरीय मौसम और फसल खुफिया प्रणाली",
        "login_title": "किसान / अधिकारी लॉगिन और लोकेशन सेटअप",
        "login_btn": "डैशबोर्ड में प्रवेश करें",
        "success_msg": "लॉगिन सफल! मौसम डाउनस्केलिंग पेज पर रीडायरेक्ट किया जा रहा है...",
    }
}

# Page State Management
if 'page' not in st.session_state:
    st.session_state['page'] = t[lang]["nav_home"]

# Navigation Menu
page = st.sidebar.radio("Navigation", [t[lang]["nav_home"], t[lang]["nav_weather"], t[lang]["nav_advisory"]], key="page")

# --- PAGE 1: LOGIN & LOCATION SELECTION ---
if page == t[lang]["nav_home"]:
    st.markdown(f'<p class="main-title">{t[lang]["title"]}</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns([1.2, 0.8])
    with col1:
        st.subheader(t[lang]["login_title"])
        user_name = st.text_input("Your Name / आपका नाम", "Ramesh Kumar")
        role = st.selectbox("Role / भूमिका", ["Farmer / किसान", "Panchayat Officer / अधिकारी"])
        
        state = st.selectbox("State / राज्य", ["Uttar Pradesh", "Bihar", "Madhya Pradesh", "Rajasthan"])
        district = st.text_input("District / जिला", "Varanasi")
        block = st.text_input("Block / ब्लॉक", "Cholapur")
        panchayat_name = st.text_input("Panchayat / पंचायत", "Baragaon")
        
        if st.button(t[lang]["login_btn"], type="primary"):
            st.session_state['logged_in'] = True
            st.session_state['panchayat'] = panchayat_name
            st.success(t[lang]["success_msg"])
            # Automatically switch to the next page (Weather Downscaling)
            st.session_state['page'] = t[lang]["nav_weather"]
            st.rerun()

    with col2:
        st.markdown("### 🌾 Welcome to AgriCast")
        st.markdown("Yeh platform low-resolution block forecasts ko high-resolution panchayat-level par downscale karta hai taaki kisanon ko sateek mausam ki jankari mil sake.")
        st.info("Kripya aage badhne ke liye apni sahi location darj karein aur 'Enter Dashboard' par click karein.")

# --- PAGE 2: WEATHER DOWNSCALING ---
elif page == t[lang]["nav_weather"]:
    st.markdown('<p class="main-title">🌦️ Spatial Weather Downscaling (Block to Panchayat)</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    if not st.session_state['logged_in']:
        st.warning("⚠️ Kripya pehle Home page par jaakar Login aur Location select karein!")
    else:
        st.success(f"Active Location: **{st.session_state['panchayat']}** | Status: Connected")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📥 Input Parameters")
            b_temp = st.slider("Block Temperature (°C)", 25.0, 45.0, 38.0)
            b_rain = st.slider("Block Rainfall (mm)", 0.0, 100.0, 45.0)
            elevation = st.slider("Panchayat Elevation / ऊंचाई (meters)", 10, 800, 250)

        # Downscaling Logic
        pred_temp = round(b_temp - (elevation * 0.0065), 2)
        pred_rain = round(b_rain * (1 + (elevation / 1500)), 2)

        st.session_state['pred_temp'] = pred_temp
        st.session_state['pred_rain'] = pred_rain

        with col2:
            st.subheader("📊 Panchayat High-Resolution Output")
            m1, m2 = st.columns(2)
            m1.metric("Panchayat Temp", f"{pred_temp} °C")
            m2.metric("Panchayat Rainfall", f"{pred_rain} mm")
            st.info("Micro-climate calculated successfully using elevation and lapse rate correction factors.")

# --- PAGE 3: SMART AGRO-ADVISORY ---
elif page == t[lang]["nav_advisory"]:
    st.markdown('<p class="main-title">🚜 Smart Agro-Advisory & Push Alerts</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    if not st.session_state['logged_in']:
        st.warning("⚠️ Kripya pehle Home page par jaakar Login aur Location select karein!")
    else:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📍 Crop & Location Details")
            st.write(f"**Panchayat:** {st.session_state['panchayat']}")
            input_temp = st.number_input("Current Temp (°C)", value=float(st.session_state['pred_temp']))
            input_rain = st.number_input("Current Rainfall (mm)", value=float(st.session_state['pred_rain']))
            crop = st.selectbox("Select Crop / फसल", ["Paddy (धान)", "Wheat (गेहूं)", "Sugarcane (गन्ना)"])
            
        with c2:
            st.subheader("💡 Advisory & SMS Status")
            if input_rain > 50:
                st.warning("⚠️ **Heavy Rain Alert:** Avoid fertilizer application. Stop irrigation immediately.")
                st.info(f"📲 SMS Sent to {st.session_state['panchayat']} farmers: 'Bhaari barish ki sambhavna hai, khad na dalein.'")
            elif input_temp > 38:
                st.error(f"🔥 **Heat Stress Warning:** High temperature detected for {crop}. Ensure proper irrigation.")
                st.info(f"📲 SMS Sent to {st.session_state['panchayat']} farmers: 'Tez garmi se fasal bachane ke liye sinchai karein.'")
            else:
                st.success(f"✅ **Optimal Conditions:** Weather is safe for regular farming activities for {crop}.")
                st.info(f"📲 SMS Sent to {st.session_state['panchayat']} farmers: 'Mausam anukul hai, sabhi kriyaayein jari rakhein.'")
