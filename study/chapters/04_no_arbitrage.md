# Chapter 4 — No-Arbitrage and Replication

## Goals

- Set up the continuous-time market model (riskless bond and risky stock).
- Define self-financing trading strategies and arbitrage.
- State the First Fundamental Theorem of Asset Pricing (FTAP).
- Construct the risk-neutral measure $\mathbb{Q}$ for the Black-Scholes market using Girsanov's theorem (Ch. 3).
- State the risk-neutral pricing principle and show how it prices attainable European claims.

## Prerequisites

- **Ch. 1** — notation: probability space $(\Omega, \mathcal{F}, \mathbb{P})$, filtration $\{\mathcal{F}_t\}$, adapted processes, conditional expectation.
- **Ch. 3** — stochastic calculus: Itô's formula, geometric Brownian motion (GBM), Girsanov's theorem (change of measure, Radon-Nikodym derivative, new Brownian motion under $\mathbb{Q}$).

---

## Market model

We work on a filtered probability space $(\Omega, \mathcal{F}, \{\mathcal{F}_t\}_{0 \le t \le T}, \mathbb{P})$ satisfying the usual conditions, over a fixed horizon $T > 0$.

**Riskless bond.** The bond price process $B_t$ evolves deterministically:

$$B_0 = 1, \qquad dB_t = r\, B_t\, dt, \qquad \text{so} \qquad B_t = e^{rt}.$$

::: where
- $r \ge 0$ is the constant continuously-compounded risk-free interest rate.
- $B_t$ is $\mathcal{F}_t$-adapted (in fact deterministic).
:::

**Risky stock.** Under the real-world measure $\mathbb{P}$, the stock price follows geometric Brownian motion:

$$dS_t = \mu\, S_t\, dt + \sigma\, S_t\, dW_t, \qquad S_0 > 0.$$

::: where
- $\mu \in \mathbb{R}$ is the constant drift (expected return per unit time).
- $\sigma > 0$ is the constant volatility.
- $W_t$ is a standard Brownian motion on $(\Omega, \mathcal{F}, \mathbb{P})$, generating $\{\mathcal{F}_t\}$.
:::

Both $B_t$ and $S_t$ are adapted to the filtration $\{\mathcal{F}_t\}$. The filtration represents the information available to investors at each time.

---

## Portfolio and self-financing

### Definition

A *portfolio* is a pair of $\{\mathcal{F}_t\}$-adapted processes $(\phi_t, \psi_t)$, where $\phi_t$ is the number of shares of stock held at time $t$ and $\psi_t$ is the number of units of bond held at time $t$. The *portfolio value* is:

$$V_t = \phi_t\, S_t + \psi_t\, B_t.$$

::: where
- $\phi_t$ — units of stock (may be negative, allowing short-selling).
- $\psi_t$ — units of bond (may be negative, allowing borrowing).
- $V_t$ — total wealth at time $t$.
:::

### Definition (self-financing)

A portfolio $(\phi_t, \psi_t)$ is *self-financing* if changes in portfolio value arise only from changes in asset prices — not from external cash flows:

$$dV_t = \phi_t\, dS_t + \psi_t\, dB_t.$$

::: where
- $dS_t$ — instantaneous change in stock price.
- $dB_t = r B_t\, dt$ — instantaneous change in bond price.
- The absence of additional terms means no cash is injected or withdrawn.
:::

### Remark

The self-financing condition rules out external cash injections or withdrawals: any rebalancing of the portfolio — shifting wealth between stock and bond — must be financed internally by selling one asset to buy another. This is the natural constraint for a *trading strategy* that operates without outside funding.

---

## Arbitrage

### Definition

An *arbitrage* is a self-financing portfolio $(\phi_t, \psi_t)$ with initial value $V_0 = 0$ such that:

$$V_T \ge 0 \quad \mathbb{P}\text{-a.s.}, \qquad \text{and} \qquad \mathbb{P}(V_T > 0) > 0.$$

::: where
- $V_0 = 0$ — the strategy requires zero initial investment.
- $V_T \ge 0$ a.s. — there is no risk of loss.
- $\mathbb{P}(V_T > 0) > 0$ — there is a strictly positive probability of profit.
:::

