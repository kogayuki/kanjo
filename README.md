# Kanjo (勘定)

**JPYC決済の経費精算を、AIが30秒で。**

Built at [Gemini AI Hackathon @Google Japan](https://luma.com/geminitokyo) (June 27, 2026)

---

## Problem

Companies using JPYC (Japanese Yen stablecoin, 1 JPYC = 1 JPY) for payments have no tool to manage expenses. They manually copy transactions from blockchain explorers into spreadsheets and categorize them by hand. **There is no expense tracker for stablecoin payments.**

## Solution

Enter a wallet address. Kanjo fetches JPYC transfer history from Polygon, identifies counterparties (DEX, DeFi, businesses, individuals), and automatically classifies each transaction into Japanese accounting categories (勘定科目) — powered by Gemini.

### Demo

> **Input**: `0x6736...` (Polygon wallet with JPYC activity)
>
> **Output**:
> | 日付 | 金額 | 取引先 | 勘定科目 |
> |------|------|--------|---------|
> | 6/15 | ¥30,000 | QuickSwap | 仕入高 |
> | 6/14 | ¥5,000 | 個人送金 | 外注費 |
> | 6/10 | ¥100,000 | Aave V3 | 投資運用 |

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

- [x] Hackathon MVP: JPYC expense classification
- [ ] CSV/PDF export for accountants
- [ ] Multi-stablecoin: USDC, USDT, DAI
- [ ] Accounting software integration (freee, MoneyForward)
- [ ] Multi-chain: Ethereum, Arbitrum
- [ ] Chat UI: ask questions about your expenses

## Author

[@yuki_k_02](https://x.com/yuki_k_02)

## License

MIT
