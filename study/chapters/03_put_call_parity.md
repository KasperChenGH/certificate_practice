# Chapter 3 — Put-Call Parity

## The Big Identity

Put-call parity is one of the most important relationships in options pricing. For European options on a non-dividend-paying stock:

$$C - P = S - Ke^{-rT}$$

::: where
- $C$ — European call price today
- $P$ — European put price today
- $S$ — current stock price
- $K$ — strike price (same for both options)
- $r$ — risk-free interest rate (continuously compounded, annualized)
- $T$ — time to expiry in years (same for both options)
- $e^{-rT}$ — discount factor (present value of $1 received at time $T$)
:::

**What it says in words:** The difference between a call and a put (same strike, same expiry) equals the difference between the stock price and the present value of the strike. In other words, owning a call and shorting a put is economically equivalent to holding a **forward contract** on the stock at price $K$.

This is not a model — it's a **no-arbitrage identity**. It holds regardless of what pricing model you use. If it's violated, there's free money on the table.

---

## Derivation by Replication

We prove parity by constructing two portfolios that have identical payoffs at expiry and therefore must have the same price today.

### Portfolio A: Call + Cash

- Buy one European call with strike $K$ (costs $C$).
- Invest $Ke^{-rT}$ in a risk-free bond (grows to $K$ at expiry).

**Cost today:** $C + Ke^{-rT}$

**Payoff at expiry:**

| Scenario | Call pays | Bond pays | Total |
|---|---|---|---|
| $S_T \ge K$ | $S_T - K$ | $K$ | $S_T$ |
| $S_T < K$ | $0$ | $K$ | $K$ |

Portfolio A pays $\max(S_T, K)$ at expiry.

### Portfolio B: Put + Stock

- Buy one European put with strike $K$ (costs $P$).
- Buy one share of stock (costs $S$).

**Cost today:** $P + S$

**Payoff at expiry:**

| Scenario | Put pays | Stock is worth | Total |
|---|---|---|---|
| $S_T \ge K$ | $0$ | $S_T$ | $S_T$ |
| $S_T < K$ | $K - S_T$ | $S_T$ | $K$ |

Portfolio B also pays $\max(S_T, K)$ at expiry.

### Conclusion

Both portfolios pay exactly $\max(S_T, K)$ in every possible scenario. By the no-arbitrage principle, they must cost the same today:

$$C + Ke^{-rT} = P + S$$

Rearranging:

$$C - P = S - Ke^{-rT}$$

That's put-call parity. No model assumptions, no probability distributions — just the observation that two identical payoffs must have the same price.

---

## Rearrangements

Put-call parity is a single equation with four unknowns. Given any three, solve for the fourth:

**Solve for the call:**

$$C = P + S - Ke^{-rT}$$

::: where
- $C$ — European call price
- $P$ — European put price
- $S$ — current stock price
- $K$ — strike price
- $r$ — risk-free rate
- $T$ — time to expiry
:::

**Solve for the put:**

$$P = C - S + Ke^{-rT}$$

::: where
- $P$ — European put price
- $C$ — European call price
- $S$ — current stock price
- $K$ — strike price
- $r$ — risk-free rate
- $T$ — time to expiry
:::

**Solve for the stock price** (useful as a consistency check):

$$S = C - P + Ke^{-rT}$$

You can even back out the implied interest rate if you know $C$, $P$, $S$, $K$, and $T$:

$$e^{-rT} = \frac{S - C + P}{K} \implies r = -\frac{1}{T}\ln\!\left(\frac{S - C + P}{K}\right)$$

::: where
- $r$ — implied risk-free rate
- $T$ — time to expiry
- $S$ — current stock price
- $C$ — European call price
- $P$ — European put price
- $K$ — strike price
:::

---

## Synthetic Positions

Put-call parity tells us that any one of the four instruments (call, put, stock, bond) can be replicated using the other three. This creates **synthetic** positions.

### Synthetic long stock

Rearrange parity as:

$$S = C - P + Ke^{-rT}$$

**Recipe:** Buy the call, sell the put (same $K$ and $T$), and invest $Ke^{-rT}$ in the risk-free bond. This combination behaves exactly like owning the stock.

**When is this useful?** If you can't easily buy the stock (short-selling restrictions, liquidity issues), you can replicate the position using options.

### Synthetic long put

$$P = C - S + Ke^{-rT}$$

**Recipe:** Buy the call, short-sell the stock, invest $Ke^{-rT}$ in the risk-free bond. This replicates a put.

