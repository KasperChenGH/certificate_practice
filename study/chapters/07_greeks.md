# Chapter 7 — The Greeks

In Chapter 6 we learned the Black-Scholes formula: given a stock price, strike, time to expiry, risk-free rate, and volatility, we can compute the fair price of a European option. But a price alone is not enough. Traders need to know **how that price changes** when market conditions shift. The *Greeks* answer exactly this question. Each Greek measures the sensitivity of the option price to one input variable, holding all others fixed.

Throughout this chapter we use a single **running example**:

$$S = 100, \quad K = 100, \quad T = 0.25, \quad r = 0.05, \quad \sigma = 0.20$$

::: where
- $S$ — stock price
- $K$ — strike price
- $T$ — time to expiry (years)
- $r$ — risk-free rate (annualized)
- $\sigma$ — volatility (annualized)
:::

First we compute the quantities every Greek depends on:

$$d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}} = \frac{\ln(1) + (0.05 + 0.02)\times 0.25}{0.20\times 0.50} = \frac{0 + 0.0175}{0.10} = 0.175$$

$$d_2 = d_1 - \sigma\sqrt{T} = 0.175 - 0.10 = 0.075$$

::: where
- $d_1, d_2$ — standardized log-moneyness measures
:::

We also need the standard normal PDF evaluated at $d_1$:

$$\varphi(d_1) = \frac{1}{\sqrt{2\pi}} e^{-d_1^2/2} = \frac{1}{\sqrt{2\pi}} e^{-0.175^2/2} = \frac{1}{2.5066} \times e^{-0.01531} \approx 0.3989 \times 0.9848 \approx 0.3928$$

::: where
- $\varphi(\cdot)$ — standard normal PDF
:::

And the CDF values: $N(d_1) = N(0.175) \approx 0.5694$ and $N(d_2) = N(0.075) \approx 0.5299$.

::: where
- $N(\cdot)$ — standard normal CDF
:::

---

## 7.1 Delta ($\Delta$)

**Definition.** Delta measures how much the option price changes when the stock price moves by \$1, all else equal.

$$\Delta_C = N(d_1), \qquad \Delta_P = N(d_1) - 1$$

::: where
- $\Delta_C$ — call delta
- $\Delta_P$ — put delta
:::

**Intuition.** If $\Delta_C = 0.57$, then when the stock rises by \$1, the call price rises by about \$0.57. Delta tells you the option's *effective stock exposure*. A call with $\Delta = 0.57$ behaves like holding 0.57 shares — at least for small moves.

**Key properties:**
- Call delta is always between 0 and 1. Put delta is always between $-1$ and 0.
- An at-the-money (ATM) call has $\Delta \approx 0.5$; a deep in-the-money (ITM) call has $\Delta \to 1$; a deep out-of-the-money (OTM) call has $\Delta \to 0$.
- Delta also roughly equals the probability (under the risk-neutral measure) that the option finishes in the money — a useful mental shortcut.

![Call delta vs stock price](study/assets/delta_curve.svg)

**Hedge ratio.** To *delta-hedge* a long call position, you short $\Delta$ shares of stock per option. This makes your portfolio insensitive to small stock moves. If you own 100 calls with $\Delta = 0.57$, you short $100 \times 0.57 = 57$ shares.

**Worked example.**

$$\Delta_C = N(0.175) \approx 0.5694$$

$$\Delta_P = 0.5694 - 1 = -0.4306$$

The ATM call delta is about 0.57: a \$1 stock move changes the call value by roughly \$0.57.

---

## 7.2 Gamma ($\Gamma$)

**Definition.** Gamma measures how fast delta itself changes when the stock moves. It is the second derivative of the option price with respect to the stock price.

$$\Gamma = \frac{\varphi(d_1)}{S \sigma \sqrt{T}}$$

::: where
- $\Gamma$ — gamma (rate of delta change)
:::

**Intuition.** Gamma is the *curvature* of the option price curve. A high gamma means delta changes rapidly — the option's payoff is very nonlinear. A straight line (like a stock) has zero gamma; a curved payoff (like an option near the strike) has high gamma.

**Key properties:**
- Gamma is the same for calls and puts (with the same $S, K, T, r, \sigma$).
- Gamma is highest for ATM options and near-expiry options. Deep ITM and deep OTM options have low gamma because their deltas are already near their extreme values.
- Long options always have positive gamma. This means you *benefit* from big moves in either direction — your delta automatically adjusts in your favor.
- Short options have negative gamma — big moves hurt you.

**Worked example.**

