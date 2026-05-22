# Chapter 1 — How Stock Prices Move

## Why Randomness Matters

If stock prices moved in predictable patterns, everyone would exploit them and the patterns would vanish. In practice, day-to-day price changes look random. Understanding *how* they are random — the shape and scale of that randomness — is the foundation of every option pricing model.

---

## Stock Returns Look Like a Bell Curve

Take any liquid stock and compute its daily percentage changes over a year. Plot a histogram and you get something close to a **normal distribution** — the classic bell curve. Most days the stock moves a little; big moves are rare.

### The Normal Distribution

A continuous random variable $X$ follows a normal distribution with mean $\mu$ and standard deviation $\sigma$ if its probability density function (PDF) is

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)$$

::: where
- $f(x)$ — probability density function
- $\mu$ — mean
- $\sigma$ — standard deviation
:::

We write $X \sim \mathcal{N}(\mu, \sigma^2)$. The special case $\mu = 0$, $\sigma = 1$ is the **standard normal** $Z \sim \mathcal{N}(0,1)$.

**The 68-95-99.7 rule.** For any normal variable:

| Range | Probability |
|---|---|
| $\mu \pm 1\sigma$ | $\approx 68\%$ |
| $\mu \pm 2\sigma$ | $\approx 95\%$ |
| $\mu \pm 3\sigma$ | $\approx 99.7\%$ |

Think of $\sigma$ as the "typical" deviation from the average. A $3\sigma$ event is extreme — it happens about 3 times in 1,000.

![Normal distribution bell curve](study/assets/normal_dist.svg)

---

## Log-Returns vs Simple Returns

### Simple return

The simple (or arithmetic) return from time $0$ to time $t$ is

$$R = \frac{S_t - S_0}{S_0}$$

::: where
- $R$ — simple return
- $S_t$ — stock price at time $t$
- $S_0$ — stock price at time $0$
:::

### Log-return

The log-return (or continuously compounded return) is

$$r = \ln\left(\frac{S_t}{S_0}\right)$$

::: where
- $r$ — log-return
:::

**Why do we prefer log-returns?** One killer property: **they are additive over time.** If the log-return from Monday to Tuesday is $r_1$ and from Tuesday to Wednesday is $r_2$, then the log-return from Monday to Wednesday is simply $r_1 + r_2$. Simple returns don't add like this — you'd need to multiply $(1 + R_1)(1 + R_2) - 1$.

Additivity makes the math clean: the sum of many small independent normal random variables is still normal. That is why assuming daily log-returns are normal leads to a tractable model.

---

## The Stock Price Model: Geometric Brownian Motion

Finance's workhorse model says that the stock price at a future time $T$ is

$$S_T = S_0 \exp\left(\left(\mu - \tfrac{1}{2}\sigma^2\right)T + \sigma\sqrt{T}\, Z\right), \quad Z \sim \mathcal{N}(0,1)$$

::: where
- $S_T$ — stock price at time $T$
- $T$ — time in years
- $Z$ — standard normal random variable
:::

Let's unpack each piece:

- **$S_0 \exp(\ldots)$:** The stock price is today's price scaled by an exponential factor. Because the exponential function is always positive, $S_T > 0$ no matter what $Z$ turns out to be. Stock prices can't go negative in this model.

- **$\mu T$:** This is the "drift." If there were no randomness ($\sigma = 0$), the stock would grow at rate $\mu$ per year. Think of it as the trend.

- **$-\frac{1}{2}\sigma^2 T$:** This is the **convexity correction** (sometimes called the Ito correction). It may look strange, but it ensures that the *expected* stock price is $S_0 e^{\mu T}$. Without it, the average of $e^X$ would overshoot because the exponential function is convex. Think of it as an accounting adjustment to keep the mean growth rate honest.

- **$\sigma \sqrt{T}\, Z$:** This is the random part. The shock $Z$ is drawn from a standard normal, so $\sigma\sqrt{T}\,Z$ has standard deviation $\sigma\sqrt{T}$. Randomness grows with the square root of time — wait four times as long and uncertainty only doubles.

### What the model says about log-returns

Taking $\ln$ of both sides:

$$\ln\left(\frac{S_T}{S_0}\right) = \left(\mu - \tfrac{1}{2}\sigma^2\right)T + \sigma\sqrt{T}\, Z$$

