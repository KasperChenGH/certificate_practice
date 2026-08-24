"""Assemble the hand-authored CFA Level I FRA bank into `../sources/cfa_fra.json`.

Unlike the other three banks, the CFA questions are not parsed from a PDF — they are
authored directly. This script validates them (unique stems, valid answer key, an
explanation for every option) and writes the canonical `sources/cfa_fra.json` that
`build.py` folds into `questions.json`.

Usage:
    python scripts/build_cfa.py <batch1.json> [<batch2.json> ...]

Each input file is a JSON array of objects with keys:
    sub, stem, options {A,B,C}, answer, explanations {A,B,C}

Running it with no arguments simply re-validates the existing `sources/cfa_fra.json`.
"""
from __future__ import annotations
import json, sys, io, hashlib, random
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / 'sources' / 'cfa_fra.json'


def validate(questions: list[dict]) -> None:
    seen_stems: dict[str, int] = {}
    for i, q in enumerate(questions, 1):
        letters = sorted(q['options'].keys())
        if letters != ['A', 'B', 'C']:
            raise ValueError(f'Q{i}: expected options A/B/C, got {letters}')
        if q['answer'] not in q['options']:
            raise ValueError(f'Q{i}: answer {q["answer"]!r} is not one of the options')
        if sorted(q['explanations'].keys()) != letters:
            raise ValueError(f'Q{i}: explanations must cover every option')
        for k, v in q['options'].items():
            if not str(v).strip():
                raise ValueError(f'Q{i}: option {k} is empty')
        for k, v in q['explanations'].items():
            if not str(v).strip():
                raise ValueError(f'Q{i}: explanation {k} is empty')
        fp = hashlib.sha1(''.join(q['stem'].split()).encode()).hexdigest()
        if fp in seen_stems:
            raise ValueError(f'Q{i}: duplicate stem, already used by Q{seen_stems[fp]}')
        seen_stems[fp] = i


LETTERS = ('A', 'B', 'C')
BALANCE_SEED = 20260824


def balance_answer_key(questions: list[dict]) -> None:
    """Rotate each question's options so correct answers spread evenly over A/B/C.

    Written by hand, the bank came out heavily skewed toward A (291/216/7 of 514),
    which lets a candidate guess well without knowing the material. Each question's
    three options are cyclically rotated — preserving their relative order — until
    the key lands on an assigned target letter. Targets are a balanced list shuffled
    with a fixed seed, so the result is deterministic but carries no visible pattern.
    """
    targets = [LETTERS[i % 3] for i in range(len(questions))]
    random.Random(BALANCE_SEED).shuffle(targets)
    for q, target in zip(questions, targets):
        shift = (LETTERS.index(target) - LETTERS.index(q['answer'])) % 3
        if not shift:
            continue
        opts, expl = q['options'], q['explanations']
        q['options'] = {LETTERS[(i + shift) % 3]: opts[L] for i, L in enumerate(LETTERS)}
        q['explanations'] = {LETTERS[(i + shift) % 3]: expl[L] for i, L in enumerate(LETTERS)}
        q['answer'] = target


def assemble(paths: list[Path]) -> list[dict]:
    raw: list[dict] = []
    for p in paths:
        raw.extend(json.loads(p.read_text(encoding='utf-8')))
    validate(raw)
    balance_answer_key(raw)
    out = []
    for i, q in enumerate(raw, 1):
        out.append({
            'id': f'cfa_fra-{i}',
            'topic': 'cfa_fra',
            'stem': q['stem'],
            'options': q['options'],
            'answer': q['answer'],
            'origin': f'CFA Level I | FRA | {q["sub"]}',
            'explanations': q['explanations'],
        })
    return out


def main() -> None:
    args = sys.argv[1:]
    if args:
        questions = assemble([Path(a) for a in args])
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(questions, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'Wrote {OUT} ({len(questions)} questions)')
    else:
        questions = json.loads(OUT.read_text(encoding='utf-8'))
        validate(questions)
        print(f'{OUT} validates: {len(questions)} questions')

    by_sub: dict[str, int] = {}
    by_key: dict[str, int] = {}
    for q in questions:
        by_sub[q['origin']] = by_sub.get(q['origin'], 0) + 1
        by_key[q['answer']] = by_key.get(q['answer'], 0) + 1
    for k in sorted(by_sub):
        print(f'  {by_sub[k]:3d}  {k}')
    print('answer key:', ' '.join(f'{k}={by_key.get(k, 0)}' for k in LETTERS))


if __name__ == '__main__':
    main()
