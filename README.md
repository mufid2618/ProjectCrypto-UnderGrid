# UNDERGRID

**Private Access. Encrypted Identity. Verified Transactions.**

Undergrid adalah simulasi akademik marketplace privat berbasis Python dan Streamlit untuk tugas akhir mata kuliah Kriptografi. Proyek ini hanya menggunakan contoh barang legal, data fiktif, dan kontak pengujian. Aplikasi tidak memproses pembayaran, saldo, escrow, atau transfer uang.

## 1. Fitur utama

- Buyer-only: akun dibuat oleh pengelola melalui CLI; tidak ada registrasi publik dan tidak ada dashboard Admin di Streamlit.
- Login berlapis: password Argon2id, USB dongle ber-token acak, puzzle Vigenère sekali pakai, serta face recognition.
- Katalog: data CSV diimpor melalui script eksternal. Field sensitif dienkripsi sebelum masuk SQLite.
- Gambar produk: metadata JSON disisipkan ke PNG menggunakan LSB, kemudian PNG hasil proses dienkripsi menjadi file `.enc`.
- Secure messaging: Vigenère kemudian AES-256-CBC dengan HMAC-SHA256 Encrypt-then-MAC.
- Database: AES-256-GCM per kolom dengan AAD yang mengikat tabel, kolom, dan ID record.
- Blockchain: linked hash SHA-256 lokal untuk mencatat `PURCHASE_INTENT` dan `REQUEST_INFORMATION`.

## 2. Tujuh kriteria kriptografi

| Kriteria | Implementasi |
|---|---|
| 1. USB dongle dan biometrik | `auth/auth_dongle.py`, `auth/biometric_auth.py` |
| 2. Password hashing | Argon2id, `auth/password_auth.py` |
| 3. Cryptographic challenge | Vigenère Cipher acak per percobaan, `auth/cryptographic_challenge.py` |
| 4. Steganografi dan enkripsi file | LSB PNG dan ChaCha20-Poly1305, `crypto/steganography.py`, `crypto/file_cipher.py` |
| 5. Super encryption | Vigenère → AES-256-CBC → HMAC-SHA256, `crypto/vigenere_aes.py` |
| 6. Column-level encryption | AES-256-GCM + AAD, `crypto/db_crypto.py` dan `database/db_manager.py` |
| 7. Blockchain sederhana | Linked hash SHA-256, `blockchain/blockchain.py` |

## 3. Arsitektur folder

```text
ProjectCrypto-UnderGrid/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── auth/
├── crypto/
├── database/
├── blockchain/
├── services/
├── ui/
├── scripts/
├── data/
├── storage/
└── tests/
```

Setiap modul memiliki satu tanggung jawab. `app.py` hanya menjadi entry point dan pengarah halaman; business logic berada pada `services/`, sedangkan algoritma berada di `crypto/`, `auth/`, dan `blockchain/`.

## 4. Persyaratan perangkat

- Baseline kompatibilitas sesuai spesifikasi tugas: CPython 3.10 64-bit. Per 6 November 2026, Python 3.10 telah melewati masa dukungan upstream; untuk pengembangan baru pertimbangkan Python 3.11+ setelah memeriksa kompatibilitas `dlib` dan dependency biometrik.
- Windows 10/11 direkomendasikan untuk demonstrasi USB dongle dan webcam.
- Webcam untuk mengambil foto saat login.
- Flashdisk USB untuk dongle.
- Koneksi internet hanya diperlukan saat instalasi dependency / pemuatan font eksternal; aplikasi dapat berjalan lokal setelah persiapan.

`face-recognition` menggunakan `dlib`. Dokumentasi paket menyebut dukungan resmi utamanya pada macOS/Linux; Windows tidak didukung resmi dan hanya memiliki panduan komunitas. Instalasi pada Windows dapat membutuhkan CMake dan Visual C++ Build Tools. Kompatibilitas wheel `dlib` bergantung pada versi Python dan arsitektur. Jika instalasi gagal, gunakan environment yang didukung dlib atau siapkan dependency native secara manual.

## 5. Instalasi

