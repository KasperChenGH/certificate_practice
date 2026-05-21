# Chapter 9 — The Greeks

## Goals

- Derive each of the five primary Greeks — Delta ($\Delta$), Gamma ($\Gamma$), Theta ($\Theta$), Vega ($\nu$), and Rho ($\rho$) — directly from the closed-form call and put prices $C$ and $P$ established in Ch. 7.
- Establish the key symmetry identity $S\varphi(d_1) = K e^{-r(T-t)} \varphi(d_2)$, which acts as the central algebraic lemma underlying every Greek derivation in this chapter.
- Verify PDE consistency: plug the closed-form Greeks into the Black-Scholes PDE written as $\Theta + rS\Delta + \tfrac{1}{2}\sigma^2 S^2 \Gamma = rV$ and confirm that it holds identically for the call.

## Prerequisites

- **Ch. 7** — the closed-form call price $C = S N(d_1) - K e^{-r(T-t)} N(d_2)$ and put price $P = K e^{-r(T-t)} N(-d_2) - S N(-d_1)$, together with the definitions of $d_1, d_2$, and put-call parity $C - P = S - K e^{-r(T-t)}$.
- **Basic calculus** — chain rule, product rule, and the fact that the derivative of $N(x)$ is the standard normal density $\varphi(x) = \tfrac{1}{\sqrt{2\pi}} e^{-x^2/2}$.

---

## The identity $S\varphi(d_1) = K e^{-r(T-t)} \varphi(d_2)$

This lemma appears in every Greek derivation. Establishing it once avoids repeated computation.

**Lemma.** $S\varphi(d_1) = K e^{-r(T-t)} \varphi(d_2)$.

::: where
- $S$ — current spot price of the underlying.
- $K$ — strike price.
- $r$ — continuously compounded risk-free rate.
- $T - t$ — time to expiry.
- $\varphi(x) = \tfrac{1}{\sqrt{2\pi}} e^{-x^2/2}$ — the standard normal probability density function.
- $d_1 = \dfrac{\ln(S/K) + (r + \sigma^2/2)(T-t)}{\sigma\sqrt{T-t}}$, $\quad d_2 = d_1 - \sigma\sqrt{T-t}$.
:::

**Proof.** We work with the ratio $\varphi(d_1)/\varphi(d_2)$. Since $\varphi(x) = \tfrac{1}{\sqrt{2\pi}} e^{-x^2/2}$,

$$\frac{\varphi(d_1)}{\varphi(d_2)} = \exp\!\Bigl(-\tfrac{1}{2}(d_1^2 - d_2^2)\Bigr).$$

We factor the exponent using the difference-of-squares identity:

$$d_1^2 - d_2^2 = (d_1 - d_2)(d_1 + d_2).$$

Since $d_2 = d_1 - \sigma\sqrt{T-t}$, we have $d_1 - d_2 = \sigma\sqrt{T-t}$. For the sum, write $d_1 + d_2 = 2d_1 - \sigma\sqrt{T-t}$. Substituting $d_1 = [\ln(S/K) + (r + \sigma^2/2)(T-t)]/[\sigma\sqrt{T-t}]$:

$$2d_1 - \sigma\sqrt{T-t} = \frac{2[\ln(S/K) + (r + \sigma^2/2)(T-t)]}{\sigma\sqrt{T-t}} - \sigma\sqrt{T-t}.$$

Combining over the common denominator $\sigma\sqrt{T-t}$:

$$2d_1 - \sigma\sqrt{T-t} = \frac{2\ln(S/K) + 2r(T-t) + \sigma^2(T-t) - \sigma^2(T-t)}{\sigma\sqrt{T-t}} = \frac{2\ln(S/K) + 2r(T-t)}{\sigma\sqrt{T-t}}.$$

Therefore,

$$d_1^2 - d_2^2 = \sigma\sqrt{T-t} \cdot \frac{2\ln(S/K) + 2r(T-t)}{\sigma\sqrt{T-t}} = 2\ln(S/K) + 2r(T-t).$$

