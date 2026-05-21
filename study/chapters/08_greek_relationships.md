# Chapter 8 — Greek Relationships

In Chapter 7 we treated the Greeks as independent sensitivities. But they are **not independent** — they are bound together by the same equation that produces the Black-Scholes formula. This chapter explores those connections and shows how traders use them in practice.

We continue with the same running parameters: $S=100,\ K=100,\ T=0.25,\ r=0.05,\ \sigma=0.20$. From Chapter 7 our ATM call Greeks are:

| Greek | Value |
|-------|-------|
| $\Delta_C$ | $0.5694$ |
| $\Gamma$ | $0.0393$ |
| $\Theta_C$ | $-10.473$ per year ($-0.0287$/day) |
| $\nu$ | $19.64$ |
| $\rho_C$ | $13.09$ |

The call price itself is $C = SN(d_1) - Ke^{-rT}N(d_2) = 100(0.5694) - 100e^{-0.0125}(0.5299) \approx 56.94 - 52.33 = 4.615$.

---

## 8.1 The Black-Scholes PDE as a Greek Identity

The Black-Scholes-Merton model says that any fairly-priced option $V$ must satisfy the **partial differential equation** (PDE):

$$\Theta + \frac{1}{2}\sigma^2 S^2 \Gamma + rS\Delta - rV = 0$$

::: where
- $\Theta$ — theta, the time decay of the option (in annualized terms)
- $\sigma$ — volatility of the underlying (annualized)
- $S$ — current stock price
- $\Gamma$ — gamma, the second derivative of option price with respect to stock price
- $r$ — risk-free interest rate (annualized, continuously compounded)
- $\Delta$ — delta, the first derivative of option price with respect to stock price
- $V$ — the option price (call or put)
:::

You do not need to derive this equation. What matters is the **interpretation**: the four terms must sum to zero. This means if you know any three Greeks (and the option price), you can solve for the fourth.

**Verification with our numbers.** Let us check that the identity holds for the ATM call:

- $\Theta = -10.473$
- $\frac{1}{2}\sigma^2 S^2 \Gamma = \frac{1}{2}(0.04)(10000)(0.0393) = 7.856$
- $rS\Delta = 0.05 \times 100 \times 0.5694 = 2.847$
- $rV = 0.05 \times 4.615 = 0.231$

Sum: $-10.473 + 7.856 + 2.847 - 0.231 = -0.001 \approx 0$ (the small residual is rounding).

---

## 8.2 The Theta-Gamma Tradeoff

This is arguably the most important relationship in options trading. Consider a **delta-neutral** portfolio — one where $\Delta = 0$ (achieved by hedging with stock). The PDE becomes:

$$\Theta + \frac{1}{2}\sigma^2 S^2 \Gamma = rV$$

::: where
- $\Theta$ — theta of the delta-neutral portfolio
- $\sigma$ — implied volatility
- $S$ — stock price
- $\Gamma$ — gamma of the portfolio
- $r$ — risk-free rate
- $V$ — value of the portfolio
:::

For short-dated options the $rV$ term is small, so approximately:

$$\Theta \approx -\frac{1}{2}\sigma^2 S^2 \Gamma$$

::: where
- $\Theta$ — theta (time decay per year)
- $\sigma$ — volatility
- $S$ — stock price
- $\Gamma$ — gamma
:::

**The key insight:** positive gamma and negative theta are two sides of the same coin. You cannot have one without the other.

- If you are **long gamma** ($\Gamma > 0$), you benefit when the stock makes big moves. But the market charges you for this privilege via negative theta — your position bleeds value every day.
- If you are **short gamma** ($\Gamma < 0$), you collect theta (your position gains value each day from time decay). But you are exposed to large losses if the stock makes a big move.

This tradeoff is inescapable. It is the fundamental tension underlying all options trading.

**Numerical check.** For our ATM call:

$$-\frac{1}{2}\sigma^2 S^2 \Gamma = -\frac{1}{2}(0.04)(10000)(0.0393) = -7.856$$

Compare with $\Theta_C = -10.473$. The difference ($-2.617$) equals $rS\Delta - rV = 2.847 - 0.231 = 2.616$, which is the financing/delta term we dropped. For short-dated, near-ATM options the approximation $\Theta \approx -\frac{1}{2}\sigma^2 S^2 \Gamma$ is quite close.

---

## 8.3 Delta Hedging in Practice

