import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="SIH26074 Weather Downscaler",
    page_icon="⛅",
    layout="wide"
)

# Custom Styling & Modern UI Backend
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #2c3e50; }
    .sub-text { color: #7f8c8d; font-size: 16px; }
    .card { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #3498db; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State to pass data smoothly across tabs
if 'pred_temp' not in st.session_state:
    st.session_state['pred_temp'] = 36.5
if 'pred_rain' not in st.session_state:
    st.session_state['pred_rain'] = 50.0

# Tabs Navigation
tab1, tab2, tab3 = st.tabs(["🏠 Home / Overview", "🌦️ Weather Downscaling", "🚜 Smart Agro-Advisory"])

# --- TAB 1: HOME ---
with tab1:
    st.markdown('<p class="main-title">🌾 Panchayat-Level Weather Downscaling & Agro-Advisory System</p>', unsafe_allow_html=True)
    st.markdown("### SIH26074 - Ministry of Earth Sciences (MoES)")
    st.markdown("---")
    
    st.markdown("""
    <div class="card">
        <p class="sub-text">
        Yeh application low-resolution <b>Block-level</b> weather forecasts ko high-resolution 
        <b>Panchayat/Village-level</b> par downscale karti hai taaki kisanon ko sateek aur local 
        mausam ki jankari mil sake.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Problem ID", "SIH26074")
    col2.metric("Category", "Software Solution")
    col3.metric("Domain", "Agriculture & Rural Dev")

# --- TAB 2: WEATHER DOWNSCALING ---
with tab2:
    st.markdown('<p class="main-title">🌦️ Spatial Weather Downscaling (Block to Panchayat)</p>', unsafe_allow_html=True)
    st.markdown("Enter coarse block parameters and panchayat topography to generate high-res forecasts.")
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📥 Input Parameters")
        b_temp = st.slider("Block Temperature (°C)", 25.0, 45.0, 38.0)
        b_rain = st.slider("Block Rainfall (mm)", 0.0, 100.0, 45.0)
        elevation = st.slider("Panchayat Elevation / Unchai (meters)", 10, 800, 250)

    # Downscaling Simulation Logic (Lapse rate & Topography)
    pred_temp = round(b_temp - (elevation * 0.0065), 2)
    pred_rain = round(b_rain * (1 + (elevation / 1500)), 2)

    # Save calculated values to session state
    st.session_state['pred_temp'] = pred_temp
    st.session_state['pred_rain'] = pred_rain

    with col_right:
        st.subheader("📊 High-Resolution Panchayat Output")
        st.success("Downscaling calculated successfully based on local elevation factors!")
        
        m1, m2 = st.columns(2)
        m1.metric(label="Panchayat Temperature", value=f"{pred_temp} °C")
        m2.metric(label="Panchayat Rainfall", value=f"{pred_rain} mm")

# --- TAB 3: AGRO-ADVISORY ---
with tab3:
    st.markdown('<p class="main-title">🚜 Agro-Meteorological Advisory Services</p>', unsafe_allow_html=True)
    st.markdown("Get custom farming recommendations based on downscaled micro-climate data.")
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📍 Location & Conditions")
        selected_panchayat = st.selectbox("Select Panchayat", ["Panchayat 1 (Sadar)", "Panchayat 2", "Panchayat 3"])
        
        # Automatically pull values from session state
        input_temp = st.number_input("Current Panchayat Temp (°C)", value=float(st.session_state['pred_temp']))
        input_rain = st.number_input("Current Panchayat Rainfall (mm)", value=float(st.session_state['pred_rain']))
        
    with c2:
        st.subheader("💡 Farm Recommendation")
        if input_rain > 50:
            st.warning("⚠️ **Heavy Rainfall Alert:** Avoid chemical fertilizer application and stop irrigation immediately in this Panchayat.")
        elif input_temp > 38:
            st.error("🔥 **Heat Stress Warning:** High temperature detected. Ensure adequate water supply/irrigation for standing crops.")
        else:
            st.success("✅ **Optimal Weather Conditions:** Safe for sowing, harvesting, and regular farming activities.")
