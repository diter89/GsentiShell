# 🤖 DobbySearch - CryptoGPT CLI Agent

**DobbySearch** is a Python-based intelligent CLI agent designed to search and analyze information related to the **crypto world** — combining live data from CoinGecko, real-time web results, and powerful AI explanations in either English or Indonesian.

---

## ✨ Features

- 🔍 **Web Search Integration:** Fetch up to 10 real-time results using DuckDuckGo.
- 💰 **Crypto Market Data:** Get token prices, market cap, volume, and 24h changes via CoinGecko.
- 🧠 **AI Prompt Analyzer:** Generate concise or detailed AI explanations on crypto topics.
- 🌐 **Multi-language Output:** Available in English (`en`) or Indonesian (`id`).
- 🔐 **Site Lock (Optional):** Filter or lock to specific news sources.
- 🤖 **Fireworks AI Integration:** Uses the `dobby-unhinged-llama-3-70b-new` model via Fireworks API for rich, uncensored responses.

---

## 🚀 How to Use

### 📌 Basic CLI Command

```bash
python3 dobbySearch \
  --prompt "nillion" \
  --web true \
  --gecko true \
  --countsearch 10 \
  --mode detail \
  --lang en
```
⚙️ CLI Options
Argument	Description
--prompt	Topic to search and analyze (required)
--web	Enable web search: true or false
--gecko	Include market data from CoinGecko: true or false
--countsearch	Number of web search results to return (default: 5–10)
--locksitus	Restrict results to specific domains (optional)
--mode	AI response style: ringkas (concise) or detail
--crypto	Enable crypto-specific mode (optional)
--lang	Output language: id (Indonesian) or en (English)

🔐 Setting Up Fireworks API Key
This tool requires a Fireworks AI API key to generate AI responses. The model used is:

sentientfoundation/models/dobby-unhinged-llama-3-70b-new

🔸 How to Configure
1. Export via terminal:
```
export FIREWORKS_API_KEY="your_api_key_here"
```
2. Or create a .env file:
```
FIREWORKS_API_KEY=your_api_key_here
```
# example:
![Screenshot_2025-07-08_00-25-25](https://github.com/user-attachments/assets/43a71f89-3cd9-4f30-b2fc-0d97d5297f45)