### Remark

An arbitrage is a *free lunch*: starting with nothing, the investor is guaranteed not to lose money and has a genuine chance of making a profit. In liquid, well-functioning markets, such opportunities are eliminated near-instantaneously by the actions of rational traders. The assumption of *no arbitrage* (NA) is the foundational no-free-lunch hypothesis of modern mathematical finance.

---

## Risk-neutral measure

### Definition

A probability measure $\mathbb{Q}$ on $(\Omega, \mathcal{F}_T)$ is called an *equivalent martingale measure* (EMM), or *risk-neutral measure*, if:

1. **Equivalence:** $\mathbb{Q} \sim \mathbb{P}$ on $\mathcal{F}_T$ — they are mutually absolutely continuous (same null sets).
2. **Martingale property:** The discounted stock price $\tilde{S}_t = e^{-rt} S_t$ is a $\mathbb{Q}$-martingale.

::: where
- $\mathbb{Q} \sim \mathbb{P}$ means $\mathbb{Q}(A) = 0 \iff \mathbb{P}(A) = 0$ for all $A \in \mathcal{F}_T$.
- $\tilde{S}_t = e^{-rt} S_t$ is the stock price denominated in units of the bond (discounted).
- $\mathbb{Q}$-martingale means $\mathbb{E}^{\mathbb{Q}}[\tilde{S}_t \mid \mathcal{F}_s] = \tilde{S}_s$ for all $0 \le s \le t \le T$.
:::

### Remark

The equivalence condition is not merely technical: if $\mathbb{Q}$ were only absolutely continuous with respect to $\mathbb{P}$ (one-way), then $\mathbb{Q}$ could assign zero probability to events that $\mathbb{P}$ considers possible — effectively ignoring scenarios the market deems realistic. Equivalence ensures both measures agree on which events are genuinely possible. The martingale property means that, under $\mathbb{Q}$, discounted asset prices have no expected drift — investors are compensated only the risk-free rate.

---

## First Fundamental Theorem of Asset Pricing

### Theorem (FTAP, stated)

In the Black-Scholes market (and more generally under mild technical conditions), the following are equivalent:

1. The market admits *no arbitrage*.
2. There exists an *equivalent martingale measure* $\mathbb{Q} \sim \mathbb{P}$.

For the general semimartingale setting, the precise statement (No Free Lunch with Vanishing Risk $\iff$ existence of EMM) is due to Delbaen and Schachermayer (1994).

### Remark

We will not prove the FTAP in full generality here. Instead, we will *construct* the EMM explicitly for the Black-Scholes market using Girsanov's theorem (Ch. 3). This construction simultaneously establishes the existence direction of the FTAP and gives us the concrete tool needed for option pricing. The key insight is that eliminating the drift of $\tilde{S}_t$ under a new measure is precisely what Girsanov achieves.

---

## Construction of $\mathbb{Q}$ for the BSM market

To make $\tilde{S}_t = e^{-rt} S_t$ a martingale, we need to remove its drift. Under $\mathbb{P}$, applying Itô's formula to $\tilde{S}_t = e^{-rt} S_t$:

$$d\tilde{S}_t = (\mu - r)\tilde{S}_t\, dt + \sigma\tilde{S}_t\, dW_t.$$

The drift $(\mu - r)$ must be killed. Girsanov's theorem achieves this by shifting the Brownian motion.

**Market price of risk.** Define:

$$\theta = \frac{\mu - r}{\sigma}.$$

::: where
- $\theta$ is called the *market price of risk* (or Sharpe ratio of the stock): the excess return per unit of volatility.
- $\mu - r$ is the excess return above the risk-free rate.
- $\sigma > 0$ is the volatility (assumed non-zero, so $\theta$ is well-defined).
:::

**Girsanov change of measure.** Define the Radon-Nikodym derivative:

$$Z_T = \frac{d\mathbb{Q}}{d\mathbb{P}}\bigg|_{\mathcal{F}_T} = \exp\!\left(-\theta W_T - \tfrac{1}{2}\theta^2 T\right).$$

