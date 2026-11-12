"""Download the covered-call data into data/.

Usage: python scripts/fetch_covered_call.py --end 2026-11-12

Writes data/dvol_daily.csv (Deribit DVOL, daily OHLC) and
data/btcusd_hourly.csv (Coinbase BTC-USD hourly candles), both from
2021-03-01 up to but not including --end (UTC). Prints a SHA-256 for each file.
"""
import argparse
import hashlib
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import requests

START = datetime(2021, 3, 1, tzinfo=timezone.utc)
DATA = Path(__file__).resolve().parent.parent / "data"


def get(url, params):
    for attempt in range(6):
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            return r.json()
        time.sleep(2 ** attempt)
    r.raise_for_status()


def fetch_dvol(end):
    rows, t = [], START
    while t < end:
        t2 = min(t + timedelta(days=365), end)
        res = get(
            "https://www.deribit.com/api/v2/public/get_volatility_index_data",
            dict(currency="BTC", resolution="1D",
                 start_timestamp=int(t.timestamp() * 1000),
                 end_timestamp=int(t2.timestamp() * 1000) - 1),
        )["result"]["data"]
        rows += res
        t = t2
    df = pd.DataFrame(rows, columns=["ts_ms", "open", "high", "low", "close"])
    df["date"] = pd.to_datetime(df.ts_ms, unit="ms", utc=True).dt.strftime("%Y-%m-%d")
    df = df.drop_duplicates("ts_ms").sort_values("ts_ms")
    return df[["date", "open", "high", "low", "close"]]


def fetch_hourly(end):
    rows, t = [], START
    while t < end:
        t2 = min(t + timedelta(hours=300), end)  # 300 candles per request
        res = get(
            "https://api.exchange.coinbase.com/products/BTC-USD/candles",
            dict(granularity=3600, start=t.isoformat(),
                 end=(t2 - timedelta(seconds=1)).isoformat()),
        )
        rows += res
        t = t2
        time.sleep(0.2)
    df = pd.DataFrame(rows, columns=["ts", "low", "high", "open", "close", "volume"])
    df["time_utc"] = pd.to_datetime(df.ts, unit="s", utc=True).dt.strftime("%Y-%m-%d %H:%M:%S")
    df = df.drop_duplicates("ts").sort_values("ts")
    return df[["time_utc", "open", "high", "low", "close", "volume"]]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--end", required=True, help="YYYY-MM-DD, exclusive, UTC")
    end = datetime.fromisoformat(ap.parse_args().end).replace(tzinfo=timezone.utc)
    DATA.mkdir(exist_ok=True)
    for name, df in [("dvol_daily.csv", fetch_dvol(end)),
                     ("btcusd_hourly.csv", fetch_hourly(end))]:
        path = DATA / name
        df.to_csv(path, index=False)
        print(f"{name}  rows={len(df)}  {df.iloc[0, 0]} to {df.iloc[-1, 0]}  sha256={sha256(path)}")
