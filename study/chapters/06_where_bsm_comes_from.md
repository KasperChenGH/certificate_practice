# Chapter 6 — Where BSM Comes From

## 6.1 The Setup

We know the Black-Scholes formula from Chapter 5, but where does it come from? This chapter tells the story without requiring stochastic calculus proofs. The goal is to understand the **logic** — why the formula must take the form it does.

The option price $V(S, t)$ depends on two things: the current stock price $S$ and the current time $t$. As the stock price wiggles around randomly, the option price moves with it. The question is: can we figure out a deterministic rule — a partial differential equation — that $V$ must satisfy?

The answer is yes, and the key idea is **delta hedging.**


## 6.2 The Delta Hedging Argument

Imagine you have sold a call option and want to eliminate your risk. Here is the recipe:

1. **Hold the option** (value $V$).
2. **Short $\Delta$ shares of stock**, where $\Delta = \partial V / \partial S$ (the option's sensitivity to the stock price).

The combined portfolio is:

$$\Pi = V - \Delta\, S$$

::: where
- $\Pi$ — hedged portfolio value
- $V$ — option price, $V(S,t)$
- $\Delta$ — option delta, $\partial V/\partial S$
- $S$ — stock price
:::

**Why does this work?** If the stock moves by a small amount $dS$, the option moves by approximately $\Delta\, dS$ (that is the definition of delta). But we are short $\Delta$ shares, so the stock position also moves by $-\Delta\, dS$. The two effects cancel:

$$d\Pi \approx dV - \Delta\, dS \approx 0 \quad \text{(to first order in } dS\text{)}$$

The portfolio is **instantaneously risk-free**. It does not care whether the stock goes up or down — the hedge absorbs the directional move.


## 6.3 The Black-Scholes PDE

Since the hedged portfolio is risk-free, it must earn the risk-free rate. Working through the details (accounting for both the first-order and second-order effects of the stock's random motion), one arrives at the **Black-Scholes partial differential equation (PDE):**

$$\frac{\partial V}{\partial t} + \frac{1}{2}\,\sigma^2\, S^2\, \frac{\partial^2 V}{\partial S^2} + r\, S\, \frac{\partial V}{\partial S} - r\, V = 0$$

::: where
- $\sigma$ — stock volatility (annualized)
- $r$ — risk-free rate
:::

This equation holds for **any** European derivative on the stock, not just calls and puts. The payoff at expiry determines which specific solution you get.


## 6.4 Term-by-Term Interpretation

Each term in the PDE has a clear financial meaning. Think of the equation as a **budget constraint** — it says the option's total rate of return, when delta-hedged, must equal the risk-free rate.

**Term 1: $\partial V / \partial t$ — Time decay (Theta)**

Even if the stock price does not move, the option's value changes simply because time passes and expiry draws closer. For a vanilla option, this is usually negative — the option loses value as time erodes. This is the "theta bleed" that option sellers collect.

**Term 2: $\frac{1}{2} \sigma^2 S^2\, \partial^2 V / \partial S^2$ — The convexity / gamma effect**

This is the most subtle and important term. The option's payoff is curved (convex for a long call or put), so random stock fluctuations actually **help** the option holder on average. Here is an analogy:

> Imagine you are standing at the bottom of a bowl. If someone randomly pushes you left or right, you end up higher on the bowl's wall either way. Convexity means random shocks help you — you gain more from favorable moves than you lose from unfavorable ones.

Mathematically, $\partial^2 V / \partial S^2$ is the **gamma** — the curvature of the option's price. When gamma is positive (long options), this term is positive, meaning random fluctuations add value. The factor $\sigma^2$ captures how large the fluctuations are, and $S^2$ scales them to the stock's price level.

**Term 3: $r\, S\, \partial V / \partial S$ — Risk-neutral drift**

In the risk-neutral world, the stock grows at rate $r$ (not $\mu$). This term accounts for that drift's effect on the option's value through its delta.

**Term 4: $-r\, V$ — Funding cost**

The hedged portfolio is worth $V$ and earns the risk-free rate. This term represents the cost of financing the position — you "pay" $rV$ per unit time to hold it. Alternatively, it is the discounting effect: future values are worth less today.

**The PDE as a balance equation:** The option's time decay (Term 1) plus the benefit from convexity (Term 2) plus the risk-neutral growth effect (Term 3) must exactly equal the funding cost (Term 4). If the equation did not balance, there would be an arbitrage opportunity.


## 6.5 Why $\mu$ Disappears

This is worth emphasizing because it is the single most important insight in derivatives pricing.

The stock's real-world drift $\mu$ — the expected return investors demand for holding risky stock — appears nowhere in the PDE. Why?

**Because delta hedging eliminates it.** The hedge portfolio $\Pi = V - \Delta S$ cancels the first-order exposure to stock moves. The $\mu$ term in the stock's dynamics ($\mu S\, dt$) shows up in both $dV$ (through delta) and $\Delta\, dS$, and they cancel exactly. What remains is only the **second-order** effect of randomness, which depends on $\sigma^2$, not $\mu$.

Practically: two traders — one bullish, one bearish — who agree on the stock's volatility will compute the same option price. Their disagreement about $\mu$ is irrelevant because both can hedge away the directional bet.


## 6.6 Boundary Conditions

The PDE alone is not enough; we need **boundary conditions** to pin down which specific option we are pricing. For a European call with strike $K$ and expiry $T$:

**At expiry ($t = T$):**

$$V(S, T) = \max(S - K,\; 0)$$

This is the call's payoff — you exercise if $S > K$ and receive $S - K$, otherwise the call expires worthless.

**At $S = 0$ (stock is worthless):**

$$V(0, t) = 0 \quad \text{for all } t$$

If the stock hits zero, it stays at zero (under the lognormal model, zero is an absorbing barrier). A call on a worthless stock is worthless.

**As $S \to \infty$ (stock is extremely valuable):**

$$V(S, t) \;\to\; S - K\,e^{-r(T - t)} \quad \text{as } S \to \infty$$

::: where
- $K$ — strike price
- $T - t$ — time remaining to expiry
:::

When the stock is enormously high, exercise is virtually certain. The call behaves like a forward contract: you will receive $S$ and pay $K$ at time $T$. The present value of that is $S - Ke^{-r(T-t)}$. (The stock term is already $S$ because you could buy the stock today and hold it.)


## 6.7 Risk-Neutral Pricing: The Probabilistic Interpretation

Here is a beautiful fact: solving the Black-Scholes PDE with the call's boundary conditions is **mathematically equivalent** to computing an expected value:

$$V(S, t) = e^{-r(T-t)}\, \mathbb{E}^Q\!\big[\max(S_T - K,\, 0)\big]$$

::: where
- $\mathbb{E}^Q[\cdot]$ — expectation under risk-neutral measure
- $S_T$ — stock price at expiry
:::

Under the risk-neutral measure, the stock price at expiry is log-normally distributed:

$$\ln S_T \sim \mathcal{N}\!\Big(\ln S + (r - \sigma^2/2)(T-t),\;\; \sigma^2(T-t)\Big)$$

This connects everything back to the binomial tree in Chapter 4. In the tree, we computed the discounted expected payoff using risk-neutral probabilities. In continuous time, we do the same — the "probabilities" are determined by the log-normal distribution with drift $r$. The PDE and the expectation are two sides of the same coin.


## 6.8 How the BSM Formula Solves the PDE

We will not grind through every line of algebra, but here is the roadmap:

**Step 1 — Change of variables.** Define $\tau = T - t$ (time remaining), and substitute $x = \ln S$. This turns the Black-Scholes PDE into the classical **heat equation** (the same PDE that governs how temperature diffuses through a metal bar). The coefficients become constant, and the equation becomes:

$$\frac{\partial u}{\partial \tau} = \frac{1}{2}\sigma^2 \frac{\partial^2 u}{\partial x^2} + \text{(first-order terms absorbed by further substitution)}$$

**Step 2 — Solve via Gaussian integral.** The heat equation has a well-known solution: convolve the boundary condition (the payoff) with a Gaussian kernel. The payoff $\max(e^x - K, 0)$ is piecewise, so the integral splits at $x = \ln K$. Each piece evaluates to a term involving $N(\cdot)$.

**Step 3 — Undo the substitution.** Translating back to the original variables $S$ and $t$, you recover:

$$C = S\, N(d_1) - K\,e^{-r(T-t)}\, N(d_2)$$

with $d_1$ and $d_2$ as defined in Chapter 5. The formula is not a lucky guess — it is the unique solution to the PDE with the call's boundary conditions.

The fact that the heat equation appears is no accident. Diffusion of heat and diffusion of a stock's log-price are governed by the same mathematics. Fischer Black, Myron Scholes, and Robert Merton recognized this connection in the early 1970s.


## 6.9 The Big Picture

Let us step back and trace the logical chain:

1. **No-arbitrage** (Chapter 4) requires that a hedged portfolio earns the risk-free rate.
2. **Delta hedging** turns this economic principle into the **Black-Scholes PDE** — a deterministic equation that all European options must satisfy.
3. The PDE is equivalent to **risk-neutral pricing**: computing the discounted expected payoff under a world where everything drifts at rate $r$.
4. For a European call, the expected value integral evaluates to the **Black-Scholes formula** (Chapter 5).

Each step builds on the previous one. The formula is not an empirical fit — it is a logical consequence of the no-arbitrage assumption, the ability to trade continuously, and the lognormal stock model.


## Practice

::: problem [Conceptual]
**Problem 6.1.** A colleague says: "The Black-Scholes formula must be wrong because it assumes investors are risk-neutral, but in reality investors are risk-averse." Explain why this criticism is misguided.

::: solution
**Solution.** The Black-Scholes formula does **not** assume investors are risk-neutral. It assumes only that arbitrage is impossible and that the stock can be traded continuously. The "risk-neutral" probabilities are a mathematical convenience, not a claim about investor preferences. The formula is derived by **replication**: since the option's payoff can be exactly replicated by trading the stock and the bond, the option's price must equal the cost of the replicating portfolio — regardless of anyone's risk preferences. Risk-neutral pricing gives the same answer as replication, but is computationally easier. It works precisely because hedging eliminates risk, making the investor's attitude toward risk irrelevant.
:::
:::

::: problem [Computation]
**Problem 6.2.** Verify that the BSM call formula satisfies the boundary condition as $S \to \infty$. That is, show that when $S$ is very large, $C(S, t) \to S - K e^{-r(T-t)}$.

::: solution
**Solution.** As $S \to \infty$, the ratio $S/K \to \infty$, so $\ln(S/K) \to +\infty$.

Looking at $d_1$:

$$d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)(T-t)}{\sigma\sqrt{T-t}} \;\to\; +\infty$$

