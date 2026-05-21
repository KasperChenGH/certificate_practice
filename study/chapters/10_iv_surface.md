# Chapter 10 — The Implied Volatility Surface

## The Failure of Constant Volatility

If the Black-Scholes-Merton model were exactly correct, every option on the same underlying stock would produce the same implied volatility, regardless of strike or expiry. After all, BSM assumes volatility $\sigma$ is a single constant.

In reality, this never happens. Compute IV for every listed option on, say, the S&P 500, and you get a different number for each contract. These differences are not noise — they form systematic, persistent patterns. The collection of all these implied volatilities, organized by strike and expiry, is called the **implied volatility surface**.

Understanding the surface is essential because it reveals where BSM's assumptions break down and how the market actually prices risk.

## The Volatility Smile

Fix an expiration date $T$ and plot IV against strike $K$. In many markets — especially FX and index options — the resulting curve is **U-shaped**: both deep out-of-the-money (OTM) puts (low strikes) and deep OTM calls (high strikes) have higher IV than at-the-money (ATM) options.

This pattern is called the **volatility smile**. It tells us the market assigns higher probability to extreme moves (in both directions) than BSM predicts. In BSM, returns are normal; in reality, they have fat tails.

## The Volatility Skew

In equity markets, the smile is not symmetric. Instead, the curve is **tilted**: OTM puts (low strikes) carry significantly higher IV than OTM calls (high strikes). This asymmetric pattern is called the **volatility skew** or **skew** for short.

For the S&P 500, a typical picture might look like:

| Strike (% of spot) | 85% | 90% | 95% | 100% (ATM) | 105% | 110% |
|---|---|---|---|---|---|---|
| IV | 28% | 24% | 21% | 19% | 18% | 17.5% |

Three forces drive the equity skew:

1. **Crash protection demand.** Portfolio managers buy OTM puts as insurance against market crashes. This persistent demand pushes up prices — and therefore IV — for low-strike options.

2. **The leverage effect.** When a stock drops, the company's debt-to-equity ratio rises, making it riskier. Higher risk means higher future volatility. So falling prices and rising volatility are correlated, which steepens the left side of the IV curve.

3. **Fat left tails.** Empirically, large negative returns occur more often than BSM predicts. The market knows this and prices it in. OTM puts need higher IV to account for the extra probability of crashes.

![Volatility smile vs equity skew](study/assets/vol_smile_skew.svg)

## Moneyness: Choosing the Right x-Axis

Plotting IV against raw strike $K$ is problematic: the curve shifts whenever the stock moves. Practitioners use **moneyness** measures that normalize the strike relative to the current forward price.

Common choices:

- **Simple moneyness:** $K / S$ — quick and intuitive.
- **Log-moneyness:** $k = \ln\!\left(\frac{K}{S\,e^{rT}}\right)$ — centers the axis at $k = 0$ for ATM forward.

$$k = \ln\!\left(\frac{K}{F}\right)$$

::: where
- $k$ — log-moneyness
- $K$ — strike price
- $F = S\,e^{rT}$ — forward price
:::

- **Delta:** express strikes as the BSM delta (e.g., "25-delta put" means the put whose BSM delta is $-0.25$). This is standard in FX markets.

Log-moneyness is the most common academic convention. Delta is the most common trading convention.

## Term Structure of Implied Volatility

Now fix the strike at ATM and vary the expiry $T$. The resulting curve — IV versus $T$ — is the **term structure** of implied volatility.

Key features:

- **Short-term IV is more volatile.** Near-term options respond sharply to news, earnings, and events. A stock reporting earnings next week might have one-week IV of 50% but one-year IV of 25%.
- **Long-term IV mean-reverts.** Over long horizons, the market expects volatility to settle toward a long-run average. This compresses the range of long-dated IV.
- **Term structure slope changes.** In calm markets, the term structure is often upward-sloping (short-term IV < long-term IV). During crises, it inverts: short-term IV spikes above long-term IV as the market prices immediate fear.

## The Full IV Surface

Combine the strike dimension and the expiry dimension. The implied volatility surface is a function:

$$\sigma_{\text{IV}}(K, T)$$

::: where
- $\sigma_{\text{IV}}(K, T)$ — IV as function of strike and expiry
:::

Visualize this as a 3D surface (strike on one horizontal axis, expiry on the other, IV on the vertical axis) or as a 2D heatmap. The surface is the complete summary of how the market prices options. Every model, every trade, every risk calculation ultimately references this surface.

