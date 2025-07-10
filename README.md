# 🤖 DobbySearch - CryptoGPT CLI Agent

**DobbySearch** adalah agen CLI berbasis Python yang cerdas, dirancang untuk melakukan pencarian informasi seputar dunia **crypto**, baik dari data langsung CoinGecko maupun berita web, serta memberikan penjelasan berbasis AI dalam bahasa Indonesia atau Inggris.

## ✨ Fitur Utama

- 🔍 **Web Search Integration:** Ambil hingga 10 hasil dari web secara real-time menggunakan DuckDuckGo.
- 💰 **Crypto Market Data:** Dapatkan harga token, market cap, volume, dan perubahan harga via CoinGecko.
- 🧠 **AI Prompt Analyzer:** Jelaskan topik crypto secara ringkas atau mendetail dengan AI.
- 🌐 **Multi-language Output:** Output tersedia dalam Bahasa Indonesia (`id`) dan Inggris (`en`).
- 🔐 **Lock Situs (Optional):** Filter situs sumber berita sesuai preferensi.

---

## 🚀 Cara Penggunaan

### 📌 Mode Terminal CLI

```bash
python3 dobbySearch --prompt "nillion" --web true --gecko true --countsearch 10 --mode detail --lang en
