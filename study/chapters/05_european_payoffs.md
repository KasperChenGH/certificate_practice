# Chapter 5 — European Option Payoffs

## Goals

- Define the call and put payoff functions and establish their basic analytical properties.
- Prove monotonicity and convexity of both payoffs in the terminal stock price and in the strike.
- Derive no-arbitrage bounds on European call and put prices via static replication arguments.
- Prove put-call parity by static replication, in both the no-dividend and continuous-dividend cases.

## Prerequisites

- **Ch. 4** — no-arbitrage framework: self-financing portfolios, the no-arbitrage (NA) condition, domination arguments.
- **Basic real analysis** — convexity, the $\max$ function, and elementary inequalities.

---

## Payoff definitions

At expiration $T$, a European option confers the right (not the obligation) to transact at a fixed strike price $K$. The resulting payoffs are:

**Call.** A European call gives the right to *buy* one share at price $K$. The payoff is:

$$f_C(S_T) = (S_T - K)^+ = \max(S_T - K, 0).$$

::: where
- $S_T$ — the stock price at expiration $T$.
- $K > 0$ — the fixed strike price.
- $(\cdot)^+$ — the positive-part operator: $x^+ = \max(x, 0)$.
:::

**Put.** A European put gives the right to *sell* one share at price $K$. The payoff is:

$$f_P(S_T) = (K - S_T)^+ = \max(K - S_T, 0).$$

::: where
- $S_T$ — the stock price at expiration $T$.
- $K > 0$ — the fixed strike price.
- $(\cdot)^+$ — the positive-part operator.
:::

**Remark.** Both payoffs are piecewise-linear and non-negative. The call payoff is unbounded above — as $S_T \to \infty$, $f_C \to \infty$ — reflecting unlimited upside. The put payoff is bounded above by $K$, since $f_P(S_T) \le K$ for all $S_T \ge 0$, achieved in the limit $S_T \to 0$.

---

## Properties of payoffs

### Monotonicity in $S_T$

**Call — non-decreasing in $S_T$.** For $S_T^{(1)} \le S_T^{(2)}$:

$$f_C(S_T^{(1)}) = (S_T^{(1)} - K)^+ \le (S_T^{(2)} - K)^+ = f_C(S_T^{(2)}).$$

::: where
- $f_C$ — call payoff function $S \mapsto (S - K)^+$
- $S_T^{(1)}, S_T^{(2)}$ — two possible terminal stock prices with $S_T^{(1)} \le S_T^{(2)}$
:::

A higher terminal stock price can only increase — or leave unchanged — the call's payoff.

**Put — non-increasing in $S_T$.** For $S_T^{(1)} \le S_T^{(2)}$:

$$f_P(S_T^{(1)}) = (K - S_T^{(1)})^+ \ge (K - S_T^{(2)})^+ = f_P(S_T^{(2)}).$$

::: where
- $f_P$ — put payoff function $S \mapsto (K - S)^+$
- $S_T^{(1)}, S_T^{(2)}$ — two possible terminal stock prices with $S_T^{(1)} \le S_T^{(2)}$
:::

A higher terminal stock price reduces the put's payoff.

### Monotonicity in $K$

**Call — non-increasing in $K$.** For fixed $S_T$ and $K_1 \le K_2$, $S_T - K_1 \ge S_T - K_2$, so $(S_T - K_1)^+ \ge (S_T - K_2)^+$. A higher strike leaves less of the terminal price "above" $K$, weakly reducing the call payoff.

**Put — non-decreasing in $K$.** For fixed $S_T$ and $K_1 \le K_2$, $K_2 - S_T \ge K_1 - S_T$, so $(K_2 - S_T)^+ \ge (K_1 - S_T)^+$. A higher strike means the put is "deeper in the money" for any given $S_T$.

### Convexity in $S_T$ and in $K$

Both payoffs are convex functions of $S_T$ (for fixed $K$) and of $K$ (for fixed $S_T$). The convexity is inherited directly from the $(\cdot)^+$ operation, which is itself convex.

**Proof of convexity of $f_C$ in $S_T$.** Let $\lambda \in [0,1]$ and $S_T^{(1)}, S_T^{(2)} \ge 0$. We must show:

$$\bigl(\lambda S_T^{(1)} + (1-\lambda) S_T^{(2)} - K\bigr)^+ \le \lambda\,(S_T^{(1)} - K)^+ + (1-\lambda)\,(S_T^{(2)} - K)^+.$$

::: where
- $\lambda$ — convex combination weight, $\lambda \in [0, 1]$
- $S_T^{(1)}, S_T^{(2)}$ — two possible terminal stock prices
- $K$ — strike price
- $(\cdot)^+$ — positive part, $\max(\cdot, 0)$
:::

Write $x_i = S_T^{(i)} - K$. The claim becomes $(\lambda x_1 + (1-\lambda)x_2)^+ \le \lambda x_1^+ + (1-\lambda) x_2^+$. Since $(\cdot)^+$ is a convex function of its argument — it equals $\max(x, 0)$, the maximum of two linear (hence convex) functions — this follows immediately from the definition of convexity:

$$(\lambda x_1 + (1-\lambda)x_2)^+ \le \lambda x_1^+ + (1-\lambda)x_2^+. \qquad \square$$

The same argument applies to $f_P$ and to convexity in $K$.

---

## Arbitrage bounds

### Theorem

For a European call with no dividends:

$$\max\!\bigl(S_0 - K e^{-rT},\, 0\bigr) \le C \le S_0.$$

For a European put with no dividends:

$$\max\!\bigl(K e^{-rT} - S_0,\, 0\bigr) \le P \le K e^{-rT}.$$

::: where
- $C$ — time-0 price of the European call.
- $P$ — time-0 price of the European put.
- $S_0$ — current stock price at time 0.
- $K$ — strike price.
- $r \ge 0$ — continuously-compounded risk-free rate.
- $T$ — time to expiration.
- $K e^{-rT}$ — present value of paying strike $K$ at time $T$.
:::

### Proof of call lower bound

We show $C \ge S_0 - K e^{-rT}$ (combined with the trivial bound $C \ge 0$, since the call payoff is non-negative, this gives the $\max$ form).

Construct **Portfolio A**: long one call, short one share of stock, long $K e^{-rT}$ invested in the risk-free bond (so it accrues to $K$ at time $T$).

The time-0 cost of Portfolio A is $C - S_0 + K e^{-rT}$.

At time $T$, the payoff of Portfolio A is:

- **If $S_T \ge K$:** $(S_T - K) - S_T + K = 0$.
- **If $S_T < K$:** $0 - S_T + K = K - S_T > 0$.

Portfolio A's payoff is always $\ge 0$ — it is non-negative in every scenario. By no-arbitrage, its time-0 value must be non-negative:

$$C - S_0 + K e^{-rT} \ge 0 \implies C \ge S_0 - K e^{-rT}.$$

::: where
- $C$ — European call price at time $0$
- $S_0$ — current stock price
- $K e^{-rT}$ — present value of the strike payment due at $T$
:::

Since also $C \ge 0$ (the call cannot have negative value — the holder simply does not exercise if $S_T < K$), we obtain $C \ge \max(S_0 - K e^{-rT}, 0)$. $\square$

### Proof of call upper bound

A call's payoff satisfies $(S_T - K)^+ \le S_T$ for all $K \ge 0$, since the positive part of $S_T - K$ is at most $S_T$ itself. A portfolio consisting of one share of stock at time 0 costs $S_0$ and delivers $S_T$ at time $T$, which dominates the call's payoff in every state. By no-arbitrage (no domination without cost):

$$C \le S_0. \qquad \square$$

### Bounds for the put

**Lower bound $P \ge K e^{-rT} - S_0$ (and $\ge 0$):** Construct Portfolio B: long one put, long one share, short $K e^{-rT}$ in bonds. Time-0 cost: $P + S_0 - K e^{-rT}$. At $T$:

- If $S_T \ge K$: payoff $= 0 + S_T - K = S_T - K \ge 0$.
- If $S_T < K$: payoff $= (K - S_T) + S_T - K = 0$.

Always $\ge 0$, so $P + S_0 - K e^{-rT} \ge 0$, giving $P \ge K e^{-rT} - S_0$. Combined with $P \ge 0$: $P \ge \max(K e^{-rT} - S_0, 0)$.

