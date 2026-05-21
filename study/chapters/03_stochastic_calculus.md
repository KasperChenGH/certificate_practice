# Chapter 3 — Stochastic Calculus

This chapter is a terse — but fully rigorous — review of the stochastic-calculus machinery used in Chapters 6, 7, and 8. Brownian motion is defined, its quadratic variation is computed in $L^2$, the Itô integral is sketched, Itô's lemma is stated and proved, and the geometric Brownian motion SDE is solved in closed form. The chapter closes with the statement of Girsanov's theorem, which will drive the construction of the risk-neutral measure in Chapter 8. The audience is assumed to have graduate-level measure-theoretic probability; nothing here is built from scratch.

## Goals

- Define Brownian motion and recall its defining properties, together with the Lévy characterization that we will reuse to verify that processes built by Girsanov are themselves Brownian motions.
- Prove that the quadratic variation of Brownian motion over $[0, t]$ converges to $t$ in $L^2$, the rigorous content of the algebraic identity $(dW_t)^2 = dt$.
- Sketch the construction of the Itô integral and state its isometry and martingale property.
- State and **prove** Itô's lemma for $C^{1, 2}$ functions of a continuous Itô process — this is the keystone result of the chapter and the engine of the Black-Scholes PDE derivation in Chapter 6.
- Solve the geometric-Brownian-motion SDE in closed form and connect the result to the lognormal expected-payoff theorem of Chapter 2.
- State Girsanov's theorem with the explicit Radon-Nikodym derivative and the Novikov integrability condition.

## Prerequisites

Chapter 2 (probability space, filtration, conditional expectation, normal and lognormal distributions); Lebesgue integration at the level of any standard graduate real-analysis text; familiarity with martingales in continuous time, at the level of Shreve, *Stochastic Calculus for Finance II*, Chapters 1–3.

## Brownian motion

### Definition

A **standard Brownian motion** on the filtered probability space $(\Omega, \mathcal{F}, \mathbb{P}, \{\mathcal{F}_t\}_{t \ge 0})$ is a continuous $\mathcal{F}_t$-adapted process $\{W_t\}_{t \ge 0}$ satisfying

- $W_0 = 0$ almost surely;
- for $0 \le s < t$, the increment $W_t - W_s$ is independent of $\mathcal{F}_s$;
- $W_t - W_s \sim \mathcal{N}(0, t - s)$.

::: where
- $(\Omega, \mathcal{F}, \mathbb{P})$ — underlying probability space
- $\{\mathcal{F}_t\}_{t \ge 0}$ — filtration carrying the information available by time $t$
- $W_t$ — value of the Brownian motion at time $t$, an $\mathcal{F}_t$-measurable real-valued random variable
- $t, s$ — time indices with $0 \le s < t$
- $W_t - W_s$ — increment over $[s, t]$, independent of the information $\mathcal{F}_s$
- $\mathcal{N}(0, t - s)$ — normal distribution with mean $0$ and variance $t - s$
- $\mathbb{P}$ — probability measure under which the increments are normal
:::

### Remark (existence)

Existence is non-trivial — Brownian motion is the path-continuous version of an uncountable family of jointly Gaussian random variables. The standard reference construction is due to Wiener (1923); we cite Shreve Vol. 2 §3.3 (or Karatzas-Shreve §2.2) and proceed.

### Theorem (Lévy characterization)

A continuous $\mathcal{F}_t$-adapted process $\{M_t\}_{t \ge 0}$ with $M_0 = 0$ is a standard Brownian motion **if and only if** both $M_t$ and $M_t^2 - t$ are $\mathcal{F}_t$-martingales.

::: where
- $M_t$ — candidate process, continuous and $\mathcal{F}_t$-adapted
- $M_t^2 - t$ — the compensated square, a martingale iff $[M, M]_t = t$
- $\mathcal{F}_t$-martingale — adapted process whose conditional expectation given $\mathcal{F}_s$ equals its time-$s$ value, for $s \le t$
:::

This is a deep result; we cite Shreve Vol. 2 §4.6 (or Karatzas-Shreve §3.3) for the proof, which goes through the exponential martingale and the uniqueness of characteristic functions. The theorem will be used in Chapter 8 to verify that the process produced by Girsanov is indeed a Brownian motion under the new measure.

## Quadratic variation

### Definition

For a partition $\Pi = \{0 = t_0 < t_1 < \cdots < t_n = t\}$ of $[0, t]$ with **mesh** $\|\Pi\| = \max_{0 \le i \le n-1} (t_{i+1} - t_i)$, the **quadratic variation** of $W$ over $\Pi$ is the random variable
$$Q_\Pi(W; t) = \sum_{i = 0}^{n - 1} \big(W_{t_{i+1}} - W_{t_i}\big)^2.$$

