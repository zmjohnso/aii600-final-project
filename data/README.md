# Data

The data files are not committed and there is no `data` release. I have not confirmed that the Deribit or Coinbase terms allow republishing the files, so each file is downloaded from its source. The script needs no account and no key. Run it from the project root with the interpreter in `.python-version` and `requirements.txt` installed:

```bash
python scripts/fetch_covered_call.py --end 2026-11-11
```

`--end` is exclusive and in UTC, so the script stops at the last complete day, 10 November 2026. The notebook checks every file it reads against the SHA-256 below before fitting. A hash that does not match means the source changed or revised its history since the download.

## Covered call (`analysis.ipynb`)

Unit of observation: one weekly option window, Friday 08:00 UTC to the next Friday 08:00 UTC, built from the two files below.

| File | Source | Rows | Span | SHA-256 |
|---|---|---|---|---|
| `dvol_daily.csv` | Deribit public API `get_volatility_index_data`, BTC, 1D. Columns: date, open, high, low, close of the DVOL index. | 2058 | 2021-03-24 to 2026-11-10 | `693f7ea9185a1a4b44f26030d4a1419d6ecfe42d6b1f97731ba83bee2c0a764f` |
| `btcusd_hourly.csv` | Coinbase Exchange public API, BTC-USD candles, 3600 s. Columns: time_utc, open, high, low, close, volume. An hour with no trades has no row. | 49931 | 2021-03-01 00:00 to 2026-11-10 23:00 | `b7e78f557013813210bddd4060d7ee7050bf141ad5078a1da1cab0dd67b64380` |
