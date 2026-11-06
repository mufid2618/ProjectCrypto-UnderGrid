"""Login Buyer dengan password Argon2id, USB dongle, puzzle, dan face match."""
from __future__ import annotations
import streamlit as st
from auth.cryptographic_challenge import generate_challenge, consume_challenge
from auth.password_auth import authenticate_buyer
from auth.auth_dongle import verify_dongle, detect_removable_drives
from auth.biometric_auth import load_encrypted_face_template, verify_face
from database import db_manager
from ui.components import render_brand


def _get_challenge():
    if "ug_challenge" not in st.session_state:
        st.session_state.ug_challenge = generate_challenge()
    return st.session_state.ug_challenge


def render_login() -> None:
    left, right = st.columns([1.08, 0.92], gap="large")
    with left:
        render_brand()
        st.markdown("## Authenticate your identity")
        st.caption("Akses privat untuk Buyer terdaftar. Tidak tersedia registrasi publik.")
        username = st.text_input("USERNAME", placeholder="buyer.username", key="ug_username")
        password = st.text_input("PASSWORD", type="password", placeholder="Enter your password", key="ug_password")
        photo = st.camera_input("FACE VERIFICATION · Ambil foto langsung dari webcam")
        st.caption("Gunakan kamera pada komputer yang menjalankan server Streamlit lokal.")
        if st.button("AUTHENTICATE", use_container_width=True):
            challenge = _get_challenge()
            token = st.session_state.get("ug_token", "")
            challenge_ok = consume_challenge(challenge, token)
            # Challenge selalu dibuang setelah satu submit, berhasil maupun gagal.
            st.session_state.ug_challenge = generate_challenge()
            buyer = db_manager.get_buyer_by_username((username or "").strip().lower())
            password_ok = bool(buyer and buyer["account_status"] == "active" and authenticate_buyer(username or "", password or ""))
            dongle_ok = bool(buyer and verify_dongle(buyer))
            face_ok = False
            if buyer and buyer.get("face_encoding_enc") and photo is not None:
                try:
                    reference = load_encrypted_face_template(buyer["face_encoding_enc"], buyer["id"])
                    face_ok = verify_face(photo.getvalue(), reference)
                except (ValueError, RuntimeError):
                    face_ok = False
            if challenge_ok and password_ok and dongle_ok and face_ok:
                st.session_state.buyer_id = buyer["id"]
                st.session_state.buyer_username = buyer["username"]
                db_manager.add_log(buyer["id"], "LOGIN_SUCCESS", {"method": "password+vigenere+dongle+face"})
                st.success("Autentikasi berhasil.")
                st.rerun()
            else:
                st.error("Autentikasi gagal. Periksa kredensial, challenge, USB dongle, dan verifikasi wajah.")
        st.markdown("<div style='color:#73847a;font-size:11px;margin-top:16px'>UNDERGRID · LOCALHOST ACCESS · NO PUBLIC SIGN-UP</div>", unsafe_allow_html=True)
    with right:
        challenge = _get_challenge()
        st.markdown('<div class="ug-card">', unsafe_allow_html=True)
        st.markdown('<div class="ug-eyebrow">01 / CRYPTOGRAPHIC CHALLENGE</div>', unsafe_allow_html=True)
        st.markdown("### Vigenère Cipher")
        st.caption("Decrypt the encrypted text using the provided Vigenère key and enter the plaintext below.")
        st.markdown("**Ciphertext**")
        st.code(challenge["ciphertext"], language=None)
        st.markdown("**Decryption key**")
        st.code(challenge["key"], language=None)
        st.text_input("DECRYPTED TOKEN", key="ug_token", placeholder="Enter plaintext A-Z")
        if st.button("REGENERATE CHALLENGE", use_container_width=True):
            challenge["used"] = True
            st.session_state.ug_challenge = generate_challenge()
            st.session_state.ug_token = ""
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        drives = detect_removable_drives()
        dongle_label = f"{len(drives)} removable device(s) detected" if drives else "No removable device detected"
        st.markdown('<div class="ug-card">', unsafe_allow_html=True)
        st.markdown('<div class="ug-eyebrow">02 / HARDWARE PRESENCE</div>', unsafe_allow_html=True)
        st.markdown("**USB Dongle Status**")
        st.markdown(f'<div class="ug-mono">{dongle_label}</div>', unsafe_allow_html=True)
        st.caption("USB diverifikasi pada host/server Streamlit, bukan otomatis pada perangkat browser jarak jauh.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.warning("Face recognition standar tidak memiliki liveness detection. Foto/video spoofing belum sepenuhnya dicegah.")
