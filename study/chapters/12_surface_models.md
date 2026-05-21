# Chapter 12 — Surface Models

## Goals

This chapter surveys four major surface models used in derivatives pricing and smile fitting: Dupire local volatility, Heston stochastic volatility, SABR, and SVI. Each model is stated with its governing SDE (or parameterization) and a table of parameter interpretations. No derivations are given — the goal is to understand what each model says, what parameters control it, and when practitioners reach for it.

## Prerequisites

- Chapter 3 — Stochastic differential equations (Itô's lemma, risk-neutral measure, Brownian motion).
- Chapter 11 — The implied volatility surface (smile, skew, term structure).

## Dupire local volatility (1994)

A natural first attempt at matching the observed vanilla surface exactly is to allow the diffusion coefficient in the BSM SDE to depend on the current spot level and time. Dupire's insight is that for *any* arbitrage-free call price surface $C(K, T)$, there exists a unique deterministic function $\sigma_{\text{loc}}(S, t)$ — the *local volatility* — such that the model

$$dS_t = r S_t\, dt + \sigma_{\text{loc}}(S_t, t)\, S_t\, d\tilde W_t$$

under the risk-neutral measure $\mathbb{Q}$ prices every vanilla call at exactly its market price. The model has one source of randomness, so it is still complete, and the local-vol surface acts as a non-parametric fit to the entire smile surface simultaneously.

where:
- $S_t$ — spot price at time $t$
- $r$ — continuously compounded risk-free rate
- $\sigma_{\text{loc}}(S_t, t)$ — local volatility, a deterministic function of spot and time
- $\tilde W_t$ — standard Brownian motion under $\mathbb{Q}$

The local-vol function can be backed out directly from observed call prices via the **Dupire formula** (stated without proof):

$$\sigma_{\text{loc}}^2(K, T) = \frac{\partial C/\partial T + r K\, \partial C/\partial K}{\tfrac{1}{2} K^2\, \partial^2 C/\partial K^2}$$

where:
- $C(K, T)$ — market price of a European call with strike $K$ and expiry $T$
- $\partial C/\partial T$ — calendar spread sensitivity (time derivative of the call surface)
- $\partial C/\partial K$ — delta sensitivity with respect to strike
- $\partial^2 C/\partial K^2$ — convexity of the call surface in strike (proportional to the risk-neutral density)

**Remark.** Local volatility fits today's surface exactly by construction. However, it suffers from poor forward dynamics — the *forward skew problem*: as the spot evolves, the future smile implied by the model tends to flatten unrealistically. Empirically, skews tend to persist with roughly stable shapes over time; only stochastic-volatility or jump-diffusion models can reproduce this behaviour. Local vol over-fits the static snapshot at the cost of forward-looking realism.

## Heston stochastic volatility (1993)

Heston introduces a second source of randomness by letting the variance $v_t$ evolve stochastically. The spot and variance are driven by correlated Brownian motions, so the model is incomplete (perfect hedging of volatility risk requires an additional instrument), but it can capture the skew and its persistence over time far more realistically than local vol.

The model is governed by two coupled SDEs under $\mathbb{Q}$:

$$dS_t = r S_t\, dt + \sqrt{v_t}\, S_t\, dW_t^1$$

where:
- $S_t$ — spot price
- $r$ — risk-free rate
- $v_t$ — instantaneous variance (so instantaneous volatility is $\sqrt{v_t}$)
- $W_t^1$ — first standard Brownian motion under $\mathbb{Q}$

$$dv_t = \kappa(\theta - v_t)\, dt + \xi\, \sqrt{v_t}\, dW_t^2$$

where:
- $v_t$ — instantaneous variance
- $\kappa$ — speed of mean reversion; how fast $v_t$ is pulled back toward $\theta$
- $\theta$ — long-run (unconditional) variance; the level $v_t$ reverts to
- $\xi$ — volatility-of-volatility (vol-of-vol); controls the dispersion of $v_t$
- $W_t^2$ — second standard Brownian motion under $\mathbb{Q}$

The two Brownian motions satisfy $\langle dW^1, dW^2 \rangle = \rho\, dt$, so correlation $\rho$ couples spot moves to variance moves — negative $\rho$ produces a downward skew consistent with equity markets.

| Symbol | Meaning |
|--------|---------|
| $v_0$ | Initial variance |
| $\kappa$ | Mean-reversion speed |
| $\theta$ | Long-run variance |
| $\xi$ | Volatility-of-volatility |
| $\rho$ | Spot-vol correlation |

**Remark.** The Heston model admits a semi-closed-form solution for European option prices via characteristic functions and Fourier inversion, making calibration computationally tractable. It is one of the most widely used models for equity derivative pricing because it captures the skew, smile curvature, and term structure of implied volatility simultaneously, with dynamics that evolve realistically forward in time.

## SABR (Hagan et al., 2002)

SABR (Stochastic Alpha Beta Rho) models the forward price $F_t$ rather than the spot, making it natural for interest-rate and FX products where forwards are the primary traded quantity. The stochastic volatility $\alpha_t$ is itself lognormal, and the CEV exponent $\beta$ controls the backbone — the relationship between the at-the-money volatility level and the forward level.

Under the forward measure, the two coupled SDEs are:

$$dF_t = \alpha_t\, F_t^\beta\, dW_t^1$$

where:
- $F_t$ — forward price at time $t$
- $\alpha_t$ — stochastic volatility process (has units of vol when $\beta = 1$)
- $\beta$ — CEV exponent; determines how vol scales with the forward level
- $W_t^1$ — first standard Brownian motion

$$d\alpha_t = \nu\, \alpha_t\, dW_t^2$$

where:
- $\alpha_t$ — stochastic volatility; evolves as a driftless geometric Brownian motion
- $\nu$ — volatility-of-volatility; controls how much $\alpha_t$ itself fluctuates
- $W_t^2$ — second standard Brownian motion

The two Brownian motions satisfy $\langle dW^1, dW^2 \rangle = \rho\, dt$.

| Symbol | Meaning |
|--------|---------|
| $\alpha$ | Initial volatility level |
| $\beta$ | Backbone parameter, $\beta \in [0, 1]$ (0 = normal, 1 = lognormal, between = CEV) |
| $\rho$ | Forward-vol correlation |
| $\nu$ | Volatility-of-volatility |

**Remark.** SABR is the industry standard in interest-rate (swaptions, caps) and FX option markets. Hagan et al. derived a closed-form approximation that expresses the implied volatility smile as an analytic function of $(\alpha, \beta, \rho, \nu, F, K, T)$, enabling fast calibration. The model captures the smile shape and its evolution with the forward level in a way that is intuitive for practitioners.

## SVI parameterization (Gatheral, 2004)

SVI (Stochastic Volatility Inspired) is not a dynamic model with an SDE — it is a direct, parametric fit to the implied variance smile at a fixed maturity. Rather than specifying how $S_t$ evolves, SVI specifies what the total implied variance slice $w(k)$ looks like as a function of log-moneyness $k$.

The parameterization is:

$$w(k) = a + b\, \big[\rho\, (k - m) + \sqrt{(k - m)^2 + \sigma^2}\,\big]$$

where $w = \sigma_{\text{IV}}^2(K, T) \cdot T$ is the total implied variance and $k = \ln(K/F)$ is the log-moneyness.

where:
- $w(k)$ — total implied variance at log-moneyness $k$; equals $\sigma_{\text{IV}}^2 \cdot T$
- $k = \ln(K/F)$ — log-moneyness; $k < 0$ for OTM puts, $k > 0$ for OTM calls
- $a$ — overall variance level (vertical shift of the smile)
- $b$ — wing slope; controls how steeply the smile rises in the wings
- $\rho$ — tilt parameter; $\rho < 0$ tilts the smile so the left wing rises more steeply (equity skew)
- $m$ — horizontal shift of the smile center in log-moneyness space
- $\sigma$ — curvature parameter; larger $\sigma$ gives a rounder bottom to the smile

| Symbol | Meaning |
|--------|---------|
| $a$ | Overall variance level |
| $b$ | Wing slope |
| $\rho$ | Tilt / skew direction, $\rho \in [-1, 1]$ |
| $m$ | Center horizontal shift |
| $\sigma$ | Curvature parameter (rounded-bottom controller) |

**Remark.** SVI is not a dynamic model — it has no SDE and implies nothing about how prices evolve over time. It is purely a fit to the static smile at one maturity at a time. Despite this limitation, it is extremely popular in equity index option markets because five parameters per maturity slice capture the smile shape accurately, the fit is fast, and the functional form can be shown to be free of butterfly arbitrage under mild constraints on the parameters.

## Comparison

Each model targets a different point on the trade-off between fit quality, tractability, and dynamic realism.

| Model | Fits surface? | Has dynamics? | Best for |
|-------|---------------|---------------|----------|
| Local Vol | Exact | Poor | Vanilla calibration |
| Heston | Approximate | Good (Markov) | Equity exotics |
| SABR | Approximate | Good | Rates, FX |
| SVI | Exact (per maturity) | No | Smile fitting |

Local vol fits perfectly but is widely regarded as a poor dynamic model; Heston and SABR trade exact fit for realistic future dynamics; SVI sacrifices dynamics entirely to achieve a simple, robust fit to today's smile. In practice, combinations are used — for example, calibrating a Heston model to the surface and using SVI as an interpolation tool between modeled strikes.

## Practice

**Problem 12.1 [Conceptual].** Why does local volatility produce poor forward dynamics, even though it fits today's surface exactly?

**Solution.** Local volatility encodes today's surface entirely into a deterministic function $\sigma_{\text{loc}}(S, t)$. As time evolves and the spot moves, the model's *future* skew — the IV surface as seen at a later date — is dictated entirely by this deterministic function. In practice, future skews observed under local vol tend to flatten out unrealistically: the model predicts that as the spot drifts, the smile will smooth away. Empirically, real skews tend to persist with similar shapes over time — a property that only stochastic-volatility or jump-diffusion models can capture, because they carry an independent source of randomness that regenerates the skew continuously. The deterministic function over-fits today's observed surface at the cost of future predictive realism. This is the *forward skew problem*: local vol matches today's prices perfectly but predicts unrealistic future smile dynamics.

---

**Problem 12.2 [Computation].** For SVI with $a = 0.04$, $b = 0.4$, $\rho = -0.5$, $m = 0$, $\sigma = 0.1$, compute the total implied variance $w(k)$ and the implied volatility $\sigma_{\text{IV}}$ at $k = -0.1$, $k = 0$, and $k = 0.1$. (Use $T = 1$ to extract IV from $w = \sigma_{\text{IV}}^2 T$.)

**Solution.**

Recall $w(k) = 0.04 + 0.4\,[-0.5\,(k - 0) + \sqrt{(k - 0)^2 + 0.01}]$, i.e., $w(k) = 0.04 + 0.4\,[-0.5k + \sqrt{k^2 + 0.01}]$.

- $k = 0$:

$$w(0) = 0.04 + 0.4\,\big[-0.5 \cdot 0 + \sqrt{0 + 0.01}\big] = 0.04 + 0.4 \cdot 0.1 = 0.04 + 0.04 = 0.08$$

So $\sigma_{\text{IV}}(0) = \sqrt{0.08} \approx 0.283$ (28.3%).

- $k = -0.1$:

$$w(-0.1) = 0.04 + 0.4\,\big[-0.5 \cdot (-0.1) + \sqrt{0.01 + 0.01}\big] = 0.04 + 0.4\,\big[0.05 + \sqrt{0.02}\big]$$

$$= 0.04 + 0.4\,\big[0.05 + 0.1414\big] = 0.04 + 0.4 \cdot 0.1914 \approx 0.04 + 0.0766 = 0.1166$$

So $\sigma_{\text{IV}}(-0.1) \approx \sqrt{0.1166} \approx 0.341$ (34.1%).

- $k = +0.1$:

$$w(0.1) = 0.04 + 0.4\,\big[-0.5 \cdot 0.1 + \sqrt{0.01 + 0.01}\big] = 0.04 + 0.4\,\big[-0.05 + 0.1414\big]$$

$$= 0.04 + 0.4 \cdot 0.0914 \approx 0.04 + 0.0366 = 0.0766$$

So $\sigma_{\text{IV}}(0.1) \approx \sqrt{0.0766} \approx 0.277$ (27.7%).

The implied volatility is highest at OTM puts ($k = -0.1$, 34.1%), falls to ATM ($k = 0$, 28.3%), and is lowest at OTM calls ($k = +0.1$, 27.7%) — a downward-sloping equity-style skew, consistent with the negative tilt parameter $\rho = -0.5$.
