# Chapter 6 — The Black-Scholes PDE

## Goals

- Derive the Black-Scholes partial differential equation from Itô's lemma and a continuously rebalanced delta-hedge replication argument.
- State the terminal and boundary conditions that pin down the European call and the European put as the unique solutions of the PDE.
- Understand why the real-world drift $\mu$ disappears from the PDE while the volatility $\sigma$ does not — the central conceptual content of replication.
- Extend the derivation to a stock paying a continuous dividend yield $q$ and read off the modified PDE.

## Prerequisites

- **Ch. 3** — Itô's lemma for $C^{2,1}$ functions of a continuous Itô process; the algebraic identity $(dW_t)^2 = dt$.
- **Ch. 4** — the no-arbitrage framework, self-financing portfolios, and the principle that a *locally riskless* portfolio must grow at the risk-free rate $r$.
- **Ch. 5** — the European call and put payoff functions $(S - K)^+$ and $(K - S)^+$, and the static no-arbitrage bounds that the PDE solution must respect.

---

## Setup

We work on a filtered probability space $(\Omega, \mathcal{F}, \mathbb{P}, \{\mathcal{F}_t\}_{t \in [0, T]})$ supporting a standard Brownian motion $W$ under $\mathbb{P}$. The market consists of two primary assets.

**Risk-free bond.** A money-market account that compounds continuously at the constant risk-free rate $r$:

$$B_t = e^{rt}, \qquad dB_t = r B_t\, dt.$$

::: where
- $B_t$ — value at time $t$ of one unit of the money-market account, with $B_0 = 1$.
- $r \ge 0$ — constant continuously-compounded risk-free rate.
- $t \in [0, T]$ — calendar time.
:::

**Risky stock.** The stock price $S$ follows geometric Brownian motion under the real-world measure $\mathbb{P}$:

$$dS_t = \mu S_t\, dt + \sigma S_t\, dW_t.$$

::: where
- $S_t$ — stock price at time $t$, strictly positive almost surely (from the closed-form solution in Ch. 3).
- $\mu \in \mathbb{R}$ — real-world drift (instantaneous expected rate of return on the stock).
- $\sigma > 0$ — instantaneous volatility, assumed constant.
- $W_t$ — standard $\mathbb{P}$-Brownian motion driving the stock.
:::

**The value function.** Let $V : (0, \infty) \times [0, T] \to \mathbb{R}$ denote the time-$t$ no-arbitrage price of a European derivative with maturity $T$ when the spot is $S_t = S$:

$$V \in C^{2, 1}\bigl((0, \infty) \times [0, T]\bigr), \qquad V(S, t) = \text{price of the derivative at time } t \text{ given } S_t = S.$$

::: where
- $V(S, t)$ — derivative price as a deterministic function of the current spot $S$ and current time $t$.
- $C^{2, 1}$ — twice continuously differentiable in $S$, once continuously differentiable in $t$. We write the partials as $V_t, V_S, V_{SS}$.
- $T$ — maturity (fixed, common to the entire chapter).
:::

That $V$ is a deterministic function of $(S_t, t)$ — i.e., that the price depends on the past only through the current spot — is the *Markovian* assumption. It is justified by the Markov property of geometric Brownian motion together with the structure of European payoffs $f(S_T)$, which depend on the path of $S$ only through its terminal value.

---

## The replicating $\Delta$-hedged portfolio

Consider the portfolio that is long one unit of the derivative and short $\phi_t$ shares of stock, with the residual held in the money-market account. Following Ch. 4, write the portfolio value as

$$\Pi_t = V(S_t, t) - \phi_t S_t + \psi_t B_t,$$

where $(\phi_t, \psi_t)$ is a self-financing trading strategy. The self-financing condition states that all changes in $\Pi_t$ come from price moves, not from injecting or withdrawing cash:

$$d\Pi_t = dV(S_t, t) - \phi_t\, dS_t + \psi_t\, dB_t.$$

::: where
- $\Pi_t$ — value at time $t$ of the hedged portfolio (long derivative, short $\phi_t$ shares of stock, $\psi_t$ units of bond).
- $\phi_t$ — number of shares of stock held short at time $t$ (the *hedge ratio*).
- $\psi_t$ — number of units of the money-market account held at time $t$.
- $dV, dS_t, dB_t$ — stochastic differentials of the derivative price, the stock, and the bond.
:::

