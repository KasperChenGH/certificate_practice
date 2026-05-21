# Chapter 11 — Surface Models

## Why Model the Surface?

The implied volatility surface is an empirical fact: different options on the same stock have different implied volatilities. BSM, with its constant $\sigma$, cannot explain this. To price exotic options, interpolate between listed strikes, or simulate future scenarios, we need models that reproduce the smile and skew.

This chapter surveys four major approaches. The goal is to understand what each model does, when you would use it, and what it gets right and wrong — not to derive the mathematics in full.

## Local Volatility (Dupire)

**Core idea:** replace the single constant $\sigma$ with a function $\sigma_{\text{loc}}(S, t)$ that depends on both the stock price and time. The stock follows:

$$dS_t = rS_t\,dt + \sigma_{\text{loc}}(S_t, t)\,S_t\,dW_t$$

::: where
- $S_t$ — stock price at time $t$
- $\sigma_{\text{loc}}(S_t, t)$ — local volatility function
- $dW_t$ — Brownian motion increment
:::

Bruno Dupire showed in 1994 that if you know the prices of European options for all strikes and expiries, you can uniquely extract $\sigma_{\text{loc}}(S, t)$. The formula involves derivatives of option prices with respect to strike and expiry — essentially, the local volatility is pinned down by the shape of the IV surface.

**When to use it:** local vol is the standard for pricing path-dependent exotics (barriers, Asian options) when you need consistency with the vanilla surface. It is deterministic, so Monte Carlo simulation is straightforward.

| Pros | Cons |
|---|---|
| Fits today's entire IV surface exactly | Predicts unrealistic future smile dynamics |
| Unique — no free parameters once the surface is given | The smile flattens as spot moves (too fast) |
| Simple to implement via finite differences | Sensitive to interpolation of the input surface |

The biggest weakness is dynamic: local vol predicts that if the stock drops 10%, the future smile will look very different from what traders actually observe. This makes it unreliable for hedging path-dependent options over time.

## Stochastic Volatility (Heston)

**Core idea:** volatility itself is random. Instead of one source of randomness (the stock), there are two: the stock and its variance. The Heston model (1993) specifies:

$$dS_t = rS_t\,dt + \sqrt{v_t}\,S_t\,dW_1$$

$$dv_t = \kappa(\theta - v_t)\,dt + \xi\sqrt{v_t}\,dW_2$$

::: where
- $v_t$ — instantaneous variance
- $\kappa$ — mean-reversion speed
- $\theta$ — long-run variance level
- $\xi$ — vol of vol
- $dW_1, dW_2$ — correlated Brownian motions ($\rho$)
- $\rho$ — stock-variance correlation
:::

**The five parameters and what they control:**

- $v_0$: today's variance level — sets the overall IV level.
- $\kappa$: mean-reversion speed — controls how quickly IV term structure flattens. Large $\kappa$ means short-term IV spikes die out fast.
- $\theta$: long-run variance — the level to which the term structure converges at long expiries.
- $\xi$: vol of vol — controls the curvature of the smile. Higher $\xi$ means a more pronounced smile (fatter tails).
- $\rho$: correlation — controls the skew. Negative $\rho$ means stock drops coincide with volatility increases, generating the equity skew.

**How skew arises:** when $\rho < 0$, a decline in $S_t$ tends to coincide with a rise in $v_t$. This asymmetry makes downside moves more volatile than upside moves, producing higher IV for low strikes.

**When to use it:** Heston is popular for equity and FX options when you need realistic smile dynamics — for instance, pricing variance swaps, forward-starting options, or managing a vol book.

| Pros | Cons |
|---|---|
| Generates realistic smile and skew dynamics | Five parameters to calibrate |
| Semi-closed-form pricing via Fourier transform | Can struggle to fit short-term steep skew |
| Captures mean-reversion of volatility | The square-root process for $v_t$ is not always flexible enough |

## SABR

**Core idea:** another stochastic volatility model, but designed for simplicity and fast calibration. SABR (Stochastic Alpha Beta Rho) is the workhorse model for interest rate options and FX.

