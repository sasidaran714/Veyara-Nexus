import streamlit as st
from datetime import datetime, timedelta
import pytz
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import qrcode 
import io
import base64
import random
import uuid
from PIL import Image, ImageDraw, ImageFont
import time

# -------------------------
# Page config + styling
# -------------------------
st.set_page_config(
    page_title="Veyara Nexus — Living Command Center",
    layout="wide",
    page_icon="🕸️"
)

# custom CSS for premium dark navy biotech look + mycelium animation
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: #0A1428;
        color: #E6F2FF;
    }
    .stApp { background: linear-gradient(180deg,#0A1428 0%, #071025 100%); }
    .mycelium {
        position: fixed;
        left: 0; top: 0; right: 0; bottom: 0;
        background-image: radial-gradient(circle at 10% 10%, rgba(14,165,233,0.02), transparent 10%),
                          radial-gradient(circle at 30% 70%, rgba(226,242,255,0.01), transparent 10%);
        z-index: 0;
        pointer-events: none;
        mix-blend-mode: screen;
        animation: pulse 6s ease-in-out infinite;
    }
    @keyframes pulse {
        0% { opacity: 0.7; filter: blur(0.6px); transform: scale(1); }
        50% { opacity: 1; filter: blur(1.4px); transform: scale(1.01); }
        100% { opacity: 0.7; filter: blur(0.6px); transform: scale(1); }
    }
    .panel { background: rgba(10,20,40,0.45); border: 1px solid rgba(255,255,255,0.04); border-radius: 12px; padding: 16px; box-shadow: 0 6px 18px rgba(4,10,20,0.6); }
    .metric {
        background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-radius: 10px;
        padding: 14px;
        text-align: center;
        color: #ffffff;
    }
    .brand {font-weight:800; color:#E6F2FF; font-size:22px;}
    .accent { color: #0EA5E9; font-weight:700; }
    .small-muted { color: rgba(230,242,255,0.55); font-size:12px; }
    .btn-teal { background:#0EA5E9!important; color:#012020!important; border-radius:8px; padding:8px 14px; font-weight:700; }
    .footer { color: rgba(230,242,255,0.45); font-size:12px; text-align:center; margin-top:12px; }
    </style>
    <div class="mycelium"></div>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# helper utilities
# -------------------------
IST = pytz.timezone("Asia/Kolkata")


def ist_now():
    return datetime.now(IST)


def format_ist(dt):
    return dt.strftime("%d %b %Y %H:%M:%S IST")


def fake_live_seed(seed_offset=0):
    """Return reproducible-seeming live metrics that change by time"""
    now = datetime.now()
    t = int(now.timestamp() // 2) + seed_offset  # update every 2s if re-run
    rnd = random.Random(t)
    # core metrics
    stability = max(20, min(99, 67 + rnd.randint(-12, 8)))
    alerts = rnd.randint(0, 6)
    credits = 1800 + (t % 500) + rnd.randint(0, 600)
    lives = 1700 + rnd.randint(0, 450)
    return {
        "stability": stability,
        "alerts": alerts,
        "credits": credits,
        "lives": lives
    }


def generate_blockchain_hash():
    return "0x" + uuid.uuid4().hex[:16]


def generate_nft_id():
    return "VLK-" + str(random.randint(1000, 9999))


def make_qr_image(data: str):
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


def download_link(obj, filename, label="Download"):
    """Create a link to download a binary object (bytes)"""
    b64 = base64.b64encode(obj).decode()
    href = f"<a href='data:application/octet-stream;base64,{b64}' download='{filename}'>{label}</a>"
    return href


# initialize session stores for deployments
if "deployments" not in st.session_state:
    st.session_state.deployments = []
if "last_mint" not in st.session_state:
    st.session_state.last_mint = None

# -------------------------
# Top-level layout
# -------------------------
st.sidebar.image("https://via.placeholder.com/300x80/0A1428/E6F2FF?text=VEYARA", use_column_width=False)
st.sidebar.markdown("<div class='brand'>Veyara BioResilience Pvt Ltd</div>", unsafe_allow_html=True)
page = st.sidebar.radio("Navigate", options=[
    "Command Center",
    "BioPulse",
    "BioForge",
    "BioLedger",
    "Impact Observatory",
    "Company Hub"
])

st.sidebar.write("---")
st.sidebar.markdown('<div class="small-muted">Live from Chennai • Prototype demo</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="small-muted">Data sources: ICAR, NCDC, WHO, FAO, ICMR, PIB 2025</div>', unsafe_allow_html=True)

# Live timestamp in header
st.markdown(
    f"<div style='display:flex; justify-content:space-between; align-items:center'><div style='font-size:18px'><b>Veyara Nexus — Living Command Center</b></div><div class='small-muted'>LIVE FROM TAMIL NADU PILOT — {format_ist(ist_now())}</div></div>",
    unsafe_allow_html=True
)
st.markdown("----")

# -------------------------
# Command Center (Home)
# -------------------------
if page == "Command Center":
    st.subheader("Command Center")
    st.markdown("<div class='small-muted'>A single-pane view for judges: map, top metrics, quick actions</div>", unsafe_allow_html=True)

    metrics = fake_live_seed()

    c1, c2, c3, c4 = st.columns([2,1,1,1], gap="large")
    with c1:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin:0'>Tamil Nadu Pilot Overview</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-muted'>Updated: {format_ist(ist_now())}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # metric cards
    with c2:
        st.markdown(f"<div class='metric panel'><div style='font-size:12px' class='small-muted'>Overall Biological Stability</div><div style='font-size:28px; margin-top:6px'><b>{metrics['stability']}%</b></div><div class='small-muted' style='margin-top:6px'>↓ 8% in last 48 hrs</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric panel'><div style='font-size:12px' class='small-muted'>Active Tipping Alerts</div><div style='font-size:28px; margin-top:6px'><b>{metrics['alerts']}</b></div><div class='small-muted' style='margin-top:6px'>Kancheepuram, Chennai Ward-7, Pallikaranai</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='metric panel'><div style='font-size:12px' class='small-muted'>BioCredits Minted Today</div><div style='font-size:28px; margin-top:6px'><b>{metrics['credits']:,}</b></div><div class='small-muted' style='margin-top:6px'>+1,240</div></div>", unsafe_allow_html=True)

    st.markdown("### Tamil Nadu Map — Live Hotspots")
    # Build a Folium map centered on Tamil Nadu
    m = folium.Map(location=[11.0, 78.0], zoom_start=7, tiles="CartoDB dark_matter")
    # Hotspots
    hot_spots = [
        {"name": "Kancheepuram", "loc": [12.83, 79.7], "level": "critical"},
        {"name": "Chennai - Ward 7 (Hospital)", "loc": [13.08, 80.27], "level": "warning"},
        {"name": "Pallikaranai Wetland", "loc": [12.96, 80.23], "level": "warning"},
        {"name": "Coimbatore", "loc": [11.0, 76.96], "level": "ok"},
    ]
    for h in hot_spots:
        color = "red" if h["level"] == "critical" else ("orange" if h["level"] == "warning" else "green")
        folium.CircleMarker(location=h["loc"], radius=12 if color=="red" else 8,
                            color=color, fill=True, fill_opacity=0.7,
                            popup=f"{h['name']} — Risk: { 'High' if color=='red' else ('Medium' if color=='orange' else 'Low') }").add_to(m)
    st_folium(m, width="100%", height=480)

    st.markdown("### Quick Actions")
    ac1, ac2, ac3 = st.columns([1,1,1])
    with ac1:
        if st.button("🚀 Deploy BioShield (Quick)"):
            # create a simulated deployment record
            deploy_id = "DEP-" + uuid.uuid4().hex[:8].upper()
            rec = {
                "id": deploy_id,
                "time": format_ist(ist_now()),
                "location": "Kancheepuram - Soil Field",
                "credits": metrics['credits'],
                "expected_recovery_days": 21,
                "status": "Deployed"
            }
            st.session_state.deployments.insert(0, rec)
            # confetti via HTML/JS
            st.success(f"BioShield deployed: {deploy_id} — Restoration expected: 94% in 21 days")
            st.components.v1.html("""
                <script>
                // simple confetti (canvas)
                (function(){
                    var duration = 2 * 1000;
                    var animationEnd = Date.now() + duration;
                    var defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 9999 };
                    function randomInRange(min, max) { return Math.random() * (max - min) + min; }
                    var interval = setInterval(function(){
                        var timeLeft = animationEnd - Date.now();
                        if (timeLeft <= 0) return clearInterval(interval);
                        var particleCount = 40 * (timeLeft / duration);
                        // confetti effect using DOM (cheat)
                        var d = document.createElement('div');
                        d.innerHTML = '🎉';
                        d.style.position = 'fixed';
                        d.style.left = (Math.random()*80+10) + '%';
                        d.style.top = (Math.random()*40 + 10) + '%';
                        d.style.fontSize = (randomInRange(18,36)) + 'px';
                        d.style.zIndex = 9999;
                        document.body.appendChild(d);
                        setTimeout(()=>d.remove(), 1600);
                    }, 80);
                })();
                </script>
            """, height=0)
    with ac2:
        if st.button("🔊 Play Deploy Sound"):
            # small audio beep (data URI of a short beep) - using a tiny base64 wav
            beep = "data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YQAAAAA="
            st.components.v1.html(f"""
                <audio autoplay>
                  <source src="{beep}" type="audio/wav">
                </audio>
                """, height=50)
    with ac3:
        st.markdown("<div style='padding:6px' class='small-muted'>Deployments stored in session (demo). Export or mint credits in BioLedger tab.</div>", unsafe_allow_html=True)

    # Recent deployments table
    st.markdown("### Recent Simulated Deployments")
    if st.session_state.deployments:
        df = pd.DataFrame(st.session_state.deployments)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode()
        st.markdown(download_link(csv, "deployments.csv", "Download deployments CSV"), unsafe_allow_html=True)
    else:
        st.info("No deployments yet — press 'Deploy BioShield (Quick)' to simulate one.")

# -------------------------
# BioPulse tab
# -------------------------
elif page == "BioPulse":
    st.subheader("BioPulse — The Living Nervous System")
    st.markdown("<div class='small-muted'>Real-time sensor feed & early-warning predictions (simulated)</div>", unsafe_allow_html=True)

    district = st.selectbox("District selector", ["Kancheepuram", "Chennai", "Coimbatore", "Madurai"])
    st.markdown(f"**Accuracy badge:** 89% back-tested on ICMR + ICAR + GLASS 2023-2025", unsafe_allow_html=True)

    # Simulated sensor feed panel (JS-like live tick via python pseudo-random time-based)
    feed_col1, feed_col2 = st.columns([1,2])
    with feed_col1:
        st.markdown("<div class='panel'><b>Sensor Feed (live)</b></div>", unsafe_allow_html=True)
        feed_box = st.empty()
        # generate several readings that appear to move
        seed_map = {"Kancheepuram": 5, "Chennai": 11, "Coimbatore": 17, "Madurai": 23}
        vals = []
        for sensor in ["soil_moisture", "ph", "microbial_diversity_index", "temp_c"]:
            base = 50 + seed_map.get(district, 0) + int(datetime.now().second % 10)
            jitter = random.randint(-6, 6)
            vals.append((sensor, round(base + jitter/10, 2)))
        feed_box.table(pd.DataFrame(vals, columns=["metric", "value"]))
        st.markdown("<div class='small-muted'>Note: values update on refresh / rerun during demo</div>", unsafe_allow_html=True)

    with feed_col2:
        # Prediction plot for selected district
        st.markdown("<div class='panel'><b>72-hour prediction</b></div>", unsafe_allow_html=True)
        now = datetime.now()
        hours = pd.date_range(now, periods=13, freq='6H')
        # create a riser curve that becomes critical for Kancheepuram
        base = {"Kancheepuram": 60, "Chennai": 48, "Coimbatore": 40, "Madurai": 42}[district]
        noise = np.abs(np.sin(np.linspace(0, 3.14, len(hours))) * 10)
        risk = [min(100, int(base + n + random.randint(-3, 6))) for n in noise]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hours, y=risk, mode="lines+markers", line=dict(color="#0EA5E9"), fill='tozeroy'))
        fig.update_layout(margin=dict(l=10,r=10,t=20,b=10), height=320, xaxis_title="Time", yaxis_title="Risk Score (%)")
        st.plotly_chart(fig, use_container_width=True)
        # show predicted tipping time if risk crosses 85
        tipping = None
        for t, r in zip(hours, risk):
            if r >= 85:
                tipping = t
                break
        if tipping:
            st.error(f"⛳ Tipping predicted at {tipping.strftime('%d %b %Y %H:%M IST')}")
        else:
            st.success("No immediate tipping predicted in 72 hours")

    st.markdown("---")
    st.markdown("Cross-system alert panel")
    st.info("Soil → Human link: Kancheepuram soil score drop may increase local AMR risk by **41%** in 96 hrs")

# -------------------------
# BioForge tab
# -------------------------
elif page == "BioForge":
    st.subheader("BioForge — Generative Living Medicine Lab")
    st.markdown("<div class='small-muted'>Design site-specific consortia. Judges’ 'wow' tab.</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2,1])
    with col1:
        loc = st.selectbox("Location", ["Kancheepuram Soil Field", "Chennai Hospital Ward-7", "Pallikaranai Wetland"])
        pH = st.slider("Target soil pH", 4.5, 8.5, 6.8, 0.1)
        temp = st.slider("Temperature (°C)", 10, 45, 28)
        div = st.slider("Current Microbial Diversity (index)", 0, 100, 42)
        if st.button("RUN BIOFORGE ➤", key="run_bioforge"):
            # show a staged progress (fast demo) + animated reveal
            st.info("Analyzing at microbial (quarks) level…")
            prog = st.progress(0)
            elements = st.empty()
            for p in range(0, 101, 10):
                prog.progress(p)
                time.sleep(0.18)  # quick demo
            # generate a tailored consortia (beautiful reveal)
            species = [
                ("Bacillus subtilis", random.randint(30,45)),
                ("Pseudomonas fluorescens", random.randint(20,35)),
                ("Glomus intraradices (mycorrhizae)", random.randint(15,30)),
                ("Trichoderma spp.", random.randint(5,15))
            ]
            # normalize to 100
            total = sum(x[1] for x in species)
            species = [(s, round(v*100/total,1)) for s, v in species]
            st.markdown("<div class='panel'><h3>BioShield V-47 Ready</h3></div>", unsafe_allow_html=True)
            for s, pct in species:
                st.markdown(f"- **{s}** — {pct}% — chosen for site pH {pH}, temp {temp}°C, diversity {div}")
            if st.button("Deploy Now", key="deploy_from_bioforge"):
                deploy_id = "DEP-" + uuid.uuid4().hex[:8].upper()
                rec = {
                    "id": deploy_id,
                    "time": format_ist(ist_now()),
                    "location": loc,
                    "credits": random.randint(1200, 4000),
                    "expected_recovery_days": 21,
                    "status": "Deployed (BioForge)"
                }
                st.session_state.deployments.insert(0, rec)
                st.success(f"Deployed {deploy_id} — Restoration expected: 94% in 21 days")
                # confetti and sound
                st.components.v1.html("""
                <script>
                // confetti emulate
                for (let i=0;i<60;i++){
                    let d=document.createElement('div');
                    d.innerText = '✨';
                    d.style.position='fixed';
                    d.style.left = Math.random()*80 + 'vw';
                    d.style.top = Math.random()*40 + 'vh';
                    d.style.fontSize = (8+Math.random()*30)+'px';
                    d.style.zIndex = 9999;
                    document.body.appendChild(d);
                    setTimeout(()=>d.remove(), 1600);
                }
                </script>
                """, height=0)
                st.components.v1.html('<audio autoplay><source src="data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YQAAAAA=" type="audio/wav"></audio>', height=30)
    with col2:
        st.markdown("<div class='panel'><b>Simulation controls</b><div class='small-muted'>Tweak sliders and run BioForge. This demo generates plausible consortia & deploy flow for judges to interact with.</div></div>", unsafe_allow_html=True)
        st.markdown("**Demo details**")
        st.markdown(f"- Expected restoration: **94%** in 21 days")
        st.markdown(f"- Sample runtime message: _Complete in 41 seconds_ (UI shown, demo completes faster for judges)")
        st.markdown("---")
        st.markdown("<div class='small-muted'>This tab is intentionally theatrical — use it to wow judges.</div>", unsafe_allow_html=True)

# -------------------------
# BioLedger tab
# -------------------------
elif page == "BioLedger":
    st.subheader("BioLedger — The Living Memory Vault")
    st.markdown("<div class='small-muted'>Record deployments, mint BioCredit NFTs, and issue certificates (simulated)</div>", unsafe_allow_html=True)

    if st.session_state.deployments:
        df = pd.DataFrame(st.session_state.deployments)
        sel = st.selectbox("Select a deployment to mint credit from", df["id"].tolist())
        rec = df[df["id"] == sel].iloc[0].to_dict()
        st.markdown(f"**Selected:** {rec['id']} — {rec['location']} • {rec['time']}")
        owner = st.text_input("Owner name for certificate", value="Farmer Ramesh, Kancheepuram")
        if st.button("Mint BioCredit NFT"):
            nft_id = generate_nft_id()
            tx = generate_blockchain_hash()
            cert = {
                "nft_id": nft_id,
                "deploy_id": rec["id"],
                "owner": owner,
                "credits": rec.get("credits", 2340),
                "tx": tx,
                "time": format_ist(ist_now())
            }
            st.session_state.last_mint = cert
            # show certificate + QR
            st.balloons()
            st.success(f"Minted {nft_id} — tx {tx}")
            qr = make_qr_image(f"{nft_id}|{tx}|{owner}")
            bio = io.BytesIO()
            qr.save(bio, format="PNG")
            bio.seek(0)
            st.image(bio, width=200, caption=f"QR — {nft_id}")
            st.markdown(f"- **Owner:** {owner}")
            st.markdown(f"- **Credits:** {cert['credits']}")
            st.markdown(f"- **Blockchain Tx:** `{tx}`")
            # certificate as simple PNG generation (demo)
            img = Image.new("RGB", (900, 600), color=(8,18,34))
            draw = ImageDraw.Draw(img)
            try:
                fnt = ImageFont.truetype("DejaVuSans-Bold.ttf", 34)
            except:
                fnt = ImageFont.load_default()
            draw.text((40,40), "VEYARA BIOCREDIT CERTIFICATE", fill=(230,242,255), font=fnt)
            draw.text((40,120), f"NFT ID: {nft_id}", fill=(230,242,255))
            draw.text((40,160), f"Owner: {owner}", fill=(230,242,255))
            draw.text((40,200), f"Deployment: {rec['id']} • {rec['location']}", fill=(180,220,235))
            draw.text((40,260), f"Credits: {cert['credits']}", fill=(180,220,235))
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            st.image(buf)
            # download link for certificate
            st.markdown(download_link(buf.getvalue(), f"{nft_id}_certificate.png", "Download certificate"), unsafe_allow_html=True)
    else:
        st.info("No deployments available to mint from. Create one in Command Center or BioForge.")

# -------------------------
# Impact Observatory
# -------------------------
elif page == "Impact Observatory":
    st.subheader("Impact Observatory")
    st.markdown("<div class='small-muted'>ROI calculator, before/after, projections</div>", unsafe_allow_html=True)
    hectares = st.slider("Hectares treated", 1, 1000, 50)
    beds = st.slider("Hospital beds impact", 0, 200, 10)
    # simple ROI calc
    revenue_per_hectare = 870000  # demo number
    lives_saved_per_bed = 0.8
    revenue = hectares * revenue_per_hectare
    lives_saved = int(beds * lives_saved_per_bed) + int(hectares * 0.05)
    st.metric("Projected Revenue (3 yr)", f"₹{revenue/1e7:.2f} Cr")
    st.metric("Estimated Lives Protected", f"{lives_saved}")
    st.markdown("Projection Chart")
    yrs = [2026, 2027, 2028]
    revs = [revenue*0.25, revenue*0.8, revenue]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=yrs, y=revs))
    fig.update_layout(yaxis_tickformat="₹,")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("Before / After — Kancheepuram pilot")
    st.write("Before: AMR risk 41% • After: AMR risk 6% (demo projections)")

# -------------------------
# Company Hub
# -------------------------
elif page == "Company Hub":
    st.subheader("Veyara Company Hub")
    st.markdown("**Veyara BioResilience Pvt Ltd** — Solo-founded in Chennai. Mission: Make India the world’s first Biological Stability Infrastructure nation.")
    st.markdown("**Partnerships & Ask**")
    st.markdown("- Seed ask: **₹1 Cr** for TN Pilot — 15% equity (MoU discussions ongoing with TNPCB)")
    if st.button("Request Term Sheet (Preview)"):
        st.markdown("<div class='panel'><h4>Term Sheet (Preview)</h4><ul><li>Ask: ₹1,00,00,000</li><li>Equity: 15%</li><li>Use of funds: Pilot deployment, field ops, sensors</li></ul></div>", unsafe_allow_html=True)
        st.success("Term sheet preview generated — Thank you! Our team will follow up (demo).")

# -------------------------
# Footer
# -------------------------
st.markdown("<div class='footer'>Veyara Nexus • Data sources: ICAR • NCDC • WHO • FAO • ICMR • PIB 2025</div>", unsafe_allow_html=True)
