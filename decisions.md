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

## 2026-11-11: covered-call data comes from the sources by script, with no `data` release

- Decision. Download DVOL (Deribit public API), BTC-USD hourly candles (Coinbase Exchange public API) and, for the backup, mining data (mempool.space) with `scripts/fetch_covered_call.py` and `scripts/fetch_miner.py`, using `--end 2026-11-11` (exclusive, UTC). `data/README.md` lists the commands and SHA-256 of each file, and `analysis.ipynb` checks them before reading. No `data` release. Prices are the open of each hourly candle, and the 13 hours with no trades are forward-filled.
- Why. I have not confirmed that any of the three terms of use allow republishing, and the README says to skip the release in that case. A fixed `--end` makes the download repeatable. A second download of the mining file gave the same hash.
- Alternative. A public `data` release, rejected until the terms are read. Kraken for prices, rejected because its OHLC endpoint returns only the latest 720 candles.
- Revisit. If a source revises its history so the hashes stop matching, or if the terms turn out to allow a release.

## 2026-11-11: split the covered-call data by date, last 52 weekly windows held out

- Decision. Cutoff 2025-11-07 08:00 UTC. The 240 training windows run from 2021-04-02 to 2025-10-31 (the last one ends on the cutoff), and the 52 held-out windows from 2025-11-07 to 2026-10-30 (the last ends 2026-11-06). Nothing is fit, scaled, or chosen on held-out rows. The notebook asserts that no training window ends after the cutoff. Inputs are known at each Friday 08:00: the previous UTC day's DVOL close and realized volatility from hourly returns up to that time.
- Why. The decision is about a later week, so the held-out set is a later year. The proposal said the last year, which is 52 windows.
- Alternative. A random split by week, rejected because it would let the model see the market regime around each held-out week. A rolling-origin split, kept only for choosing the realized-volatility window inside the training windows.
- Revisit. If the held-out year is too thin to separate the model from the baseline (it was, see the model entry), the final could add a second held-out period or report a rolling-origin score over more years.

## 2026-11-11: model is a 90th-percentile linear quantile regression on DVOL and 30-day realized volatility

- Decision. $q_{0.9}(r) = a + b\,d + c\,x$, where $r$ is the 7-day log return, $d$ is DVOL scaled to one week and $x$ is realized volatility scaled the same way, fit by minimizing pinball loss at tau = 0.9 with `scipy.optimize.linprog`. The 30-day window for $x$ was chosen over the 7-day window on training windows only (pinball loss 0.01127 against 0.01166 over the last 52 training weeks). Fitted $a = 0.103$, $b = 0.532$, $c = -0.816$. Uncertainty is a pairs bootstrap of 500 draws with seed 600. The baseline is the normal 90th percentile $1.2816 \cdot d$, which is DVOL alone with zero drift.
- Why. A 90th-percentile forecast is what sets the strike, and pinball loss is the loss of a quantile. With 240 training windows a three-parameter linear model is as much as the data can fit.
- Alternative. A volatility forecast fed into a normal quantile, rejected earlier in this file because volatility is only a proxy for the tail. Both volatility windows in one model, rejected as too many parameters for 240 windows.
- Revisit. On the last 52 training weeks the baseline already had the lower pinball loss (0.01044), and on the held-out year the model is not distinguishable from it (+0.00059 BTC per week, SE 0.00072). The fitted slopes are not different from zero, so the model sets nearly a constant strike. If that holds at the final, try shrinking the model toward the baseline, or fit a model of the volatility ratio, and decide on training windows only.

## 2026-11-11: loss is net BTC per week against holding, with a Black-Scholes premium at DVOL

