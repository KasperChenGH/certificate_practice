# Chapter 10 — Implied Volatility

## Goals

- Define implied volatility (IV) as the unique $\sigma$ that equates the Black-Scholes call price to a market-observed price.
- Prove uniqueness of IV via the fact that vega $\nu > 0$ everywhere on the no-arbitrage domain.
- Explain the Newton-Raphson algorithm for numerically inverting the BSM formula.
- Contrast IV (forward-looking, market-derived) with realized volatility (backward-looking, statistically estimated).

## Prerequisites

- **Chapter 7** — closed-form Black-Scholes call price $C(S, K, T, r, \sigma)$.
- **Chapter 9** — vega $\nu = \partial C / \partial \sigma = S \varphi(d_1) \sqrt{T}$ and its positivity.

## Definition

The Black-Scholes call pricing formula depends on six inputs: the current stock price $S$, strike $K$, time to expiry $T$, risk-free rate $r$ — all directly observable in the market — and the volatility $\sigma$, which is *not* directly observable.

Given a market-observed call price $C_{\text{mkt}}$, the **implied volatility** $\sigma_{\text{IV}}$ is the unique value of $\sigma > 0$ satisfying

$$\text{BSM}_C(S, K, T, r, \sigma_{\text{IV}}) = C_{\text{mkt}},$$

::: where
| Symbol | Meaning |
|---|---|
| $\text{BSM}_C(S, K, T, r, \sigma)$ | Black-Scholes call price (Ch. 7) |
| $C_{\text{mkt}}$ | Market-observed call price |
| $\sigma_{\text{IV}}$ | Implied volatility — the unique solution |
:::

**Remark.** IV is what the market is *pricing in* — it is not a forecast of future stock moves in the statistical sense, but rather a measure of the volatility the market is incorporating into the current option price, including any risk premia demanded by option sellers.

## Existence and Uniqueness

**Theorem (existence and uniqueness).** For any $C_{\text{mkt}} \in \bigl(\max(S - K e^{-rT}, 0),\; S\bigr)$ — the no-arbitrage price range established in Ch. 5 — there exists a unique $\sigma_{\text{IV}} > 0$ such that $\text{BSM}_C(\sigma_{\text{IV}}) = C_{\text{mkt}}$.

**Proof.**

**Existence.** The function $\sigma \mapsto \text{BSM}_C(\sigma)$ is continuous on $(0, \infty)$. Examine its boundary behaviour:

- As $\sigma \to 0^+$: with zero volatility, the stock evolves deterministically as $S_T = S_0 e^{rT}$. The call's payoff is therefore $\max(S e^{rT} - K, 0)$ with certainty, and discounting back gives
$$\text{BSM}_C(\sigma) \;\to\; \max(S - K e^{-rT}, 0).$$
This is the lower bound of the no-arbitrage interval.

- As $\sigma \to \infty$: both $d_1$ and $d_2 = d_1 - \sigma\sqrt{T}$ are affected; $N(d_1) \to 1$ while $N(d_2) \to 0$, and the discounted strike term $K e^{-rT} N(d_2)$ vanishes. Hence
$$\text{BSM}_C(\sigma) \;\to\; S.$$
This is the upper bound of the no-arbitrage interval.

By the Intermediate Value Theorem, for any $C_{\text{mkt}}$ in the open interval $\bigl(\max(S - K e^{-rT}, 0),\, S\bigr)$, there exists at least one $\sigma_{\text{IV}} > 0$ achieving $\text{BSM}_C(\sigma_{\text{IV}}) = C_{\text{mkt}}$.

**Uniqueness.** From Ch. 9, vega satisfies

$$\nu(\sigma) = S\, \varphi(d_1)\, \sqrt{T} > 0 \quad \text{for all } \sigma > 0, T > 0, S > 0,$$

since $\varphi(d_1) > 0$ everywhere. Therefore $\sigma \mapsto \text{BSM}_C(\sigma)$ is strictly increasing, and a strictly increasing function can attain each value at most once. Hence $\sigma_{\text{IV}}$ is unique. $\blacksquare$

