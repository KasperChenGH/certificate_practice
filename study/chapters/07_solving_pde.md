# Chapter 7 — Solving the PDE

## Goals

- Reduce the Black-Scholes partial differential equation to the constant-coefficient heat equation via an explicit change of variables.
- Solve the heat equation by convolution against its Gaussian fundamental solution (the heat kernel).
- Back-substitute through the chain of variable changes to recover the closed-form European call price $C(S, t) = S\, N(d_1) - K e^{-r(T - t)}\, N(d_2)$.
- Verify the closed form satisfies the terminal and boundary conditions of Ch. 6.
- Derive the European put formula from put-call parity, and state the dividend-adjusted formula.

## Prerequisites

- **Ch. 6** — the Black-Scholes PDE $V_t + \tfrac{1}{2}\sigma^2 S^2 V_{SS} + r S V_S - r V = 0$ on $(0, \infty) \times [0, T)$, together with the terminal condition $V(S, T) = (S - K)^+$, the absorbing boundary $C(0, t) = 0$, and the deep-ITM asymptote $C(S, t) \sim S - K e^{-r(T-t)}$ as $S \to \infty$.
- **Basic PDE theory** — the one-dimensional heat equation $u_\tau = u_{xx}$ on $\mathbb{R}$, its Gaussian fundamental solution, and the representation of solutions as convolutions of initial data against the heat kernel.
- **Calculus** — completing the square in a quadratic exponent, change-of-variables in a Gaussian integral, and the definition of the cumulative standard normal $N(x) = \int_{-\infty}^x \varphi(s)\, ds$ with $\varphi(s) = \tfrac{1}{\sqrt{2\pi}} e^{-s^2/2}$.

---

## Strategy

The Black-Scholes PDE has variable coefficients: the diffusion term $\tfrac{1}{2}\sigma^2 S^2 V_{SS}$ scales quadratically in $S$, the drift term $r S V_S$ scales linearly, and the discount term $- r V$ is constant. This $S$-dependence obscures the structural fact that — beneath the variable coefficients — the equation is *parabolic* and is locally equivalent to the simplest parabolic PDE imaginable, the constant-coefficient heat equation $\partial u / \partial \tau = \partial^2 u / \partial x^2$. Three substitutions remove the obstruction in succession. First, $x = \ln(S/K)$ converts the multiplicative scaling in $S$ into additive translation in $x$, eliminating the $S^2$ and $S$ prefactors. Second, the rescaling $\tau = \tfrac{1}{2}\sigma^2 (T - t)$ flips the backward equation into a forward equation and absorbs the $\sigma$ into the time variable. Third, factoring $u(x, \tau) = e^{\alpha x + \beta \tau}\, v(x, \tau)$ with carefully chosen $\alpha, \beta$ cancels the surviving first-order and zero-order terms, leaving the bare heat equation for $v$. The heat equation has a known closed-form Green's function, and convolving it against the transformed initial data gives an explicit integral that — after completing the square and recognizing two Gaussian integrals — evaluates to a difference of cumulative-normal values. Unwinding the three substitutions returns the Black-Scholes formula.

---

## Change of variables

We carry out the three substitutions in order. Let $V(S, t)$ denote the call price satisfying the BSM PDE.

### Substitution 1 — logarithmic spot and rescaled time

Define

$$x = \ln(S/K), \qquad \tau = \tfrac{1}{2}\sigma^2 (T - t), \qquad V(S, t) = K\, u(x, \tau).$$

::: where
- $x = \ln(S/K) \in \mathbb{R}$ — the *log-moneyness* of the option, dimensionless. As $S$ ranges over $(0, \infty)$, $x$ ranges over $(-\infty, \infty)$.
- $\tau = \tfrac{1}{2}\sigma^2 (T - t) \in [0, \tfrac{1}{2}\sigma^2 T]$ — rescaled time-to-expiry. Note that $\tau$ increases as $t$ decreases: $\tau = 0$ at $t = T$ and $\tau$ grows as we move backward toward $t = 0$.
- $K$ — strike, used as the unit of value so that $u = V/K$ is dimensionless.
- $u(x, \tau)$ — the call price expressed in strike units, as a function of log-moneyness and rescaled time.
:::

We compute the partial derivatives of $V$ in terms of those of $u$ via the chain rule. Since $S = K e^x$ and $t = T - 2\tau/\sigma^2$,

$$\frac{\partial}{\partial t} = -\tfrac{1}{2}\sigma^2 \frac{\partial}{\partial \tau}, \qquad \frac{\partial}{\partial S} = \frac{1}{S}\frac{\partial}{\partial x}, \qquad \frac{\partial^2}{\partial S^2} = \frac{1}{S^2}\left(\frac{\partial^2}{\partial x^2} - \frac{\partial}{\partial x}\right).$$

::: where
- $\partial / \partial t = -\tfrac{1}{2}\sigma^2\, \partial/\partial \tau$ — comes from $d\tau / dt = -\tfrac{1}{2}\sigma^2$.
- $\partial / \partial S = (1/S)\, \partial/\partial x$ — comes from $dx/dS = 1/S$.
- The second derivative picks up an extra $-\partial/\partial x$ from differentiating $1/S$.
:::

Substituting $V = K u$ into the BSM PDE and multiplying through by $1/K$:

$$-\tfrac{1}{2}\sigma^2 u_\tau + \tfrac{1}{2}\sigma^2 S^2 \cdot \frac{1}{S^2}\bigl(u_{xx} - u_x\bigr) + r S \cdot \frac{1}{S} u_x - r u = 0.$$

The $S$-dependence cancels exactly:

$$-\tfrac{1}{2}\sigma^2 u_\tau + \tfrac{1}{2}\sigma^2 \bigl(u_{xx} - u_x\bigr) + r u_x - r u = 0.$$

Dividing by $\tfrac{1}{2}\sigma^2$ and rearranging, with $k := 2 r / \sigma^2$,

$$\frac{\partial u}{\partial \tau} = \frac{\partial^2 u}{\partial x^2} + (k - 1)\frac{\partial u}{\partial x} - k u.$$

::: where
- $k = 2r/\sigma^2$ — a dimensionless ratio of the discount rate to the diffusion scale. Sometimes called the *cost-of-carry parameter* in this context.
- $(k - 1)\, u_x$ — a first-order *advection* term whose coefficient is constant in $(x, \tau)$.
- $- k u$ — a zero-order *reaction* term, also with constant coefficient.
- $u_\tau, u_x, u_{xx}$ — partial derivatives of $u$ with respect to the new variables.
:::

The variable coefficients of the original PDE are gone. The equation for $u$ is a constant-coefficient *convection-reaction-diffusion* equation on $\mathbb{R} \times [0, \tfrac{1}{2}\sigma^2 T]$, which is one substitution away from the bare heat equation.

### Substitution 2 — exponential factorization

To eliminate the $u_x$ and $u$ terms, we look for a multiplicative factor $e^{\alpha x + \beta \tau}$ that absorbs the lower-order terms when we factor $u$ as

$$u(x, \tau) = e^{\alpha x + \beta \tau}\, v(x, \tau).$$

::: where
- $\alpha, \beta \in \mathbb{R}$ — constants to be determined so that $v$ solves the bare heat equation.
- $v(x, \tau)$ — the transformed call price, after both substitutions. We will solve the heat equation for $v$ and then back-substitute.
:::

Compute the partial derivatives of $u$ in terms of those of $v$:

$$u_\tau = e^{\alpha x + \beta \tau}(\beta v + v_\tau),$$

$$u_x = e^{\alpha x + \beta \tau}(\alpha v + v_x),$$

$$u_{xx} = e^{\alpha x + \beta \tau}\bigl(\alpha^2 v + 2 \alpha v_x + v_{xx}\bigr).$$

Substituting into the intermediate PDE and dividing through by the common factor $e^{\alpha x + \beta \tau}$:

$$\beta v + v_\tau = \alpha^2 v + 2 \alpha v_x + v_{xx} + (k - 1)(\alpha v + v_x) - k v.$$

Collecting terms by derivative order,

$$v_\tau = v_{xx} + \bigl[2 \alpha + (k - 1)\bigr] v_x + \bigl[\alpha^2 + (k - 1)\alpha - k - \beta\bigr] v.$$

For $v$ to satisfy the bare heat equation $v_\tau = v_{xx}$, both bracketed coefficients must vanish:

$$2\alpha + (k - 1) = 0 \quad \Longrightarrow \quad \alpha = -\tfrac{1}{2}(k - 1),$$

$$\alpha^2 + (k - 1)\alpha - k - \beta = 0 \quad \Longrightarrow \quad \beta = \alpha^2 + (k - 1)\alpha - k.$$

Substituting $\alpha = -\tfrac{1}{2}(k - 1)$ into the second equation,

$$\beta = \tfrac{1}{4}(k - 1)^2 - \tfrac{1}{2}(k - 1)^2 - k = -\tfrac{1}{4}(k - 1)^2 - k.$$

::: where
- $\alpha = -\tfrac{1}{2}(k - 1)$ — chosen to cancel the first-order $v_x$ term.
- $\beta = -\tfrac{1}{4}(k - 1)^2 - k$ — chosen, after fixing $\alpha$, to cancel the zero-order $v$ term.
- Both constants depend on $k = 2r/\sigma^2$ alone — they encode the discount and drift of the original PDE.
:::

With these choices, $v(x, \tau)$ satisfies the heat equation:

$$\boxed{\;\frac{\partial v}{\partial \tau} = \frac{\partial^2 v}{\partial x^2}, \qquad (x, \tau) \in \mathbb{R} \times (0, \tfrac{1}{2}\sigma^2 T].\;}$$

The transformation chain — written compactly — is

$$V(S, t) \;\xrightarrow{V = K u}\; u(x, \tau) \;\xrightarrow{u = e^{\alpha x + \beta \tau} v}\; v(x, \tau),$$

with the convention that $x = \ln(S/K)$ and $\tau = \tfrac{1}{2}\sigma^2 (T - t)$.

---

## Heat-equation Green's function

The heat equation on $\mathbb{R}$ has a classical fundamental solution, the *Gaussian heat kernel*.

**Lemma (heat kernel).** The function

$$G(x, \tau) = \frac{1}{\sqrt{4 \pi \tau}}\, e^{-x^2 / (4 \tau)}$$

solves $\partial_\tau G = \partial_{xx} G$ for $\tau > 0$ and satisfies $G(\cdot, \tau) \to \delta_0$ as $\tau \downarrow 0$ in the distributional sense.

