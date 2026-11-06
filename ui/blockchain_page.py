"""Tampilan ledger dan verifikasi integritas chain."""
import json
import streamlit as st
from blockchain.blockchain import get_all_blocks, validate_chain
from ui.styles import render_page_heading


def render_blockchain() -> None:
    render_page_heading("TAMPER-EVIDENT LEDGER", "Blockchain ledger", "Ledger lokal append-only dengan linked hash SHA-256.")
    blocks = get_all_blocks()
    valid = validate_chain(blocks)
    st.metric("Chain validation", "VALID" if valid else "INVALID", delta="Integrity check")
    if st.button("VERIFY BLOCKCHAIN"):
        st.success("Seluruh blok valid." if validate_chain() else "Validasi gagal: ditemukan inkonsistensi.")
    for block in reversed(blocks):
        with st.expander(f"Block #{block['index']} · {block['event_type']} · {block['timestamp']}"):
            st.write("**Payload**")
            st.json(json.loads(block["payload_json"]))
            st.write("**Previous hash**")
            st.code(block["previous_hash"], language=None)
            st.write("**Current hash**")
            st.code(block["current_hash"], language=None)
    st.caption("Ledger ini merupakan simulasi lokal yang tamper-evident, bukan blockchain terdistribusi atau bukti pembayaran aktual.")
