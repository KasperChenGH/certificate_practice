# Chapter 5 — The Black-Scholes Formula

## 5.1 The Call Price Formula

The Black-Scholes-Merton (BSM) formula gives the price of a European call option on a non-dividend-paying stock:

$$C = S_0\, N(d_1) - K\, e^{-rT}\, N(d_2)$$

::: where
- $C$ — European call price
- $S_0$ — current stock price
- $K$ — strike price
- $r$ — risk-free rate (annualized)
- $T$ — time to expiration (years)
- $N(\cdot)$ — standard normal CDF
- $d_1, d_2$ — defined below
:::

The quantities $d_1$ and $d_2$ are:

$$d_1 = \frac{\ln(S_0 / K) + (r + \sigma^2 / 2)\, T}{\sigma \sqrt{T}}, \qquad d_2 = d_1 - \sigma \sqrt{T}$$

::: where
- $\sigma$ — volatility of log-returns (annualized)
:::


## 5.2 What Each Piece Means

The formula $C = S_0 N(d_1) - K e^{-rT} N(d_2)$ has two terms. Think of it as "what you get minus what you pay":

| Term | Interpretation |
|---|---|
| $S_0\, N(d_1)$ | The delta-weighted stock position. This is the present value of receiving the stock, weighted by $N(d_1)$. It represents the hedge: to replicate the call, hold $N(d_1)$ shares. |
| $K\, e^{-rT}\, N(d_2)$ | The present value of the strike payment, weighted by the probability of exercise. You pay $K$ only if the call finishes in the money, which happens with risk-neutral probability $N(d_2)$. |

**Key facts:**

- $N(d_2)$ is the **risk-neutral probability** that $S_T > K$ (the call expires in the money).
- $N(d_1) \geq N(d_2)$ always. The quantity $N(d_1)$ is also a probability, but it is computed under a slightly different weighting that tilts toward higher stock prices. Practically, $N(d_1)$ is the option's **delta** — the number of shares you hold to hedge.
- When the option is deep in the money ($S_0 \gg K$), both $N(d_1)$ and $N(d_2)$ approach 1, and $C \to S_0 - K e^{-rT}$ (intrinsic value).
- When the option is far out of the money ($S_0 \ll K$), both approach 0, and $C \to 0$.

![BSM call price vs intrinsic value](study/assets/bsm_price_curve.svg)


## 5.3 The Put Formula

By put-call parity ($P = C - S_0 + K e^{-rT}$), the European put price is:

$$P = K\, e^{-rT}\, N(-d_2) - S_0\, N(-d_1)$$

::: where
- $P$ — European put price
:::

The symmetry is clean: replace $N(d)$ with $N(-d)$ and swap the sign of the two terms.


## 5.4 The Five Inputs

The BSM formula requires exactly five inputs:

| Input | Observable? | Notes |
|---|---|---|
| $S_0$ (stock price) | Yes | Current market price |
| $K$ (strike) | Yes | Specified in the option contract |
| $T$ (time to expiry) | Yes | Calendar calculation (trading days or actual days, convention-dependent) |
| $r$ (risk-free rate) | Yes | Treasury yield or OIS rate matching maturity $T$ |
| $\sigma$ (volatility) | **No** | Must be estimated from historical data or **implied** from market option prices |

Four inputs are directly observable. The fifth, $\sigma$, is where all the action is. When traders quote volatility (e.g., "the 30-day vol is 22%"), they are effectively quoting an option price through the BSM formula. This is the concept of **implied volatility**, which we will study in detail later.


## 5.5 Assumptions Behind BSM

The formula rests on several idealizations:

1. **Constant volatility.** $\sigma$ does not change over the life of the option. (In reality, it does — leading to the volatility smile.)
2. **No dividends.** The stock pays no dividends before expiry. (We relax this in Section 5.8.)
3. **Continuous trading.** You can hedge continuously, at any instant. (In practice, you hedge at discrete intervals.)
4. **No transaction costs or taxes.** Every trade is frictionless.
5. **European exercise only.** The option can only be exercised at expiry.
6. **Log-normal stock price.** The stock price follows geometric Brownian motion, so log-returns are normally distributed.

These assumptions are never exactly true, but they give a remarkably useful baseline. Departures from BSM are measured as corrections to it, not replacements.