The log-return is **normally distributed** with mean $(\mu - \frac{1}{2}\sigma^2)T$ and standard deviation $\sigma\sqrt{T}$.

---

## The Lognormal Distribution

Since $\ln S_T$ is normal, $S_T$ itself follows a **lognormal distribution**. Its key features:

- **Bounded below by zero.** Prices can't go negative.
- **Right-skewed.** The distribution has a long tail to the right — there is no cap on how high the stock can go, but it can never fall below zero.
- **Not symmetric.** Unlike the bell curve, the lognormal peaks to the left of the mean and trails off slowly to the right.

Picture a histogram of possible future stock prices: a cluster near the current price, a tail stretching upward toward very high prices, and a hard wall at zero.

---

## Volatility: What $\sigma$ Really Means

Volatility $\sigma$ is the annualized standard deviation of log-returns. Here's how to make it concrete:

- **$\sigma = 0.20$ (20%)** means the stock's log-return over one year has a standard deviation of 20%. In a given year, roughly 68% of the time the stock ends within $\pm 20\%$ of its drift-adjusted expected value.

- **Daily volatility.** There are about 252 trading days per year, so the daily standard deviation is approximately

$$\sigma_{\text{daily}} \approx \frac{\sigma}{\sqrt{252}} \approx \frac{0.20}{15.87} \approx 0.0126 = 1.26\%$$

::: where
- $\sigma_{\text{daily}}$ — daily volatility
:::

So a stock with $\sigma = 0.20$ typically moves about 1.3% per day.

- **Historical volatility** is computed from past prices — look backward.
- **Implied volatility** is extracted from current option prices — look forward. We will explore implied volatility in later chapters.

---

## Worked Example

**Setup.** $S_0 = 100$, $\mu = 0.08$ (8% expected annual return), $\sigma = 0.20$ (20% volatility), $T = 1$ year.

### (a) Expected stock price

The expected value of $S_T$ under this model is

$$E[S_T] = S_0 e^{\mu T} = 100 \times e^{0.08 \times 1} = 100 \times 1.0833 = 108.33$$

::: where
- $E[S_T]$ — expected stock price
:::

### (b) Probability that $S_T > 120$

We need $P(S_T > 120)$.

**Step 1 — Rewrite in log terms.** The stock price $S_T$ itself is not normally distributed, but $\ln S_T$ is. So we take the log of both sides to convert the question into one we can solve with a bell curve:

$$S_T > 120 \quad \Longleftrightarrow \quad \ln S_T > \ln 120 = 4.7875$$

**Step 2 — Identify the bell curve.** Start from GBM and take $\ln$ of both sides:

$$S_T = S_0 \times \exp\left((\mu - \tfrac{1}{2}\sigma^2)T + \sigma\sqrt{T}\, Z\right)$$

$$\ln S_T = \ln S_0 + (\mu - \tfrac{1}{2}\sigma^2)T + \sigma\sqrt{T}\, Z$$

The $\times$ became $+$ because $\ln(A \times e^B) = \ln A + B$. Now the right side is just a constant plus a normal random variable, so:

$$\ln S_T \sim \mathcal{N}\left(\ln S_0 + (\mu - \tfrac{1}{2}\sigma^2)T,\; \sigma^2 T\right)$$

Plug in numbers:

- Mean of $\ln S_T$: $\ln 100 + (0.08 - 0.02)(1) = 4.6052 + 0.06 = 4.6652$
- Std dev of $\ln S_T$: $\sigma\sqrt{T} = 0.20 \times \sqrt{1} = 0.20$

So the bell curve for $\ln S_T$ is centered at 4.6652 with a width (std dev) of 0.20.

**Step 3 — Standardize.** Every bell curve has a different center and width, so we can't look up probabilities directly. We convert to the **standard** bell curve $\mathcal{N}(0,1)$ by asking: "How many standard deviations away from the center is our target value?"

$$z = \frac{\text{target} - \text{mean}}{\text{std dev}} = \frac{4.7875 - 4.6652}{0.20} = \frac{0.1223}{0.20} = 0.6116$$

This tells us 4.7875 sits **0.61 standard deviations above the center** of the bell curve.

**Step 4 — Look up the probability.** Now we just need: what fraction of the standard bell curve sits to the right of $z = 0.6116$? Using a standard normal table (or calculator):

$$P(S_T > 120) = P(Z > 0.6116) = 1 - \Phi(0.6116) \approx 1 - 0.7296 = 0.2704$$