We will choose $\phi_t$ in just one way — to cancel the random ($dW_t$) component of $d\Pi_t$ — and read off the PDE from the requirement that the remaining (deterministic) growth be the risk-free rate.

For the derivation that follows, only the *hedge ratio* $\phi_t$ matters. The bond holding $\psi_t$ is determined implicitly by the self-financing constraint and the choice $\phi_t = V_S$; it is convenient to write the argument in terms of the reduced portfolio $\Pi_t = V(S_t, t) - V_S(S_t, t)\, S_t$, with the bond leg absorbed into "the deterministic growth at rate $r$" via no-arbitrage.

---

## Derivation of the PDE

We carry out the derivation in four steps.

### Step 1 — Apply Itô's lemma to $V$

By Itô's lemma for $C^{2,1}$ functions of the Itô process $S_t$ (Ch. 3),

$$dV(S_t, t) = V_t\, dt + V_S\, dS_t + \tfrac{1}{2} V_{SS}\, (dS_t)^2.$$

Substitute $dS_t = \mu S_t\, dt + \sigma S_t\, dW_t$ and use the Itô algebra rule $(dW_t)^2 = dt$, $(dt)^2 = dt\, dW_t = 0$, so that $(dS_t)^2 = \sigma^2 S_t^2\, dt$:

$$dV = \Bigl(V_t + \mu S V_S + \tfrac{1}{2} \sigma^2 S^2 V_{SS}\Bigr) dt + \sigma S V_S\, dW_t.$$

::: where
- $V_t = \partial V / \partial t$ — partial derivative of the price with respect to time, evaluated at $(S_t, t)$.
- $V_S = \partial V / \partial S$ — partial derivative with respect to the spot (the hedge ratio).
- $V_{SS} = \partial^2 V / \partial S^2$ — second partial derivative with respect to the spot (related to gamma, Ch. 9).
- $S = S_t$ — current spot, treated as the spatial variable in the partial derivatives evaluated along the path.
- $\mu, \sigma$ — drift and volatility coefficients of the stock SDE.
- $dW_t$ — increment of the driving Brownian motion.
- $dt$ — infinitesimal time increment.
:::

### Step 2 — Subtract $V_S\, dS_t$ to cancel the $dW_t$ term

Compute $V_S\, dS_t = V_S \cdot \mu S\, dt + V_S \cdot \sigma S\, dW_t$. Subtracting from the Itô expansion above:

$$dV - V_S\, dS_t = \Bigl(V_t + \mu S V_S + \tfrac{1}{2} \sigma^2 S^2 V_{SS} - \mu S V_S\Bigr) dt + \bigl(\sigma S V_S - \sigma S V_S\bigr) dW_t,$$

which simplifies to

$$dV - V_S\, dS_t = \Bigl(V_t + \tfrac{1}{2} \sigma^2 S^2 V_{SS}\Bigr) dt.$$

::: where
- $V_S\, dS_t$ — the "$\Delta$-hedge" leg of the portfolio's $\mathbb{P}$-dynamics.
- $\sigma S V_S\, dW_t$ — the random component of $dV$, exactly cancelled by $V_S\, dS_t$.
- The right-hand side has no $dW_t$ term — the hedged portfolio is *locally riskless*.
:::

The cancellation of the $dW_t$ term is the heart of replication: the choice $\phi_t = V_S$ exactly offsets the stock-driven randomness in the derivative. Note that this cancellation works *only* because the diffusion coefficient of $V_S\, dS_t$ matches the diffusion coefficient of $dV$ — both are proportional to $\sigma S V_S$. The matching is automatic; it is a structural consequence of Itô's lemma, not a free choice.

### Step 3 — Equate to no-arbitrage growth at rate $r$

The portfolio $\Pi_t = V(S_t, t) - V_S(S_t, t)\, S_t$ now has dynamics

$$d\Pi_t = dV - V_S\, dS_t = \Bigl(V_t + \tfrac{1}{2} \sigma^2 S^2 V_{SS}\Bigr) dt,$$

which is locally deterministic — it has no $dW_t$ component. By the no-arbitrage principle of Ch. 4, a self-financing locally riskless portfolio must earn the instantaneous risk-free rate; otherwise an arbitrage exists between this portfolio and the money-market account. Hence

$$d\Pi_t = r \Pi_t\, dt = r \bigl(V - V_S S\bigr)\, dt.$$