## 5.6 Worked Example 1 — ATM Call

**Given:** $S_0 = 100$, $K = 100$, $T = 0.25$ (3 months), $r = 0.05$, $\sigma = 0.20$.

**Step 1: Compute $d_1$.**

$$d_1 = \frac{\ln(100 / 100) + (0.05 + 0.20^2/2) \times 0.25}{0.20 \times \sqrt{0.25}}$$

$$= \frac{0 + (0.05 + 0.02) \times 0.25}{0.20 \times 0.5} = \frac{0.0175}{0.10} = 0.1750$$

**Step 2: Compute $d_2$.**

$$d_2 = 0.1750 - 0.20 \times 0.5 = 0.1750 - 0.10 = 0.0750$$

**Step 3: Look up $N(d_1)$ and $N(d_2)$.**

Using a standard normal table (or calculator):

- $N(0.1750) = 0.5694$
- $N(0.0750) = 0.5299$

**Step 4: Compute the call price.**

$$C = 100 \times 0.5694 - 100 \times e^{-0.05 \times 0.25} \times 0.5299$$

$$= 56.94 - 100 \times 0.9876 \times 0.5299$$

$$= 56.94 - 52.33 = 4.61$$

**Step 5: Compute the put price via put-call parity.**

$$P = C - S_0 + K e^{-rT} = 4.61 - 100 + 98.76 = 3.37$$

**Sanity checks:**

- The call is ATM, so the price is modest — about 4.6% of the stock price. Reasonable for 3-month, 20% vol.
- The put is slightly cheaper than the call because the forward is above the strike ($S_0 e^{rT} = 101.26 > 100$).
- $N(d_2) = 0.5299$: there is roughly a 53% risk-neutral chance the call finishes in the money. Just over a coin flip for an ATM option — sensible.


## 5.7 Worked Example 2 — OTM Put

**Given:** $S_0 = 100$, $K = 90$, $T = 0.50$ (6 months), $r = 0.03$, $\sigma = 0.25$.

**Step 1: Compute $d_1$.**

$$d_1 = \frac{\ln(100 / 90) + (0.03 + 0.25^2 / 2) \times 0.50}{0.25 \times \sqrt{0.50}}$$

$$= \frac{0.10536 + (0.03 + 0.03125) \times 0.50}{0.25 \times 0.7071}$$

$$= \frac{0.10536 + 0.03063}{0.17678} = \frac{0.13599}{0.17678} = 0.7694$$

**Step 2: Compute $d_2$.**

$$d_2 = 0.7694 - 0.17678 = 0.5926$$

**Step 3: Look up normal CDF values.**

For the put, we need $N(-d_1)$ and $N(-d_2)$:

- $N(-0.7694) = 1 - N(0.7694) = 1 - 0.7792 = 0.2208$
- $N(-0.5926) = 1 - N(0.5926) = 1 - 0.7233 = 0.2767$

**Step 4: Compute the put price.**

$$P = K\, e^{-rT}\, N(-d_2) - S_0\, N(-d_1)$$

$$= 90 \times e^{-0.03 \times 0.50} \times 0.2767 - 100 \times 0.2208$$

$$= 90 \times 0.9851 \times 0.2767 - 22.08$$

$$= 88.66 \times 0.2767 - 22.08 = 24.53 - 22.08 = 2.45$$

**Sanity checks:**

- The put is 10% out of the money with 6 months left. A price of \$2.45 (2.45% of the stock) feels right.
- $N(-d_2) = 0.2767$: about a 28% risk-neutral chance the stock drops below 90 in 6 months. Plausible.


## 5.8 Extension — Continuous Dividend Yield

If the stock pays a continuous dividend yield $q$ (common for indices), replace $S_0$ with $S_0 e^{-qT}$ everywhere in the formula:

$$C = S_0\, e^{-qT}\, N(d_1) - K\, e^{-rT}\, N(d_2)$$

$$d_1 = \frac{\ln(S_0 / K) + (r - q + \sigma^2/2)\, T}{\sigma \sqrt{T}}, \qquad d_2 = d_1 - \sigma \sqrt{T}$$

::: where
- $q$ — continuous dividend yield (annualized)
:::

The intuition: dividends reduce the effective stock price available to the call holder, because the call holder does not receive dividends. The put holder benefits, since dividends push the stock price down.


