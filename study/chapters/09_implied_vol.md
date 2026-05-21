# Chapter 9 — Implied Volatility

## The Missing Input

The Black-Scholes-Merton formula for a European call requires five inputs:

$$C = S\,N(d_1) - K e^{-rT}N(d_2)$$

::: where
- $C$ — call price
- $S$ — current stock price
- $K$ — strike price
- $T$ — time to expiration
- $r$ — risk-free rate
- $N$ — standard normal CDF
- $d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}$, $\;d_2 = d_1 - \sigma\sqrt{T}$
- $\sigma$ — volatility of underlying
:::

Four of these inputs are directly observable: you can look up $S$ on a screen, $K$ and $T$ are written in the option contract, and $r$ comes from Treasury yields. The fifth input, $\sigma$, is not observable. It represents future volatility — how much the stock will bounce around between now and expiration — and nobody knows that in advance.

This creates a practical problem: you cannot use BSM to price an option without first choosing a value for $\sigma$. Implied volatility turns this problem on its head.

## Definition of Implied Volatility

Instead of plugging in $\sigma$ to get a price, we start with the market price and work backward to find the $\sigma$ that produces it.

**Implied volatility (IV)** is the value $\sigma_{\text{IV}}$ such that:

$$\text{BSM}(S, K, T, r, \sigma_{\text{IV}}) = C_{\text{market}}$$

::: where
- $\sigma_{\text{IV}}$ — implied volatility
- $C_{\text{market}}$ — observed market call price
- $\text{BSM}$ — BSM pricing function
:::

In words: implied volatility is the market's answer to the question "what constant volatility would make BSM agree with the price people are actually paying?"

## Why IV Exists and Is Unique

You might worry: does such a $\sigma_{\text{IV}}$ always exist? Could there be more than one? The answer is reassuring — for any valid market price, IV exists and is unique. Here is the intuition:

1. **BSM price increases with $\sigma$.** This follows from vega being positive: $\nu = S\sqrt{T}\,\varphi(d_1) > 0$. Higher volatility means the option has more chance of finishing deep in the money, so it is worth more.

2. **Lower bound.** As $\sigma \to 0$, the stock price becomes deterministic. The call converges to its discounted intrinsic value $\max(S - Ke^{-rT}, 0)$.

3. **Upper bound.** As $\sigma \to \infty$, $d_1 \to +\infty$ and $d_2 \to -\infty$, so $N(d_1) \to 1$ and $N(d_2) \to 0$. The call price approaches $S$ (the stock price itself).

So the BSM call price is a continuous, strictly increasing function of $\sigma$ that ranges from intrinsic value up to $S$. By the intermediate value theorem, any market price $C_{\text{market}}$ in that range corresponds to exactly one $\sigma_{\text{IV}}$.

**Intuitive summary:** higher vol means the option is worth more. There is exactly one vol level that makes BSM match any given price.

## Computing IV: Newton-Raphson

Since there is no closed-form formula for IV (you cannot "invert" BSM algebraically), we solve numerically. The standard method is **Newton-Raphson iteration**.

We want to find the root of $f(\sigma) = \text{BSM}(\sigma) - C_{\text{market}} = 0$. Newton-Raphson updates:

$$\sigma_{n+1} = \sigma_n - \frac{f(\sigma_n)}{f'(\sigma_n)} = \sigma_n - \frac{\text{BSM}(\sigma_n) - C_{\text{market}}}{\nu(\sigma_n)}$$

::: where
- $\sigma_n$ — IV estimate at iteration $n$
- $\nu$ — vega (BSM sensitivity to $\sigma$)
- $\varphi$ — standard normal PDF
:::

The key insight is that the derivative $f'(\sigma)$ is just vega, which we already know how to compute. Because vega is always positive and BSM is smooth, Newton-Raphson converges very quickly — typically **2 to 4 iterations** to machine precision.

### Worked Example

**Given:** $C_{\text{market}} = \$7.97$, $S = 100$, $K = 100$, $T = 0.5$, $r = 0.05$.

Find the implied volatility. Start with $\sigma_0 = 0.30$.

**Iteration 1.** Compute $d_1$ and $d_2$ at $\sigma = 0.30$:

$$d_1 = \frac{\ln(100/100) + (0.05 + 0.09/2)(0.5)}{0.30\sqrt{0.5}} = \frac{0 + 0.0475}{0.2121} = 0.2240$$

$$d_2 = 0.2240 - 0.2121 = 0.0119$$

Look up $N(0.2240) = 0.5886$, $N(0.0119) = 0.5047$. The BSM price is:

$$C_0 = 100(0.5886) - 100e^{-0.025}(0.5047) = 58.86 - 49.22 = 9.64$$

Vega: $\nu = 100\sqrt{0.5}\,\varphi(0.2240) = 70.71 \times 0.3940 = 27.86$

Update: $\sigma_1 = 0.30 - \frac{9.64 - 7.97}{27.86} = 0.30 - 0.0600 = 0.2400$

**Iteration 2.** At $\sigma = 0.2400$:

$$d_1 = \frac{0 + (0.05 + 0.0288)(0.5)}{0.2400\sqrt{0.5}} = \frac{0.0394}{0.1697} = 0.2321$$

$$d_2 = 0.2321 - 0.1697 = 0.0624$$

$N(0.2321) = 0.5918$, $N(0.0624) = 0.5249$. BSM price:

$$C_1 = 100(0.5918) - 97.53(0.5249) = 59.18 - 51.19 = 7.99$$

Update: $\sigma_2 = 0.2400 - \frac{7.99 - 7.97}{27.50} \approx 0.2393$

After just two iterations we are within a penny. The implied volatility is approximately **24%**.

## IV as the Market's Language

Professional options traders rarely discuss prices in dollar terms. Instead, they quote **implied volatility**.

Why? Because a dollar price is hard to compare across options. A $\$5$ call could be cheap or expensive depending on the stock price, time to expiry, and strike. But an IV of 25% has immediate meaning: the market is pricing in roughly a 25% annualized standard deviation for the underlying.

**What IV tells you:**

- **Expected magnitude of moves.** IV of 20% means the market expects the stock to move roughly $\pm 20\%$ over a year (one standard deviation). Over shorter periods, scale by $\sqrt{T}$: monthly expected move $\approx 20\% / \sqrt{12} \approx 5.8\%$.
- **Relative cheapness.** If two similar stocks have options with IV of 15% and 30%, the second is pricing in twice as much uncertainty.
- **Event pricing.** IV spikes before earnings, FDA decisions, or elections — events that could cause large moves.

## Implied vs Realized Volatility

It is important to distinguish two different volatility concepts:

| | Realized (Historical) Volatility | Implied Volatility |
|---|---|---|
| **Direction** | Backward-looking | Forward-looking |
| **Source** | Computed from past daily returns | Extracted from current option prices |
| **Formula** | $\sigma_{\text{real}} = \sqrt{\frac{252}{n-1}\sum_{i=1}^{n}(r_i - \bar{r})^2}$ | Solve $\text{BSM}(\sigma_{\text{IV}}) = C_{\text{market}}$ |
| **Interpretation** | How much did the stock actually move? | How much does the market expect it to move? |

### The Volatility Risk Premium

A persistent empirical fact: **implied volatility is usually higher than subsequently realized volatility.** On average for the S&P 500, IV exceeds realized vol by 2-4 percentage points.

This gap is the **volatility risk premium (VRP)**:

$$\text{VRP} = \sigma_{\text{IV}} - \sigma_{\text{realized}}$$

::: where
- $\text{VRP}$ — volatility risk premium
- $\sigma_{\text{realized}}$ — realized volatility
:::

Why does this premium exist? Option sellers bear the risk of large, sudden moves. They demand compensation — just as insurance companies charge premiums above expected losses. Option buyers (hedgers) willingly overpay because they value the protection.

This is why systematic option selling strategies (e.g., covered calls, short straddles) tend to be profitable on average — they harvest the volatility risk premium. But these strategies carry tail risk: when realized vol does exceed implied vol (crashes, crises), the losses can be severe.

## Practice

::: problem [Computation]
**Problem 9.1.** A European call has market price $C_{\text{market}} = \$3.50$. The underlying trades at $S = 50$, the strike is $K = 52$, time to expiration is $T = 0.25$ years, and the risk-free rate is $r = 0.03$. Starting from $\sigma_0 = 0.25$, perform one Newton-Raphson iteration to update your IV estimate.

*Use: $N(x)$ from a table or calculator. At $\sigma = 0.25$: $d_1 = -0.0635$, $d_2 = -0.1885$, $\text{BSM} = \$2.39$, $\nu = 9.92$.*

::: solution
**Solution.** Apply the Newton-Raphson update:

$$\sigma_1 = \sigma_0 - \frac{\text{BSM}(\sigma_0) - C_{\text{market}}}{\nu(\sigma_0)} = 0.25 - \frac{2.39 - 3.50}{9.92} = 0.25 - \frac{-1.11}{9.92} = 0.25 + 0.1119 = 0.3619$$

The updated IV estimate after one iteration is $\sigma_1 \approx 36.2\%$. The large jump from 25% to 36% reflects the fact that the market price ($\$3.50$) is significantly above the BSM price at $\sigma = 0.25$ ($\$2.39$), so the market is pricing in much more volatility. A second iteration would refine this further.
:::
:::

::: problem [Conceptual]
**Problem 9.2.** Explain why implied volatility is always uniquely determined for a call option whose market price satisfies $\max(S - Ke^{-rT}, 0) < C_{\text{market}} < S$. What goes wrong if the market price violates these bounds?

::: solution
**Solution.** The BSM call price is a continuous, strictly increasing function of $\sigma$ (because vega is strictly positive for $\sigma > 0$). As $\sigma \to 0$, the BSM price converges to the discounted intrinsic value $\max(S - Ke^{-rT}, 0)$. As $\sigma \to \infty$, the BSM price converges to $S$. By the intermediate value theorem, for any target price in the open interval $(\max(S - Ke^{-rT}, 0),\; S)$, there exists exactly one $\sigma_{\text{IV}}$ that produces it.

If $C_{\text{market}} \leq \max(S - Ke^{-rT}, 0)$, the option is priced at or below intrinsic value, violating no-arbitrage (you could buy the call, exercise, and profit). No positive $\sigma$ can produce such a low BSM price. If $C_{\text{market}} \geq S$, the call costs more than the stock itself, which is also an arbitrage violation. In either case, no implied volatility exists — the market price is inconsistent with BSM under any volatility.
:::
:::

::: problem [Computation]
**Problem 9.3.** Over the past month, a stock's daily returns (annualized) give a realized volatility of $\sigma_{\text{realized}} = 18\%$. The ATM one-month option has $\sigma_{\text{IV}} = 23\%$.

(a) What is the volatility risk premium?

(b) If you sold a one-month ATM straddle (short call + short put) and the stock subsequently realized exactly 18% volatility, would you expect a profit or loss? Why?

::: solution
**Solution.**

(a) The volatility risk premium is:

$$\text{VRP} = \sigma_{\text{IV}} - \sigma_{\text{realized}} = 23\% - 18\% = 5\%$$

(b) You would expect a **profit**. By selling the straddle, you collected premiums based on 23% implied volatility. If the stock only realizes 18% volatility, the actual moves are smaller than what was priced in. Your delta-hedging costs (or equivalently, the realized payoff to the option buyer) will be less than the premium you received. The 5-point gap between implied and realized vol is your profit source.

Intuitively, you sold "expensive" insurance and the actual damage was less than what the insurance premium assumed.
:::
:::
