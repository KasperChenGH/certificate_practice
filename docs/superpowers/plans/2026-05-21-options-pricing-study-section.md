# Options Pricing Study Section — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a graduate-level Options Pricing Theory study section as a 4th content area to `certificate_practice/index.html`, with 12 chapters of rigorous European-options content rendered in-browser via marked + KaTeX. After verification, delete the old `C:\Users\User\Desktop\Options_Pricing_Theory\` folder.

**Architecture:** Two new pages (chapter list + chapter view) added to the existing single-file webapp. Chapter markdown files live under `study/chapters/` and are fetched and rendered on demand. Custom `:::` block preprocessor handles `problem`, `solution`, and `where` (symbol-definition) blocks. localStorage tracks last-read chapter and visited set.

**Tech Stack:** HTML/CSS/vanilla JS (existing); `marked@12` (markdown→HTML via CDN); `katex@0.16.9` + auto-render (math typesetting via CDN); localStorage for state.

**Spec:** `docs/superpowers/specs/2026-05-21-options-pricing-study-section-design.md`

**Working directory:** All paths below are relative to `C:\Users\User\Desktop\certificate_practice\` unless otherwise noted.

**Commit style:** Match existing repo convention — short imperative messages, no conventional-commit prefix. E.g., `Add Options Pricing study section scaffold`, not `feat: add scaffold`.

---

## Phase 1 — Scaffolding (Tasks 1-10)

Build the empty study section: navigation, page rendering, preprocessor, styles. No content yet — chapter files are stubs until Phase 2.

---

### Task 1: Create study directory layout and stub chapter files

**Files:**
- Create: `study/index.json`
- Create: `study/chapters/01_preface.md` … `study/chapters/12_surface_models.md` (12 stubs)
- Create: `study/assets/.gitkeep`

- [ ] **Step 1: Make directories**

Run from `C:\Users\User\Desktop\certificate_practice\`:
```
mkdir study\chapters study\assets 2>nul
```

- [ ] **Step 2: Create `study/index.json` with full chapter list**

Content:
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

- [ ] **Step 3: Create 12 stub chapter files**

Each stub file contains only:
```markdown
# Chapter N — <Title>

*(Content to be authored in a later task.)*
```

For example, `study/chapters/01_preface.md`:
```markdown
# Chapter 1 — Preface and Notation

*(Content to be authored in a later task.)*
```

Repeat for chapters 2-12, substituting the matching title from `study/index.json`.

- [ ] **Step 4: Create `study/assets/.gitkeep`** (empty file, so the directory is tracked by git)

- [ ] **Step 5: Commit**

```
git add study/
git commit -m "Add Options Pricing study section scaffold"
```

---

### Task 2: Add KaTeX and marked CDN tags to index.html

**Files:**
- Modify: `index.html` (around the existing `<style>` tag near top of `<head>`)

- [ ] **Step 1: Open `index.html` and locate line 7**

Existing line 7:
```html
<title>金融證照練習</title>
```

- [ ] **Step 2: Insert these four lines immediately after `<title>`** (before the `<style>` opening tag)

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
```

- [ ] **Step 3: Manual verification**

Run a local server and open the page in a browser:
```
python -m http.server 8000
```
Then open `http://localhost:8000` in Chrome. Open DevTools console and run:
```js
typeof marked, typeof katex, typeof renderMathInElement
```
Expected output: `"object" "object" "function"` (all three defined).

- [ ] **Step 4: Commit**

```
git add index.html
git commit -m "Add KaTeX and marked CDN tags"
```

---

### Task 3: Add the study CSS block (scoped under .study)

**Files:**
- Modify: `index.html` (inside `<style>`, before the closing `</style>` tag at line 141)

- [ ] **Step 1: Insert this CSS block immediately before `</style>`**

```css
  /* ===== Study section (Options Pricing Theory) ===== */
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

  @media (prefers-color-scheme: dark) {
    .study .where { background: rgba(110, 161, 216, 0.08); }
    .study-chapter-row:active { background: #2a2a2c; }
  }
```

- [ ] **Step 2: Commit**

```
git add index.html
git commit -m "Add CSS for study section"
```

---

### Task 4: Add the new home button and two new page divs

**Files:**
- Modify: `index.html` (home section around line 169 and after `#page-review` around line 214)

- [ ] **Step 1: Add the home button**

Find existing line 169 (the `#btn-review` button):
```html
    <button class="btn review" id="btn-review">常錯題複習</button>
```

Insert the new button immediately before `#btn-review`:
```html
    <button class="btn" id="btn-study">Options Pricing Theory<div class="topic-meta">Self-study lessons</div></button>
```

- [ ] **Step 2: Add the two new page divs**

Find the closing of `#page-review` (currently `</div>` at line 214). Immediately after `</div>` (the one closing `#page-review`), insert:

```html
  <!-- STUDY: chapter list -->
  <div id="page-study-list" class="hidden study">
    <h1 id="study-title">—</h1>
    <p class="meta" id="study-subtitle">—</p>
    <div id="study-resume-banner" class="hidden card" style="border-left:4px solid var(--accent);margin-bottom:12px;">
      <div style="font-weight:600;margin-bottom:4px;">Resume</div>
      <div class="meta" id="study-resume-meta">—</div>
      <button class="btn" id="btn-study-resume" style="margin-top:10px;margin-bottom:0;">Continue</button>
    </div>
    <div id="study-chapter-list"></div>
    <button class="btn secondary" id="btn-study-home" style="margin-top:16px;">← Home</button>
  </div>

  <!-- STUDY: chapter view -->
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

- [ ] **Step 3: Manual verification**

Open the page in a browser. The home screen should now show four content buttons (3 Chinese + "Options Pricing Theory"). The new button visually matches the others. Tapping it does nothing yet (no JS wired) — that's expected.

- [ ] **Step 4: Commit**

```
git add index.html
git commit -m "Add study section button and page divs"
```

---

### Task 5: Update show() and add STUDY constants

**Files:**
- Modify: `index.html` (JS section)

- [ ] **Step 1: Extend `show()` to include the two new page IDs**

Find the existing `show()` function (around line 312):
```js
function show(pageId) {
  document.querySelectorAll('#page-home,#page-quiz,#page-results,#page-review')
    .forEach(p => p.classList.add('hidden'));
  el(pageId).classList.remove('hidden');
  window.scrollTo(0, 0);
}
```

Replace with:
```js
function show(pageId) {
  document.querySelectorAll('#page-home,#page-quiz,#page-results,#page-review,#page-study-list,#page-study-chapter')
    .forEach(p => p.classList.add('hidden'));
  el(pageId).classList.remove('hidden');
  window.scrollTo(0, 0);
}
```

- [ ] **Step 2: Add study constants and state near the existing `LS_KEY` / `LS_QUIZ_KEY` declarations (around line 235)**

Immediately after:
```js
const LS_QUIZ_KEY = 'quiz_state_v1';
```

Insert:
```js
const LS_STUDY_KEY = 'study_state_v1';
let STUDY_INDEX = null;   // { title, subtitle, chapters: [{file, title}] } — loaded lazily on first study-section open
```

- [ ] **Step 3: Add localStorage helpers near other LS helpers**

Find the existing `loadHistory` / `saveHistory` block (around line 236-245). After `saveHistory()`, insert:

```js
function loadStudyState() {
  try {
    const s = JSON.parse(localStorage.getItem(LS_STUDY_KEY) || '{}');
    return { lastChapter: typeof s.lastChapter === 'number' ? s.lastChapter : null,
             visited: Array.isArray(s.visited) ? s.visited : [] };
  } catch { return { lastChapter: null, visited: [] }; }
}
function saveStudyState(state) {
  localStorage.setItem(LS_STUDY_KEY, JSON.stringify(state));
}
function markChapterVisited(idx) {
  const s = loadStudyState();
  s.lastChapter = idx;
  if (!s.visited.includes(idx)) s.visited.push(idx);
  saveStudyState(s);
}
```

- [ ] **Step 4: Manual verification in DevTools console**

Reload the page, then in console:
```js
loadStudyState()
```
Expected: `{ lastChapter: null, visited: [] }`.

Then:
```js
markChapterVisited(3); loadStudyState()
```
Expected: `{ lastChapter: 3, visited: [3] }`.

Clean up:
```js
localStorage.removeItem('study_state_v1')
```

- [ ] **Step 5: Commit**

```
git add index.html
git commit -m "Add study state helpers and update show()"
```

---

### Task 6: Implement the markdown :::-block preprocessor

The preprocessor runs on raw chapter markdown **before** `marked.parse`. It transforms three custom block types: `::: problem [tag]`, `::: solution`, and `::: where`.

**Files:**
- Modify: `index.html` (JS section)

- [ ] **Step 1: Add the preprocessor function**

Insert this function after the study localStorage helpers (right after `markChapterVisited`):

```js
// Preprocess study markdown: convert ::: problem [tag] / ::: solution / ::: where blocks
// into HTML wrappers. Runs BEFORE marked.parse so inner markdown is still processed normally.
// Block syntax:
//   ::: problem [Derivation]      <- opens a problem block, tag inside [...]
//   ...statement markdown...
//   ::: solution                  <- nested solution block
//   ...solution markdown...
//   :::                           <- closes solution
//   :::                           <- closes problem
//   ::: where                     <- standalone block; body is a markdown list
//   - $X$ — description
//   :::
function preprocessStudyMarkdown(src) {
  const lines = src.split(/\r?\n/);
  const out = [];
  const stack = [];        // top of stack = current open block tag
  let inFence = false;     // true while inside a ``` code fence

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Track fenced code blocks — ::: lines inside code fences are literal
    if (/^\s*```/.test(line)) {
      inFence = !inFence;
      out.push(line);
      continue;
    }
    if (inFence) {
      out.push(line);
      continue;
    }

    // Block opener: ::: problem [...]  or  ::: solution  or  ::: where
    const open = line.match(/^:::\s+(problem|solution|where)(?:\s*\[([^\]]*)\])?\s*$/);
    if (open) {
      const kind = open[1];
      const tag = open[2] || '';
      if (kind === 'problem') {
        const safeTag = escapeStudyAttr(tag);
        out.push(`<div class="problem">`);
        out.push(`<div class="ptag">${safeTag}</div>`);
        out.push(`<div class="problem-stmt">`);
        stack.push({ kind: 'problem', hasSolution: false });
      } else if (kind === 'solution') {
        const top = stack[stack.length - 1];
        if (!top || top.kind !== 'problem') {
          console.warn('::: solution outside of ::: problem at line', i + 1);
          out.push(line);
          continue;
        }
        top.hasSolution = true;
        out.push(`</div>`); // close problem-stmt
        out.push(`<button class="reveal-btn" type="button">Show solution</button>`);
        out.push(`<div class="solution">`);
        stack.push({ kind: 'solution' });
      } else if (kind === 'where') {
        out.push(`<div class="where">`);
        out.push(`<div class="where-label">where</div>`);
        stack.push({ kind: 'where' });
      }
      continue;
    }

    // Block closer: bare :::
    if (/^:::\s*$/.test(line)) {
      const top = stack.pop();
      if (!top) {
        console.warn('Unmatched ::: at line', i + 1);
        out.push(line);
        continue;
      }
      if (top.kind === 'problem') {
        // If no nested solution was opened, close problem-stmt too
        if (!top.hasSolution) {
          out.push(`</div>`); // close problem-stmt
        }
        out.push(`</div>`); // close .problem
      } else if (top.kind === 'solution') {
        out.push(`</div>`); // close .solution
      } else if (top.kind === 'where') {
        out.push(`</div>`); // close .where
      }
      continue;
    }

    out.push(line);
  }

  // Warn on unclosed blocks
  while (stack.length) {
    console.warn('Unclosed study block:', stack.pop().kind);
  }

  return out.join('\n');
}

function escapeStudyAttr(s) {
  return String(s).replace(/[&<>"']/g, c => ({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  }[c]));
}
```

- [ ] **Step 2: Manual smoke test in DevTools**

In DevTools console (after reloading the page):
```js
preprocessStudyMarkdown(`# Test\n\n::: problem [Derivation]\nProblem A.\n\n::: solution\nAnswer.\n:::\n:::\n`)
```

Expected output (whitespace-flexible):
```
# Test

<div class="problem">
<div class="ptag">Derivation</div>
<div class="problem-stmt">
Problem A.

</div>
<button class="reveal-btn" type="button">Show solution</button>
<div class="solution">
Answer.
</div>
</div>
```

Test the `where` block:
```js
preprocessStudyMarkdown(`$$x=y$$\n\n::: where\n- $x$ — input\n- $y$ — output\n:::\n`)
```

Expected output includes `<div class="where">`, `<div class="where-label">where</div>`, the bulleted list, and a closing `</div>`.

Test mismatched `:::`:
```js
preprocessStudyMarkdown(`:::\n`)
```
Expected: console warning "Unmatched ::: at line 1" and the line passes through literally.

Test that `:::` inside a code fence is ignored:
```js
preprocessStudyMarkdown('```\n:::\nfoo\n```\n')
```
Expected: output is identical to input (no transformation inside the fence).

- [ ] **Step 3: Commit**

```
git add index.html
git commit -m "Add study markdown preprocessor for problem/solution/where blocks"
```

---

### Task 7: Implement openStudySection, renderStudyList, openChapter

**Files:**
- Modify: `index.html` (JS section)

- [ ] **Step 1: Add chapter loading and rendering functions**

Insert after `escapeStudyAttr` (from Task 6):

```js
async function loadStudyIndex() {
  if (STUDY_INDEX) return STUDY_INDEX;
  const r = await fetch('study/index.json');
  if (!r.ok) throw new Error('Failed to load study/index.json: ' + r.status);
  STUDY_INDEX = await r.json();
  return STUDY_INDEX;
}

async function openStudySection() {
  try {
    await loadStudyIndex();
  } catch (e) {
    alert('Failed to load study section: ' + e.message);
    return;
  }
  renderStudyList();
  show('page-study-list');
}

function renderStudyList() {
  const idx = STUDY_INDEX;
  el('study-title').textContent = idx.title;
  el('study-subtitle').textContent = idx.subtitle;

  const state = loadStudyState();
  const banner = el('study-resume-banner');
  if (state.lastChapter !== null && state.lastChapter >= 0 && state.lastChapter < idx.chapters.length) {
    const ch = idx.chapters[state.lastChapter];
    el('study-resume-meta').textContent = `Chapter ${state.lastChapter + 1} — ${ch.title}`;
    banner.classList.remove('hidden');
  } else {
    banner.classList.add('hidden');
  }

  const list = el('study-chapter-list');
  list.innerHTML = '';
  idx.chapters.forEach((ch, i) => {
    const row = document.createElement('div');
    row.className = 'study-chapter-row';
    const visited = state.visited.includes(i);
    row.innerHTML =
      `<div style="display:flex;align-items:center;gap:12px;flex:1;min-width:0;">
         <span class="num">${i + 1}.</span>
         <span style="flex:1;min-width:0;">${escapeHtml(ch.title)}</span>
       </div>
       <span class="visited">${visited ? '✓' : ''}</span>`;
    row.onclick = () => openChapter(i);
    list.appendChild(row);
  });
}

async function openChapter(idx) {
  const indexData = STUDY_INDEX;
  if (!indexData || idx < 0 || idx >= indexData.chapters.length) return;
  const ch = indexData.chapters[idx];

  let raw;
  try {
    const r = await fetch('study/chapters/' + ch.file);
    if (!r.ok) throw new Error('HTTP ' + r.status);
    raw = await r.text();
  } catch (e) {
    el('study-chapter-content').innerHTML =
      `<p style="color:var(--bad)">Failed to load chapter: ${escapeHtml(e.message)}</p>`;
    show('page-study-chapter');
    return;
  }

  const container = el('study-chapter-content');

  // Graceful fallback if CDN libs failed to load
  if (typeof marked === 'undefined') {
    container.innerHTML = `<pre style="white-space:pre-wrap;font-family:inherit;font-size:14px">${escapeHtml(raw)}</pre>`;
  } else {
    const preprocessed = preprocessStudyMarkdown(raw);
    container.innerHTML = marked.parse(preprocessed);
    if (typeof renderMathInElement !== 'undefined') {
      renderMathInElement(container, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$',  right: '$',  display: false }
        ],
        throwOnError: false,
      });
    }
    // Wire reveal buttons
    container.querySelectorAll('.problem .reveal-btn').forEach(btn => {
      btn.onclick = () => {
        const problem = btn.closest('.problem');
        const revealed = problem.classList.toggle('revealed');
        btn.textContent = revealed ? 'Hide solution' : 'Show solution';
      };
    });
  }

  // Update state
  markChapterVisited(idx);

  // Update header / nav
  el('study-chapter-label').textContent = `Ch. ${idx + 1} — ${ch.title}`;
  el('study-chapter-counter').textContent = `${idx + 1} / ${indexData.chapters.length}`;
  el('study-progress-fill').style.width = `${((idx + 1) / indexData.chapters.length) * 100}%`;
  el('btn-study-prev').disabled = idx === 0;
  el('btn-study-prev').style.opacity = idx === 0 ? 0.4 : 1;
  el('btn-study-next').disabled = idx === indexData.chapters.length - 1;
  el('btn-study-next').style.opacity = idx === indexData.chapters.length - 1 ? 0.4 : 1;
  el('btn-study-prev').dataset.idx = idx - 1;
  el('btn-study-next').dataset.idx = idx + 1;

  show('page-study-chapter');
}
```

- [ ] **Step 2: Commit**

```
git add index.html
git commit -m "Add chapter loading and rendering for study section"
```

---

### Task 8: Wire all study buttons in boot()

**Files:**
- Modify: `index.html` (inside the existing `async function boot()` near line 501)

- [ ] **Step 1: Add button wiring**

Find the existing line in `boot()`:
```js
  el('btn-resume').onclick = () => { const s = loadSavedQuiz(); if (s) resumeQuiz(s); };
  el('btn-discard').onclick = () => { clearQuizState(); el('resume-banner').classList.add('hidden'); };
