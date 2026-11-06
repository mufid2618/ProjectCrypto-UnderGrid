"""Inisialisasi schema SQLite dan genesis block."""
from database.db_manager import init_db
from blockchain.blockchain import create_genesis_block

if __name__ == "__main__":
    init_db()
    create_genesis_block()
    print("Database Undergrid berhasil diinisialisasi.")