::: where
- $\Pi$ — partition of $[0, t]$, an ordered finite set of breakpoints
- $t_i$ — the $i$-th breakpoint, with $t_0 = 0$ and $t_n = t$
- $n$ — number of subintervals in the partition
- $\|\Pi\|$ — mesh of the partition, the longest subinterval length
- $W_{t_i}$ — value of $W$ at the breakpoint $t_i$
- $Q_\Pi(W; t)$ — partition-dependent quadratic variation of $W$ on $[0, t]$
:::

### Theorem (Quadratic variation of Brownian motion)

As $\|\Pi\| \to 0$,
$$Q_\Pi(W; t) \xrightarrow{L^2} t,$$
that is, $\mathbb{E}\big[(Q_\Pi(W; t) - t)^2\big] \to 0$.

::: where
- $Q_\Pi(W; t)$ — quadratic variation of $W$ over the partition $\Pi$
- $t$ — terminal time, deterministic
- $L^2$ — convergence in mean square, $\|X_n - X\|_2 \to 0$
- $\mathbb{E}\big[(Q_\Pi(W; t) - t)^2\big]$ — mean-square distance between $Q_\Pi$ and $t$
:::

### Proof

Let $\Delta W_i = W_{t_{i+1}} - W_{t_i}$ and $\Delta t_i = t_{i+1} - t_i$. By the definition of Brownian motion, $\Delta W_i \sim \mathcal{N}(0, \Delta t_i)$ and the increments $\{\Delta W_i\}_{i = 0}^{n - 1}$ are mutually independent.

**Step 1: mean of each squared increment.** Since $\Delta W_i \sim \mathcal{N}(0, \Delta t_i)$,
$$\mathbb{E}[\Delta W_i^2] = \operatorname{Var}(\Delta W_i) = \Delta t_i.$$

**Step 2: variance of each squared increment.** Standardizing, write $\Delta W_i = \sqrt{\Delta t_i}\, Z_i$ with $Z_i \sim \mathcal{N}(0, 1)$. Then $\Delta W_i^2 = \Delta t_i \cdot Z_i^2$ and $Z_i^2 \sim \chi^2_1$, which has variance $2$. Therefore
$$\operatorname{Var}(\Delta W_i^2) = (\Delta t_i)^2 \cdot \operatorname{Var}(Z_i^2) = 2 (\Delta t_i)^2.$$

::: where
- $\Delta W_i$ — Brownian increment over $[t_i, t_{i+1}]$, $\sim \mathcal{N}(0, \Delta t_i)$
- $\Delta t_i = t_{i+1} - t_i$ — length of the $i$-th subinterval
- $Z_i$ — standardized increment, $Z_i \sim \mathcal{N}(0, 1)$
- $\chi^2_1$ — chi-squared distribution with one degree of freedom, $\mathbb{E}[\chi^2_1] = 1$, $\operatorname{Var}(\chi^2_1) = 2$
:::

**Step 3: mean of $Q_\Pi$.** Summing,
$$\mathbb{E}[Q_\Pi(W; t)] = \sum_{i = 0}^{n - 1} \mathbb{E}[\Delta W_i^2] = \sum_{i = 0}^{n - 1} \Delta t_i = t.$$

**Step 4: variance of $Q_\Pi$.** By independence of the increments,
$$\operatorname{Var}\!\big(Q_\Pi(W; t)\big) = \sum_{i = 0}^{n - 1} \operatorname{Var}(\Delta W_i^2) = \sum_{i = 0}^{n - 1} 2 (\Delta t_i)^2 \le 2 \|\Pi\| \sum_{i = 0}^{n - 1} \Delta t_i = 2 \|\Pi\| \cdot t.$$
As $\|\Pi\| \to 0$, the bound $2 \|\Pi\| \cdot t \to 0$.

**Step 5: combine.** Since $\mathbb{E}[Q_\Pi(W; t)] = t$ exactly and $\operatorname{Var}(Q_\Pi(W; t)) \to 0$,
$$\mathbb{E}\big[(Q_\Pi(W; t) - t)^2\big] = \operatorname{Var}(Q_\Pi(W; t)) + \big(\mathbb{E}[Q_\Pi(W; t)] - t\big)^2 = \operatorname{Var}(Q_\Pi(W; t)) \to 0.$$
Hence $Q_\Pi(W; t) \to t$ in $L^2$. $\blacksquare$

