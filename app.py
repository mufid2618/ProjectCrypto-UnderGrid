"""Entry point aplikasi Undergrid."""
from __future__ import annotations
import streamlit as st
from config import APP_NAME, APP_TAGLINE
from database.db_manager import init_db, get_buyer_by_id
from blockchain.blockchain import create_genesis_block
from ui.styles import apply_styles, render_page_heading
from ui.login_page import render_login
from ui.components import render_brand
from ui.dashboard import render_dashboard
from ui.catalog_page import render_catalog
from ui.messages_page import render_messages
from ui.blockchain_page import render_blockchain

st.set_page_config(page_title=APP_NAME, page_icon="🔐", layout="wide", initial_sidebar_state="expanded")
apply_styles()

try:
    init_db()
    create_genesis_block()
except Exception as exc:
    st.error(f"Database belum siap: {exc}")
    st.info("Jalankan scripts/generate_keys.py kemudian scripts/init_db.py.")
    st.stop()

if "buyer_id" not in st.session_state:
    render_login()
    st.stop()

buyer = get_buyer_by_id(int(st.session_state.buyer_id))
if not buyer or buyer["account_status"] != "active":
    st.session_state.clear()
    st.rerun()

with st.sidebar:
    render_brand()
    st.caption(f"Authenticated as **{buyer['username']}**")
    page = st.radio("NAVIGATION", ["Overview", "Catalog", "Secure messages", "Blockchain ledger"], label_visibility="collapsed")
    st.divider()
    st.caption("LOCAL SECURITY SESSION")
    st.markdown('<div class="ug-mono">PASSWORD · FACE · USB · CHALLENGE</div>', unsafe_allow_html=True)
    if st.button("LOG OUT", use_container_width=True):
        from database.db_manager import add_log
        add_log(buyer["id"], "LOGOUT", {"session": "closed"})
        st.session_state.clear()
        st.rerun()

if page == "Overview":
    render_dashboard(buyer)
elif page == "Catalog":
    render_catalog(buyer["id"])
elif page == "Secure messages":
    render_messages(buyer["id"])
elif page == "Blockchain ledger":
    render_blockchain()