::: where
- $\Pi_t = V(S_t, t) - V_S(S_t, t) S_t$ — the delta-hedged portfolio after $dW$-cancellation.
- $r$ — risk-free rate, applied to the locally riskless portfolio by the no-arbitrage principle.
- $r(V - V_S S)\, dt$ — required instantaneous growth of $\Pi_t$ under no-arbitrage.
:::

### Step 4 — Equate the two expressions for $d\Pi_t$

Setting Step 2 equal to Step 3 (both equal $d\Pi_t$):

$$\Bigl(V_t + \tfrac{1}{2} \sigma^2 S^2 V_{SS}\Bigr) dt = r \bigl(V - V_S S\bigr) dt.$$

Cancel $dt$ and rearrange:

$$\boxed{\,V_t + \tfrac{1}{2} \sigma^2 S^2 V_{SS} + r S V_S - r V = 0.\,}$$

::: where
- $V_t, V_S, V_{SS}$ — time, first-spatial, and second-spatial partials of the price.
- $S$ — current spot (the spatial variable on the domain $(0, \infty)$).
- $\sigma$ — instantaneous volatility (squared in the diffusion term).
- $r$ — risk-free rate.
- The PDE is *linear*, *parabolic*, and *backward in time* (the coefficient of $V_t$ is $+1$, and the natural data is given at $t = T$).
:::

This is the **Black-Scholes partial differential equation**. Every European derivative with payoff $f(S_T)$ whose price $V(S, t)$ is sufficiently smooth must satisfy this equation on $(0, \infty) \times [0, T)$.

---

## The PDE in standard notation

The equation derived above, written in Leibniz notation for reference:

$$\frac{\partial V}{\partial t} + \tfrac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + r S \frac{\partial V}{\partial S} - r V = 0, \qquad (S, t) \in (0, \infty) \times [0, T).$$

::: where
- $\partial V / \partial t$ — sensitivity of the price to calendar time (the "theta"-like derivative).
- $\partial V / \partial S$ — sensitivity of the price to the spot (delta).
- $\partial^2 V / \partial S^2$ — convexity of the price in the spot (gamma).
- $(0, \infty)$ — admissible range of the spot $S$ (excluding the absorbing barrier $S = 0$, which enters as a boundary condition).
- $[0, T)$ — interior of the time interval; the terminal condition is posed at $t = T$.
:::

### Remark (drift vanishes)

The real-world drift $\mu$ does **not** appear in the PDE. The price $V(S, t)$ is independent of the rate at which the stock tends to grow under $\mathbb{P}$. The intuition is sharp: the delta hedge $\phi_t = V_S$ neutralizes all directional exposure to $S_t$, leaving only the *magnitude* of random fluctuations (encoded by $\sigma$) and the cost of carrying the residual cash position (encoded by $r$). Two investors who disagree completely about the expected return of the stock — one bullish ($\mu \gg r$), one bearish ($\mu < 0$) — must nevertheless agree on the price of every European option, because both can replicate the payoff using the same self-financing strategy at the same cost. This is arguably the single most counterintuitive consequence of dynamic replication.

A second remark: the PDE depends on $\sigma$, and only $\sigma$ — not on the joint $(\mu, \sigma)$. This is why option prices give us a *direct* window into the market's perception of volatility (implied volatility, Ch. 10) but no direct view of the drift.

---

## Terminal and boundary conditions

The PDE alone does not pin down a unique solution. It is a *backward parabolic* equation on the strip $(0, \infty) \times [0, T)$, and we need data at $t = T$ together with conditions at the spatial boundaries $S = 0$ and $S \to \infty$.

### Terminal condition

The PDE is solved backward in time from $t = T$. At expiration, the no-arbitrage price equals the contractual payoff:

$$V(S, T) = \text{payoff}(S).$$

For the two contracts of primary interest:

- **European call.** $\quad C(S, T) = (S - K)^+ = \max(S - K, 0).$
- **European put.** $\quad P(S, T) = (K - S)^+ = \max(K - S, 0).$

::: where
- $V(S, T)$ — value of the derivative at expiry, as a function of the terminal spot $S = S_T$.
- $C(S, T), P(S, T)$ — terminal values of the call and put, respectively.
- $K$ — strike price (positive constant).
- $(\cdot)^+$ — positive-part operator $x \mapsto \max(x, 0)$.
:::

### Boundary at $S = 0$

