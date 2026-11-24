# Final project defense rehearsal

**Wednesday, December 2 · 6½ minutes total · one directed question**

Aim for about three minutes of speaking. Rehearse without devices or AI. The action is a hypothetical BTC-settled weekly covered call on BTC already held.

| Point | What to explain aloud |
| --- | --- |
| Decision | Each Friday estimate next week's return distribution. Choose the strike with the highest expected BTC gain after an illustrative cost, then choose coverage by maximizing expected log wealth. Hold when the best size is zero. Compare with a full call and half Kelly. |
| Data and timing | The Coin Metrics daily price labeled Thursday is the Friday 00:00 UTC reference. Use 240 training windows from October 2020 through May 2025, followed by 52 non-overlapping weeks ending May 22, 2026. Training ends at the holdout boundary. |
| Forecast | Historical 30-day realized volatility estimates scale. The primary test adds trailing seven-day volatility, leaving every premium unchanged. Standardized training residuals supply the shape of next week's return distribution. The secondary comparison adds a seven-day on-chain fee-per-transaction feature lagged an extra day. |
| Finding | At the main premium, the 30-day model and the 30-plus-7-day model both finished about 12.0% ahead of holding in simulated BTC. The extra spot signal slightly worsened q90 pinball loss. Lagged fees improved q90 loss in the secondary comparison. The four-week paired growth interval for that model spans zero. |
| Risk | There were five writes in the main scenario. A forced full ATM call during a hypothetical 20% spot rally at representative inputs lost 13.6% of BTC relative to holding. In the actual sample, lowering the modeled premiums by 20% reduced the model's compounded advantage to 2.0%. |
| Value | At the representative candidate strike, the gross premium had to cover about 65,417 sats per BTC covered to meet expected payout and cost. Doubling training history did not change growth at the reported precision. Authorized seven-day bids and actual settlement prices would test the weakest assumption. |

The seven-day estimates summarize past spot moves. The study leaves the option market's estimate of future volatility unobserved. The cost of setting the strike too low is an upside payout that can consume many small premiums. A strike set too high gives up potential premium.