Since $\theta$ is constant, the Novikov condition $\mathbb{E}^{\mathbb{P}}[\exp(\tfrac{1}{2}\theta^2 T)] < \infty$ is satisfied, so $Z_T$ is a valid Radon-Nikodym derivative ($\mathbb{E}^{\mathbb{P}}[Z_T] = 1$). By Girsanov's theorem,

$$\tilde{W}_t = W_t + \theta\, t$$

is a standard Brownian motion under $\mathbb{Q}$.

::: where
- $Z_T > 0$ a.s. under $\mathbb{P}$, guaranteeing $\mathbb{Q} \sim \mathbb{P}$.
- $\tilde{W}_t$ is $\mathbb{Q}$-Brownian motion; it replaces $W_t$ in all subsequent calculations under $\mathbb{Q}$.
- The exponent $-\theta W_T - \tfrac{1}{2}\theta^2 T$ is the Doléans-Dade exponential of the process $-\theta W_t$.
:::

### Theorem

Under $\mathbb{Q}$, the stock price satisfies:

$$dS_t = r\, S_t\, dt + \sigma\, S_t\, d\tilde{W}_t.$$

::: where
- The drift changes from $\mu$ (under $\mathbb{P}$) to $r$ (under $\mathbb{Q}$): the risk-neutral drift equals the risk-free rate.
- $\tilde{W}_t$ is standard Brownian motion under $\mathbb{Q}$.
- Volatility $\sigma$ is unchanged by the measure change — a key feature of Girsanov.
:::

### Proof

Substitute $dW_t = d\tilde{W}_t - \theta\, dt$ into the $\mathbb{P}$-SDE for $S_t$:

$$dS_t = \mu\, S_t\, dt + \sigma\, S_t\, dW_t = \mu\, S_t\, dt + \sigma\, S_t\,(d\tilde{W}_t - \theta\, dt) = (\mu - \sigma\theta)\, S_t\, dt + \sigma\, S_t\, d\tilde{W}_t.$$

Since $\sigma\theta = \sigma \cdot \dfrac{\mu - r}{\sigma} = \mu - r$, the drift becomes:

$$\mu - \sigma\theta = \mu - (\mu - r) = r. \qquad \square$$

### Corollary

The discounted stock price $\tilde{S}_t = e^{-rt} S_t$ satisfies:

$$d\tilde{S}_t = \sigma\, \tilde{S}_t\, d\tilde{W}_t.$$

It is driftless under $\mathbb{Q}$, hence a $\mathbb{Q}$-martingale, confirming that $\mathbb{Q}$ is an EMM.

### Proof

Apply Itô's formula to $f(t, S) = e^{-rt} S$. The partial derivatives are $\partial_t f = -r e^{-rt} S$, $\partial_S f = e^{-rt}$, $\partial_{SS} f = 0$. Therefore:

$$d\tilde{S}_t = \partial_t f\, dt + \partial_S f\, dS_t + \tfrac{1}{2}\partial_{SS} f\,(dS_t)^2 = -r e^{-rt} S_t\, dt + e^{-rt}\, dS_t.$$

Substituting the $\mathbb{Q}$-SDE $dS_t = r S_t\, dt + \sigma S_t\, d\tilde{W}_t$:

$$d\tilde{S}_t = -r\tilde{S}_t\, dt + e^{-rt}(r S_t\, dt + \sigma S_t\, d\tilde{W}_t) = -r\tilde{S}_t\, dt + r\tilde{S}_t\, dt + \sigma\tilde{S}_t\, d\tilde{W}_t = \sigma\tilde{S}_t\, d\tilde{W}_t.$$

::: where
- The $dt$ terms cancel exactly: $-r\tilde{S}_t\, dt + r\tilde{S}_t\, dt = 0$.
- The result $d\tilde{S}_t = \sigma \tilde{S}_t\, d\tilde{W}_t$ has no drift term — $\tilde{S}_t$ is a local martingale under $\mathbb{Q}$.
- Since the diffusion coefficient $\sigma \tilde{S}_t$ is square-integrable on $[0, T]$ (as $\tilde{S}_t$ is log-normal with bounded moments), $\tilde{S}_t$ is a true $\mathbb{Q}$-martingale. $\square$
:::