So $\tfrac{1}{2}(d_1^2 - d_2^2) = \ln(S/K) + r(T-t)$. Substituting back:

$$\frac{\varphi(d_1)}{\varphi(d_2)} = \exp\!\Bigl(-\ln(S/K) - r(T-t)\Bigr) = \frac{K}{S} e^{-r(T-t)}.$$

Rearranging: $S\,\varphi(d_1) = K e^{-r(T-t)} \varphi(d_2)$. $\square$

---

## Delta

**Definition.** Delta measures the rate of change of the option price with respect to the spot price:

$$\Delta_C = \frac{\partial C}{\partial S}, \qquad \Delta_P = \frac{\partial P}{\partial S}.$$

::: where
- $C$ — call price; $P$ — put price; $S$ — current spot price.
- $\Delta_C > 0$: the call gains value as the spot rises. $\Delta_P < 0$: the put loses value as the spot rises.
- Delta is also the hedge ratio — holding $\Delta_C$ shares of stock and being short one call produces a locally risk-free portfolio (Ch. 6).
:::

**Theorem.** For a European call and put (no dividends):

$$\Delta_C = N(d_1), \qquad \Delta_P = N(d_1) - 1 = -N(-d_1).$$

::: where
- $N(\cdot)$ — cumulative standard normal distribution function, ranging in $(0, 1)$.
- $d_1$ — as defined in the lemma above.
- Both $\Delta_C \in (0,1)$ and $\Delta_P \in (-1, 0)$ for all valid parameter values.
- The relation $\Delta_C - \Delta_P = 1$ is the derivative of put-call parity $C - P = S - Ke^{-r(T-t)}$ with respect to $S$.
:::

**Proof.** Differentiate $C = S N(d_1) - K e^{-r(T-t)} N(d_2)$ with respect to $S$, applying the product rule and chain rule:

$$\Delta_C = N(d_1) + S \cdot \varphi(d_1) \cdot \frac{\partial d_1}{\partial S} - K e^{-r(T-t)} \cdot \varphi(d_2) \cdot \frac{\partial d_2}{\partial S}.$$

Since $d_1 = [\ln(S/K) + (r + \sigma^2/2)(T-t)]/[\sigma\sqrt{T-t}]$ and $d_2 = d_1 - \sigma\sqrt{T-t}$, both $d_1$ and $d_2$ depend on $S$ only through $\ln(S/K)$. Therefore:

$$\frac{\partial d_1}{\partial S} = \frac{\partial d_2}{\partial S} = \frac{1}{S \sigma \sqrt{T-t}}.$$

The two extra terms become:

$$S \cdot \varphi(d_1) \cdot \frac{1}{S\sigma\sqrt{T-t}} - K e^{-r(T-t)} \cdot \varphi(d_2) \cdot \frac{1}{S\sigma\sqrt{T-t}} = \frac{S\varphi(d_1) - K e^{-r(T-t)}\varphi(d_2)}{S\sigma\sqrt{T-t}}.$$

By the lemma, $S\varphi(d_1) = K e^{-r(T-t)} \varphi(d_2)$, so the numerator is zero. The extra terms cancel exactly, leaving:

$$\Delta_C = N(d_1). \quad \square$$

For the put, differentiate put-call parity $P = C - S + K e^{-r(T-t)}$ with respect to $S$:

$$\Delta_P = \Delta_C - 1 = N(d_1) - 1 = -N(-d_1). \quad \square$$

---

## Gamma

**Definition.** Gamma measures the rate of change of Delta with respect to the spot price, i.e., the second derivative of the option price with respect to $S$:

$$\Gamma = \frac{\partial^2 C}{\partial S^2} = \frac{\partial^2 P}{\partial S^2}.$$