::: where
| Symbol | Meaning |
|---|---|
| $\nu(\sigma)$ | Vega: $\partial \text{BSM}_C / \partial \sigma = S \varphi(d_1) \sqrt{T}$ |
| $\varphi(\cdot)$ | Standard normal PDF |
| $d_1$ | $({\ln(S/K) + (r + \sigma^2/2)T})/(\sigma\sqrt{T})$ |
| $\max(S - K e^{-rT}, 0)$ | Intrinsic lower bound (no-arb, Ch. 5) |
| $S$ | Upper bound: call cannot exceed spot |
:::

**Remark.** Outside the no-arbitrage interval, no $\sigma_{\text{IV}} > 0$ exists — the market quote violates static no-arbitrage constraints. In practice this indicates either a transient quote error or a genuine (rare) free-money opportunity that arbitrageurs would close immediately.

## Newton-Raphson Algorithm

Since $\text{BSM}_C$ has no closed-form inverse in $\sigma$, we solve numerically. Define the residual function

$$f(\sigma) := \text{BSM}_C(\sigma) - C_{\text{mkt}},$$

so we seek $f(\sigma) = 0$. Because $f'(\sigma) = \nu(\sigma) > 0$, Newton's method applies directly. Starting from an initial guess $\sigma_0$, each iterate is

$$\boxed{\sigma_{n+1} = \sigma_n - \frac{f(\sigma_n)}{\nu(\sigma_n)} = \sigma_n - \frac{\text{BSM}_C(\sigma_n) - C_{\text{mkt}}}{\nu(\sigma_n)}},$$

::: where
| Symbol | Meaning |
|---|---|
| $\sigma_n$ | Current volatility iterate |
| $\text{BSM}_C(\sigma_n)$ | Black-Scholes call price at $\sigma_n$ |
| $C_{\text{mkt}}$ | Target market price |
| $\nu(\sigma_n)$ | Vega at $\sigma_n$: $S \varphi(d_1(\sigma_n)) \sqrt{T}$ |
:::

**Convergence remark.** Vega is smooth and strictly positive on the entire no-arbitrage range. Near the root, Newton's method converges *quadratically* — the number of correct decimal places roughly doubles each iteration. In practice, a starting guess of $\sigma_0 \approx 0.30$ (30%) is a reasonable prior for equity options; this typically converges to six decimal-place accuracy in at most five iterations.

## Implied Volatility vs. Realized Volatility

Two distinct notions of volatility arise in practice:

**Implied volatility (IV)** is *forward-looking*. It is derived by inverting the BSM formula given the current market option price. IV reflects the market's expectation of future volatility, as well as any risk premia that option sellers demand for bearing tail risk. IV is unobservable directly — it exists only through the option market.

**Realized volatility (RV)** is *backward-looking*. It is computed from historical stock returns. The standard estimator over an $n$-day window is

$$\hat{\sigma}_{\text{RV}}^2 = \frac{1}{n-1} \sum_{i=1}^{n} (r_i - \bar{r})^2 \cdot 252,$$

::: where
| Symbol | Meaning |
|---|---|
| $r_i = \ln(S_i / S_{i-1})$ | Daily log return on day $i$ |
| $\bar{r} = \frac{1}{n}\sum_{i=1}^n r_i$ | Sample mean of log returns |
| $252$ | Annualisation factor (trading days per year) |
| $n$ | Window length in trading days |
:::

**Remark.** Empirically, IV typically *exceeds* RV on equity indices. This gap is the **volatility risk premium (VRP)** — compensation paid by option buyers to sellers for bearing the risk of large moves. Measured ex post:

$$\text{VRP} = \mathbb{E}\bigl[\text{IV}^2 - \text{RV}^2\bigr],$$

where the expectation is taken over historical option-expiry windows and has been persistently positive on indices such as the S&P 500. Sellers of variance (e.g., via variance swaps) have historically harvested this premium as a systematic strategy.

## Practice
::: problem [Conceptual]
**Problem 10.1 [Conceptual].** Why is the function $\sigma \mapsto \text{BSM}_C(\sigma)$ strictly monotonic? What happens to $\text{BSM}_C$ as $\sigma \to 0^+$ and $\sigma \to \infty$?

