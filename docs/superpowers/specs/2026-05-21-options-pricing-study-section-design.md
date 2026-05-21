# Options Pricing Theory — Study Section Integration Design

**Date:** 2026-05-21
**Owner:** kasper.chen@stranity.com
**Status:** Design approved, pending implementation plan

---

## Background

The user has two separate projects:

1. `C:\Users\User\Desktop\Options_Pricing_Theory\` — a markdown-based options pricing lesson with a Python PDF generator. The current lesson covers BSM, Greeks, IV, and the volatility surface at a trader-intuition level, with no probability/stochastic-calculus foundations and no derivations.
2. `C:\Users\User\Desktop\certificate_practice\` — a single-file mobile-friendly webapp (`index.html` + `questions.json`) hosting three Taiwan financial-certification quiz banks (期貨商業務員 / 證券商高級業務員 / 金融市場常識與職業道德). Apple-style design, Traditional Chinese UI, localStorage state, GitHub Pages deployment.

The user wants to consolidate: move the options pricing content into `certificate_practice/` as a fourth content area — a **study section** (lesson-style reading, not a quiz bank) — so the material can be studied online. The existing PDF pipeline is no longer needed; the website is the delivery vehicle. The old project folder will be deleted after migration.

The new content must:

- Be focused exclusively on **European options theory** (BSM is European-only anyway; American/Bermudan get a contrast paragraph at most).
- Include a **probability/stochastic-calculus primer** appropriate for a grad-level math/stats reader (terse review + full rigor on key results: Itô, Girsanov, martingale representation).
- Derive the Black-Scholes equation **both ways**: replicating-portfolio PDE (with boundary conditions at S=0 and S→∞) and risk-neutral expectation, then reconcile via Feynman-Kac.
- Present **all formulas in proper LaTeX math** (rendered via KaTeX in-browser) with every symbol explicitly defined.
- **Every formula is immediately followed by a "where" block** that defines every symbol appearing in that formula, so the reader never has to scroll back to find what a symbol means. Even symbols defined earlier in the chapter are restated under each formula.
- Embed **2-3 practice problems with worked solutions after each major concept**: one conceptual, one derivation/proof, one computation. Click-to-reveal solutions.

---

## Goals

1. Add a fourth home-screen content area to `certificate_practice/index.html` labeled "Options Pricing Theory" that opens a study/reading experience using the existing site's visual design.
2. Author a self-contained, rigorous, 12-chapter graduate-level European options textbook in markdown, stored under `certificate_practice/study/chapters/`.
3. Render chapters in-browser with `marked.js` (markdown → HTML) and KaTeX (`$...$` and `$$...$$` math).
4. Support click-to-reveal practice problem solutions via a `::: problem [tag] ... ::: solution ... ::: :::` markdown convention.
5. Persist last-read chapter and visited-chapter set in `localStorage` so the user can resume.
6. Keep the existing quiz functionality untouched.
7. Delete the old `C:\Users\User\Desktop\Options_Pricing_Theory\` folder after migration.

## Non-goals

- No changes to existing quiz logic, results page, or review page.
- No changes to `questions.json` or quiz-bank build scripts.
- No PDF generation, no print stylesheet.
- No quiz-bank-style integration for study problems (they remain click-to-reveal, not multiple-choice with localStorage stats).
- No translation of the existing Chinese quiz UI to English.
- No build step for study content — chapters are markdown rendered at runtime.
- No full derivations for surface models (Dupire / Heston / SABR / SVI) — they are stated only.

---

## Repository layout

```
certificate_practice/
├── index.html                       Modified: KaTeX/marked CDN + 4th home button + 2 new pages + ~150 lines JS
├── questions.json                   Unchanged
├── CLAUDE.md                        Updated to document the study section
├── README.md                        Updated to mention the study section
├── scripts/                         Unchanged
├── sources/                         Unchanged
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-05-21-options-pricing-study-section-design.md   This file
└── study/                           NEW
    ├── index.json                   Ordered chapter list with titles
    ├── chapters/
    │   ├── 01_preface.md
    │   ├── 02_probability.md
    │   ├── 03_stochastic_calculus.md
    │   ├── 04_no_arbitrage.md
    │   ├── 05_european_payoffs.md
    │   ├── 06_bsm_pde.md
    │   ├── 07_solving_pde.md
    │   ├── 08_risk_neutral.md
    │   ├── 09_greeks.md
    │   ├── 10_implied_vol.md
    │   ├── 11_iv_surface.md
    │   └── 12_surface_models.md
    └── assets/                      Reserved for any inline images/diagrams