- Decision. For a call struck at $K = S_0 e^{\hat q}$, the gain per week against not selling is $C(S_0, K, \sigma, 7/365)/S_0 - \max(S_T - K, 0)/S_T$, with $C$ the Black-Scholes call at zero rate and $\sigma$ the previous day's DVOL close. Held-out scores: baseline +0.00026 BTC per week (SE 0.00241), model +0.00085 (SE 0.00182), paired difference +0.00059 (SE 0.00072). Both strikes were exceeded too rarely on the held-out year (2 and 1 of 52, against 5 expected).
- Why. Deribit options settle in BTC, so the payout and the premium are both in BTC. The proposal says the Black-Scholes premium is the assumption trusted least, because DVOL measures 30 days and the options are 7-day, and skew and the bid-ask spread are ignored. The same premium formula is used for both strikes, so the comparison is between strikes.
- Alternative. Real option quotes, rejected because I could not find free historical ones. The strike rule from the critical fractile (the forecast chance of finishing above $K$ equals the chance the premium implies), which is for the final.
- Revisit. If Black-Scholes premiums look far from real quotes, or if a spot check against current Deribit quotes shows a large gap, either of which would change the size of the scores but not necessarily their ranking.

## 2026-11-11: miner data uses Coinbase daily closes for price, and the 7-day mean for the current hashprice

- Decision. Hashprice is $144 \times$ (subsidy plus fees per block, in BTC) $\times$ BTC/USD $/$ hashrate in PH/s, in USD/PH/s/day. The block reward, fees and hashrate come from mempool.space and the price from Coinbase's daily close, both fetched by `scripts/fetch_miner.py` with `--end 2026-11-11`. Daily rows run 2016-01-01 to 2026-11-10 (3967). The current hashprice used as the baseline is the mean of the last 7 days. Difficulty is not a separate input.
- Why. mempool.space's own `usd` column only changes weekly before 2023 (86 percent of days repeat the previous day), which would turn the early hashprice into a step function. Its daily hashrate estimate is noisy (median daily log change of hashprice 0.08), so the 7-day mean is a steadier starting point. Difficulty is computed from hashrate and moves with it. The mining file's hash changed between this morning's first download and a later one, so mempool.space revises recent rows. Two downloads in a row now agree, and `data/README.md` has the new hash.
- Alternative. The mempool.space price column, rejected as above. Today's single-day hashprice as the baseline, rejected as too noisy.
- Revisit. If the hash stops matching, re-download with the same `--end` and see which rows changed.

## 2026-11-11: split the miner data at the April 2024 halving, with a 30-day embargo

- Decision. Cutoff 2024-04-20. Training rows are forecast dates from 2016-02-06 to 2024-03-20 (their 30-day target ends before the cutoff), minus rows whose trailing week or target window contains the 2016 or 2020 halving: 2892 rows. Held-out rows are forecast dates from 2024-04-27 (a week after the halving) to 2026-10-11 (the last date with a complete 30-day target): 898 rows, scored on 30 non-overlapping monthly decisions. The notebook asserts that no training target reaches the cutoff. Standardizing means and standard deviations come from the training rows only.
- Why. A halving cuts revenue per block in half in one day, which the inputs cannot see, so the three halvings are structural breaks. The decision is about a later month, so a later period is held out. Overlapping 30-day targets make the effective sample far smaller than the row count.
- Alternative. Holding out only the last year, rejected because it would leave about 12 monthly decisions. Random rows, rejected because neighboring days share their target.
- Revisit. If 30 months from one post-halving regime is too thin to separate a model from the baseline (it was, see the model entry).

## 2026-11-11: miner model is a linear regression of the log hashprice ratio on hashrate growth, fee share and BTC return

- Decision. $y = \log(m_{30}/\text{hp7}) = a + b_1\,\text{g\_hr} + b_2\,\text{fee} + b_3\,\text{ret}$, least squares on standardized inputs, where $m_{30}$ is the mean hashprice over the next 30 days, `g_hr` is the 30-day log growth of the 7-day mean hashrate, `fee` is the fee share of revenue over 7 days, and `ret` is the 30-day log BTC return. Fitted on the training rows: $a = -0.006$, $b_1 = 0.005$, $b_2 = -0.030$, $b_3 = 0.033$. Only $b_3$ has a 90 percent moving-block bootstrap interval (30-day blocks, 500 draws, seed 600) that excludes zero. The baseline is $\hat y = 0$.
- Why. A ratio keeps rows comparable across a hashprice that fell from about \$1,300 to about \$45 over the sample. A linear model with three inputs is as much as about 100 effective independent months can support.
- Alternative. Forecasting the level of hashprice, rejected for the scale reason above. Adding a mean-reversion term, held for the final.
- Revisit. On the held-out period the model's log-forecast RMSE is 0.0936 against 0.0963 for the baseline, and the two rules commit in the same months except for at most one of 30. If the final needs a model that changes decisions, the inputs would have to carry more than the 7-day mean does, for example a forward hashrate signal.

