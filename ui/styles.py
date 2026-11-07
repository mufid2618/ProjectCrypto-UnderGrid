"""CSS tema dark premium untuk Streamlit."""
import streamlit as st


def apply_styles() -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root { --ug-bg:#101513; --ug-panel:#171f1b; --ug-border:#29362f; --ug-green:#46d39a; --ug-muted:#94a69c; }
    html, body, [class*="css"] { font-family:'Manrope',sans-serif; }
    .stApp { background: radial-gradient(circle at 80% 0%, #1a2b23 0%, #101513 42%); color:#e8f0eb; }
    [data-testid="stSidebar"] { background:#0c110f; border-right:1px solid var(--ug-border); }
    [data-testid="stSidebar"] * { color:#dce8e0; }
    h1,h2,h3 { letter-spacing:-.035em; }
    .ug-eyebrow { color:var(--ug-green); font:500 11px 'DM Mono',monospace; letter-spacing:.18em; text-transform:uppercase; }
    .ug-title { color:#f2f8f4; font-size:34px; font-weight:800; letter-spacing:-.05em; margin:3px 0 5px; }
    .ug-subtitle { color:var(--ug-muted); font-size:14px; margin-bottom:24px; }
    .ug-card { background:linear-gradient(145deg,rgba(27,39,32,.96),rgba(19,27,23,.96)); border:1px solid var(--ug-border); border-radius:16px; padding:18px 20px; margin-bottom:14px; }
    .ug-kpi { color:var(--ug-muted); font-size:12px; text-transform:uppercase; letter-spacing:.09em; }
    .ug-kpi-value { color:#f2f8f4; font-size:27px; font-weight:800; margin-top:8px; }
    .ug-mono { font-family:'DM Mono',monospace; color:#92e6bf; font-size:12px; overflow-wrap:anywhere; }
    .stButton>button { border-radius:10px; border:1px solid #3c8d68; background:#1d563d; color:#f1fff7; font-weight:700; }
    .stButton>button:hover { border-color:#69e6a8; background:#276d4d; color:white; }
    .stTextInput input,.stTextArea textarea { background:#111a15; border-color:#324238; color:#ecf5ef; }
    [data-testid="stMetric"] { background:#17211b; border:1px solid var(--ug-border); padding:14px; border-radius:14px; }
    hr { border-color:#29362f; }
    </style>
    """, unsafe_allow_html=True)


def render_page_heading(eyebrow: str, title: str, subtitle: str = "") -> None:
    st.markdown(f'<div class="ug-eyebrow">{eyebrow}</div><div class="ug-title">{title}</div><div class="ug-subtitle">{subtitle}</div>', unsafe_allow_html=True)