---

## Risk-neutral pricing principle

### Theorem (Pricing)

Any attainable European claim with payoff $f(S_T)$ at time $T$ has time-$t$ value:

$$V_t = e^{-r(T - t)}\, \mathbb{E}^{\mathbb{Q}}\!\big[f(S_T) \,\big|\, \mathcal{F}_t\big].$$

::: where
- $f(S_T)$ — the payoff function (e.g., $(S_T - K)^+$ for a European call).
- $e^{-r(T-t)}$ — discount factor from $T$ back to $t$ at the risk-free rate.
- $\mathbb{E}^{\mathbb{Q}}[\,\cdot\, | \mathcal{F}_t]$ — conditional expectation under $\mathbb{Q}$ given information at time $t$.
- "Attainable" means the claim can be replicated by a self-financing portfolio.
:::

### Justification (sketch)

Suppose $(\phi_t, \psi_t)$ is a self-financing replicating portfolio with $V_T = f(S_T)$ a.s. The discounted portfolio value $\tilde{V}_t = e^{-rt} V_t$ satisfies, by the self-financing condition and Itô:

$$d\tilde{V}_t = \phi_t\, d\tilde{S}_t = \phi_t \cdot \sigma \tilde{S}_t\, d\tilde{W}_t.$$

This is a stochastic integral with respect to $\tilde{W}_t$ — it has no drift and is therefore a local $\mathbb{Q}$-martingale. Under suitable integrability conditions it is a true $\mathbb{Q}$-martingale, so:

$$\tilde{V}_t = \mathbb{E}^{\mathbb{Q}}[\tilde{V}_T \mid \mathcal{F}_t] = e^{-rT}\,\mathbb{E}^{\mathbb{Q}}[f(S_T) \mid \mathcal{F}_t].$$

Multiplying both sides by $e^{rt}$ gives $V_t = e^{-r(T-t)}\,\mathbb{E}^{\mathbb{Q}}[f(S_T) \mid \mathcal{F}_t]$. Full justification — including the connection to the Feynman-Kac representation — is deferred to Ch. 8.

### Remark

This is the central engine of option pricing theory. The price of any attainable derivative is the discounted expected payoff under the risk-neutral measure $\mathbb{Q}$ — not the real-world measure $\mathbb{P}$. Crucially, $\mu$ (the real-world drift) does not appear in the pricing formula: under $\mathbb{Q}$, all assets grow at the risk-free rate $r$. The measure $\mathbb{Q}$ encodes the market's collective risk preferences into $\theta = (\mu - r)/\sigma$, and once $\mathbb{Q}$ is fixed, pricing reduces to computing a conditional expectation. In Ch. 8 we apply this to derive the Black-Scholes formula.

---

## Practice

**Problem 4.1 [Conceptual].** Why must the equivalent martingale measure be *equivalent* to (not merely absolutely continuous with respect to) $\mathbb{P}$? What goes wrong if it's only absolutely continuous?

**Solution.** Mutual absolute continuity ($\mathbb{Q} \sim \mathbb{P}$) means $\mathbb{Q}$ and $\mathbb{P}$ share exactly the same null sets: an event is $\mathbb{Q}$-impossible if and only if it is $\mathbb{P}$-impossible. If $\mathbb{Q}$ were only absolutely continuous with respect to $\mathbb{P}$ (i.e., $\mathbb{Q} \ll \mathbb{P}$ but not $\mathbb{P} \ll \mathbb{Q}$), two problems arise:

1. **$\mathbb{Q}$ ignores $\mathbb{P}$-possible events.** There could be events $A$ with $\mathbb{P}(A) > 0$ but $\mathbb{Q}(A) = 0$. The pricing measure would effectively declare certain realistic market scenarios impossible, potentially mispricing claims whose payoffs depend on those scenarios.

2. **Arbitrage may survive.** The equivalence of measures is what ensures that a $\mathbb{Q}$-admissible strategy cannot exploit $\mathbb{P}$-possible events for free profit. One-way absolute continuity breaks this symmetry and can permit strategies that are "safe" under $\mathbb{Q}$ but profitable under $\mathbb{P}$.