```

Immediately after those two lines, insert:
```js

  // Study section wiring
  el('btn-study').onclick = openStudySection;
  el('btn-study-home').onclick = () => { show('page-home'); renderHome(); };
  el('btn-study-back').onclick = () => { renderStudyList(); show('page-study-list'); };
  el('btn-study-resume').onclick = () => {
    const s = loadStudyState();
    if (s.lastChapter !== null) openChapter(s.lastChapter);
  };
  el('btn-study-prev').onclick = () => {
    const i = parseInt(el('btn-study-prev').dataset.idx, 10);
    if (!isNaN(i) && i >= 0) openChapter(i);
  };
  el('btn-study-next').onclick = () => {
    const i = parseInt(el('btn-study-next').dataset.idx, 10);
    if (!isNaN(i) && STUDY_INDEX && i < STUDY_INDEX.chapters.length) openChapter(i);
  };
```

- [ ] **Step 2: Manual end-to-end smoke test (scaffold-only)**

Start `python -m http.server 8000` and open in browser:

1. Tap "Options Pricing Theory" → chapter list shows with 12 stub chapters titled correctly.
2. Tap any chapter → chapter view shows the stub heading. `Previous` / `Next` enable correctly (Prev disabled on Ch.1, Next disabled on Ch.12).
3. Tap "Next" → next chapter loads. Progress bar updates. Counter shows "2 / 12".
4. Tap "← Chapters" → back to list. A `✓` appears next to chapters you visited.
5. Tap "← Home" → home screen.
6. Return to study section → resume banner shows "Chapter X — Title" matching last viewed.
7. Tap "Continue" → that chapter opens.
8. Existing quiz flow unaffected: start a 期貨 quiz, answer 2 questions, abort, return home.

- [ ] **Step 3: Commit**

```
git add index.html
git commit -m "Wire study navigation buttons"
```

---

### Task 9: Verify mobile rendering and graceful CDN-failure fallback

**Files:** (verification only — no code changes unless an issue is found)

- [ ] **Step 1: Mobile viewport check**

In Chrome DevTools, set device to "iPhone 12 Pro" (390 × 844). Open the study section. Verify:
- Chapter list rows are tappable (≥ 44 px tall) and don't horizontally overflow.
- Chapter view: progress bar, content area, and Prev/Next buttons fit within viewport width.
- No horizontal page scroll.

- [ ] **Step 2: CDN-failure fallback check**

In DevTools → Network tab, set throttling to "Offline" *after* the page has loaded (so the CDN-failure path triggers when opening a chapter without `marked` loaded). Easier alternative: temporarily comment out the three `<script defer src="...marked...">`/`...katex...` lines, reload, and open a chapter.

Expected: chapter content shows the raw markdown inside a `<pre>` with preserved newlines. Page does not error out; navigation still works.

Restore the CDN tags.

- [ ] **Step 3: Commit (no-op if no fixes needed)**

If you made any tweaks to fix mobile or fallback behavior:
```
git add index.html
git commit -m "<short imperative describing the fix>"
```

Otherwise skip this step.

---

### Task 10: Update CLAUDE.md with the new study section

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Append a new "Study section (Options Pricing Theory)" subsection at the end of `CLAUDE.md`**

Add this content (place it after the existing "Deployment" section):

```markdown

## Study section (Options Pricing Theory)

A 4th content area: in-browser self-study lessons on European options theory.
English UI scoped to this section; the existing 3 quiz buttons stay Chinese.

**Pipeline:** markdown chapter file → custom `:::` preprocessor → `marked.parse` → KaTeX
`renderMathInElement`. All loaded from CDN (`marked@12`, `katex@0.16.9`). Fallback:
if a CDN is unavailable, the chapter renders as raw markdown in a `<pre>` block.

**Content:** `study/chapters/01_preface.md` … `study/chapters/12_surface_models.md`,
indexed by `study/index.json`. Edit a chapter, refresh the page — no build step.

**Markdown conventions specific to study chapters:**

- `::: problem [Tag]` … `::: solution` … `:::` … `:::` — practice problem with
  click-to-reveal solution. `[Tag]` is a free-form label such as `Derivation`,
  `Conceptual`, `Computation`.
- `::: where` … `:::` — symbol-definition block. Body must be a markdown list of the
  form `- $sym$ — description`. **Every non-trivial formula in the chapters must be
  followed by a `where` block** that defines every symbol that appears in it (even
  symbols defined earlier — restate them so the reader never has to scroll back).
- All math uses standard `$inline$` and `$$display$$` delimiters.

**localStorage:**

| Key | Schema | Purpose |
|-----|--------|---------|
| `study_state_v1` | `{ lastChapter: number\|null, visited: number[] }` | Resume position + which chapters have been opened. |

**Pages:**

| Page | Behaviour |
|------|-----------|
| Study list | Title + subtitle from `study/index.json`. Optional Resume banner. Tappable rows for all 12 chapters; visited chapters show ✓. |
| Study chapter | Sticky progress bar. Chapter content rendered from markdown. Previous/Next buttons (disabled at ends). Back link to chapter list. |
```

- [ ] **Step 2: Commit**

```
git add CLAUDE.md
git commit -m "Document study section in CLAUDE.md"
```

---

## Phase 2 — Content authoring (Tasks 11-22)

Each task replaces one stub chapter file with its full graduate-level content.

**Authoring rules applied to every chapter:**

1. **Formula → where block.** Every non-trivial display formula is followed immediately by a `::: where ... :::` block listing every symbol that appears in it. Inline formulas like `$T=0.25$` are exempt.
2. **Theorem → proof.** Every theorem statement is followed by a proof (or "Proof sketch" if the full proof is non-instructive — Lévy characterization, etc.). Proofs appear in `<div class="proof">` blocks via the `:::`-style convention OR plain markdown headings — use h3 `### Proof`/`### Proof sketch` headings (the CSS theorem-box treatment is reserved for `<div>` literals if needed; markdown headings are the default).
3. **Practice block.** Every chapter ends with `## Practice` containing 2-3 problems: one conceptual, one derivation/proof, one computation. Each is a `::: problem [Tag]` block with a nested `::: solution`.
4. **Math typesetting.** Use Greek letters (`\mu`, `\sigma`), proper subscripts (`S_t`), `\mathbb{P}` / `\mathbb{Q}` / `\mathbb{R}` / `\mathbb{E}`, `\partial`, etc. Never substitute ASCII (no `S_t` written as `S(t)`).
5. **No back-references for symbols.** Restate symbols in every where block, even if defined earlier.

**After each chapter task: smoke-test the chapter in the browser.**

For every chapter authoring task, after writing the file, run this manual verification before committing:
- Start `python -m http.server 8000` if not running.
- Open the chapter from the chapter list.
- Verify all `$...$` and `$$...$$` formulas render with KaTeX (no stray `$` characters in the output).
- Verify every display formula is followed by a `where` box.
- Verify the Practice section shows 2-3 problems, each with a working "Show solution" button.
- Verify no console errors.

---

### Task 11: Author Chapter 1 — Preface and Notation

**Files:**
- Modify: `study/chapters/01_preface.md`

- [ ] **Step 1: Write the chapter**

Replace the stub content with a chapter containing:

1. **Heading and intro paragraph.** State the scope: "This document develops European-options pricing theory at the graduate level, from probability foundations through the implied-volatility surface. American and Bermudan options are not covered."
2. **Symbol table** as a markdown table. Two columns: Symbol / Meaning. Include at minimum: $S_t$, $K$, $T$, $t$, $r$, $q$, $\sigma$, $\mu$, $\Delta$, $\Gamma$, $\Theta$, $\nu$ (vega), $\rho$, $d_1$, $d_2$, $N(\cdot)$, $N'(\cdot)$, $\Phi$, $\varphi$, $W_t$, $\mathbb{P}$, $\mathbb{Q}$, $\mathcal{F}_t$, $\mathbb{E}$, $\mathbb{E}^{\mathbb{Q}}$, $C$, $P$, $V$. Use KaTeX inline math in the table.
3. **Conventions:**
   - Time in years; rates and volatilities annualized.
   - Continuous compounding throughout.
   - $W_t$ is a standard Brownian motion on $(\Omega, \mathcal{F}, \mathbb{P})$ with filtration $\{\mathcal{F}_t\}_{t \geq 0}$.
   - "Stock" means a non-dividend-paying stock unless `$q$` is mentioned.
   - All options are European unless explicitly noted otherwise.
4. **Reader prerequisites:** measure-theoretic probability at the level of Shreve Vol. 1; familiarity with multivariable calculus and ODEs.
5. **How to use this document:** "Each chapter ends with a `## Practice` section. Click *Show solution* after attempting the problem yourself."