::: solution
**Solution.** Strict monotonicity follows from $\nu = S \varphi(d_1) \sqrt{T} > 0$ for all $\sigma > 0$, $T > 0$, $S > 0$ — vega is strictly positive everywhere on the domain because the normal PDF $\varphi > 0$ everywhere. Therefore $\text{BSM}_C$ is differentiable with a strictly positive derivative, making it strictly increasing.

- As $\sigma \to 0^+$: with zero volatility, $S_T = S_0 e^{rT}$ is deterministic, and the call converges to the discounted deterministic payoff: $C \to \max(S e^{rT} - K, 0)\, e^{-rT} = \max(S - K e^{-rT}, 0)$.
- As $\sigma \to \infty$: $N(d_1) \to 1$ and $K e^{-rT} N(d_2) \to 0$, so $C \to S$. Intuitively, with infinite volatility the call nearly always ends up deep in-the-money; its value approaches the stock price itself.
:::
:::

---

::: problem [Derivation]
**Problem 10.2 [Derivation].** Derive the Newton-Raphson update formula starting from the first-order Taylor expansion of $\text{BSM}_C(\sigma)$ around the current iterate $\sigma_n$.

::: solution
**Solution.** Define $f(\sigma) = \text{BSM}_C(\sigma) - C_{\text{mkt}}$. First-order Taylor expansion around $\sigma_n$:

$$f(\sigma) \approx f(\sigma_n) + f'(\sigma_n)(\sigma - \sigma_n).$$

Setting $f(\sigma) = 0$ and solving for $\sigma$:

$$\sigma \approx \sigma_n - \frac{f(\sigma_n)}{f'(\sigma_n)} = \sigma_n - \frac{\text{BSM}_C(\sigma_n) - C_{\text{mkt}}}{\nu(\sigma_n)}.$$

This is precisely the Newton iterate $\sigma_{n+1}$. The approximation becomes exact at the root, and because $f$ is smooth with $f' > 0$ near the root, successive iterates converge quadratically.
:::
:::

---

::: problem [Computation]
**Problem 10.3 [Computation].** Market call price $C_{\text{mkt}} = \$4.61$ with $S = K = 100$, $T = 0.25$ years, $r = 0.05$. Starting from $\sigma_0 = 0.30$, perform two Newton-Raphson iterations. Report $\sigma_1$ and $\sigma_2$.

::: solution
**Solution.** All inputs are at-the-money ($S = K = 100$) with a 3-month expiry.

**Iteration 1: $\sigma_0 = 0.30$.**

Compute $d_1$:
$$d_1 = \frac{\ln(100/100) + (0.05 + 0.045) \cdot 0.25}{0.30 \cdot \sqrt{0.25}} = \frac{0 + 0.02375}{0.15} = 0.1583.$$

Compute $d_2$:
$$d_2 = d_1 - \sigma\sqrt{T} = 0.1583 - 0.15 = 0.0083.$$

Standard normal values: $N(0.1583) \approx 0.5629$, $N(0.0083) \approx 0.5033$, $e^{-rT} = e^{-0.0125} \approx 0.9876$.

Call price:
$$C(0.30) = 100 \cdot 0.5629 - 100 \cdot 0.9876 \cdot 0.5033 = 56.29 - 49.70 = \$6.59.$$

Vega (with $\varphi(0.1583) \approx 0.3938$):
$$\nu(0.30) = 100 \cdot 0.3938 \cdot 0.50 = 19.69.$$

Newton update:
$$\sigma_1 = 0.30 - \frac{6.59 - 4.61}{19.69} = 0.30 - \frac{1.98}{19.69} = 0.30 - 0.1005 \approx \mathbf{0.1995}.$$

**Iteration 2: $\sigma_1 \approx 0.20$.**

From Ch. 7 Problem 7.3, $C(0.20) \approx \$4.61$, exactly matching the target. Therefore $f(\sigma_1) \approx 0$, and the Newton correction is negligible:

$$\sigma_2 \approx \sigma_1 - \frac{4.61 - 4.61}{\nu(\sigma_1)} \approx \mathbf{0.20}.$$

**Result.** After one Newton step: $\sigma_1 \approx 0.20$; after two steps: $\sigma_2 \approx 0.20$ (converged). The true implied volatility is $\sigma_{\text{IV}} = 0.20$. This illustrates quadratic convergence — the iterate moved from 0.30 to essentially the exact answer in a single step.
:::
:::