$$\Gamma = \frac{0.3928}{100 \times 0.20 \times 0.50} = \frac{0.3928}{10.0} = 0.0393$$

This means if the stock moves from \$100 to \$101, the call delta changes from about 0.5694 to approximately $0.5694 + 0.0393 = 0.6087$.

---

## 7.3 Theta ($\Theta$)

**Definition.** Theta measures how much the option price decreases as time passes, with one fewer day to expiry, all else equal. It is the rate of time decay.

$$\Theta_C = -\frac{S \varphi(d_1) \sigma}{2\sqrt{T}} - r K e^{-rT} N(d_2)$$

$$\Theta_P = -\frac{S \varphi(d_1) \sigma}{2\sqrt{T}} + r K e^{-rT} N(-d_2)$$

::: where
- $\Theta_C$ — call theta (per year)
- $\Theta_P$ — put theta (per year)
:::

**Intuition.** Options are wasting assets. Every day that passes without a stock move, the option loses a bit of value because there is less time for a favorable move to occur. Theta quantifies this bleed. You can think of it as the "daily rental cost" of holding an option.

**Key properties:**
- Theta is usually negative for long calls and long puts (you lose value each day).
- Time decay accelerates as expiry approaches — theta is most negative for ATM, near-expiry options.
- The relationship between theta and gamma is deep: positive gamma costs negative theta. We will explore this in Chapter 8.

**Worked example.** Computing the annualized theta for the call:

First term: $-\frac{S \varphi(d_1) \sigma}{2\sqrt{T}} = -\frac{100 \times 0.3928 \times 0.20}{2 \times 0.50} = -\frac{7.856}{1.0} = -7.856$

Second term: $-rKe^{-rT}N(d_2) = -0.05 \times 100 \times e^{-0.0125} \times 0.5299 = -0.05 \times 100 \times 0.9876 \times 0.5299 = -2.617$

$$\Theta_C = -7.856 - 2.617 = -10.473 \text{ per year}$$

To convert to a per-day figure, divide by 365 (calendar days):

$$\Theta_C^{\text{daily}} = \frac{-10.473}{365} \approx -0.0287 \text{ per day}$$

The ATM call loses about **\$0.029 per day** (roughly 3 cents) to time decay.

---

## 7.4 Vega ($\nu$)

**Definition.** Vega measures how much the option price changes when implied volatility moves by one percentage point (0.01 in decimal).

$$\nu = S \varphi(d_1) \sqrt{T}$$

::: where
- $\nu$ — vega (vol sensitivity)
:::

**Intuition.** Higher volatility means bigger expected moves, which makes options more valuable (both calls and puts). Vega tells you how much you gain or lose when the market's volatility expectation shifts. If $\nu = 19.64$, then a 1-percentage-point increase in implied vol (say from 20% to 21%) raises the option price by about \$0.1964.

**Key properties:**
- Vega is always positive for long options (both calls and puts). Higher vol = more expensive options.
- Vega is the same for calls and puts with the same parameters.
- Vega is highest for ATM, longer-dated options. Near-expiry ATM options have high gamma but low vega; longer-dated ATM options have the reverse.
- Technically, "vega" is not a Greek letter — but it is universally called a "Greek" in practice.

**Worked example.**

$$\nu = 100 \times 0.3928 \times 0.50 = 19.64$$

If implied vol rises from 20% to 21% (a change of 0.01), the option price increases by approximately $19.64 \times 0.01 = \$0.1964$.

---

## 7.5 Rho ($\rho$)

**Definition.** Rho measures how much the option price changes when the risk-free interest rate moves by one percentage point.

$$\rho_C = K T e^{-rT} N(d_2), \qquad \rho_P = -K T e^{-rT} N(-d_2)$$

::: where
- $\rho_C$ — call rho
- $\rho_P$ — put rho
:::