```

After implementation passes verification, the entire `C:\Users\User\Desktop\Options_Pricing_Theory\` folder is deleted.

---

## User flow

### Home screen (existing + 1 new button)

```
[期貨商業務員]
[證券商高級業務員]
[金融市場常識與職業道德]
[Options Pricing Theory]          ← NEW, navy like quiz buttons, English label
[常錯題複習]
[清除作答紀錄]
```

The new button's `topic-meta` subtitle reads "Self-study lessons" (English) to differentiate it from quiz buttons.

### Chapter list page (`page-study-list`)

```
Options Pricing Theory
A self-contained graduate treatment of European options.

[ Resume: Chapter 6 — Black-Scholes PDE ]      ← only shown if study_state_v1.lastChapter exists

1. Preface and Notation                    ✓
2. Probability Review                      ✓
3. Stochastic Calculus
4. No-Arbitrage and Replication
...
12. Surface Models

[← Home]
```

A small `✓` next to a chapter title indicates it appears in `study_state_v1.visited`.

### Chapter view page (`page-study-chapter`)

```
[← Chapters]    Ch. 6 of 12          [progress bar]

# (chapter content — headings, theorem boxes, math, worked
   examples, practice problems with click-to-reveal solutions)

[← Previous: Ch.5]                     [Next: Ch.7 →]
```

`[← Previous]` is disabled on Ch. 1, `[Next →]` is disabled on Ch. 12. Tapping `[← Chapters]` returns to the chapter list. Scroll resets to top on chapter change.

---

## Content design

### Chapter template

Every chapter follows the same shape:

```
# Chapter N — Title

## Goals
- bullet list of what the reader will be able to do/derive/state by the end

## Prerequisites
- pointers to earlier chapters and outside knowledge assumed

## (Content sections)
  ### Definition X.Y
  ### Theorem X.Y     (statement)
  ### Proof           (or "Proof sketch")
  ### Remark
  ### Worked example  (numerical when applicable)

## Practice
  ### Problem N.1 [Conceptual]
  ### Problem N.2 [Derivation]
  ### Problem N.3 [Computation]
  (each with click-to-reveal solution)

## Summary
- 3-5 take-away facts
```

### Formula-and-where convention (applies everywhere)

**Every** non-trivial formula in the body, in worked examples, and in problem solutions is followed by a "where" block listing every symbol that appears in that formula. Even symbols that were defined earlier in the chapter are restated. Trivial inline formulas (e.g., `$S=100$`, `$T=0.25$`) are exempt.

Authored in markdown as:

````
$$
dS_t = \mu S_t\, dt + \sigma S_t\, dW_t
$$

::: where
- $S_t$ — stock price at time $t$
- $\mu$ — drift (annualized expected log-return)
- $\sigma$ — volatility (annualized standard deviation of returns)
- $dW_t$ — increment of a standard Brownian motion under $\mathbb{P}$
- $dt$ — infinitesimal time increment
:::
````

The preprocessor (described in section *Markdown problem-block preprocessor*) handles the `::: where ... :::` block in addition to `::: problem`/`::: solution`. Output HTML:

```html
<div class="where">
  <div class="where-label">where</div>
  <ul>
    <li><span class="sym">$S_t$</span> — stock price at time $t$</li>
    ...
  </ul>