## 2026-11-11: miner loss is profit per PH/s per month for a commit rule, across a grid of breakevens

- Decision. The miner commits when the forecast mean hashprice is above the breakeven $b$ and then earns $(\text{realized} - b) \times 30$ per PH/s for the month, otherwise 0. The score is the mean over 30 non-overlapping held-out months, next to always committing. $b$ runs from \$30 to \$60 per PH/s/day in steps of \$5. At \$45: always commit +\$19, baseline rule +\$120, model rule +\$120 (the same months).
- Why. The proposal treats the breakeven as a parameter, since a real miner's cost is not in public data. The grid covers the 10th to 90th percentile of held-out hashprice (\$32 to \$59). The range was set by looking at held-out hashprice levels, not by fitting anything on them. A grid anchored on the last training year (\$60 to \$104) sits above every held-out value, so every rule would never commit. Over-forecasting is the costlier error because it commits the miner to a cost it may not cover.
- Alternative. A grid from the training percentiles, rejected as above. A single breakeven, rejected because the answer depends on it.
- Revisit. If a real miner's cost can be sourced, use that value as the headline and keep the grid as the sensitivity check.

## 2026-11-11: the strike comes from the critical fractile and the fraction written from Kelly, after the instructor's feedback

- Decision. Issue 2 on the repository says the covered call, the held-out year and the score in BTC can stay, and that the fixed 90th percentile and the fixed size of one call cannot. The strike is now the $q$ in $K = S_0 e^{q}$ that maximizes the expected gain $g(q, R) = p(q) - (1 - e^{q - R})^+$ over the predictive distribution of the 7-day log return $R$, searched on a grid from at the money to 30 percent above in steps of 0.005. At the optimum the forecast chance of finishing above the strike, weighted by $S_0/S_T$, equals the chance $N(d_2)$ that the premium implies. After the strike, the fraction $f$ of the stack written is the one in $[0, 1]$ (steps of 0.01) that maximizes the mean of $\log(1 + f\,g)$ over the predictive draws. Half of that fraction is reported too. The rule is frozen on the training windows and scored on the 52 held-out Fridays by the mean of $\log W$, against holding ($f = 0$) and against a full call every week ($f = 1$), plus a full call at a fixed strike about 10 percent out of the money. The score is labeled as a Black-Scholes calculation at the previous day's DVOL, not a Deribit fill, and the notebook says DVOL is also an input. The DVOL baseline is the same rule applied to a normal return with zero mean and DVOL's volatility, as 2,000 quantiles.
- Why. The instructor's feedback, and it follows from the payoff: a strike set too low costs more, and that cost picks the number. The win-or-lose Kelly formula does not apply because the loss is continuous and occurs only above the strike. The check in the notebook confirms the condition: for the model the weighted exceedance averages 0.223 and $N(d_2)$ averages 0.221. Friday-to-Friday returns do not overlap, so the 52 held-out Fridays are scored one by one. The inputs do overlap, so the standard errors are probably a little small.
- Alternative. The fixed 90th percentile and a full call every week, which this entry replaces. It supersedes the target entry of 2026-10-27 (90th percentile) and the loss entry of 2026-11-11 (net BTC per week for a full call). A baseline with the risk-neutral drift instead of zero was tried first and also put every strike at the money, with a Kelly fraction of 1.0 instead of 0.76.
- Revisit. The DVOL baseline sits at the at-the-money edge of the strike grid in every week, so its result depends on the grid's lower edge. If real option quotes become available, replace the Black-Scholes premium.

## 2026-11-11: the model is a location-scale model with the empirical shape of the training residuals