::: where
- $\Delta W_i, \Delta t_i$ — Brownian increment and time increment over the $i$-th subinterval
- $Z_i$ — standardized normal $\mathcal{N}(0, 1)$
- $\|\Pi\|$ — mesh of the partition
- $n$ — number of subintervals
- $t$ — terminal time, equal to $\sum_i \Delta t_i$
- $\operatorname{Var}(\cdot)$ — variance under $\mathbb{P}$
- $L^2$ — mean-square convergence
:::

### Remark

The path quadratic variation of $W$ on $[0, t]$ is denoted $[W, W]_t = t$, and the infinitesimal shorthand is $(dW_t)^2 = dt$. This is the algebraic rule that makes Itô calculus work: a Taylor expansion to second order in $dW_t$ does not vanish; it contributes a $dt$ term. The first-order variation of a Brownian path is, in contrast, almost surely infinite — Brownian paths have unbounded first variation on every interval — so the chain rule of ordinary calculus fails.

## The Itô integral (sketch)

The Itô integral $\int_0^t H_s\, dW_s$ is constructed in three steps.

**Step A: simple integrands.** A process $H$ is **simple** if there is a partition $\{0 = s_0 < s_1 < \cdots < s_m = t\}$ such that $H_s = H_{s_i}$ for $s \in [s_i, s_{i+1})$, with each $H_{s_i}$ being $\mathcal{F}_{s_i}$-measurable and square-integrable. For such $H$ define
$$\int_0^t H_s\, dW_s = \sum_{i = 0}^{m - 1} H_{s_i}\, (W_{s_{i+1} \wedge t} - W_{s_i \wedge t}).$$

::: where
- $H$ — simple (step) integrand
- $s_i$ — partition points of the integrand's piecewise-constant decomposition
- $H_{s_i}$ — value of $H$ on $[s_i, s_{i+1})$, $\mathcal{F}_{s_i}$-measurable
- $\wedge$ — minimum operator, $a \wedge b = \min(a, b)$
- $\int_0^t H_s\, dW_s$ — Itô integral, defined first for simple integrands
:::

### Theorem (Itô isometry, statement)

For every simple $H$ with $\mathbb{E}\int_0^t H_s^2\, ds < \infty$,
$$\mathbb{E}\!\left[\left(\int_0^t H_s\, dW_s\right)^2\right] = \mathbb{E}\!\int_0^t H_s^2\, ds.$$

::: where
- $H$ — square-integrable simple integrand
- $\int_0^t H_s\, dW_s$ — Itô integral of $H$ against $W$ on $[0, t]$
- $\int_0^t H_s^2\, ds$ — ordinary (pathwise Lebesgue) integral of $H^2$
- $\mathbb{E}$ — expectation under $\mathbb{P}$
:::

**Step B: extension.** Let $\mathbb{H}^2_T$ denote the space of $\mathcal{F}_t$-predictable processes $H$ with $\mathbb{E}\int_0^T H_s^2\, ds < \infty$. The simple processes are dense in $\mathbb{H}^2_T$ for the norm $\|H\|_{\mathbb{H}^2} = (\mathbb{E}\int_0^T H_s^2\, ds)^{1/2}$, and the Itô integral on simple processes is a linear isometry into $L^2(\Omega, \mathcal{F}_T, \mathbb{P})$. Standard $L^2$ extension gives the Itô integral on all of $\mathbb{H}^2_T$.

**Step C: martingale property.** The resulting process $t \mapsto \int_0^t H_s\, dW_s$ admits a continuous version, and that version is a square-integrable $\mathcal{F}_t$-martingale on $[0, T]$.

We omit the proofs of the isometry, the density of simple integrands, and the continuity / martingale property; the standard reference is Shreve Vol. 2 §4.2–4.3 (or Karatzas-Shreve §3.2). What matters downstream is that (i) the integral exists for adapted square-integrable integrands, (ii) it has zero mean, (iii) the isometry computes its variance, and (iv) it is a martingale.

## Itô's lemma

This is the keystone of the chapter, and the one place where we write the proof in full.

### Theorem (Itô's lemma)

Let $X_t$ be a continuous Itô process satisfying
$$dX_t = \mu_t\, dt + \sigma_t\, dW_t, \qquad X_0 \in \mathbb{R},$$
with $\mu_t$ and $\sigma_t$ adapted processes satisfying $\int_0^T |\mu_s|\, ds < \infty$ and $\mathbb{E}\int_0^T \sigma_s^2\, ds < \infty$ almost surely. Let $f : \mathbb{R}_+ \times \mathbb{R} \to \mathbb{R}$ be a function of class $C^{1, 2}$ — once continuously differentiable in $t$, twice continuously differentiable in $x$. Then
$$df(t, X_t) = \!\left[ \frac{\partial f}{\partial t}(t, X_t) + \mu_t \frac{\partial f}{\partial x}(t, X_t) + \frac{1}{2} \sigma_t^2 \frac{\partial^2 f}{\partial x^2}(t, X_t) \right]\! dt + \sigma_t \frac{\partial f}{\partial x}(t, X_t)\, dW_t.$$