The stock SDE has coefficients $\mu S$ and $\sigma S$, both multiplicative in $S$. If $S_{t_0} = 0$ for some $t_0$, then for all $t \ge t_0$:

$$dS_t = \mu \cdot 0 \cdot dt + \sigma \cdot 0 \cdot dW_t = 0,$$

so $S_t = 0$ for all $t \ge t_0$. The origin is an **absorbing state**: once $S$ reaches $0$, it stays there. In particular, conditional on $S_t = 0$ at any earlier time, the terminal value $S_T$ equals $0$ almost surely.

**Call boundary at $S = 0$.** If $S_t = 0$, then $S_T = 0$ almost surely, and the call's payoff $(0 - K)^+ = 0$ is certain. The time-$t$ value of a certain payoff of $0$ is $0$:

$$C(0, t) = 0 \quad \text{for all } t \in [0, T].$$

**Put boundary at $S = 0$.** If $S_t = 0$, then $S_T = 0$ almost surely, and the put's payoff $(K - 0)^+ = K$ is certain. The time-$t$ value of receiving the constant $K$ at time $T$ is its discounted value at the risk-free rate:

$$P(0, t) = K e^{-r(T - t)} \quad \text{for all } t \in [0, T].$$

::: where
- $C(0, t), P(0, t)$ — call and put values at the absorbing boundary $S = 0$.
- $K e^{-r(T - t)}$ — present value at time $t$ of receiving the strike $K$ at maturity.
- $T - t$ — time remaining to expiry.
- The certainty of $S_T = 0$ given $S_t = 0$ is the financial content of *absorbing* behavior at the origin.
:::

### Boundary as $S \to \infty$

For very large spot, the asymptotic behavior of each payoff dominates.

**Call boundary as $S \to \infty$.** For $S$ very large, the call is deep in-the-money, and exercise at $T$ is essentially certain. In this regime $(S_T - K)^+ \approx S_T - K$. A static replication of the payoff $S_T - K$ is: long one share of stock (paying $S_T$ at $T$) and short $K e^{-r(T-t)}$ in the money-market account (paying $K$ at $T$, costing $K e^{-r(T-t)}$ at $t$). Its time-$t$ cost is $S - K e^{-r(T-t)}$, so

$$C(S, t) \sim S - K e^{-r(T-t)} \quad \text{as } S \to \infty.$$

::: where
- $C(S, t)$ — call price at time $t$ when the spot is $S$.
- $S - K e^{-r(T-t)}$ — time-$t$ value of a forward contract on the stock with delivery price $K$ at time $T$.
- "$\sim$" — asymptotic equivalence: $C(S, t) / \bigl(S - K e^{-r(T-t)}\bigr) \to 1$ as $S \to \infty$.
- The asymptote is the **intrinsic forward value**: a deep-ITM call behaves like a forward contract.
:::

**Put boundary as $S \to \infty$.** For very large spot, the put is deep out-of-the-money, and the probability $\mathbb{P}(S_T < K)$ tends to $0$ as $S \to \infty$ (the lognormal distribution of $S_T$ given $S_t = S$ has all of its mass shifted to large values). Equivalently, the put price is bounded above by $K e^{-r(T-t)}$ (its static upper bound from Ch. 5), and the lower bound $\max(K e^{-r(T-t)} - S, 0)$ vanishes as $S$ grows. Hence

$$P(S, t) \to 0 \quad \text{as } S \to \infty.$$

::: where
- $P(S, t)$ — put price at time $t$ when the spot is $S$.
- $\mathbb{P}(S_T < K \mid S_t = S) \to 0$ — exercise probability for the put vanishes as $S \to \infty$, since the lognormal distribution concentrates far above $K$.
- The asymptote is the financial intuition that a deep-OTM put is nearly worthless.
:::

---

## Uniqueness

The Black-Scholes PDE together with

1. the terminal condition $V(S, T) = \text{payoff}(S)$,
2. the boundary condition at $S = 0$ (e.g., $C(0, t) = 0$ for the call, $P(0, t) = K e^{-r(T-t)}$ for the put), and
3. the asymptotic condition as $S \to \infty$ (e.g., $C(S, t) \sim S - K e^{-r(T-t)}$ for the call, $P(S, t) \to 0$ for the put),