Delta hedging is the process of maintaining a delta-neutral position by continuously adjusting your stock hedge. Here is how it works step by step:

**Step 1 — Initiate.** Buy 1 call at \$4.615. Short $\Delta = 0.5694$ shares at \$100. Net delta = 0.

**Step 2 — The stock moves.** Suppose the stock rises to \$101. Because of gamma, delta increases:

$$\Delta_{\text{new}} \approx 0.5694 + 0.0393 \times 1 = 0.6087$$

Your hedge is now stale — you are short 0.5694 shares but need to be short 0.6087 shares. You sell an additional 0.0393 shares.

**Step 3 — Repeat.** Each time the stock moves, delta changes and you re-hedge. In theory you do this continuously; in practice, once or twice a day.

**The P&L of delta hedging.** Over a small time interval $\Delta t$, the P&L of a delta-hedged option position is approximately:

$$\text{P\&L} \approx \frac{1}{2}\Gamma (\Delta S)^2 + \Theta \cdot \Delta t$$

::: where
- $\Gamma$ — gamma of the option
- $\Delta S$ — stock price change over the interval
- $\Theta$ — theta of the option (per unit time, matching the units of $\Delta t$)
- $\Delta t$ — length of the time interval
:::

The two terms compete:
- The **gamma term** $\frac{1}{2}\Gamma(\Delta S)^2$ is always positive for long gamma. Big stock moves generate profit.
- The **theta term** $\Theta \cdot \Delta t$ is negative for long options. Time passing costs you.

**When do you profit?** You profit when realized stock moves are *larger* than what the implied volatility assumed. Specifically:

- If the stock's **realized volatility** exceeds the **implied volatility** you paid for, the gamma gains more than offset the theta losses. You make money.
- If realized vol is less than implied vol, theta wins. You lose money.

This is the fundamental source of P&L for options market-makers and volatility traders. Buying options is a bet that the stock will move more than the market expects; selling options is a bet that it will move less.

---

## 8.4 Put-Call Greek Relationships

Put-call parity states:

$$C - P = S - Ke^{-rT}$$

::: where
- $C$ — European call price
- $P$ — European put price
- $S$ — current stock price
- $K$ — strike price
- $r$ — risk-free rate
- $T$ — time to expiry
:::

Since the right side ($S - Ke^{-rT}$) is just a portfolio of stock and a bond, we can differentiate both sides to relate the Greeks of calls and puts.

### Delta

Differentiate with respect to $S$:

$$\Delta_C - \Delta_P = 1$$

::: where
- $\Delta_C$ — delta of the call
- $\Delta_P$ — delta of the put
:::

**Why:** The right side $S - Ke^{-rT}$ has delta = 1 (the stock contributes +1, the bond contributes 0). So the call delta exceeds the put delta by exactly 1.

**Check:** $0.5694 - (-0.4306) = 1.0000$. Confirmed.

### Gamma

Differentiate delta with respect to $S$:

$$\Gamma_C = \Gamma_P$$

::: where
- $\Gamma_C$ — gamma of the call
- $\Gamma_P$ — gamma of the put
:::

**Why:** The right side has constant delta (= 1), so its gamma is zero. Therefore call and put gammas must be equal.

### Vega

Differentiate with respect to $\sigma$:

$$\nu_C = \nu_P$$

::: where
- $\nu_C$ — vega of the call
- $\nu_P$ — vega of the put
:::

**Why:** The right side $S - Ke^{-rT}$ does not depend on volatility at all, so its vega is zero. Call and put vegas must be equal.

### Theta

Differentiate with respect to $T$ (with a sign change because theta is $-\partial V/\partial T'$ where $T' = T_{\text{expiry}} - t$, but applying the chain rule to put-call parity directly):

$$\Theta_C - \Theta_P = -rKe^{-rT}$$

::: where
- $\Theta_C$ — theta of the call
- $\Theta_P$ — theta of the put
- $r$ — risk-free rate
- $K$ — strike price
- $T$ — time to expiry
:::

**Why:** The time derivative of $-Ke^{-rT}$ contributes $-rKe^{-rT}$, while the stock term $S$ contributes nothing.

**Check:** $-rKe^{-rT} = -0.05 \times 100 \times 0.9876 = -4.938$ per year, so $\Theta_P = \Theta_C + 4.938 = -10.473 + 4.938 = -5.535$ per year, or $-0.0152$ per day.

### Rho

Differentiate with respect to $r$:

$$\rho_C - \rho_P = KTe^{-rT}$$