## 5.9 Sensitivity Intuition (Preview of Greeks)

Before we formalize the Greeks in a later chapter, here is the qualitative picture of how each input affects the call price:

| If this goes **up**... | Call price... | Put price... | Why? |
|---|---|---|---|
| $S_0$ (stock price) | Rises | Falls | Call is more likely to finish ITM |
| $K$ (strike) | Falls | Rises | Higher hurdle for the call |
| $T$ (time to expiry) | Usually rises | Usually rises | More time = more chance of a big move |
| $r$ (risk-free rate) | Rises | Falls | Higher $r$ lowers the PV of paying $K$ |
| $\sigma$ (volatility) | Rises | Rises | More uncertainty = more option value |

The BSM formula quantifies each of these sensitivities exactly. The partial derivatives — delta, gamma, theta, vega, rho — are the Greeks, and they are all available in closed form.


## Practice

::: problem [Computation]
**Problem 5.1.** A stock trades at $S_0 = 80$, with $K = 85$, $T = 0.50$, $r = 0.04$, $\sigma = 0.30$. Compute the BSM price of the European call. Show all intermediate steps ($d_1$, $d_2$, $N(d_1)$, $N(d_2)$).

::: solution
**Solution.**

**Step 1:** Compute $d_1$.

$$d_1 = \frac{\ln(80/85) + (0.04 + 0.30^2/2) \times 0.50}{0.30 \times \sqrt{0.50}}$$

$$= \frac{-0.06062 + (0.04 + 0.045) \times 0.50}{0.30 \times 0.7071} = \frac{-0.06062 + 0.04250}{0.21213}$$

$$= \frac{-0.01812}{0.21213} = -0.0854$$

**Step 2:** Compute $d_2$.

$$d_2 = -0.0854 - 0.21213 = -0.2976$$

**Step 3:** Look up CDF values.

- $N(-0.0854) = 0.4660$
- $N(-0.2976) = 0.3830$

**Step 4:** Compute call price.

$$C = 80 \times 0.4660 - 85 \times e^{-0.04 \times 0.50} \times 0.3830$$

$$= 37.28 - 85 \times 0.9802 \times 0.3830 = 37.28 - 31.89 = 5.39$$

The European call is worth approximately **\$5.39**.
:::
:::

::: problem [Computation]
**Problem 5.2.** Using the same parameters as Problem 5.1 ($S_0 = 80$, $K = 85$, $T = 0.50$, $r = 0.04$, $\sigma = 0.30$), compute the European put price in two ways: (a) directly from the BSM put formula, and (b) via put-call parity. Verify they agree.

::: solution
**Solution.**

**(a) Direct BSM put formula.**

From Problem 5.1, $d_1 = -0.0854$ and $d_2 = -0.2976$.

- $N(-d_1) = N(0.0854) = 0.5340$
- $N(-d_2) = N(0.2976) = 0.6170$

$$P = 85 \times e^{-0.02} \times 0.6170 - 80 \times 0.5340$$

$$= 83.32 \times 0.6170 - 42.72 = 51.41 - 42.72 = 8.69$$

**(b) Put-call parity.**

$$P = C - S_0 + K e^{-rT} = 5.39 - 80 + 85 \times 0.9802 = 5.39 - 80 + 83.32 = 8.71$$

The two methods agree (the small difference of \$0.02 is due to rounding in intermediate steps).
:::
:::

::: problem [Conceptual]
**Problem 5.3.** Explain why an increase in volatility $\sigma$ raises the price of both calls and puts, even though higher volatility means the stock might go down (bad for calls) just as much as it might go up (bad for puts).

::: solution
**Solution.** Options have **asymmetric payoffs**: the holder benefits from favorable moves but is protected from unfavorable ones (the payoff is floored at zero). Higher volatility increases the magnitude of potential moves in both directions, but:

- For a call, a big upward move generates a large payoff, while a big downward move is capped at zero loss (the call simply expires worthless — you never lose more than the premium).
- For a put, the same logic applies in reverse: big downward moves are profitable, while upward moves are capped.

In both cases, the upside from larger moves outweighs the "downside" (which is already bounded). Therefore, more volatility always means more option value, regardless of whether it is a call or a put. Formally, this is captured by **vega** being positive for both calls and puts.
:::
:::
