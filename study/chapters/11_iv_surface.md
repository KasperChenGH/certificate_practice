# Chapter 11 — The IV Surface

## Goals

- Define the implied volatility (IV) surface $\sigma_{\text{IV}}(K, T)$ as a two-dimensional function of strike and expiry.
- Explain smile and skew shapes across strikes for fixed maturity, and term structure across maturities for fixed strike style.
- Prove the Breeden-Litzenberger theorem: the risk-neutral density of $S_T$ equals $e^{rT} \partial^2 C / \partial K^2$.
- State the butterfly arbitrage constraint ($\partial^2 C / \partial K^2 \ge 0$) as a direct corollary.
- State and justify the calendar arbitrage constraint: total implied variance is non-decreasing in $T$ at fixed moneyness.
- Contrast sticky-strike and sticky-delta conventions and derive the skew-adjusted delta formula.

## Prerequisites

- **Chapter 7** — closed-form Black-Scholes call price $C(S_0, K, T, r, \sigma)$ and the structure of $d_1$, $d_2$.
- **Chapter 10** — definition of implied volatility as the unique $\sigma$ inverting the BSM formula given a market price.

## The surface

In Chapter 10 we treated implied volatility as a single number: given one market option price, we inverted the BSM formula and obtained one $\sigma_{\text{IV}}$. But the market trades options at many strikes $K$ and many expiries $T$ simultaneously. Each $(K, T)$ pair produces its own implied volatility. The collection of all these values defines the **IV surface**:

$$\sigma_{\text{IV}} : (K, T) \mapsto \sigma_{\text{IV}}(K, T).$$

The surface is two-dimensional — one axis for strike, one for expiry. In a pure Black-Scholes world, where the true data-generating process has a single constant volatility $\sigma$, inverting BSM at any $(K, T)$ would return the same number: the surface would be perfectly flat. In reality, it is not flat, and the deviations from flatness carry rich information about market structure, risk premia, and the risk-neutral distribution of $S_T$.

### Smile

For a **fixed expiry** $T$, plot $\sigma_{\text{IV}}$ as a function of strike $K$. A **smile** is a U-shaped pattern: IV is higher for deep out-of-the-money (OTM) puts (low $K$) and higher for deep OTM calls (high $K$) relative to at-the-money (ATM) options. Both wings of the smile sit above the center. This shape is common in **FX and commodity markets**, where large moves are nearly as likely in either direction and option buyers demand elevated IV for protection against extreme outcomes on both sides.

### Skew

A **skew** — more precisely a *negative skew* or *put skew* — is a downward-sloping pattern: IV decreases monotonically as $K$ rises. OTM puts carry materially higher IV than OTM calls of the same absolute distance from ATM. This shape is the **standard pattern in equity index markets** (S&P 500, Eurostoxx, Nikkei). The skew reflects asymmetry in the risk-neutral distribution: the market prices in a much heavier left tail than right tail.

### Term structure

For a **fixed strike style** (e.g., holding ATM — meaning $K = S_0 e^{(r-q)T}$ for each $T$), plot $\sigma_{\text{IV}}$ as a function of $T$. This is the **term structure of implied volatility**.

- **Contango** (upward-sloping term structure): long-dated IV exceeds short-dated IV. This is the typical state in calm markets. It arises because uncertainty compounds over time; markets also embed a premium for uncertainty about long-run volatility itself.
- **Backwardation** (downward-sloping term structure): short-dated IV exceeds long-dated IV. This arises around near-term event risk — earnings announcements, FDA drug decisions, elections — where the market prices a concentrated burst of short-horizon uncertainty that is expected to resolve quickly. Once the event passes, longer-dated options are priced at lower volatility because the post-event world is expected to be calmer.

## Why equity skew exists

Several distinct mechanisms contribute to the persistent negative skew observed in equity index markets.

**Crash protection demand.** Institutional investors hold large long-equity portfolios and need to hedge tail risk. They buy OTM put options to obtain downside protection. This persistent, structural demand bids up the prices of OTM puts. Since the BSM formula is inverted to find IV, a higher price translates directly into a higher implied volatility. OTM calls face no analogous structural buyer — in fact they face natural sellers (see below) — so their IV remains lower. The asymmetry in demand between puts and calls is sufficient on its own to generate skew.

**Leverage effect (Black 1976).** When a firm's stock price falls, its outstanding debt does not shrink proportionally in the short run. The debt-to-equity ratio therefore rises, meaning the firm is now more leveraged. Higher leverage implies higher equity volatility — holders of a levered claim on assets face more amplified swings. Thus a falling stock price is mechanically associated with rising volatility. This negative correlation between spot returns and volatility changes means the risk-neutral distribution must accommodate the possibility of large down moves coinciding with elevated volatility, fattening the left tail and generating skew.

