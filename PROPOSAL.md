# Proposal

## Hypothesis

Adding trailing seven-day spot volatility to a fitted 30-day volatility baseline improves forecasts of the upper tail of next-week BTC/USD returns and the resulting covered-call decisions under the same hypothetical option premiums. The original proposal and the instructor's payoff and sizing feedback are recorded in issue #2 and the decision log. This revision changes the data and premium inputs.

## Data

Use the Coin Metrics Community BTC daily spot reference archive and, for a separate secondary test, lagged fees per on-chain transaction. The archive is licensed under CC BY-NC 4.0. Use 240 training weeks followed by 52 non-overlapping holdout weeks. Daily references allow Friday 00:00 UTC decisions and expiries. The archive does not supply observed seven-day option premiums, so each policy receives the same hypothetical Black–Scholes curve anchored to trailing spot volatility with explicit price and cost sensitivities. The data provenance, pinned snapshot, and attribution appear in the data README.

## Decision affected by the model

A hypothetical BTC holder chooses whether to write a weekly BTC-settled covered call, selects the strike from expected net BTC payoff, and then chooses the fraction of BTC covered by maximizing expected log growth. A strike that is too low can surrender more upside than its premium compensates for. A strike that is too high forgoes premium. Compare to holding and writing a full call, include half Kelly, and score everyone on the same Fridays in weekly BTC log growth.
