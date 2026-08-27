"""Rebuild `questions.json` from the source PDFs in `../sources/`.

Run from the repo root:
    python scripts/build.py

Or from anywhere:
    python /path/to/repo/scripts/build.py

Outputs `questions.json` at the repo root (next to index.html).
"""
from __future__ import annotations
import json, os, re, sys, io, hashlib, importlib.util
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / 'sources'
SCRIPTS = REPO / 'scripts'
OUT = REPO / 'questions.json'

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

parse_bank = _load('parse_bank', SCRIPTS / 'parse_bank.py')
parse_sec = _load('parse_sec', SCRIPTS / 'parse_sec.py')
parse_paper = _load('parse_paper', SCRIPTS / 'parse_paper.py')

# --- 1. Futures: parse from the existing dedup answers PDF -----------------

def build_futures() -> list[dict]:
    """Parse `futures_exam_dedup_answers.pdf` directly (logic from
    parse_futures_from_answers.py)."""
    import fitz
    pdf = SRC / 'futures_exam_dedup_answers.pdf'
    doc = fitz.open(pdf)
    text = ''.join(doc[p].get_text() + '\n' for p in range(len(doc)))
    blocks = re.split(r'(?m)^第\s*(\d+)\s*題\s*$', text)
    questions = []
    for i in range(1, len(blocks), 2):
        qnum = int(blocks[i])
        body = re.sub(r'(?m)^第\s*\d+\s*頁\s*$', '', blocks[i+1] if i+1 < len(blocks) else '').strip()
        m_ans = re.search(r'答案\s*\n([A-D])\b', body)
        m_orig = re.search(r'原始對應\s*\n([^\n]+)', body)
        if not (m_ans and m_orig): continue
        m_stem = re.search(r'題目[：:](.*?)\(A\)', body, re.DOTALL)
        if not m_stem: continue
        stem = re.sub(r'\s+', '', m_stem.group(1))
        opts_text = body[body.index('(A)'):]
        bounds = []
        cursor = 0
        for letter in 'ABCD':
            idx = opts_text.find(f'({letter})', cursor)
            if idx < 0: break
            bounds.append((letter, idx))
            cursor = idx + 3
        opts = {'A':'','B':'','C':'','D':''}
        for k, (letter, pos) in enumerate(bounds):
            end = bounds[k+1][1] if k+1 < len(bounds) else len(opts_text)
            opts[letter] = re.sub(r'\s+', '', opts_text[pos+3:end])
        # Hard-coded patch for one malformed entry (missing "(" before "B)")
        if qnum == 432 and not opts.get('B'):
            opts = {
                'A': '交割結算基金餘額之百分之三十',
                'B': '交割結算基金全年提列金額之百分之五十',
                'C': '交割結算基金餘額之百分之五十',
                'D': '交割結算基金全年提列金額之百分之三十',
            }
        questions.append({
            'id': f'futures-{qnum}',
            'topic': 'futures',
            'stem': stem,
            'options': opts,
            'answer': m_ans.group(1),
            'origin': m_orig.group(1).strip(),
        })
    return questions

# --- 1b. Single-subject papers (sources/papers/) ----------------------------

PAPERS = SRC / 'papers'

def _papers(topic: str, subject: str, sessions: list[tuple[str, str]]) -> list[dict]:
    """Parse one subject across sessions. `sessions` is [(label, filename stem)]."""
    out = []
    for label, base in sessions:
        qs = parse_paper.parse_paper(
            str(PAPERS / f'{base}_試題.pdf'), str(PAPERS / f'{base}_答案.pdf'),
            label, subject)
        for q in qs:
            out.append({
                'id': f'{topic}-{base}-{q["qnum"]}',
                'topic': topic,
                'stem': q['stem'],
                'options': q['options'],
                'answer': q['answer'],
                'origin': f'{label}｜{subject}｜第 {q["qnum"]} 題',
            })
    return out


def build_futures_papers() -> list[dict]:
    return _papers('futures', '期貨交易法規',
                   [('115年第1次', '115Q1_期貨交易法規'),
                    ('114年第3次', '114Q3_期貨交易法規')])