And since $d_2 = d_1 - \sigma\sqrt{T-t}$, we also have $d_2 \to +\infty$.

As $d \to +\infty$, $N(d) \to 1$. Therefore:

$$C = S\,N(d_1) - K e^{-r(T-t)}\,N(d_2) \;\to\; S \cdot 1 - K e^{-r(T-t)} \cdot 1 = S - K e^{-r(T-t)}$$

This confirms the boundary condition: when the stock price is enormously high, the call's value approaches the forward value $S - Ke^{-r(T-t)}$. Exercise is virtually certain, so the call behaves like a prepaid forward contract.
:::
:::

::: problem [Conceptual]
**Problem 6.3.** The Black-Scholes PDE contains the term $\frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2}$. Explain in plain language what this term represents and why it is positive for a long call position.

::: solution
**Solution.** This term captures the **gamma effect** — the benefit (or cost) that random stock fluctuations create for a non-linear position.

A long call has positive gamma ($\partial^2 V / \partial S^2 > 0$) because its payoff is convex: the price curve bends upward. When the stock jumps up, the call gains more value than it loses when the stock drops by the same amount. On average, random fluctuations help the call holder.

The size of this benefit depends on:
- $\sigma^2$: larger volatility means larger random fluctuations, amplifying the convexity benefit.
- $S^2$: the dollar magnitude of the stock's moves scales with its price level.
- $\partial^2 V / \partial S^2$: the curvature of the option price — how non-linear the option is at the current stock price.

This gamma benefit is not free. It is exactly offset by **theta** — the time decay of the option. The PDE tells us that the time-decay cost equals the expected gamma benefit plus the drift and discounting terms. For a delta-hedged position, the gamma gains and theta losses balance out so that the net return is the risk-free rate.
:::
:::
