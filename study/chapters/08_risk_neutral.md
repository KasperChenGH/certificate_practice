# Chapter 8 — Risk-Neutral Derivation

## Goals

- Re-derive the Black-Scholes-Merton closed form by directly integrating the discounted risk-neutral expectation $e^{-r(T-t)}\, \mathbb{E}^{\mathbb{Q}}\big[(S_T - K)^+ \mid \mathcal{F}_t\big]$, bypassing the PDE machinery of Ch. 7.
- State the Feynman-Kac theorem, the formal bridge linking parabolic PDEs to expectations of terminal payoffs under a diffusion measure, and sketch the proof that the BSM PDE arises from the discounted-expectation pricing rule.
- Confirm that the two routes — PDE solving (Ch. 7) and risk-neutral expectation (this chapter) — produce *exactly the same* closed-form call price, and explain why this agreement is structural, not coincidental.
- Provide a numerically verifiable Monte Carlo recipe for the call price, allowing the reader to sanity-check the closed form against an independent stochastic simulation.

## Prerequisites

- **Ch. 2** — the lognormal expected-payoff theorem $\mathbb{E}\big[(S_T - K)^+\big] = S_0\, e^{mT}\, N(d_1) - K\, N(d_2)$ for $\log S_T$ normal with drift parameter $m$. This is the keystone identity we will instantiate at $m = r$.
- **Ch. 3** — Itô's formula, geometric Brownian motion (GBM), and the explicit GBM solution $S_t = S_0 \exp\big((\mu - \sigma^2/2) t + \sigma W_t\big)$ in solved form; Girsanov's theorem for changing the drift of a Brownian motion under an equivalent measure.
- **Ch. 4** — construction of the risk-neutral measure $\mathbb{Q}$ for the BSM market; the resulting $\mathbb{Q}$-SDE $dS_t = r S_t\, dt + \sigma S_t\, d\tilde W_t$ with $\tilde W$ a $\mathbb{Q}$-Brownian motion; the risk-neutral pricing rule $V_t = e^{-r(T-t)}\, \mathbb{E}^{\mathbb{Q}}\big[f(S_T) \mid \mathcal{F}_t\big]$.
- **Ch. 5** — European payoff structure and put-call parity (used implicitly when we cross-reference Ch. 7's put formula).
- **Ch. 7** — the closed-form European call price $C(S, t) = S\, N(d_1) - K\, e^{-r(T - t)}\, N(d_2)$ derived via the PDE route, which we will reproduce here by a completely different method.

---

## Setup

From Ch. 4, the construction of the risk-neutral measure $\mathbb{Q}$ on the Black-Scholes market gives the $\mathbb{Q}$-dynamics of the stock as

$$dS_t = r\, S_t\, dt + \sigma\, S_t\, d\tilde W_t,$$

with $\tilde W$ a standard Brownian motion under $\mathbb{Q}$. Equivalently, $S$ is a geometric Brownian motion with drift $r$ (the risk-free rate) and volatility $\sigma$.

The risk-neutral pricing rule, also established in Ch. 4, states that the time-$t$ no-arbitrage price of a European-style claim with $\mathcal{F}_T$-measurable terminal payoff $f(S_T)$ is

$$V_t = e^{-r(T - t)}\, \mathbb{E}^{\mathbb{Q}}\!\big[\, f(S_T)\,\big|\, \mathcal{F}_t\,\big].$$

::: where
- $S_t$ — spot price of the underlying at time $t \in [0, T]$, taking values in $(0, \infty)$.
- $r$ — constant continuously compounded risk-free rate; the discount factor over $[t, T]$ is $e^{-r(T-t)}$.
- $\sigma > 0$ — constant instantaneous volatility of the stock under both $\mathbb{P}$ and $\mathbb{Q}$ (Girsanov leaves $\sigma$ invariant; only the drift changes).
- $\tilde W_t$ — standard Brownian motion under $\mathbb{Q}$, constructed from the physical Brownian motion $W_t$ via $\tilde W_t = W_t + \theta t$ with market price of risk $\theta = (\mu - r)/\sigma$ (Ch. 4).
- $\mathcal{F}_t$ — the natural filtration of $W$ (equivalently of $\tilde W$ — equivalence of measures preserves the null sets and hence the filtration up to completion).
- $f : (0, \infty) \to \mathbb{R}$ — the terminal payoff function; for a European call, $f(s) = (s - K)^+$.
- $\mathbb{E}^{\mathbb{Q}}[\cdot \mid \mathcal{F}_t]$ — conditional expectation under $\mathbb{Q}$ given the information available at time $t$.
- $V_t$ — the time-$t$ no-arbitrage price of the claim, equivalently the time-$t$ cost of the replicating portfolio (Ch. 6).
:::

This chapter consists of two derivations: an explicit integration of the call's risk-neutral expectation (which produces Ch. 7's closed form by a different route), and the statement of Feynman-Kac that explains *why* the two routes must agree.

