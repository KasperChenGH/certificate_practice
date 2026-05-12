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
                'origin': f'{cat}｜第 {q["qnum"]} 題',
            })
    # Clean up temp file
    tmp = REPO/'_tmp_bank.jsonl'
    if tmp.exists(): tmp.unlink()
    return out

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

def main():
    print('Building futures...')
    futures = dedup(build_futures())
    print(f'  -> {len(futures)} unique futures questions')

    print('Building securities...')
    securities = dedup(build_securities())
    print(f'  -> {len(securities)} unique securities questions')

    print('Building finance_ethics...')
    finance_ethics = dedup(build_finance_ethics())
    print(f'  -> {len(finance_ethics)} unique finance_ethics questions')

    data = {
        'futures': futures,
        'securities': securities,
        'finance_ethics': finance_ethics,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    sz = OUT.stat().st_size
    print(f'\nWrote {OUT} ({sz} bytes, {sz/1024:.1f} KB)')

if __name__ == '__main__':
    main()
