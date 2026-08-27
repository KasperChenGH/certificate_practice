# CLAUDE.md — certificate_practice

## Project

Mobile-friendly quiz webapp for Taiwan financial certification exams, hosted on GitHub Pages.
Live URL: `https://certifications.courses/`
(custom domain, set by the root `CNAME` file; the old
`kasperchengh.github.io/certificate_practice/` address redirects to it)

## Before searching the web for questions

**Read `docs/SEARCH_LOG.md` first.** It records every source already looked at — the ones
that worked, the dead ends, and the exams that are blocked for reasons no further search
will fix. Append to it after any search, including the ones that find nothing.

## Scope

Two pages, static data, no backend:

- `index.html` — the landing page at the domain root. **Generated**: edit
  `design/Main.dc.html` and run `node design/build-site.mjs`; never edit `index.html`
  directly, a rebuild overwrites it.
- `app.html` — the quiz app itself (hand-maintained). Mobile-first, with desktop
  layouts behind `@media (min-width: 1024px)`.
- `questions.json` + `blueprints.json` — fetched relatively, so both work at any root.

**Deep link:** `app.html?topic=<key>` starts that paper immediately. The landing page's
exam directory links every live row this way. 證券商業務員 and 證券交易相關法規與實務乙科
both point at `securities_rep`: they are different certificates — 100 題 over two subjects
versus 50 題 over one of them — that share the one subject this bank holds.

The deep link deliberately does **not** start a paper when one is
already in progress: that would discard the saved answers, so it lands on the home page
with the resume banner instead. Covered by `design/linktest.mjs`.

Run locally: `python -m http.server 8000` then open `http://localhost:8000`.

## Question banks

Bank keys, display names and sizes are **not listed here** — they went stale every time
a paper was added. `questions.json` is the list; `app.html`'s `TOPIC_NAMES` is the naming;
`blueprints.json` carries each bank's paper composition and its `coverage` block
(pool / draw / ratio). To see the current state:

```bash
python -c "import json;d=json.load(open('questions.json',encoding='utf-8'));print({k:len(v) for k,v in d.items()})"
```

A bank may be retired by dropping it from `build.py`'s `main()`; keep its builder and
source PDFs so it can be restored, and see `check_explanation_coverage` below for the
trap that lies in wait when it is.

### Exam blueprints

A practice paper mirrors the real exam's subject split instead of drawing at random.
`sources/exam_blueprints.json` is the one home for that; `build.py` validates it against the
built banks and emits `blueprints.json` for the app.


`build.py` **fails** if a blueprint names a subject no question carries, asks for more
questions than exist, or names a bank that is not built — a typo would otherwise yield a
silently short or empty section. Covered by `scripts/test_blueprints.py`.

Subjects come from the `subject` field, which `tag_subjects()` copies out of the middle of
`origin` at build time, so the origin format is parsed in exactly one place.

Scoring is **per subject**. `pass_mark` (70) is applied per section where the exam defines
one: the Taiwan exams fail a candidate who fails one subject regardless of the total.
`cfa_fra` deliberately omits `pass_mark` — CFA Institute does not publish a minimum passing
score, let alone a per-topic one — so its sections show scores with no pass/fail verdict. The results page and each history
record carry the per-subject split. A bank with no blueprint falls back to a random
`QUIZ_SIZE` draw, and anything keyed off quiz length reads `currentSize()`, never the
`QUIZ_SIZE` constant.

`overallStats()` counts only question IDs present in the loaded banks. History for a retired
bank stays in localStorage and would otherwise inflate the totals forever.

The three Taiwan banks are 4-choice (A–D) and Traditional Chinese. `cfa_fra` follows the
CFA exam's own 3-choice (A–C) format and is in English. `optionLetters(q)` in `index.html`
derives the letters from the non-empty options, so both formats render from one code path.

## questions.json schema