---

## Distribution of $S_T$ under $\mathbb{Q}$

The $\mathbb{Q}$-SDE $dS_t = r\, S_t\, dt + \sigma\, S_t\, d\tilde W_t$ is a geometric Brownian motion. By the Ch. 3 GBM solution (apply Itô to $\log S$), the closed-form solution from time $t$ to time $T$ is

$$S_T = S_t\, \exp\!\Big(\big(r - \tfrac{1}{2}\sigma^2\big)(T - t) + \sigma\, (\tilde W_T - \tilde W_t)\Big).$$

Since $\tilde W_T - \tilde W_t$ is independent of $\mathcal{F}_t$ and distributed as $\mathcal{N}(0, T - t)$ under $\mathbb{Q}$, the conditional distribution of $\log S_T$ given $\mathcal{F}_t$ is normal:

$$\log S_T \,\big|\, \mathcal{F}_t \;\sim\; \mathcal{N}\!\Big(\log S_t + \big(r - \tfrac{1}{2}\sigma^2\big)(T - t),\; \sigma^2 (T - t)\Big) \quad \text{under } \mathbb{Q}.$$

::: where
- $\log S_T \mid \mathcal{F}_t$ — the conditional distribution of the terminal log-price, given the information at time $t$.
- Mean $\log S_t + (r - \tfrac{1}{2}\sigma^2)(T - t)$ — note the *Itô correction* $-\tfrac{1}{2}\sigma^2(T-t)$: even though $S$ has drift $r$, its log has drift $r - \tfrac{1}{2}\sigma^2$ by Itô's formula applied to $\log s$.
- Variance $\sigma^2 (T - t)$ — the integrated diffusion coefficient; this is also the *total variance* used in the Black-Scholes formula via $\sigma\sqrt{T - t}$.
- $\mathbb{Q}$ — the risk-neutral measure; under $\mathbb{P}$ the drift of $\log S$ would be $\mu - \tfrac{1}{2}\sigma^2$ instead, with the same variance.
- Equivalently, $S_T = S_t\, e^{X}$ where $X \sim \mathcal{N}\big((r - \tfrac{1}{2}\sigma^2)(T-t),\, \sigma^2(T-t)\big)$ under $\mathbb{Q}$ conditional on $\mathcal{F}_t$ — i.e., $S_T \mid \mathcal{F}_t$ is *lognormal*.
:::

This is the exact lognormal setup of Ch. 2's keystone theorem, with $S_0 \to S_t$, $T \to T - t$, and $m = r$.

---

## Pricing the call by expectation

### Theorem (Risk-neutral call price)

Let $S$ follow the $\mathbb{Q}$-SDE $dS_t = r S_t\, dt + \sigma S_t\, d\tilde W_t$ and let $C_t$ denote the time-$t$ no-arbitrage price of the European call with strike $K$ and maturity $T$. Then

