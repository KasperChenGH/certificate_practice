# Chapter 1 — Preface and Notation

This document develops European-options pricing theory at the graduate level, beginning with the probability-theoretic foundations and building through to the implied-volatility surface. The exposition is deliberately narrow in scope: American and Bermudan options — whose valuation requires optimal stopping theory — are not covered. The Black-Scholes-Merton framework, which is intrinsically European, serves as the unifying lens throughout. Every formula is derived, every assumption is stated, and every non-trivial step is justified. The goal is to give the reader a rigorous working understanding of options pricing, not merely a collection of recipes.

## Notation

The following symbols are used consistently throughout all chapters. Inline math is written in KaTeX; every symbol introduced below is defined at its first meaningful use in the text and redefined in `where` blocks wherever a formula appears.

| Symbol | Meaning |
|--------|---------|
| $S_t$ | Stock (or underlying asset) price at time $t$ |
| $K$ | Strike price of an option |
| $T$ | Option maturity (calendar time, in years) |
| $t$ | Current time, with $0 \le t \le T$ |
| $\tau = T - t$ | Time to expiry (in years) |
| $r$ | Continuously compounded risk-free interest rate (annualized) |
| $q$ | Continuous dividend yield (annualized) |
| $\sigma$ | Volatility: annualized standard deviation of log-returns |
| $\mu$ | Drift of the stock under the physical measure $\mathbb{P}$ |
| $C$ | European call option price |
| $P$ | European put option price |
| $V$ | Generic European option value (call or put) |
| $\Delta$ | Delta: $\partial V / \partial S$ |
| $\Gamma$ | Gamma: $\partial^2 V / \partial S^2$ |
| $\Theta$ | Theta: $\partial V / \partial t$ |
| $\nu$ | Vega: $\partial V / \partial \sigma$ (Greek letter nu, not Latin v) |
| $\rho$ | Rho: $\partial V / \partial r$ |
| $d_1,\, d_2$ | Auxiliary variables in the Black-Scholes formula (defined in Ch. 7) |
| $N(\cdot)$ or $\Phi(\cdot)$ | Standard normal CDF |
| $N'(\cdot)$ or $\varphi(\cdot)$ | Standard normal PDF |
| $W_t$ | Standard Brownian motion under $\mathbb{P}$ |
| $\tilde{W}_t$ | Standard Brownian motion under the risk-neutral measure $\mathbb{Q}$ |
| $\mathbb{P}$ | Physical (real-world) probability measure |
| $\mathbb{Q}$ | Risk-neutral probability measure |
| $\mathcal{F}_t$ | Sigma-algebra of information available at time $t$ |
| $\mathbb{E}$ | Expectation under $\mathbb{P}$ |
| $\mathbb{E}^{\mathbb{Q}}$ | Expectation under $\mathbb{Q}$ |
| $(x)^+$ | Positive part: $\max(x,\, 0)$ |
| $\mathbf{1}_A$ | Indicator function of event $A$ |
| $\kappa$ | Mean-reversion speed of variance (introduced in Ch. 12, Heston model) |
| $\theta$ | Long-run variance level (introduced in Ch. 12, Heston model) |
| $\xi$ | Volatility of volatility (introduced in Ch. 12, Heston model) |

## Conventions

The following conventions hold throughout unless a chapter explicitly states otherwise.

- **Time is measured in years.** A three-month option has $T = 0.25$.
- **Interest rates and volatilities are annualized.** A rate of 5% means $r = 0.05$; a vol of 20% means $\sigma = 0.20$.
- **All compounding is continuous.** The present value of one dollar received at time $T$ is $e^{-rT}$, never $(1 + r)^{-T}$.
- **The probability space is filtered.** $W_t$ is a standard Brownian motion on a complete filtered probability space $(\Omega, \mathcal{F}, \mathbb{P}, \{\mathcal{F}_t\}_{t \ge 0})$, where the filtration $\{\mathcal{F}_t\}$ is the natural augmented filtration of $W_t$.
- **"Stock" means a non-dividend-paying stock** unless the dividend yield $q$ is explicitly invoked. When $q = 0$, the formulas simplify and $q$ is dropped.
- **All options are European** unless the text explicitly says otherwise. "European" means the option can only be exercised at maturity $T$.
- **We work in continuous time.** Discrete-time analogues (binomial trees, finite-difference grids) appear only where they help build intuition for a continuous-time result; they are not the primary objects of study.

## Prerequisites

This document assumes graduate-level mathematical maturity. Specifically, the reader should be comfortable with the following before beginning Chapter 2:

- **Measure-theoretic probability** at roughly the level of Shreve, *Stochastic Calculus for Finance I*: probability spaces, sigma-algebras, filtrations, random variables, conditional expectation, convergence theorems, and $L^p$ spaces. Itô's formula is developed from scratch in Chapter 3, so prior exposure to stochastic calculus is helpful but not required.
- **Multivariable calculus**, including partial derivatives, the chain rule in several variables, and the heat equation as a motivating example of a PDE. Familiarity with separation of variables and the Fourier transform is helpful for the PDE chapters.
- **Ordinary and partial differential equations.** Chapter 8 derives the Black-Scholes PDE and solves it by reduction to the heat equation; the reader should be comfortable with the method of characteristics and boundary-value problems.
- **Linear algebra** at the level of eigendecomposition and matrix norms. Used sparingly, primarily in numerical methods.
- **Basic complex analysis is not assumed.** Fourier inversion in Chapter 11 is handled via real-variable arguments where possible; when a contour integral appears, it is explained in place.

## How to Read This Document

The chapters are sequential: each one builds on the definitions, theorems, and notational conventions introduced in all preceding chapters. A reader who is comfortable with stochastic calculus may skim Chapters 2–4 but should not skip Chapter 1 (this preface), since the notational conventions established here are used without reminder later.

Every theorem is followed by either a complete proof or a proof sketch with precise citations to the omitted steps. When a proof is only sketched, the sketch is labeled *Proof sketch* and the gap is identified explicitly — the reader is never left wondering whether a step was rigorous or hand-wavy.

Every non-trivial formula is followed by a `where` block that defines every symbol appearing in the formula, even if that symbol has already been defined in an earlier chapter. This means the reader can always understand a formula in isolation, without scrolling back. The `where` blocks are deliberately redundant; treat them as self-contained reference cards.

Each chapter from Chapter 2 onward ends with a `## Practice` section containing two or three problems at roughly the difficulty of a qualifying examination. The problems consolidate the chapter's main results. Attempt each problem before revealing the solution — the solution is hidden behind a toggle so that the temptation to read ahead is reduced but the answer remains accessible.

*(No Practice section; the first problem set appears in Chapter 2.)*
