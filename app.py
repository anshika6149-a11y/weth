import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="SIH26074 Weather Downscaler",
    page_icon="🌾",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #2c3e50; }
    .sub-text { color: #7f8c8d; }
    </style>
""", unsafe_allow_html=True)

# Tabs Navigation
tab1, tab2, tab3 = st.tabs(["🏠 Home / Overview", "📊 Weather Downscaling", "💡 Smart Agro-Advisory"])

# --- TAB 1: HOME ---
with tab1:
    st.markdown('<p class="main-title">🌾 Panchayat-Level Weather Downscaling & Agro-Advisory System</p>', unsafe_allow_html=True)
    st.markdown("### SIH26074 - Ministry of Earth Sciences (MoES)[span_1](start_span)[span_1](end_span)")
    st.markdown("---")
    st.write("Yeh application low-resolution **Block-level** weather forecasts ko high-resolution **Panchayat/Village-level** par downscale karti hai[span_2](start_span)[span_2](end_span).")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Problem ID", "SIH26074")
    col2.metric("Category", "Software[span_3](start_span)[span_3](end_span)")
    col3.metric("Domain", "Agriculture & Rural Dev[span_4](start_span)[span_4](end_span)")

# --- TAB 2: WEATHER DOWNSCALING ---
with tab2:
    st.markdown('<p class="main-title">📊 Spatial Weather Downscaling (Block to Panchayat)</p>', unsafe_allow_html=True)
    st.markdown("Enter coarse block parameters and panchayat topography to generate high-res forecasts.")
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("🎛️ Input Parameters")
        b_temp = st.slider("Block Temperature (°C)", 25.0, 45.0, 38.0)
        b_rain = st.slider("Block Rainfall (mm)", 0.0, 100.0, 45.0)
        elevation = st.slider("Panchayat Elevation / Unchai (meters)", 10, 800, 250)

    # Downscaling Simulation Logic (Lapse rate & Topography)
    pred_temp = round(b_temp - (elevation * 0.0065), 2)
    pred_rain = round(b_rain * (1 + (elevation / 1500)), 2)

    with col_right:
        st.subheader("📍 High-Resolution Panchayat Output")
        st.success("Downscaling calculated successfully based on local elevation factors!")
        
        m1, m2 = st.columns(2)
        m1.metric(label="Panchayat Temperature", value=f"{pred_temp} °C")
        m2.metric(label="Panchayat Rainfall", value=f"{pred_rain} mm")

# --- TAB 3: AGRO-ADVISORY ---
with tab3:
    st.markdown('<p class="main-title">💡 Agro-Meteorological Advisory Services</p>', unsafe_allow_html=True)
    st.markdown("Get custom farming recommendations based on downscaled micro-climate data.")
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        selected_panchayat = st.selectbox("Select Panchayat", ["Panchayat 1 (Sadar)", "Panchayat 2", "Panchayat 3"])
        input_temp = st.number_input("Current Panchayat Temp (°C)", value=pred_temp if 'pred_temp' in locals() else 36.5)
        input_rain = st.number_input("Current Panchayat Rainfall (mm)", value=pred_rain if 'pred_rain' in locals() else 50.0)
        
    with c2:
        st.subheader("📋 Farm Recommendation")
        if input_rain > 50:
            st.warning("⚠️ **Heavy Rainfall Alert:** Avoid chemical fertilizer application and stop irrigation immediately in this Panchayat.")
        elif input_temp > 38:
            st.error("☀️ **Heat Stress Warning:** High temperature detected. Ensure adequate water supply/irrigation for standing crops.")
        else:
            st.success("✅ **Optimal Weather Conditions:** Safe for sowing, harvesting, and regular farming activities.")