::: where
- $X_t$ — Itô process with drift $\mu_t$ and diffusion $\sigma_t$
- $\mu_t$ — adapted drift coefficient (integrable in $t$ pathwise)
- $\sigma_t$ — adapted diffusion coefficient (square-integrable)
- $W_t$ — standard Brownian motion driving $X$
- $f(t, x)$ — $C^{1, 2}$ function of time and space
- $\partial f / \partial t$ — partial derivative of $f$ in its time argument
- $\partial f / \partial x$ — partial derivative of $f$ in its space argument
- $\partial^2 f / \partial x^2$ — second partial derivative of $f$ in its space argument
- $dt, dW_t$ — formal differential symbols, integrated against time and Brownian motion respectively
:::

### Proof

The heuristic is a Taylor expansion to second order, using $(dW_t)^2 = dt$ and $(dt)^2 = dt \cdot dW_t = 0$ as algebraic rules:
$$df = \partial_t f\, dt + \partial_x f\, dX_t + \tfrac{1}{2} \partial_{xx} f\, (dX_t)^2.$$
With $dX_t = \mu_t\, dt + \sigma_t\, dW_t$ the cross term $(dX_t)^2 = \sigma_t^2\, dt$, and substituting gives the stated formula. We now make this rigorous.

Fix a partition $0 = t_0 < t_1 < \cdots < t_n = t$ of $[0, t]$ with mesh $\|\Pi\| \to 0$, and write the increment of $f$ as a telescoping sum:
$$f(t, X_t) - f(0, X_0) = \sum_{i = 0}^{n - 1} \big[ f(t_{i+1}, X_{t_{i+1}}) - f(t_i, X_{t_i}) \big].$$

Apply a second-order Taylor expansion to each summand around $(t_i, X_{t_i})$. With $\Delta t_i = t_{i+1} - t_i$ and $\Delta X_i = X_{t_{i+1}} - X_{t_i}$,
$$f(t_{i+1}, X_{t_{i+1}}) - f(t_i, X_{t_i}) = \partial_t f(t_i, X_{t_i})\, \Delta t_i + \partial_x f(t_i, X_{t_i})\, \Delta X_i + \tfrac{1}{2} \partial_{xx} f(t_i, X_{t_i})\, (\Delta X_i)^2 + R_i,$$
where $R_i$ collects all higher-order remainder terms: $O((\Delta t_i)^2)$ from the time direction, the cross term $\partial_{tx} f \cdot \Delta t_i\, \Delta X_i$, and the second-derivative remainder from continuity of $\partial_{xx} f$.

::: where
- $\Delta t_i = t_{i+1} - t_i$ — increment of time in the $i$-th subinterval
- $\Delta X_i = X_{t_{i+1}} - X_{t_i}$ — increment of the Itô process $X$ over the $i$-th subinterval
- $\partial_t f(t_i, X_{t_i})$ — time partial of $f$ evaluated at the left endpoint
- $\partial_x f(t_i, X_{t_i}), \partial_{xx} f(t_i, X_{t_i})$ — space partials of $f$ at the left endpoint
- $R_i$ — Taylor remainder collecting higher-order terms
- $\Pi$ — partition of $[0, t]$ with mesh $\|\Pi\| \to 0$
:::

We now identify the limit of each piece as $\|\Pi\| \to 0$.

**Time-derivative sum.** The summand $\partial_t f(t_i, X_{t_i})\, \Delta t_i$ is a Riemann sum for the continuous path $s \mapsto \partial_t f(s, X_s)$, which is continuous in $s$ by joint continuity of $\partial_t f$ and continuity of $X$. Therefore
$$\sum_{i = 0}^{n - 1} \partial_t f(t_i, X_{t_i})\, \Delta t_i \longrightarrow \int_0^t \partial_t f(s, X_s)\, ds$$
pathwise as $\|\Pi\| \to 0$.

**First-order space sum.** Writing $\Delta X_i = \mu_{t_i} \Delta t_i + \sigma_{t_i} \Delta W_i + \text{(small)}$ — where the "small" piece reflects the difference between left-endpoint coefficients and the true integrals over $[t_i, t_{i+1}]$, which vanishes in $L^2$ for bounded $\mu, \sigma$ —
$$\sum_{i = 0}^{n - 1} \partial_x f(t_i, X_{t_i})\, \Delta X_i \longrightarrow \int_0^t \partial_x f(s, X_s)\, \mu_s\, ds + \int_0^t \partial_x f(s, X_s)\, \sigma_s\, dW_s$$
in $L^2$. The first integral is a Lebesgue integral pathwise; the second is the Itô integral, whose definition is precisely the $L^2$ limit of left-endpoint Riemann-type sums of the form $\sum H_{t_i} \Delta W_i$.

