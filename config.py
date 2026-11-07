"""Konfigurasi pusat Undergrid."""
from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

DB_PATH = Path(os.getenv("UNDERGRID_DB_PATH", "data/undergrid.db"))
STORAGE_PATH = Path(os.getenv("UNDERGRID_STORAGE_PATH", "storage/products"))
if not DB_PATH.is_absolute():
    DB_PATH = PROJECT_ROOT / DB_PATH
if not STORAGE_PATH.is_absolute():
    STORAGE_PATH = PROJECT_ROOT / STORAGE_PATH

FACE_THRESHOLD = float(os.getenv("UNDERGRID_FACE_THRESHOLD", "0.48"))
DONGLE_REQUIRE_SERIAL = os.getenv("UNDERGRID_DONGLE_REQUIRE_SERIAL", "false").strip().lower() in {"1", "true", "yes"}
DONGLE_FILENAME = "undergrid.key"
APP_NAME = "UNDERGRID"
APP_TAGLINE = "Private Access. Encrypted Identity. Verified Transactions."
