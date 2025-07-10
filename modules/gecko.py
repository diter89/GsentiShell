import requests
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel
from rich import box

class CoinGeckoClient:
    def __init__(self):
        self.console = Console()
        self.api_base = "https://api.coingecko.com/api/v3"
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def search_tokens(self, query):
        """Mencari token berdasarkan nama, symbol, atau ID."""
        try:
            res = requests.get(f"{self.api_base}/search?query={query}", headers=self.headers, timeout=10)
            res.raise_for_status()
            found = []
            q = query.lower()
            for r in res.json().get("coins", []):
                if q in r["id"].lower() or q in r["symbol"].lower() or q in r["name"].lower():
                    found.append(r["id"])
            return found
        except Exception as e:
            self.console.print(f"[red]❌ Gagal mencari token: {e}[/red]")
            return []

    def fetch_details(self, ids, page=1, per_page=10):
        """Mengambil detail token dari CoinGecko API."""
        try:
            res = requests.get(
                f"{self.api_base}/coins/markets",
                headers=self.headers,
                params={
                    "vs_currency": "usd",
                    "ids": ",".join(ids),
                    "order": "market_cap_desc",
                    "per_page": per_page,
                    "page": page,
                    "price_change_percentage": "24h"
                },
                timeout=10
            )
            res.raise_for_status()
            return res.json()
        except Exception as e:
            self.console.print(f"[red]❌ Gagal mengambil data CoinGecko: {e}[/red]")
            return []

    def color_percent(self, p):
        """Format persentase perubahan harga dengan warna."""
        try:
            p = float(p)
            return f"[green]+{p:.2f}%[/green]" if p >= 0 else f"[red]{p:.2f}%[/red]"
        except:
            return "-"

    def clean_number(self, n):
        """Format angka besar dengan koma."""
        try:
            return f"{int(float(n)):,}"
        except:
            return "0"

    def format_market_cap(self, cap):
        """Format market cap ke format yang lebih akurat."""
        try:
            cap = float(cap)
            if cap >= 1e9:
                return f"${cap/1e9:,.2f}B"
            elif cap >= 1e6:
                return f"${cap/1e6:,.2f}M"
            else:
                return f"${cap:,.2f}"
        except:
            return "$0.00"

    def display_table(self, data):
        """Menampilkan data token dalam tabel."""
        table = Table(
            title="📊 Crypto Market Cap (Live)",
            show_lines=True,
            expand=True,
            highlight=False,
            box=box.ROUNDED,
            header_style="blue bold",
            border_style="#FFFFFF bold"
        )
        table.add_column("#", justify="right", style="cyan")
        table.add_column("Symbol", style="blue bold dim")
        table.add_column("Name", style="green bold")
        table.add_column("Price", justify="right", style="green bold dim")
        table.add_column("Market Cap", justify="right", style="magenta bold")
        table.add_column("Supply", justify="right", style="yellow bold")
        table.add_column("% 24h", justify="center")

        for i, c in enumerate(data, 1):
            try:
                price = c.get("current_price") or 0.0
                cap = c.get("market_cap") or 0.0
                supply = c.get("circulating_supply") or 0.0
                name = c.get("name") or "Unknown"
                symbol = (c.get("symbol") or "???").upper()

                table.add_row(
                    str(i),
                    symbol,
                    name,
                    f"${price:,.6f}" if price < 1 else f"${price:,.2f}",
                    self.format_market_cap(cap),
                    self.clean_number(supply),
                    self.color_percent(c.get("price_change_percentage_24h", 0)),
                )
            except Exception as e:
                self.console.print(f"[yellow]⚠️ Gagal parsing data token ke-{i}: {e}[/yellow]")

        self.console.print(table)
        return data  # Kembalikan data untuk analisis AI

    def display_progress(self, data):
        """Menampilkan progress bar untuk market cap."""
        self.console.print(Panel("📉 Market Cap Bar + Harga per Coin", expand=False))
        max_cap = max((c.get("market_cap") or 0) for c in data) or 1

        with Progress(
            TextColumn("[bold blue]{task.fields[symbol]:<8}"),
            BarColumn(bar_width=None),
            TextColumn("{task.fields[value]}")
        ) as prog:
            for c in data:
                try:
                    cap = c.get("market_cap") or 0
                    price = c.get("current_price") or 0.0
                    value = f"{cap/1e9:,.2f}B @ ${price:,.6f}" if price < 1 else f"{cap/1e9:,.2f}B @ ${price:,.2f}"
                    prog.add_task(
                        "", total=max_cap, completed=cap,
                        symbol=(c.get("symbol") or "???").upper(),
                        value=value
                    )
                except:
                    continue
        return data  # Kembalikan data untuk analisis AI
