"""Download the pinned Coin Metrics Community Bitcoin archive."""
import hashlib
from pathlib import Path

import requests


COMMIT = "f1a36afb962731c387bb03982758ab0103063da5"
URL = f"https://raw.githubusercontent.com/coinmetrics/data/{COMMIT}/csv/btc.csv"
SHA256 = "06495ff8e643432e6948b7b4686ce44fc106217287dabdc1b38351d9ddec46c3"
DATA = Path(__file__).resolve().parents[1] / "data" / "coinmetrics_btc.csv"


def main():
    response = requests.get(URL, timeout=60)
    response.raise_for_status()
    if hashlib.sha256(response.content).hexdigest() != SHA256:
        raise ValueError("Coin Metrics archive checksum does not match the pinned snapshot")
    DATA.parent.mkdir(exist_ok=True)
    temporary = DATA.with_suffix(".tmp")
    temporary.write_bytes(response.content)
    temporary.replace(DATA)
    print(f"Saved {DATA}")


if __name__ == "__main__":
    main()