def build_securities_rep() -> list[dict]:
    return _papers('securities_rep', '證券交易相關法規與實務',
                   [('115年第1次', '115Q1_證券商業務員'),
                    ('114年第3次', '114Q3_證券商業務員')])


def build_sitca() -> list[dict]:
    return _papers('sitca', '投信投顧相關法規',
                   [('115年第1次', '115Q1_投信投顧'),
                    ('114年第3次', '114Q3_投信投顧')])


# --- 2. Securities Senior: parse 試題 + 答案 PDFs ----------------------------

def build_securities() -> list[dict]:
    sessions = [
        ('115年第1次', SRC/'sec/115Q1_投資學_試題.pdf', SRC/'sec/115Q1_答案.pdf'),
        ('114年第3次', SRC/'sec/114Q3_投資學_試題.pdf', SRC/'sec/114Q3_答案.pdf'),
    ]
    out = []
    PAPER_SHORT = ['投資學', '財務分析', '法規與實務']
    for label, qpdf, apdf in sessions:
        qs = parse_sec.parse_questions_pdf(str(qpdf), label)
        answers = parse_sec.parse_answers_pdf(str(apdf))
        qs = parse_sec.merge_qa(qs, answers)
        for q in qs:
            short = PAPER_SHORT[q['paper_idx']]
            out.append({
                'id': f'securities-{label}-p{q["paper_idx"]}-{q["qnum"]}',
                'topic': 'securities',
                'stem': q['stem'],
                'options': q['options'],
                'answer': q['answer'],
                'origin': f'{label}｜{short}｜第 {q["qnum"]} 題',
            })
    return out

# --- 3. Finance + Ethics: parse two SFI bank PDFs ---------------------------

def build_finance_ethics() -> list[dict]:
    """The SFI 1,120-question official bank, effective 113年9月1日.

    Two subjects: 金融市場常識 and 職業道德.
    """
    out = []
    DIGIT2LETTER = {'1':'A','2':'B','3':'C','4':'D'}
    for path, cat in [(SRC/'sfi_金融市場常識-113.pdf', '金融市場常識'),
                      (SRC/'sfi_職業道德-113.pdf', '職業道德')]:
        qs = parse_bank.parse_pdf(str(path), cat, str(REPO/'_tmp_bank.jsonl'))
        for q in qs:
            opts = q['options']
            if isinstance(opts, list):
                opts = {'A':opts[0], 'B':opts[1], 'C':opts[2], 'D':opts[3]}
            out.append({
                'id': f'finance_ethics-{cat}-{q["qnum"]}',
                'topic': 'finance_ethics',
                'stem': q['stem'],
                'options': opts,
                'answer': DIGIT2LETTER.get(str(q['answer']), q['answer']),
                'origin': f'113年9月版｜{cat}｜第 {q["qnum"]} 題',
            })
    # Clean up temp file
    tmp = REPO/'_tmp_bank.jsonl'
    if tmp.exists(): tmp.unlink()
    return out

# --- 4. CFA Level I FRA: hand-authored bank (not parsed from a PDF) ---------

def build_cfa_fra() -> list[dict]:
    """Load `sources/cfa_fra.json`, which is authored directly rather than parsed.

    Regenerate/validate it with `python scripts/build_cfa.py`.
    """
    path = SRC / 'cfa_fra.json'
    if not path.exists():
        print('  !! sources/cfa_fra.json missing - skipping cfa_fra')
        return []
    return json.loads(path.read_text(encoding='utf-8'))

# --- Dedup + assemble ------------------------------------------------------

def _norm(s: str) -> str:
    return re.sub(r'\s+', '', s or '')

def _fp(q: dict) -> str:
    text = _norm(q['stem']) + '|' + '|'.join(_norm(q['options'].get(k,'')) for k in 'ABCD')
    return hashlib.sha1(text.encode()).hexdigest()

def dedup(qs: list[dict]) -> list[dict]:
    seen = {}
    for q in qs:
        seen.setdefault(_fp(q), q)
    return list(seen.values())

STEM_OVERRIDES = SRC / 'stem_overrides.json'
BLUEPRINTS_IN = SRC / 'exam_blueprints.json'
BLUEPRINTS_OUT = REPO / 'blueprints.json'


