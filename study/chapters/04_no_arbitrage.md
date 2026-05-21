# Chapter 4 — No-Arbitrage Pricing

## 4.1 The No-Arbitrage Principle

The most powerful idea in financial pricing is deceptively simple: **you cannot make risk-free profit from nothing.** If a strategy requires zero upfront investment and has no chance of losing money, then it cannot have any chance of making money either. If it did, every rational trader would pile in, and prices would adjust until the opportunity vanished.

This has a direct consequence for pricing:

> **Law of One Price.** If two portfolios produce the exact same payoff in every possible future state of the world, they must have the same price today.

If Portfolio A cost less than Portfolio B but paid the same thing tomorrow, you could buy A, sell B, pocket the difference, and face zero risk. That is an arbitrage — and we assume the market eliminates it.

Think of it like two vending machines side by side, both dispensing the same can of soda. If one charges \$1.00 and the other \$0.80, everyone buys from the cheaper one until prices equalize.


## 4.2 Replication

The law of one price gives us a pricing method: **replication.** If we can build a portfolio of simpler instruments (stocks, bonds) that exactly copies the payoff of an option, then the option's fair price equals the cost of that replicating portfolio.

This is the logic behind virtually every option pricing formula. We never need to guess how likely the stock is to go up or down. We just need to find the recipe — how many shares of stock and how much borrowing reproduces the option's payoff — and then read off the cost.


## 4.3 The Risk-Neutral Idea

When you price an option by replication, something remarkable happens: **the stock's expected return $\mu$ drops out of the formula.** Two traders who completely disagree on where the stock is heading will still agree on the option price, because the price is pinned down by hedging, not by a directional bet.

This leads to a convenient shortcut called **risk-neutral pricing:**

> In a hypothetical "risk-neutral world," every asset earns the risk-free rate $r$ on average. The option price equals the **discounted expected payoff**, where the expectation is computed in this risk-neutral world.

$$V_0 = e^{-rT}\, \mathbb{E}^Q\big[\text{payoff at time } T\big]$$

::: where
- $V_0$ — option price today
- $r$ — risk-free rate
- $T$ — time to expiry in years
- $\mathbb{E}^Q[\cdot]$ — risk-neutral expectation
:::

**Why does this work?** Because the option seller can delta-hedge — continuously adjusting a stock position to offset the option's risk. Once the directional risk is hedged away, the remaining portfolio is risk-free and must earn rate $r$. So the option's value is determined as if the world were risk-neutral.