```bash
git clone https://github.com/mufid2618/ProjectCrypto-UnderGrid.git
cd ProjectCrypto-UnderGrid
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Untuk Linux/macOS, aktivasi environment menggunakan `source .venv/bin/activate`.

## 6. Konfigurasi secret keys

Buat file `.env` yang berisi key acak:

```bash
python -m scripts.generate_keys
```

Script menolak menimpa `.env` yang sudah ada. Simpan backup `.env` secara offline dan pisahkan backup dari repository. Jangan pernah memasukkan `.env`, database produksi, template wajah, dongle asli, atau file `.enc` ke GitHub.

Key dipisahkan berdasarkan fungsi: `UNDERGRID_DB_KEY`, `UNDERGRID_FILE_KEY`, `UNDERGRID_AES_KEY`, `UNDERGRID_HMAC_KEY`, dan `UNDERGRID_DONGLE_SECRET`. `UNDERGRID_VIGENERE_KEY` digunakan oleh lapisan cipher klasik sebagai demonstrasi; kunci ini bukan pengganti key AES/HMAC.

## 7. Inisialisasi database dan provisioning Buyer

```bash
python -m scripts.init_db
python -m scripts.create_buyer
```

Untuk reset password Buyer melalui CLI, jalankan `python -m scripts.reset_buyer nama_buyer`.

Password diminta secara tersembunyi dan tidak dicatat ke log. Minimal password 10 karakter. Provisioning akun hanya tersedia melalui CLI pengelola.

### USB dongle

Hubungkan flashdisk, lalu jalankan:

```bash
python -m scripts.generate_dongle nama_buyer E:\
```

Contoh mount point Linux:

```bash
python -m scripts.generate_dongle nama_buyer /media/user/USB
```

Script menulis `undergrid.key` berisi token acak ke USB dan menyimpan HMAC token pada database. Token mentah tidak ditampilkan. Deteksi removable disk berbeda antar-OS dan tidak semua OS menyediakan volume serial. Mode serial dapat diaktifkan dengan `UNDERGRID_DONGLE_REQUIRE_SERIAL=true`; implementasi volume serial saat ini tersedia untuk Windows.

### Pendaftaran wajah

Ambil foto referensi yang jelas, satu wajah, lalu jalankan:

```bash
python -m scripts.enroll_face nama_buyer path/foto_referensi.jpg
```

Hanya encoding wajah terenkripsi yang disimpan; foto sumber tidak disalin ke database. Gunakan foto dengan izin pemiliknya.

## 8. Import katalog

Gunakan CSV yang memuat kolom `sku,name,category,description,price,seller_contact,image_path`. Kolom opsional: `specifications,secret_note,status`.

```bash
python -m scripts.import_catalog data/sample_catalog.csv
```

Contoh CSV dan gambar demo tersedia di folder `data/`. Import akan membuat PNG dengan pesan LSB, mengenkripsinya menggunakan ChaCha20-Poly1305, dan menyimpan path serta field sensitif terenkripsi di SQLite.

## 9. Menjalankan aplikasi

```bash
streamlit run app.py
```

Jalankan Streamlit **di komputer lokal yang memiliki flashdisk USB**. USB dongle diverifikasi oleh proses Python pada host Streamlit, bukan oleh browser dari jarak jauh. Untuk demonstrasi tugas, buka aplikasi melalui `http://localhost:8501` pada komputer yang sama.

## 10. Pengujian

```bash
pytest -q
```

Unit test menggunakan temporary SQLite dan key uji. Test USB memakai temporary folder/mocked mount; test biometrik memverifikasi enkripsi template tanpa membutuhkan webcam. Pengujian verifikasi wajah langsung memerlukan dependency `face_recognition` dan kamera.

## 11. Alur enkripsi

### Pesan

```text
Plaintext → Vigenère → PKCS7 → AES-256-CBC → HMAC-SHA256 → Base64
```

Saat dekripsi, HMAC diverifikasi **sebelum** CBC didekripsi. AES dan HMAC menggunakan kunci terpisah.

### Gambar

```text
PNG asli → LSB JSON → PNG stego → ChaCha20-Poly1305 → file .enc
```

Di sisi Buyer, file didekripsi di memori (`bytes`) dan diekstrak; tidak perlu membuat PNG plaintext permanen.

### Database

Setiap nilai sensitif dienkripsi memakai AES-256-GCM dengan nonce acak 12 byte. AAD dibuat dari identitas tabel, kolom, dan record, sehingga ciphertext tidak dapat dipindah ke kolom/record lain tanpa kegagalan autentikasi.

## 12. Panduan demonstrasi tujuh kriteria

