# Proposal (backup option: miner economics)

## Hypothesis

Bitcoin hashprice 30 days ahead can be forecast better from hashrate growth, difficulty, transaction fees and the BTC price than from today's hashprice alone, so a small miner can commit to power costs only when revenue is likely to cover them.

The quantity I will forecast is hashprice, in USD per petahash per second per day (USD/PH/s/day), averaged over the 30 days after each forecast date.

## Data

Hashrate, difficulty, block subsidy and transaction fees come from the mempool.space API, which reads them from the blockchain. BTC/USD daily prices come from a public exchange API (Coinbase or Kraken). The unit of observation is one day, from 2016 to the present, roughly 3,500 rows. Overlapping 30-day targets make the effective sample much smaller. Each halving changes revenue per block abruptly, so I treat the halvings as structural breaks and hold out the period after the April 2024 halving, which is a short window.

What I measure differs from what the decision needs. Hashprice is revenue for a hypothetical miner. A real miner's revenue differs through pool fees, block luck and downtime, and its profit depends on machine efficiency and electricity price, which public data does not contain. I treat the breakeven hashprice as a parameter and report results across a range of values.

Chain data is public, but I have not confirmed whether the API and exchange terms allow republishing the files. Until I do, the files stay off GitHub and `data/README.md` gives the command that downloads them.

## Decision affected by the model

The actor is a small miner. Before each month the miner decides whether to extend or sign a fixed-price power contract, or to sell part of next month's output forward. Profit over a month is about (hashprice − breakeven) × hashrate × days, where the breakeven is the electricity cost per PH/s per day. If the forecast puts hashprice above the breakeven, the miner commits. If it puts it below, the miner waits or hedges.

Over-forecasting hashprice costs more. The miner locks in fixed costs, and a drop in the BTC price or a rise in network hashrate leaves it mining at a loss. Under-forecasting only delays a profitable commitment. The score is the profit the rule would have earned, per PH/s per month, against the rule of always committing.