Conversely, without $\mathbb{P} \ll \mathbb{Q}$, $\mathbb{Q}$ might assign positive probability to events $\mathbb{P}$ considers impossible (e.g., negative stock prices), which would invalidate the model's financial interpretation. Equivalence ensures both measures agree on what is genuinely possible in the market.

---

**Problem 4.2 [Derivation].** Use Itô's formula to show $d\tilde{S}_t = \sigma\tilde{S}_t\, d\tilde{W}_t$ under $\mathbb{Q}$, confirming $\tilde{S}_t$ is a $\mathbb{Q}$-martingale.

**Solution.** Let $\tilde{S}_t = e^{-rt} S_t$. Apply Itô's formula to $f(t, x) = e^{-rt} x$:

$$\partial_t f = -r e^{-rt} x, \qquad \partial_x f = e^{-rt}, \qquad \partial_{xx} f = 0.$$

By Itô's formula:

$$d\tilde{S}_t = \partial_t f\, dt + \partial_x f\, dS_t + \tfrac{1}{2}\partial_{xx} f\,(dS_t)^2 = -r e^{-rt} S_t\, dt + e^{-rt}\, dS_t.$$

Under $\mathbb{Q}$, the stock satisfies $dS_t = r S_t\, dt + \sigma S_t\, d\tilde{W}_t$. Substituting:

$$d\tilde{S}_t = -r e^{-rt} S_t\, dt + e^{-rt}(r S_t\, dt + \sigma S_t\, d\tilde{W}_t).$$

Collecting $dt$ terms: $-r e^{-rt} S_t\, dt + r e^{-rt} S_t\, dt = 0$. Therefore:

$$d\tilde{S}_t = e^{-rt} \cdot \sigma S_t\, d\tilde{W}_t = \sigma \tilde{S}_t\, d\tilde{W}_t.$$

This SDE has no drift term — $\tilde{S}_t$ is a local $\mathbb{Q}$-martingale. Since $\tilde{S}_t = S_0 \exp((\sigma \tilde{W}_t - \tfrac{1}{2}\sigma^2 t))$ under $\mathbb{Q}$ (log-normal with finite second moments), the stochastic integral $\int_0^t \sigma \tilde{S}_s\, d\tilde{W}_s$ is square-integrable on $[0, T]$. Hence $\tilde{S}_t$ is a true $\mathbb{Q}$-martingale, confirming $\mathbb{Q}$ is an EMM. $\square$

---

**Problem 4.3 [Computation].** Suppose $r = 0.05$, $\mu = 0.10$, $\sigma = 0.20$. Compute the market price of risk $\theta$ and the Radon-Nikodym derivative $Z_T = d\mathbb{Q}/d\mathbb{P}$ for $T = 1$, evaluated at $W_1 = 0$.

**Solution.**

*Step 1: Market price of risk.*

$$\theta = \frac{\mu - r}{\sigma} = \frac{0.10 - 0.05}{0.20} = \frac{0.05}{0.20} = 0.25.$$

*Step 2: Radon-Nikodym derivative.*

$$Z_T = \exp\!\left(-\theta W_T - \tfrac{1}{2}\theta^2 T\right).$$

*Step 3: Evaluate at $W_1 = 0$, $T = 1$.*

$$Z_1 = \exp\!\left(-0.25 \cdot 0 - \tfrac{1}{2} \cdot (0.25)^2 \cdot 1\right) = \exp\!\left(0 - \tfrac{1}{2} \cdot 0.0625\right) = \exp(-0.03125).$$

Computing: $\exp(-0.03125) \approx 0.9692$.

*Interpretation.* At $W_1 = 0$ (a "typical" path), the change-of-measure weight is close to 1, meaning paths near the mean are roughly equally likely under both $\mathbb{P}$ and $\mathbb{Q}$. The slight discount ($0.9692 < 1$) reflects that $\mathbb{Q}$ down-weights the real-world drift advantage: since $\mu > r$, paths that performed well under $\mathbb{P}$ are given slightly lower $\mathbb{Q}$-weight, shifting probability mass toward the risk-neutral growth rate.