**Second-order sum.** Expand $(\Delta X_i)^2$:
$$(\Delta X_i)^2 = \mu_{t_i}^2 (\Delta t_i)^2 + 2 \mu_{t_i} \sigma_{t_i} \Delta t_i\, \Delta W_i + \sigma_{t_i}^2 (\Delta W_i)^2 + \varepsilon_i,$$
where $\varepsilon_i$ collects negligible cross-terms involving coefficient differences. The first piece is $O((\Delta t_i)^2)$ — summed, of order $\|\Pi\| \cdot t \to 0$. The cross piece has mean zero and variance $O((\Delta t_i)^3)$ per term — summed, $L^2$-norm of order $\|\Pi\|^{3/2} \cdot \sqrt{t} \to 0$. The third piece is the only one that survives: it converges in $L^2$ to the quadratic-variation integral. Indeed, by the same $L^2$ argument used for the quadratic variation of $W$ — replacing the constant integrand by the locally constant integrand $\sigma_{t_i}^2$, which is bounded by hypothesis —
$$\sum_{i = 0}^{n - 1} \partial_{xx} f(t_i, X_{t_i})\, \sigma_{t_i}^2 (\Delta W_i)^2 \xrightarrow{L^2} \int_0^t \partial_{xx} f(s, X_s)\, \sigma_s^2\, ds.$$
Multiplying by the $\tfrac{1}{2}$ prefactor,
$$\tfrac{1}{2} \sum_{i = 0}^{n - 1} \partial_{xx} f(t_i, X_{t_i})\, (\Delta X_i)^2 \longrightarrow \tfrac{1}{2} \int_0^t \partial_{xx} f(s, X_s)\, \sigma_s^2\, ds.$$

**Remainder.** The remainders $R_i$ are of strictly higher order in $\Delta t_i$ and $\Delta X_i$ than the terms retained, and continuity of the second partials together with the $L^2$ bound on $\Delta X_i^2 \le C \Delta t_i$ (in mean) gives $\sum_i \mathbb{E}[|R_i|] \to 0$. Hence the remainder sum vanishes in $L^2$.

**Combine.** Putting the four limits together,
$$f(t, X_t) - f(0, X_0) = \int_0^t \!\left[ \partial_t f + \mu_s\, \partial_x f + \tfrac{1}{2} \sigma_s^2\, \partial_{xx} f \right]\! ds + \int_0^t \sigma_s\, \partial_x f\, dW_s,$$
with each partial of $f$ evaluated at $(s, X_s)$. Differentiating both sides formally — i.e., reading the displayed identity in its differential form — yields the stated SDE for $df(t, X_t)$. $\blacksquare$

### Remark (Itô applied to Brownian motion itself)

When $X_t = W_t$, i.e., $\mu_t = 0$ and $\sigma_t = 1$, Itô's lemma reduces to
$$df(t, W_t) = \!\left(\partial_t f(t, W_t) + \tfrac{1}{2} \partial_{xx} f(t, W_t)\right)\! dt + \partial_x f(t, W_t)\, dW_t.$$

::: where
- $W_t$ — standard Brownian motion
- $f(t, x)$ — $C^{1, 2}$ function
- $\partial_t f, \partial_x f, \partial_{xx} f$ — partial derivatives of $f$
- $dt, dW_t$ — formal time and Brownian differentials
:::

The extra $\tfrac{1}{2} \partial_{xx} f$ drift term is the signature of stochastic — as opposed to ordinary — calculus. It is the source of the $\tfrac{1}{2} \sigma^2$ correction that appears throughout option pricing.

## Geometric Brownian motion

### Theorem

The SDE
$$dS_t = \mu S_t\, dt + \sigma S_t\, dW_t, \qquad S_0 > 0,$$
with constants $\mu \in \mathbb{R}$ and $\sigma > 0$, has the unique strong solution
$$S_t = S_0 \exp\!\left(\big(\mu - \tfrac{1}{2}\sigma^2\big)\, t + \sigma\, W_t\right).$$

::: where
- $S_t$ — geometric Brownian motion price process
- $S_0 > 0$ — initial spot price, deterministic
- $\mu$ — drift coefficient (real)
- $\sigma > 0$ — volatility coefficient
- $W_t$ — standard Brownian motion under $\mathbb{P}$
- $t$ — time, $t \ge 0$
- $\exp$ — natural exponential
:::

### Proof