::: where
- $G(x, \tau)$ — heat kernel, the fundamental solution of $\partial_\tau v = \partial_{xx} v$ starting from a point mass at $x = 0$.
- $\sqrt{4 \pi \tau}$ — normalization constant ensuring $\int_{-\infty}^\infty G(x, \tau)\, dx = 1$ for all $\tau > 0$.
- $\delta_0$ — Dirac delta at the origin; the heat kernel concentrates at $x = 0$ as $\tau \downarrow 0$.
:::

**Verification.** We check $G_\tau = G_{xx}$ by direct computation. Take logarithms to organize the algebra: $\ln G = -\tfrac{1}{2}\ln(4\pi\tau) - x^2/(4\tau)$, so

$$\frac{G_\tau}{G} = -\frac{1}{2\tau} + \frac{x^2}{4\tau^2}, \qquad \frac{G_x}{G} = -\frac{x}{2\tau}, \qquad \frac{G_{xx}}{G} = -\frac{1}{2\tau} + \frac{x^2}{4\tau^2}.$$

The last identity uses $G_{xx} = (G_x)_x = G \cdot \bigl(- \tfrac{1}{2\tau}\bigr) + G_x \cdot \bigl(-\tfrac{x}{2\tau}\bigr) = -\frac{G}{2\tau} + \frac{x^2 G}{4\tau^2}$. Comparing the two expressions, $G_\tau / G = G_{xx} / G$, hence $G_\tau = G_{xx}$ for $\tau > 0$. $\square$

::: where
- $G_\tau, G_x, G_{xx}$ — partial derivatives of the heat kernel; computed by logarithmic differentiation.
- The cancellation $G_\tau/G = G_{xx}/G$ — both equal $-1/(2\tau) + x^2/(4\tau^2)$.
- $\tau > 0$ — required for $G$ to be smooth; the $\tau \downarrow 0$ limit is a distributional one (the delta function), not a pointwise one.
:::

The fact that $G$ concentrates at a delta function as $\tau \downarrow 0$ is the property that makes convolution against $G$ the solution operator of the initial-value problem: the convolution $v_0 * G(\cdot, \tau)$ smoothly transitions from $v_0$ at $\tau = 0$ to a $\tau$-smoothed version for $\tau > 0$. We take this on faith (it is standard PDE theory) and use it directly in the next section.

---

## Convolution against the call IC

We now determine the initial condition $v(x, 0)$ — i.e., the value of $v$ at $\tau = 0$, which corresponds to $t = T$, the expiration time — and convolve it against the heat kernel.

### Initial condition

The terminal condition on $V$ is $V(S, T) = (S - K)^+$. At $\tau = 0$:

$$V(S, T) = K\, u(x, 0) \quad \Longrightarrow \quad u(x, 0) = \frac{(S - K)^+}{K} = \left(\frac{S}{K} - 1\right)^+ = (e^x - 1)^+,$$

using $S = K e^x$. Then from $u = e^{\alpha x + \beta \tau} v$, at $\tau = 0$:

$$v(x, 0) = e^{-\alpha x}\, u(x, 0) = e^{-\alpha x} (e^x - 1)^+.$$

::: where
- $V(S, T) = (S - K)^+$ — terminal payoff of the European call (Ch. 6).
- $u(x, 0) = (e^x - 1)^+$ — the payoff written in log-moneyness coordinates and strike units.
- $v(x, 0) = e^{-\alpha x}(e^x - 1)^+$ — the heat-equation initial condition, after the exponential factorization.
- $(e^x - 1)^+ > 0$ iff $e^x > 1$ iff $x > 0$ — the support of the initial condition is the half-line $x > 0$.
:::

### Convolution

For $\tau > 0$, the solution of the heat equation with initial data $v(x, 0)$ is given by convolution with the heat kernel:

$$v(x, \tau) = \int_{-\infty}^\infty G(x - y, \tau)\, v(y, 0)\, dy = \int_{-\infty}^\infty \frac{1}{\sqrt{4\pi\tau}}\, e^{-(x - y)^2 / (4\tau)}\, v(y, 0)\, dy.$$

::: where
- $v(x, \tau)$ — solution of the heat equation at time $\tau$ with initial data $v(\cdot, 0)$.
- $G(x - y, \tau)$ — heat kernel centered at $y$; the convolution diffuses point sources of $v(y, 0)$ outward.
- $y$ — integration variable (the "source" coordinate at $\tau = 0$).
:::

Since $v(y, 0) = e^{-\alpha y}(e^y - 1)^+$ vanishes for $y \le 0$, the integration range collapses to $(0, \infty)$:

$$v(x, \tau) = \int_0^\infty \frac{1}{\sqrt{4\pi\tau}}\, e^{-(x - y)^2 / (4\tau)} \cdot e^{-\alpha y}(e^y - 1)\, dy.$$

Split the factor $(e^y - 1)$ to obtain two integrals:

$$v(x, \tau) = \underbrace{\int_0^\infty \frac{1}{\sqrt{4\pi\tau}}\, e^{-(x - y)^2 / (4\tau)} \cdot e^{(1 - \alpha) y}\, dy}_{=: I_1} \;-\; \underbrace{\int_0^\infty \frac{1}{\sqrt{4\pi\tau}}\, e^{-(x - y)^2 / (4\tau)} \cdot e^{-\alpha y}\, dy}_{=: I_2}.$$