::: where
- $\rho_C$ — rho of the call
- $\rho_P$ — rho of the put
- $K$ — strike price
- $T$ — time to expiry
- $r$ — risk-free rate
:::

**Why:** Differentiating $-Ke^{-rT}$ with respect to $r$ gives $KTe^{-rT}$.

**Check:** $KTe^{-rT} = 100 \times 0.25 \times 0.9876 = 24.69$, so $\rho_P = 13.09 - 24.69 = -11.60$.

---

## 8.5 Portfolio Greeks

Greeks are **additive** across positions. If your portfolio contains $n_i$ units of instrument $i$ (options, stock, etc.), the portfolio Greeks are:

$$\Delta_{\text{port}} = \sum_i n_i \Delta_i, \qquad \Gamma_{\text{port}} = \sum_i n_i \Gamma_i, \qquad \text{etc.}$$

::: where
- $n_i$ — number of units of instrument $i$ (positive for long, negative for short)
- $\Delta_i, \Gamma_i$ — delta and gamma of instrument $i$
:::

This additivity is what makes Greek-based risk management practical: you sum up the Greeks across hundreds of positions to get a single set of portfolio-level numbers.

**Example: ATM Straddle.** A straddle is long 1 ATM call + long 1 ATM put with the same strike and expiry.

| Greek | Call | Put | Straddle (sum) |
|-------|------|-----|---------------|
| $\Delta$ | $+0.5694$ | $-0.4306$ | $+0.1388$ |
| $\Gamma$ | $0.0393$ | $0.0393$ | $0.0786$ |
| $\Theta$/day | $-0.0287$ | $-0.0152$ | $-0.0439$ |
| $\nu$ | $19.64$ | $19.64$ | $39.28$ |

The straddle has near-zero delta (roughly market-neutral), double the gamma, double the vega, and double the theta of a single option. It is a pure volatility bet.

---

## 8.6 Practical Hedging Scenarios

### Delta-Neutral, Long Gamma

**Setup:** Buy ATM straddles (or buy options and delta-hedge with stock).

**Profile:**
- $\Delta \approx 0$: no directional bias
- $\Gamma > 0$: benefit from big moves
- $\Theta < 0$: pay daily time decay
- $\nu > 0$: benefit if implied vol rises

**When to use:** You believe the stock will move more than implied vol suggests, or you expect a volatility spike (earnings, FDA announcement, etc.).

### Delta-Neutral, Short Gamma

**Setup:** Sell ATM straddles (or sell options and delta-hedge).

**Profile:**
- $\Delta \approx 0$
- $\Gamma < 0$: hurt by big moves
- $\Theta > 0$: collect daily time decay
- $\nu < 0$: hurt if implied vol rises

**When to use:** You believe the stock will be quiet — realized vol will be less than implied vol. You collect theta day after day, hoping for no surprises.

### Vega Trades

**Long vega:** Buy a straddle when you expect implied volatility to increase (e.g., before an uncertain event). You profit from the vol increase even if the stock does not move yet.

**Short vega:** Sell a straddle when you think implied vol is too high and will decline (e.g., after earnings when uncertainty resolves).

---

## 8.7 Worked Example: 100-Lot Straddle Position

A trader buys **100 ATM straddles** (100 calls + 100 puts), each on 1 share, with our standard parameters.

**Portfolio Greeks:**

$$\Delta_{\text{port}} = 100 \times 0.5694 + 100 \times (-0.4306) = 56.94 - 43.06 = 13.88$$

$$\Gamma_{\text{port}} = 100 \times 0.0393 + 100 \times 0.0393 = 7.86$$

$$\Theta_{\text{port}}^{\text{daily}} = 100 \times (-0.0287) + 100 \times (-0.0152) = -2.87 - 1.52 = -\$4.39 \text{ per day}$$

$$\nu_{\text{port}} = 100 \times 19.64 + 100 \times 19.64 = 3{,}928$$

::: where
- $\Delta_{\text{port}}$ — portfolio delta (equivalent shares of stock exposure)
- $\Gamma_{\text{port}}$ — portfolio gamma
- $\Theta_{\text{port}}^{\text{daily}}$ — portfolio theta per calendar day
- $\nu_{\text{port}}$ — portfolio vega
:::

**Interpretation.** The position costs \$4.39 per day in time decay. To break even each day, the gamma gains must offset this:

$$\frac{1}{2}\Gamma_{\text{port}}(\Delta S)^2 \geq |\Theta_{\text{port}}^{\text{daily}}|$$