admits a unique $C^{2,1}$ solution of moderate growth at infinity. The justification is the **Feynman-Kac theorem** (developed in Ch. 8): the unique solution is the discounted expected payoff under the risk-neutral measure,

$$V(S, t) = e^{-r(T - t)}\, \mathbb{E}^{\mathbb{Q}}\!\left[\,\text{payoff}(S_T)\,\bigm|\, S_t = S\,\right],$$

and this representation is intrinsically unique once the dynamics of $S$ under $\mathbb{Q}$ are fixed. We defer the formal statement and proof to Ch. 8; for the present chapter, uniqueness is taken on faith.

A practical reading: any *candidate* solution to the PDE that matches the terminal payoff and respects the two boundary conditions *is* the no-arbitrage price. This is precisely how Ch. 7 will proceed — by changing variables, reducing the PDE to the heat equation, applying the heat-kernel solution, and verifying that the resulting closed form satisfies all four conditions.

---

## Remark — extension to dividends

If the underlying pays a continuous dividend yield $q \ge 0$, the holder of one share collects dividend cash at rate $q S_t\, dt$. The self-financing condition for the hedged portfolio is modified — the short stock position *pays out* dividends at rate $q \phi_t S_t\, dt$, which is a cash outflow from the portfolio. Repeating Steps 1-4 of the derivation with this correction yields the modified PDE:

$$\frac{\partial V}{\partial t} + \tfrac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + (r - q) S \frac{\partial V}{\partial S} - r V = 0.$$

::: where
- $q \ge 0$ — continuous dividend yield (constant).
- $(r - q) S V_S$ — the modified first-order coefficient; the drift of $S$ under $\mathbb{Q}$ becomes $r - q$ rather than $r$.
- $- r V$ — unchanged; the discounting of the option value happens at $r$, not $r - q$.
- All other terms — identical to the no-dividend case.
:::

Intuition: the dividend reduces the effective growth rate of the stock under the pricing measure. The forward price becomes $S e^{(r - q)(T - t)}$ rather than $S e^{r(T - t)}$. The boundary conditions are also modified — for the call, the upper asymptote becomes $C(S, t) \sim S e^{-q(T-t)} - K e^{-r(T-t)}$, because the share you would hold to replicate the payoff itself pays out dividends. The full derivation is the content of Problem 6.3.

---

## Practice

**Problem 6.1 [Conceptual].** Explain in one paragraph why the real-world drift $\mu$ disappears from the Black-Scholes PDE while the volatility $\sigma$ does not. What is the financial intuition?

**Solution.** The PDE is derived by choosing the hedge ratio $\phi_t = V_S$ to cancel the $dW_t$ term in the dynamics of the portfolio $\Pi_t = V(S_t, t) - \phi_t S_t$. This cancellation depends *only* on the diffusion coefficient of the stock (which is proportional to $\sigma$), not on the drift coefficient (which is proportional to $\mu$). Once the random component is cancelled, the residual dynamics of $\Pi_t$ is purely deterministic and must — by the no-arbitrage principle — grow at the instantaneous risk-free rate $r$. The drift $\mu$ enters the picture only via $V_S \cdot \mu S\, dt$ in Itô's expansion of $dV$, and is exactly offset by the matching term $-\phi_t \mu S\, dt = -V_S \mu S\, dt$ from the short stock leg. Financially: replication eliminates the holder's exposure to whether the stock goes up or down on average. The option price therefore depends on the *magnitude* of random fluctuations ($\sigma$) and the risk-free funding rate ($r$), but not on the directional bet ($\mu$). Two market participants who disagree about whether the stock is "going up" or "going down" must nonetheless agree on the option's price, because both can hedge to the same risk-free outcome at the same cost.

---

