# sources/papers — single-subject SFI exam papers

Each `*_試題.pdf` is one subject's paper (50 multiple-choice questions). Each
`*_答案.pdf` is the session's official answer sheet, which covers **every subject in
that exam**, not just the paper next to it.

Parsed by `scripts/parse_paper.py`, wired into `questions.json` by `scripts/build.py`.

| Session | Subject | Feeds topic |
|---|---|---|
| 115年第1次 / 114年第3次 | 期貨交易法規 | `futures` (merged with the dedup bank) |
| 115年第1次 / 114年第3次 | 證券交易相關法規與實務 (證券商業務員) | `securities_rep` |
| 115年第1次 / 114年第3次 | 投信投顧相關法規 | `sitca` |

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

## Why three banks are thin, and what would fix them

證基會 publishes a complete official 題庫 for only two of these exams:

| Bank | Source | Size |
|---|---|---|
| `futures` | `../futures_exam_dedup_answers.pdf` official bank + 2 papers | 691 |
| `finance_ethics` | `../sfi_金融市場常識-113.pdf` + `../sfi_職業道德-113.pdf` | 1,120 |

For 證券商高級業務員, 證券商業務員 and 投信投顧, no official bank is published — only
past papers. So those pools are bounded by how many sittings have been collected, which
is currently two each (114年第3次 and 115年第1次):

| Bank | Papers × questions | Pool | Draw | Repeat rate |
|---|---|---|---|---|
| `securities` | 2 sittings × 3 subjects × 50 | 297 | 150 | ~51% |
| `securities_rep` | 2 sittings × 50 | 100 | 50 | 50% |
| `sitca` | 2 sittings × 50 | 97 | 50 | ~52% |

The draw is the real paper composition and cannot be shrunk without misrepresenting the
exam, so the only fix is more sittings — each one adds 50 questions per subject. Three
more sittings per bank would clear the 3× ratio that `build.py` warns below. They are
listed in `_thin_ok` in `../exam_blueprints.json` until then, and the site says so on
both the landing directory and the exam card.