**Heavy left tails in equity returns.** Even setting aside leverage, equity returns exhibit excess kurtosis and negative skewness historically. Markets crash faster than they rally. The risk-neutral distribution implied by option prices must be consistent with these dynamics (at least approximately, after adjusting for risk premia). A heavy left tail requires OTM put prices — and therefore OTM put IVs — to be elevated relative to a lognormal benchmark.

**Demand-supply asymmetry.** Covered-call writing — selling OTM calls against long stock positions — is a widespread strategy among yield-seeking investors. This creates a structural supply of OTM calls, keeping their prices (and IVs) suppressed relative to where they would trade in a pure demand-driven market. On the demand side, portfolio insurers and risk managers are natural buyers of OTM puts. Together, excess supply of OTM calls and excess demand for OTM puts drive a wedge between the two wings, producing skew even if crash risk and leverage effects were absent.

## Breeden-Litzenberger

**Theorem (Breeden-Litzenberger).** Under risk-neutral pricing, the risk-neutral density $\rho_{S_T}$ of the terminal stock price $S_T$ is recoverable from call prices by taking the second derivative with respect to strike:

$$\rho_{S_T}(K) = e^{rT} \frac{\partial^2 C(S_0, K, T)}{\partial K^2},$$

::: where
| Symbol | Meaning |
|---|---|
| $C(S_0, K, T)$ | Time-0 call price with strike $K$ and expiry $T$ |
| $\rho_{S_T}(K)$ | Risk-neutral probability density of $S_T$ evaluated at $K$ |
| $r$ | Continuously compounded risk-free rate |
| $T$ | Time to expiry |
| $e^{rT}$ | Growth factor: converts discounted density back to un-discounted |
:::

**Proof.** Under risk-neutral measure $\mathbb{Q}$, the call price is the discounted expectation of its payoff:

$$C(S_0, K, T) = e^{-rT}\, \mathbb{E}^{\mathbb{Q}}\!\bigl[(S_T - K)^+\bigr] = e^{-rT} \int_K^{\infty} (s - K)\, \rho(s)\, ds,$$

where $\rho(s)$ is the risk-neutral density of $S_T$. We differentiate twice in $K$ using the Leibniz integral rule.

**First derivative.** Write the integral as $\int_K^\infty (s-K)\rho(s)\,ds$. Differentiating with respect to $K$:

- The lower limit of integration is $K$, contributing a boundary term $-(K - K)\rho(K) = 0$.
- The integrand $(s - K)$ depends on $K$, contributing $\int_K^\infty (-1)\,\rho(s)\,ds = -\int_K^\infty \rho(s)\,ds$.

Therefore:

$$\frac{\partial C}{\partial K} = e^{-rT} \left(-\int_K^\infty \rho(s)\,ds\right) = -e^{-rT}\,\mathbb{Q}(S_T > K).$$

This has an intuitive reading: the first derivative of a call price in strike is (up to sign and discounting) the risk-neutral probability of expiring in the money.

**Second derivative.** Differentiate once more in $K$:

$$\frac{\partial^2 C}{\partial K^2} = -e^{-rT} \cdot \frac{\partial}{\partial K}\mathbb{Q}(S_T > K) = -e^{-rT} \cdot \frac{\partial}{\partial K}\int_K^\infty \rho(s)\,ds = e^{-rT}\,\rho(K).$$

(The derivative of $\int_K^\infty \rho(s)\,ds$ with respect to $K$ is $-\rho(K)$, by the fundamental theorem of calculus.)

**Rearranging:**

$$\rho(K) = e^{rT} \frac{\partial^2 C}{\partial K^2}. \qquad \blacksquare$$

**Corollary (butterfly arbitrage constraint).** Since $\rho(K) \ge 0$ for all $K$ (densities are non-negative), the Breeden-Litzenberger formula immediately implies:

$$\frac{\partial^2 C}{\partial K^2} \ge 0 \quad \text{for all } K > 0.$$

The call price is **convex** in strike. This is the **butterfly arbitrage constraint**.

## No-arbitrage constraints on the surface

Any quoted surface of call prices — or equivalently any surface of implied volatilities — must satisfy two families of no-arbitrage constraints to be consistent with a valid probability model.

### Butterfly arbitrage

The butterfly constraint states that call prices must be convex in strike:

$$\frac{\partial^2 C}{\partial K^2} \ge 0 \quad \text{for all } K.$$

