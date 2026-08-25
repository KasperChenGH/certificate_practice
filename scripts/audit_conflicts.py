"""Find questions that contradict each other across exam sessions.

The banks span 112年第1次 (2023) to 115年第1次 (2026). When a rule changes, an old
paper's answer becomes wrong while the bank still carries it. There is no authoritative
feed to check against here, but there is a strong internal signal: the same question
asked in two sessions with two different correct answers. Either a rule moved, or one
of them is mis-keyed. Both are worth a human look.

Dedup uses an exact stem+options fingerprint, so a reworded restatement of the same
question survives as a separate entry — which is exactly what this looks for.

Two questions count as "the same" only when BOTH the stem and the set of options are
near-identical. Stem alone is not enough: generic stems such as 下列敘述何者有誤? recur
across sessions attached to completely different options.

Answers are compared on the TEXT of the keyed option, never the letter, since sessions
shuffle option order. That text is normalised for the variants that carry no meaning:
臺/台, 僅 before an enumeration, punctuation, and whitespace.

    python scripts/audit_conflicts.py [--threshold 0.85] [--all]

Exit status is 0 always — this reports, it does not gate the build.
"""
from __future__ import annotations
import json, re, sys, io, argparse
from difflib import SequenceMatcher
from itertools import combinations
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
QUESTIONS = REPO / 'questions.json'

PUNCT = re.compile(r'[\s,，。：:；;、？?（）()「」『』【】\.]+')


def norm(s: str) -> str:
    return PUNCT.sub('', (s or '').replace('臺', '台'))


def norm_answer(s: str) -> str:
    """Normalise a keyed option for comparison.

    '僅甲、乙、丙' and '甲、乙、丙' are the same claim; so are 新台幣/新臺幣. Leading
    '僅' is dropped only in front of an enumeration, never from prose such as
    '僅限主管機關核准者'.
    """
    t = norm(s)
    t = re.sub(r'^僅(?=[甲乙丙丁戊己ABCD一二三四1234])', '', t)
    t = t.replace('選項', '')
    return t


def session_of(origin: str) -> str:
    """Sort key that orders 112年第1次 < 113年第2次 < 115年第1次."""
    m = re.search(r'(\d{3})\s*年第\s*(\d)\s*次', origin or '')
    return f'{m.group(1)}-{m.group(2)}' if m else '000-0'


def opts_blob(q: dict) -> str:
    return norm('|'.join(sorted(v for v in q['options'].values() if v)))


def shingles(s: str, k: int = 4) -> set[str]:
    return {s[i:i + k] for i in range(max(1, len(s) - k + 1))}


def prepare(qs: list[dict]) -> None:
    for q in qs:
        q['_stem'] = norm(q['stem'])
        q['_opts'] = opts_blob(q)
        q['_key'] = norm_answer(q['options'].get(q['answer'], ''))


def near_duplicate_pairs(qs: list[dict], threshold: float = 0.85):
    """Yield (score, qa, qb) for questions alike in BOTH stem and option set.

    Assumes prepare() has run. Shared with audit_staleness.py so both audits agree
    on what counts as "the same question".
    """
    buckets: dict[str, list[int]] = defaultdict(list)
    for i, q in enumerate(qs):
        for sh in shingles(q['_stem'] + q['_opts']):
            buckets[sh].append(i)
    cand: set[tuple[int, int]] = set()
    for idxs in buckets.values():
        if len(idxs) > 40:
            continue
        for a, b in combinations(sorted(idxs), 2):
            cand.add((a, b))
    for a, b in cand:
        qa, qb = qs[a], qs[b]
        if abs(len(qa['_stem']) - len(qb['_stem'])) > 40:
            continue
        rs = SequenceMatcher(None, qa['_stem'], qb['_stem']).ratio()
        if rs < threshold:
            continue
        ro = SequenceMatcher(None, qa['_opts'], qb['_opts']).ratio()
        if ro < threshold:
            continue
        yield (rs + ro) / 2, qa, qb


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--threshold', type=float, default=0.85)
    ap.add_argument('--all', action='store_true',
                    help='also list agreeing near-duplicates')
    args = ap.parse_args()

    data = json.loads(QUESTIONS.read_text(encoding='utf-8'))
    # The CFA bank is authored in one pass rather than accumulated across exam
    # sessions, so cross-session drift does not apply to it.
    qs = [q for topic, items in data.items() if topic != 'cfa_fra' for q in items]
    prepare(qs)
    print(f'Comparing {len(qs)} questions from the Taiwan banks '
          f'(threshold {args.threshold})\n')

    conflicts, agree = [], []
    for r, qa, qb in near_duplicate_pairs(qs, args.threshold):
        if qa['_key'] and qa['_key'] == qb['_key']:
            agree.append((r, qa, qb))
        else:
            conflicts.append((r, qa, qb))

    conflicts.sort(key=lambda t: -t[0])
    print(f'Near-duplicate pairs (stem AND options both >= {args.threshold}): '
          f'{len(conflicts) + len(agree)}')
    print(f'  answers agree    : {len(agree)}')
    print(f'  answers CONFLICT : {len(conflicts)}\n')

    if args.all:
        for r, qa, qb in sorted(agree, key=lambda t: -t[0]):
            print(f'  agree {r:.2f}  {qa["id"]} / {qb["id"]}')
        print()

    for r, qa, qb in conflicts:
        older, newer = sorted((qa, qb), key=lambda q: session_of(q.get('origin', '')))
        print('=' * 78)
        print(f'similarity {r:.2f}')
        for tag, q in (('older', older), ('newer', newer)):
            print(f'  [{tag}] {q["id"]}  {q.get("origin", "")}')
            print(f'         {q["stem"][:110]}')
            print(f'         keyed ({q["answer"]}) {q["options"].get(q["answer"], "")[:90]}')
    if not conflicts:
        print('No contradictory answers found between near-duplicate questions.')


if __name__ == '__main__':
    # Only when run directly: this module is also imported by audit_staleness.py.
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    main()