def tag_subjects(data: dict) -> None:
    """Copy the subject out of `origin` into its own field.

    The Taiwan banks use '112 年第1 次｜期貨交易法規｜第 5 題' and the CFA bank uses
    'CFA Level I | FRA | Income Statement'. Both put the subject in the middle field.
    The app needs it to compose a paper by subject, and parsing it in JS would put the
    origin format in two places.
    """
    for qs in data.values():
        for q in qs:
            origin = q.get('origin', '')
            sep = '｜' if '｜' in origin else ('|' if '|' in origin else None)
            if not sep:
                continue
            parts = [x.strip() for x in origin.split(sep)]
            if len(parts) == 3:
                q['subject'] = parts[2] if sep == '|' else parts[1]


COVERAGE = SRC / 'explanation_coverage.json'
# Below this pool-to-draw ratio a paper cannot vary much: at 2.0x two consecutive
# sittings exhaust the pool, so half of every paper is a question you just saw.
THIN_RATIO = 3.0


def check_explanation_coverage(data: dict, accept_drop: bool = False) -> None:
    """Fail if a bank comes back with fewer explanations than it last shipped.

    carry_over_explanations reads the previous questions.json, so a bank that is
    absent from it for even one commit loses every explanation on the next rebuild
    with no error — that is how 1,120 finance_ethics explanations were nearly lost.
    Comparing against the last build does not catch it, because by then the bank had
    been gone for several commits. So the baseline is committed and entries for banks
    that are not in the current build are kept, which is what makes retiring a bank
    and restoring it later safe.

    Pass --accept-coverage-drop to record a drop you actually intend.
    """
    current = {t: sum(1 for q in qs if q.get('explanations')) for t, qs in data.items()}
    baseline = json.loads(COVERAGE.read_text(encoding='utf-8')) if COVERAGE.exists() else {}

    dropped = [(t, baseline[t], current[t]) for t in current
               if t in baseline and current[t] < baseline[t]]
    if dropped and not accept_drop:
        lines = '\n'.join(f'    {t}: {was} -> {now}  (lost {was - now})'
                           for t, was, now in dropped)
        raise ValueError(
            'explanation coverage went backwards:\n' + lines +
            '\n  These are not reproducible from the source PDFs. Recover them from git\n'
            "  (git show <commit>:questions.json), re-attach by question id where the\n"
            '  answer key still agrees, then rebuild. If the drop is intended, rerun\n'
            '  with --accept-coverage-drop.')

    # Keep baselines for banks not in this build, so a retired bank is still protected.
    baseline.update(current)
    COVERAGE.write_text(json.dumps(baseline, ensure_ascii=False, indent=1) + '\n',
                        encoding='utf-8')
    total = sum(current.values())
    print(f'Explanation coverage: {total} / {sum(len(v) for v in data.values())}'
          + (f'  (accepted a drop in {len(dropped)} bank(s))' if dropped else ''))