Apply Itô's lemma to $Y_t = \ln S_t$ — that is, to the function $f(x) = \ln x$ with partials $f'(x) = 1/x$ and $f''(x) = -1/x^2$. Note $\partial_t f = 0$ here. With $\mu_t = \mu S_t$ and $\sigma_t = \sigma S_t$, Itô's lemma gives
$$dY_t = \frac{1}{S_t}\, dS_t + \tfrac{1}{2} \cdot \!\left(-\frac{1}{S_t^2}\right)\! \cdot \sigma^2 S_t^2\, dt = \frac{1}{S_t}\big(\mu S_t\, dt + \sigma S_t\, dW_t\big) - \tfrac{1}{2} \sigma^2\, dt.$$

::: where
- $Y_t = \ln S_t$ — log-price process
- $f(x) = \ln x$ — function used in Itô's lemma
- $f'(x) = 1/x, f''(x) = -1/x^2$ — first and second derivatives
- $\mu_t = \mu S_t, \sigma_t = \sigma S_t$ — drift and diffusion of $S_t$
- $\sigma^2 S_t^2$ — squared diffusion entering the Itô correction
:::

Simplifying,
$$dY_t = \mu\, dt + \sigma\, dW_t - \tfrac{1}{2} \sigma^2\, dt = \big(\mu - \tfrac{1}{2} \sigma^2\big)\, dt + \sigma\, dW_t.$$

Integrating from $0$ to $t$,
$$Y_t - Y_0 = \big(\mu - \tfrac{1}{2} \sigma^2\big)\, t + \sigma\, W_t,$$
i.e., $\ln(S_t / S_0) = (\mu - \tfrac{1}{2} \sigma^2)\, t + \sigma\, W_t$, hence
$$S_t = S_0 \exp\!\left(\big(\mu - \tfrac{1}{2} \sigma^2\big)\, t + \sigma\, W_t\right).$$

Existence is confirmed by direct verification: the process defined by the right-hand side satisfies $dS_t = \mu S_t\, dt + \sigma S_t\, dW_t$ by another application of Itô's lemma to $g(x) = S_0 e^x$ evaluated at the Itô process $(\mu - \tfrac{1}{2}\sigma^2)\, t + \sigma\, W_t$. Uniqueness of the strong solution follows from the Lipschitz / linear-growth conditions on the coefficients $x \mapsto \mu x$ and $x \mapsto \sigma x$; we cite Shreve Vol. 2 §6.2 (or Karatzas-Shreve §5.2) for the standard existence-and-uniqueness theorem invoked here. $\blacksquare$

### Corollary (Lognormal distribution of $S_T$)

For each $T > 0$, $S_T$ is lognormally distributed with
$$\ln S_T \sim \mathcal{N}\!\left(\ln S_0 + \big(\mu - \tfrac{1}{2} \sigma^2\big) T, \; \sigma^2 T\right).$$

::: where
- $S_T$ — geometric-Brownian-motion price at the horizon $T$
- $S_0$ — initial spot
- $\mu, \sigma$ — drift and volatility of the SDE
- $T > 0$ — horizon, in years
- $\mathcal{N}(\,\cdot\,, \,\cdot\,)$ — normal distribution, parametrized by mean and variance
:::

This is immediate from the closed-form solution: $\ln S_T = \ln S_0 + (\mu - \tfrac{1}{2}\sigma^2) T + \sigma W_T$ is an affine transformation of $W_T \sim \mathcal{N}(0, T)$, so its distribution is normal with the stated mean and variance.

### Remark (link to Chapter 2)

The lognormal expected-payoff theorem of Chapter 2 was stated for
$$S_T = S_0 \exp\!\left(\big(m - \tfrac{1}{2}\sigma^2\big) T + \sigma \sqrt{T}\, Z\right), \qquad Z \sim \mathcal{N}(0, 1).$$
The chapter-2 parameter $m$ plays the role of the Chapter-3 drift $\mu$, and $\sigma\sqrt{T}\, Z$ has exactly the distribution of $\sigma W_T$. Hence GBM is precisely the dynamic model whose terminal marginal distribution is what Chapter 2's static computation already priced. Chapter 8 will combine GBM with Girsanov to set $m = r$ — the risk-free rate — and recover Black-Scholes.

## Girsanov's theorem (stated)

### Theorem (Girsanov)

