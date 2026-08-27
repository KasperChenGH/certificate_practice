# sources/papers — single-subject SFI exam papers

Each `*_試題.pdf` is one subject's paper (50 multiple-choice questions). Each
`*_答案.pdf` is the session's official answer sheet, which covers **every subject in
that exam**, not just the paper next to it.

Parsed by `scripts/parse_paper.py`, wired into `questions.json` by `scripts/build.py`.

| Session | Subject | Feeds topic |
|---|---|---|
| 115年第2次 / 115年第1次 / 114年第3次 | 期貨交易法規 ＋ 期貨交易理論與實務 | `futures` (merged with the dedup bank) |
| 115年第2次 | 投資學 ／ 財務分析 ／ 法規與實務 | `securities` (merged with the `sec/` sessions) |
| 115年第2次 / 115年第1次 / 114年第3次 | 證券交易相關法規與實務 | `securities_rep` |
| 115年第2次 / 115年第1次 / 114年第3次 | 投信投顧相關法規 | `sitca` |
| 115年第2次 / 115年第1次 | 期貨信託法規及自律規範 | `futures_trust` |
| 115年第2次 / 115年第1次 | 企業內部控制理論與實務 | `internal_control` |
| 115年第4次 / 114年第4次 ＋ 高雄考區 | 永續發展 | `sustainability` |

## A paper carries more than the subject it is filed under

`115Q1_證券商業務員_試題.pdf` is the whole 100-question paper — 證券交易相關法規與實務 50
＋ 證券投資與財務分析 50 — and `115Q1_投信投顧_試題.pdf` is the whole 150-question,
three-subject paper. Each bank reads one section out of its paper, so **the file name
names the exam, not the bank's contents**.

Two parser bugs were latent in that arrangement until sections other than the first
were needed, because every bank happens to read section 1:

- `parse_questions_pdf` ignored `subject` and read questions from the top of the
  document. Asking for section 2 returned section 1's questions paired with section 2's
  key — the same 50 questions, every answer wrong. It now narrows to the 科目 heading
  that names the subject.
- `parse_answers_by_subject` matched a subject as a substring of a label. `財務分析`
  matches both `證券投資與財務分析－試卷「投資學」` and `…試卷「財務分析」`, so 財務分析
  silently took 投資學's key. Matching more than one label is now an error; pass
  `「財務分析」` to disambiguate.

## Why the answer block is chosen by label, not by position

An answer PDF lays out a session title, then for each subject a label line
("期貨交易法規試題解答") followed by a grid of number/letter pairs. Taking the first
grid would silently attach another subject's key — every question would still look
well-formed, and every answer would be wrong.

`parse_answers_by_subject` therefore extracts blocks **with coordinates**, finds the
label containing the subject name, and reads the grid that follows it. It raises
rather than guess if the label is missing, or if the resulting key is not a gapless
run starting at 1.

## Not included: 證券投資分析人員 (CSIA)

`期貨證照/_raw/probe/s01_04*.pdf` and `s02_04*.pdf` hold the 證券投資分析人員 papers
(28 and 35 multiple-choice questions). They are **deliberately excluded**.

Their answer PDF prints two subjects side by side in a single two-column grid, with
both labels on one line:

```
y= 89.1  投資學試題答案   證券交易相關法規與實務試題答案
y=123.6  1 D 2 C 3 B 4 C 5 C 1 C 2 B 3 B 4 C 5 A 6 A 7 C ...
```

The two keys interleave in the extracted text and the column-to-subject mapping
cannot be established from vertical position. `parse_answers_by_subject` raises on
this layout by design. Recovering these ~63 questions needs column-aware extraction
plus an independent check on the resulting key — worth doing, but not worth guessing.

## Where the older sittings came from

**證基會 only publishes the two most recent sittings** ("本基金會提供前兩季筆試所有測驗
類別試題及選擇題答案下載"), so older papers cannot be fetched from the site at all.

The download URLs are stable slots — `Download/01/<code>.pdf` is always the most recent
sitting and `Download/02/<code>.pdf` the one before — which means an Internet Archive
capture of those URLs holds whichever paper was current on the crawl date. Captures from
2021, 2023, 2024 and 2026 yielded 24 further sittings across four subjects.

Every archived pair is only used after the 年第N次 in the paper matches the 年第N次 in its
key: the two files are separate captures, and a mismatched pair would key one sitting's
questions against another's answers. `scripts/build.py` names each staged file by the
session read out of the PDF, not by the crawl date.

A complete official 題庫 exists for exactly two exams: `futures`
(`../futures_exam_dedup_answers.pdf`) and `finance_ethics` (`../sfi_金融市場常識-113.pdf`
＋ `../sfi_職業道德-113.pdf`, 1,120 questions). Every other bank is past papers only, so
its size is (sittings collected) × (questions per paper).

Banks under the 3× pool-to-draw ratio `build.py` warns below are listed in `_thin_ok` in
`../exam_blueprints.json`, and an entry there that is no longer thin is a build error —
otherwise the list silently stops meaning anything.


## Not yet included

| Exam | Blocker |
|---|---|
| 證券投資分析人員 | The key prints two subjects side by side in one grid; column-to-subject mapping cannot be established from vertical position. `parse_answers_by_subject` raises on it by design. |
| 期貨交易分析人員 | Four subjects, and the paper carries non-multiple-choice sections. |
| 防制洗錢與打擊資恐專業人員 | Questions 61–80 are 複選題 with keys like `ABCD`; the app only models one correct option. |
| 證券商業務員 證券投資與財務分析, 投信投顧業務員 remaining two subjects | Parseable now that the parser is subject-aware — these are the next papers to wire in, not a blocker. |

## An answer key can carry errata

`115Q2` 投信投顧相關法規 prints "第36題修正為(A)(B)均給分" below the grid. Two things follow:
a prose line must never be tokenised as answers (it read as `36 -> A` and overwrote the
real key), and a question with two accepted options cannot be stored against a single
answer. `parse_answers_by_subject` returns those question numbers and `parse_paper` drops
them.