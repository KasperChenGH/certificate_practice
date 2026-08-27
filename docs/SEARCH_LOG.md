# Search log — where question sources have already been looked for

**Read this before running any web search for exam questions.** Every search below has
already been done; the point of the file is that the dead ends are not re-walked and the
working sources are re-used directly instead of re-discovered.

Append to it whenever a search is run — including the ones that find nothing, which are
the entries that save the most time.

Format per entry: what was wanted, what was searched or fetched, what came back, and
whether it is worth returning to.

---

## The one source that matters

**證基會 考題下載 — <https://www.sfi.org.tw/Node?id=217>**

Official past papers *with official answer keys*, which is what this pipeline needs:
`scripts/parse_paper.py` refuses to guess a key, so a source without a published key is
close to useless here.

It publishes **only the two most recent sittings** — "本基金會提供前兩季筆試所有測驗類別
試題及選擇題答案下載". Older papers come off the site entirely. That, not collection
effort, is the ceiling on every bank built from past papers.

Download URLs are **stable slots**:

```
https://examweb.sfi.org.tw/Download/<slot>/<code>.pdf     試題
https://examweb.sfi.org.tw/Download/<slot>/<code>a.pdf    解答
slot 01 = most recent sitting   ·   slot 02 = the one before
```

| code | exam | in the build? |
|---|---|---|
| 01 | 期貨商業務員 | yes — `futures` |
| 02 | 證券商業務員 (2 科, 100 題) | yes — `securities_rep` reads 證券交易相關法規與實務 only |
| 03 | 證券商高級業務員 (3 科) | yes — `securities` |
| 04 | 證券投資分析人員 (4 科) | **no** — see blockers |
| 06 | 投信投顧業務員 (3 科, 150 題) | yes — `sitca` reads 投信投顧相關法規 only |
| 34 | 期貨交易分析人員 (4 科) | **no** — see blockers |
| 36 | 企業內部控制 | yes — `internal_control` |
| 40 | 投信投顧相關法規乙科 | yes — feeds `sitca` |
| 53 | 證券交易相關法規與實務乙科 | yes — feeds `securities_rep` |
| 59 | 期貨信託基金銷售機構銷售人員 | yes — `futures_trust` |
| 81 | 永續發展基礎能力測驗 | yes — `sustainability` |
| 82 | 永續發展基礎能力測驗 (高雄考區) | yes — `sustainability` |
| 99 | 防制洗錢與打擊資恐專業人員 | **no** — see blockers |

**Standing action:** pull slot `01` for every code once a quarter. Each sitting is
online for two quarters and then gone; anything not captured is only recoverable from a
web archive, and only if a crawler happened to visit.

## Older sittings: Internet Archive captures of those same slots

Because the slot URLs are stable, a capture of `Download/01/53.pdf` taken in 2023 holds
whatever paper was current in 2023. This is the only route to sittings 證基會 has dropped.

```
http://web.archive.org/cdx/search/cdx?url=examweb.sfi.org.tw/Download/01/53.pdf&output=text&fl=timestamp,digest&collapse=digest
https://web.archive.org/web/<timestamp>id_/https://examweb.sfi.org.tw/Download/01/53.pdf
```

Distinct captures found (per slot, per code): **2021-04-13, 2023-09-30, 2024-06-15/16,
2026-04-11** — four each, except `01/59` which has none. Re-checking is only worth it
after a new crawl, so treat these four dates as exhausted.

Yielded 24 usable sittings across codes 36 / 40 / 53 / 59.

**The trap:** paper and key are *separate captures*. Pairing by crawl date alone can key
one sitting's questions against another's answers. `scripts/build.py` stages a pair only
when the `年第N次` in the paper matches the one in its key, and names the file from the
session read out of the PDF, never from the crawl date.

Rejected by that check, do not retry without fixing the underlying PDF:

| File | Problem |
|---|---|
| `02/40` capture 2021-04-13 | question 28 has an empty stem or option |
| `02/40` capture 2023-09-30 | only 9 of 50 questions parse |

## Dead ends — do not search these again

| Tried | Result |
|---|---|
| `https://examweb.sfi.org.tw/reg/history.aspx` | maintenance page: "目前本會站台正在施工中，請稍後再試" |
| `https://www.sfi.org.tw/exam/exam6/exam6-3` | 404 頁面不存在. The working path is `Node?id=217` |
| `Download/03/`, `/04/`, `/05/` for codes 53, 40, 36, 59 | all non-200. Only two slots exist; there is no deeper archive on the live site |
| WebSearch `證基會 examweb.sfi.org.tw 歷屆試題 下載 期貨商業務員 投信投顧 證券商業務員` | only re-surfaced sfi.org.tw's own nodes (214 / 216 / 217 / 247). Nothing a direct fetch of `Node?id=217` does not give |

## Also fetched

| URL | Purpose | Result |
|---|---|---|
| `https://examweb.sfi.org.tw/regexam/index.aspx` | official exam names and categories | the five categories the landing directory is now organised by (證券、投信投顧暨期貨從業人員資格測驗 / 能力測驗 / 金融常識測驗 / 防制洗錢測驗 / 永續發展基礎能力測驗). Still the authority for naming |

---

## Blockers, not gaps

These have official papers available at the URLs above. They are absent from the build
for reasons that a further search will not solve.

| Exam | Why it is not in the build |
|---|---|
| 證券投資分析人員 (04) | The key prints two subjects side by side in one grid; column-to-subject mapping cannot be recovered from vertical position. `parse_answers_by_subject` raises on it by design. Needs column-aware extraction plus an independent check on the result |
| 期貨交易分析人員 (34) | Four subjects, and the paper carries non-multiple-choice sections |
| 防制洗錢與打擊資恐 (99) | Questions 61–80 are 複選題 with keys like `ABCD`. The app models exactly one correct option, so this needs an app change, not a source |

## Never searched — genuinely open

- **Third-party question sites.** Not searched at all: the official source covered every
  exam that is currently in the build, and a reposted question carries an unverified key.
  Worth trying only for the exams below, and only with the key treated as suspect.
- **能力測驗: 債券人員, 股務人員, 工商倫理, 資產證券化, 票券商業務人員, 公司治理.** These do
  **not** appear on `Node?id=217` — of the ability tests only 企業內部控制 and 永續發展 are
  published there. No official past papers exist to fetch, so third-party is the only
  route.
- **CFA Level II / III.** No search run. `cfa_fra` (Level I) was hand-authored against the
  curriculum rather than sourced, so the same approach would apply.
- **`sources/exam_blueprints.json` pass marks** for the newer banks were read off each
  paper's own 注意 line, not looked up. If a pass mark ever matters more precisely,
  證基會's 簡章 (`Node?id=216`) is the place to check.
