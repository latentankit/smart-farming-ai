import streamlit as st
import requests
from PIL import Image
import os
import io
import base64
import datetime

# ============================================================
#  PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Smart Farming AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = os.getenv("API_URL", "https://ankit2293-smart-farming-api.hf.space")
GITHUB_URL = "https://github.com/latentankit/smart-farming-ai"

LANGUAGES = {
    "English": "en", "Hindi": "hi", "Tamil": "ta",
    "Telugu": "te", "Punjabi": "pa", "Bengali": "bn",
}

# ============================================================
#  GLOBAL STYLES + HERO
# ============================================================
st.markdown("""
<style>
    .block-container { padding-top: 1rem; max-width: 1200px; }
    #MainMenu, footer {visibility: hidden;}

    .hero {
        position: relative;
        background: linear-gradient(rgba(20,60,25,.62), rgba(20,60,25,.72)),
            url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1600&q=80');
        background-size: cover; background-position: center;
        padding: 70px 40px; border-radius: 20px; margin-bottom: 26px;
        box-shadow: 0 14px 40px rgba(20,60,25,.35);
    }
    .hero h1 { color:#fff; margin:0; font-size:2.8rem; font-weight:800;
        letter-spacing:.5px; text-shadow:0 2px 10px rgba(0,0,0,.35); }
    .hero p { color:#e8f5e9; margin:12px 0 0; font-size:1.2rem; max-width:680px;
        text-shadow:0 1px 6px rgba(0,0,0,.3); }
    .hero .pill { display:inline-block; margin-top:18px; background:rgba(255,255,255,.18);
        border:1px solid rgba(255,255,255,.35); color:#fff; padding:8px 16px;
        border-radius:30px; font-weight:600; font-size:.9rem; }

    .feat-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:26px; }
    @media (max-width:900px){ .feat-grid{ grid-template-columns:repeat(2,1fr);} }
    .feat { border-radius:16px; overflow:hidden; background:#fff; border:1px solid #ececec;
        box-shadow:0 4px 14px rgba(0,0,0,.06); transition:transform .2s ease, box-shadow .2s ease; }
    .feat:hover { transform:translateY(-4px); box-shadow:0 10px 24px rgba(46,125,50,.18); }
    .feat img { width:100%; height:120px; object-fit:cover; display:block; }
    .feat .body { padding:14px 16px; }
    .feat .body h4 { margin:0 0 4px; color:#1b5e20; font-size:1.05rem; }
    .feat .body p { margin:0; color:#667; font-size:.85rem; }

    .stTabs [data-baseweb="tab-list"]{ gap:6px; flex-wrap:wrap; }
    .stTabs [data-baseweb="tab"]{ background:#f0f8f0; border-radius:10px 10px 0 0;
        padding:10px 18px; font-weight:600; color:#2e7d32; }
    .stTabs [aria-selected="true"]{ background:#2e7d32 !important; color:#fff !important; }

    div[data-testid="stMetric"]{ background:#f7fbf7; border:1px solid #e0efe0; border-radius:14px;
        padding:14px 18px; box-shadow:0 2px 6px rgba(0,0,0,.04); }
    div[data-testid="stMetricValue"]{ color:#1b5e20; font-weight:700; }

    .stButton button{ border-radius:10px; font-weight:700; }

    .banner{ padding:16px 20px; border-radius:14px; margin:6px 0 16px; font-weight:600; }
    .b-green{ background:#e8f5e9; border-left:6px solid #2e7d32; color:#1b5e20; }
    .b-yellow{ background:#fff8e1; border-left:6px solid #f9a825; color:#7a5b00; }
    .b-red{ background:#ffebee; border-left:6px solid #c62828; color:#8e0000; }

    .footer{ text-align:center; color:#9aa; font-size:.85rem; margin-top:34px; }
</style>

<div class="hero">
    <h1>🌿 Smart Farming AI</h1>
    <p>Detect plant diseases instantly, get treatment plans, track weather &amp; rainfall,
       plan irrigation, and boost yield — all powered by deep learning.</p>
    <span class="pill">⚡ 99.68% accuracy • 38 disease classes • 14 crops</span>
</div>

<div class="feat-grid">
    <div class="feat">
        <img src="https://images.unsplash.com/photo-1416879595882-3373a0480b5b?auto=format&fit=crop&w=500&q=80">
        <div class="body"><h4>🔬 Disease Detection</h4><p>Upload a leaf, get instant diagnosis & severity.</p></div>
    </div>
    <div class="feat">
        <img src="https://images.unsplash.com/photo-1592210454359-9043f067919b?auto=format&fit=crop&w=500&q=80">
        <div class="body"><h4>🌤️ Weather &amp; Rain</h4><p>Live conditions + 24h rainfall forecast.</p></div>
    </div>
    <div class="feat">
        <img src="https://images.unsplash.com/photo-1574943320219-553eb213f72d?auto=format&fit=crop&w=500&q=80">
        <div class="body"><h4>💧 Irrigation</h4><p>Exact daily water needs for your crop.</p></div>
    </div>
    <div class="feat">
        <img src="https://images.unsplash.com/photo-1625246333195-78d9c38ad449?auto=format&fit=crop&w=500&q=80">
        <div class="body"><h4>📈 Yield Boost</h4><p>Predict output &amp; get improvement tips.</p></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
#  SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 🌿 Smart Farming AI")
    st.caption("AI assistant for plant health & farm decisions")
    st.divider()
    lang_name = st.selectbox("🌍 Chatbot Language", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[lang_name]
    st.divider()
    if st.button("⚡ Wake / Check Backend", use_container_width=True):
        with st.spinner("Pinging backend..."):
            try:
                r = requests.get(f"{API_URL}/", timeout=60)
                st.success("Backend online ✓") if r.status_code == 200 else st.warning(f"Status: {r.status_code}")
            except Exception:
                st.error("Backend waking up — retry in 30s")
    st.divider()
    st.markdown("**🔗 Links**")
    st.markdown(f"- [GitHub Repo]({GITHUB_URL})")
    st.markdown("- [Model Card](https://huggingface.co/ankit2293/plant-disease-efficientnet)")
    st.caption("Built by Ankit Kumar")

# ============================================================
#  TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🔬 Diagnose", "🗺️ Grad-CAM", "🌤️ Weather", "💧 Irrigation",
    "🌱 Fertilizer", "📈 Yield", "💬 Chatbot",
])

# ---------------- TAB 1 — DIAGNOSE ----------------
with tab1:
    col1, col2 = st.columns([1, 1.6])
    with col1:
        st.markdown("#### 📤 Upload Leaf Image")
        uploaded = st.file_uploader("Choose a leaf photo", type=["jpg", "jpeg", "png"], key="diagnose")
        if uploaded:
            st.image(Image.open(uploaded), caption="Uploaded Leaf", use_container_width=True)
            analyze = st.button("🔍 Analyze", type="primary", use_container_width=True)
        else:
            st.info("👆 Upload a clear leaf photo to begin.")
            analyze = False
    with col2:
        if uploaded and analyze:
            with st.spinner("🧠 Analyzing leaf..."):
                try:
                    files = {"file": ("leaf.jpg", uploaded.getvalue(), "image/jpeg")}
                    resp = requests.post(f"{API_URL}/predict", files=files, timeout=90)
                    if resp.status_code == 503:
                        st.warning("⚠️ Backend waking up — wait 30s and retry.")
                    else:
                        resp.raise_for_status()
                        result = resp.json()
                        disease = result["disease"].replace("___", " — ").replace("_", " ")
                        sev = result["severity"]; sev_label = sev.get("label", "Unknown"); sev_pct = sev.get("percentage", 0)
                        banner = {"Mild": "b-green", "Moderate": "b-yellow", "Severe": "b-red"}.get(sev_label, "b-green")
                        icon = {"Mild": "○", "Moderate": "🟡", "Severe": "●"}.get(sev_label, "⚪")
                        st.markdown(f'<div class="banner {banner}">{icon} <b>{disease}</b> &nbsp;•&nbsp; Severity: {sev_label} ({sev_pct}% infected) &nbsp;•&nbsp; Confidence: {result["confidence"]*100:.1f}%</div>', unsafe_allow_html=True)
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Disease", disease.split(" — ")[-1] if " — " in disease else disease)
                        m2.metric("Confidence", f"{result['confidence']*100:.1f}%")
                        m3.metric("Severity", f"{icon} {sev_label}")
                        st.markdown("##### 🔝 Top 3 Predictions")
                        for i, p in enumerate(result["top3_predictions"]):
                            nm = p["disease"].replace("___", " — ").replace("_", " ")
                            st.progress(p["confidence"], text=f"{i+1}. {nm} — {p['confidence']*100:.1f}%")
                        st.markdown("##### 💊 Treatment Plan")
                        st.markdown(result["treatment"])
                        now = datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")
                        tclean = result["treatment"].replace("**", "").replace("#", "").replace("*", "")
                        rows = "".join(f"<tr><td>{i+1}</td><td>{p['disease'].replace('___',' - ').replace('_',' ')}</td><td>{p['confidence']*100:.1f}%</td></tr>" for i, p in enumerate(result["top3_predictions"]))
                        html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
body{{font-family:Arial;margin:40px;color:#333}}.h{{background:#2e7d32;color:#fff;padding:20px;border-radius:8px}}
.s{{margin:18px 0;padding:14px;border:1px solid #ddd;border-radius:8px}}table{{width:100%;border-collapse:collapse}}
th{{background:#2e7d32;color:#fff;padding:9px;text-align:left}}td{{padding:8px;border:1px solid #ddd}}tr:nth-child(even){{background:#f0f8f0}}
</style></head><body><div class="h"><h1>🌿 Smart Farming AI — Diagnosis Report</h1><p>Generated: {now}</p></div>
<div class="s"><h2>Summary</h2><table><tr><th>Field</th><th>Value</th></tr>
<tr><td>Disease</td><td>{disease}</td></tr><tr><td>Confidence</td><td>{result['confidence']*100:.1f}%</td></tr>
<tr><td>Severity</td><td>{sev_label} ({sev_pct}% infected)</td></tr></table></div>
<div class="s"><h2>Top 3 Predictions</h2><table><tr><th>#</th><th>Disease</th><th>Confidence</th></tr>{rows}</table></div>
<div class="s"><h2>Treatment Plan</h2><p>{tclean.replace(chr(10),'<br>')}</p></div></body></html>"""
                        st.download_button("📥 Download Report (HTML)", data=html.encode("utf-8"),
                                           file_name=f"diagnosis_{result['disease']}.html", mime="text/html")
                        st.caption("💡 Open in browser → Ctrl/Cmd+P → Save as PDF")
                except requests.exceptions.Timeout:
                    st.error("✗ Timed out. Backend loading — retry in 30s.")
                except Exception as e:
                    st.error(f"✗ Error: {e}")
        else:
            st.info("Results will appear here after you click Analyze.")

# ---------------- TAB 2 — GRAD-CAM ----------------
with tab2:
    st.markdown("#### 🗺️ Grad-CAM Heatmap")
    st.caption("See which part of the leaf the AI focused on.")
    up_gc = st.file_uploader("Upload leaf image", type=["jpg", "jpeg", "png"], key="gradcam")
    if up_gc and st.button("🔥 Generate Heatmap", type="primary"):
        with st.spinner("Generating heatmap... (up to 60s)"):
            try:
                files = {"file": ("leaf.jpg", up_gc.getvalue(), "image/jpeg")}
                resp = requests.post(f"{API_URL}/gradcam", files=files, timeout=120)
                if resp.status_code == 503:
                    st.warning("⚠️ Backend waking up — retry in 30s.")
                else:
                    resp.raise_for_status()
                    img = Image.open(io.BytesIO(base64.b64decode(resp.json()["heatmap"])))
                    c1, c2 = st.columns(2)
                    c1.image(up_gc, caption="Original", use_container_width=True)
                    c2.image(img, caption="Grad-CAM Heatmap", use_container_width=True)
                    st.markdown('<div class="banner b-red">● Red = disease focus &nbsp;|&nbsp; ◦ Blue = healthy tissue</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"✗ Error: {e}")
    elif not up_gc:
        st.info("Upload a leaf image to generate the heatmap.")

# ---------------- TAB 3 — WEATHER ----------------
with tab3:
    st.markdown("#### 🌤️ Weather, Rainfall & Disease Risk")
    st.caption("Live conditions + 24-hour rainfall forecast.")
    def _local(ts, off): return datetime.datetime.utcfromtimestamp(ts + off).strftime("%a %d %b, %I:%M %p")
    def _clk(ts, off):   return datetime.datetime.utcfromtimestamp(ts + off).strftime("%I:%M %p")
    c1, c2 = st.columns([1, 1.8])
    with c1:
        city = st.text_input("City", placeholder="e.g. Mumbai, Delhi, Katra")
        if st.button("🌍 Get Weather", type="primary"):
            if city:
                with st.spinner("Fetching live weather..."):
                    try:
                        key = os.getenv("OPENWEATHER_API_KEY", "")
                        d = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric", timeout=10).json()
                        if d.get("cod") != 200:
                            st.error(f"✗ City not found: {city}")
                        else:
                            tz = d.get("timezone", 0); temp = d["main"]["temp"]; hum = d["main"]["humidity"]
                            risks = {
                                "Late Blight": "● High" if hum > 80 and 10 < temp < 24 else "🟡 Medium" if hum > 70 and 10 < temp < 24 else "○ Low",
                                "Powdery Mildew": "● High" if 20 < temp < 30 and hum < 60 else "🟡 Medium" if 15 < temp < 30 and hum < 70 else "○ Low",
                                "Rust": "● High" if hum > 75 and 15 < temp < 25 else "🟡 Medium" if hum > 65 and 15 < temp < 25 else "○ Low",
                                "Bacterial Blight": "● High" if hum > 80 and temp > 28 else "🟡 Medium" if hum > 70 and temp > 25 else "○ Low",
                            }
                            fc = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}&units=metric", timeout=10).json()
                            forecast = []
                            if str(fc.get("cod")) == "200":
                                for s in fc["list"][:8]:
                                    forecast.append({"time": _clk(s["dt"], tz), "rain": s.get("rain", {}).get("3h", 0.0), "pop": int(s.get("pop", 0) * 100)})
                            st.session_state["weather"] = {
                                "city": f'{d["name"]}, {d["sys"].get("country","")}', "temp": temp, "feels": d["main"]["feels_like"],
                                "hum": hum, "pressure": d["main"]["pressure"], "wind": d["wind"]["speed"], "wdeg": d["wind"].get("deg", 0),
                                "clouds": d.get("clouds", {}).get("all", 0), "vis": d.get("visibility", 0) / 1000,
                                "rain1h": d.get("rain", {}).get("1h", 0.0), "desc": d["weather"][0]["description"],
                                "time": _local(d["dt"], tz), "sunrise": _clk(d["sys"]["sunrise"], tz), "sunset": _clk(d["sys"]["sunset"], tz),
                                "risks": risks, "forecast": forecast,
                            }
                    except Exception as e:
                        st.error(f"✗ Error: {e}")
            else:
                st.warning("Please enter a city name.")
    with c2:
        if "weather" in st.session_state:
            w = st.session_state["weather"]
            st.markdown(f"### 📍 {w['city']}")
            st.caption(f"🕒 {w['time']} • {w['desc'].capitalize()}")
            a, b, c = st.columns(3)
            a.metric("🌡️ Temp", f"{w['temp']}°C", f"Feels {w['feels']}°C")
            b.metric("💧 Humidity", f"{w['hum']}%")
            c.metric("🌧️ Rain (1h)", f"{w['rain1h']} mm")
            d_, e_, f_ = st.columns(3)
            d_.metric("💨 Wind", f"{w['wind']} m/s", f"{w['wdeg']}°")
            e_.metric("◦ Pressure", f"{w['pressure']} hPa")
            f_.metric("☁️ Clouds", f"{w['clouds']}%")
            g_, h_, i_ = st.columns(3)
            g_.metric("👁️ Visibility", f"{w['vis']:.1f} km")
            h_.metric("🌅 Sunrise", w["sunrise"])
            i_.metric("🌇 Sunset", w["sunset"])
            if w["forecast"]:
                st.markdown("##### 🌧️ Next 24h Rainfall Forecast")
                cols = st.columns(len(w["forecast"]))
                for col, s in zip(cols, w["forecast"]):
                    col.metric(s["time"], f"{s['rain']} mm", f"{s['pop']}% rain")
            st.markdown("##### ⚠️ Disease Risk Today")
            for dis, rk in w["risks"].items():
                st.markdown(f"**{dis}:** {rk}")
        else:
            st.info("Enter a city and click Get Weather.")

# ---------------- TAB 4 — IRRIGATION ----------------
with tab4:
    st.markdown("#### 💧 Smart Irrigation Advisor")
    CROPS = {"Tomato":5.0,"Potato":4.5,"Corn":5.5,"Apple":4.0,"Grape":3.5,"Wheat":4.0,"Rice":8.0,"Pepper":4.5,"Strawberry":3.5,"Soybean":4.5}
    STAGE = {"seedling":0.5,"growing":1.0,"flowering":1.25,"fruiting":1.05}
    c1, c2 = st.columns(2)
    with c1:
        crop = st.selectbox("🌱 Crop", list(CROPS.keys()))
        stage = st.selectbox("📅 Growth Stage", list(STAGE.keys()))
        soil = st.selectbox("🌍 Soil Type", ["Loamy","Sandy","Clay","Silt"])
        area = st.number_input("📐 Area (hectares)", min_value=0.1, value=1.0, step=0.1)
    with c2:
        temp = st.slider("🌡️ Temperature (°C)", 0, 50, 25)
        hum = st.slider("💧 Humidity (%)", 0, 100, 60)
        rain = st.slider("🌧️ Rainfall today (mm)", 0.0, 50.0, 0.0, step=0.5)
    if st.button("💧 Calculate Irrigation", type="primary"):
        base = CROPS[crop] * STAGE[stage]
        tf = 1.3 if temp > 35 else 1.15 if temp > 30 else 0.8 if temp < 15 else 1.0
        hf = 0.85 if hum > 80 else 1.2 if hum < 40 else 1.0
        sf = {"Sandy":1.3,"Loamy":1.0,"Clay":0.8,"Silt":0.9}[soil]
        daily = base * tf * hf * sf
        net = max(0, daily - rain)
        liters = round(net * area * 10000)
        sched = ("No irrigation needed — rainfall sufficient","Check tomorrow") if net == 0 else \
                ("Light irrigation","Every 3-4 days") if net < 2 else \
                ("Moderate irrigation","Every 2 days") if net < 4 else ("Heavy irrigation","Daily")
        st.markdown(f'<div class="banner b-green">▪ {sched[0]} &nbsp;•&nbsp; 🔄 {sched[1]}</div>', unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("Daily Need", f"{daily:.2f} mm")
        m2.metric("Net Need", f"{net:.2f} mm")
        m3.metric("Total Water", f"{liters:,} L")
        st.info("⏰ Best time: early morning (5–7 AM) or evening (6–8 PM)")

# ---------------- TAB 5 — FERTILIZER ----------------
with tab5:
    st.markdown("#### 🌱 Fertilizer Recommendation")
    NPK = {"Tomato":(120,80,100),"Potato":(150,100,150),"Corn":(135,60,40),"Wheat":(120,60,40),
           "Rice":(100,50,50),"Apple":(70,35,70),"Grape":(60,30,60),"Soybean":(30,75,45),
           "Pepper":(110,70,90),"Strawberry":(80,60,80)}
    c1, c2 = st.columns(2)
    with c1:
        fcrop = st.selectbox("🌱 Crop", list(NPK.keys()), key="fcrop")
        fstage = st.selectbox("📅 Growth Stage", ["seedling","growing","flowering","fruiting"], key="fstage")
    with c2:
        fsoil = st.selectbox("🌍 Soil Fertility", ["Low","Medium","High"], key="fsoil")
        farea = st.number_input("📐 Area (hectares)", min_value=0.1, value=1.0, step=0.1, key="farea")
    if st.button("🌱 Get Recommendation", type="primary"):
        n, p, k = NPK[fcrop]
        smul = {"Low":1.2,"Medium":1.0,"High":0.8}[fsoil]
        stmul = {"seedling":0.4,"growing":1.0,"flowering":1.2,"fruiting":0.9}[fstage]
        n, p, k = n*smul*stmul, p*smul*stmul, k*smul*stmul
        dap = p / 0.46
        urea = max(0, (n - dap*0.18)) / 0.46
        mop = k / 0.60
        st.markdown(f'<div class="banner b-green">Target NPK for {fcrop} ({fstage}, {fsoil}): {n:.0f}-{p:.0f}-{k:.0f} kg/ha</div>', unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("Urea (46% N)", f"{urea*farea:.0f} kg")
        m2.metric("DAP (P+N)", f"{dap*farea:.0f} kg")
        m3.metric("MOP (60% K)", f"{mop*farea:.0f} kg")
        st.info("💡 Split nitrogen into 2–3 doses. Apply phosphorus at sowing/transplanting.")

# ---------------- TAB 6 — YIELD ----------------
with tab6:
    st.markdown("#### 📈 Crop Yield Prediction")
    YIELD = {"Tomato":(25,"t/ha"),"Potato":(20,"t/ha"),"Corn":(5.5,"t/ha"),"Wheat":(3.5,"t/ha"),
             "Rice":(4.5,"t/ha"),"Apple":(15,"t/ha"),"Grape":(8,"t/ha"),"Soybean":(2.5,"t/ha"),
             "Sugarcane":(70,"t/ha"),"Cotton":(1.8,"t/ha")}
    c1, c2 = st.columns(2)
    with c1:
        yc = st.selectbox("🌱 Crop", list(YIELD.keys()), key="yc")
        ya = st.number_input("📐 Area (hectares)", min_value=0.1, value=1.0, step=0.1, key="ya")
        ys = st.selectbox("🌍 Soil Type", ["Loamy","Sandy","Clay","Silt"], key="ys")
        yi = st.selectbox("💧 Irrigation", ["Drip","Sprinkler","Flood","Rainfed"], key="yi")
    with c2:
        yr = st.slider("🌧️ Annual Rainfall (mm)", 200, 3000, 800, key="yr")
        yt = st.slider("🌡️ Avg Temp (°C)", 10, 45, 25, key="yt")
        yf = st.slider("🌿 Fertilizer (kg/ha)", 0, 300, 100, key="yf")
        yd = st.selectbox("🦠 Disease Pressure", ["None","Low","Medium","High"], key="yd")
    if st.button("📈 Predict Yield", type="primary", key="ybtn"):
        base, unit = YIELD[yc]
        sf = {"Loamy":1.15,"Clay":0.95,"Silt":1.05,"Sandy":0.85}[ys]
        rf = 0.7 if yr<400 else 0.85 if yr<700 else 1.1 if yr<1200 else 1.05 if yr<2000 else 0.9
        tf = 0.75 if yt<15 else 0.9 if yt<20 else 1.1 if yt<30 else 0.95 if yt<35 else 0.75
        irf = {"Drip":1.2,"Sprinkler":1.1,"Flood":1.0,"Rainfed":0.85}[yi]
        ff = 0.8 if yf<50 else 0.95 if yf<100 else 1.1 if yf<200 else 1.05
        df = {"None":1.0,"Low":0.92,"Medium":0.8,"High":0.6}[yd]
        pred = base*sf*rf*tf*irf*ff*df
        ratio = pred/base
        rating = "🌟 Excellent" if ratio>=1.1 else "✓ Good" if ratio>=0.9 else "⚠️ Average" if ratio>=0.7 else "✗ Poor"
        bn = "b-green" if ratio>=0.9 else "b-yellow" if ratio>=0.7 else "b-red"
        st.markdown(f'<div class="banner {bn}">{rating} — {pred:.1f} {unit} &nbsp;•&nbsp; {((ratio-1)*100):+.0f}% vs average</div>', unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("Predicted Yield", f"{pred:.1f} {unit}")
        m2.metric("Total Production", f"{pred*ya:.1f} t")
        m3.metric("Rating", rating)
        st.markdown("##### ▪ Factor Impact")
        for nmf, vf in {"Soil":sf,"Rainfall":rf,"Temperature":tf,"Irrigation":irf,"Fertilizer":ff,"Disease":df}.items():
            st.markdown(f"{'○' if vf>=1 else '●'} **{nmf}:** {vf:.2f}× ({(vf-1)*100:+.0f}%)")

# ---------------- TAB 7 — CHATBOT ----------------
with tab7:
    st.markdown(f"#### 💬 Farming Assistant &nbsp; <span style='font-size:.8rem;color:#888'>({lang_name})</span>", unsafe_allow_html=True)
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.api_history = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    if prompt := st.chat_input("Ask about diseases, treatments, farming..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.api_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    resp = requests.post(f"{API_URL}/chat",
                        json={"message": prompt, "history": st.session_state.api_history[:-1]}, timeout=60)
                    if resp.status_code == 503:
                        st.warning("⚠️ Backend waking up — retry in 30s.")
                    else:
                        resp.raise_for_status()
                        reply = resp.json()["response"]
                        if lang_code != "en":
                            try:
                                from deep_translator import GoogleTranslator
                                reply = GoogleTranslator(source="auto", target=lang_code).translate(reply)
                            except Exception:
                                st.caption("⚠️ Translation unavailable — showing English")
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                        st.session_state.api_history.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"✗ Error: {e}")

# ============================================================
#  FOOTER
# ============================================================
st.markdown('<div class="footer">🌿 Smart Farming AI • EfficientNet-B3 (99.68%) • Built by Ankit Kumar</div>', unsafe_allow_html=True)