</div>
```

KaTeX auto-render then typesets the math inside `<li>` and `.sym` spans.

### Chapter outline

| # | Title | Substance |
|---|-------|-----------|
| 1 | Preface and Notation | Symbol table, conventions, European-only scope statement, intended reader |
| 2 | Probability Review | (Ω, F, P), filtrations, conditional expectation, tower property, normal/lognormal MGFs. Theorems stated; key identities (lognormal mean/variance, E[(S−K)⁺] under log-normal) proved |
| 3 | Stochastic Calculus | Brownian motion (definition + Lévy characterization stated). Quadratic variation [W,W]_t = t proved in L². Itô integral construction sketched. Itô's lemma stated and proved for f ∈ C^{1,2}. GBM as unique solution of dS = μS dt + σS dW (verified by Itô). Girsanov stated with explicit RN derivative |
| 4 | No-Arbitrage and Replication | Self-financing condition derived. First Fundamental Theorem stated. Risk-neutral measure Q characterized: discounted price S̃_t = e^{-rt}S_t is a Q-martingale |
| 5 | European Option Payoffs | Payoff functions, monotonicity & convexity in S, K. Put-call parity proved via static replication. Standard arbitrage bounds |
| 6 | The Black-Scholes PDE | Set V(S,t) ∈ C^{2,1}. Portfolio Π = V − Δ S with Δ = ∂V/∂S. Itô on V, dW cancels by Δ choice. Self-financing + no-arbitrage forces dΠ = rΠ dt, yielding ∂V/∂t + ½σ²S² ∂²V/∂S² + rS ∂V/∂S − rV = 0. Boundary conditions stated and justified: terminal V(S,T) = payoff; for call C(0,t)=0, C(S,t) ~ S − Ke^{-r(T-t)} as S→∞; for put P(0,t)=Ke^{-r(T-t)}, P(S,t)→0 as S→∞. Uniqueness via Feynman-Kac (forward reference to Ch. 8) |
| 7 | Solving the PDE | Change of variables x = ln(S/K), τ = ½σ²(T−t), V = K e^{αx+βτ} u(x,τ) with α, β chosen to kill drift and rV term. Reduces to ∂u/∂τ = ∂²u/∂x². Solve via Gaussian heat kernel. Back-substitute → C = S N(d₁) − K e^{-rT} N(d₂). Verify the closed form satisfies the PDE and both BCs |
| 8 | Risk-Neutral Derivation | Girsanov with θ = (μ−r)/σ removes drift. Under Q, dS = rS dt + σS dW^Q. Compute C = e^{-rT} E^Q[(S_T−K)⁺] directly by integrating against the log-normal density; recover the same closed form. Feynman-Kac links PDE and expectation views |
| 9 | The Greeks | Δ, Γ, Θ, Vega, ρ derived by differentiating the closed form. Identity ½σ²S²Γ + rSΔ + Θ = rV restated as a sanity check on the PDE |
| 10 | Implied Volatility | IV defined as unique σ solving market_price = BSM(σ). Uniqueness from Vega > 0 (proved). Newton-Raphson with convergence note. IV vs realized vol |
| 11 | The IV Surface | Smile/skew/term structure described. No-arbitrage constraints proved from RN density non-negativity: butterfly (∂²C/∂K² ≥ 0) and calendar (total variance non-decreasing). Sticky strike vs sticky delta. Skew-adjusted delta |
| 12 | Surface Models | Dupire local vol, Heston, SABR, SVI: SDE statements and one-line motivation each. No derivations |

### Sample practice problem

The example the user provided in the original request:

```
::: problem [Derivation]
**Problem 6.2.** Derive the Black-Scholes PDE for a non-dividend-paying stock $S$
following $dS = \mu S\, dt + \sigma S\, dW$ under $\mathbb{P}$. State and justify
the boundary conditions at $S=0$ and as $S \to \infty$ for a European call.