The Breeden-Litzenberger theorem proved this must hold: any violation implies $\rho(K) < 0$ at some point, which is impossible for a probability density. The violation is directly exploitable: construct a **butterfly spread** centered at the offending strike $K$. For small $h > 0$, buy $C(K - h)$, sell $2C(K)$, and buy $C(K + h)$. The cost of this position is $C(K-h) - 2C(K) + C(K+h)$, which equals $h^2 \cdot \partial^2 C/\partial K^2 + O(h^4)$ by a second-order Taylor expansion. If $\partial^2 C / \partial K^2 < 0$, the butterfly spread has *negative cost* — you receive cash upfront — yet its payoff at expiry is always non-negative (a butterfly payoff is a tent function, always $\ge 0$). This is a static free-money arbitrage.

### Calendar arbitrage

For the surface to be arbitrage-free across maturities, define the **total implied variance**:

$$w(k, T) = \sigma_{\text{IV}}(k, T)^2 \cdot T,$$

where $k = \ln(K / F(T))$ is the log-moneyness relative to the forward and $F(T) = S_0 e^{(r-q)T}$ is the forward price, where

| Symbol | Meaning |
|---|---|
| $w(k, T)$ | Total implied variance at log-moneyness $k$ and expiry $T$ |
| $k = \ln(K/F(T))$ | Log-moneyness relative to the forward |
| $F(T) = S_0 e^{(r-q)T}$ | Forward price of the stock at time $T$ |
| $q$ | Continuous dividend yield |
| $\sigma_{\text{IV}}(k, T)$ | Implied volatility at moneyness $k$ and expiry $T$ |

The **calendar arbitrage constraint** requires $w(k, T)$ to be **non-decreasing in $T$** for each fixed $k$:

$$\frac{\partial w}{\partial T}(k, T) \ge 0.$$

The economic justification is that an option with longer time to expiry has strictly greater time value, all else equal. An option's value encompasses all the uncertainty that can occur between now and expiry; a longer-dated option covers a strictly larger set of future scenarios. More formally, a longer-dated option can always be replicated by holding a shorter-dated option and then re-entering at expiry — giving a lower bound on the longer-dated option's value. If $w$ decreased in $T$ at some moneyness, you could construct a calendar spread (sell the near option, buy the far option at the same moneyness) that has negative net cost but non-negative payoff, again a free arbitrage.

## Sticky strike vs sticky delta

The IV surface is a snapshot at a given moment in time. When the stock price $S_0$ moves, the surface shifts. There are two canonical conventions for describing how it moves, and the choice has direct consequences for delta hedging.

**Sticky strike** assumes that when spot moves, the implied volatility at each *fixed absolute strike* $K$ remains unchanged. The surface is anchored to the strike axis. As spot falls, the ATM strike (the one closest to current spot) moves to lower $K$ values; by the skew shape, lower strikes carry higher IV. Therefore under sticky strike, when spot falls, the IV of the at-the-money option *rises automatically* as the ATM point slides leftward along the fixed skew curve. Sticky strike is the natural convention in calmer markets where the surface moves slowly and strikes do not need to be continuously re-expressed in relative terms.

**Sticky delta** (also called sticky moneyness) assumes that when spot moves, the implied volatility at each *fixed delta* (or equivalently, fixed moneyness $K/S$) remains the same. The entire surface translates horizontally with spot — it is pinned to the moneyness axis, not the absolute strike axis. Under sticky delta, the ATM implied volatility is constant regardless of where spot goes, because ATM is always at moneyness 1 by definition. Sticky delta is common in fast-moving or jumpy markets, and in FX, where options are quoted and risk-managed in delta space rather than in absolute strikes.

Real markets sit between these two extremes: the surface partially shifts when spot moves, with the degree of stickiness varying by market regime. The distinction matters because it changes how much delta you need to hold.

**Skew-adjusted delta.** Under standard BSM, $\Delta_{\text{BSM}} = \partial C / \partial S$. But this ignores the fact that when $S$ moves, the IV used to price the option also shifts (under sticky-delta dynamics). The total sensitivity of the call price to a move in spot is:

$$\Delta_{\text{adj}} = \Delta_{\text{BSM}} + \nu \cdot \frac{\partial \sigma_{\text{IV}}}{\partial S},$$

::: where
| Symbol | Meaning |
|---|---|
| $\Delta_{\text{BSM}}$ | Standard BSM delta: $\partial C / \partial S$ holding $\sigma_{\text{IV}}$ fixed |
| $\nu = \partial C / \partial \sigma$ | Vega: sensitivity of call price to a change in $\sigma$ |
| $\partial \sigma_{\text{IV}} / \partial S$ | How the relevant IV changes as spot moves (regime-dependent) |
| $\Delta_{\text{adj}}$ | Total delta accounting for the skew shift |
:::

