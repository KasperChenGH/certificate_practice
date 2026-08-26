# Handover — certificate_practice
Updated: 2026-08-26

Kept in the repo rather than `~/.claude/projects/…` so it travels with `git pull`.

## Current state

Quiz site for four Taiwan finance certifications plus a CFA Level I FRA drill —
**1,699 questions**. Static: one `index.html` plus `questions.json` and
`blueprints.json`, no backend, no build step.

Live at **https://certifications.courses/** (GoDaddy DNS, GitHub Pages hosting), with a
Let's Encrypt certificate valid to 2026-11-24 and Enforce HTTPS on.

## What was done this session

- **CFA Level I FRA bank: 133 → 514 questions**, hand-authored across 13 FSA sections.
  Answer key was skewed A=291/B=216/C=7; `build_cfa.py` now rotates options onto a
  balanced, fixed-seed target list (A=172/B=171/C=171) and prints the distribution.
- **Recovered 6 unused SFI papers** from `期貨證照/_raw/probe/`: futures 592 → 691, plus
  two new banks (`securities_rep` 100, `sitca` 97). Retired `金融市場常識與職業道德`
  (exam passed) — parser and PDFs kept, just not built.
- **測驗紀錄 (exam history)**: every submitted exam recorded with its wrong questions,
  per-topic summary, and 檢視本次錯題 straight off the results page.
- **Exam blueprints**: each paper now mirrors the real exam's subject split
  (futures = 法規 50 + 理論與實務 50) with **per-subject scoring**, since these exams
  fail you for failing one subject.
- **Audits**: `audit_conflicts.py` found 0 real contradictions across 1,185 questions;
  `audit_staleness.py` flags age and rule-change risk.
- Fixed 4 wrong explanations (SOFR contract size, DJIA spread, Eurodollar time value,
  交割結算基金 事前/事後) and one 同上題 stem that broke under shuffling.

## Key decisions made

- **Explanations for the 293 recovered questions were deliberately NOT written.**
  Taiwan regulatory rationale from memory risks confidently wrong statutory specifics —
  exactly how the SOFR error got in. The answer still shows; only 解析 is absent.
- **證券投資分析人員 papers excluded.** Their answer PDF is a two-column interleaved
  grid; the column→subject mapping can't be read from position. See
  `sources/papers/README.md`. ~63 questions recoverable with column-aware parsing.
- **Apex domain, not www.** A CNAME can't sit at a zone apex, so it needs the four A
  records. The repo `CNAME` file (≠ a DNS CNAME record) is what binds the domain.
- **Stayed on GitHub Pages, not GCP.** Static site; GCP costs money, needs a load
  balancer for HTTPS, and would hit the identical DNS-cache delay.

## Pending / next steps

**Nothing blocking. The site is live at https://certifications.courses/ with a valid
Let's Encrypt certificate and Enforce HTTPS on; `http://` 301s to `https://`.**

Optional, in rough order of value:

1. Explanations for the 293 recovered questions (99 futures, 97 securities_rep,
   97 sitca) — only if sourced rather than written from memory.
2. Recover the 證券投資分析人員 papers (~63 questions); needs column-aware parsing of a
   two-column answer key. See `sources/papers/README.md`.
3. `www` CNAME → `kasperchengh.github.io` (currently points at the apex, which works).
4. Confirm the 證券商高級業務員 blueprint: it is set to 150 questions to mirror the
   source paper's three 試卷. Change in `sources/exam_blueprints.json` if the real exam
   is a 100-question two-subject paper.

## Important context

- **DNS was correct within minutes; caches were the whole problem.** Records verified
  at both GoDaddy nameservers. The delay was resolver caching — the office resolver
  flapped between fresh and stale for over an hour. Nothing was misconfigured.
- GoDaddy **Forwarding** pins the apex A record and must be deleted before the DNS
  panel will accept multiple A records. `check_domain.py` detects it.
- GoDaddy's parking page served a **308 permanent redirect** to `https://`. Browsers
  cache those hard; a stale one can survive correct DNS. Hard-refresh or incognito.
- **Editing a stem directly in `questions.json` does not survive a rebuild** — stems come
  from the PDF parse. Use `sources/stem_overrides.json`. Explanations *are* carried over
  (matched by id, then fingerprint).
- `build.py` **fails** on a blueprint naming an unknown subject, an oversized section, or
  a stem referencing another question with no override. Those guards are deliberate.
- **The certificate request wedged once.** GitHub reported the domain valid and
  `is_https_eligible: True` for 15 hours while never creating a certificate record at
  all. Re-saving the same domain via the API is a no-op. What fixed it: delete the root
  `CNAME`, push, let Pages rebuild without a custom domain, then restore `CNAME` and
  push — the certificate was approved within seconds. Doing it through the file rather
  than the Pages UI keeps the commits in your own history.

## Files touched this session

```
index.html                      history pages, blueprint sampling, per-subject scoring
questions.json / blueprints.json    generated — rebuild with scripts/build.py
CNAME                           certifications.courses
scripts/  build.py  build_cfa.py  parse_paper.py  check_domain.py  dnsq.py
          await_https.py  audit_conflicts.py  audit_staleness.py
          test_blueprints.py  test_stem_overrides.py
sources/  cfa_fra.json  cfa_batches/  papers/  exam_blueprints.json
          stem_overrides.json
CLAUDE.md  README.md  sources/papers/README.md
```

Rebuild everything: `pip install pymupdf && python scripts/build.py` (deterministic —
byte-identical on unchanged inputs).