```json
{
  "futures": [
    {
      "id": "futures-1",
      "topic": "futures",
      "stem": "...",
      "options": { "A": "...", "B": "...", "C": "...", "D": "..." },
      "answer": "A",
      "origin": "112年第1次 Q1",
      "explanations": {
        "A": "正確。...",
        "B": "錯誤。...",
        "C": "錯誤。...",
        "D": "錯誤。..."
      }
    }
  ]
}
```

`explanations` is LLM-generated (Traditional Chinese, per-option) and is **not
reproducible from the source PDFs**. Coverage is not total — questions from newly added
papers carry the official answer and no explanation until one is written. The per-bank
count lives in `sources/explanation_coverage.json`, which is also the guard's baseline.

## Data sources

Two of the banks come from a complete official 題庫; every other bank is built from past
papers, so its size is (sittings collected) × (questions per paper).

- **Where each bank's papers come from, and why some exams are absent**:
  `sources/papers/README.md`
- **Which URLs have already been searched, and which were dead ends**:
  `docs/SEARCH_LOG.md`

證基會 publishes only the two most recent sittings, so papers must be pulled each quarter
or recovered from a web archive afterwards. Answer blocks are matched to subjects **by
printed label with coordinates**, never by position, and the parser raises rather than
guess — an answer PDF covers every subject in that session's exam.

Rebuild: `python scripts/build.py` (requires `pip install pymupdf`).


`build.py` carries `explanations` over from the existing `questions.json`, so a rebuild does
not drop the LLM-generated explanations (they are not reproducible from the source PDFs).
Carry-over matches on question **id** first (requiring the answer key to agree), falling back
to a stem+options fingerprint — so a stem override does not orphan its explanations.

### Stem overrides

A printed paper presents questions in order, so 同上題 / 承上題 works there. This app draws a
random subset and shuffles it, so such a stem is unanswerable. `sources/stem_overrides.json`
holds self-contained rewrites, applied by `build.py` after dedup.

**Editing a stem directly in `questions.json` does not survive a rebuild** — stems come
straight from the PDF parse, unlike explanations. Use the override file.

Each entry records the original text and the build fails if the parse no longer matches it.
`build.py` also **fails when any stem references another question and has no override**, which
is what stops this class of bug returning when new papers are added.

## Key files

```
app.html            The quiz app — quiz logic, review, history, localStorage, all CSS/JS
index.html          Landing page. GENERATED from design/Main.dc.html
questions.json      Combined question bank (UTF-8, includes explanations)
blueprints.json     Per-bank paper composition + coverage ratios, emitted by build.py
docs/SEARCH_LOG.md  Every source already searched — read before searching again
scripts/
  build.py          Orchestrator — rebuilds questions.json from source PDFs
  parse_bank.py     Parses SFI 金融市場常識 / 職業道德 bank PDFs
  parse_sec.py      Parses 證券高業 試題 + 答案 PDFs (3 papers per session)
  parse_paper.py    Parses one subject out of a paper; picks the answer block by label
  build_cfa.py      Validates + assembles the hand-authored CFA bank
  test_*.py         Build guards: blueprints, explanation coverage, stem overrides
sources/            Source PDFs + cfa_fra.json + papers/ (see papers/README.md)
design/             Landing-page source, site build, and the browser test suites
_expl_work/         Explanation generation artifacts
```

## App pages

| Page       | Behaviour |
|-----------|-----------|
| Home      | Stats card (total attempts / accuracy / wrong-pool size). Resume banner shown if a saved quiz exists. Pick topic → start 100-question quiz. |
| Quiz      | Tap option → immediate locked feedback. Correct option goes green, wrong selection goes red. 解析 block shows per-option explanation for all 4 choices. Navigate with 上一題 / 下一題. Last question becomes 交卷. Bottom has 儲存並回到首頁 (saves progress, returns home) and 放棄並回首頁 (clears progress after confirm). |
| Results   | Score, topic name, wrong count. 檢視本次錯題 opens this exam's wrong questions directly; 回首頁 returns. |
| Review    | 常錯題複習 — lists questions wrong ≥ 50% of last 10 attempts (min 3 attempts). Aggregate view across attempts, so no single "your answer". |
| History   | 測驗紀錄 — one row per submitted exam, newest first: topic, timestamp, score pill (green ≥ 70%, red below), wrong count. Above the list, a per-topic summary of attempts / best / average / most recent. 清除測驗紀錄 clears only this log. |
| History detail | The wrong questions from one exam: every option with ✓ on the correct answer and ✗ on what was picked, 你的答案 / 未作答, and the 解析 block where the question has one. |

