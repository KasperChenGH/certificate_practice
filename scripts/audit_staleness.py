"""Flag questions at risk of having gone stale, and show how old the banks are.

`audit_conflicts.py` proves internal consistency: it finds a question asked in two
sessions with two different answers. That catches a rule change only when the same
question was asked again after the change. It cannot catch a rule that moved after a
question's last appearance.

This script covers the other axis. It does not decide correctness — there is no
authoritative feed here — it produces a ranked review list:

  1. Age profile per bank, so you know how much of it predates the current rules.
  2. References to superseded benchmarks and delisted instruments (LIBOR, Eurodollar).
  3. Old questions turning on a hard number — a monetary threshold, a percentage, a
     day count. These are what regulators actually revise, and a revision leaves no
     internal trace if the question was never re-asked.

    python scripts/audit_staleness.py [--oldest 113] [--limit 12]
"""
from __future__ import annotations
import json, re, sys, io, argparse, importlib.util
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REPO = Path(__file__).resolve().parent.parent
QUESTIONS = REPO / 'questions.json'

# Benchmarks and contracts that have been replaced or delisted. A question can still be
# examinable history, but the answer should be read with the transition in mind.
SUPERSEDED = {
    'LIBOR': 'replaced by SOFR/risk-free rates; LIBOR panels ceased 2021-2023',
    '倫敦銀行同業拆款利率': 'LIBOR by another name',
    '歐洲美元': 'CME stopped listing new Eurodollar futures in 2023; open interest converted to SOFR',
    'Eurodollar': 'CME stopped listing new Eurodollar futures in 2023',
}

# A hard number in the keyed answer is what a rule change moves.
NUMERIC = re.compile(
    r'\d[\d,]*\s*(?:%|％|元|億|萬|千萬|百萬|日|天|個月|年|倍|口|成|分之|基點|bp)'
    r'|百分之[一二三四五六七八九十百千零〇\d]+'
    r'|[一二三四五六七八九十]+(?:日|天|個月|年|倍|成)'
)


def year_of(origin: str) -> int | None:
    m = re.search(r'(\d{3})\s*年第', origin or '')
    return int(m.group(1)) if m else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--oldest', type=int, default=113,
                    help='questions from before this ROC year are treated as at-risk')
    ap.add_argument('--limit', type=int, default=12, help='samples to print per section')
    args = ap.parse_args()

    data = json.loads(QUESTIONS.read_text(encoding='utf-8'))

    # ---- 1. age profile -----------------------------------------------------
    print('=' * 78)
    print('AGE PROFILE  (ROC year of the source exam session)')
    print('=' * 78)
    for topic, qs in data.items():
        if topic == 'cfa_fra':
            print(f'{topic:16s} {len(qs):5d}  authored against the current curriculum, '
                  f'no session history')
            continue
        years = Counter(year_of(q.get('origin', '')) for q in qs)
        parts = ' '.join(f'{y}年:{n}' for y, n in sorted(years.items(), key=lambda t: (t[0] or 0)))
        unknown = years.get(None, 0)
        print(f'{topic:16s} {len(qs):5d}  {parts}' + ('  (unknown origin)' if unknown else ''))

    # ---- 2. superseded references ------------------------------------------
    print()
    print('=' * 78)
    print('REFERENCES TO SUPERSEDED BENCHMARKS / DELISTED CONTRACTS')
    print('=' * 78)
    hits = defaultdict(list)
    for topic, qs in data.items():
        for q in qs:
            blob = q['stem'] + ' ' + ' '.join(q['options'].values())
            for term in SUPERSEDED:
                if term in blob:
                    hits[term].append(q)
    if not hits:
        print('none')
    for term, qlist in sorted(hits.items(), key=lambda t: -len(t[1])):
        print(f'\n{term}  ({len(qlist)} questions) — {SUPERSEDED[term]}')
        for q in qlist[:args.limit]:
            print(f'   {q["id"]:36s} {q.get("origin","")}')
            print(f'      {q["stem"][:96]}')
        if len(qlist) > args.limit:
            print(f'   ... and {len(qlist) - args.limit} more')

    # ---- 3. old questions turning on a hard number --------------------------
    print()
    print('=' * 78)
    print(f'PRE-{args.oldest}年 QUESTIONS WHOSE ANSWER IS A HARD NUMBER')
    print('=' * 78)
    print('Highest staleness risk: a revised threshold leaves no internal trace unless')
    print('the question was asked again afterwards. Verify against the current rule.\n')
    at_risk = []
    for topic, qs in data.items():
        if topic == 'cfa_fra':
            continue
        for q in qs:
            y = year_of(q.get('origin', ''))
            if y is None or y >= args.oldest:
                continue
            keyed = q['options'].get(q['answer'], '')
            if NUMERIC.search(keyed):
                at_risk.append((topic, q, keyed))
    # Re-confirmation: if the same question was asked again in year >= --oldest and
    # kept the same answer, the threshold demonstrably still held at that later date.
    spec = importlib.util.spec_from_file_location(
        'ac', Path(__file__).resolve().parent / 'audit_conflicts.py')
    ac = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ac)

    pool = [q for topic, items in data.items() if topic != 'cfa_fra' for q in items]
    ac.prepare(pool)
    confirmed_by: dict[str, dict] = {}
    for _, qa, qb in ac.near_duplicate_pairs(pool):
        if qa['_key'] != qb['_key']:
            continue
        for old_q, new_q in ((qa, qb), (qb, qa)):
            yo = year_of(old_q.get('origin', ''))
            yn = year_of(new_q.get('origin', ''))
            if yo is not None and yn is not None and yo < args.oldest <= yn:
                confirmed_by[old_q['id']] = new_q

    confirmed = [t for t in at_risk if t[1]['id'] in confirmed_by]
    unconfirmed = [t for t in at_risk if t[1]['id'] not in confirmed_by]
    print(f'{len(at_risk)} questions flagged: '
          f'{len(confirmed)} re-confirmed by a later paper, '
          f'{len(unconfirmed)} unconfirmed\n')

    if confirmed:
        print(f'--- re-confirmed (same answer still keyed in {args.oldest}年 or later) ---')
        for topic, q, keyed in confirmed:
            newer = confirmed_by[q['id']]
            print(f'  {q["id"]:30s} {q.get("origin","")}')
            print(f'     still keyed the same in {newer["id"]}  {newer.get("origin","")}')
        print()

    print(f'--- unconfirmed: never re-asked in {args.oldest}年 or later ---')
    for topic, q, keyed in unconfirmed[:args.limit]:
        print(f'  {q["id"]:36s} {q.get("origin","")}')
        print(f'     Q: {q["stem"][:92]}')
        print(f'     A: ({q["answer"]}) {keyed[:80]}')
    if len(unconfirmed) > args.limit:
        print(f'  ... and {len(unconfirmed) - args.limit} more '
              f'(raise --limit to see them all)')

    print()
    print('=' * 78)
    print('This is a review list, not a list of errors. Nothing here is known to be')
    print('wrong; these are the questions whose correctness depends on rules that may')
    print('have moved since the paper was set.')


if __name__ == '__main__':
    main()
