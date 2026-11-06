"""Dashboard ringkas Buyer."""
import streamlit as st
from database import db_manager
from blockchain.blockchain import validate_chain
from ui.styles import render_page_heading
from ui.components import stat_card


def render_dashboard(buyer: dict) -> None:
    render_page_heading("BUYER CONSOLE", f"Welcome back, {buyer['username']}", "Ringkasan akses dan status keamanan akun Undergrid.")
    products = db_manager.product_count()
    blocks = db_manager.get_blocks()
    logs = db_manager.list_buyer_logs(buyer["id"])
    c1, c2, c3 = st.columns(3)
    with c1: stat_card("Available products", str(products), "Catalog inventory")
    with c2: stat_card("Ledger blocks", str(len(blocks)), "Local append-only chain")
    with c3: stat_card("Authentication", "VERIFIED", "Current session")
    st.markdown("### Security overview")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ug-card"><div class="ug-kpi">Identity controls</div><h4>Multi-factor access</h4><p style="color:#94a69c;font-size:13px">Argon2id password · Vigenère challenge · USB dongle · Face recognition</p><div class="ug-mono">SESSION AUTHENTICATED</div></div>', unsafe_allow_html=True)
    with col2:
        valid = validate_chain(blocks)
        status = "VALID" if valid else "INVALID"
        st.markdown(f'<div class="ug-card"><div class="ug-kpi">Blockchain integrity</div><h4>{status}</h4><p style="color:#94a69c;font-size:13px">SHA-256 linked hash validation</p><div class="ug-mono">{blocks[-1]["current_hash"][:24] if blocks else "NO BLOCKS"}...</div></div>', unsafe_allow_html=True)
    st.markdown("### Your recent activity")
    if not logs:
        st.info("Belum ada aktivitas yang tercatat.")
    else:
        for item in logs[:8]:
            st.markdown(f'<div class="ug-card"><b>{item["event_type"]}</b><div style="color:#94a69c;font-size:12px">{item["created_at"]}</div><div class="ug-mono">{item.get("details", {})}</div></div>', unsafe_allow_html=True)
