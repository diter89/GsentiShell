import os
import requests
import json
import time

API_KEY = os.getenv("FIREWORKS_API_KEY", "")

def analyze_with_dobby(text, lang="id", roleplay="default", retry=3):
    roleplay_instruction = {
        "default": "Berikan respons yang profesional dan informatif.",
        "wizard": "Berikan respons dengan gaya penyihir blockchain yang mistis dan penuh metafora magis.",
        "trader": "Berikan respons dengan gaya trader crypto yang sarkastik, agresif, dan penuh jargon pasar."
    }[roleplay] if lang == "id" else {
        "default": "Provide a professional and informative response.",
        "wizard": "Provide a response in the style of a mystical blockchain wizard, full of magical metaphors.",
        "trader": "Provide a response in the style of a sarcastic, aggressive crypto trader, full of market jargon."
    }
    lang_instruction = (
        "Hasilkan output dalam bahasa Indonesia jika lang='id', atau dalam bahasa Inggris jika lang='en'. "
        "Pastikan bahasa konsisten di seluruh output."
    ) if lang == "id" else (
        "Generate output in English if lang='en', or in Indonesian if lang='id'. "
        "Ensure the language is consistent throughout the output."
    )
    prompt = (
        f"{lang_instruction}\n{roleplay_instruction}\n\n"
        "Analisis data harga crypto dari CoinGecko dan berita dari web. Fokus pada proyek utama sesuai query. "
        "Berikan output yang terstruktur: \n"
        "1. **Harga dan Data Token**: Untuk setiap token dari CoinGecko, sebutkan nama, simbol, harga, market cap, volume 24 jam, dan perubahan harga 24 jam. "
        "Gunakan markup [bold], [green], [red], [yellow], [blue] untuk menonjolkan informasi penting. \n"
        "2. **Berita dan Hype**: Rangkum berita terkini dan hype pasar yang relevan dengan proyek crypto utama, seperti pembaruan teknologi (misalnya, proof-of-stake, EIP, L2), adopsi institusional, atau sentimen pasar. Hindari informasi umum; fokus pada perkembangan spesifik. Jika tidak ada berita relevan, katakan 'Tidak ada berita spesifik ditemukan'. \n"
        "3. **Teknologi di Balik Token**: Jelaskan teknologi inti proyek utama (misalnya, blockchain, smart contract, konsensus, atau upgrade terbaru) secara singkat dan spesifik. \n"
        "Gunakan bullet points untuk setiap poin penting, tetap ringkas, dan hindari penjelasan bertele-tele."
        "\n\n" + text
    ) if lang == "id" else (
        f"{lang_instruction}\n{roleplay_instruction}\n\n"
        "Analyze crypto price data from CoinGecko and news from the web. Focus on the main project as per the query. "
        "Provide a structured output: \n"
        "1. **Price and Token Data**: For each token from CoinGecko, list the name, symbol, price, market cap, 24h volume, and 24h price change. "
        "Use markup [bold], [green], [red], [yellow], [blue] to highlight key information. \n"
        "2. **News and Hype**: Summarize recent news and market hype relevant to the main crypto project, such as technology updates (e.g., proof-of-stake, EIP, L2), institutional adoption, or market sentiment. Avoid general information; focus on specific developments. If no relevant news is found, state 'No specific news found'. \n"
        "3. **Technology Behind the Token**: Briefly and specifically explain the core technology of the main project (e.g., blockchain, smart contract, consensus, or recent upgrades). \n"
        "Use bullet points for each key point, keep it concise, and avoid verbose explanations."
        "\n\n" + text
    )
    payload = {
        "model": "accounts/sentientfoundation/models/dobby-unhinged-llama-3-3-70b-new",
        "max_tokens": 2048,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [{"role": "user", "content": prompt}]
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    for attempt in range(retry):
        try:
            res = requests.post("https://api.fireworks.ai/inference/v1/chat/completions",
                                headers=headers, data=json.dumps(payload), timeout=15)
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            error_msg = f"Attempt {attempt + 1}/{retry} failed: {str(e)}"
            if attempt == retry - 1:
                # Fallback response
                fallback_msg = (
                    "🧙‍♂️ *Dobby si Penyihir Blockchain kehilangan mantra API-nya!* Maaf, wahai pengembara, server Fireworks sedang rewel. "
                    "Berikut ringkasan singkat berdasarkan data yang ada:\n\n"
                    "1. **Harga dan Data Token**: Lihat tabel di atas untuk detail harga dari CoinGecko.\n"
                    "2. **Berita dan Hype**: Tidak ada analisis spesifik karena API bermasalah. Cek web untuk berita terbaru.\n"
                    "3. **Teknologi di Balik Token**: Sahara AI menggunakan blockchain untuk kedaulatan data dan smart contract untuk distribusi reward.\n\n"
                    "Coba lagi nanti atau periksa API Key!"
                ) if lang == "id" and roleplay == "wizard" else (
                    "Yo, bro, API’s acting like a bear market! Dobby the Trader can’t get through. "
                    "Here’s a quick rundown based on what we got:\n\n"
                    "1. **Price and Token Data**: Check the table above for CoinGecko stats.\n"
                    "2. **News and Hype**: No deep analysis, API’s down. Hit the web for news.\n"
                    "3. **Technology Behind the Token**: Sahara AI’s got blockchain for data sovereignty and smart contracts for rewards.\n\n"
                    "Try again later or check your API Key!"
                ) if lang == "en" and roleplay == "trader" else (
                    "Maaf, API Fireworks bermasalah. Berikut ringkasan dasar:\n\n"
                    "1. **Harga dan Data Token**: Lihat tabel di atas untuk detail harga dari CoinGecko.\n"
                    "2. **Berita dan Hype**: Tidak ada analisis spesifik karena API bermasalah. Cek web untuk berita terbaru.\n"
                    "3. **Teknologi di Balik Token**: Sahara AI menggunakan blockchain untuk kedaulatan data dan smart contract untuk distribusi reward.\n\n"
                    "Coba lagi nanti atau periksa API Key!"
                ) if lang == "id" else (
                    "Sorry, the Fireworks API is down. Here’s a basic summary:\n\n"
                    "1. **Price and Token Data**: Check the table above for CoinGecko stats.\n"
                    "2. **News and Hype**: No detailed analysis due to API issues. Check the web for news.\n"
                    "3. **Technology Behind the Token**: Sahara AI uses blockchain for data sovereignty and smart contracts for reward distribution.\n\n"
                    "Try again later or check your API Key!"
                )
                print(f"[red]❌ {error_msg}[/red]")
                return fallback_msg
            time.sleep(2)  # Delay 2 detik sebelum retry