$$C_t \;=\; e^{-r(T - t)}\, \mathbb{E}^{\mathbb{Q}}\!\big[\,(S_T - K)^+\,\big|\, \mathcal{F}_t\,\big].$$

::: where
- $C_t$ — time-$t$ call price; equivalent to the replicating-portfolio value of Ch. 6.
- $(S_T - K)^+ = \max(S_T - K, 0)$ — terminal payoff of the European call (Ch. 5).
- $e^{-r(T-t)}$ — deterministic discount factor pulling the expected payoff from time $T$ back to time $t$.
- $\mathbb{E}^{\mathbb{Q}}[\cdot \mid \mathcal{F}_t]$ — conditional expectation under the risk-neutral measure constructed in Ch. 4.
- The theorem is the instance $f(s) = (s - K)^+$ of the general risk-neutral pricing rule.
:::

### Closed-form evaluation

We instantiate Ch. 2's *Lognormal Expected Payoff* theorem. That theorem says: if $S_T = S_0\, \exp\!\big((m - \tfrac{1}{2}\sigma^2) T + \sigma\sqrt{T}\, Z\big)$ with $Z \sim \mathcal{N}(0, 1)$, then

$$\mathbb{E}\big[(S_T - K)^+\big] = S_0\, e^{mT}\, N(d_1) - K\, N(d_2),$$

with $d_1 = [\log(S_0 / K) + (m + \tfrac{1}{2}\sigma^2) T] / (\sigma\sqrt{T})$ and $d_2 = d_1 - \sigma\sqrt{T}$.

The conditional distribution of $S_T$ under $\mathbb{Q}$ given $\mathcal{F}_t$ matches this setup exactly with the substitutions

$$S_0 \longrightarrow S_t, \qquad T \longrightarrow T - t, \qquad m \longrightarrow r.$$

Applying the theorem (the proof in Ch. 2 carries over verbatim because all that mattered was the lognormal structure with drift parameter $m$, and we are simply renaming $m$ to $r$),

$$\mathbb{E}^{\mathbb{Q}}\!\big[(S_T - K)^+\,\big|\, \mathcal{F}_t\big] \;=\; S_t\, e^{r(T - t)}\, N(d_1) - K\, N(d_2).$$

::: where
- The substitution $m \to r$ — automatic, because under $\mathbb{Q}$ the drift of $\log S$ is exactly $r - \tfrac{1}{2}\sigma^2$ (cf. previous section).
- $d_1$ — equals $\big[\log(S_t / K) + (r + \tfrac{1}{2}\sigma^2)(T - t)\big] / (\sigma\sqrt{T - t})$ after substitution.
- $d_2 = d_1 - \sigma\sqrt{T - t}$ — same as in Ch. 7.
- $S_t\, e^{r(T - t)}$ — the *risk-neutral forward price* of the stock from time $t$ to time $T$: under $\mathbb{Q}$, $\mathbb{E}^{\mathbb{Q}}[S_T \mid \mathcal{F}_t] = S_t\, e^{r(T-t)}$.
- No proof is required here — Ch. 2 did the integral; we are only relabeling parameters.
:::

Now discount by $e^{-r(T - t)}$:

$$C_t \;=\; e^{-r(T - t)} \cdot \big[\, S_t\, e^{r(T - t)}\, N(d_1) - K\, N(d_2)\,\big] \;=\; S_t\, N(d_1) - K\, e^{-r(T - t)}\, N(d_2).$$

The $e^{r(T-t)}$ and $e^{-r(T-t)}$ on the first term cancel, while the second term retains its discount factor.

$$\boxed{\;C_t \;=\; S_t\, N(d_1) \;-\; K\, e^{-r(T - t)}\, N(d_2).\;}$$

This is *identical*, term for term, to the Ch. 7 closed form derived by PDE. $\checkmark$

---

## Feynman-Kac theorem

The agreement of the PDE and risk-neutral derivations is not an accident; it is a theorem.

### Theorem (Feynman-Kac)