**Upper bound $P \le K e^{-rT}$:** The put payoff is at most $K$ (achieved if $S_T = 0$). A bond paying $K$ at time $T$ costs $K e^{-rT}$ today and dominates the put. By no-arbitrage, $P \le K e^{-rT}$. $\square$

---

## Put-call parity (no dividends)

### Theorem

For European call and put options on the same underlying with the same strike $K$ and expiration $T$, and no dividends:

$$C - P = S_0 - K e^{-rT}.$$

::: where
- $C$ — time-0 European call price.
- $P$ — time-0 European put price.
- $S_0$ — current stock price.
- $K$ — common strike price.
- $T$ — time to expiration.
- $r$ — continuously-compounded risk-free rate.
- $e^{-rT}$ — discount factor over $[0, T]$.
:::

### Proof

Construct two portfolios and compare their payoffs at time $T$:

**Portfolio A:** Long one call, short one put (same $K$, same $T$). Time-0 cost: $C - P$.

**Portfolio B:** Long one share of stock, short $K e^{-rT}$ in bonds (i.e., borrow $K e^{-rT}$ today, repay $K$ at $T$). Time-0 cost: $S_0 - K e^{-rT}$.

At time $T$, the payoff of Portfolio A is:

$$(S_T - K)^+ - (K - S_T)^+ = \begin{cases} (S_T - K) - 0 = S_T - K & \text{if } S_T \ge K, \\ 0 - (K - S_T) = S_T - K & \text{if } S_T < K. \end{cases}$$

::: where
- $S_T$ — terminal stock price
- $K$ — strike price
- $(\cdot)^+$ — positive part
- $A$ — payoff of portfolio "long call, short put" at time $T$
:::

In both cases, Portfolio A's payoff equals $S_T - K$.

At time $T$, Portfolio B's payoff is $S_T - K$ (the bond accrues to $K$, which is repaid).

Portfolios A and B have identical payoffs in every state of the world at time $T$. By no-arbitrage, they must have the same value at time 0:

$$C - P = S_0 - K e^{-rT}. \qquad \square$$

---

## Put-call parity (with continuous dividend yield $q$)

### Theorem

When the underlying pays a continuous dividend yield $q \ge 0$:

$$C - P = S_0 e^{-qT} - K e^{-rT}.$$

::: where
- $C$ — time-0 European call price.
- $P$ — time-0 European put price.
- $S_0$ — current stock price.
- $K$ — common strike price.
- $T$ — time to expiration.
- $r$ — continuously-compounded risk-free rate.
- $q$ — continuously-compounded dividend yield.
- $S_0 e^{-qT}$ — present value of one share, adjusted for dividends paid over $[0, T]$.
:::

### Proof

Modify Portfolio B. To hold one share at time $T$ while collecting dividends continuously, invest in $e^{-qT}$ shares at time 0. Dividends are continuously reinvested, so the position grows to exactly one share at $T$.

**Portfolio A:** Long one call, short one put. Time-0 cost: $C - P$.

**Portfolio B:** Long $e^{-qT}$ shares (position grows to one share at $T$ via dividend reinvestment), short $K e^{-rT}$ in bonds. Time-0 cost: $S_0 e^{-qT} - K e^{-rT}$.

At time $T$, both portfolios deliver $S_T - K$ in all states (the analysis is identical to the no-dividend case at $T$). By no-arbitrage:

$$C - P = S_0 e^{-qT} - K e^{-rT}. \qquad \square$$

**Remark.** The quantity $S_0 e^{-qT}$ is the *dividend-adjusted forward price* of the stock: it represents the present value of receiving one share at time $T$, accounting for the dividend yield that effectively reduces the stock's growth rate under the risk-neutral measure. Setting $q = 0$ recovers the no-dividend formula.

---

## Synthetic positions

Put-call parity $C - P = S_0 e^{-qT} - K e^{-rT}$ can be rearranged to express any one of the four instruments — call, put, stock, bond — as a combination of the other three. These are called *synthetic* positions.

**Synthetic long stock.** Rearrange to $S_0 e^{-qT} = C - P + K e^{-rT}$. Investing $e^{-qT}$ shares today (equivalently, financing a long stock position adjusted for dividends) is replicated by: long call + short put + $K e^{-rT}$ in the risk-free bond. In the $q = 0$ case: long stock $\approx$ long call + short put + present value of strike in bond.

