# Handover — certificate_practice
Updated: 2026-08-26

Kept in the repo rather than `~/.claude/projects/…` so it travels with `git pull`.

## Current state

Quiz site for four Taiwan finance certifications plus a CFA Level I FRA drill —
**1,699 questions**. Static: one `index.html` plus `questions.json` and
`blueprints.json`, no backend, no build step.

Just moved to the custom domain **certifications.courses** (GoDaddy DNS, GitHub Pages
hosting). **HTTP works and is fully verified. HTTPS is not live** and looks stuck rather
than merely slow — see Pending item 1, which is the first thing to do.

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

1. **HTTPS certificate — appears STUCK, needs a manual re-trigger.**
   DNS is finished and verified from GitHub's own side:
   `is_pointed_to_github_pages_ip`, `is_served_by_pages`, `is_valid` and
   `is_https_eligible` are all **True**, `caa_error` is None, `www` is valid, and the
   ACME challenge path answers from GitHub on port 80. Despite that, a watcher polled
   for **2 hours (58 checks, all `eligible=True`) and no certificate was ever issued** —
   the Pages API has no `https_certificate` key at all, meaning the request was never
   initiated rather than being in progress. Re-saving the same domain via
   `PUT /pages -f cname=…` did not help; it is a no-op.

   **Do this first on the other machine** — the documented remedy is to remove and
   re-add the custom domain so Pages re-requests the certificate:
   Settings → Pages → Custom domain → clear the field → Save → wait ~1 min →
   re-enter `certifications.courses` → Save.

   Expect GitHub to delete and recreate the root `CNAME` file as it does this, which
   creates commits on `main` — `git pull` before pushing anything afterwards.

   Then:
   ```bash
   python scripts/check_domain.py          # says exactly what is outstanding
   python scripts/await_https.py           # polls, then enables Enforce HTTPS
   ```
   Do not enable enforcement before the certificate exists — it errors.
   Until it is issued the site works on `http://` only.
2. Optional: `www` CNAME → `kasperchengh.github.io` (currently points at the apex,
   which works).
3. Optional: explanations for the 293 questions, if sourced rather than invented.
4. Optional: recover the 證券投資分析人員 papers.

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
- A background HTTPS watcher was running on the previous machine; it does not follow the
  repo. Re-run `await_https.py` if the certificate is still pending.

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