Let $S$ follow the $\mathbb{Q}$-SDE $dS_u = r\, S_u\, du + \sigma\, S_u\, d\tilde W_u$ on $[t, T]$ with $S_t = s > 0$, and let $g : (0, \infty) \to \mathbb{R}$ be a sufficiently regular payoff (continuous and of at most polynomial growth, say). Define

$$V(s, t) \;:=\; e^{-r(T - t)}\, \mathbb{E}^{\mathbb{Q}}\!\big[\, g(S_T)\,\big|\, S_t = s\,\big].$$

Then $V \in C^{2, 1}\big((0, \infty) \times [0, T)\big)$ (twice differentiable in $s$, once in $t$) and $V$ solves the Black-Scholes PDE

$$V_t \;+\; \tfrac{1}{2}\sigma^2 s^2\, V_{ss} \;+\; r\, s\, V_s \;-\; r\, V \;=\; 0, \qquad (s, t) \in (0, \infty) \times [0, T),$$

with terminal condition $V(s, T) = g(s)$.

::: where
- $V(s, t)$ — the price functional: the discounted $\mathbb{Q}$-expected payoff conditional on $S_t = s$.
- $g$ — the payoff; for the European call $g(s) = (s - K)^+$, which satisfies the polynomial-growth hypothesis.
- $C^{2,1}$ — twice continuously differentiable in the spatial variable $s$ and once in time $t$; the natural regularity class for parabolic PDEs.
- Terminal condition $V(s, T) = g(s)$ — at $t = T$ the discount factor and conditional expectation become trivial: $V(s, T) = 1 \cdot \mathbb{E}^{\mathbb{Q}}[g(S_T) \mid S_T = s] = g(s)$.
- The coefficient $\tfrac{1}{2}\sigma^2 s^2$ is exactly $\tfrac{1}{2}(\sigma s)^2$ — the squared diffusion coefficient of the $\mathbb{Q}$-SDE; the coefficient $rs$ is the $\mathbb{Q}$-drift.
:::

### Sketch of proof

Apply Itô's formula to $V(S_u, u)$ along the $\mathbb{Q}$-SDE on $[t, T]$. Using $dS_u = r S_u\, du + \sigma S_u\, d\tilde W_u$ and $d\langle S\rangle_u = \sigma^2 S_u^2\, du$,

$$dV(S_u, u) \;=\; \Big(V_t + r\, S_u\, V_s + \tfrac{1}{2}\sigma^2 S_u^2\, V_{ss}\Big)\, du \;+\; \sigma\, S_u\, V_s\, d\tilde W_u.$$

Now consider the *discounted* price $M_u := e^{-r(u - t)}\, V(S_u, u)$. By the product rule (Itô),

$$dM_u \;=\; e^{-r(u-t)}\Big[\, -r\, V \;+\; V_t \;+\; r\, S_u\, V_s \;+\; \tfrac{1}{2}\sigma^2 S_u^2\, V_{ss}\,\Big]\, du \;+\; e^{-r(u-t)}\, \sigma\, S_u\, V_s\, d\tilde W_u.$$

The key claim is that $M_u$ is a $\mathbb{Q}$-martingale on $[t, T]$. Granting this for the moment, the drift coefficient of $M_u$ must vanish:

$$-r\, V \;+\; V_t \;+\; r\, s\, V_s \;+\; \tfrac{1}{2}\sigma^2 s^2\, V_{ss} \;=\; 0,$$

which is precisely the BSM PDE.

It remains to show $M_u$ is a $\mathbb{Q}$-martingale. By the definition of $V$,

$$V(S_u, u) \;=\; e^{-r(T - u)}\, \mathbb{E}^{\mathbb{Q}}\!\big[\, g(S_T)\,\big|\, \mathcal{F}_u\,\big],$$

so $M_u = e^{-r(u-t)}\, e^{-r(T-u)}\, \mathbb{E}^{\mathbb{Q}}[g(S_T) \mid \mathcal{F}_u] = e^{-r(T-t)}\, \mathbb{E}^{\mathbb{Q}}[g(S_T) \mid \mathcal{F}_u]$. Conditional expectations under a fixed measure form a martingale by the tower property: for $u \le v$,