**Intuition.** A higher interest rate reduces the present value of the strike you pay at expiry, making calls more valuable (you effectively pay less in today's dollars) and puts less valuable. For most short-dated equity options, rho is the smallest Greek — interest rates don't move much day to day. It matters more for long-dated options (LEAPS) or in environments with volatile rates.

**Worked example.**

$$\rho_C = 100 \times 0.25 \times e^{-0.0125} \times 0.5299 = 25.0 \times 0.9876 \times 0.5299 = 13.085$$

If the risk-free rate rises from 5% to 6% (a change of 0.01), the call price increases by approximately $13.085 \times 0.01 = \$0.131$.

---

## 7.6 Summary of All Greeks

Collecting all results for our ATM call ($S=100, K=100, T=0.25, r=0.05, \sigma=0.20$):

| Greek | Symbol | Call value | Put value | Highest when | Sign (long) |
|-------|--------|-----------|-----------|-------------|-------------|
| Delta | $\Delta$ | $+0.5694$ | $-0.4306$ | Deep ITM | Call: +, Put: $-$ |
| Gamma | $\Gamma$ | $0.0393$ | $0.0393$ | ATM, near expiry | Always + |
| Theta | $\Theta$ | $-0.0287$/day | $-0.0151$/day | ATM, near expiry | Usually $-$ |
| Vega | $\nu$ | $19.64$ | $19.64$ | ATM, long-dated | Always + |
| Rho | $\rho$ | $13.09$ | $-11.78$ | Long-dated, ITM | Call: +, Put: $-$ |

**Practical takeaways:**
- **Delta** tells you your directional exposure.
- **Gamma** tells you how that exposure changes — it's the source of option "convexity."
- **Theta** is the cost of holding that convexity.
- **Vega** is your exposure to changes in market fear/uncertainty.
- **Rho** usually matters least, except for long-dated options.

---

## Practice

::: problem [Conceptual]
**Problem 7.1.** A trader holds a portfolio of 200 call options, each with $\Delta = 0.60$ and $\Gamma = 0.04$. She delta-hedges by shorting shares. (a) How many shares does she short? (b) If the stock immediately rises by \$2, estimate her new delta per option and how many additional shares she needs to short.

::: solution
**Solution.** (a) She shorts $200 \times 0.60 = 120$ shares.

(b) After a \$2 rise, the new delta per option is approximately:

$$\Delta_{\text{new}} \approx 0.60 + \Gamma \times \Delta S = 0.60 + 0.04 \times 2 = 0.68$$

The total delta is now $200 \times 0.68 = 136$ shares equivalent. She already has 120 shares short, so she needs to short an additional $136 - 120 = 16$ shares to re-hedge.
:::
:::

::: problem [Computation]
**Problem 7.2.** Using the same parameters as the running example ($S=100, K=100, T=0.25, r=0.05, \sigma=0.20$), compute the vega of the option. If implied volatility drops from 20% to 18%, estimate the change in the call price.

::: solution
**Solution.** We computed $\varphi(d_1) \approx 0.3928$. Vega is:

$$\nu = S \varphi(d_1) \sqrt{T} = 100 \times 0.3928 \times 0.50 = 19.64$$

A drop from 20% to 18% is $\Delta\sigma = -0.02$. The estimated price change is:

$$\Delta C \approx \nu \times \Delta\sigma = 19.64 \times (-0.02) = -\$0.393$$

The call price falls by approximately \$0.39.
:::
:::

::: problem [Derivation]
**Problem 7.3.** Using the Black-Scholes call formula $C = SN(d_1) - Ke^{-rT}N(d_2)$ and the fact that $\frac{\partial d_1}{\partial S} = \frac{1}{S\sigma\sqrt{T}}$ and $d_2 = d_1 - \sigma\sqrt{T}$, show that $\Delta_C = N(d_1)$.

*Hint:* You will need the identity $S\varphi(d_1) = Ke^{-rT}\varphi(d_2)$.

::: solution
**Solution.** Differentiate $C = SN(d_1) - Ke^{-rT}N(d_2)$ with respect to $S$:

$$\Delta_C = \frac{\partial C}{\partial S} = N(d_1) + S\varphi(d_1)\frac{\partial d_1}{\partial S} - Ke^{-rT}\varphi(d_2)\frac{\partial d_2}{\partial S}$$

Since $d_2 = d_1 - \sigma\sqrt{T}$ and $\sigma\sqrt{T}$ does not depend on $S$, we have $\frac{\partial d_2}{\partial S} = \frac{\partial d_1}{\partial S} = \frac{1}{S\sigma\sqrt{T}}$. Substituting:

$$\Delta_C = N(d_1) + \frac{S\varphi(d_1)}{S\sigma\sqrt{T}} - \frac{Ke^{-rT}\varphi(d_2)}{S\sigma\sqrt{T}}$$

$$= N(d_1) + \frac{1}{S\sigma\sqrt{T}}\Big[S\varphi(d_1) - Ke^{-rT}\varphi(d_2)\Big]$$

By the identity $S\varphi(d_1) = Ke^{-rT}\varphi(d_2)$, the bracketed term is zero, and we get:

$$\Delta_C = N(d_1) \qquad \blacksquare$$
:::
:::
