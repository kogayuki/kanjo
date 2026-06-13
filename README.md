# Kanjo (勘定)

**Talk to any wallet.** AI analyzes on-chain ERC-20 activity and explains it in plain language.

---

## What it does

Enter a wallet address and ask questions in natural language. Kanjo fetches ERC-20 transfer history from the blockchain, classifies counterparty addresses, and generates an analysis powered by Gemini.

## Tech Stack

- **Frontend**: Next.js App Router, Tailwind CSS
- **AI**: Gemini 3.5 Flash (Managed Agents)
- **On-chain Data**: PolygonScan API
- **Database**: Firestore (address labels, cache)
- **Hosting**: Vercel

## Development

```bash
npm install
npm run dev
```

## License

MIT