::: solution
(Full worked answer reproducing the Ch. 6 derivation in self-contained form, plus
a paragraph for each boundary condition with the financial reasoning: $S$ pinned
at $0$ stays at $0$ under GBM, so the call is worthless; deep ITM call is
approximately a forward contract on $S$ minus the discounted strike.)
:::
:::
```

This is the canonical example of how derivation-style problems are authored.

---

## Implementation contract

### 1. File migration

- Author new chapters 01-12 fresh in `certificate_practice/study/chapters/` against the outline above. The new chapters are written to the design, not copy-pasted from the old project.
- The old `Options_Pricing_Theory/markdown/*.md` files serve as reference material only during authoring (rough mapping: old `01_Foundations.md` → new Ch. 4-5; old `02_Black_Scholes_Model.md` → new Ch. 6-8; old `03_The_Greeks.md` → new Ch. 9; old `04_Implied_Volatility.md` → new Ch. 10; old `05_IV_Surface.md` → new Ch. 11; old `06_Putting_It_Together.md` → distributed). Reference only — content depth, structure, and rigor level differ substantially.
- The combined `Options_Pricing_Complete_Lesson.md` is not migrated.
- The old `pdf/`, `to_pdf.py`, `cheatsheet_to_pdf.py`, `knowledge/`, `CLAUDE.md`, and `Formula_Cheatsheet.md` are not migrated.
- After end-to-end verification of the website (chapter list + all 12 chapters rendering, navigation working, quiz functionality unchanged), delete the entire `C:\Users\User\Desktop\Options_Pricing_Theory\` folder.

### 2. New file: `certificate_practice/study/index.json`

```json
{
  "title": "Options Pricing Theory",
  "subtitle": "A self-contained graduate treatment of European options.",
  "chapters": [
    { "file": "01_preface.md",             "title": "Preface and Notation" },
    { "file": "02_probability.md",         "title": "Probability Review" },
    { "file": "03_stochastic_calculus.md", "title": "Stochastic Calculus" },
    { "file": "04_no_arbitrage.md",        "title": "No-Arbitrage and Replication" },
    { "file": "05_european_payoffs.md",    "title": "European Option Payoffs" },
    { "file": "06_bsm_pde.md",             "title": "The Black-Scholes PDE" },
    { "file": "07_solving_pde.md",         "title": "Solving the PDE" },
    { "file": "08_risk_neutral.md",        "title": "Risk-Neutral Derivation" },
    { "file": "09_greeks.md",              "title": "The Greeks" },
    { "file": "10_implied_vol.md",         "title": "Implied Volatility" },
    { "file": "11_iv_surface.md",          "title": "The IV Surface" },
    { "file": "12_surface_models.md",      "title": "Surface Models" }
  ]
}
```

### 3. Edits to `certificate_practice/index.html`

**a. `<head>` — add deferred CDN tags:**

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
```

**b. Home screen — add fourth content button after the three quiz buttons, before `#btn-review`:**

```html
<button class="btn" id="btn-study">Options Pricing Theory
  <div class="topic-meta">Self-study lessons</div>
</button>
```

**c. New page divs after `#page-review`:**

```html
<div id="page-study-list" class="hidden study">
  <h1 id="study-title">—</h1>
  <p class="meta" id="study-subtitle">—</p>
  <div id="study-resume-banner" class="hidden card" style="border-left:4px solid var(--accent);">
    <div style="font-weight:600;margin-bottom:4px;">Resume</div>
    <div class="meta" id="study-resume-meta">—</div>
    <button class="btn" id="btn-study-resume" style="margin-top:10px;margin-bottom:0;">Continue</button>
  </div>
  <div id="study-chapter-list"></div>
  <button class="btn secondary" id="btn-study-home">← Home</button>
</div>

<div id="page-study-chapter" class="hidden study">
  <div class="progress-wrap">
    <div class="progress-bar"><div class="progress-fill" id="study-progress-fill"></div></div>
    <div class="progress-label">
      <span id="study-chapter-label">—</span>
      <span id="study-chapter-counter">—</span>
    </div>
  </div>
  <button class="btn secondary" id="btn-study-back" style="margin-bottom:12px;">← Chapters</button>
  <div id="study-chapter-content" class="card"></div>
  <div class="nav">
    <button class="btn secondary" id="btn-study-prev">← Previous</button>
    <button class="btn" id="btn-study-next">Next →</button>
  </div>
</div>
```

**d. CSS — add `.study`-scoped rules from the Styling section below.**

**e. JS — extend `show()` page list to include `page-study-list` and `page-study-chapter`. Add new code:**

- `STUDY_INDEX` global — populated on first study-section open from `study/index.json`.
- `STUDY_STATE_KEY = 'study_state_v1'`, schema `{ lastChapter: number, visited: number[] }`.
- `loadStudyState() / saveStudyState()` — JSON localStorage round-trip.
- `openStudySection()` — wire button; fetches `study/index.json` if not cached, renders chapter list.
- `renderStudyList()` — paints chapter cards; highlights resume banner if `lastChapter` exists.
- `openChapter(idx)`:
  1. Fetch `study/chapters/<file>`.
  2. Preprocess `::: problem [tag] ... ::: solution ... ::: :::` blocks into `<div class="problem"><div class="ptag">tag</div>...<button class="reveal-btn">Show solution</button><div class="solution">...</div></div>`.
  3. `marked.parse()`.
  4. `renderMathInElement()` (KaTeX auto-render with `[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}]`).
  5. Update `study_state_v1.lastChapter = idx`, push to `visited`.
  6. Wire reveal buttons.
  7. Update progress bar, prev/next button states.
  8. `show('page-study-chapter')`.
- Prev/Next/Back handlers wired.
- CDN load failure handling: if `marked` or `katex` is undefined when `openChapter` is called, show the raw markdown in a `<pre>` block as a fallback (still readable, with `$...$` visible).

### 4. Markdown block preprocessor (problem, solution, where)

Implemented as a small state machine (~50 lines of JS) inside `index.html`. Runs **before** `marked.parse` on each chapter's markdown. It handles three custom block types: `::: problem [tag]`, `::: solution`, and `::: where`.

**Problem / solution example:**

```
::: problem [Derivation]
**Problem 6.2.** ... $math$ ...

::: solution
... worked answer ...
:::
:::
```

transforms to:

```html
<div class="problem">
  <div class="ptag">Derivation</div>
  <div class="problem-stmt">**Problem 6.2.** ... $math$ ...</div>
  <button class="reveal-btn">Show solution</button>
  <div class="solution">... worked answer ...</div>
</div>
```

**Where example:**

```
::: where
- $S_t$ — stock price at time $t$
- $\sigma$ — volatility
:::
```

transforms to:

```html
<div class="where">
  <div class="where-label">where</div>
  <ul>
    <li>$S_t$ — stock price at time $t$</li>
    <li>$\sigma$ — volatility</li>
  </ul>
</div>
```

The inner markdown (`**bold**`, `$math$`, etc.) is then processed by marked + KaTeX normally. The reveal button toggles `.problem.revealed` on its parent `<div class="problem">` and swaps its own label between "Show solution" and "Hide solution".

**Preprocessor rules:**
- A line starting with `:::` followed by `problem`, `solution`, or `where` opens a block.
- A bare `:::` line closes the most recently opened block.
- `:::` lines inside fenced code blocks (between matching ``` fences) are ignored.
- Mismatched nesting (e.g., `:::` with no open block) is logged to console and rendered as literal text.

### 5. Styling (scoped to `.study`)

```css
.study h1 { font-size: 24px; margin: 8px 0 16px; }
.study h2 { font-size: 19px; margin: 24px 0 8px; color: var(--accent); }
.study h3 { font-size: 16px; margin: 16px 0 6px; }
.study p, .study li { font-size: 15px; line-height: 1.65; }

.study .thm, .study .defn, .study .proof, .study .remark {
  border-left: 4px solid var(--accent);
  padding: 10px 14px; margin: 14px 0;
  background: var(--card); border-radius: 4px 10px 10px 4px;
}
.study .thm::before { content: "Theorem"; font-weight: 700; color: var(--accent);
                      display: block; font-size: 12px; letter-spacing: 0.5px; }
.study .defn::before { content: "Definition"; font-weight: 700; color: var(--accent);
                       display: block; font-size: 12px; letter-spacing: 0.5px; }
.study .proof::before { content: "Proof"; font-weight: 700; color: var(--accent);
                        display: block; font-size: 12px; letter-spacing: 0.5px; }
.study .remark { border-left-color: var(--muted); }
.study .remark::before { content: "Remark"; font-weight: 700; color: var(--muted);
                         display: block; font-size: 12px; letter-spacing: 0.5px; }

.study .where {
  background: rgba(30, 58, 95, 0.04);
  border-left: 3px solid var(--accent);
  padding: 8px 12px 8px 14px; margin: 6px 0 14px;
  border-radius: 0 6px 6px 0;
}
.study .where .where-label {
  font-size: 11px; font-weight: 700; color: var(--accent);
  letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 4px;
}
.study .where ul { margin: 0; padding-left: 18px; }
.study .where li { font-size: 14px; line-height: 1.55; margin-bottom: 2px; color: var(--text); }
.study .where li .katex { font-size: 1em; }

.study .problem { background: var(--card); border: 1px solid var(--border);
                  border-radius: 10px; padding: 14px; margin: 14px 0; }
.study .problem .ptag { display: inline-block; font-size: 11px; font-weight: 700;
                        color: var(--accent); letter-spacing: 0.5px;
                        text-transform: uppercase; margin-bottom: 6px; }
.study .problem .solution { display: none; margin-top: 12px; padding-top: 12px;
                            border-top: 1px solid var(--border); }
.study .problem.revealed .solution { display: block; }
.study .reveal-btn { background: transparent; color: var(--accent);
                     border: 1px solid var(--accent); border-radius: 8px;
                     padding: 8px 14px; font-weight: 600; cursor: pointer; font-family: inherit; }
.study .reveal-btn:active { background: rgba(30,58,95,0.08); }

.study .katex-display { overflow-x: auto; overflow-y: hidden; padding: 4px 0; }

.study-chapter-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 16px; background: var(--card);
  border: 1px solid var(--border); border-radius: 10px;
  margin-bottom: 8px; cursor: pointer; font-size: 15px;
}
.study-chapter-row:active { background: #eef0f4; }
.study-chapter-row .num { color: var(--muted); font-weight: 600; min-width: 28px; }
.study-chapter-row .visited { color: var(--good); font-size: 16px; }
```

### 6. CLAUDE.md updates (in `certificate_practice/CLAUDE.md`)

Add a new "Study section" subsection describing:

- The 4th content area: Options Pricing Theory.
- English UI scoped to the study section only.
- Chapter pipeline: markdown → `marked.parse` → KaTeX `renderMathInElement`. CDN-loaded.
- Storage: `study_state_v1` localStorage key, schema `{ lastChapter, visited }`.
- Problem-box markdown convention.
- How to add or edit chapters (edit the .md file, refresh the page — no build step).

### 7. README updates

Add a one-line feature mention in the README's feature list referencing the study section.

---

## Definition of done

1. Tapping the new home button opens the chapter list. The list shows 12 chapters with correct titles.
2. All 12 chapters open from the chapter list. Each renders math correctly (no stray `$` left in the output, fractions/sums/integrals display properly). Each contains 2-3 practice problems with working click-to-reveal solutions. **Every non-trivial formula is followed by a `where` block defining every symbol that appears in it.**
3. `Previous` is disabled on Chapter 1; `Next` is disabled on Chapter 12; intermediate chapters allow both.
4. After viewing a chapter and returning to the chapter list, a `Resume: Ch. N — Title` banner appears; tapping `Continue` reopens that chapter.
5. Chapters previously visited show a check mark in the chapter list.
6. Existing quiz functionality is unchanged. Smoke test: start a 期貨商業務員 quiz, answer 3 questions, tap `儲存並回到首頁`, resume from home, abort. All steps behave as before.
7. CSS used by the study section does not bleed into quiz pages (theorem boxes don't appear in the quiz; reveal buttons don't appear on the home page).
8. The whole site renders correctly on mobile at width 375px (chapter content scrolls horizontally only inside `.katex-display` for wide formulas; the page itself does not horizontal-scroll).
9. The old `C:\Users\User\Desktop\Options_Pricing_Theory\` folder is deleted from disk.
10. `git status` in `certificate_practice/` shows expected adds/modifications and nothing else.

---

## Risks and mitigations

| Risk | Mitigation |
|------|-----------|
| CDN unavailable when opening study section | Fallback: render markdown as `<pre>` if `marked`/`katex` undefined. Site still loads and reads. |
| Authoring all 12 chapters at graduate rigor is a large content task | Implementation plan can split chapter authoring across multiple sessions / parallel agents per chapter group. |
| `::: problem ::: solution :::` preprocessor regex edge cases (nested code blocks, math with `:::` literal, etc.) | Preprocessor uses a state machine on `:::`-prefixed lines, not a single regex. Reject `:::` lines inside code fences. |
| Existing site CSS already uses `.feedback`, `.expl-block`, etc.; risk of class name collision | All new CSS is scoped under `.study` selector. Verified no existing class names overlap. |
| Old project folder deletion is irreversible | Verify website end-to-end before deleting. Keep old folder until the last implementation step. |
| Mobile horizontal overflow on wide formulas | `.katex-display { overflow-x: auto; }` confines scroll to the formula box only. |

---

## Out of scope

- Quiz-bank-style integration for study problems (no MC, no localStorage stats for the study section beyond `lastChapter` / `visited`).
- Print stylesheet / PDF export.
- Bookmarking sub-sections within a chapter (resume is chapter-level only).
- Search across the study content.
- Translating any existing Chinese UI to English.
- Building the surface models (Heston / SABR / SVI / Dupire) at full-derivation depth.
- Updating the `scripts/build.py` or question-bank pipeline.