::: where
- $\Gamma$ — the curvature of the option's price-spot relationship. High gamma means delta changes rapidly with $S$, so the hedge needs frequent rebalancing.
- $\Gamma$ is the same for a call and a put with the same parameters — taking the second derivative of parity $C - P = S - Ke^{-r(T-t)}$ gives $\Gamma_C - \Gamma_P = 0$.
- $\Gamma \geq 0$ always: options are convex functions of $S$.
:::

**Theorem.**

$$\Gamma = \frac{\varphi(d_1)}{S \sigma \sqrt{T-t}}.$$

::: where
- $\varphi(d_1)$ — the standard normal density evaluated at $d_1$.
- $S\sigma\sqrt{T-t}$ — a scale factor combining spot, volatility, and square-root time; it has the dimension of dollars times a pure number, so $\Gamma$ has units of $1/\$$ (delta change per dollar move in $S$).
:::

**Proof.** Differentiate $\Delta_C = N(d_1)$ with respect to $S$:

$$\Gamma = \frac{\partial}{\partial S} N(d_1) = \varphi(d_1) \cdot \frac{\partial d_1}{\partial S} = \varphi(d_1) \cdot \frac{1}{S\sigma\sqrt{T-t}}. \quad \square$$

---

## Theta

**Definition.** Theta measures the rate of change of the option price with respect to calendar time $t$ (not time-to-expiry $\tau = T - t$):

$$\Theta = \frac{\partial V}{\partial t}.$$

::: where
- $\Theta$ — represents time decay. As time passes ($t$ increases toward $T$), option value generally decreases for a long call or put, so $\Theta < 0$ in typical cases.
- Convention: often quoted per day by dividing by 365 (or 252 trading days). Here we state the per-year (per unit $t$) formula.
:::

**Formula (call, no dividends).**

$$\Theta_C = -\frac{S \varphi(d_1) \sigma}{2\sqrt{T-t}} - r K e^{-r(T-t)} N(d_2).$$

::: where
- The first term, $-S\varphi(d_1)\sigma/(2\sqrt{T-t})$, captures time decay through the volatility channel: as $T - t$ decreases, $d_1$ and $d_2$ become more extreme, reducing the uncertainty about whether the option expires in-the-money. This term is always negative.
- The second term, $-rK e^{-r(T-t)} N(d_2)$, captures the time value of the discounted strike. As $t$ increases toward $T$, the present value of $K$ rises toward $K$ itself, which disadvantages the call holder (who must pay $K$ at expiry). This term is also always negative.
- Both terms are negative, so $\Theta_C < 0$ always: long calls lose value with the passage of time, all else equal.
:::

**Derivation (sketch).** Differentiate $C = S N(d_1) - K e^{-r(T-t)} N(d_2)$ with respect to $t$, treating $T - t$ as the operative variable. Using $\partial(T-t)/\partial t = -1$, the chain rule yields contributions from three sources:

1. **The $N(d_1)$ term.** Since $d_1$ depends on $t$ through $\sqrt{T-t}$, we get $S\varphi(d_1) \cdot \partial d_1/\partial t$.

2. **The discount factor $e^{-r(T-t)}$.** Differentiating with respect to $t$ gives $+r e^{-r(T-t)}$, contributing $+rK e^{-r(T-t)} N(d_2)$.

3. **The $N(d_2)$ term.** Gives $-Ke^{-r(T-t)} \varphi(d_2) \cdot \partial d_2/\partial t$.

Now, $\partial d_1/\partial t$ and $\partial d_2/\partial t$ differ only by $-\sigma/(2\sqrt{T-t})$ (since $d_1 - d_2 = \sigma\sqrt{T-t}$, so $\partial d_1/\partial t - \partial d_2/\partial t = \sigma/(2\sqrt{T-t})$). The cross-terms involving $S\varphi(d_1)\partial d_1/\partial t$ and $K e^{-r(T-t)}\varphi(d_2)\partial d_2/\partial t$ cancel by the lemma (since $S\varphi(d_1) = K e^{-r(T-t)}\varphi(d_2)$ and $\partial d_1/\partial t = \partial d_2/\partial t$ up to the extra $\sigma/(2\sqrt{T-t})$ piece). After cancellation, the surviving piece from the $d_1, d_2$ time-dependence is:

$$S\varphi(d_1) \cdot \Bigl(-\frac{\sigma}{2\sqrt{T-t}}\Bigr) = -\frac{S\varphi(d_1)\sigma}{2\sqrt{T-t}}.$$

The discount factor's time derivative contributes the second term, but with a sign flip (since we are differentiating $e^{-r(T-t)}$ with respect to $t$, which gives $+r e^{-r(T-t)}$, and the $N(d_2)$ carries the negative sign from the put-side): combining yields $-rK e^{-r(T-t)} N(d_2)$. (Full details involve careful bookkeeping of the signs; the structural logic is as stated.)

**Put theta (similarly).** Differentiating $P = Ke^{-r(T-t)} N(-d_2) - S N(-d_1)$ or using put-call parity, the lemma-cancellation works identically and the discount term changes sign because $N(-d_2)$ replaces $N(d_2)$:

$$\Theta_P = -\frac{S \varphi(d_1) \sigma}{2\sqrt{T-t}} + r K e^{-r(T-t)} N(-d_2).$$

::: where
- The first term is identical to the call — the volatility-decay channel is symmetric.
- The second term is $+rK e^{-r(T-t)} N(-d_2)$ rather than negative: deep out-of-the-money puts have $N(-d_2) \approx 1$, and the accruing discount on the strike is a benefit to the put holder (the put pays $K - S_T$, and a smaller present value of $K$ received in the future is recovered). Puts can have positive theta when they are deep in-the-money.
:::

---

## Vega

**Definition.** Vega measures the rate of change of the option price with respect to the volatility parameter $\sigma$:

$$\nu = \frac{\partial V}{\partial \sigma}.$$

::: where
- $\nu$ (Greek letter "nu") — not a letter in the standard Greek alphabet for finance; the symbol $\nu$ is conventional.
- Vega is not a letter of the Greek alphabet, but it is grouped with the Greeks in market practice.
- $\nu > 0$ always for both calls and puts (long volatility positions): greater uncertainty in $S_T$ increases the expected value of either convex payoff.
:::

**Theorem.** Vega is the same for calls and puts:

$$\nu = S \varphi(d_1) \sqrt{T-t}.$$

::: where
- $S\varphi(d_1)$ — the spot price weighted by the standard normal density at $d_1$.
- $\sqrt{T-t}$ — the square-root-of-time factor; vega grows with time to expiry because more time means more scope for volatility to act.
- $\nu_C = \nu_P$: this follows immediately from put-call parity $C - P = S - Ke^{-r(T-t)}$, which is independent of $\sigma$, so $\partial C/\partial\sigma = \partial P/\partial\sigma$.
:::

**Proof.** Differentiate $C = S N(d_1) - K e^{-r(T-t)} N(d_2)$ with respect to $\sigma$:

$$\nu = S \cdot \varphi(d_1) \cdot \frac{\partial d_1}{\partial \sigma} - K e^{-r(T-t)} \cdot \varphi(d_2) \cdot \frac{\partial d_2}{\partial \sigma}.$$

We compute the $\sigma$-derivatives of $d_1$ and $d_2$. Write $d_1 = [\ln(S/K) + r(T-t)]/[\sigma\sqrt{T-t}] + \sigma\sqrt{T-t}/2$ and $d_2 = d_1 - \sigma\sqrt{T-t}$. Then:

$$\frac{\partial d_1}{\partial \sigma} = -\frac{\ln(S/K) + r(T-t)}{\sigma^2\sqrt{T-t}} + \frac{\sqrt{T-t}}{2}, \qquad \frac{\partial d_2}{\partial \sigma} = \frac{\partial d_1}{\partial \sigma} - \sqrt{T-t}.$$

The key observation is:

$$\frac{\partial d_1}{\partial \sigma} - \frac{\partial d_2}{\partial \sigma} = \sqrt{T-t}.$$

Group the two terms in $\nu$ as follows:

$$\nu = S \varphi(d_1) \cdot \frac{\partial d_1}{\partial \sigma} - K e^{-r(T-t)} \varphi(d_2) \cdot \frac{\partial d_2}{\partial \sigma}.$$

By the lemma, $S\varphi(d_1) = K e^{-r(T-t)}\varphi(d_2)$; call this common value $A$. Then:

$$\nu = A \cdot \frac{\partial d_1}{\partial \sigma} - A \cdot \frac{\partial d_2}{\partial \sigma} = A \left(\frac{\partial d_1}{\partial \sigma} - \frac{\partial d_2}{\partial \sigma}\right) = A \cdot \sqrt{T-t} = S\varphi(d_1)\sqrt{T-t}. \quad \square$$

The cancellation works because the lemma makes the two $\varphi$ terms equal, and the difference $\partial d_1/\partial\sigma - \partial d_2/\partial\sigma = \sqrt{T-t}$ is simple.

---

## Rho

**Theorem.** The rho of a European call and put (no dividends) are:

$$\rho_C = K(T-t) e^{-r(T-t)} N(d_2), \qquad \rho_P = -K(T-t) e^{-r(T-t)} N(-d_2).$$

::: where
- $\rho = \partial V / \partial r$ — the sensitivity of the option price to the risk-free rate.
- $\rho_C > 0$: higher interest rates raise call prices (the cost of the discounted strike falls, benefiting the call holder). $\rho_P < 0$: higher rates lower put prices (the present value of the cash receipt $K$ at expiry falls).
- $K(T-t)$ — rho scales with the dollar amount of the strike and the time to expiry.
- $e^{-r(T-t)} N(d_2)$ — the risk-neutral probability that the option expires in-the-money, discounted.
:::

**Sketch.** Differentiate $C = SN(d_1) - Ke^{-r(T-t)}N(d_2)$ with respect to $r$. There are three contributions:

$$\rho_C = S\varphi(d_1)\frac{\partial d_1}{\partial r} - Ke^{-r(T-t)}N(d_2)\cdot(-(-(T-t))) - Ke^{-r(T-t)}\varphi(d_2)\frac{\partial d_2}{\partial r}.$$

More carefully: differentiating $Ke^{-r(T-t)} N(d_2)$ with respect to $r$ gives $-K(T-t)e^{-r(T-t)}N(d_2) + Ke^{-r(T-t)}\varphi(d_2)\partial d_2/\partial r$. Since $\partial d_1/\partial r = \partial d_2/\partial r = \sqrt{T-t}/\sigma$ (only the $r(T-t)$ term in $d_1$ depends on $r$), the terms $S\varphi(d_1)\partial d_1/\partial r$ and $Ke^{-r(T-t)}\varphi(d_2)\partial d_2/\partial r$ cancel by the lemma exactly as in the delta derivation. What remains is:

$$\rho_C = K(T-t)e^{-r(T-t)} N(d_2). \quad \square$$

For the put, differentiating $P = Ke^{-r(T-t)}N(-d_2) - SN(-d_1)$ or using parity gives $\rho_P = \rho_C - K(T-t)e^{-r(T-t)} = -K(T-t)e^{-r(T-t)}N(-d_2)$.

---

## PDE consistency

The Black-Scholes-Merton PDE in the notation of Ch. 6, written in terms of the Greeks, takes the compact form:

$$\Theta + rS\Delta + \tfrac{1}{2}\sigma^2 S^2 \Gamma = rV.$$

::: where
- $\Theta = \partial V/\partial t$ — time decay.
- $\Delta = \partial V/\partial S$ — delta, the first spatial derivative.
- $\Gamma = \partial^2 V/\partial S^2$ — gamma, the second spatial derivative.
- $V$ — the option price itself (call or put).
- The PDE holds for any twice-differentiable function $V(S, t)$ that prices a no-arbitrage derivative in the BSM framework.
:::