def write_blueprints(data: dict) -> None:
    """Validate sources/exam_blueprints.json against the built banks, then emit it.

    A subject name that does not match the data, or a section asking for more
    questions than exist, would silently yield a short or empty section at quiz time.
    Both are build failures instead.

    Filling the paper is not the same as being able to vary it. A subject drawing 50
    from a pool of 97 repeats about half of every paper, so a subject thinner than
    THIN_RATIO must be listed in the blueprint file's `_thin_ok`. Known-thin subjects
    warn; a newly thin one fails, which is what stops a section from quietly becoming
    unpracticable when a paper is added or a draw is enlarged.
    """
    if not BLUEPRINTS_IN.exists():
        print('  !! sources/exam_blueprints.json missing - skipping blueprints')
        return
    raw = json.loads(BLUEPRINTS_IN.read_text(encoding='utf-8'))
    blueprints = {k: v for k, v in raw.items() if not k.startswith('_')}
    thin_ok = set(raw.get('_thin_ok', []))
    known_thin, new_thin = [], []

    for topic, bp in blueprints.items():
        if topic not in data:
            raise ValueError(f'exam_blueprints.json: no bank named {topic!r}')
        available = {}
        for q in data[topic]:
            available[q.get('subject')] = available.get(q.get('subject'), 0) + 1
        for sec in bp['subjects']:
            have = available.get(sec['subject'], 0)
            if not have:
                raise ValueError(
                    f'exam_blueprints.json: {topic} has no questions whose subject is '
                    f'{sec["subject"]!r}. Available: {sorted(k for k in available if k)}')
            if have < sec['count']:
                raise ValueError(
                    f'exam_blueprints.json: {topic}/{sec["subject"]} asks for '
                    f'{sec["count"]} questions but only {have} exist')
        total = sum(sec['count'] for sec in bp['subjects'])
        print(f'  {topic}: {total} questions = ' +
              ' + '.join(f'{sec["count"]} {sec["subject"]}' for sec in bp['subjects']))

        # Record the ratio so the thinness is inspectable rather than folklore.
        bp['coverage'] = {
            'pool': len(data[topic]),
            'draw': total,
            'ratio': round(len(data[topic]) / total, 2),
            'subjects': {sec['subject']: {
                'pool': available.get(sec['subject'], 0),
                'draw': sec['count'],
                'ratio': round(available.get(sec['subject'], 0) / sec['count'], 2),
            } for sec in bp['subjects']},
        }
        for sec in bp['subjects']:
            ratio = available.get(sec['subject'], 0) / sec['count']
            if ratio < THIN_RATIO:
                (known_thin if f'{topic}/{sec["subject"]}' in thin_ok
                 else new_thin).append((topic, sec['subject'],
                                        available.get(sec['subject'], 0),
                                        sec['count'], ratio))

    def _fmt(rows):
        return '\n'.join(
            f'    {t}/{sub}: draws {draw} from {pool} ({r:.2f}x) — about '
            f'{min(draw / pool, 1.0):.0%} of each paper repeats the one before'
            for t, sub, pool, draw, r in rows)

    if new_thin:
        raise ValueError(
            f'these subjects draw from a pool thinner than {THIN_RATIO}x:\n'
            + _fmt(new_thin) +
            '\n  Add questions, shrink the draw, or — if the real paper is this size and\n'
            '  the pool is all that exists — list them in _thin_ok in\n'
            '  sources/exam_blueprints.json so the thinness is a recorded decision.')
    if known_thin:
        print(f'  !! thin pools (known, listed in _thin_ok):\n' + _fmt(known_thin))

    BLUEPRINTS_OUT.write_text(json.dumps(blueprints, ensure_ascii=False, indent=1),
                              encoding='utf-8')
    print(f'Wrote {BLUEPRINTS_OUT}')

# A paper presents questions in order; this app shuffles a random subset. Any stem that
# points at another question is unanswerable here and must be rewritten to stand alone.
CROSS_REF_RE = re.compile(r'同上題|承上題|續上題|依上題|接上題|同前題|依前題|上一題|下一題')


def apply_stem_overrides(data: dict) -> None:
    """Rewrite stems listed in sources/stem_overrides.json, then verify none remain.

    Each override asserts the stem it replaces, so a parser change cannot silently
    rewrite the wrong question. After applying them, any remaining cross-reference is
    a hard error: a new paper has introduced one and it needs an override entry.
    """
    overrides = {}
    if STEM_OVERRIDES.exists():
        overrides = {k: v for k, v in
                     json.loads(STEM_OVERRIDES.read_text(encoding='utf-8')).items()
                     if not k.startswith('_')}

    by_id = {q['id']: q for qs in data.values() for q in qs}
    applied = 0
    for qid, spec in overrides.items():
        q = by_id.get(qid)
        if q is None:
            raise ValueError(
                f'stem_overrides.json: {qid} is not in the build. It may have been '
                'deduped away or renumbered — re-check the override.')
        if q['stem'] == spec['stem']:
            continue                      # already applied upstream; nothing to do
        if q['stem'] != spec['was']:
            raise ValueError(
                f'stem_overrides.json: {qid} no longer matches the recorded original.\n'
                f'  expected: {spec["was"]!r}\n  parsed:   {q["stem"]!r}')
        q['stem'] = spec['stem']
        applied += 1
    print(f'Applied {applied} stem override(s)')

    stragglers = [(q['id'], q['stem'][:60]) for qs in data.values() for q in qs
                  if CROSS_REF_RE.search(q['stem']) and q['id'] not in overrides]
    if stragglers:
        lines = '\n'.join(f'  {i}: {t}' for i, t in stragglers)
        raise ValueError(
            'These stems reference another question, which breaks once the quiz '
            'shuffles. Add a self-contained rewrite to sources/stem_overrides.json:\n'
            + lines)