- Decision. $r = \mu + \sigma_t z$ with $\log\sigma_t = \alpha + \beta\log d_t + \gamma\log x_t$, where $d$ is DVOL and $x$ is realized volatility, both scaled to one week. The parameters are fit by Gaussian quasi-likelihood (`scipy.optimize.minimize`) on the 240 training windows. The predictive distribution for a Friday is $\mu + \sigma_t z_j$ over the 240 standardized training residuals, so its skew and tails come from the data. The realized-volatility window was chosen by the Gaussian log score on the last 52 training weeks: 7 days (-2.2806) over 30 days (-2.2721), and both are worse than the baseline's -2.2919. Fitted: $\mu = 0.0038$, $\alpha = -1.60$, $\beta = 0.63$ (90 percent bootstrap interval 0.20 to 1.18), $\gamma = -0.21$ (-0.58 to 0.17). The bootstrap is a pairs resample of the training windows, 300 draws, seed 600. This replaces the quantile regression entry of 2026-11-11.
- Why. Kelly needs draws from a full predictive distribution, which a single quantile cannot give. A scale model with an empirical shape needs four parameters and no assumption about the tails. The baseline is the case $\alpha = 0$, $\beta = 1$, $\gamma = 0$ with a normal shape.
- Alternative. Quantile regressions at several levels, rejected as harder to turn into one distribution. A Student-t shape, rejected because the empirical residuals are skewed (-0.30) and their 90th percentile (1.21) is below the normal's (1.28).
- Revisit. $\gamma$ is not distinguishable from zero, and its sign (more realized volatility, richer premium) is the opposite of the hypothesis. If the final cannot show that realized volatility adds anything, the honest claim is about the shape and the shrinkage of DVOL ($\beta < 1$), and the hypothesis should be restated. The held-out results: the model's Kelly rule earns 0.0053 log BTC per coin per week (SE 0.0018) against holding, 0.0004 (SE 0.0029) more than the DVOL baseline's, and 0.0052 (SE 0.0026) more per week than a fixed 10 percent strike, with a worst week of -4.0 percent against -12.5 percent for the baseline.

## 2026-11-11: the covered call is the primary project and the miner is the fallback

- Decision. `analysis.ipynb` (covered call) is the project for the 9 December final. `analysis-miner.ipynb` stays on `main` as it is, as the fallback, and gets no more work unless the covered call fails.
- Why. The instructor's feedback in issue 2 says the covered-call proposal can proceed, with the changes made above, and says nothing about the miner. On the held-out data neither model beats its baseline clearly: the covered-call model ties the DVOL baseline on growth with smaller swings, and the miner model changes the baseline's decisions in at most one of 30 months. The covered call has a richer decision (a strike and a fraction), and the feedback already shows how to score it.
- Alternative. The miner proposal, whose rule beats always committing by a wide margin but whose model adds almost nothing to the 7-day mean.
- Revisit. Switch if the covered call cannot be made to meet `CHECKLIST.md` by 9 December, for example if the simulation check cannot recover the parameters.

## 2026-11-11: drop the miner fallback and keep only the covered-call project

- Decision. The miner proposal is removed from the working tree: `PROPOSAL-backup-miner.md`, `analysis-miner.ipynb`, `scripts/fetch_miner.py`, its two figures and its data files, and the miner section of `data/README.md`. The project is the covered call in `analysis.ipynb` alone. This supersedes the entry of 2026-10-27 that kept the miner as a backup and the entry above that named it the fallback. Those entries stay as history.
- Why. I want one project. The instructor's feedback in issue 2 covers only the covered call and says it can proceed, and the miner's model changed the baseline's decisions in at most one of 30 held-out months. Its results at the time of removal: the 7-day-mean rule earned \$120 per PH/s per month at a \$45 breakeven against \$19 for always committing, and the regression model's log forecast error was 0.0936 against 0.0963.
- Alternative. Keeping the miner as a fallback, which the entries above chose. `PROPOSAL-backup-miner.md` is still in the git history. The miner notebook, script, figures and data were never committed, so a copy of each is in the folder `aii600-miner-archive` next to the project, outside the repository.
- Revisit. If the covered call cannot meet `CHECKLIST.md` by 9 December, the miner work would have to be restored from that archive and the proposal reopened, which the instructor has not reviewed.
