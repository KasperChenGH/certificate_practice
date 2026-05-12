# CLAUDE.md — certificate_practice

## Project

Mobile-friendly quiz webapp for Taiwan financial certification exams, hosted on GitHub Pages.
Live URL: `https://kasperchengh.github.io/certificate_practice/`

## Scope

Single-file frontend (`index.html`) + static data (`questions.json`). No backend, no build step.
Run locally: `python -m http.server 8000` then open `http://localhost:8000`.

## Question banks

| Topic key         | Display name               | Count |
|-------------------|---------------------------|-------|
| `futures`         | 期貨商業務員               | 592   |
| `securities`      | 證券商高級業務員            | 297   |
| `finance_ethics`  | 金融市場常識與職業道德       | 1120  |

Each quiz draws exactly 100 random questions from the chosen bank.

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

Source PDFs live in `sources/`. Rebuild script: `python scripts/build.py` (requires `pip install pymupdf`).

## Key files

```
index.html          Full webapp — quiz logic, review page, localStorage, all CSS/JS
questions.json      Combined question bank (~1.5 MB, UTF-8, includes explanations)
scripts/
  build.py          Orchestrator — rebuilds questions.json from source PDFs
  parse_bank.py     Parses SFI 金融市場常識 / 職業道德 bank PDFs
  parse_sec.py      Parses 證券高業 試題 + 答案 PDFs (3 papers per session)
sources/            Source PDFs (~6.5 MB)
_expl_work/         Explanation generation artifacts (pilot + 14 chunks, merge.py)
```

## App pages

| Page       | Behaviour |
|-----------|-----------|
| Home      | Stats card (total attempts / accuracy / wrong-pool size). Resume banner shown if a saved quiz exists. Pick topic → start 100-question quiz. |
| Quiz      | Tap option → immediate locked feedback. Correct option goes green, wrong selection goes red. 解析 block shows per-option explanation for all 4 choices. Navigate with 上一題 / 下一題. Last question becomes 交卷. Bottom has 儲存並回到首頁 (saves progress, returns home) and 放棄並回首頁 (clears progress after confirm). |
| Results   | Score out of 100, topic name, wrong count. 回首頁 button. |
| Review    | 常錯題複習 — lists questions wrong ≥ 50% of last 10 attempts (min 3 attempts). Shows all options + correct answer + error ratio. |

## localStorage

| Key | Schema | Purpose |
|-----|--------|---------|
| `quiz_history_v1` | `{ [questionId]: { attempts: [true\|false, ...] } }` (last 10 kept) | Per-question attempt history; drives stats and often-wrong detection. Cleared via 清除作答紀錄. |
| `quiz_state_v1` | `{ topic, questionIds[], answers[], idx }` | In-progress quiz snapshot. Saved after every answer and navigation. Cleared on submit or 放棄. |

## Quiz resume flow

State is auto-saved after every answer and navigation tap. To explicitly pause: tap **儲存並回到首頁** — goes home without touching state. On next visit a banner shows "繼續上次測驗 — [topic] 已作答 X / 100 題" with **繼續作答** and **捨棄** buttons.

## Constants (top of index.html `<script>`)

```js
const QUIZ_SIZE = 100;
const RECENT_WINDOW = 10;   // sliding window for often-wrong detection
const MIN_ATTEMPTS = 3;     // min attempts before a question can be "often wrong"
const WRONG_RATIO = 0.5;    // threshold: ≥50% wrong → often wrong
```

## Work completed

1. Parsed all source PDFs into structured JSONL using PyMuPDF + custom row-clustering parsers.
2. Deduplicated questions via SHA-1 fingerprint on normalized stem text.
3. Built initial webapp with 3-topic quiz, localStorage history, "often wrong" review page.
4. UI refinements: abort button spacing, inline per-question correct-answer feedback, score-only results page.
5. LLM-generated per-option explanations (Traditional Chinese) for all 2009 questions via parallel subagents; merged into questions.json.
6. Updated quiz UI to display 解析 explanation block after every answered question.
7. Quiz state persistence: auto-saved to localStorage after every answer/navigation; resume banner on home page; 儲存並回到首頁 button for explicit mid-quiz pause.

## Deployment

Push `index.html` + `questions.json` to `main` branch — GitHub Pages deploys automatically.
Do **not** commit `_expl_work/` (large intermediate files, not needed for the site).