::: where
- $I_1$ — integral of the heat kernel against $e^{(1 - \alpha)y}$ on $(0, \infty)$.
- $I_2$ — integral of the heat kernel against $e^{-\alpha y}$ on $(0, \infty)$.
- The split is permitted by linearity; both integrals are absolutely convergent for $\tau > 0$ (the Gaussian decay dominates the exponential growth in $y$).
:::

### Completing the square in $I_1$

Combine the exponents in $I_1$:

$$-\frac{(x - y)^2}{4\tau} + (1 - \alpha) y = -\frac{(x - y)^2 - 4\tau(1 - \alpha)y}{4\tau}.$$

Expand $(x - y)^2 = x^2 - 2xy + y^2$ and group in $y$:

$$(x - y)^2 - 4\tau(1 - \alpha)y = y^2 - 2\bigl[x + 2\tau(1 - \alpha)\bigr] y + x^2.$$

Complete the square in $y$: with $m_1 := x + 2\tau(1 - \alpha)$,

$$y^2 - 2 m_1 y + x^2 = (y - m_1)^2 - m_1^2 + x^2.$$

So the exponent becomes

$$-\frac{(y - m_1)^2}{4\tau} + \frac{m_1^2 - x^2}{4\tau}.$$

The constant term $\bigl(m_1^2 - x^2\bigr)/(4\tau)$ pulls out of the integral. Substituting $z = (y - m_1)/\sqrt{2\tau}$ — so that $dy = \sqrt{2\tau}\, dz$ and the lower limit $y = 0$ becomes $z = -m_1/\sqrt{2\tau}$ — gives

$$I_1 = e^{(m_1^2 - x^2)/(4\tau)} \cdot \int_{-m_1 / \sqrt{2\tau}}^\infty \frac{1}{\sqrt{2\pi}}\, e^{-z^2 / 2}\, dz = e^{(m_1^2 - x^2)/(4\tau)} \cdot N\!\left(\frac{m_1}{\sqrt{2\tau}}\right).$$

::: where
- $m_1 = x + 2\tau(1 - \alpha)$ — the *mean* of the Gaussian in $y$ after completing the square.
- $z = (y - m_1)/\sqrt{2\tau}$ — standardized integration variable; $\sqrt{2\tau}$ is the corresponding standard deviation.
- $N(\cdot)$ — cumulative standard normal: $N(a) = \int_{-\infty}^a \tfrac{1}{\sqrt{2\pi}} e^{-z^2/2}\, dz$. We use $\int_{-a}^\infty = N(a)$, valid by symmetry of the normal density.
- $e^{(m_1^2 - x^2)/(4\tau)}$ — the constant factor pulled out of the integral when completing the square.
:::

### Completing the square in $I_2$

The same procedure with $1 - \alpha$ replaced by $-\alpha$. Set $m_2 := x + 2\tau(-\alpha) = x - 2\tau\alpha$. Then

$$I_2 = e^{(m_2^2 - x^2)/(4\tau)} \cdot N\!\left(\frac{m_2}{\sqrt{2\tau}}\right).$$

::: where
- $m_2 = x - 2\tau\alpha$ — analogous shifted mean for the second integral.
- Same standardization and normal-tail identity as in $I_1$.
:::

### Closed form for $v$

Combining,

$$v(x, \tau) = e^{(m_1^2 - x^2)/(4\tau)} N\!\left(\frac{m_1}{\sqrt{2\tau}}\right) - e^{(m_2^2 - x^2)/(4\tau)} N\!\left(\frac{m_2}{\sqrt{2\tau}}\right).$$

::: where
- $v(x, \tau)$ — the solution of the heat equation with the transformed call's initial data.
- $m_1, m_2$ — shifted means defined above; both depend linearly on $x$ and $\tau$.
- The two exponential prefactors will simplify dramatically once we multiply by $e^{\alpha x + \beta \tau}$ to recover $u$.
:::

---

## Back-substitution

We now unwind the chain $v \to u \to V$.

### Recover $u(x, \tau)$

From $u = e^{\alpha x + \beta \tau} v$:

$$u(x, \tau) = e^{\alpha x + \beta \tau}\left[\,e^{(m_1^2 - x^2)/(4\tau)} N\!\left(\frac{m_1}{\sqrt{2\tau}}\right) - e^{(m_2^2 - x^2)/(4\tau)} N\!\left(\frac{m_2}{\sqrt{2\tau}}\right)\right].$$

