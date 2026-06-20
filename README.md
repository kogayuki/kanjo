# Kanjo (勘定)

**Talk to any wallet.** AI analyzes on-chain ERC-20 activity and explains it in plain language.

Built at [Gemini AI Hackathon @Google Japan](https://luma.com/geminitokyo) (June 27, 2026)

---

## Problem

Blockchain explorers show raw transaction data — hex addresses, token IDs, and gas fees. For non-technical users, it's unreadable. **There's no easy way to understand "what happened in this wallet."**

## Solution

Enter any wallet address. Kanjo fetches ERC-20 transfer history from the blockchain, classifies counterparty addresses (DEX, DeFi, CEX, personal transfers), and generates a natural language analysis powered by Gemini.

### Demo

> **Input**: `0x6736...` (Polygon wallet)
>
> **Output**: "This wallet actively trades JPYC and USDC on DEXs. 65% of transactions are swaps on QuickSwap, with a spike in March. The pattern suggests an active DeFi trader."

## Architecture

```
User (Browser)
    | wallet address
    v
Next.js (Vercel) / AI Studio (Cloud Run)
    |
    +-- Etherscan API V2 --> ERC-20 Transfer events (Polygon)
    |
    +-- Firestore --> Known address labels (32 protocols)
    |
    +-- Gemini 3.5 Flash --> Natural language analysis + chart data
    |
    v
Report: summary + category breakdown + monthly trend
```

### Google Cloud Integration

| Component | Service |
|-----------|---------|
| LLM | Gemini 3.5 Flash |
| Agent Runtime | Managed Agents (Gemini API) |
| Database | Firestore |
| Hosting | Cloud Run (hackathon) / Vercel (production) |

## Tech Stack

- **AI**: Gemini 3.5 Flash, Managed Agents
- **Frontend**: Next.js App Router, Tailwind CSS, Chart.js
- **On-chain Data**: Etherscan API V2 (Polygon, chainid=137)
- **Database**: Firestore (address labels, token metadata, cache)
- **Hosting**: Vercel (production) / Cloud Run (hackathon demo)

## Project Structure

```
kanjo/
├── src/app/            # Next.js App Router pages
├── firestore/          # Seed data
│   ├── address_labels.json   # 32 known protocol addresses
│   └── token_metadata.json   # 12 major tokens
├── prompts/            # Managed Agent system prompt
├── scripts/            # Firestore seeding, demo wallet finder
└── demo_data/          # Pre-fetched transfer data (fallback)
```

## Development

```bash
npm install
npm run dev
```

### Environment Variables

```bash
# .env.local
POLYGONSCAN_API_KEY=your-etherscan-api-key
GEMINI_API_KEY=your-gemini-api-key
```

## Roadmap

- [x] Hackathon MVP: address input -> static report
- [ ] Chat UI: talk to any wallet in natural language
- [ ] Multi-chain: Ethereum, Arbitrum, Injective
- [ ] Share: post analysis to X
- [ ] Wallet bookmarks

## Author

[@yuki_k_02](https://x.com/yuki_k_02)

## License

MIT