The model specifies:

$$dF_t = \alpha_t F_t^{\beta}\,dW_1$$

$$d\alpha_t = \nu\,\alpha_t\,dW_2$$

::: where
- $F_t$ — forward price
- $\alpha_t$ — stochastic volatility level
- $\beta$ — backbone parameter ($0 \leq \beta \leq 1$)
- $\nu$ — vol of vol
- $\rho$ — forward-volatility correlation
:::

The key feature of SABR is Hagan's **approximate closed-form formula** for implied volatility as a function of strike. Given the four parameters $(\alpha, \beta, \rho, \nu)$, you can directly compute $\sigma_{\text{IV}}(K)$ without solving any PDE or running a simulation.

**Parameter intuition:**
- $\alpha$: sets the overall level of volatility.
- $\beta$: determines the "backbone" — how ATM vol changes with the forward level. $\beta = 1$ gives lognormal dynamics; $\beta = 0$ gives normal dynamics.
- $\rho$: controls skew. Negative $\rho$ tilts the smile to the left (equity-style skew).
- $\nu$: controls curvature. Higher $\nu$ means a more pronounced smile.

**When to use it:** SABR is the default model for swaptions, caps/floors, and FX options. Traders calibrate it separately for each expiry.

| Pros | Cons |
|---|---|
| Approximate closed-form IV — very fast | Calibrated per expiry (no term-structure dynamics) |
| Intuitive parameters | Approximation can break down for extreme strikes |
| Industry standard for rates and FX | Not suitable for path-dependent exotics |

## SVI (Stochastic Volatility Inspired)

**Core idea:** forget the dynamics entirely. SVI is a **parametric curve** fitted directly to the implied variance surface. It is a tool for interpolation and extrapolation, not a model of how the stock moves.

The SVI parameterization expresses total implied variance as a function of log-moneyness:

$$w(k) = a + b\left(\rho(k - m) + \sqrt{(k - m)^2 + \sigma^2}\right)$$

::: where
- $w(k)$ — total implied variance
- $k$ — log-moneyness
- $a$ — overall variance level
- $b$ — slope ($\geq 0$)
- $\rho$ — skew rotation ($-1 < \rho < 1$)
- $m$ — horizontal translation
- $\sigma$ — vertex curvature ($> 0$)
:::

The five parameters have a natural geometric interpretation. The curve is a translated, rotated hyperbola. The parameter $\rho$ tilts it (generating skew), $\sigma$ controls how rounded the vertex is (smile curvature), and $m$ shifts the center.

**When to use it:** SVI is used for building smooth, arbitrage-free volatility surfaces from discrete market quotes. It is the standard tool at many banks and data vendors for surface construction.

| Pros | Cons |
|---|---|
| Extremely fast (just evaluate a formula) | No underlying dynamics — purely a fit |
| Smooth, well-behaved interpolation | Cannot simulate future surface evolution |
| Easy to enforce no-arbitrage constraints | Fitting across expiries requires care (SSVI extension) |
| Only 5 parameters per slice | Not suitable for exotic pricing or hedging |

## Model Comparison

Which model for which task? The following table summarizes:

| Use Case | Local Vol | Heston | SABR | SVI |
|---|---|---|---|---|
| **Vanilla pricing / surface fitting** | Excellent | Good | Good (per expiry) | Excellent |
| **Exotic pricing** | Good (static) | Good | Poor | Not applicable |
| **Dynamic hedging** | Poor (bad dynamics) | Good | Moderate | Not applicable |
| **Risk management / scenarios** | Moderate | Good | Moderate | Poor |
| **Speed of calibration** | Moderate | Slow | Fast | Very fast |
| **Interest rate / FX options** | Rarely used | Sometimes | Industry standard | Sometimes |
| **Equity index options** | Common | Common | Rare | Common |