1. Tunjukkan flashdisk berisi `undergrid.key`, lalu login dengan akun Buyer yang sudah diprovisikan. Lepas flashdisk untuk memperlihatkan kegagalan dongle.
2. Jelaskan bahwa database menyimpan string hash Argon2id, bukan password plaintext.
3. Tampilkan ciphertext Vigenère dan kunci petunjuk pada login. Dekripsi manual, lalu tunjukkan challenge berubah sesudah submit.
4. Import katalog, lalu tunjukkan file `.enc`. Pada halaman detail produk, metadata LSB diekstrak setelah dekripsi.
5. Kirim pesan, perlihatkan ciphertext di UI/database. Jalankan script export eksternal untuk dekripsi oleh pengelola.
6. Tunjukkan kolom database terenkripsi dan jelaskan AES-GCM/AAD. Mengubah AAD menyebabkan dekripsi gagal.
7. Buat purchase intent simulasi dan tunjukkan block baru serta tombol Verify Blockchain.

## 13. Catatan keamanan dan keterbatasan

- Vigenère challenge menampilkan key pada layar. Ini adalah puzzle verifikasi / demonstrasi cipher klasik, bukan CAPTCHA tahan bot atau faktor autentikasi mandiri.
- Face recognition dasar tidak menyediakan liveness detection; sistem rentan pada spoofing foto/video. Gunakan sebagai demonstrasi biometrik akademik, bukan sistem produksi.
- Face encoding adalah data biometrik sensitif. Batasi akses, dapatkan persetujuan eksplisit, dan hapus data saat tidak dibutuhkan.
- USB token file dapat disalin. Pengikatan serial volume hanya tersedia bila OS dan perangkat mendukung; ini bukan hardware security module.
- Key file `.env` adalah single point of failure. Kehilangan key membuat data terenkripsi tidak dapat dipulihkan. Buat backup offline yang aman.
- AES-CBC digunakan hanya karena tugas meminta algoritma tersebut; integritas diberikan oleh HMAC Encrypt-then-MAC dengan key terpisah.
- LSB adalah steganografi, bukan enkripsi. Kerahasiaan payload gambar bergantung pada enkripsi ChaCha20-Poly1305 terhadap file.
- Ledger SQLite lokal bersifat append-only pada tingkat aplikasi dan tamper-evident, bukan blockchain terdistribusi yang absolut immutable.
- `PURCHASE_INTENT` dan `REQUEST_INFORMATION` hanyalah event simulasi. Tidak ada pembayaran aktual, wallet, saldo, atau escrow.
- Aplikasi ini merupakan fondasi tugas akademik; lakukan review keamanan independen sebelum penggunaan nyata.

## 14. Troubleshooting

- **Key belum tersedia:** jalankan `python -m scripts.generate_keys`, pastikan `.env` berada di root proyek.
- **Database kosong:** jalankan `python -m scripts.init_db`, lalu buat Buyer dan import katalog.
- **Dongle tidak terdeteksi:** jalankan app di host yang sama dengan USB; periksa mount point dan permission file.
- **Face recognition gagal install:** gunakan Python 3.10 64-bit dan instalasi `dlib` yang kompatibel dengan OS.
- **File gambar gagal didekripsi:** pastikan key `UNDERGRID_FILE_KEY` tidak berubah dan file `.enc` utuh.
- **Pesan gagal didekripsi:** pastikan `UNDERGRID_VIGENERE_KEY`, AES key, dan HMAC key sama dengan saat pesan dienkripsi.

## 15. Status validasi pada lingkungan pengembangan

Pengujian yang dijalankan pada lingkungan pembuat proyek menggunakan CPython 3.13.5 dan library yang tersedia di runtime (cryptography 46.0.4, argon2-cffi 25.x, Pillow 12.x, NumPy 2.x, psutil 7.x, pytest 9.x). `python -m compileall -q .` berhasil dan seluruh unit/integration test yang tersedia lulus.

Streamlit dan `face_recognition` tidak tersedia di runtime tersebut, dan pemasangan dependency dari internet tidak dapat dilakukan di sana. Karena itu, tampilan Streamlit belum dijalankan langsung dalam sesi validasi ini, dan verifikasi wajah melalui webcam fisik belum diuji. Versi dependency di `requirements.txt` adalah pin instalasi proyek yang diselaraskan dengan baseline tugas; lakukan instalasi dan uji perangkat pada komputer demonstrasi sebelum presentasi.