# The instruction line that opens each paper ("本測驗為單一選擇題,請依題意選出一個正確
# 或最適當的答案"), sometimes preceded by the session title, sits directly below the last
# option of the preceding page. Every extractor here reads it as part of option (D) of
# question 50, so the text is stripped after parsing rather than in each parser.
HEADER_BLEED = re.compile(
    r'(?:\d+\s*年第\s*\d+\s*次.{0,40}?試題)?'   # optional session title
    r'\s*(?:本測驗)?\s*[為一]?\s*(?:單一)?\s*'
    r'選擇題\s*[，,]\s*請依題意選出一個正確或最適當的答案\s*$')


def strip_header_bleed(data: dict) -> None:
    """Remove the next page's instruction line from the end of an option."""
    fixed = 0
    for qs in data.values():
        for q in qs:
            for k, v in q['options'].items():
                clean = HEADER_BLEED.sub('', v).strip()
                if clean != v:
                    if not clean:
                        raise ValueError(
                            f'{q["id"]} option {k}: stripping the header bleed would '
                            f'empty the option — the pattern is too greedy for {v!r}')
                    q['options'][k] = clean
                    fixed += 1
    print(f'Stripped page-header bleed from {fixed} options')


def carry_over_explanations(data: dict) -> None:
    """Re-attach `explanations` from the existing questions.json.

    The per-option explanations were generated once (see `_expl_work/`) and are not
    reproducible from the source PDFs, so a rebuild must not drop them.
    """
    if not OUT.exists():
        return
    prev = json.loads(OUT.read_text(encoding='utf-8'))
    by_id, by_fp = {}, {}
    for qs in prev.values():
        for q in qs:
            if q.get('explanations'):
                by_id[q['id']] = (q['answer'], q['explanations'])
                by_fp[_fp(q)] = q['explanations']
    kept = 0
    for qs in data.values():
        for q in qs:
            if q.get('explanations'):
                continue
            # Match on id first: a stem override (see apply_stem_overrides) changes the
            # text and therefore the fingerprint, but the question is the same one. The
            # answer key must agree, so an explanation can never be attached to a
            # question whose correct option has moved.
            hit = by_id.get(q['id'])
            if hit and hit[0] == q['answer']:
                q['explanations'] = hit[1]
                kept += 1
            elif _fp(q) in by_fp:
                q['explanations'] = by_fp[_fp(q)]
                kept += 1
    print(f'Carried over explanations for {kept} questions')


def main():
    print('Building futures...')
    futures = dedup(build_futures() + build_futures_papers())
    print(f'  -> {len(futures)} unique futures questions')

    print('Building securities...')
    securities = dedup(build_securities())
    print(f'  -> {len(securities)} unique securities questions')

    print('Building finance_ethics...')
    finance_ethics = dedup(build_finance_ethics())
    print(f'  -> {len(finance_ethics)} unique finance_ethics questions')

    print('Building securities_rep...')
    securities_rep = dedup(build_securities_rep())
    print(f'  -> {len(securities_rep)} unique securities_rep questions')

    print('Building sitca...')
    sitca = dedup(build_sitca())
    print(f'  -> {len(sitca)} unique sitca questions')

    print('Loading cfa_fra...')
    cfa_fra = build_cfa_fra()
    print(f'  -> {len(cfa_fra)} cfa_fra questions')

    data = {
        'futures': futures,
        'securities': securities,
        'securities_rep': securities_rep,
        'finance_ethics': finance_ethics,
        'sitca': sitca,
        'cfa_fra': cfa_fra,
    }
    apply_stem_overrides(data)
    strip_header_bleed(data)
    tag_subjects(data)
    carry_over_explanations(data)
    check_explanation_coverage(data, accept_drop='--accept-coverage-drop' in sys.argv)
    print('Blueprints...')
    write_blueprints(data)

    OUT.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    sz = OUT.stat().st_size
    print(f'\nWrote {OUT} ({sz} bytes, {sz/1024:.1f} KB)')

if __name__ == '__main__':
    main()