Let $\{\theta_t\}_{t \in [0, T]}$ be an adapted process satisfying the **Novikov condition**
$$\mathbb{E}\!\left[\exp\!\left(\tfrac{1}{2} \int_0^T \theta_s^2\, ds\right)\right] < \infty.$$
Define the **Radon-Nikodym derivative**
$$Z_T = \exp\!\left(-\int_0^T \theta_s\, dW_s - \tfrac{1}{2} \int_0^T \theta_s^2\, ds\right),$$
and a new probability measure $\mathbb{Q}$ on $(\Omega, \mathcal{F}_T)$ by
$$\frac{d\mathbb{Q}}{d\mathbb{P}} = Z_T.$$
Then $\mathbb{Q}$ is equivalent to $\mathbb{P}$ on $\mathcal{F}_T$, and the process
$$\tilde W_t = W_t + \int_0^t \theta_s\, ds, \qquad t \in [0, T],$$
is a standard Brownian motion under $\mathbb{Q}$.

::: where
- $\theta_t$ — adapted "market price of risk" process, drift to be removed
- $W_t$ — standard Brownian motion under $\mathbb{P}$
- $Z_T$ — Radon-Nikodym derivative of $\mathbb{Q}$ with respect to $\mathbb{P}$ on $\mathcal{F}_T$
- $\int_0^T \theta_s\, dW_s$ — Itô integral, finite under the Novikov condition
- $\int_0^T \theta_s^2\, ds$ — pathwise Lebesgue integral, finite under Novikov
- $\mathbb{P}, \mathbb{Q}$ — original and shifted measures on $(\Omega, \mathcal{F}_T)$, equivalent on $\mathcal{F}_T$
- $\tilde W_t$ — drifted process, a Brownian motion under $\mathbb{Q}$
- Novikov condition — integrability hypothesis ensuring $Z$ is a true martingale, not merely a local one
:::

### Remark (proof omitted)

The proof requires the Lévy characterization stated above, together with the optional-stopping theorem applied to the exponential martingale $Z$, plus the verification that $\tilde W$ has the right covariation under $\mathbb{Q}$. We cite Shreve Vol. 2 §5.2 (or Karatzas-Shreve §3.5) for the full argument.

### Remark (use)

Girsanov is the engine of risk-neutral pricing. In Chapter 8 we take $\theta_t = (\mu - r) / \sigma$ — the so-called market price of risk — so that
$$d\tilde W_t = dW_t + \frac{\mu - r}{\sigma}\, dt,$$
and the discounted stock price $e^{-rt} S_t$ becomes a $\mathbb{Q}$-martingale: under the new measure, the drift of $S_t$ is exactly $r$, not $\mu$. Pricing by discounted $\mathbb{Q}$-expectation then yields the Black-Scholes formula. Chapter 4 develops the no-arbitrage logic that motivates this change of measure; Chapter 8 carries out the computation.

## Practice

::: problem [Conceptual]
**Problem 3.1.** Why does $(dW_t)^2 = dt$ at the level of Itô calculus? What is the precise rigorous statement underlying this heuristic identity?

::: solution
**Heuristic.** The shorthand $(dW_t)^2 = dt$ is a formal algebraic rule: when applied inside a second-order Taylor expansion of $f(t, X_t)$, it produces the correct Itô correction term. It captures the fact that Brownian increments scale like the square root of the time increment — $\Delta W_i \sim \sqrt{\Delta t_i}\, Z_i$ with $Z_i \sim \mathcal{N}(0, 1)$ — so squared increments scale like $\Delta t_i$, which is first-order in the time step. Squared increments do **not** vanish in the limit, in stark contrast with $(\Delta t_i)^2$ and $\Delta t_i \cdot \Delta W_i$, which do.

**Rigorous statement.** Fix $t > 0$ and a sequence of partitions $\Pi_n$ of $[0, t]$ with mesh $\|\Pi_n\| \to 0$. Then
$$Q_{\Pi_n}(W; t) = \sum_{i} (W_{t_{i+1}} - W_{t_i})^2 \xrightarrow{L^2} t.$$
Equivalently, the path quadratic variation of Brownian motion is deterministic and linear: $[W, W]_t = t$. This is the rigorous content of $(dW_t)^2 = dt$. It is responsible for the Itô correction $\tfrac{1}{2} \sigma^2\, \partial_{xx} f$ in Itô's lemma — the term that, applied to $\ln S_t$, drops the drift of $S_t$ from $\mu$ down to $\mu - \tfrac{1}{2}\sigma^2$ in the closed-form GBM solution. $\blacksquare$
:::
:::

::: problem [Derivation]
**Problem 3.2.** Use Itô's lemma to derive the SDE satisfied by $Y_t = W_t^2$, and verify that $W_t^2 - t$ is an $\mathcal{F}_t$-martingale.