## localStorage

| Key | Schema | Purpose |
|-----|--------|---------|
| `quiz_history_v1` | `{ [questionId]: { attempts: [true\|false, ...] } }` (last 10 kept) | Per-question attempt history; drives stats and often-wrong detection. Entries for retired banks are ignored, not deleted. Cleared via 清除作答紀錄. |
| `quiz_state_v1` | `{ topic, questionIds[], answers[], idx }` | In-progress quiz snapshot. Saved after every answer and navigation. Cleared on submit or 放棄. |
| `quiz_results_v1` | `[{ t: topic, ts: epoch ms, n: asked, c: correct, w: [[questionId, picked\|null], ...] }]` newest first, capped at `MAX_RESULTS` (50) | One record per **submitted** exam — an abandoned quiz is never recorded. Only wrong answers are stored; question text is looked up from `DATA` at render time, so a record outlives an edit to the bank. `null` in `w` means the question was left blank. Cleared via 清除測驗紀錄, independently of `quiz_history_v1`. |

Writes to `quiz_results_v1` retry after dropping the oldest records, so a full quota
degrades to a shorter history instead of throwing. A record whose bank has since been
retired still renders: `topicLabel()` falls back to `RETIRED_TOPIC_NAMES`, and questions
that no longer resolve are counted in a "已不在目前題庫中" note rather than skipped silently.

## Quiz resume flow

State is auto-saved after every answer and navigation tap. To explicitly pause: tap **儲存並回到首頁** — goes home without touching state. On next visit a banner shows "繼續上次測驗 — [topic] 已作答 X / 100 題" with **繼續作答** and **捨棄** buttons.

## Constants (top of index.html `<script>`)

```js
const QUIZ_SIZE = 100;
const RECENT_WINDOW = 10;   // sliding window for often-wrong detection
const MIN_ATTEMPTS = 3;     // min attempts before a question can be "often wrong"
const WRONG_RATIO = 0.5;    // threshold: ≥50% wrong → often wrong
```

## Design sources (`design/`)

The site's visual design lives here as Design Component artboards, published as a canvas
at claude.ai. Working files, all committed:

| File | Role |
|---|---|
| `Main.dc.html` | The landing page — **the source `index.html` is built from** |
| `build-site.mjs` | `Main.dc.html` → `../index.html`, with head, meta and reserved ad slots |
| `build-screens.mjs` | Generates the six phone app-screen artboards |
| `build-desktop.mjs` | Generates the six desktop app-screen artboards |
| `canvas.json` | Artboard layout, two pages, annotations |
| `preview.mjs` | Unwraps a `.dc.html` into a standalone page for screenshotting |
| `shoot.mjs` | Full-page screenshot at an exact viewport, over CDP |
| `flowtest.mjs` | Drives the real app end to end and asserts + captures each screen |

Screens are generated rather than hand-written because artboards share nothing at
runtime — six hand-maintained copies of the shell CSS would drift within a day.

**`shoot.mjs` exists because `chrome --headless --screenshot` lies.** It enforces a
minimum window width (485px), then crops the image to whatever you asked for, so a
"390px" shot silently shows a wider layout with the right-hand side sliced off — which
reads exactly like a responsive bug that is not there. It also disables the cache and
pins `prefers-color-scheme`, both of which produced wrong readings before they were set.

## Ad slots

Every page carries one reserved slot (the landing has two), marked in the markup with a
comment where the AdSense `<ins>` unit goes. No publisher id is in the repo.

Two rules the layout enforces, worth keeping:

1. **Fixed height on every slot.** A late-loading ad must not shift the page — that is
   the CLS score, which affects both ranking and ad revenue.
2. **Never adjacent to the thing the screen exists for.** On 作答中 especially: people
   tap fast through 100 questions, and an ad beside the options is the accidental-click
   pattern that gets AdSense accounts limited. Its slot sits at the foot of the desktop
   side panel and at the very bottom on phones, below every control.

## Auditing the banks

Two read-only scripts. Neither changes data nor gates the build.

```bash
python scripts/audit_conflicts.py [--all]      # cross-session contradictions
python scripts/audit_staleness.py [--limit N]  # age profile + staleness risk list
```

`audit_conflicts.py` finds the same question asked in two sessions with two different
correct answers — either a rule changed or one is mis-keyed. Two questions count as the
same only when **both** stem and option set are >= 85% similar; stem alone is not enough,
since a generic stem like 下列敘述何者有誤? recurs with entirely different options. Answers
compare on the keyed option's **text**, never its letter (sessions shuffle option order),
with 臺/台 and a leading 僅 before an enumeration normalised away — those variants produced
most of the initial false positives.

`audit_staleness.py` covers what conflicts cannot: a rule that moved *after* a question's
last appearance leaves no internal trace. It reports the age profile, references to
superseded benchmarks (LIBOR, 歐洲美元), and pre-113年 questions whose answer is a hard
number, split into re-confirmed (asked again later, same answer) and unconfirmed.

Last run: **0 real contradictions** across 1,185 Taiwan-bank questions — 58 near-duplicate
pairs, 55 agreeing, and the 3 flagged are distinct questions that merely read alike
(買權/賣權, 投信/投顧, 多頭/空頭).

## Work completed

1. Parsed all source PDFs into structured JSONL using PyMuPDF + custom row-clustering parsers.
2. Deduplicated questions via SHA-1 fingerprint on normalized stem text.
3. Built initial webapp with 3-topic quiz, localStorage history, "often wrong" review page.
4. UI refinements: abort button spacing, inline per-question correct-answer feedback, score-only results page.
5. LLM-generated per-option explanations (Traditional Chinese), merged into questions.json.
6. Updated quiz UI to display 解析 explanation block after every answered question.
7. Quiz state persistence: auto-saved to localStorage after every answer/navigation; resume banner on home page; 儲存並回到首頁 button for explicit mid-quiz pause.
8. Added the CFA Level I FRA bank (514 hand-authored 3-choice questions with per-option
   explanations) and removed the Options Pricing Theory study section, its markdown
   pipeline, and the marked/KaTeX CDN dependencies.
9. Recovered six unused SFI papers from `期貨證照/_raw/probe/`: +99 futures questions and
   two new banks (`securities_rep`, `sitca`). Quiz length became per-bank; stats now
   ignore retired-bank history.
10. Restored `finance_ethics` and rebuilt the landing directory on 證基會's official
    category names.
11. Pulled every paper 證基會 currently publishes, plus 24 older sittings recovered from
    web-archive captures of the same download slots — three new banks and several more
    sittings for the existing ones. See `docs/SEARCH_LOG.md`.

**Known gap:** questions from newly added papers carry the official answer but no
`explanations`, and the 解析 block does not render for them. Writing Taiwan regulatory
rationale from memory risks confidently wrong statutory specifics, so it is left undone
rather than guessed; where an answer is a bare statutory threshold the explanation states
the rule instead of inventing a rationale. Current coverage per bank:
`sources/explanation_coverage.json`.

`build_cfa.py` also **rebalances the answer key**: hand-authored questions came out
heavily skewed toward A, so each question's options are cyclically rotated (preserving
their relative order, and carrying explanations with them) until the key lands on a
target letter from a balanced, fixed-seed-shuffled list. Keep this step if the bank is
extended — it prints the A/B/C distribution on every run.

## Deployment

Push `index.html` + `questions.json` to `main` branch — GitHub Pages deploys automatically.
Do **not** commit `_expl_work/` (large intermediate files, not needed for the site).
