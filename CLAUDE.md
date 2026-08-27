# CLAUDE.md — certificate_practice

## Project

Mobile-friendly quiz webapp for Taiwan financial certification exams, hosted on GitHub Pages.
Live URL: `https://certifications.courses/`
(custom domain, set by the root `CNAME` file; the old
`kasperchengh.github.io/certificate_practice/` address redirects to it)

## Scope

Two pages, static data, no backend:

- `index.html` — the landing page at the domain root. **Generated**: edit
  `design/Main.dc.html` and run `node design/build-site.mjs`; never edit `index.html`
  directly, a rebuild overwrites it.
- `app.html` — the quiz app itself (hand-maintained). Mobile-first, with desktop
  layouts behind `@media (min-width: 1024px)`.
- `questions.json` + `blueprints.json` — fetched relatively, so both work at any root.

Run locally: `python -m http.server 8000` then open `http://localhost:8000`.

## Question banks

| Topic key         | Display name               | Count |
|-------------------|---------------------------|-------|
| `futures`         | 期貨商業務員               | 691   |
| `securities`      | 證券商高級業務員            | 297   |
| `securities_rep`  | 證券商業務員                | 100   |
| `sitca`           | 投信投顧業務員              | 97    |
| `cfa_fra`         | CFA Level I — Financial Reporting & Analysis | 514 |

**Retired:** `finance_ethics` (金融市場常識與職業道德, 1120 q) — exam passed, no longer
published. `build_finance_ethics()`, `parse_bank.py`, and the source PDFs are kept; restore
by calling it from `build.py`'s `main()` again.

### Exam blueprints

A practice paper mirrors the real exam's subject split instead of drawing at random.
`sources/exam_blueprints.json` is the one home for that; `build.py` validates it against the
built banks and emits `blueprints.json` for the app.

| Bank | Paper drawn |
|---|---|
| `futures` | 100 = 期貨交易法規 50 + 期貨交易理論與實務 50 |
| `securities` | 150 = 投資學 50 + 財務分析 50 + 法規與實務 50 |
| `securities_rep` | 50 = 證券交易相關法規與實務 50 |
| `sitca` | 50 = 投信投顧相關法規 50 |
| `cfa_fra` | 90 = a full CFA session length, 13 sections proportional to bank coverage |

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

`explanations` was LLM-generated for all 2009 questions (Traditional Chinese, per-option).

## Data sources

- **期貨商業務員**: deduplicated PDF covering 112年第1次 → 114年第1次 (592 q after dedup)
- **證券商高級業務員**: SFI past papers 114年第3次 + 115年第1次; 3 concatenated sub-papers per PDF (投資學 / 財務分析 / 法規)
- **金融市場常識與職業道德**: SFI official 1,120-question bank effective 113年9月1日
- **期貨交易法規 / 證券商業務員 / 投信投顧**: single-subject SFI papers for 114年第3次 and
  115年第1次, in `sources/papers/` — see the README there. Answer blocks are matched to
  subjects **by printed label with coordinates**, never by position, because each answer PDF
  covers every subject in that session's exam.
- **CFA Level I FRA**: 514 questions hand-authored against the CFA Level I Financial Statement
  Analysis curriculum — not parsed from any PDF. Canonical file: `sources/cfa_fra.json`,
  assembled from batch files by `scripts/build_cfa.py`.

Source PDFs live in `sources/`. Rebuild script: `python scripts/build.py` (requires `pip install pymupdf`).
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
index.html          Full webapp — quiz logic, review page, localStorage, all CSS/JS
questions.json      Combined question bank (~1.5 MB, UTF-8, includes explanations)
scripts/
  build.py          Orchestrator — rebuilds questions.json from source PDFs
  parse_bank.py     Parses SFI 金融市場常識 / 職業道德 bank PDFs
  parse_sec.py      Parses 證券高業 試題 + 答案 PDFs (3 papers per session)
  parse_paper.py    Parses a single-subject paper; picks the answer block by subject label
  build_cfa.py      Validates + assembles the hand-authored CFA bank into sources/cfa_fra.json
  test_blueprints.py  Asserts build.py rejects a blueprint that does not match the data
sources/            Source PDFs (~6.5 MB) + cfa_fra.json + papers/ (single-subject papers)
_expl_work/         Explanation generation artifacts (pilot + 14 chunks, merge.py)
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
5. LLM-generated per-option explanations (Traditional Chinese) for all 2009 questions via parallel subagents; merged into questions.json.
6. Updated quiz UI to display 解析 explanation block after every answered question.
7. Quiz state persistence: auto-saved to localStorage after every answer/navigation; resume banner on home page; 儲存並回到首頁 button for explicit mid-quiz pause.
8. Added the CFA Level I FRA bank (514 hand-authored 3-choice questions with per-option
   explanations) and removed the Options Pricing Theory study section, its markdown
   pipeline, and the marked/KaTeX CDN dependencies.
9. Recovered six unused SFI papers from `期貨證照/_raw/probe/`: +99 futures questions and
   two new banks (`securities_rep`, `sitca`). Retired `finance_ethics`. Quiz length became
   per-bank; stats now ignore retired-bank history.

**Known gap:** the 293 questions added in step 9 have no `explanations` (99 futures, 97
securities_rep, 97 sitca). The 解析 block simply does not render for them. Writing Taiwan
regulatory rationale from memory risks confidently wrong statutory specifics, so it was
left undone rather than guessed.

`build_cfa.py` also **rebalances the answer key**: hand-authored questions came out
heavily skewed toward A, so each question's options are cyclically rotated (preserving
their relative order, and carrying explanations with them) until the key lands on a
target letter from a balanced, fixed-seed-shuffled list. Keep this step if the bank is
extended — it prints the A/B/C distribution on every run.

## Deployment

Push `index.html` + `questions.json` to `main` branch — GitHub Pages deploys automatically.
Do **not** commit `_expl_work/` (large intermediate files, not needed for the site).