**Key insight:** $\mu$ (the stock's real-world expected return) never appears in option pricing formulas. Only $\sigma$ (volatility) matters, because that is what the hedger cannot eliminate.


## 4.4 One-Period Binomial Model

Let us make this concrete with the simplest possible model.

**Setup.** A stock trades at $S_0$ today. Over one period, it either goes **up** by factor $u$ to $uS_0$, or **down** by factor $d$ to $dS_0$. A risk-free bond earns gross return $R = e^{r\Delta t}$ per period.

We want to price a European call with strike $K$ and one period to expiry.

### Step 1 — Risk-neutral probabilities

We find the probability $p$ that makes the stock's expected return equal to the risk-free rate:

$$p = \frac{R - d}{u - d}$$

::: where
- $p$ — risk-neutral up probability
- $R$ — gross risk-free return per period
- $u$ — up factor
- $d$ — down factor
- $\Delta t$ — period length in years
:::

For this to make sense, we need $d < R < u$; otherwise there would be an arbitrage between the stock and the bond.

### Step 2 — Option payoffs

At expiry, the call pays:

- **Up state:** $C_u = \max(uS_0 - K,\; 0)$
- **Down state:** $C_d = \max(dS_0 - K,\; 0)$

### Step 3 — Discounted expected payoff

$$C_0 = \frac{1}{R}\big[p\, C_u + (1 - p)\, C_d\big]$$

::: where
- $C_0$ — call price today
- $C_u$ — call payoff in up state
- $C_d$ — call payoff in down state
:::

### Worked Example

Suppose $S_0 = 100$, $u = 1.10$, $d = 0.95$, $R = 1.02$, and $K = 100$.

**Risk-neutral probability:**

$$p = \frac{1.02 - 0.95}{1.10 - 0.95} = \frac{0.07}{0.15} = 0.4667$$

**Payoffs:**

- Up: $C_u = \max(110 - 100, 0) = 10$
- Down: $C_d = \max(95 - 100, 0) = 0$

**Call price:**

$$C_0 = \frac{1}{1.02}\big[0.4667 \times 10 + 0.5333 \times 0\big] = \frac{4.667}{1.02} = 4.575$$

### Step 4 — Verify with the replicating portfolio

We can independently confirm this by building a portfolio of $\Delta$ shares of stock and $B$ dollars in the bond that matches the option payoff in both states:

$$\Delta = \frac{C_u - C_d}{(u - d)\,S_0} = \frac{10 - 0}{(1.10 - 0.95)\times 100} = \frac{10}{15} = 0.6667$$

$$B = \frac{1}{R}\,\frac{u\, C_d - d\, C_u}{u - d} = \frac{1}{1.02}\,\frac{1.10 \times 0 - 0.95 \times 10}{0.15} = \frac{-9.5}{0.153} = -62.09$$

::: where
- $\Delta$ — hedge ratio (shares held)
- $B$ — bond position (negative = borrowing)
:::

Portfolio cost today: $\Delta \times S_0 + B = 0.6667 \times 100 + (-62.09) = 4.58$. This matches our risk-neutral price (small rounding aside), confirming no-arbitrage consistency.


## 4.5 Multi-Period Binomial Trees

The one-period model extends naturally. At each node, the stock branches into an up and a down move. We work **backwards** from expiry:

1. Compute option payoffs at all terminal nodes.
2. At each earlier node, apply the one-period formula: $V = \frac{1}{R}[p\,V_u + (1-p)\,V_d]$.
3. Roll back to time zero.

With $n$ periods, the terminal stock prices form a **recombining tree** — an up followed by a down gives the same price as a down followed by an up ($udS = duS$). This keeps the tree manageable: $n+1$ terminal nodes instead of $2^n$.

**Connection to Black-Scholes.** As we increase the number of steps $n$ and shrink $\Delta t$ so that the tree's volatility matches $\sigma$, the binomial price converges to the Black-Scholes formula. The discrete hedging strategy becomes continuous delta hedging. This is one of the most elegant limit results in finance — the simple coin-flip model, repeated fast enough, reproduces the continuous-time answer.


## 4.6 Why It All Works — Delta Hedging

The deep reason no-arbitrage pricing works is **dynamic hedging.** The option seller does not simply sell and hope. At each instant (or each step in the tree), the seller holds $\Delta$ shares of stock, perfectly offsetting the option's sensitivity to stock moves. Because the directional risk is hedged away:

- The portfolio earns the risk-free rate.
- The option's fair value is determined by $\sigma$, not $\mu$.
- Two traders with opposite views on the market direction agree on the option price.

Hedging is never perfect in practice — volatility changes, stocks jump, and trading is discrete — but the no-arbitrage framework gives us the theoretical benchmark that all real-world pricing is built upon.


## Practice

::: problem [Conceptual]
**Problem 4.1.** Explain in two or three sentences why the stock's expected return $\mu$ does not appear in the binomial option pricing formula. What feature of the pricing method makes $\mu$ irrelevant?

::: solution
**Solution.** The binomial price is derived by replication: we construct a portfolio of stock and bonds that matches the option's payoff in every state. Because the replicating portfolio works regardless of whether the up or down state occurs, the real-world probabilities (which depend on $\mu$) cancel out. Only the volatility $\sigma$ (encoded in $u$ and $d$) and the risk-free rate $r$ survive.
:::
:::

::: problem [Computation]
**Problem 4.2.** A stock trades at $S_0 = 50$. Over one period it goes up by factor $u = 1.20$ or down by factor $d = 0.90$. The gross risk-free return is $R = 1.04$. Price a European put with strike $K = 55$ using risk-neutral pricing. Verify by constructing the replicating portfolio.

::: solution
**Solution.**

**Risk-neutral probability:**

$$p = \frac{R - d}{u - d} = \frac{1.04 - 0.90}{1.20 - 0.90} = \frac{0.14}{0.30} = 0.4667$$

**Payoffs:**

- Up: $P_u = \max(55 - 60, 0) = 0$
- Down: $P_d = \max(55 - 45, 0) = 10$

**Put price:**

$$P_0 = \frac{1}{1.04}\big[0.4667 \times 0 + 0.5333 \times 10\big] = \frac{5.333}{1.04} = 5.128$$

**Replicating portfolio:**

$$\Delta = \frac{P_u - P_d}{(u - d)\,S_0} = \frac{0 - 10}{0.30 \times 50} = \frac{-10}{15} = -0.6667$$

$$B = \frac{1}{R}\,\frac{u\,P_d - d\,P_u}{u - d} = \frac{1}{1.04}\,\frac{1.20 \times 10 - 0.90 \times 0}{0.30} = \frac{12}{0.312} = 38.46$$

Portfolio cost: $-0.6667 \times 50 + 38.46 = -33.33 + 38.46 = 5.13$. This matches the risk-neutral price (up to rounding), confirming consistency.
:::
:::

::: problem [Derivation]
**Problem 4.3.** In the one-period binomial model, show that the risk-neutral probability $p = (R - d)/(u - d)$ is the unique value of $p$ such that $\mathbb{E}^Q[S_1] = R\,S_0$, i.e., the stock's expected gross return under $p$ equals the risk-free return.

::: solution
**Solution.**

Under probability $p$, the expected future stock price is:

$$\mathbb{E}^Q[S_1] = p\,(uS_0) + (1 - p)\,(dS_0) = S_0\big[pu + (1-p)d\big]$$

Setting this equal to $R\,S_0$ (the stock must earn the risk-free rate in the risk-neutral world):

$$S_0\big[pu + (1-p)d\big] = R\,S_0$$

Dividing both sides by $S_0$:

$$pu + d - pd = R$$

$$p(u - d) = R - d$$

$$p = \frac{R - d}{u - d}$$

This is the unique solution because $u \neq d$, so the denominator is nonzero. The condition $d < R < u$ guarantees $0 < p < 1$, confirming it is a valid probability.
:::
:::