$$\mathbb{E}^{\mathbb{Q}}[M_v \mid \mathcal{F}_u] \;=\; e^{-r(T-t)}\, \mathbb{E}^{\mathbb{Q}}\!\big[\, \mathbb{E}^{\mathbb{Q}}[g(S_T) \mid \mathcal{F}_v]\,\big|\, \mathcal{F}_u\,\big] \;=\; e^{-r(T-t)}\, \mathbb{E}^{\mathbb{Q}}[g(S_T) \mid \mathcal{F}_u] \;=\; M_u.$$

Hence $M$ is a $\mathbb{Q}$-martingale, its drift vanishes, and the PDE follows. For the full proof with regularity assumptions on $g$ and the diffusion coefficients (needed to justify the smoothness of $V$ via parabolic regularity), see Shreve, *Stochastic Calculus for Finance II*, §6.4. $\square$

::: where
- The Itô expansion of $V(S_u, u)$ — uses $V \in C^{2,1}$; the smoothness is itself a theorem (parabolic regularity), which is the hard step glossed over here.
- The discount factor $e^{-r(u-t)}$ produces the $-rV$ contribution via $d(e^{-r(u-t)}) = -r\, e^{-r(u-t)}\, du$.
- The martingale property comes from the tower property of conditional expectations under a fixed measure; no Girsanov reasoning is needed here.
- The "drift must vanish" step uses that a continuous martingale of finite variation is constant — formally, the drift integrand is identically zero almost everywhere.
:::

### Remark

Feynman-Kac is the formal bridge: *PDE solutions equal expectations of terminal payoffs under a diffusion measure.* The two derivations in this chapter and Ch. 7 are therefore *not independent* — they are two views of the same underlying mathematical fact. The PDE side gives a deterministic boundary-value problem on $(0, \infty) \times [0, T]$; the expectation side gives a stochastic-integral representation. Each side has computational and conceptual advantages, but neither is privileged: the call price is the *common value* of two equivalent characterizations.

---

## Comparison with Chapter 7

The two routes to the Black-Scholes formula proceed as follows.

**Ch. 7 — PDE route.** Start from the BSM PDE $V_t + \tfrac{1}{2}\sigma^2 S^2 V_{SS} + r S V_S - r V = 0$ with the call's terminal and boundary conditions. Substitute $x = \log(S/K)$ and $\tau = \tfrac{1}{2}\sigma^2(T-t)$ to eliminate the variable coefficients, then factor out an exponential $e^{\alpha x + \beta \tau}$ to cancel the lower-order terms, reducing the equation to the bare heat equation $v_\tau = v_{xx}$ on $\mathbb{R}$. Convolve the call's transformed initial condition against the Gaussian heat kernel, complete the square in two integrals, recognize the integrals as cumulative normals, and back-substitute through the variable changes. The output is $C(S, t) = S\, N(d_1) - K\, e^{-r(T-t)}\, N(d_2)$.

**Ch. 8 — Risk-neutral expectation route.** Under $\mathbb{Q}$ (constructed in Ch. 4), the stock follows GBM with drift $r$, so $\log S_T \mid \mathcal{F}_t$ is normal with mean $\log S_t + (r - \tfrac{1}{2}\sigma^2)(T-t)$ and variance $\sigma^2(T-t)$. Invoke the lognormal expected-payoff theorem from Ch. 2 with $m = r$ to evaluate $\mathbb{E}^{\mathbb{Q}}[(S_T - K)^+ \mid \mathcal{F}_t]$ in closed form. Discount by $e^{-r(T-t)}$. The output is the same $C(S, t) = S\, N(d_1) - K\, e^{-r(T-t)}\, N(d_2)$.