Under sticky strike, $\partial \sigma_{\text{IV}} / \partial S = 0$ (IV at a fixed $K$ does not change with $S$), so $\Delta_{\text{adj}} = \Delta_{\text{BSM}}$. Under sticky delta, $\sigma_{\text{IV}}$ at a fixed moneyness does not change with $S$, but the IV relevant for a fixed-$K$ option does change as $K/S$ changes; this gives a non-zero correction. In practice, market makers estimate $\partial \sigma_{\text{IV}} / \partial S$ from the observed skew and use $\Delta_{\text{adj}}$ to set their hedge ratios.

## Practice
::: problem [Conceptual]
**Problem 11.1 [Conceptual].** Why does equity skew have OTM puts carrying higher IV than OTM calls? Give two distinct explanations.

::: solution
**Solution.** - *Crash protection demand*: institutional portfolios hold large long-stock positions. They hedge tail risk by buying OTM put options in quantity. This persistent, structural demand bids up OTM put prices above what a symmetric lognormal model would predict. Higher prices invert to higher IVs. OTM calls face no comparable structural buyer — indeed they face natural sellers (covered-call writers) — so their IVs are kept lower by supply pressure. The asymmetry in demand between the two wings is enough on its own to generate a persistent negative skew.
- *Leverage effect*: when a stock price falls, the firm's outstanding debt does not decline proportionally in the short run. The ratio of debt to equity therefore rises, increasing the firm's effective leverage. Higher leverage amplifies equity volatility — the equity is a more junior claim on a fixed asset base, making it riskier. Consequently, a falling spot is mechanically associated with rising realized volatility. The risk-neutral distribution must reflect this negative correlation between spot returns and future volatility, which fattens the left tail of the distribution relative to a lognormal and forces OTM put IVs higher.
:::
:::

---

::: problem [Derivation]
**Problem 11.2 [Derivation].** Prove the Breeden-Litzenberger formula.

::: solution
**Solution.** Under risk-neutral pricing with discount factor $e^{-rT}$:

$$C(S_0, K, T) = e^{-rT} \int_K^{\infty} (s - K)\,\rho(s)\,ds,$$

where $\rho$ is the risk-neutral density of $S_T$.

**First derivative in $K$.** Apply Leibniz rule. The boundary term at $s = K$ contributes $(K - K)\rho(K) = 0$. The integrand contributes $\partial(s-K)/\partial K = -1$:

$$\frac{\partial C}{\partial K} = e^{-rT}\!\int_K^\infty (-1)\,\rho(s)\,ds = -e^{-rT}\,\mathbb{Q}(S_T > K).$$

**Second derivative in $K$.** Differentiate $-e^{-rT}\int_K^\infty \rho(s)\,ds$ with respect to $K$. The fundamental theorem of calculus gives $\partial/\partial K \int_K^\infty \rho(s)\,ds = -\rho(K)$:

$$\frac{\partial^2 C}{\partial K^2} = -e^{-rT} \cdot (-\rho(K)) = e^{-rT}\,\rho(K).$$

**Rearranging:**

$$\rho(K) = e^{rT}\,\frac{\partial^2 C}{\partial K^2}. \qquad \blacksquare$$

Since $\rho(K) \ge 0$, we immediately obtain the butterfly constraint: $\partial^2 C / \partial K^2 \ge 0$ for all $K$.
:::
:::

---

::: problem [Computation]
**Problem 11.3 [Computation].** Three call prices are observed at equally spaced strikes: $C(95) = 7.20$, $C(100) = 4.60$, $C(105) = 2.50$. Compute the finite-difference approximation to $\partial^2 C / \partial K^2$ at $K = 100$ and verify whether the butterfly arbitrage constraint holds.

::: solution
**Solution.** Use the central second-difference formula with step $h = 5$:

$$\frac{\partial^2 C}{\partial K^2}\bigg|_{K=100} \approx \frac{C(95) - 2\,C(100) + C(105)}{h^2} = \frac{7.20 - 2(4.60) + 2.50}{5^2}.$$

Computing the numerator:

$$7.20 - 9.20 + 2.50 = 0.50.$$

Therefore:

$$\frac{\partial^2 C}{\partial K^2}\bigg|_{K=100} \approx \frac{0.50}{25} = 0.02.$$

The result is **positive** ($0.02 > 0$), so the butterfly arbitrage constraint $\partial^2 C / \partial K^2 \ge 0$ **holds** at $K = 100$. By Breeden-Litzenberger, this is equivalent to a positive risk-neutral density $\rho(100) = e^{rT} \cdot 0.02 > 0$, consistent with a valid probability model. Had the result been negative, one could construct a butterfly spread — long $C(95)$, short $2C(100)$, long $C(105)$ — at negative cost with a non-negative payoff, constituting a free arbitrage.
:::
:::
