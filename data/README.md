# Data provenance

Run from the repository root with the pinned Python environment.

```bash
python scripts/fetch_covered_call.py
```

The script downloads and verifies the pinned [Coin Metrics Community BTC archive](https://github.com/coinmetrics/data/blob/f1a36afb962731c387bb03982758ab0103063da5/csv/btc.csv) at commit `f1a36afb962731c387bb03982758ab0103063da5`. The notebook checks the same SHA-256 before analysis. The raw CSV is kept outside git.

**Attribution.** Coin Metrics, Inc., *Free Coin Metrics data archives*, BTC daily CSV, [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Charts and numerical results in this version are noncommercial coursework derived from that archive. This project aggregates and transforms the daily source observations.

| Field | Use |
| --- | --- |
| `PriceUSD` | BTC/USD end-of-day spot reference. A row labeled Thursday is observed as of Friday 00:00 UTC. |
| `FeeTotNtv` | Total on-chain transaction fees in BTC. |
| `TxCnt` | Transaction count, the denominator for mean fee per transaction. |

The study uses 292 non-overlapping Friday-to-Friday weeks, with the final 52 held out. It shifts daily price labels by one day and uses one extra day of lag for the seven-day fee feature. Both the modeled entry reference and the settlement proxy use midnight UTC. The published data license applies to source data and its derived material. The pricing curves are simulated.

See the [archive license](https://github.com/coinmetrics/data/blob/master/LICENSE) and [PriceUSD field documentation](https://github.com/coinmetrics/docs-website/blob/master/asset-metrics/market/priceusd.md).
