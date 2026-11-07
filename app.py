
"""Entry point aplikasi Undergrid."""
from __future__ import annotations

import streamlit as st

from config import APP_NAME
from database.db_manager import (
    init_db,
    get_buyer_by_id,
    add_log,
)
from blockchain.blockchain import create_genesis_block

from ui.styles import apply_styles
from ui.login_page import render_login
from ui.components import render_brand
from ui.dashboard import render_dashboard
from ui.catalog_page import render_catalog
from ui.messages_page import render_messages
from ui.blockchain_page import render_blockchain


# ---------------------------------------------------------
# KONFIGURASI APLIKASI
# ---------------------------------------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_styles()


# ---------------------------------------------------------
# INISIALISASI DATABASE DAN BLOCKCHAIN
# ---------------------------------------------------------

try:
    init_db()
    create_genesis_block()

except Exception as exc:
    st.error(f"Database belum siap: {exc}")
    st.info(
        "Jalankan scripts/generate_keys.py "
        "kemudian scripts/init_db.py."
    )
    st.stop()


# ---------------------------------------------------------
# FUNGSI LOGOUT
# ---------------------------------------------------------

def logout():
    """Mencatat logout dan menghapus seluruh session Buyer."""

    buyer_id = st.session_state.get("buyer_id")

    if buyer_id:
        try:
            add_log(
                int(buyer_id),
                "LOGOUT",
                {"session": "closed"}
            )
        except Exception:
            pass

    # Menghapus seluruh data autentikasi dan widget.
    st.session_state.clear()


# ---------------------------------------------------------
# TAHAP AUTENTIKASI
# ---------------------------------------------------------

# Jika belum login, tampilkan halaman autentikasi.
# Tahap USB, wajah, password, dan Vigenere
# diatur oleh ui/login_page.py.

if not st.session_state.get("buyer_id"):
    render_login()
    st.stop()


# ---------------------------------------------------------
# VALIDASI SESSION BUYER
# ---------------------------------------------------------

try:
    buyer_id = int(st.session_state.get("buyer_id"))
    buyer = get_buyer_by_id(buyer_id)

except (ValueError, TypeError):
    buyer = None

if not buyer or buyer["account_status"] != "active":
    st.session_state.clear()
    st.rerun()


# ---------------------------------------------------------
# SIDEBAR DAN NAVIGASI BUYER
# ---------------------------------------------------------

with st.sidebar:

    render_brand()

    st.caption(
        f"Authenticated as **{buyer['username']}**"
    )

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Catalog",
            "Secure messages",
            "Blockchain ledger"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.caption("LOCAL SECURITY SESSION")

    st.markdown(
        '<div class="ug-mono">'
        'PASSWORD · FACE · USB · CHALLENGE'
        '</div>',
        unsafe_allow_html=True
    )

    st.button(
        "LOG OUT",
        use_container_width=True,
        on_click=logout
    )


# ---------------------------------------------------------
# HALAMAN UTAMA UNDERGRID
# ---------------------------------------------------------

if page == "Overview":

    render_dashboard(buyer)

elif page == "Catalog":

    render_catalog(buyer["id"])

elif page == "Secure messages":

    render_messages(buyer["id"])

elif page == "Blockchain ledger":

    render_blockchain()