The PDE route generalizes naturally to *path-independent* payoffs that may differ from the call (digital options, power options, etc.) — the PDE structure is unchanged, only the terminal condition is replaced, but the convolution integral has to be redone for each new payoff. The risk-neutral route generalizes naturally to *path-dependent* payoffs (Asian options averaging $S$ over $[0, T]$, barrier options conditioning on $\sup_{s \le T} S_s$, lookback options, etc.) because conditional expectations under $\mathbb{Q}$ can be computed by Monte Carlo simulation of $\mathbb{Q}$-paths, even when no closed form exists. The PDE route for path-dependent payoffs requires higher-dimensional PDEs in additional state variables (the running average, the running maximum, etc.) and is computationally heavier. Each route is the natural tool in its domain; together they cover the practical pricing landscape.

---

## Practice

::: problem [Conceptual]
**Problem 8.1.** Risk-neutral pricing says the price equals the discounted expected payoff under $\mathbb{Q}$, and under $\mathbb{Q}$ the expected return on the stock is $r$. But real investors do not earn $r$ — they expect $\mu > r$ for a typical equity, since equities carry risk. Reconcile these two statements: why does pricing under a measure that "doesn't describe reality" give the correct no-arbitrage price?
:::

::: solution
The risk-neutral measure $\mathbb{Q}$ is a *mathematical pricing device*, not a description of investor expectations or observed returns. The construction of $\mathbb{Q}$ in Ch. 4 used Girsanov's theorem to shift the drift of the Brownian motion by exactly the market price of risk $\theta = (\mu - r)/\sigma$, transforming the physical SDE $dS_t = \mu S_t\, dt + \sigma S_t\, dW_t$ into the risk-neutral SDE $dS_t = r S_t\, dt + \sigma S_t\, d\tilde W_t$. Under $\mathbb{Q}$, the discounted stock price $e^{-rt} S_t$ is a martingale — this is the defining property of an equivalent martingale measure, and it is what makes discounted expectation an arbitrage-consistent pricing rule.

The key insight from Ch. 6 is that the option price equals the cost of a *replicating portfolio* in stock and bond, not the expected discounted payoff under $\mathbb{P}$. The replicating cost is a no-arbitrage quantity — it does not depend on investors' risk preferences or their assessments of $\mu$. The market price of risk $\theta$, which encodes investors' risk-aversion-driven excess return, drops out of the replicating cost: if you can hedge the option dynamically, the hedging cost is determined by the stock's volatility $\sigma$ and the riskless rate $r$ alone. The drift $\mu$ never appears.

The risk-neutral measure is precisely the measure under which the discounted-expectation formula reproduces this replicating cost. Two ways of saying the same thing: (i) "price by replication under $\mathbb{P}$ — no expected returns appear because perfect hedging removes them"; (ii) "price by discounted expectation under $\mathbb{Q}$ — under $\mathbb{Q}$ the drift is artificially set to $r$, so all returns cancel against the discount factor." These are mathematically equivalent (Ch. 4 made this explicit via Girsanov), and both give the unique no-arbitrage price. The substitution $\mu \to r$ in the formulas is not a claim about reality; it is the analytical signature of the no-arbitrage hedging argument.

A useful way to memorize this: under $\mathbb{Q}$, *every traded asset has expected return $r$* (because that is the only consistent way to make the discounted price a martingale). This is true even for derivatives. The fact that real investors require a risk premium for holding the stock is irrelevant to the option's hedging cost, because the hedger holds offsetting positions in stock and bond that exactly neutralize the stock's return.
:::

---

::: problem [Derivation]
**Problem 8.2.** Derive the Black-Scholes call price from scratch by directly evaluating $e^{-r T}\, \mathbb{E}^{\mathbb{Q}}\big[(S_T - K)^+\big]$ at $t = 0$ — without invoking the Ch. 2 theorem. Show the change of variable to a standard normal and explicitly compute the two resulting Gaussian integrals.
:::

::: solution
**Setup.** Under $\mathbb{Q}$ with $S_0$ fixed, write

