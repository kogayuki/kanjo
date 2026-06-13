"""
Kanjo - Demo Wallet Finder
Finds Polygon wallets with rich JPYC + multi-token ERC-20 activity.

Usage:
  export POLYGONSCAN_API_KEY=your-key
  python scripts/find_demo_wallets.py

Strategy:
  1. Fetch recent JPYC Transfer events
  2. Count unique wallets by tx frequency
  3. For top candidates, check total ERC-20 diversity
  4. Output ranked list of demo-ready wallets
"""

import json
import os
import sys
import time
import urllib.request

JPYC_CONTRACT = "0xE7C3D8C9a439feDe00D2600032D5dB0Be71C3c29"
POLYGONSCAN_BASE = "https://api.polygonscan.com/api"


def fetch(params: dict) -> dict:
    api_key = os.environ.get("POLYGONSCAN_API_KEY")
    if not api_key:
        print("[ERROR] POLYGONSCAN_API_KEY not set")
        sys.exit(1)
    params["apikey"] = api_key
    query = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{POLYGONSCAN_BASE}?{query}"
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode())


def get_jpyc_transfers(page: int = 1, offset: int = 1000) -> list:
    """Get recent JPYC transfers."""
    data = fetch({
        "module": "account",
        "action": "tokentx",
        "contractaddress": JPYC_CONTRACT,
        "page": str(page),
        "offset": str(offset),
        "sort": "desc",
    })
    if data["status"] != "1":
        print(f"[WARN] API returned: {data.get('message', 'unknown error')}")
        return []
    return data["result"]


def count_wallets(transfers: list) -> dict:
    """Count tx frequency per wallet."""
    counts = {}
    for tx in transfers:
        for addr in [tx["from"], tx["to"]]:
            addr = addr.lower()
            if addr not in counts:
                counts[addr] = {"tx_count": 0, "tokens": set()}
            counts[addr]["tx_count"] += 1
            counts[addr]["tokens"].add(tx["tokenSymbol"])
    return counts


def check_erc20_diversity(address: str) -> dict:
    """Check how many different ERC-20 tokens a wallet has interacted with."""
    time.sleep(0.25)  # Rate limit: 5 calls/sec
    data = fetch({
        "module": "account",
        "action": "tokentx",
        "address": address,
        "page": "1",
        "offset": "200",
        "sort": "desc",
    })
    if data["status"] != "1":
        return {"total_tx": 0, "unique_tokens": 0, "tokens": []}

    transfers = data["result"]
    tokens = set()
    for tx in transfers:
        tokens.add(tx["tokenSymbol"])

    return {
        "total_tx": len(transfers),
        "unique_tokens": len(tokens),
        "tokens": sorted(tokens),
    }


def main():
    print("[1/3] Fetching recent JPYC transfers...")
    transfers = get_jpyc_transfers()
    if not transfers:
        print("[ERROR] No transfers found")
        sys.exit(1)
    print(f"  Found {len(transfers)} transfers")

    print("[2/3] Counting wallet activity...")
    wallets = count_wallets(transfers)

    # Filter: at least 5 JPYC txs
    candidates = {
        addr: info for addr, info in wallets.items()
        if info["tx_count"] >= 5
    }
    # Sort by tx count
    ranked = sorted(candidates.items(), key=lambda x: x[1]["tx_count"], reverse=True)

    print(f"  {len(ranked)} candidates with 5+ JPYC txs")

    print("[3/3] Checking top 10 for ERC-20 diversity...")
    results = []
    for addr, info in ranked[:10]:
        diversity = check_erc20_diversity(addr)
        results.append({
            "address": addr,
            "jpyc_tx_count": info["tx_count"],
            "total_erc20_tx": diversity["total_tx"],
            "unique_tokens": diversity["unique_tokens"],
            "tokens": diversity["tokens"],
        })
        print(f"  {addr[:10]}... JPYC:{info['tx_count']} Total:{diversity['total_tx']} Tokens:{diversity['unique_tokens']}")

    # Sort by unique_tokens * total_tx (prefer diverse + active)
    results.sort(key=lambda x: x["unique_tokens"] * x["total_erc20_tx"], reverse=True)

    print("\n=== Demo Wallet Candidates (ranked) ===\n")
    for i, r in enumerate(results[:5], 1):
        print(f"#{i} {r['address']}")
        print(f"   JPYC txs: {r['jpyc_tx_count']}")
        print(f"   Total ERC-20 txs: {r['total_erc20_tx']}")
        print(f"   Unique tokens: {r['unique_tokens']}")
        print(f"   Tokens: {', '.join(r['tokens'][:10])}")
        print()

    # Save results
    out_path = os.path.join(os.path.dirname(__file__), "..", "demo_data", "wallet_candidates.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"[SAVED] {out_path}")


if __name__ == "__main__":
    main()