Each exponential prefactor combines with $e^{\alpha x + \beta \tau}$ into a single exponential, which simplifies after substituting the values of $\alpha$, $\beta$, $m_1$, $m_2$. The algebra is mechanical: expand $m_i^2$, collect powers of $x$ and $\tau$, and use $\alpha = -\tfrac{1}{2}(k-1)$, $\beta = -\tfrac{1}{4}(k-1)^2 - k$. After simplification (a useful exercise — Problem 7.1's optional addendum), the first prefactor becomes $e^x = S/K$ and the second becomes $e^{-k\tau} = e^{-r(T-t)}$:

$$u(x, \tau) = \frac{S}{K} N\!\left(\frac{m_1}{\sqrt{2\tau}}\right) - e^{-r(T-t)} N\!\left(\frac{m_2}{\sqrt{2\tau}}\right).$$

::: where
- $S/K = e^x$ — back-substitution of the spot in strike units.
- $e^{-k\tau} = e^{-r(T-t)}$ — uses $k\tau = (2r/\sigma^2) \cdot \tfrac{1}{2}\sigma^2(T-t) = r(T-t)$.
- The two normal-CDF arguments $m_i / \sqrt{2\tau}$ now play the role of $d_1$ and $d_2$.
:::

### Recover $V(S, t)$ and identify $d_1, d_2$

Multiplying by $K$ to obtain $V = K u$,

$$V(S, t) = S \cdot N\!\left(\frac{m_1}{\sqrt{2\tau}}\right) - K e^{-r(T-t)} \cdot N\!\left(\frac{m_2}{\sqrt{2\tau}}\right).$$

It remains to translate $m_1/\sqrt{2\tau}$ and $m_2/\sqrt{2\tau}$ back to $(S, t)$. We have

$$\frac{m_1}{\sqrt{2\tau}} = \frac{x + 2\tau(1 - \alpha)}{\sqrt{2\tau}}, \qquad \frac{m_2}{\sqrt{2\tau}} = \frac{x - 2\tau\alpha}{\sqrt{2\tau}}.$$

Using $x = \ln(S/K)$, $\tau = \tfrac{1}{2}\sigma^2(T-t)$, $\alpha = -\tfrac{1}{2}(k-1)$, $k = 2r/\sigma^2$, so that $2\tau(1 - \alpha) = \tau(k + 1) = \tfrac{1}{2}\sigma^2(T-t) \cdot (2r/\sigma^2 + 1) = (r + \tfrac{1}{2}\sigma^2)(T-t)$, and $\sqrt{2\tau} = \sigma\sqrt{T-t}$:

$$\frac{m_1}{\sqrt{2\tau}} = \frac{\ln(S/K) + (r + \tfrac{1}{2}\sigma^2)(T-t)}{\sigma\sqrt{T-t}} =: d_1.$$

Similarly $2\tau(-\alpha) = \tau(k - 1) = (r - \tfrac{1}{2}\sigma^2)(T-t)$, hence

$$\frac{m_2}{\sqrt{2\tau}} = \frac{\ln(S/K) + (r - \tfrac{1}{2}\sigma^2)(T-t)}{\sigma\sqrt{T-t}} = d_1 - \sigma\sqrt{T-t} =: d_2.$$

### Final closed form

$$\boxed{\;C(S, t) = S\, N(d_1) - K e^{-r(T - t)}\, N(d_2),\;}$$

where

$$d_1 = \frac{\ln(S/K) + (r + \tfrac{1}{2}\sigma^2)(T - t)}{\sigma\sqrt{T - t}}, \qquad d_2 = d_1 - \sigma\sqrt{T - t}.$$

::: where
- $C(S, t)$ — no-arbitrage time-$t$ price of the European call with strike $K$ and maturity $T$ on a non-dividend-paying stock.
- $S$ — current spot price at time $t$.
- $K$ — strike.
- $r$ — constant continuously-compounded risk-free rate.
- $\sigma$ — constant instantaneous volatility of the stock.
- $T - t$ — time remaining to expiry.
- $N(\cdot)$ — cumulative standard normal CDF.
:::

::: where
- $d_1$ — numerator $\ln(S/K) + (r + \tfrac{1}{2}\sigma^2)(T-t)$ is the *risk-neutral* log-moneyness, lifted by half the integrated variance.
- $d_2 = d_1 - \sigma\sqrt{T-t}$ — same numerator with $\tfrac{1}{2}\sigma^2$ replaced by $-\tfrac{1}{2}\sigma^2$; the *physical* log-moneyness in the risk-neutral measure.
- $\sigma\sqrt{T-t}$ — total volatility (one standard deviation of log-returns over the remaining horizon).
- $N(d_1)$ — *delta* of the call (Ch. 9); $N(d_2)$ — risk-neutral probability of finishing in-the-money (Ch. 8).
:::

This is the **Black-Scholes formula** for the European call.

---

## Verification

We check that $C(S, t) = S N(d_1) - K e^{-r(T-t)} N(d_2)$ satisfies the PDE and the boundary conditions of Ch. 6.

### PDE (sketch)

The strategy is direct differentiation. Define $\varphi(z) = \tfrac{1}{\sqrt{2\pi}} e^{-z^2 / 2}$, the standard normal density. The key identity is

$$S\, \varphi(d_1) = K e^{-r(T - t)} \varphi(d_2).$$

::: where
- $\varphi(z)$ — standard normal probability density, $N'(z) = \varphi(z)$.
- The identity $S \varphi(d_1) = K e^{-r(T-t)} \varphi(d_2)$ — follows from $d_2 = d_1 - \sigma\sqrt{T-t}$ by direct algebra on $\exp(-d_1^2/2)$ vs. $\exp(-d_2^2/2)$. See Problem 7.2.
:::

Using this identity, the *cross-terms* that arise when computing $C_S$, $C_{SS}$, $C_t$ all cancel in pairs. The surviving terms reorganize into the BSM PDE. The full computation is mechanical and appears in Ch. 9 (when we compute the Greeks $\Delta = C_S = N(d_1)$, $\Gamma = C_{SS} = \varphi(d_1)/(S\sigma\sqrt{T-t})$, $\Theta = C_t$); we defer the algebra.

### Terminal condition: $C(S, T) = (S - K)^+$

As $t \to T$, $\tau = \tfrac{1}{2}\sigma^2(T-t) \to 0$, and $\sigma\sqrt{T-t} \to 0$. The behavior of $d_1, d_2$ depends on the sign of $\ln(S/K)$:

- If $S > K$ (in-the-money): $\ln(S/K) > 0$, so $d_1, d_2 \to +\infty$, hence $N(d_1), N(d_2) \to 1$, and $C(S, t) \to S - K e^{0} = S - K$.
- If $S < K$ (out-of-the-money): $\ln(S/K) < 0$, so $d_1, d_2 \to -\infty$, hence $N(d_1), N(d_2) \to 0$, and $C(S, t) \to 0$.
- If $S = K$ (at-the-money): a more careful expansion (using $\ln(S/K) = 0$ and $\sigma\sqrt{T-t} \to 0$) shows $C(K, t) \to 0$ as well, consistent with $(K - K)^+ = 0$.

Combined: $C(S, T) = \max(S - K, 0) = (S - K)^+$, the call payoff. $\checkmark$

### Lower boundary: $C(0, t) = 0$

As $S \to 0$, $\ln(S/K) \to -\infty$. For fixed $T - t > 0$, the term $(r + \tfrac{1}{2}\sigma^2)(T-t)$ is bounded, so $d_1 \to -\infty$ and likewise $d_2 \to -\infty$. Therefore $N(d_1), N(d_2) \to 0$, and the leading term in $C(S, t)$ is

$$C(S, t) = S \cdot N(d_1) - K e^{-r(T-t)} \cdot N(d_2) \to 0 \cdot 0 - K e^{-r(T-t)} \cdot 0 = 0.$$

More rigorously, $S \cdot N(d_1) \to 0$ because $N(d_1) \to 0$ at a Gaussian rate while $S \to 0$ only linearly. $\checkmark$

### Upper asymptote: $C(S, t) \sim S - K e^{-r(T - t)}$ as $S \to \infty$

As $S \to \infty$, $\ln(S/K) \to +\infty$, so $d_1, d_2 \to +\infty$, hence $N(d_1), N(d_2) \to 1$:

$$C(S, t) \to S \cdot 1 - K e^{-r(T-t)} \cdot 1 = S - K e^{-r(T-t)}.$$

The ratio $C(S, t) / (S - K e^{-r(T-t)}) \to 1$, confirming the asymptotic equivalence stated in Ch. 6. $\checkmark$

---

## Put formula

The put price follows from the call price by **put-call parity** (Ch. 5):

$$C(S, t) - P(S, t) = S - K e^{-r(T - t)}.$$

Rearranging, $P = C - S + K e^{-r(T-t)}$. Substituting the closed-form call:

$$P(S, t) = S\, N(d_1) - K e^{-r(T-t)}\, N(d_2) - S + K e^{-r(T-t)}.$$

Group: $S\bigl[N(d_1) - 1\bigr] + K e^{-r(T-t)}\bigl[1 - N(d_2)\bigr]$. Using the symmetry of the standard normal, $1 - N(d) = N(-d)$:

$$\boxed{\;P(S, t) = K e^{-r(T - t)}\, N(-d_2) - S\, N(-d_1),\;}$$

with the same $d_1, d_2$ as in the call formula.

::: where
- $P(S, t)$ — no-arbitrage time-$t$ price of the European put with strike $K$ and maturity $T$.
- $N(-d_i) = 1 - N(d_i)$ — symmetry of the standard normal CDF.
- $-N(d_1) S$, $K e^{-r(T-t)} N(-d_2)$ — the put-side analogs of the call's two terms, with the signs and the CDF arguments mirrored.
:::

A one-paragraph derivation in words: a portfolio long one call and short one put pays $S_T - K$ at expiration, which is the payoff of a forward contract with delivery price $K$. The forward has time-$t$ value $S - K e^{-r(T-t)}$ by static replication (Ch. 5). Solving for $P$ and substituting the closed-form call yields the put formula. The flip from $N(d_i)$ to $N(-d_i)$ is the analytical signature of the put's reversed payoff structure — the put pays off when $S_T < K$, dual to the call's $S_T > K$.

---

## Continuous dividends ($q > 0$)

For a stock paying a continuous dividend yield $q \ge 0$, the BSM PDE becomes (Ch. 6)

$$V_t + \tfrac{1}{2}\sigma^2 S^2 V_{SS} + (r - q) S V_S - r V = 0,$$

with terminal condition $V(S, T) = (S - K)^+$ for a call. Repeating the change-of-variables analysis with $r$ replaced by $r - q$ in the *drift* coefficient — but leaving the discount term $- r V$ unchanged — produces a modified dimensionless parameter $\tilde k = 2(r - q)/\sigma^2$ in the exponential factorization. After working through the same convolution argument, the closed form is

$$\boxed{\;C(S, t) = S e^{-q(T - t)}\, N(d_1) - K e^{-r(T - t)}\, N(d_2),\;}$$

where

$$d_1 = \frac{\ln(S/K) + (r - q + \tfrac{1}{2}\sigma^2)(T - t)}{\sigma\sqrt{T - t}}, \qquad d_2 = d_1 - \sigma\sqrt{T - t}.$$

::: where
- $q \ge 0$ — continuous dividend yield (constant).
- $S e^{-q(T-t)}$ — the dividend-adjusted forward present-value of the share; replicating one share at $T$ requires only $e^{-q(T-t)}$ shares today via continuous reinvestment of dividends.
- $r - q$ — the *net cost of carry*, replacing $r$ in the drift of the log-moneyness.
- $K e^{-r(T-t)}$ — present value of the strike, still discounted at $r$ (not $r - q$) because the strike is a *cash* obligation, not a share obligation.
- $\tilde k = 2(r - q)/\sigma^2$ — the dimensionless ratio that plays the role of $k$ in the dividend-adjusted analysis.
:::

Derivation outline: substitute $\tilde k = 2(r - q)/\sigma^2$ for $k$ in the change-of-variables block, repeat the convolution argument verbatim, and observe that $k\tau = r(T-t)$ is no longer the only place where the discount appears — the prefactor $e^{x}$ in $u$ now becomes $e^{x - q(T-t)} = (S/K) e^{-q(T-t)}$, yielding the $S e^{-q(T-t)}$ leading coefficient. The strike's $e^{-r(T-t)}$ discount survives because the $- r V$ term in the PDE is unchanged.

The put formula extends analogously by put-call parity (with the dividend-adjusted forward $S e^{-q(T-t)} - K e^{-r(T-t)}$):

$$P(S, t) = K e^{-r(T - t)} N(-d_2) - S e^{-q(T - t)} N(-d_1).$$

---

## Practice

**Problem 7.1 [Conceptual].** Why does the transformation $V(S, t) = K\, u(x, \tau)$ remove the constant $K$ from the heat-equation form? What other transformations could you choose instead, and why is this the natural one?

**Solution.** The value function $V$ has units of dollars and depends parametrically on the strike $K$, which is also a dollar amount. Dividing by $K$ makes $u = V/K$ *dimensionless* — a pure number in strike units. The BSM PDE is linear and homogeneous in $V$ (every term has $V$ to the first power), so scaling $V$ by an overall constant does not alter the structure of the PDE; it merely strips the constant from the equation. One could choose other scalings — for instance, $V/S$ would also be dimensionless — but $V/K$ is the *canonical* choice for three reasons. First, the strike $K$ is a fixed parameter while $S$ is the spatial variable; dividing by $S$ would introduce additional terms in the chain rule and complicate the change of variables. Second, the call payoff in strike units, $(S - K)^+/K = (S/K - 1)^+$, depends on the dimensionless quantity $S/K$ alone, which suggests immediately the further variable $x = \ln(S/K)$. The pair $(V/K, S/K)$ is the natural reduction of the problem to dimensionless form. Third, the boundary conditions in strike units become $u(0, \tau)$-style conditions — for example, $u(x, 0) = (e^x - 1)^+$, a function of $x$ alone, with no residual $K$-dependence — which is exactly what is needed to absorb $K$ into the variable $x$ rather than leaving it as a coefficient in the PDE.

---

**Problem 7.2 [Derivation].** Verify by direct differentiation that the closed-form call formula $C(S, t) = S\, N(d_1) - K e^{-r(T - t)}\, N(d_2)$ satisfies the Black-Scholes PDE $C_t + \tfrac{1}{2}\sigma^2 S^2 C_{SS} + r S C_S - r C = 0$.

**Solution.** We will need the auxiliary identity

$$S\, \varphi(d_1) = K e^{-r(T - t)}\, \varphi(d_2), \qquad \varphi(z) = \tfrac{1}{\sqrt{2\pi}}\, e^{-z^2/2}.$$

*Proof of the identity.* From $d_2 = d_1 - \sigma\sqrt{T-t}$,

$$d_1^2 - d_2^2 = (d_1 - d_2)(d_1 + d_2) = \sigma\sqrt{T-t} \cdot (2 d_1 - \sigma\sqrt{T-t}) = 2 d_1 \sigma\sqrt{T-t} - \sigma^2(T-t).$$

Substituting $d_1 = [\ln(S/K) + (r + \tfrac{1}{2}\sigma^2)(T-t)]/[\sigma\sqrt{T-t}]$:

$$2 d_1 \sigma\sqrt{T-t} = 2\ln(S/K) + 2(r + \tfrac{1}{2}\sigma^2)(T-t) = 2\ln(S/K) + 2 r(T-t) + \sigma^2(T-t).$$

Therefore

$$d_1^2 - d_2^2 = 2\ln(S/K) + 2 r(T-t).$$

Hence $\tfrac{1}{2}(d_2^2 - d_1^2) = -\ln(S/K) - r(T-t)$, so

$$\varphi(d_2) / \varphi(d_1) = e^{(d_1^2 - d_2^2)/2} = e^{\ln(S/K) + r(T-t)} = (S/K)\, e^{r(T-t)},$$

which rearranges to $K e^{-r(T-t)} \varphi(d_2) = S\, \varphi(d_1)$. $\checkmark$

*Compute $C_S$ (delta).* Using $\partial d_1/\partial S = \partial d_2/\partial S = 1/(S\sigma\sqrt{T-t})$ and the chain rule,

$$C_S = N(d_1) + S \varphi(d_1) \cdot \frac{1}{S\sigma\sqrt{T-t}} - K e^{-r(T-t)} \varphi(d_2) \cdot \frac{1}{S\sigma\sqrt{T-t}}.$$

The cross-terms cancel by the identity: $S\varphi(d_1) = K e^{-r(T-t)} \varphi(d_2)$. Hence

$$C_S = N(d_1).$$

*Compute $C_{SS}$ (gamma).* From $C_S = N(d_1)$,

$$C_{SS} = \varphi(d_1) \cdot \frac{\partial d_1}{\partial S} = \frac{\varphi(d_1)}{S\sigma\sqrt{T-t}}.$$

*Compute $C_t$ (theta).* The time derivatives of $d_1, d_2$ are

$$\frac{\partial d_1}{\partial t} = -\frac{(r + \tfrac{1}{2}\sigma^2)}{\sigma\sqrt{T-t}} + \frac{\ln(S/K) + (r + \tfrac{1}{2}\sigma^2)(T-t)}{\sigma} \cdot \frac{1}{2(T-t)^{3/2}}.$$

Differentiating $C$ in $t$, again the cross-terms involving $\partial d_i/\partial t$ cancel via $S\varphi(d_1) = K e^{-r(T-t)} \varphi(d_2)$, leaving only the term from differentiating $e^{-r(T-t)}$ and the term involving $\partial(d_1 - d_2)/\partial t$:

$$C_t = -\frac{S \varphi(d_1) \sigma}{2\sqrt{T-t}} - r K e^{-r(T-t)} N(d_2).$$

*Substitute into the PDE.* Compute each term:

$$r S C_S = r S\, N(d_1),$$

$$\tfrac{1}{2}\sigma^2 S^2 C_{SS} = \tfrac{1}{2}\sigma^2 S^2 \cdot \frac{\varphi(d_1)}{S\sigma\sqrt{T-t}} = \frac{S\sigma \varphi(d_1)}{2\sqrt{T-t}},$$

$$r C = r S N(d_1) - r K e^{-r(T-t)} N(d_2).$$

Adding $C_t + \tfrac{1}{2}\sigma^2 S^2 C_{SS} + r S C_S - r C$:

$$\left[-\frac{S\sigma\varphi(d_1)}{2\sqrt{T-t}} - r K e^{-r(T-t)} N(d_2)\right] + \frac{S\sigma\varphi(d_1)}{2\sqrt{T-t}} + r S N(d_1) - \left[r S N(d_1) - r K e^{-r(T-t)} N(d_2)\right] = 0.$$

Every term cancels in pairs:

- $-\tfrac{S\sigma\varphi(d_1)}{2\sqrt{T-t}}$ (from $C_t$) cancels $+\tfrac{S\sigma\varphi(d_1)}{2\sqrt{T-t}}$ (from $\tfrac{1}{2}\sigma^2 S^2 C_{SS}$);
- $-r K e^{-r(T-t)} N(d_2)$ (from $C_t$) cancels $+ r K e^{-r(T-t)} N(d_2)$ (from $-rC$);
- $+ r S N(d_1)$ (from $r S C_S$) cancels $- r S N(d_1)$ (from $-rC$).

Hence the PDE holds. $\square$

---

**Problem 7.3 [Computation].** Price an at-the-money European call on a non-dividend-paying stock: $S = K = 100$, $T - t = 0.25$ (three months), $r = 0.05$, $q = 0$, $\sigma = 0.20$. Compute $d_1$, $d_2$, $N(d_1)$, $N(d_2)$, and $C$ to two decimal places.

**Solution.**

*Step 1 — $d_1$.* With $\ln(S/K) = \ln 1 = 0$ and $r + \tfrac{1}{2}\sigma^2 = 0.05 + 0.02 = 0.07$:

$$d_1 = \frac{0 + 0.07 \cdot 0.25}{0.20 \cdot \sqrt{0.25}} = \frac{0.0175}{0.20 \cdot 0.5} = \frac{0.0175}{0.10} = 0.175.$$

*Step 2 — $d_2$.* $d_2 = d_1 - \sigma\sqrt{T-t} = 0.175 - 0.10 = 0.075.$

*Step 3 — $N(d_1), N(d_2)$.* From standard normal tables (or a series expansion of $N$ around $0$):

$$N(0.175) \approx 0.5694, \qquad N(0.075) \approx 0.5299.$$

*Step 4 — Discount factor.* $e^{-r(T-t)} = e^{-0.05 \cdot 0.25} = e^{-0.0125} \approx 0.9876$.

*Step 5 — Call price.*

$$C = S\, N(d_1) - K e^{-r(T-t)}\, N(d_2) = 100 \cdot 0.5694 - 100 \cdot 0.9876 \cdot 0.5299.$$

Compute:

- $100 \cdot 0.5694 = 56.94$.
- $100 \cdot 0.9876 \cdot 0.5299 \approx 100 \cdot 0.5233 = 52.33$.
- $C \approx 56.94 - 52.33 = 4.61$.

**The ATM three-month call is worth approximately $\$4.61$.**

A useful sanity check: for an at-the-money call, the Brenner-Subrahmanyam approximation gives $C \approx 0.4\, S\, \sigma\sqrt{T-t} = 0.4 \cdot 100 \cdot 0.10 = 4.00$. Our exact answer $4.61$ exceeds this because the approximation ignores the interest-rate contribution (the term $(r + \tfrac{1}{2}\sigma^2)(T-t)$ in $d_1$). Setting $r = 0$ in the formula gives $C \approx 3.99$, in close agreement with the approximation. $\square$