$$S_T \;=\; S_0\, \exp\!\Big(\big(r - \tfrac{1}{2}\sigma^2\big) T + \sigma\sqrt{T}\, Z\Big), \qquad Z \sim \mathcal{N}(0, 1).$$

The exercise event $\{S_T > K\}$ translates to a condition on $Z$:

$$S_T > K \;\iff\; \big(r - \tfrac{1}{2}\sigma^2\big) T + \sigma\sqrt{T}\, Z > \log(K / S_0) \;\iff\; Z > -d_2,$$

where (computing as in Ch. 2)

$$-d_2 \;=\; \frac{\log(K/S_0) - (r - \tfrac{1}{2}\sigma^2) T}{\sigma\sqrt{T}} \;=\; -\,\frac{\log(S_0/K) + (r - \tfrac{1}{2}\sigma^2) T}{\sigma\sqrt{T}}.$$

So $\{S_T > K\} = \{Z > -d_2\}$. We also introduce $d_1 := d_2 + \sigma\sqrt{T}$.

**Split the expectation.** Since $(S_T - K)^+ = (S_T - K)\, \mathbf{1}_{S_T > K}$,

$$\mathbb{E}^{\mathbb{Q}}\!\big[(S_T - K)^+\big] \;=\; \mathbb{E}^{\mathbb{Q}}\!\big[S_T\, \mathbf{1}_{S_T > K}\big] \;-\; K\, \mathbb{Q}(S_T > K). \tag{$\star$}$$

**Second piece — the probability term.** Using symmetry of the standard normal,

$$\mathbb{Q}(S_T > K) \;=\; \mathbb{Q}(Z > -d_2) \;=\; \mathbb{Q}(Z < d_2) \;=\; N(d_2).$$

**First piece — the stock-times-indicator term.** Write the expectation explicitly as a Gaussian integral and pull the deterministic factor $S_0\, e^{(r - \sigma^2/2) T}$ out:

$$\mathbb{E}^{\mathbb{Q}}\!\big[S_T\, \mathbf{1}_{Z > -d_2}\big] \;=\; \int_{-d_2}^{\infty} S_0\, e^{(r - \sigma^2/2) T + \sigma\sqrt{T}\, z}\, \varphi(z)\, dz,$$

where $\varphi(z) = \tfrac{1}{\sqrt{2\pi}}\, e^{-z^2/2}$ is the standard normal density. Combine the exponentials inside the integrand by completing the square in $z$:

$$\sigma\sqrt{T}\, z - \tfrac{z^2}{2} \;=\; -\tfrac{1}{2}\big(z^2 - 2\sigma\sqrt{T}\, z\big) \;=\; -\tfrac{1}{2}\big(z - \sigma\sqrt{T}\big)^2 + \tfrac{1}{2}\sigma^2 T.$$

Substitute and pull the constant $e^{\sigma^2 T / 2}$ outside the integral:

$$\mathbb{E}^{\mathbb{Q}}\!\big[S_T\, \mathbf{1}_{Z > -d_2}\big] \;=\; S_0\, e^{(r - \sigma^2/2) T + \sigma^2 T / 2}\, \int_{-d_2}^{\infty} \tfrac{1}{\sqrt{2\pi}}\, e^{-(z - \sigma\sqrt{T})^2 / 2}\, dz \;=\; S_0\, e^{r T}\, \int_{-d_2}^{\infty} \varphi\!\big(z - \sigma\sqrt{T}\big)\, dz.$$

Substitute $u = z - \sigma\sqrt{T}$, so $du = dz$ and the lower limit becomes $u = -d_2 - \sigma\sqrt{T} = -d_1$:

$$\mathbb{E}^{\mathbb{Q}}\!\big[S_T\, \mathbf{1}_{S_T > K}\big] \;=\; S_0\, e^{r T}\, \int_{-d_1}^{\infty} \varphi(u)\, du \;=\; S_0\, e^{r T}\, \mathbb{Q}(Z > -d_1) \;=\; S_0\, e^{r T}\, N(d_1).$$