::: solution
Apply Itô's lemma to $f(t, w) = w^2$ with $X_t = W_t$ (so $\mu_t = 0$, $\sigma_t = 1$). The partials are
$$\partial_t f = 0, \qquad \partial_w f = 2w, \qquad \partial_{ww} f = 2.$$
Substitute into Itô:
$$d(W_t^2) = \big(\partial_t f + 0 \cdot \partial_w f + \tfrac{1}{2} \cdot 1 \cdot \partial_{ww} f\big)\, dt + 1 \cdot \partial_w f\, dW_t = \big(0 + 0 + \tfrac{1}{2} \cdot 2\big)\, dt + 2 W_t\, dW_t = dt + 2 W_t\, dW_t.$$

::: where
- $W_t$ — standard Brownian motion
- $f(t, w) = w^2$ — function being differentiated by Itô's lemma
- $\partial_t f, \partial_w f, \partial_{ww} f$ — partials of $f$
- $d(W_t^2)$ — Itô differential of $W_t^2$
:::

**Martingale verification.** Integrate from $0$ to $t$, using $W_0 = 0$:
$$W_t^2 - 0 = \int_0^t 1\, ds + \int_0^t 2 W_s\, dW_s = t + 2 \int_0^t W_s\, dW_s,$$
hence
$$W_t^2 - t = 2 \int_0^t W_s\, dW_s.$$
The right-hand side is the Itô integral of the adapted square-integrable integrand $2 W_s$ — square-integrable because $\mathbb{E}\int_0^t 4 W_s^2\, ds = 4 \int_0^t s\, ds = 2 t^2 < \infty$ — and the Itô integral of any such integrand is a continuous $\mathcal{F}_t$-martingale with initial value $0$. Therefore $W_t^2 - t$ is an $\mathcal{F}_t$-martingale with $W_0^2 - 0 = 0$, as required by the Lévy characterization. $\blacksquare$
:::
:::

::: problem [Computation]
**Problem 3.3.** A stock follows geometric Brownian motion with $S_0 = 100$, $\mu = 0.08$, $\sigma = 0.20$, and horizon $t = 1$. Compute $\mathbb{E}[S_1]$ and $\operatorname{Var}(S_1)$, showing the intermediate steps.

::: solution
**Closed-form solution.** From the GBM theorem,
$$S_1 = S_0 \exp\!\left(\big(\mu - \tfrac{1}{2} \sigma^2\big) \cdot 1 + \sigma\, W_1\right) = 100 \exp\!\left((0.08 - 0.02) + 0.20\, W_1\right) = 100\, e^{0.06 + 0.20\, W_1},$$
with $W_1 \sim \mathcal{N}(0, 1)$. Hence
$$\ln S_1 \sim \mathcal{N}\!\left(\ln 100 + 0.06, \; 0.04\right).$$

::: where
- $S_1$ — GBM price at $t = 1$
- $S_0 = 100$ — initial spot
- $\mu = 0.08$ — drift
- $\sigma = 0.20$ — volatility
- $W_1$ — standard normal Brownian increment
- $\mathcal{N}(\,\cdot, \cdot)$ — normal distribution, mean and variance
:::

**Mean.** Using the lognormal mean formula $\mathbb{E}[e^X] = e^{\mu_X + \sigma_X^2/2}$ from Chapter 2 with $\mu_X = \ln 100 + 0.06$ and $\sigma_X^2 = 0.04$,
$$\mathbb{E}[S_1] = \exp\!\left(\ln 100 + 0.06 + \tfrac{1}{2} \cdot 0.04\right) = 100 \cdot e^{0.06 + 0.02} = 100\, e^{0.08}.$$
Numerically $e^{0.08} \approx 1.08329$, giving
$$\mathbb{E}[S_1] \approx 108.33.$$
(This is the textbook identity $\mathbb{E}[S_t] = S_0\, e^{\mu t}$ for GBM.)

**Variance.** Using the lognormal variance corollary from Chapter 2 with the same parameters,
$$\operatorname{Var}(S_1) = e^{2\mu_X + \sigma_X^2}\big(e^{\sigma_X^2} - 1\big) = S_0^2\, e^{2\mu t}\big(e^{\sigma^2 t} - 1\big) = 100^2 \cdot e^{2 \cdot 0.08} \cdot \big(e^{0.04} - 1\big).$$
Numerically $e^{0.16} \approx 1.17351$ and $e^{0.04} - 1 \approx 0.04081$:
$$\operatorname{Var}(S_1) \approx 10000 \cdot 1.17351 \cdot 0.04081 \approx 478.9.$$

**Standard deviation.** $\operatorname{SD}(S_1) = \sqrt{\operatorname{Var}(S_1)} \approx \sqrt{478.9} \approx 21.9$.

So $\mathbb{E}[S_1] \approx 108.33$ and $\operatorname{Var}(S_1) \approx 478.9$. $\blacksquare$
:::
:::
