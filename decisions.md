# Decisions

This file is the history of the project. Append an entry when a choice changes the work: the quantity, the data, the split, the model, the loss, or the action. Leave old entries in place. A later entry can reverse an earlier one. If a result depends on a random draw, record the seed under Why. The split entry records the cutoff date, or the seed and the fraction. The pull request that merges the code names this entry.

## YYYY-MM-DD: short title

- Decision. What you chose.
- Why. The evidence.
- Alternative. What you rejected.
- Revisit. What would change the choice.

## 2026-10-27: forecast weekly BTC realized volatility for covered-call sizing

- Decision. Forecast the annualized realized volatility of BTC/USD over the 7 days between Deribit Friday 08:00 UTC expiries, using trailing realized volatility and the DVOL index. The decision it informs is whether a long-term holder sells a weekly covered call, and how far out of the money, to grow the holding in BTC.
- Why. I hold bitcoin and the decision is one I would make myself each week. Weekly expiries give a clear target and a clear action. DVOL is available from Deribit's public API, which I checked by pulling daily rows. The forecast is only useful if it beats DVOL alone, so that is the baseline to beat. No seed yet; one will be recorded when a model with a random draw is chosen.
- Alternative. Forecasting 30-day bitcoin hashprice (USD/PH/s/day) for a miner deciding on a fixed-price power or hosting contract, drafted in `PROPOSAL-backup-miner.md`. Also considered and set aside: bitcoin fee-rate forecasting, prediction-market calibration on Fed and election outcomes, and Fed or CPI surprise forecasting.
- Revisit. Switch to the miner proposal if DVOL history turns out too short for a train and test split, if Deribit's terms rule out the data even for private use, or if the preliminary results show no forecast that beats DVOL alone.

## 2026-10-27: forecast the upper tail of the 7-day BTC return, not its volatility

- Decision. Change the forecast target to the 90th percentile of the 7-day log return of BTC/USD between Deribit Friday 08:00 UTC expiries, from trailing realized volatility and DVOL. The strike of a weekly covered call comes from that forecast. The loss is the BTC-settled payoff, premium minus (S_T - K) / S_T, scored in BTC per week against holding. Hold out the last year of windows. This replaces the target in the entry above.
- Why. Volatility is a proxy for what the strike depends on, which is the upper tail of the week's move. A tail quantile ties the forecast to the action the way the lab's critical fractile does. I could not confirm that free historical option prices exist, so premiums are Black-Scholes prices that use DVOL as the volatility. That is the assumption I trust least. The held-out year is about 50 weekly windows from one market regime, and the proposal says so. No seed yet.
- Alternative. Keep forecasting volatility, which is easier to score but not tied to the strike. Also rejected: puts, which accumulate coins but are outside this project.
- Revisit. If Black-Scholes premiums look far from real quotes, if the held-out year is too thin to separate the forecast from DVOL, or if Deribit's terms rule out the data.

## 2026-10-27: backup option is the miner proposal

- Decision. Keep `PROPOSAL-backup-miner.md` as the fallback. It forecasts 30-day hashprice in USD/PH/s/day. The actor is a small miner deciding on a fixed-price power contract or a forward sale. The loss is (hashprice - breakeven) x hashrate x days, with the breakeven treated as a parameter and results reported across a range.
- Why. The target is public and fully obtainable, and the loss is a formula. A real miner's costs are not in public data, so a range of breakevens stands in for them.
- Alternative. The covered-call proposal in `PROPOSAL.md`, which stays primary for now.
- Revisit. Switch to the miner proposal if the option premiums cannot be defended, or if the preliminary results show no forecast that beats DVOL alone. Drop it if the post-halving window is too short to test.
