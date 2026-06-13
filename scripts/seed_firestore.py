"""
Kanjo - Firestore Seed Script
Loads address_labels and token_metadata into Firestore.

Usage:
  export GOOGLE_CLOUD_PROJECT=your-project-id
  python scripts/seed_firestore.py

Requires:
  pip install google-cloud-firestore
"""

import json
import sys
from pathlib import Path

from google.cloud import firestore


def load_json(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def seed_address_labels(db: firestore.Client, data: dict) -> int:
    collection = db.collection("address_labels")
    count = 0
    for entry in data["addresses"]:
        address = entry["address"].lower()
        doc = {
            "label": entry["label"],
            "category": entry["category"],
        }
        if "subcategory" in entry:
            doc["subcategory"] = entry["subcategory"]
        if "note" in entry:
            doc["note"] = entry["note"]
        collection.document(address).set(doc)
        count += 1
    return count


def seed_token_metadata(db: firestore.Client, data: dict) -> int:
    collection = db.collection("token_metadata")
    count = 0
    for token in data["tokens"]:
        address = token["address"].lower()
        doc = {
            "symbol": token["symbol"],
            "name": token["name"],
            "decimals": token["decimals"],
            "type": token["type"],
        }
        if token.get("pegged_to"):
            doc["pegged_to"] = token["pegged_to"]
        if token.get("note"):
            doc["note"] = token["note"]
        collection.document(address).set(doc)
        count += 1
    return count


def main():
    base = Path(__file__).parent.parent / "firestore"

    labels_path = base / "address_labels.json"
    tokens_path = base / "token_metadata.json"

    if not labels_path.exists():
        print(f"[ERROR] {labels_path} not found")
        sys.exit(1)
    if not tokens_path.exists():
        print(f"[ERROR] {tokens_path} not found")
        sys.exit(1)

    db = firestore.Client()
    print(f"[INFO] Connected to project: {db.project}")

    labels_data = load_json(str(labels_path))
    n_labels = seed_address_labels(db, labels_data)
    print(f"[OK] address_labels: {n_labels} entries")

    tokens_data = load_json(str(tokens_path))
    n_tokens = seed_token_metadata(db, tokens_data)
    print(f"[OK] token_metadata: {n_tokens} entries")

    print("[DONE] Firestore seeding complete")


if __name__ == "__main__":
    main()