**Problem 6.2 [Derivation].** *(The user's original example.)* Derive the Black-Scholes partial differential equation for a non-dividend-paying stock $S$ following $dS = \mu S\, dt + \sigma S\, dW$ under the real-world measure $\mathbb{P}$. State and justify the boundary conditions at $S = 0$ and as $S \to \infty$ for a European call.

**Solution.** *(Self-contained; this reproduces the full derivation from the chapter body, intended to be readable without reference to the surrounding text.)*

*Setup.* Work on a filtered probability space supporting a $\mathbb{P}$-Brownian motion $W$. The market contains a risk-free bond $B_t = e^{rt}$ with $dB_t = r B_t\, dt$ and a stock $S$ obeying

$$dS_t = \mu S_t\, dt + \sigma S_t\, dW_t.$$

::: where
- $\mu$ — real-world drift; $\sigma > 0$ — instantaneous volatility; $r$ — constant risk-free rate.
- $W_t$ — standard $\mathbb{P}$-Brownian motion.
:::

Let $V(S, t)$ be the time-$t$ no-arbitrage price of a European call with strike $K$ and maturity $T$. Assume $V \in C^{2, 1}\bigl((0, \infty) \times [0, T]\bigr)$.

*Replicating portfolio.* Consider the self-financing portfolio long one call, short $\phi_t$ shares of stock, with the residual held in the money-market account. Its value is

$$\Pi_t = V(S_t, t) - \phi_t S_t + \psi_t B_t, \qquad d\Pi_t = dV - \phi_t\, dS_t + \psi_t\, dB_t.$$

We will choose $\phi_t = V_S$ to make $\Pi_t$ instantaneously riskless.

*Step 1 — Itô on $V$.* Applying Itô's lemma and substituting $dS_t = \mu S\, dt + \sigma S\, dW_t$ with $(dS_t)^2 = \sigma^2 S^2\, dt$:

$$dV = \Bigl(V_t + \mu S V_S + \tfrac{1}{2} \sigma^2 S^2 V_{SS}\Bigr) dt + \sigma S V_S\, dW_t.$$

::: where
- $V_t, V_S, V_{SS}$ — partial derivatives of $V$ in $t$ and twice in $S$.
- $S = S_t$ — current spot.
- $\sigma S V_S\, dW_t$ — random component to be cancelled by the hedge.
:::

*Step 2 — Cancel $dW$.* With $\phi_t = V_S$, subtract $V_S\, dS_t = V_S \mu S\, dt + V_S \sigma S\, dW_t$:

$$dV - V_S\, dS_t = \Bigl(V_t + \tfrac{1}{2} \sigma^2 S^2 V_{SS}\Bigr) dt.$$

::: where
- The $\mu S V_S\, dt$ terms cancel; the $\sigma S V_S\, dW_t$ terms cancel.
- The right-hand side is purely deterministic — the hedge is locally riskless.
:::

*Step 3 — No-arbitrage growth.* The reduced portfolio $\Pi_t = V - V_S S$ is now locally riskless. By the no-arbitrage principle of Ch. 4, it must grow at the risk-free rate:

$$d\Pi_t = r \Pi_t\, dt = r(V - V_S S)\, dt.$$

::: where
- $r$ — risk-free rate at which any locally riskless self-financing portfolio must grow under no-arbitrage.
- $V - V_S S$ — current value of the delta-hedged portfolio.
:::

*Step 4 — Equate and rearrange.* Equating the two expressions for $d\Pi_t$ from Steps 2 and 3 and dividing by $dt$:

$$V_t + \tfrac{1}{2} \sigma^2 S^2 V_{SS} = r V - r V_S S \;\;\Longrightarrow\;\; \boxed{\,V_t + \tfrac{1}{2} \sigma^2 S^2 V_{SS} + r S V_S - r V = 0.\,}$$

::: where
- The boxed equation is the Black-Scholes PDE; $\mu$ does not appear.
- Valid on $(S, t) \in (0, \infty) \times [0, T)$.
:::

*Terminal condition.* At expiry, the call price equals its payoff:

$$C(S, T) = (S - K)^+.$$

*Boundary at $S = 0$.* The stock SDE has multiplicative coefficients $\mu S$ and $\sigma S$. If $S_{t_0} = 0$, then $dS_t = 0$ for all $t \ge t_0$, so $S$ is *absorbed* at the origin and $S_T = 0$ almost surely. The call's terminal payoff is then $(0 - K)^+ = 0$, certain. The time-$t$ value of a certain payoff of $0$ is $0$:

$$C(0, t) = 0 \quad \text{for all } t \in [0, T].$$

::: where
- The absorbing behavior is a structural feature of GBM with multiplicative coefficients vanishing at $S = 0$.
- The call has zero value at the origin because the stock cannot recover and the strike cannot be reached.
:::

*Boundary as $S \to \infty$.* For very large spot, the call is deep in-the-money, and exercise at $T$ is essentially certain. The terminal payoff $(S_T - K)^+$ converges to $S_T - K$. A static replication of the payoff $S_T - K$ is: long one share of stock (paying $S_T$ at $T$, costing $S$ today) and short $K e^{-r(T-t)}$ in the bond (paying $K$ at $T$, costing $K e^{-r(T-t)}$ today). The time-$t$ cost is $S - K e^{-r(T-t)}$, hence

$$C(S, t) \sim S - K e^{-r(T-t)} \quad \text{as } S \to \infty.$$

::: where
- The asymptote is the value of a *forward contract* on $S$ with delivery price $K$ at $T$ — a deep-ITM call replicates a forward.
- "$\sim$" — asymptotic ratio tends to $1$ as $S \to \infty$; the difference vanishes at the rate of the probability $\mathbb{P}(S_T < K)$.
:::

*Summary.* The Black-Scholes PDE with the call's terminal condition $C(S, T) = (S - K)^+$, boundary condition $C(0, t) = 0$, and asymptotic condition $C(S, t) \sim S - K e^{-r(T-t)}$ as $S \to \infty$ jointly determine the European call price uniquely. The closed-form solution is obtained in Ch. 7. $\square$

---

**Problem 6.3 [Computation].** Modify the derivation to include a continuous dividend yield $q$. State the resulting partial differential equation.

**Solution.** When the stock pays a continuous dividend yield $q$, the holder of one share receives dividend cash at rate $q S_t\, dt$. In the hedged portfolio $\Pi_t = V(S_t, t) - \phi_t S_t + \psi_t B_t$, the short stock position implies the *holder of the hedge* must *pay out* dividend cash at rate $q \phi_t S_t\, dt$. The self-financing condition becomes:

$$d\Pi_t = dV - \phi_t\, dS_t - q \phi_t S_t\, dt + \psi_t\, dB_t.$$

::: where
- $-q \phi_t S_t\, dt$ — dividend cash paid out by the short stock position, exiting the portfolio.
- All other quantities — as in the no-dividend case.
:::

*Repeat Steps 1-2.* Itô's lemma on $V$ gives, exactly as before,

$$dV - V_S\, dS_t = \Bigl(V_t + \tfrac{1}{2} \sigma^2 S^2 V_{SS}\Bigr) dt$$

(the dividend correction lives outside this calculation — it modifies the *portfolio* dynamics, not the Itô expansion of $V$). Choosing $\phi_t = V_S$ and including the dividend outflow:

$$d\Pi_t = \Bigl(V_t + \tfrac{1}{2} \sigma^2 S^2 V_{SS}\Bigr) dt - q V_S S\, dt.$$

::: where
- $\phi_t = V_S$ — hedge ratio, unchanged in form.
- $-q V_S S\, dt$ — dividend cash that the hedger must pay out at rate $q V_S S$, reducing the portfolio's growth.
:::

*Repeat Step 3 — no-arbitrage.* The reduced portfolio $\Pi_t = V - V_S S$ is locally riskless after the $dW$-cancellation and must still grow at the risk-free rate by no-arbitrage:

$$d\Pi_t = r(V - V_S S)\, dt.$$

*Equate.* Setting the two expressions for $d\Pi_t$ equal:

$$V_t + \tfrac{1}{2} \sigma^2 S^2 V_{SS} - q V_S S = r V - r V_S S,$$

which rearranges to

$$\boxed{\,V_t + \tfrac{1}{2} \sigma^2 S^2 V_{SS} + (r - q) S V_S - r V = 0.\,}$$

::: where
- $r - q$ — drift of $S$ under the risk-neutral measure when dividends are paid at rate $q$; the *net cost of carry*.
- $- r V$ — discount of the option value at the funding rate $r$, unchanged from the no-dividend case.
- $q = 0$ — recovers the standard Black-Scholes PDE of Section 4.
:::

*Boundary remark.* The boundary conditions also shift slightly. At $S = 0$ the stock is still absorbed (the coefficients $\mu S$ and $\sigma S$ vanish, dividends from zero stock are zero), so the call still satisfies $C(0, t) = 0$. As $S \to \infty$, however, the share used to replicate the payoff itself pays dividends at rate $q$, and one must hold only $e^{-q(T-t)}$ shares at time $t$ to grow into one share at $T$ via continuous dividend reinvestment. The deep-ITM call asymptote becomes

$$C(S, t) \sim S e^{-q(T-t)} - K e^{-r(T-t)} \quad \text{as } S \to \infty,$$

the value of a *dividend-adjusted* forward contract. $\square$
