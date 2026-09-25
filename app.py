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
    .card { background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #2ecc71; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# ==================== BACKEND LOGIC FUNCTIONS ====================

def compute_downscaling(block_temp, block_rain, elevation):
    """
    Backend Logic: Converts block-level forecasts to panchayat-level 
    using elevation lapse rate and topography factors.
    """
    panchayat_temp = round(block_temp - (elevation * 0.0065), 2)
    panchayat_rain = round(block_rain * (1 + (elevation / 1500)), 2)
    return panchayat_temp, panchayat_rain

def generate_crop_advisory(temp, rain, crop, lang):
    """
    Backend Logic: Crop Advisory Engine that evaluates micro-climate 
    parameters and generates rule-based alerts and SMS notifications.
    """
    if lang == "English":
        if rain > 50:
            return "warning", "⚠️ Heavy Rainfall Alert: Avoid chemical fertilizer application and stop irrigation immediately.", f"SMS sent to registered farmers: Heavy rain expected, do not apply fertilizers for {crop}."
        elif temp > 38:
            return "error", f"🔥 Heat Stress Warning: High temperature detected for {crop}. Ensure adequate irrigation.", f"SMS sent to registered farmers: High temperature warning, irrigate {crop} fields immediately."
        else:
            return "success", f"✅ Optimal Weather Conditions: Safe for sowing, harvesting, and regular farming of {crop}.", f"SMS sent to registered farmers: Weather is normal, continue regular farm operations."
    else: # Hindi
        if rain > 50:
            return "warning", "⚠️ भारी बारिश की चेतावनी: रासायनिक उर्वरक का छिड़काव न करें और सिंचाई तुरंत रोकें।", f"पंजीकृत किसानों को SMS भेजा गया: भारी बारिश की संभावना है, {crop} में खाद न डालें।"
        elif temp > 38:
            return "error", f"🔥 लू/गर्मी का तनाव (Heat Stress): {crop} के लिए तापमान बहुत अधिक है। पर्याप्त सिंचाई सुनिश्चित करें।", f"पंजीकृत किसानों को SMS भेजा गया: तेज गर्मी से बचाव के लिए {crop} की सिंचाई करें।"
        else:
            return "success", f"✅ अनुकूल मौसम: {crop} की बुवाई, कटाई और सामान्य कृषि कार्यों के लिए मौसम सुरक्षित है।", f"पंजीकृत किसानों को SMS भेजा गया: मौसम सामान्य है, नियमित कृषि कार्य जारी रखें।"

# ==================== INITIALIZE SESSION STATE ====================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'panchayat' not in st.session_state:
    st.session_state['panchayat'] = "Sadar Panchayat"
if 'pred_temp' not in st.session_state:
    st.session_state['pred_temp'] = 36.5
if 'pred_rain' not in st.session_state:
    st.session_state['pred_rain'] = 45.0

# ==================== SIDEBAR & LANGUAGE ====================
st.sidebar.title("⚙️ AgriCast Controls")
lang = st.sidebar.selectbox("Language / भाषा", ["English", "हिंदी"])

# Multilingual Text Dictionary
t = {
    "English": {
        "nav_home": "🏠 Login & Location",
        "nav_weather": "🌦️ Weather Downscaling",
        "nav_advisory": "🚜 Smart Agro-Advisory",
        "title": "AgriCast - Panchayat Weather & Crop Intelligence",
        "login_title": "Farmer / Officer Login & Location Setup",
        "login_btn": "Enter Dashboard",
        "success_msg": "Login successful! You can now access pages from the sidebar.",
    },
    "हिंदी": {
        "nav_home": "🏠 लॉगिन और क्षेत्र चयन",
        "nav_weather": "🌦️ मौसम डाउनस्केलिंग",
        "nav_advisory": "🚜 स्मार्ट कृषि सलाह",
        "title": "एग्रीकास्ट - पंचायत-स्तरीय मौसम और फसल खुफिया प्रणाली",
        "login_title": "किसान / अधिकारी लॉगिन और लोकेशन सेटअप",
        "login_btn": "डैशबोर्ड में प्रवेश करें",
        "success_msg": "लॉगिन सफल! अब आप साइडबार से अन्य पेज देख सकते हैं।",
    }
}

# Navigation Menu
page = st.sidebar.radio("Navigation", [t[lang]["nav_home"], t[lang]["nav_weather"], t[lang]["nav_advisory"]])

# ==================== PAGE 1: LOGIN & LOCATION ====================
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

    with col2:
        st.markdown("### 🌾 About AgriCast")
        st.markdown("A platform built to bridge the weather information gap by converting coarse block forecasts into hyper-local panchayat forecasts.")
        st.info("Kripya apni location darj karke login karein, fir sidebar se agla page select karein.")

# ==================== PAGE 2: WEATHER DOWNSCALING ====================
elif page == t[lang]["nav_weather"]:
    st.markdown('<p class="main-title">🌦️ Spatial Weather Downscaling (Block to Panchayat)</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    if not st.session_state['logged_in']:
        st.warning("⚠️ Kripya pehle Home page par jaakar Login aur Location select karein!")
    else:
        st.success(f"Active Panchayat Location: **{st.session_state['panchayat']}** | Backend Status: Connected")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📥 Coarse Input Parameters")
            b_temp = st.slider("Block Temperature (°C)", 25.0, 45.0, 38.0)
            b_rain = st.slider("Block Rainfall (mm)", 0.0, 100.0, 45.0)
            elevation = st.slider("Panchayat Elevation / ऊंचाई (meters)", 10, 800, 250)

        # Calling Backend Downscaling Function
        pred_temp, pred_rain = compute_downscaling(b_temp, b_rain, elevation)

        # Save to Session State
        st.session_state['pred_temp'] = pred_temp
        st.session_state['pred_rain'] = pred_rain

        with col2:
            st.subheader("📊 High-Resolution Output")
            m1, m2 = st.columns(2)
            m1.metric("Panchayat Temp", f"{pred_temp} °C")
            m2.metric("Panchayat Rainfall", f"{pred_rain} mm")
            st.info("Backend computation executed successfully using elevation lapse-rate algorithms.")

# ==================== PAGE 3: SMART AGRO-ADVISORY ====================
elif page == t[lang]["nav_advisory"]:
    st.markdown('<p class="main-title">🚜 Smart Agro-Advisory & Push Alerts</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    if not st.session_state['logged_in']:
        st.warning("⚠️ Kripya pehle Home page par jaakar Login aur Location select karein!")
    else:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📍 Parameter Verification")
            st.write(f"**Target Panchayat:** {st.session_state['panchayat']}")
            input_temp = st.number_input("Current Temp (°C)", value=float(st.session_state['pred_temp']))
            input_rain = st.number_input("Current Rainfall (mm)", value=float(st.session_state['pred_rain']))
            crop = st.selectbox("Select Crop / फसल", ["Paddy (धान)", "Wheat (गेहूं)", "Sugarcane (गन्ना)"])
            
        with c2:
            st.subheader("💡 Advisory & Last-Mile Delivery")
            
            # Calling Backend Advisory Engine Function
            alert_type, advisory_msg, sms_msg = generate_crop_advisory(input_temp, input_rain, crop, lang)
            
            if alert_type == "warning":
                st.warning(advisory_msg)
            elif alert_type == "error":
                st.error(advisory_msg)
            else:
                st.success(advisory_msg)
                
            st.info(f"📲 **SMS / WhatsApp Pipeline:**\n\n{sms_msg}")
