"""Dashboard Buyer dan gerbang akses Catalog."""
from pathlib import Path
import streamlit as st
from database import db_manager
from blockchain.blockchain import validate_chain
from ui.styles import render_page_heading
from ui.components import stat_card

CAESAR_CIPHERTEXT = "EXNDNDWDORJ"
CAESAR_SHIFT = 3
CATALOG_CODE = "UG-CATALOG-2026"
GUIDE_PATH = Path(__file__).resolve().parent.parent / "data" / "panduan_rahasia.txt"


def caesar_decrypt(text: str, shift: int) -> str:
    result = []
    for char in text:
        if "A" <= char <= "Z":
            result.append(chr((ord(char) - ord("A") - shift) % 26 + ord("A")))
        elif "a" <= char <= "z":
            result.append(chr((ord(char) - ord("a") - shift) % 26 + ord("a")))
        else:
            result.append(char)
    return "".join(result)


def render_dashboard(buyer: dict) -> None:
    render_page_heading("BUYER CONSOLE", f"Welcome back, {buyer['username']}", "Ringkasan akses dan status keamanan akun Undergrid.")
    products = db_manager.product_count()
    blocks = db_manager.get_blocks()
    logs = db_manager.list_buyer_logs(buyer["id"])

    c1, c2, c3 = st.columns(3)
    with c1:
        stat_card("Available products", str(products), "Catalog inventory")
    with c2:
        stat_card("Ledger blocks", str(len(blocks)), "Local append-only chain")
    with c3:
        stat_card("Authentication", "VERIFIED", "Current session")

    st.markdown("### Security overview")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ug-card"><div class="ug-kpi">Identity controls</div><h4>Multi-factor access</h4><p style="color:#94a69c;font-size:13px">Argon2id password · Vigenère challenge · USB dongle · Face recognition</p><div class="ug-mono">SESSION AUTHENTICATED</div></div>', unsafe_allow_html=True)
    with col2:
        valid = validate_chain(blocks)
        status = "VALID" if valid else "INVALID"
        latest_hash = blocks[-1]["current_hash"][:24] if blocks else "NO BLOCKS"
        st.markdown(f'<div class="ug-card"><div class="ug-kpi">Blockchain integrity</div><h4>{status}</h4><p style="color:#94a69c;font-size:13px">SHA-256 linked hash validation</p><div class="ug-mono">{latest_hash}...</div></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### 01 · Secret Message")
    st.write("Selesaikan tantangan Caesar Cipher untuk mendapatkan file panduan akses katalog.")
    st.caption("Dekripsikan ciphertext berikut. Kunci pergeseran: 3.")
    st.code(CAESAR_CIPHERTEXT)
    answer = st.text_input("JAWABAN CAESAR CIPHER", placeholder="Masukkan plaintext hasil dekripsi", key="dashboard_caesar_answer")

    if st.button("VERIFIKASI JAWABAN", key="verify_caesar"):
        expected = caesar_decrypt(CAESAR_CIPHERTEXT, CAESAR_SHIFT)
        if answer.strip().upper() == expected:
            st.session_state["secret_txt_unlocked"] = True
            st.success("Jawaban benar. File panduan sekarang dapat diunduh.")
        else:
            st.session_state["secret_txt_unlocked"] = False
            st.error("Jawaban salah. Silakan coba kembali.")

    if st.session_state.get("secret_txt_unlocked", False):
        st.success("Tantangan berhasil diselesaikan.")
        try:
            guide_text = GUIDE_PATH.read_text(encoding="utf-8")
            st.download_button("DOWNLOAD panduan_rahasia.txt", data=guide_text.encode("utf-8"), file_name="panduan_rahasia.txt", mime="text/plain", use_container_width=True)
        except OSError as exc:
            st.error(f"File panduan tidak dapat dibaca: {exc}")

    st.divider()
    st.markdown("### 02 · Catalog Access")
    st.write("Masukkan kode rahasia yang tercantum di dalam file TXT.")
    code = st.text_input("KODE KATALOG", type="password", placeholder="Masukkan kode dari panduan TXT", key="dashboard_catalog_code")

    if st.button("VERIFIKASI KODE", key="verify_catalog_code"):
        if code.strip() == CATALOG_CODE:
            st.session_state["catalog_unlocked"] = True
            st.success("Kode benar. Akses Catalog berhasil dibuka.")
        else:
            st.session_state["catalog_unlocked"] = False
            st.error("Kode rahasia salah.")

    if st.session_state.get("catalog_unlocked", False):
        st.success("CATALOG UNLOCKED")
        if st.button("BUKA CATALOG", type="primary", use_container_width=True):
            st.session_state["show_catalog"] = True
            st.rerun()
    else:
        st.info("Catalog masih terkunci. Selesaikan verifikasi kode untuk membukanya.")

    st.divider()
    st.markdown("### Your recent activity")
    if not logs:
        st.info("Belum ada aktivitas yang tercatat.")
    else:
        for item in logs[:8]:
            st.markdown(f'<div class="ug-card"><b>{item["event_type"]}</b><div style="color:#94a69c;font-size:12px">{item["created_at"]}</div><div class="ug-mono">{item.get("details", {})}</div></div>', unsafe_allow_html=True)