No formulas heavy enough to need a `where` block in this chapter, so `where` blocks may be omitted here. No Practice section in Ch. 1 (it's a preface — make this an explicit exception).

- [ ] **Step 2: Smoke-test in browser** (per the rules above)

- [ ] **Step 3: Commit**

```
git add study/chapters/01_preface.md
git commit -m "Write Chapter 1 — Preface and Notation"
```

---

### Task 12: Author Chapter 2 — Probability Review

**Files:**
- Modify: `study/chapters/02_probability.md`

- [ ] **Step 1: Write the chapter**

Sections:

1. **Goals / Prerequisites** (one-liner each).
2. **Probability space.** Definition of $(\Omega, \mathcal{F}, \mathbb{P})$, $\sigma$-algebra, measurable function, random variable. Stated, no proofs.
3. **Filtration.** Definition of $\{\mathcal{F}_t\}_{t \geq 0}$, adapted process, predictable process. Stated.
4. **Expectation and conditional expectation.**
   - Definition of $\mathbb{E}[X]$ via Lebesgue integral (stated).
   - **Theorem (Tower property).** For sub-$\sigma$-algebras $\mathcal{G} \subseteq \mathcal{H}$: $\mathbb{E}[\mathbb{E}[X \mid \mathcal{H}] \mid \mathcal{G}] = \mathbb{E}[X \mid \mathcal{G}]$.
   - **Proof sketch.** Use the defining property of conditional expectation and uniqueness.
5. **Normal and lognormal distributions.**
   - Normal density $\varphi(x) = \tfrac{1}{\sqrt{2\pi}} e^{-x^2/2}$ — with `where` block.
   - Standard normal CDF $N(x) = \int_{-\infty}^x \varphi(u)\,du$ — with `where` block.
   - **Theorem.** If $X \sim \mathcal{N}(\mu, \sigma^2)$, then $\mathbb{E}[e^X] = e^{\mu + \sigma^2/2}$ (MGF at $t=1$) — with `where` block.
   - **Proof.** Complete the square inside the integral of $\int e^x \varphi_{\mu,\sigma^2}(x)\,dx$.
   - **Corollary.** If $Y = e^X$ with $X \sim \mathcal{N}(\mu, \sigma^2)$, then $\mathbb{E}[Y] = e^{\mu + \sigma^2/2}$ and $\operatorname{Var}(Y) = e^{2\mu + \sigma^2}(e^{\sigma^2} - 1)$ — with `where` block.
6. **Lognormal expected payoff.**
   - **Theorem.** If $S_T = S_0 \exp((m - \tfrac{1}{2}\sigma^2)T + \sigma\sqrt{T} Z)$ with $Z \sim \mathcal{N}(0,1)$, then $\mathbb{E}[(S_T - K)^+] = S_0 e^{mT} N(d_1) - K\, N(d_2)$ with $d_1 = \frac{\ln(S_0/K) + (m + \sigma^2/2)T}{\sigma\sqrt{T}}$ and $d_2 = d_1 - \sigma\sqrt{T}$. **Each formula gets a `where` block.**
   - **Proof.** Split the expectation as $\mathbb{E}[S_T \mathbf{1}_{S_T > K}] - K\,\mathbb{P}(S_T > K)$; evaluate each piece by change of variable and direct integration. Full proof written out.
   - **Remark.** This is the engine of the Black-Scholes formula. Foreshadow Ch. 8.

7. **Practice (3 problems):**
   - **Problem 2.1 [Conceptual].** Why does the tower property hold? Give the financial interpretation when $\mathcal{G}$ represents today's information and $\mathcal{H}$ represents tomorrow's.
   - **Problem 2.2 [Derivation].** Prove the MGF identity $\mathbb{E}[e^X] = e^{\mu + \sigma^2/2}$ for $X \sim \mathcal{N}(\mu, \sigma^2)$.
   - **Problem 2.3 [Computation].** $S_0 = 100$, $\sigma = 0.2$, $m = 0.05$, $T = 1$, $K = 100$. Compute $\mathbb{E}[(S_T - K)^+]$ to two decimal places using the closed form. Show $d_1$, $d_2$, $N(d_1)$, $N(d_2)$.

Each problem has a full worked solution in its `::: solution` block.

- [ ] **Step 2: Smoke-test in browser**

- [ ] **Step 3: Commit**

```
git add study/chapters/02_probability.md
git commit -m "Write Chapter 2 — Probability Review"
```

---

### Task 13: Author Chapter 3 — Stochastic Calculus

**Files:**
- Modify: `study/chapters/03_stochastic_calculus.md`

- [ ] **Step 1: Write the chapter**

Sections:

1. **Goals / Prerequisites.**
2. **Brownian motion (definition).** $W_0 = 0$, independent increments, $W_t - W_s \sim \mathcal{N}(0, t-s)$, continuous paths (a.s.).
3. **Lévy characterization (stated).** $X$ is BM iff $X$ is a continuous martingale with $\langle X \rangle_t = t$.
4. **Quadratic variation.** Definition: $[W,W]_t = \lim_{\|\Pi\| \to 0} \sum (W_{t_{i+1}} - W_{t_i})^2$ over partitions $\Pi$. With `where` block.
   - **Theorem.** $[W,W]_t = t$ a.s. (equivalently, the limit holds in $L^2$).
   - **Proof in $L^2$.** Compute $\mathbb{E}\big[\sum (\Delta W_i)^2 - t\big]^2$, use independence + normal moments, show variance vanishes as $\|\Pi\| \to 0$. Full proof written out.
5. **Itô integral (sketch).** Definition for simple integrands, isometry, extension. Statement of $\int_0^t H_s\,dW_s$ for predictable $H$ with $\mathbb{E}\int_0^t H_s^2\,ds < \infty$. State Itô isometry.
6. **Itô's lemma.**
   - **Theorem (Itô).** Let $X_t$ satisfy $dX_t = \mu_t\,dt + \sigma_t\,dW_t$ and let $f \in C^{1,2}(\mathbb{R}_+ \times \mathbb{R})$. Then $df(t, X_t) = \big(\partial_t f + \mu_t \partial_x f + \tfrac{1}{2}\sigma_t^2 \partial_{xx} f\big)\,dt + \sigma_t \partial_x f\,dW_t$. With `where` block listing every symbol.
   - **Proof (C^{1,2} case).** Taylor expand to second order, use quadratic variation $(dW)^2 = dt$, $(dt)^2 = 0$, $dt\,dW = 0$. Full proof with the rigorous interpretation as integrated form.
7. **Geometric Brownian motion.**
   - **Theorem.** The SDE $dS_t = \mu S_t\,dt + \sigma S_t\,dW_t$ with $S_0 > 0$ has the unique solution $S_t = S_0 \exp((\mu - \tfrac{1}{2}\sigma^2) t + \sigma W_t)$. With `where` block.
   - **Proof.** Apply Itô to $\ln S_t$; show $d \ln S_t = (\mu - \tfrac{1}{2}\sigma^2)\,dt + \sigma\,dW_t$. Integrate. Uniqueness from Lipschitz coefficients (cited).
8. **Girsanov's theorem (stated, with explicit RN derivative).**
   - **Theorem (Girsanov).** Let $\theta$ be adapted with $\mathbb{E}\big[\exp\big(\tfrac{1}{2} \int_0^T \theta_s^2\,ds\big)\big] < \infty$ (Novikov). Define $Z_T = \exp\big(-\int_0^T \theta_s\,dW_s - \tfrac{1}{2} \int_0^T \theta_s^2\,ds\big)$ and $d\mathbb{Q} / d\mathbb{P} = Z_T$. Then $\tilde W_t = W_t + \int_0^t \theta_s\,ds$ is a standard Brownian motion under $\mathbb{Q}$. With `where` block.
   - **Remark (no proof).** Proof requires the optional stopping theorem and the Lévy characterization; we cite Shreve Vol. 2 Ch. 5. This result will be used in Ch. 8.
9. **Practice (3 problems):**
   - **Problem 3.1 [Conceptual].** Why does $(dW)^2 = dt$ at the level of Itô calculus? What is the precise rigorous statement?
   - **Problem 3.2 [Derivation].** Use Itô's lemma to derive the SDE for $Y_t = W_t^2$. Verify that $W_t^2 - t$ is a martingale.
   - **Problem 3.3 [Computation].** Stock follows GBM with $S_0 = 100$, $\mu = 0.08$, $\sigma = 0.2$. Compute $\mathbb{E}[S_1]$ and $\operatorname{Var}(S_1)$.

Full solutions in each `::: solution`.

- [ ] **Step 2: Smoke-test in browser**

- [ ] **Step 3: Commit**

```
git add study/chapters/03_stochastic_calculus.md
git commit -m "Write Chapter 3 — Stochastic Calculus"
```

---

### Task 14: Author Chapter 4 — No-Arbitrage and Replication

**Files:**
- Modify: `study/chapters/04_no_arbitrage.md`

- [ ] **Step 1: Write the chapter**

Sections:

1. **Goals / Prerequisites.**
2. **Market model.** Riskless bond $B_t = e^{rt}$ with $B_0 = 1$. Stock $S_t$ following GBM under $\mathbb{P}$. Both adapted to $\{\mathcal{F}_t\}$.
3. **Portfolio and self-financing.**
   - **Definition.** A portfolio is a pair $(\phi_t, \psi_t)$ of adapted processes representing units of stock and bond. Value $V_t = \phi_t S_t + \psi_t B_t$.
   - **Definition (self-financing).** $dV_t = \phi_t\,dS_t + \psi_t\,dB_t$ (no exogenous cash flow). With `where` block.
4. **Arbitrage.**
   - **Definition.** An arbitrage is a self-financing portfolio with $V_0 = 0$, $V_T \geq 0$ a.s., and $\mathbb{P}(V_T > 0) > 0$.
5. **Risk-neutral measure.**
   - **Definition.** $\mathbb{Q}$ is an *equivalent martingale measure* if $\mathbb{Q} \sim \mathbb{P}$ and the discounted stock price $\tilde S_t = e^{-rt} S_t$ is a $\mathbb{Q}$-martingale.
6. **First Fundamental Theorem of Asset Pricing (stated).** No-arbitrage $\iff$ an equivalent martingale measure exists. Cite Delbaen-Schachermayer.
7. **Construction of $\mathbb{Q}$ for the BSM market.** Apply Girsanov with $\theta = (\mu - r)/\sigma$. Verify $\tilde S_t$ is a $\mathbb{Q}$-martingale by Itô.
   - **Theorem.** Under $\mathbb{Q}$, $S_t$ follows $dS_t = r S_t\,dt + \sigma S_t\,d\tilde W_t$. With `where` block.
   - **Proof.** Plug $W_t = \tilde W_t - \int_0^t \theta\,ds$ into the $\mathbb{P}$-SDE for $S_t$.
8. **Pricing principle.** Any attainable contingent claim $X$ paying $f(S_T)$ at $T$ has price $V_t = e^{-r(T-t)}\mathbb{E}^{\mathbb{Q}}[f(S_T) \mid \mathcal{F}_t]$. With `where` block. State as a consequence of no-arb + replication; full justification deferred to Ch. 8.
9. **Practice (3 problems):**
   - **Problem 4.1 [Conceptual].** Why must the equivalent martingale measure be equivalent to (not just absolutely continuous w.r.t.) $\mathbb{P}$? What goes wrong if it's only absolutely continuous?
   - **Problem 4.2 [Derivation].** Use Itô to show $d\tilde S_t = \sigma \tilde S_t\,d\tilde W_t$ under $\mathbb{Q}$ (no drift), confirming $\tilde S_t$ is a $\mathbb{Q}$-martingale.
   - **Problem 4.3 [Computation].** $r = 0.05$, $\mu = 0.10$, $\sigma = 0.20$. Compute the market price of risk $\theta$ and the Radon-Nikodym derivative $Z_T = d\mathbb{Q}/d\mathbb{P}$ for $T=1$, evaluated at $W_1 = 0$.

- [ ] **Step 2: Smoke-test in browser**

- [ ] **Step 3: Commit**

```
git add study/chapters/04_no_arbitrage.md
git commit -m "Write Chapter 4 — No-Arbitrage and Replication"
```

---

### Task 15: Author Chapter 5 — European Option Payoffs

**Files:**
- Modify: `study/chapters/05_european_payoffs.md`

- [ ] **Step 1: Write the chapter**

Sections:

1. **Goals / Prerequisites.**
2. **Payoff definitions.** Call: $f_C(S_T) = (S_T - K)^+$. Put: $f_P(S_T) = (K - S_T)^+$. With `where` blocks.
3. **Properties.** Monotonicity in $S$ (calls increasing, puts decreasing). Convexity in $S$ and in $K$ (justified geometrically).
4. **Arbitrage bounds.**
   - **Theorem.** $\max(S_0 - K e^{-rT}, 0) \leq C \leq S_0$ and $\max(K e^{-rT} - S_0, 0) \leq P \leq K e^{-rT}$. With `where` blocks.
   - **Proof.** Construct explicit dominating / dominated portfolios; invoke no-arbitrage.
5. **Put-call parity.**
   - **Theorem.** $C - P = S_0 - K e^{-rT}$ (no dividend) for European options. With `where` block.
   - **Proof.** Consider the portfolio long call + short put + $K e^{-rT}$ in bond. Its payoff at $T$ matches one share. By no-arbitrage, current values match.
   - **With continuous dividend yield $q$.** $C - P = S_0 e^{-qT} - K e^{-rT}$. With `where` block. Same proof with adjusted forward.
6. **Synthetic positions.** Briefly: synthetic stock = long call + short put + cash. Synthetic call, synthetic put. (Brief paragraph each.)
7. **Practice (3 problems):**
   - **Problem 5.1 [Conceptual].** Why is the lower bound $S_0 - K e^{-rT}$ for a call (rather than $S_0 - K$)?
   - **Problem 5.2 [Derivation].** Prove the put-call parity formula by explicit construction of the static replicating portfolio. Verify the payoff matches at $T$ and apply no-arbitrage at $t=0$.
   - **Problem 5.3 [Computation].** $S_0 = 50$, $K = 50$, $T = 0.5$, $r = 0.04$, $q = 0$. A call trades for $\$3.50$ in the market. What is the no-arbitrage put price?

- [ ] **Step 2: Smoke-test in browser**

- [ ] **Step 3: Commit**

```
git add study/chapters/05_european_payoffs.md
git commit -m "Write Chapter 5 — European Option Payoffs"
```

---

### Task 16: Author Chapter 6 — The Black-Scholes PDE

**This is the keystone chapter** — covers the user's example problem (derive BSM, boundary conditions).

**Files:**
- Modify: `study/chapters/06_bsm_pde.md`

- [ ] **Step 1: Write the chapter**

Sections:

1. **Goals / Prerequisites.**
2. **Setup.** Smooth value function $V(S,t) \in C^{2,1}$. Stock follows $dS_t = \mu S_t\,dt + \sigma S_t\,dW_t$ under $\mathbb{P}$. Bond $B_t = e^{rt}$. With `where` block.
3. **The Δ-hedged portfolio.** Form $\Pi_t = V(S_t, t) - \Delta_t S_t$ with $\Delta_t = \partial V / \partial S$ chosen to be self-financing (justified by setting $\psi_t$ to absorb).
4. **Theorem (Black-Scholes PDE).** The value function of any European option in this market satisfies
$$\frac{\partial V}{\partial t} + \tfrac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS \frac{\partial V}{\partial S} - rV = 0,$$
for $(S, t) \in (0, \infty) \times [0, T)$. With `where` block listing every symbol.
5. **Proof.** Apply Itô to $V(S_t, t)$:
   $$dV = \big(\partial_t V + \mu S \partial_S V + \tfrac{1}{2}\sigma^2 S^2 \partial_{SS} V\big)\,dt + \sigma S \partial_S V\,dW.$$
   With `where` block.

   So
   $$d\Pi = dV - \Delta\,dS = \big(\partial_t V + \tfrac{1}{2}\sigma^2 S^2 \partial_{SS} V\big)\,dt.$$
   With `where` block. The $dW$ term cancels by the choice $\Delta = \partial_S V$ — this is the riskless hedge.

   Since $\Pi$ is locally riskless, no-arbitrage forces $d\Pi = r\Pi\,dt = r(V - \Delta S)\,dt$. Equate the two expressions for $d\Pi$ and rearrange to obtain the PDE.

6. **Boundary conditions.** *Section title rendered prominently.*

   - **Terminal condition.** $V(S, T) = \text{payoff}(S)$. Specifically, $C(S,T) = (S-K)^+$ and $P(S,T) = (K-S)^+$. With `where` block.

   - **Lower boundary at $S = 0$.**
     - *Call:* $C(0, t) = 0$ for all $t \in [0, T]$. **Justification:** Under GBM the SDE has multiplicative coefficients $\mu S$ and $\sigma S$; if $S_t = 0$ at any $t$, the SDE forces $dS_u = 0$ for $u \geq t$, so $S$ is pinned at $0$ forever. The terminal payoff $(0 - K)^+ = 0$. Combined with discounting, $C(0,t) = 0$.
     - *Put:* $P(0, t) = K e^{-r(T-t)}$. **Justification:** Same pinning argument — $S_T = 0$ is certain given $S_t = 0$. The payoff $(K - 0)^+ = K$ is certain, discounted to time $t$ at the risk-free rate.

   - **Upper boundary as $S \to \infty$.**
     - *Call:* $C(S, t) \sim S - K e^{-r(T-t)}$ as $S \to \infty$. **Justification:** Deep-ITM the option is virtually certain to be exercised; its value approaches the forward contract $S_t - K e^{-r(T-t)}$ (the value of a long stock minus the present value of paying $K$ at $T$).
     - *Put:* $P(S, t) \to 0$ as $S \to \infty$. **Justification:** Probability of $S_T < K$ vanishes; the option becomes worthless.

7. **Uniqueness.** Cite Feynman-Kac (proved in Ch. 8): the PDE + terminal + boundary conditions has a unique smooth solution.

8. **Remark.** $\mu$ disappears from the PDE — the price doesn't depend on the real-world drift of the stock. This is the *most* counterintuitive consequence of replication.

9. **Practice (3 problems):**
   - **Problem 6.1 [Conceptual].** Explain in one paragraph why $\mu$ disappears from the BSM PDE while $\sigma$ does not. What is the financial intuition?
   - **Problem 6.2 [Derivation].** Derive the Black-Scholes PDE for a non-dividend-paying stock $S$ following $dS = \mu S\,dt + \sigma S\,dW$. State and justify the boundary conditions at $S = 0$ and as $S \to \infty$ for a European call. *(This is the example problem the user gave.)* Full worked solution.
   - **Problem 6.3 [Computation].** Modify the derivation to include a continuous dividend yield $q$. State the resulting PDE.

   For Problem 6.2, the `::: solution` reproduces the full derivation above in self-contained form (no "see above" references), plus both boundary conditions with their financial justifications.

   For Problem 6.3, solution shows: when $S$ pays dividend yield $q$, the self-financing condition becomes $d\Pi = dV - \Delta\,dS - q \Delta S\,dt$ (dividend cash absorbed). Repeating the derivation yields
   $$\frac{\partial V}{\partial t} + \tfrac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + (r-q)S \frac{\partial V}{\partial S} - rV = 0.$$
   With `where` block.

- [ ] **Step 2: Smoke-test in browser** — *extra-thorough on this chapter:* verify every formula's `where` block exists, all four boundary conditions are stated and justified, and Problem 6.2's solution is self-contained.

- [ ] **Step 3: Commit**

```
git add study/chapters/06_bsm_pde.md
git commit -m "Write Chapter 6 — The Black-Scholes PDE"
```

---

### Task 17: Author Chapter 7 — Solving the PDE

**Files:**
- Modify: `study/chapters/07_solving_pde.md`

- [ ] **Step 1: Write the chapter**

Sections:

1. **Goals / Prerequisites.**
2. **Strategy.** Reduce the BSM PDE to the heat equation by a sequence of changes of variable, solve the heat equation via Green's function, back-substitute.
3. **Change of variables.**
   - $x = \ln(S/K)$, $\tau = \tfrac{1}{2}\sigma^2 (T - t)$. With `where` block.
   - Substitution carries the BSM PDE into
$$\frac{\partial u}{\partial \tau} = \frac{\partial^2 u}{\partial x^2} + (k - 1)\frac{\partial u}{\partial x} - k u,$$
where $k = 2r/\sigma^2$ and $V = K u(x, \tau)$. With `where` block.
   - Eliminate the lower-order terms by writing $u(x, \tau) = e^{\alpha x + \beta \tau} v(x, \tau)$ with $\alpha = -\tfrac{1}{2}(k-1)$, $\beta = -\tfrac{1}{4}(k-1)^2 - k$. Show algebra.
   - Result: $v_\tau = v_{xx}$ on $\mathbb{R} \times (0, T \sigma^2/2)$ with initial condition derived from the call payoff.
4. **Heat-equation Green's function.**
   - **Lemma (heat kernel).** The fundamental solution of $v_\tau = v_{xx}$ is $G(x, \tau) = \tfrac{1}{\sqrt{4\pi \tau}} e^{-x^2/(4\tau)}$. With `where` block.
   - **Proof sketch.** Direct verification: compute $G_\tau$ and $G_{xx}$.
5. **Convolution with the call IC.** Compute $v(x, \tau) = \int_{-\infty}^\infty G(x - y, \tau) v(y, 0)\,dy$ where $v(y, 0)$ is the transformed call payoff $\max(e^y - 1, 0) \cdot K \cdot e^{-\alpha y}$. Carry out the integral by completing the square; result is two Gaussian integrals expressed via $N(\cdot)$.
6. **Back-substitution.** Substitute back $u = e^{\alpha x + \beta \tau} v$, $V = K u$, undo $x = \ln(S/K)$, $\tau = \tfrac{1}{2}\sigma^2(T-t)$. Arrive at:
$$C(S, t) = S\, N(d_1) - K e^{-r(T-t)}\, N(d_2),$$
with $d_1 = \frac{\ln(S/K) + (r + \tfrac{1}{2}\sigma^2)(T-t)}{\sigma\sqrt{T-t}}$, $d_2 = d_1 - \sigma\sqrt{T-t}$. With `where` block for the call formula AND for the $d_1, d_2$ definitions.
7. **Verification.** Show by direct differentiation that $C(S,t)$ satisfies the PDE and the boundary conditions from Ch. 6. (Sketch the verification.)
8. **Put formula.** Either repeat the heat-equation reduction with the put IC, or apply put-call parity from Ch. 5. Result: $P(S,t) = K e^{-r(T-t)} N(-d_2) - S\, N(-d_1)$. With `where` block.
9. **With continuous dividend yield $q$.** State the modified formula: $C = S e^{-q(T-t)} N(d_1) - K e^{-r(T-t)} N(d_2)$ with $d_1$ using $(r - q + \tfrac{1}{2}\sigma^2)$. With `where` block. Derivation outline (apply the same transformation to the modified PDE from Ch. 6 Problem 6.3).
10. **Practice (3 problems):**
    - **Problem 7.1 [Conceptual].** Why does the transformation $V = K u$ make the constant $K$ disappear from the heat-equation form?
    - **Problem 7.2 [Derivation].** Verify by direct differentiation that the closed-form call formula satisfies the BSM PDE.
    - **Problem 7.3 [Computation].** Price an ATM call: $S = K = 100$, $T = 0.25$, $r = 0.05$, $q = 0$, $\sigma = 0.20$. Compute $d_1$, $d_2$, $N(d_1)$, $N(d_2)$, and $C$ to two decimal places.

- [ ] **Step 2: Smoke-test in browser**

- [ ] **Step 3: Commit**

```
git add study/chapters/07_solving_pde.md
git commit -m "Write Chapter 7 — Solving the PDE"
```

---

### Task 18: Author Chapter 8 — Risk-Neutral Derivation

**Files:**
- Modify: `study/chapters/08_risk_neutral.md`

- [ ] **Step 1: Write the chapter**

Sections:

1. **Goals / Prerequisites.**
2. **Setup.** Recall from Ch. 4 that under $\mathbb{Q}$, $S_t$ follows $dS_t = r S_t\,dt + \sigma S_t\,d\tilde W_t$.
3. **Distribution of $S_T$ under $\mathbb{Q}$.** Apply Ch. 3 GBM result: $S_T = S_0 \exp\big((r - \tfrac{1}{2}\sigma^2)T + \sigma \tilde W_T\big)$, so $\ln S_T \sim \mathcal{N}\big(\ln S_0 + (r - \tfrac{1}{2}\sigma^2)T, \sigma^2 T\big)$ under $\mathbb{Q}$. With `where` block.
4. **Pricing by risk-neutral expectation.**
   - **Theorem.** $C_0 = e^{-rT}\, \mathbb{E}^{\mathbb{Q}}\big[(S_T - K)^+\big]$. With `where` block.
   - **Proof.** Pricing principle from Ch. 4 applied to the European call's terminal payoff.
5. **Closed-form evaluation.** Apply the lognormal expected-payoff theorem from Ch. 2 with $m = r$:
   - $C_0 = e^{-rT}\big[S_0 e^{rT} N(d_1) - K\, N(d_2)\big] = S_0\, N(d_1) - K e^{-rT}\, N(d_2)$.
   - Matches Ch. 7's PDE-derived formula.
   - With `where` block.
6. **Feynman-Kac theorem (stated).**
   - **Theorem.** Let $V(S, t) = e^{-r(T-t)}\, \mathbb{E}^{\mathbb{Q}}[g(S_T) \mid S_t = S]$ where $S_u$ follows $dS_u = r S_u\,du + \sigma S_u\,d\tilde W_u$. Then $V$ solves the BSM PDE with terminal $V(S, T) = g(S)$. With `where` block.
   - **Remark.** This is the formal bridge: PDE solutions are expectations of payoffs under $\mathbb{Q}$. Cite Shreve Vol. 2 §6.4 for proof.
7. **Practice (3 problems):**
   - **Problem 8.1 [Conceptual].** Risk-neutral pricing says the price equals the discounted expected payoff. But under $\mathbb{Q}$, the *expected return* on the stock is $r$ — investors don't actually earn $r$ in the real world. Reconcile these two statements.
   - **Problem 8.2 [Derivation].** Derive the Black-Scholes call price by evaluating $e^{-rT} \mathbb{E}^{\mathbb{Q}}[(S_T - K)^+]$ directly. Show the change of variable to standard normal and the two resulting Gaussian integrals.
   - **Problem 8.3 [Computation].** Numerically verify: with $S_0 = 100$, $K = 100$, $T = 0.25$, $r = 0.05$, $\sigma = 0.20$, simulate $10^4$ samples of $S_T$ under $\mathbb{Q}$, compute the average of $\max(S_T - K, 0)$, discount, and compare to the closed form. (Provide pseudocode in the solution.)

- [ ] **Step 2: Smoke-test in browser**

- [ ] **Step 3: Commit**

```
git add study/chapters/08_risk_neutral.md
git commit -m "Write Chapter 8 — Risk-Neutral Derivation"
```

---

### Task 19: Author Chapter 9 — The Greeks

**Files:**
- Modify: `study/chapters/09_greeks.md`

- [ ] **Step 1: Write the chapter**

Sections:

1. **Goals / Prerequisites.**
2. **Definition.** Each Greek is a partial derivative of the option price w.r.t. one input.
3. **Delta.**
   - $\Delta_C = \partial C / \partial S$, $\Delta_P = \partial P / \partial S$. With `where` block.
   - **Theorem.** $\Delta_C = N(d_1)$, $\Delta_P = N(d_1) - 1 = -N(-d_1)$ (no dividends). With `where` block.
   - **Proof.** Differentiate the closed form. A key identity: $S \varphi(d_1) = K e^{-r(T-t)} \varphi(d_2)$ (used to cancel cross terms). Prove this identity by direct computation from $d_2 = d_1 - \sigma\sqrt{T-t}$.
4. **Gamma.**
   - $\Gamma = \partial^2 C / \partial S^2 = \partial^2 P / \partial S^2$. With `where` block.
   - **Theorem.** $\Gamma = \varphi(d_1) / (S \sigma \sqrt{T-t})$. With `where` block.
   - **Proof.** Differentiate $\Delta_C = N(d_1)$ w.r.t. $S$. Use chain rule and $\partial d_1 / \partial S = 1/(S\sigma\sqrt{T-t})$.
5. **Theta.**
   - $\Theta = \partial V / \partial t$. With `where` block.
   - State formula for $\Theta_C$ (with no dividends).
   - **Sketch of derivation.** Differentiate closed form; use $\partial d_1 / \partial t = -\partial d_2 / \partial t - \sigma/(2\sqrt{T-t})$.
6. **Vega.**
   - $\nu = \partial V / \partial \sigma$. With `where` block.
   - **Theorem.** $\nu = S \varphi(d_1) \sqrt{T-t}$ (same for calls and puts). With `where` block.
   - **Proof.** Differentiate, use the $S\varphi(d_1) = K e^{-r(T-t)} \varphi(d_2)$ identity to cancel.
7. **Rho.** $\rho_C = K(T-t) e^{-r(T-t)} N(d_2)$, $\rho_P = -K(T-t) e^{-r(T-t)} N(-d_2)$. With `where` blocks.
8. **PDE consistency check.**
   - The BSM PDE can be rewritten as $\Theta + r S \Delta + \tfrac{1}{2}\sigma^2 S^2 \Gamma = r V$. With `where` block.
   - **Remark.** This identity is a sanity check on the closed form: plug in the Greek formulas and verify the PDE holds.
9. **Practice (3 problems):**
   - **Problem 9.1 [Conceptual].** Why is $\nu_C = \nu_P$ but $\Delta_C \neq \Delta_P$?
   - **Problem 9.2 [Derivation].** Prove the identity $S \varphi(d_1) = K e^{-r(T-t)} \varphi(d_2)$.
   - **Problem 9.3 [Computation].** ATM call: $S = K = 100$, $T = 0.25$, $r = 0.05$, $\sigma = 0.20$. Compute $\Delta$, $\Gamma$, $\Theta$, $\nu$, $\rho$.

- [ ] **Step 2: Smoke-test in browser**

- [ ] **Step 3: Commit**

```
git add study/chapters/09_greeks.md
git commit -m "Write Chapter 9 — The Greeks"
```

---

### Task 20: Author Chapter 10 — Implied Volatility

**Files:**
- Modify: `study/chapters/10_implied_vol.md`

- [ ] **Step 1: Write the chapter**

Sections:

1. **Goals / Prerequisites.**
2. **Definition.** Given a market call price $C_{\text{mkt}}$ at $(S, K, T, r)$, implied volatility $\sigma_{\text{IV}}$ is the unique $\sigma > 0$ solving $\text{BSM}_C(S, K, T, r, \sigma) = C_{\text{mkt}}$. With `where` block.
3. **Existence and uniqueness.**
   - **Theorem.** For any $C_{\text{mkt}} \in (\max(S - K e^{-rT}, 0), S)$ there exists a unique $\sigma_{\text{IV}} > 0$ solving the equation.
   - **Proof.** Existence via continuity and the intermediate value theorem. Uniqueness via $\nu_C = S \varphi(d_1) \sqrt{T} > 0$ (strict monotonicity). Cite Ch. 9 for the vega formula.
4. **Newton-Raphson algorithm.**
   - Iteration: $\sigma_{n+1} = \sigma_n - (\text{BSM}_C(\sigma_n) - C_{\text{mkt}}) / \nu(\sigma_n)$. With `where` block.
   - **Convergence remark.** Quadratic convergence in the neighborhood of the root; vega is well-behaved away from extremes; in practice converges in $\leq 5$ iterations.
5. **Implied volatility ≠ realized volatility.** Brief contrast.
6. **Practice (3 problems):**
   - **Problem 10.1 [Conceptual].** Why is the function $\sigma \mapsto \text{BSM}_C(\sigma)$ strictly monotonic? What would happen for $\sigma \to 0$? For $\sigma \to \infty$?
   - **Problem 10.2 [Derivation].** Derive the Newton-Raphson update formula starting from the first-order Taylor expansion of $\text{BSM}_C(\sigma)$ around the current iterate.
   - **Problem 10.3 [Computation].** Market call price $\$4.61$ for $S = K = 100$, $T = 0.25$, $r = 0.05$. Starting from $\sigma_0 = 0.30$, perform two Newton iterations. Report $\sigma_1$, $\sigma_2$.

- [ ] **Step 2: Smoke-test in browser**

- [ ] **Step 3: Commit**

```
git add study/chapters/10_implied_vol.md
git commit -m "Write Chapter 10 — Implied Volatility"
```

---

### Task 21: Author Chapter 11 — The IV Surface

**Files:**
- Modify: `study/chapters/11_iv_surface.md`

- [ ] **Step 1: Write the chapter**

Sections:

1. **Goals / Prerequisites.**
2. **The surface.** $\sigma_{\text{IV}}(K, T)$ — a function of strike and expiry. Not constant in practice, contrary to the BSM assumption.
3. **Smile and skew.** Definitions; equity-skew direction (OTM puts > OTM calls); FX smile.
4. **Term structure.** Contango vs. backwardation.
5. **No-arbitrage constraints on the surface.**
   - **Butterfly constraint.** $\partial^2 C / \partial K^2 \geq 0$ for all $K$.
   - **Proof.** Risk-neutral density $\rho_{S_T}(K) = e^{rT} \partial^2 C / \partial K^2$ (Breeden-Litzenberger). Density must be non-negative.
   - **Theorem (Breeden-Litzenberger).** $\rho_{S_T}(K) = e^{rT} \partial^2 C(S_0, K, T) / \partial K^2$. With `where` block.
   - **Proof.** Differentiate $C = e^{-rT} \int_K^\infty (s - K) \rho(s)\,ds$ twice w.r.t. $K$ using Leibniz.
   - **Calendar constraint.** Total implied variance $w(K, T) = \sigma_{\text{IV}}(K, T)^2 T$ is non-decreasing in $T$ for each fixed $K$ (in moneyness $\ln(K/F)$). With `where` block. Proof outline: arbitrage via calendar spreads.
6. **Sticky strike vs. sticky delta.** Definitions, financial interpretation, which holds when. Sticky-delta adjustment to delta: $\Delta_{\text{adj}} = \Delta_{\text{BSM}} + \nu \cdot \partial \sigma_{\text{IV}} / \partial S$. With `where` block.
7. **Practice (3 problems):**
   - **Problem 11.1 [Conceptual].** Why does equity skew have OTM puts > OTM calls? Give two distinct explanations (e.g., crash demand; leverage effect).
   - **Problem 11.2 [Derivation].** Prove Breeden-Litzenberger.
   - **Problem 11.3 [Computation].** Given three call prices $C(K_1)$, $C(K_2)$, $C(K_3)$ at equally spaced strikes $K_1 < K_2 < K_3$, write down a finite-difference test for the butterfly constraint. Apply it to the made-up prices $C(95) = 7.2$, $C(100) = 4.6$, $C(105) = 2.5$.

- [ ] **Step 2: Smoke-test in browser**

- [ ] **Step 3: Commit**

```
git add study/chapters/11_iv_surface.md
git commit -m "Write Chapter 11 — The IV Surface"
```

---

### Task 22: Author Chapter 12 — Surface Models (stated only)

**Files:**
- Modify: `study/chapters/12_surface_models.md`

- [ ] **Step 1: Write the chapter**

Sections (each model: one paragraph of motivation + SDE statement + parameter table; no derivations):

1. **Goals / Prerequisites.**
2. **Dupire local volatility.**
   - SDE under $\mathbb{Q}$: $dS_t = r S_t\,dt + \sigma_{\text{loc}}(S_t, t) S_t\,d\tilde W_t$. With `where` block.
   - One-paragraph: fits the entire vanilla surface exactly; deterministic vol function; bad forward smile dynamics.
3. **Heston (stochastic vol).**
   - $dS_t = r S_t\,dt + \sqrt{v_t} S_t\,dW_t^1$, $dv_t = \kappa(\theta - v_t)\,dt + \xi \sqrt{v_t}\,dW_t^2$, with $\langle dW^1, dW^2\rangle = \rho\,dt$. With `where` block.
   - Parameter table: $v_0, \kappa, \theta, \xi, \rho$ with meanings.
4. **SABR.**
   - $dF_t = \alpha_t F_t^\beta\,dW_t^1$, $d\alpha_t = \nu \alpha_t\,dW_t^2$, $\langle dW^1, dW^2 \rangle = \rho\,dt$. With `where` block.
   - Parameter table: $\alpha, \beta, \rho, \nu$.
5. **SVI parameterization.**
   - $w(k) = a + b \big[\rho (k - m) + \sqrt{(k - m)^2 + \sigma^2}\big]$ where $w = \sigma_{\text{IV}}^2 T$, $k = \ln(K/F)$. With `where` block.
   - Parameter table.
6. **Practice (2 problems — exception, fewer since this is survey-only):**
   - **Problem 12.1 [Conceptual].** Why does local volatility produce poor forward dynamics, even though it fits today's surface exactly?
   - **Problem 12.2 [Computation].** For SVI with $a = 0.04$, $b = 0.4$, $\rho = -0.5$, $m = 0$, $\sigma = 0.1$, compute the total implied variance and implied volatility at $k = -0.1$, $0$, $0.1$.

- [ ] **Step 2: Smoke-test in browser**

- [ ] **Step 3: Commit**

```
git add study/chapters/12_surface_models.md
git commit -m "Write Chapter 12 — Surface Models"
```

---

## Phase 3 — Cleanup and verification (Tasks 23-25)

---

### Task 23: End-to-end verification

**Files:** (no code changes unless an issue is found)

- [ ] **Step 1: Start local server**

```
python -m http.server 8000
```

- [ ] **Step 2: Run the complete verification checklist**

For each item, confirm the result before moving on:

1. **Home screen** — 4 content buttons visible (3 Chinese + Options Pricing Theory). Quiz stats unchanged.
2. **Open study section** — chapter list shows 12 chapters with correct titles. No console errors.
3. **Open every chapter (1-12)** — for each:
   - Content renders (no `*(Content to be authored...)*` stub text left anywhere).
   - All KaTeX math renders (no stray `$` characters in body, no red KaTeX error messages).
   - Every display formula has an immediately following `where` block.
   - Theorem statements followed by proofs (or "Proof sketch").
   - Practice section has 2-3 problems (Ch. 1 may be exempt; Ch. 12 may have 2).
   - Every problem's "Show solution" button reveals the solution; "Hide solution" hides it again.
   - No console errors.
4. **Navigation** — Previous on Ch. 1 disabled; Next on Ch. 12 disabled; otherwise both work. Back to chapter list works. ✓ marks appear next to visited chapters. Resume banner appears and Continue jumps to last-read chapter.
5. **Mobile viewport** (Chrome DevTools "iPhone 12 Pro" 390 × 844) — chapter list rows tappable. Wide formulas scroll horizontally inside their `.katex-display` box only; page itself does not horizontal-scroll. Reveal buttons tappable.
6. **Dark mode** (Chrome DevTools → Rendering → emulate `prefers-color-scheme: dark`) — study pages remain readable; theorem/where boxes still have visible contrast.
7. **CDN-fail fallback** — temporarily comment out the three CDN `<script>` tags, reload, open a chapter: content shows as raw markdown inside `<pre>`, no crash. Restore.
8. **Quiz smoke test** — pick 期貨商業務員, start a quiz, answer 3 questions, tap 儲存並回到首頁, resume from home, abort. All behaves as before. No changes to existing flow.
9. **localStorage isolation** — open DevTools → Application → localStorage. Confirm new key `study_state_v1` exists; existing `quiz_history_v1` and `quiz_state_v1` keys are unchanged.
10. **`git status`** — only expected files added/modified: `index.html`, `CLAUDE.md`, `README.md`, `docs/superpowers/specs/`, `docs/superpowers/plans/`, `study/`. No stray files.

- [ ] **Step 3: Fix any failures found**

If a check fails, fix it inline. Commit each fix with a short imperative message describing what was fixed.

- [ ] **Step 4: Commit (no-op if no fixes needed)**

---

### Task 24: Update README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add a feature line for the study section**

Locate the README's feature list (or top-of-document description). Append (or insert appropriately):

```markdown
- **Options Pricing Theory study section** — in-browser, KaTeX-rendered graduate-level European-options lessons with click-to-reveal practice problems. Self-contained; no build step.
```

If the README has no feature list, add a short paragraph in the appropriate location instead. Keep changes minimal.

- [ ] **Step 2: Commit**

```
git add README.md
git commit -m "Mention Options Pricing study section in README"
```

---

### Task 25: Delete the old Options_Pricing_Theory folder

**This is a destructive, irreversible action — perform only after Task 23 verification passes.**

**Files (external):**
- Delete: `C:\Users\User\Desktop\Options_Pricing_Theory\` (the entire folder)

- [ ] **Step 1: Confirm prerequisites**

- Task 23 verification completed without unresolved failures.
- All previous commits pushed or at least present locally — confirm with `git log --oneline -25`.
- The certificate_practice site renders all 12 chapters correctly in the browser.

- [ ] **Step 2: Delete the folder**

Run from any directory (not from inside the folder being deleted):

```powershell
Remove-Item -Recurse -Force "C:\Users\User\Desktop\Options_Pricing_Theory"
```

- [ ] **Step 3: Verify deletion**

```powershell
Test-Path "C:\Users\User\Desktop\Options_Pricing_Theory"
```

Expected: `False`.

- [ ] **Step 4: (Optional) Push to GitHub**

If the user wants to deploy:

```
git push origin main
```

GitHub Pages will pick up the changes automatically. No commit needed for the folder deletion — the deleted folder was outside the repository.

---

## Self-review notes (after writing this plan)

**Spec coverage check:**

- ✅ 4th home button: Task 4.
- ✅ Two new pages: Task 4 (HTML), Tasks 7-8 (JS).
- ✅ markdown → marked → KaTeX pipeline: Tasks 2, 6, 7.
- ✅ Click-to-reveal solutions: Task 6 (preprocessor), Task 7 (button wiring).
- ✅ `::: where` symbol blocks: Task 6 (preprocessor), Task 3 (CSS), enforced in every chapter task (11-22).
- ✅ `study_state_v1` localStorage: Task 5.
- ✅ Resume banner: Task 4 (HTML), Task 7 (renderStudyList), Task 8 (button wiring).
- ✅ CSS scoped to `.study`: Task 3.
- ✅ CDN fallback: Task 7 (graceful `<pre>` fallback), Task 9 (verification).
- ✅ 12 chapters with the right substance: Tasks 11-22, each chapter outline matches the spec's chapter table.
- ✅ Boundary conditions in Ch. 6: Task 16, explicit section + Problem 6.2.
- ✅ Both BSM derivations (PDE + risk-neutral): Tasks 16-17 (PDE → heat eq.) and Task 18 (Girsanov → expectation).
- ✅ CLAUDE.md update: Task 10.
- ✅ README update: Task 24.
- ✅ Delete old folder: Task 25.

**Placeholder scan:** No TBDs. All code blocks are complete and executable. Each chapter authoring task specifies sections + theorems + practice problems concretely. Where a task says "compute" or "provide pseudocode in the solution," the implementer has enough information to write the content.

**Type / signature consistency:** `loadStudyState` returns `{lastChapter, visited}` — used consistently. `STUDY_INDEX` shape stated in Task 5 and matches `study/index.json` shape from Task 1. CSS class names (`.study`, `.problem`, `.solution`, `.where`, `.thm`, `.defn`, `.proof`, `.remark`, `.reveal-btn`, `.ptag`, `.study-chapter-row`) used consistently across Tasks 3, 4, 6, 7. Button IDs (`btn-study`, `btn-study-home`, `btn-study-back`, `btn-study-resume`, `btn-study-prev`, `btn-study-next`) used consistently in Tasks 4 and 8.