**Synthetic long call.** Rearrange to $C = P + S_0 e^{-qT} - K e^{-rT}$. A long call is replicated by: long put + long (dividend-adjusted) stock position + short $K e^{-rT}$ in bonds (i.e., borrowing the present value of the strike).

**Synthetic long put.** Rearrange to $P = C - S_0 e^{-qT} + K e^{-rT}$. A long put is replicated by: long call + short (dividend-adjusted) stock + long $K e^{-rT}$ in bonds. In the $q = 0$ case: long put $\approx$ long call + short stock + $K e^{-rT}$ in bond.

All three follow immediately from put-call parity — no additional proof is required.

---

## Practice
::: problem [Conceptual]
**Problem 5.1 [Conceptual].** Why is the call lower bound $S_0 - K e^{-rT}$ rather than $S_0 - K$?

::: solution
**Solution.** The strike $K$ is paid at expiration $T$, not at time 0. Today's value of "the obligation to pay $K$ at time $T$" is $K e^{-rT}$ — discounting at the continuously-compounded risk-free rate $r$ over horizon $T$. The lower bound $C \ge S_0 - K e^{-rT}$ corresponds exactly to the present value of a forward contract that pays $S_T - K$ at time $T$: its time-0 value is $S_0 - K e^{-rT}$ (by no-arbitrage — long stock, short $K$ in bonds). Using $S_0 - K$ instead would ignore time value of money: it would misprice the bond leg of the replicating portfolio and would not generally hold (for example, with $r > 0$ and $T$ large, $S_0 - K$ can be a tighter bound than is warranted, leading to apparent arbitrage that vanishes once discounting is accounted for correctly).
:::
:::

---

::: problem [Derivation]
**Problem 5.2 [Derivation].** Prove the put-call parity formula $C - P = S_0 - K e^{-rT}$ by explicit construction of the static replicating portfolio. Verify the payoff matches at $T$ and apply no-arbitrage at $t = 0$.

::: solution
**Solution.** We construct two portfolios with identical payoffs at $T$.

**Portfolio A (long call, short put).**

- At time 0: pay $C$, receive $P$; net cost $C - P$.
- At time $T$: payoff $= (S_T - K)^+ - (K - S_T)^+$.
  - If $S_T \ge K$: $= (S_T - K) - 0 = S_T - K$.
  - If $S_T < K$: $= 0 - (K - S_T) = S_T - K$.
- In all cases: payoff of A $= S_T - K$.

**Portfolio B (long stock, short bond).**

- At time 0: buy one share at cost $S_0$; borrow $K e^{-rT}$ (agree to repay $K$ at $T$); net cost $S_0 - K e^{-rT}$.
- At time $T$: receive $S_T$ from the share; repay $K$ on the bond; net payoff $= S_T - K$.

Portfolios A and B deliver $S_T - K$ in every state of the world at $T$. They have identical payoffs. By no-arbitrage, their time-0 values must be equal:

$$C - P = S_0 - K e^{-rT}. \qquad \square$$
:::
:::

---

::: problem [Computation]
**Problem 5.3 [Computation].** Suppose $S_0 = 50$, $K = 50$, $T = 0.5$, $r = 0.04$, $q = 0$. A European call trades in the market for $C = \$3.50$. What is the no-arbitrage price of the European put with the same strike and expiration?

::: solution
**Solution.** Apply put-call parity (no dividends):

$$C - P = S_0 - K e^{-rT}.$$

Compute the discounted strike:

$$K e^{-rT} = 50 \cdot e^{-0.04 \times 0.5} = 50 \cdot e^{-0.02} \approx 50 \times 0.9802 \approx 49.01.$$

Compute the right-hand side:

$$S_0 - K e^{-rT} = 50 - 49.01 = 0.99.$$

Solve for $P$:

$$P = C - 0.99 = 3.50 - 0.99 = \$2.51.$$

The no-arbitrage put price is $P \approx \$2.51$. Any deviation from this price would allow a riskless profit via the static replication described in Problem 5.2.
:::
:::