## Sticky Strike vs Sticky Delta

When the stock price moves, how does the surface respond? Two idealized regimes describe the extremes:

**Sticky strike:** the IV assigned to a specific strike $K$ does not change when the spot price $S$ moves. If the 100-strike option had 20% IV yesterday, it still has 20% IV today even if the stock moved from 100 to 105. The surface is "anchored" to fixed strikes.

**Sticky delta:** the IV assigned to a specific delta level (e.g., 25-delta put) does not change when spot moves. The surface is "anchored" to moneyness. If the stock rallies, the strike that corresponds to 25-delta shifts upward, and it carries the same IV as before.

In practice, equity index skew behaves somewhere between the two:
- Over short time horizons and small moves, sticky strike is a reasonable approximation.
- Over longer horizons and larger moves, the surface shifts in a way closer to sticky delta.
- Empirically, the truth is a blend, and it varies by market regime.

The distinction matters for hedging. Your delta hedge depends on how IV reacts to spot changes — if you assume the wrong regime, your hedge ratios will be off.

## Skew-Adjusted Delta

The textbook BSM delta for a European call is:

$$\Delta_{\text{BS}} = N(d_1)$$

::: where
- $\Delta_{\text{BS}}$ — Black-Scholes delta
- $d_1 = \frac{\ln(S/K) + (r + \sigma_{\text{IV}}^2/2)T}{\sigma_{\text{IV}}\sqrt{T}}$
:::

But this formula assumes that when $S$ changes by $\$1$, implied volatility stays constant. In reality, as $S$ moves, the option's moneyness changes, and the skew means it picks up a different IV. The true sensitivity of the option price to spot includes this indirect effect:

$$\Delta_{\text{adj}} = \Delta_{\text{BS}} + \nu \cdot \frac{\partial \sigma_{\text{IV}}}{\partial S}$$

::: where
- $\Delta_{\text{adj}}$ — skew-adjusted delta
- $\nu$ — vega
- $\frac{\partial \sigma_{\text{IV}}}{\partial S}$ — IV sensitivity to spot
:::

For equity index options with negative skew, $\frac{\partial \sigma_{\text{IV}}}{\partial S} < 0$ (IV rises when spot falls). This makes the adjusted delta of a call **smaller** than the BSM delta, and the adjusted delta of a put **more negative**. Ignoring this correction leads to systematic hedging errors.

## No-Arbitrage Constraints on the Surface

Not every surface shape is valid. Arbitrage-free pricing imposes constraints:

### Calendar Spread Constraint

The **total implied variance** $w(T) = \sigma_{\text{IV}}^2(K, T) \cdot T$ must be non-decreasing in $T$ for each fixed strike $K$.

$$\sigma_{\text{IV}}^2(K, T_2) \cdot T_2 \geq \sigma_{\text{IV}}^2(K, T_1) \cdot T_1 \quad \text{for } T_2 > T_1$$

::: where
- $T_1, T_2$ — two expiries with $T_2 > T_1$
:::

If this is violated, the **forward variance** between $T_1$ and $T_2$ would be negative, which is impossible (variance cannot be negative). In trading terms, you could construct a calendar spread arbitrage: sell the shorter-dated option and buy the longer-dated one for a risk-free profit.

### Butterfly Constraint

For a fixed expiry, the IV curve across strikes must produce non-negative option prices for all strikes. Equivalently, the implied probability density must be non-negative everywhere. In practice, this means the curve $\sigma_{\text{IV}}(K)$ cannot be too concave — a deep dip in the middle would imply negative probability for some price range.

The butterfly spread test: for any three equally spaced strikes $K_1 < K_2 < K_3$, the butterfly payoff must have a non-negative price:

$$C(K_1) - 2C(K_2) + C(K_3) \geq 0$$

::: where
- $C(K_i)$ — call price at strike $K_i$
:::

Violations of either constraint signal data errors or mispricings that would be quickly exploited.

## Practice

::: problem [Conceptual]
**Problem 10.1.** The S&P 500 currently trades at 5000. The one-month ATM IV is 22%, while the one-month 90%-moneyness put (strike 4500) has IV of 32%. Explain three economic reasons why the OTM put has higher IV than the ATM option.

::: solution
**Solution.** Three reasons for the elevated IV on the OTM put:

1. **Demand for crash protection.** Institutional investors systematically buy OTM index puts to hedge portfolio downside. This persistent demand pressure raises the price — and therefore the implied volatility — of low-strike puts.

2. **Leverage effect.** If the index were to fall toward 4500, the constituent companies would have higher debt-to-equity ratios, making them fundamentally riskier. The market prices in this conditional increase in volatility at low strikes.

3. **Fat left tails.** Historical equity returns exhibit negative skewness and excess kurtosis — large drops occur more frequently than the normal distribution predicts. The IV skew reflects the market's recognition that BSM understates crash probabilities. A 10% decline (which would bring the index near 4500) is more likely than lognormal returns suggest, and the 32% IV compensates for that.
:::
:::

::: problem [Computation]
**Problem 10.2.** Two European calls on the same stock (same strike $K = 100$) have the following implied volatilities:

- 3-month ($T_1 = 0.25$): $\sigma_{\text{IV}} = 30\%$
- 6-month ($T_2 = 0.50$): $\sigma_{\text{IV}} = 22\%$

(a) Compute the total implied variance at each expiry.

(b) Does this surface satisfy the calendar spread constraint? If not, what kind of arbitrage could you exploit?

::: solution
**Solution.**

(a) Total implied variance $w = \sigma_{\text{IV}}^2 \cdot T$:

$$w(T_1) = (0.30)^2 \times 0.25 = 0.0900 \times 0.25 = 0.0225$$

$$w(T_2) = (0.22)^2 \times 0.50 = 0.0484 \times 0.50 = 0.0242$$

(b) We need $w(T_2) \geq w(T_1)$. Here $0.0242 \geq 0.0225$, so the constraint **is satisfied** (barely). The forward variance between 3 and 6 months is:

$$w(T_2) - w(T_1) = 0.0242 - 0.0225 = 0.0017$$

This corresponds to a forward volatility of $\sqrt{0.0017 / 0.25} = \sqrt{0.0068} \approx 8.2\%$, which is very low but non-negative. No calendar spread arbitrage exists, though the extremely low forward vol suggests the term structure is nearly inverted and the short-term volatility spike is expected to dissipate quickly.

*Note: if the 6-month IV were even slightly lower — say 21% — then $w(T_2) = 0.0441 \times 0.50 = 0.02205 < 0.0225 = w(T_1)$, and a calendar spread arbitrage would exist: sell the 3-month option (expensive variance) and buy the 6-month option (cheap variance).*
:::
:::

::: problem [Derivation]
**Problem 10.3.** Starting from the BSM call price $C(S, \sigma_{\text{IV}}(S))$, where IV depends on spot through the skew, derive the skew-adjusted delta formula:

$$\Delta_{\text{adj}} = \Delta_{\text{BS}} + \nu \cdot \frac{\partial \sigma_{\text{IV}}}{\partial S}$$

Explain why this correction makes the adjusted delta of an equity index call smaller than its BSM delta.

::: solution
**Solution.** The call price depends on spot both directly and through IV:

$$C = C(S,\; \sigma_{\text{IV}}(S))$$

Apply the total derivative with respect to $S$:

$$\Delta_{\text{adj}} = \frac{dC}{dS} = \frac{\partial C}{\partial S}\bigg|_{\sigma\text{ fixed}} + \frac{\partial C}{\partial \sigma} \cdot \frac{\partial \sigma_{\text{IV}}}{\partial S}$$

The first term is the standard BSM delta $\Delta_{\text{BS}} = N(d_1)$. The second term involves vega $\nu = \frac{\partial C}{\partial \sigma}$ multiplied by the skew slope $\frac{\partial \sigma_{\text{IV}}}{\partial S}$. Therefore:

$$\Delta_{\text{adj}} = \Delta_{\text{BS}} + \nu \cdot \frac{\partial \sigma_{\text{IV}}}{\partial S}$$

For equity indices, the skew is negative: $\frac{\partial \sigma_{\text{IV}}}{\partial S} < 0$ (when the index falls, IV rises). Since vega is always positive, the correction term $\nu \cdot \frac{\partial \sigma_{\text{IV}}}{\partial S}$ is negative. Therefore $\Delta_{\text{adj}} < \Delta_{\text{BS}}$ for a call.

Intuitively, when spot rises by $\$1$, the call gains from the direct price increase ($\Delta_{\text{BS}}$ effect), but it also loses a little because the IV drops (negative skew), reducing the option's time value. The net sensitivity is smaller than BSM suggests.
:::
:::
