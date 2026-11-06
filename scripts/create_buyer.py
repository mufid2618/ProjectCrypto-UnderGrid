"""CLI untuk provisioning akun Buyer; tidak ada registrasi publik."""
import getpass
from auth.password_auth import create_buyer_account
from database.db_manager import init_db

if __name__ == "__main__":
    init_db()
    username = input("Username Buyer: ").strip().lower()
    password = getpass.getpass("Password (minimal 10 karakter): ")
    confirm = getpass.getpass("Ulangi password: ")
    if password != confirm:
        raise SystemExit("Password tidak sama.")
    buyer_id = create_buyer_account(username, password)
    print(f"Akun Buyer berhasil dibuat. ID: {buyer_id}. Lanjutkan provisioning dongle dan biometrik.")
