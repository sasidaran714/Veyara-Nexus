import streamlit as st
from datetime import datetime
import pytz
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import random
import uuid

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Veyara Nexus — Living Command Center",
    layout="wide",
    page_icon="🕸️"
)

# --------------------------------------------------
# GLOBAL DARK THEME FIX (STRONG WHITE TEXT)
# --------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: #0A1428;
        color: #E6F2FF !important;
    }

    .stApp {
        background: linear-gradient(180deg,#0A1428 0%, #071025 100%);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #071025 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #E6F2FF !important;
    }

    div[role="radiogroup"] label {
        color: #E6F2FF !important;
    }

    /* Panels */
    .panel {
        background: rgba(10,20,40,0.6);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 14px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 6px 18px rgba(0,0,0,0.5);
    }

    .metric-box {
        font-size: 36px;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 8px;
    }

    .footer {
        color: rgba(230,242,255,0.6);
        font-size: 12px;
        text-align: center;
        margin-top: 30px;
    }

    h2, h3 {
        color: #FFFFFF !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

IST = pytz.timezone("Asia/Kolkata")

def ist_now():
    return datetime.now(IST)

def format_ist(dt):
    return dt.strftime("%d %b %Y %H:%M:%S IST")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.markdown("## 🧬 Veyara BioResilience Pvt Ltd")

page = st.sidebar.radio("Navigate", [
    "Command Center",
    "BioPulse",
    "BioForge",
    "BioLedger",
    "Impact Observatory",
    "Company Hub"
])

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    f"""
    <h2>Veyara Nexus — Living Command Center</h2>
    <p style="opacity:0.7;">LIVE FROM TAMIL NADU PILOT — {format_ist(ist_now())}</p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# --------------------------------------------------
# COMMAND CENTER
# --------------------------------------------------
if page == "Command Center":

    st.subheader("Command Center")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            "<div class='panel'><div class='metric-box'>78%</div>Biological Stability</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            "<div class='panel'><div class='metric-box'>3</div>Active Alerts</div>",
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            "<div class='panel'><div class='metric-box'>2,840</div>BioCredits Minted</div>",
            unsafe_allow_html=True
        )

    st.markdown("### Tamil Nadu Map")

    m = folium.Map(location=[11.0, 78.0], zoom_start=7, tiles="CartoDB dark_matter")
    folium.CircleMarker([12.83,79.7], radius=10, color="red", fill=True).add_to(m)
    folium.CircleMarker([13.08,80.27], radius=8, color="orange", fill=True).add_to(m)

    st_folium(m, width="100%", height=450)

# --------------------------------------------------
# BIOPULSE
# --------------------------------------------------
elif page == "BioPulse":

    st.subheader("BioPulse — Live Prediction Engine")

    hours = pd.date_range(datetime.now(), periods=10, freq="6H")
    risk = np.random.randint(45, 90, size=10)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hours,
        y=risk,
        mode="lines+markers",
        line=dict(color="#0EA5E9")
    ))

    fig.update_layout(
        font=dict(color="#E6F2FF"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    fig.update_xaxes(color="#E6F2FF")
    fig.update_yaxes(color="#E6F2FF")

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# BIOFORGE
# --------------------------------------------------
elif page == "BioForge":

    st.subheader("BioForge — Generative Microbial Engine")

    location = st.selectbox("Select Location", [
        "Kancheepuram",
        "Chennai",
        "Coimbatore"
    ])

    if st.button("Run BioForge"):
        st.success("BioShield V-47 Generated Successfully")
        st.write("• Bacillus subtilis — 40%")
        st.write("• Pseudomonas fluorescens — 32%")
        st.write("• Mycorrhizae — 28%")

# --------------------------------------------------
# BIOLEDGER
# --------------------------------------------------
elif page == "BioLedger":

    st.subheader("BioLedger — NFT Minting Vault")

    if st.button("Mint BioCredit NFT"):
        nft = "VLK-" + str(random.randint(1000,9999))
        tx = "0x" + uuid.uuid4().hex[:12]
        st.success(f"Minted {nft}")
        st.write(f"Blockchain Tx: `{tx}`")

# --------------------------------------------------
# IMPACT OBSERVATORY
# --------------------------------------------------
elif page == "Impact Observatory":

    st.subheader("Impact Observatory")

    hectares = st.slider("Hectares Treated", 1, 500, 50)
    revenue = hectares * 870000

    fig = go.Figure()
    fig.add_trace(go.Bar(x=["2026","2027","2028"],
                         y=[revenue*0.3, revenue*0.7, revenue]))

    fig.update_layout(
        font=dict(color="#E6F2FF"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    fig.update_xaxes(color="#E6F2FF")
    fig.update_yaxes(color="#E6F2FF")

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# COMPANY HUB
# --------------------------------------------------
elif page == "Company Hub":

    st.subheader("Company Hub")
    st.write("Seed Ask: ₹1 Cr for Tamil Nadu Pilot")
    st.write("Equity Offered: 15%")
    st.write("Founder: Nishaanth — Chennai")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    "<div class='footer'>Veyara Nexus • Biological Stability Infrastructure</div>",
    unsafe_allow_html=True
)