**Combine.** Plug both pieces into $(\star)$:

$$\mathbb{E}^{\mathbb{Q}}\!\big[(S_T - K)^+\big] \;=\; S_0\, e^{r T}\, N(d_1) \;-\; K\, N(d_2).$$

**Discount.** Multiply by $e^{-r T}$ to obtain the time-zero call price:

$$C_0 \;=\; e^{-r T}\big[\, S_0\, e^{r T}\, N(d_1) - K\, N(d_2)\,\big] \;=\; S_0\, N(d_1) \;-\; K\, e^{-r T}\, N(d_2). \qquad \checkmark$$

This matches the Ch. 7 closed form at $t = 0$, with the same $d_1, d_2$. The argument lifts to general $t$ by replacing $T \to T - t$ and $S_0 \to S_t$ throughout, using the Markov property of $S$ under $\mathbb{Q}$. $\square$
:::

---

::: problem [Computation]
**Problem 8.3.** Numerically verify the closed-form call price by Monte Carlo simulation. Use $S_0 = 100$, $K = 100$, $T = 0.25$, $r = 0.05$, $\sigma = 0.20$. Write pseudocode to simulate $10^4$ samples of $S_T$ under $\mathbb{Q}$, compute the average of $\max(S_T - K, 0)$, discount by $e^{-r T}$, and compare with the closed-form value $\approx \$4.61$ (from Problem 7.3).
:::

::: solution
**Pseudocode.**

```
# Inputs
S_0   = 100.0
K     = 100.0
T     = 0.25
r     = 0.05
sigma = 0.20
N     = 10_000

# Draw N standard normal samples
Z = standard_normal_samples(N)

# Simulate terminal stock prices under Q
S_T = [ S_0 * exp((r - sigma^2 / 2) * T + sigma * sqrt(T) * Z_i) for Z_i in Z ]

# Compute discounted payoff average
payoffs        = [ max(S_i - K, 0) for S_i in S_T ]
call_estimate  = exp(-r * T) * mean(payoffs)

print(call_estimate)
```

**Expected output.** With $N = 10^4$, the Monte Carlo estimate is

$$\hat C_0 \;\approx\; 4.61 \;\pm\; \text{(Monte Carlo error)}.$$

The Monte Carlo standard error is approximately $\sigma_{\text{payoff}} / \sqrt{N}$, where $\sigma_{\text{payoff}}$ is the standard deviation of the discounted payoff samples. For an at-the-money short-dated call with $\sigma\sqrt{T} = 0.10$, a rough back-of-the-envelope gives $\sigma_{\text{payoff}} \approx 10$ dollars (the payoff is positive only when $S_T > K$, conditional on which it is order $S_0 \sigma\sqrt{T} \approx 10$), so the standard error is approximately $10 / \sqrt{10\,000} = 0.10$. The 95% confidence interval is therefore $\hat C_0 \pm 1.96 \cdot 0.10 \approx \hat C_0 \pm 0.20$.

The closed-form value $C_0 \approx 4.61$ from Problem 7.3 falls comfortably inside any reasonable realization of $\hat C_0 \pm 0.20$, confirming that the two methods agree. As $N$ is increased, $\hat C_0$ converges to $4.61$ at rate $1/\sqrt{N}$, the standard Monte Carlo rate. Practitioners typically use $N = 10^6$ to $10^7$ samples plus variance-reduction techniques (antithetic variates, control variates with the underlying $S_T$) to drive the error well below typical bid-ask spreads.

This computation is conceptually important: it is a direct *non-PDE* verification of the closed form. The pseudocode never references the Black-Scholes PDE, the heat equation, the convolution argument, or Feynman-Kac — it simply simulates the $\mathbb{Q}$-SDE and averages. The fact that this naive Monte Carlo recipe agrees with the closed form is empirical confirmation that the two routes in this chapter and Ch. 7 are computing the same quantity. $\square$
:::
