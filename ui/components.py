"""Komponen UI reusable."""
import streamlit as st


def render_brand() -> None:
    st.markdown("""
    <div style="padding:8px 0 25px">
      <div class="ug-eyebrow">PRIVATE ACCESS SYSTEM</div>
      <div style="font-size:25px;font-weight:800;letter-spacing:-1.5px">UNDER<span style="color:#46d39a">GRID</span></div>
      <div style="font-size:11px;color:#82958a">Private Access. Encrypted Identity.</div>
    </div>
    """, unsafe_allow_html=True)


def stat_card(label: str, value: str, detail: str = "") -> None:
    st.markdown(
        f'<div class="ug-card"><div class="ug-kpi">{label}</div><div class="ug-kpi-value">{value}</div><div style="font-size:11px;color:#94a69c;margin-top:5px">{detail}</div></div>',
        unsafe_allow_html=True,
    )