Solving for the breakeven daily stock move:

$$(\Delta S)_{\text{BE}} = \sqrt{\frac{2|\Theta_{\text{port}}^{\text{daily}}|}{\Gamma_{\text{port}}}} = \sqrt{\frac{2 \times 4.39}{7.86}} = \sqrt{1.117} \approx \$1.06$$

::: where
- $(\Delta S)_{\text{BE}}$ — the daily stock move needed to break even
- $|\Theta_{\text{port}}^{\text{daily}}|$ — absolute value of daily portfolio theta
- $\Gamma_{\text{port}}$ — portfolio gamma
:::

The stock must move at least about **\$1.06 per day** (roughly 1.06% for a \$100 stock) for the straddle to break even on its time decay. If daily moves average more than this, the position profits; if less, it loses.

To fully delta-hedge, the trader would short about 14 shares (the residual portfolio delta), making the position purely a gamma/theta/vega trade.

---

## Practice

::: problem [Conceptual]
**Problem 8.1.** A trader holds a delta-neutral portfolio that is long gamma. She notices that the stock has been very quiet for the past week, barely moving. (a) Is her portfolio making or losing money? (b) What would need to happen for her to start profiting? (c) If implied volatility also drops during this quiet period, how does that affect her position?

::: solution
**Solution.** (a) She is losing money. A long-gamma, delta-neutral position has negative theta. Every quiet day, the theta term dominates because the gamma gains from $\frac{1}{2}\Gamma(\Delta S)^2$ are tiny when $\Delta S$ is small.

(b) The stock needs to start making moves large enough that $\frac{1}{2}\Gamma(\Delta S)^2 > |\Theta|\Delta t$. In other words, realized volatility needs to exceed implied volatility.

(c) A drop in implied vol hurts her further. She is long vega (long options always are), so a decline in implied vol reduces the mark-to-market value of her options on top of the theta losses.
:::
:::

::: problem [Computation]
**Problem 8.2.** Using the BSM PDE identity $\Theta + \frac{1}{2}\sigma^2 S^2 \Gamma + rS\Delta - rV = 0$, and the following values for a European put: $\Gamma_P = 0.0393$, $\Delta_P = -0.4306$, $V_P = 3.734$, $S = 100$, $\sigma = 0.20$, $r = 0.05$, compute $\Theta_P$ (annualized).

::: solution
**Solution.** Rearranging the PDE:

$$\Theta_P = -\frac{1}{2}\sigma^2 S^2 \Gamma_P - rS\Delta_P + rV_P$$

Substituting:

$$\Theta_P = -\frac{1}{2}(0.04)(10000)(0.0393) - 0.05(100)(-0.4306) + 0.05(3.734)$$

$$= -7.856 + 2.153 + 0.187 = -5.516 \text{ per year}$$

Converting to daily: $\Theta_P^{\text{daily}} = -5.516/365 \approx -\$0.0151$ per day.

This matches what we would get from the direct theta formula and is consistent with the put-call relationship $\Theta_C - \Theta_P = -rKe^{-rT} = -4.938$, since $-10.473 - (-5.516) = -4.957 \approx -4.938$ (difference due to rounding).
:::
:::

::: problem [Derivation]
**Problem 8.3.** Starting from put-call parity $C - P = S - Ke^{-rT}$, derive the relationship $\Gamma_C = \Gamma_P$. Then explain intuitively why this must be true by thinking about what gamma measures.

::: solution
**Solution.** **Derivation.** Differentiate put-call parity once with respect to $S$:

$$\frac{\partial C}{\partial S} - \frac{\partial P}{\partial S} = 1 \quad \Longrightarrow \quad \Delta_C - \Delta_P = 1$$

Differentiate again with respect to $S$:

$$\frac{\partial^2 C}{\partial S^2} - \frac{\partial^2 P}{\partial S^2} = 0 \quad \Longrightarrow \quad \Gamma_C - \Gamma_P = 0 \quad \Longrightarrow \quad \Gamma_C = \Gamma_P \qquad \blacksquare$$

**Intuition.** Gamma measures the *curvature* of the option price as a function of $S$. Put-call parity says that the call price and put price differ by $S - Ke^{-rT}$, which is a straight line in $S$ (slope 1, zero curvature). Adding a straight line to a curve does not change the curvature. Therefore the call and put must have the same curvature — the same gamma — at every stock price.
:::
:::