**When is this useful?** If the put market is illiquid but calls are actively traded, you manufacture the put from what's available.

### Synthetic long call

$$C = P + S - Ke^{-rT}$$

**Recipe:** Buy the put, buy the stock, borrow $Ke^{-rT}$ (i.e., short the bond). This replicates a call.

---

## Worked Example

**Setup.** $S = 100$, $K = 100$, $r = 0.05$, $T = 0.5$ (six months), $C = 8.00$. Find $P$.

**Step 1.** Compute the present value of the strike:

$$Ke^{-rT} = 100 \times e^{-0.05 \times 0.5} = 100 \times e^{-0.025} = 100 \times 0.97531 = 97.53$$

::: where
- $K$ — strike price ($100$)
- $r$ — risk-free rate ($0.05$)
- $T$ — time to expiry ($0.5$ years)
:::

**Step 2.** Apply put-call parity:

$$P = C - S + Ke^{-rT} = 8.00 - 100 + 97.53 = 5.53$$

::: where
- $P$ — European put price (what we're solving for)
- $C$ — European call price ($8.00$)
- $S$ — current stock price ($100$)
- $Ke^{-rT}$ — present value of the strike ($97.53$)
:::

**Answer:** The put should be priced at $P = 5.53$.

**Sanity check:** The call costs more than the put ($8.00 > 5.53$). This makes sense because the ATM call benefits from the stock's upward drift (positive interest rate makes the forward price $Se^{rT} = 102.53 > K = 100$), so the call is slightly ITM on a forward basis and the put is slightly OTM.

---

## Put-Call Parity with Dividends

If the stock pays known dividends during the life of the option, the stock price $S$ is replaced by $S$ minus the present value of all dividends paid before expiry:

$$C - P = S - \text{PV}(\text{div}) - Ke^{-rT}$$

::: where
- $C$ — European call price
- $P$ — European put price
- $S$ — current stock price
- $\text{PV}(\text{div})$ — present value of all dividends paid during the option's life
- $K$ — strike price
- $r$ — risk-free rate
- $T$ — time to expiry
:::

**Why the adjustment?** The stock holder receives dividends; the call holder does not. So the stock is worth more than a pure forward claim by exactly the present value of those dividends. To keep the two portfolios equivalent, we must subtract the dividends from the stock side.

**Example.** $S = 100$, $K = 100$, $r = 0.05$, $T = 1$, and the stock pays a single dividend of $2.00$ in 6 months.

$$\text{PV}(\text{div}) = 2.00 \times e^{-0.05 \times 0.5} = 2.00 \times 0.9753 = 1.95$$

$$C - P = 100 - 1.95 - 100 e^{-0.05} = 98.05 - 95.12 = 2.93$$

If $C = 9.00$, then $P = 9.00 - 2.93 = 6.07$.

For a **continuous dividend yield** $q$ (common for index options), replace $S$ with $Se^{-qT}$:

$$C - P = Se^{-qT} - Ke^{-rT}$$

::: where
- $q$ — continuous dividend yield (annualized)
- $Se^{-qT}$ — stock price adjusted for dividends reinvested continuously
:::

---

## Arbitrage When Parity Is Violated

Put-call parity isn't just a formula — it's a trading rule. If the market violates it, you can lock in a risk-free profit.

### The Test

Compute both sides of parity and check:

$$C - P \quad \text{vs} \quad S - Ke^{-rT}$$

If the left side is too high, the call is relatively overpriced (or the put is underpriced). If the left side is too low, the reverse.

### Example: Call Is Relatively Overpriced

**Market data.** $S = 100$, $K = 100$, $r = 0.05$, $T = 0.5$, $C = 10.00$, $P = 4.00$.

**Parity check:**

- Left side: $C - P = 10.00 - 4.00 = 6.00$
- Right side: $S - Ke^{-rT} = 100 - 97.53 = 2.47$

The left side exceeds the right side by $6.00 - 2.47 = 3.53$. The call/put combination is overpriced relative to the stock/bond combination.

**Arbitrage strategy:** Sell the expensive side, buy the cheap side.

| Action | Cash flow today |
|---|---|
| Sell the call | $+10.00$ |
| Buy the put | $-4.00$ |
| Buy the stock | $-100.00$ |
| Borrow $Ke^{-rT} = 97.53$ at rate $r$ | $+97.53$ |
| **Net cash received** | **$+3.53$** |

**At expiry:**

- If $S_T \ge 100$: The call is exercised against you — deliver the stock for $100$. The put expires worthless. Use the $100$ received to repay the loan ($100$). Net payoff = $0$.
- If $S_T < 100$: The call expires worthless. Exercise your put — sell the stock for $100$. Use the $100$ to repay the loan. Net payoff = $0$.

In both cases, the expiry payoff is zero. But you already collected $3.53 upfront. That's a risk-free profit.

**Key insight:** The arbitrage always involves selling the overpriced side and buying the underpriced side. The positions cancel out at expiry, leaving only the initial cash difference as profit.

---

## Summary of Key Relationships

| Formula | What it tells you |
|---|---|
| $C - P = S - Ke^{-rT}$ | Basic put-call parity (no dividends) |
| $C - P = S - \text{PV}(\text{div}) - Ke^{-rT}$ | With discrete dividends |
| $C - P = Se^{-qT} - Ke^{-rT}$ | With continuous dividend yield $q$ |
| $C = P + S - Ke^{-rT}$ | Synthetic call |
| $P = C - S + Ke^{-rT}$ | Synthetic put |
| $S = C - P + Ke^{-rT}$ | Synthetic stock |

---

## Practice

::: problem [Computation]
**Problem 3.1.** A European call with $K = 50$ and $T = 0.25$ is priced at $C = 4.50$. The stock trades at $S = 52$ and the risk-free rate is $r = 0.03$. Find the price of the corresponding European put.

::: solution
**Solution.**

Step 1: Discount the strike.

$$Ke^{-rT} = 50 \times e^{-0.03 \times 0.25} = 50 \times e^{-0.0075} = 50 \times 0.99252 = 49.63$$

Step 2: Apply put-call parity.

$$P = C - S + Ke^{-rT} = 4.50 - 52 + 49.63 = 2.13$$

The put is priced at $P = 2.13$.
:::
:::

::: problem [Computation]
**Problem 3.2.** You observe $S = 80$, $K = 85$, $r = 0.06$, $T = 1$, $C = 7.00$, $P = 8.00$. The stock pays no dividends. Check whether put-call parity holds. If not, construct the arbitrage trade and compute the risk-free profit.

::: solution
**Solution.**

**Parity check:**

- Left side: $C - P = 7.00 - 8.00 = -1.00$
- Right side: $S - Ke^{-rT} = 80 - 85e^{-0.06} = 80 - 85 \times 0.94176 = 80 - 80.05 = -0.05$

Parity says $C - P$ should equal $-0.05$, but we observe $-1.00$. The left side is too low by $0.95$, meaning the call is underpriced relative to the put (equivalently, the put is overpriced relative to the call).

**Arbitrage:** Buy the cheap side (call + bond), sell the expensive side (put + stock).

| Action | Cash flow today |
|---|---|
| Buy the call | $-7.00$ |
| Sell the put | $+8.00$ |
| Short-sell the stock | $+80.00$ |
| Invest $Ke^{-rT} = 80.05$ in risk-free bond | $-80.05$ |
| **Net cash received** | **$+0.95$** |

**At expiry:**

- If $S_T \ge 85$: Exercise the call, buy stock at $85$, use it to close the short. The put expires worthless. The bond returns $85$. Net: pay $85$ (call exercise), receive $85$ (bond) = $0$.
- If $S_T < 85$: The call expires worthless. The put is exercised against you — you must buy the stock at $85$, which you use to close the short. Bond returns $85$. Net: pay $85$ (put assignment), receive $85$ (bond) = $0$.

Profit = $0.95$, locked in today, with zero risk at expiry.
:::
:::

::: problem [Derivation]
**Problem 3.3.** Starting from put-call parity with a continuous dividend yield, $C - P = Se^{-qT} - Ke^{-rT}$, show that if $r = q$, then the ATM call ($K = S$) and ATM put have the same price.

::: solution
**Solution.**

Set $K = S$ (ATM) and $r = q$:

$$C - P = Se^{-qT} - Se^{-rT}$$

Since $r = q$:

$$C - P = Se^{-rT} - Se^{-rT} = 0$$

Therefore $C = P$.

**Intuition:** When $r = q$, the forward price is $F = Se^{(r-q)T} = S$. The forward price equals the current stock price, so the ATM option is also "at-the-money-forward." In this special case, the call and put are perfectly symmetric — the probability of finishing above $S$ contributes equally to the call as the probability of finishing below $S$ contributes to the put (in risk-neutral terms). So they have the same price.
:::
:::
