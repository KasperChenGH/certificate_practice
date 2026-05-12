# 金融證照練習 / Taiwan Finance Cert Practice

Mobile-friendly web quiz for three Taiwan finance certifications:

- 期貨商業務員 — 592 questions
- 證券商高級業務員 — 297 questions
- 金融市場常識與職業道德 — 1,120 questions

Each test draws exactly **100 random questions** from the chosen bank.
Wrong-answer history is kept per-device in `localStorage` (no backend, no account).

## Live demo

After enabling GitHub Pages, the site will be at:
`https://kasperchengh.github.io/certificate_practice/`

## Run locally

```bash
python -m http.server 8000
# open http://localhost:8000
```

Don't open `index.html` directly — `fetch('questions.json')` needs an HTTP origin.

## Publish via GitHub Pages

1. Push these files to the `main` branch of this repo.
2. On GitHub: **Settings → Pages** → Source = "Deploy from a branch", Branch = `main` / `/ (root)`, Save.
3. After ~1 minute the URL above goes live.
4. Open it on your phone → browser menu → "Add to Home Screen" for an app-like icon.

## Features

| Page | What it does |
|---|---|
| Home | Stats card (total attempts / accuracy / wrong-pool size). Pick a topic to start a 100-question quiz, or open the "常錯題複習" review page. |
| Quiz | Tap an option, navigate with **上一題 / 下一題**. Final question's button becomes **交卷**. Mid-quiz abort returns to Home (current quiz is discarded). |
| Results | Score out of 100. Lists each question you missed with the correct answer and your selection. **回首頁** to return. |
| Review (常錯題) | Lists every question you've gotten wrong on ≥ 50% of your **last 10** attempts, gated by a minimum of 3 attempts. |

## Files

- `index.html` — UI + quiz/review logic (~18 KB)
- `questions.json` — combined question bank for all three exams (~820 KB, UTF-8)

## Data sources

All questions parsed from public material hosted by 證券暨期貨市場發展基金會 (SFI):
- 期貨商業務員: existing deduplicated bank covering 112年第1次 → 114年第1次
- 證券商高級業務員: SFI past papers 114年第3次 + 115年第1次 (all three sub-papers)
- 金融市場常識與職業道德: SFI official 1,120-question bank (effective 113年9月1日)

## Notes

- Question history is keyed by question ID and stored in your browser only. Clearing browser data resets it.
- The "Often wrong" threshold (10-attempt window, 3-attempt minimum, 50% miss rate) is constants near the top of `index.html` — feel free to tune.