**Rules of thumb:**
- Need to fit today's surface for interpolation? Use **SVI**.
- Pricing a vanilla book on rates or FX? Use **SABR**.
- Need realistic dynamics for hedging or exotics on equities? Use **Heston** (or local-stochastic vol hybrids).
- Need exact calibration to vanillas for pricing barriers? Use **local vol**, but be cautious about hedge ratios.

In practice, many desks combine models. A common approach is **local-stochastic volatility (LSV)**, which layers a local vol component on top of Heston to get both exact calibration and realistic dynamics. But that is a topic for a more advanced course.

## Practice

::: problem [Conceptual]
**Problem 11.1.** A junior trader proposes using the Heston model to price swaptions (interest rate options). A senior trader says SABR is a better choice for this market. Give two reasons why SABR is preferred over Heston for swaptions.

::: solution
**Solution.** Two reasons SABR is preferred:

1. **Speed of calibration.** SABR has an approximate closed-form formula for implied volatility as a function of strike. This means calibration is nearly instantaneous — just fit four parameters to the observed smile for each expiry. Heston requires numerical Fourier inversion to compute option prices, making calibration significantly slower. In rates markets where traders reprice thousands of swaptions throughout the day, speed is critical.

2. **Industry convention and parameter intuition.** SABR is the established standard for interest rate options. Its parameters ($\alpha, \beta, \rho, \nu$) map directly to quantities rates traders think about: overall vol level, backbone behavior, skew, and smile curvature. Risk systems, communication between desks, and regulatory models are all built around SABR parameters. Using Heston would create friction with the rest of the market infrastructure.

Additionally, swaptions are typically quoted and hedged per expiry, and SABR is designed for exactly this slice-by-slice approach. Heston's strength — modeling term-structure dynamics — is less relevant when each expiry is managed independently.
:::
:::

::: problem [Computation]
**Problem 11.2.** An SVI fit for the 3-month expiry ($T = 0.25$) on an equity index produces parameters $a = 0.01$, $b = 0.15$, $\rho = -0.40$, $m = 0.02$, $\sigma = 0.10$.

Compute the total implied variance and implied volatility for an ATM option ($k = 0$) and a 10%-OTM put ($k = -0.10$).

::: solution
**Solution.** Apply the SVI formula $w(k) = a + b\left(\rho(k - m) + \sqrt{(k - m)^2 + \sigma^2}\right)$.

**ATM ($k = 0$):**

$$w(0) = 0.01 + 0.15\left(-0.40(0 - 0.02) + \sqrt{(0 - 0.02)^2 + 0.01}\right)$$

$$= 0.01 + 0.15\left(0.008 + \sqrt{0.0004 + 0.01}\right)$$

$$= 0.01 + 0.15\left(0.008 + \sqrt{0.0104}\right)$$

$$= 0.01 + 0.15\left(0.008 + 0.1020\right) = 0.01 + 0.15 \times 0.1100 = 0.01 + 0.01650 = 0.02650$$

Implied volatility: $\sigma_{\text{IV}} = \sqrt{w / T} = \sqrt{0.02650 / 0.25} = \sqrt{0.1060} = 0.3256$, or about **32.6%**.

**10%-OTM put ($k = -0.10$):**

$$w(-0.10) = 0.01 + 0.15\left(-0.40(-0.10 - 0.02) + \sqrt{(-0.10 - 0.02)^2 + 0.01}\right)$$

$$= 0.01 + 0.15\left(-0.40(-0.12) + \sqrt{0.0144 + 0.01}\right)$$

$$= 0.01 + 0.15\left(0.048 + \sqrt{0.0244}\right)$$

$$= 0.01 + 0.15\left(0.048 + 0.1562\right) = 0.01 + 0.15 \times 0.2042 = 0.01 + 0.03063 = 0.04063$$

Implied volatility: $\sigma_{\text{IV}} = \sqrt{0.04063 / 0.25} = \sqrt{0.1625} = 0.4031$, or about **40.3%**.

The OTM put has significantly higher IV (40.3% vs 32.6%), reflecting the negative skew captured by $\rho = -0.40$.
:::
:::
