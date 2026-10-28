# Proposal

## Hypothesis

Trailing realized volatility together with Deribit's implied-volatility index (DVOL) forecasts the upper tail of bitcoin's next-week return better than DVOL alone, so a holder who sets weekly covered-call strikes from that forecast earns more BTC per week than one who sets them from DVOL.

The quantity I will forecast is the 90th percentile of the 7-day log return of BTC/USD, in percent, from one Friday 08:00 UTC option expiry to the next.

## Data

DVOL comes from Deribit's public API (`get_volatility_index_data`), one row per day from 2021 to the present. BTC/USD hourly prices come from a public exchange API (Coinbase or Kraken). The unit of observation is one weekly expiry window, roughly 290 windows. The sources collect both series themselves. DVOL is a model-based index of 30-day implied volatility built from Deribit option quotes. Prices are exchange trades. The split is by date, with the last year held out, which is about 50 windows from one market regime.

What I measure differs from what the decision needs in three ways. DVOL is a 30-day measure, but the options are 7-day. I could not confirm that free historical option prices exist, so I price each call with Black-Scholes using DVOL as the volatility. That ignores skew and bid-ask spread, and it is the assumption I trust least. Consecutive windows share information, so the effective sample is smaller than 290.

I have not confirmed whether either source's terms allow republishing. Until I do, the files stay off GitHub and `data/README.md` gives the command that downloads them.

## Decision affected by the model

The actor is a long-term holder of bitcoin (me, with a small position) who sells one weekly covered call each Friday. Deribit options settle in BTC, so the holder keeps the coin. Each week the payoff is the premium, minus (S_T − K) / S_T in BTC when the price finishes above the strike K. The forecast sets K: sell at the strike where the forecast chance of finishing above it equals the fractile the premium and payout imply, as in the lab's booking rule. The score is BTC gained or lost per week against holding without selling.

A strike set too low costs more. A rally can pay out many weeks of premium at once. A strike set too high only gives up some premium. I test calls only. Cash-secured puts, which accumulate coins, are outside this project.
