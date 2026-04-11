# src/processors/sorting_pipeline.py
# Modular CounterBalance Sorting Pipeline - Upgraded for UnClassZer0
# Drop bulky noisy chunks into INBOX → get clean reusable output in OUTBOX

import os
import hashlib
import json
import shutil
from pathlib import Path
from datetime import datetime

# Config - make OUTBOX your desktop entry point if you want
INBOX_DIR = Path("INBOX")
OUTBOX_DIR = Path("OUTBOX")          # ← This is your clean entry point on desktop (symlink it)
DUPLICATES_DIR = Path("OUTBOX_DUPLICATES")
PROCESSED_DIR = Path("OUTBOX_PROCESSED")
HASH_DB = Path("System_Logs/hashes/GLOBAL_INBOX_hashes.json")

HASH_DB.parent.mkdir(parents=True, exist_ok=True)
if not HASH_DB.exists():
    HASH_DB.write_text("{}")

def get_file_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def is_duplicate(file_path):
    db = json.loads(HASH_DB.read_text() or "{}")
    file_hash = get_file_hash(file_path)
    filename = file_path.name
    if file_hash in db or filename in db.values():
        return True
    return False

def register_file(file_path):
    db = json.loads(HASH_DB.read_text() or "{}")
    db[get_file_hash(file_path)] = file_path.name
    HASH_DB.write_text(json.dumps(db, indent=2))

def process_inbox():
    INBOX_DIR.mkdir(exist_ok=True)
    OUTBOX_DIR.mkdir(exist_ok=True)
    DUPLICATES_DIR.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(exist_ok=True)

    for file_path in INBOX_DIR.iterdir():
        if file_path.is_file():
            if is_duplicate(file_path):
                shutil.move(str(file_path), DUPLICATES_DIR / file_path.name)
                print(f"Duplicate moved: {file_path.name}")
            else:
                register_file(file_path)
                # TODO: plug in chunking + extraction here (modular)
                shutil.move(str(file_path), OUTBOX_DIR / file_path.name)
                print(f"Processed to OUTBOX: {file_path.name}")

if __name__ == "__main__":
    process_inbox()