import requests
from bs4 import BeautifulSoup
import time

def duckduckgo_multi_scrape(query, jumlah=10, max_pages=1):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    url = "https://html.duckduckgo.com/html/"
    hasil = []

    for page in range(1, max_pages + 1):
        data = {"q": query, "s": (page - 1) * jumlah}
        try:
            response = requests.post(url, headers=headers, data=data, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("a", class_="result__a", href=True)
            snippets = soup.find_all("a", class_="result__snippet")

            for i in range(min(jumlah, len(results))):
                hasil.append({
                    "judul": results[i].text.strip(),
                    "link": results[i]["href"],
                    "snippet": snippets[i].text.strip() if i < len(snippets) else "No snippet"
                })
            time.sleep(0.5)  # Delay untuk hindari rate limit
        except Exception as e:
            hasil.append({
                "judul": "Gagal scraping",
                "link": "",
                "snippet": f"Error pada halaman {page}: {str(e)}"
            })
        if len(results) < jumlah: 
            break

    return hasil[:jumlah] if hasil else []
