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

## Retired: 金融市場常識與職業道德

That bank is no longer published (exam passed). `build_finance_ethics()` in
`build.py` and `parse_bank.py` are kept, along with the source PDFs in `sources/`,
so it can be restored by calling it from `main()` again.