::: where
- $\Phi(\cdot)$ — standard normal CDF (the table that tells you how much of the bell curve is to the left of a given $z$-value)
:::

**Interpretation.** There is about a **27% chance** the stock finishes above 120 after one year. In other words, 27% of the bell curve's area lies to the right of our target.

---

## Practice

::: problem [Computation]
**Problem 1.1.** A stock has $S_0 = 50$, $\mu = 0.10$, $\sigma = 0.30$, and $T = 0.5$ (six months). Compute:
(a) The expected stock price $E[S_T]$.
(b) The standard deviation of $\ln S_T$.
(c) The probability that the stock falls below $40$.

::: solution
**Solution.**

**(a)** $E[S_T] = 50 \times e^{0.10 \times 0.5} = 50 \times e^{0.05} = 50 \times 1.05127 = 52.56$.

**(b)** $\text{Std dev of } \ln S_T = \sigma\sqrt{T} = 0.30 \times \sqrt{0.5} = 0.30 \times 0.7071 = 0.2121$.

**(c)** Mean of $\ln S_T = \ln 50 + (0.10 - 0.045)(0.5) = 3.9120 + 0.0275 = 3.9395$.

We need $P(\ln S_T < \ln 40) = P(\ln S_T < 3.6889)$.

$z = \frac{3.6889 - 3.9395}{0.2121} = \frac{-0.2506}{0.2121} = -1.1816$

$P(Z < -1.1816) = \Phi(-1.1816) \approx 0.1187$.

There is about an **11.9% chance** the stock falls below 40.
:::
:::

::: problem [Computation]
**Problem 1.2.** Two stocks both have $\sigma = 0.25$. Stock A has $\mu = 0.05$ and Stock B has $\mu = 0.12$. Both start at $S_0 = 100$ with $T = 2$ years. Compute the expected price and the probability of doubling ($S_T > 200$) for each stock.

::: solution
**Solution.**

**Stock A:**
- $E[S_T] = 100 e^{0.05 \times 2} = 100 e^{0.10} = 110.52$.
- Mean of $\ln S_T = \ln 100 + (0.05 - 0.03125)(2) = 4.6052 + 0.0375 = 4.6427$.
- Std dev $= 0.25\sqrt{2} = 0.3536$.
- $P(S_T > 200)$: $z = \frac{\ln 200 - 4.6427}{0.3536} = \frac{5.2983 - 4.6427}{0.3536} = \frac{0.6556}{0.3536} = 1.854$.
- $P = 1 - \Phi(1.854) \approx 1 - 0.9681 = 0.0319$ or about **3.2%**.

**Stock B:**
- $E[S_T] = 100 e^{0.12 \times 2} = 100 e^{0.24} = 127.12$.
- Mean of $\ln S_T = \ln 100 + (0.12 - 0.03125)(2) = 4.6052 + 0.1775 = 4.7827$.
- Std dev $= 0.3536$ (same volatility).
- $P(S_T > 200)$: $z = \frac{5.2983 - 4.7827}{0.3536} = \frac{0.5156}{0.3536} = 1.458$.
- $P = 1 - \Phi(1.458) \approx 1 - 0.9276 = 0.0724$ or about **7.2%**.

Higher drift more than doubles the probability of doubling, even though volatility is the same.
:::
:::

::: problem [Conceptual]
**Problem 1.3.** Explain intuitively why the convexity correction $-\frac{1}{2}\sigma^2$ appears in the GBM formula. What would go wrong if we used $S_T = S_0 e^{\mu T + \sigma\sqrt{T}\,Z}$ without it?

::: solution
**Solution.** The exponential function is convex — it curves upward. By Jensen's inequality, the average of $e^X$ is greater than $e^{\text{average of } X}$. So if the log-return had mean $\mu T$ (i.e., $X = \mu T + \sigma\sqrt{T}\,Z$), then $E[e^X] > e^{\mu T}$, meaning the expected stock price would be *higher* than $S_0 e^{\mu T}$.

The correction term $-\frac{1}{2}\sigma^2 T$ shifts the mean of the log-return downward by exactly the right amount so that $E[S_T] = S_0 e^{\mu T}$.

Without the correction, a stock with higher volatility would have a higher expected price even if both stocks had the same drift $\mu$. That doesn't make economic sense — higher volatility means more risk, not a free lunch in expected return.
:::
:::