We verify this identity for the European call by direct substitution of the closed-form Greeks:

$$\Theta_C + rS\Delta_C + \tfrac{1}{2}\sigma^2 S^2 \Gamma = rC.$$

Substituting the formulas derived above:

$$\underbrace{-\frac{S\varphi(d_1)\sigma}{2\sqrt{T-t}} - rKe^{-r(T-t)}N(d_2)}_{\Theta_C} + rS\underbrace{N(d_1)}_{\Delta_C} + \tfrac{1}{2}\sigma^2 S^2 \cdot \underbrace{\frac{\varphi(d_1)}{S\sigma\sqrt{T-t}}}_{\Gamma}.$$

Simplify the last term:

$$\tfrac{1}{2}\sigma^2 S^2 \cdot \frac{\varphi(d_1)}{S\sigma\sqrt{T-t}} = \frac{S\varphi(d_1)\sigma}{2\sqrt{T-t}}.$$

Now collect the two terms involving $S\varphi(d_1)$:

$$-\frac{S\varphi(d_1)\sigma}{2\sqrt{T-t}} + \frac{S\varphi(d_1)\sigma}{2\sqrt{T-t}} = 0.$$

These cancel exactly. The PDE reduces to:

$$-rKe^{-r(T-t)}N(d_2) + rSN(d_1) = rC.$$

Dividing through by $r$ (assuming $r > 0$):

$$SN(d_1) - Ke^{-r(T-t)}N(d_2) = C.$$

This is precisely the closed-form call formula from Ch. 7. The PDE is satisfied identically. $\checkmark$

---

## Practice

**Problem 9.1 [Conceptual].** Why is $\nu_C = \nu_P$ but $\Delta_C \neq \Delta_P$? What is the financial intuition?

**Solution.** The equality $\nu_C = \nu_P$ follows algebraically from put-call parity: $C - P = S - Ke^{-r(T-t)}$. The right-hand side contains no $\sigma$, so differentiating with respect to $\sigma$ gives $\partial C/\partial\sigma - \partial P/\partial\sigma = 0$, hence $\nu_C = \nu_P$. Financially, both calls and puts are convex functions of $S_T$: a call payoff $(S_T - K)^+$ and a put payoff $(K - S_T)^+$ are each piecewise linear with a "kink." By Jensen's inequality, greater uncertainty in $S_T$ (higher $\sigma$) increases the expected value of any convex payoff. This benefit is symmetric for calls and puts — they are related by parity and share the same convexity structure. Vega captures this shared sensitivity to dispersion.

Delta, however, measures directional sensitivity, not dispersion sensitivity. The call gains when $S$ rises ($\Delta_C = N(d_1) > 0$) and the put loses when $S$ rises ($\Delta_P = N(d_1) - 1 < 0$). The parity relationship gives $\Delta_C - \Delta_P = 1$ (the right-hand side $S - Ke^{-r(T-t)}$ has derivative 1 with respect to $S$). The convexity argument does not distinguish the direction of $S$ movements; the delta argument does.

---

**Problem 9.2 [Derivation].** Prove the identity $S\varphi(d_1) = Ke^{-r(T-t)}\varphi(d_2)$.

**Solution.** This is the content of the lemma in the section "The identity $S\varphi(d_1) = Ke^{-r(T-t)}\varphi(d_2)$" above. We reproduce the proof:

Starting from $\varphi(d_1)/\varphi(d_2) = \exp(-\tfrac{1}{2}(d_1^2 - d_2^2))$, factor the exponent as $(d_1 - d_2)(d_1 + d_2)$. With $d_1 - d_2 = \sigma\sqrt{T-t}$ and $d_1 + d_2 = 2d_1 - \sigma\sqrt{T-t}$, substitute $d_1 = [\ln(S/K) + (r+\sigma^2/2)(T-t)]/[\sigma\sqrt{T-t}]$ to obtain $d_1 + d_2 = [2\ln(S/K) + 2r(T-t)]/[\sigma\sqrt{T-t}]$. Then $d_1^2 - d_2^2 = 2\ln(S/K) + 2r(T-t)$, so:

$$\frac{\varphi(d_1)}{\varphi(d_2)} = e^{-\ln(S/K) - r(T-t)} = \frac{K}{S}e^{-r(T-t)}.$$

Rearranging: $S\varphi(d_1) = Ke^{-r(T-t)}\varphi(d_2)$. $\square$

---

**Problem 9.3 [Computation].** ATM call: $S = K = 100$, $T - t = 0.25$, $r = 0.05$, $\sigma = 0.20$. Compute $\Delta$, $\Gamma$, $\Theta$ (per year), $\nu$ (per unit $\sigma$ change), and $\rho$.

**Solution.** From Ch. 7 Problem 7.3, $d_1 = 0.175$ and $d_2 = 0.075$, and $\varphi(0.175) \approx 0.3927$. We also use $N(0.175) \approx 0.5694$, $N(0.075) \approx 0.5299$, and $e^{-0.05 \times 0.25} = e^{-0.0125} \approx 0.9876$.

**Delta:**

$$\Delta_C = N(d_1) = N(0.175) \approx 0.5694.$$

The call has a delta of approximately $0.57$: for each $\$1$ rise in $S$, the call gains about $\$0.57$.

**Gamma:**

$$\Gamma = \frac{\varphi(d_1)}{S\sigma\sqrt{T-t}} = \frac{0.3927}{100 \times 0.20 \times \sqrt{0.25}} = \frac{0.3927}{100 \times 0.20 \times 0.5} = \frac{0.3927}{10} = 0.03927 \text{ per share}.$$

For each $\$1$ move in $S$, the delta changes by approximately $0.039$.

**Theta (per year):**

$$\Theta_C = -\frac{S\varphi(d_1)\sigma}{2\sqrt{T-t}} - rKe^{-r(T-t)}N(d_2).$$

First term:

$$-\frac{100 \times 0.3927 \times 0.20}{2 \times 0.5} = -\frac{7.854}{1.0} = -7.854.$$

Second term:

$$-0.05 \times 100 \times 0.9876 \times 0.5299 = -0.05 \times 52.33 = -2.616.$$

Combining:

$$\Theta_C \approx -7.854 - 2.616 = -10.47 \text{ per year.}$$

Per day (divide by 365): $\Theta_C \approx -10.47/365 \approx -\$0.029$ per day.

**Vega (per unit change in $\sigma$):**

$$\nu = S\varphi(d_1)\sqrt{T-t} = 100 \times 0.3927 \times 0.5 = 19.64.$$

Per 1% change in volatility (multiply by 0.01): $\nu \approx \$0.196$ per 1% vol move.

**Rho (per unit change in $r$):**

$$\rho_C = K(T-t)e^{-r(T-t)}N(d_2) = 100 \times 0.25 \times 0.9876 \times 0.5299 \approx 13.08.$$

Per 1% change in the interest rate (multiply by 0.01): $\rho_C \approx \$0.131$ per 1% rate move.

**Summary table:**

| Greek | Formula | Value |
|-------|---------|-------|
| $\Delta_C$ | $N(d_1)$ | $0.5694$ |
| $\Gamma$ | $\varphi(d_1)/(S\sigma\sqrt{T-t})$ | $0.03927$ per $\$$ |
| $\Theta_C$ | $-S\varphi(d_1)\sigma/(2\sqrt{T-t}) - rKe^{-r(T-t)}N(d_2)$ | $-10.47$ per year |
| $\nu$ | $S\varphi(d_1)\sqrt{T-t}$ | $19.64$ per unit $\sigma$ |
| $\rho_C$ | $K(T-t)e^{-r(T-t)}N(d_2)$ | $13.08$ per unit $r$ |
