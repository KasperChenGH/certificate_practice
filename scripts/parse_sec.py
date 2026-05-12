"""
Parse 證券高業 試題 PDFs — each PDF contains 3 papers concatenated:
  1) 投資學  2) 財務分析  3) 證券交易相關法規與實務
Each paper has 50 questions numbered 1..50. We detect paper boundaries when qnum resets.
Pair with answers from 答案 PDF (3 paper × 50 answers each).
"""
from __future__ import annotations
import fitz, re, json, os, sys, io

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

QSTART_RE = re.compile(r'^(\d+)\.(?:\s+(.*))?$')
OPT_RE = re.compile(r'^\(([A-D])\)\s*(.*)$')

PAPER_NAMES = [
    '證券投資與財務分析－試卷「投資學」',
    '證券投資與財務分析－試卷「財務分析」',
    '證券交易相關法規與實務',
]

HEADER_RES = [
    re.compile(r'^\d{2,3}\s*年第\d+次'),
    re.compile(r'^專業科目'),
    re.compile(r'^請填應試號碼'),
    re.compile(r'^※\s*注意'),
    re.compile(r'^第\s*\d+\s*頁'),
]

def _is_header(s: str) -> bool:
    for r in HEADER_RES:
        if r.match(s):
            return True
    if re.fullmatch(r'\d+', s) and len(s) <= 3: return True
    if '反面尚有試題' in s: return True
    if '單一選擇題' in s and len(s) > 20: return True
    return False

def parse_questions_pdf(pdf_path: str, session_label: str) -> list[dict]:
    """Two-pass parser:
       Pass 1: find question boundaries by qnum start-of-line markers; collect raw text per question.
       Pass 2: split each question's raw text into stem + 4 options using ordered (A)(B)(C)(D)."""
    doc = fitz.open(pdf_path)
    full_text = ''
    for p in range(len(doc)):
        full_text += doc[p].get_text() + '\n'
    lines = full_text.split('\n')

    raw_questions = []  # list of {qnum, paper_idx, content_lines}
    cur = None
    paper_idx = 0
    prev_qnum = 0

    for raw in lines:
        s = raw.strip()
        if not s: continue
        if _is_header(s): continue

        mq = QSTART_RE.match(s)
        if mq:
            qn = int(mq.group(1))
            stem_init = (mq.group(2) or '').strip()
            # Detect paper boundary
            if cur and qn == 1 and prev_qnum >= 5:
                paper_idx = min(paper_idx + 1, len(PAPER_NAMES) - 1)
            if cur:
                raw_questions.append(cur)
            cur = {
                'qnum': qn,
                'paper_idx': paper_idx,
                'session': session_label,
                'subject': PAPER_NAMES[paper_idx],
                'content_lines': [stem_init] if stem_init else [],
            }
            prev_qnum = qn
            continue

        if cur:
            cur['content_lines'].append(s)

    if cur:
        raw_questions.append(cur)

    # Pass 2: split each into stem + options
    out = []
    for rq in raw_questions:
        # Concatenate without inserting spaces (Chinese text)
        content = ''.join(rq['content_lines'])
        # Strip trailing footer text that may have leaked in (e.g., "XXX年第X次...資格測驗試題")
        content = re.sub(r'\d{2,3}\s*年第\d+次.*$', '', content)
        stem, opts = split_stem_options_letters(content)
        out.append({
            'qnum': rq['qnum'],
            'paper_idx': rq['paper_idx'],
            'session': rq['session'],
            'subject': rq['subject'],
            'stem': stem,
            'options': opts,
        })
    return out

def split_stem_options_letters(content: str) -> tuple[str, dict]:
    """Find (A),(B),(C),(D) in order and split."""
    cursor = 0
    boundaries = []
    for letter in 'ABCD':
        target = f'({letter})'
        idx = content.find(target, cursor)
        if idx < 0:
            break
        boundaries.append((letter, idx))
        cursor = idx + len(target)
    if not boundaries:
        return content.strip(), {'A': '', 'B': '', 'C': '', 'D': ''}
    stem = content[:boundaries[0][1]].strip()
    opts = {'A': '', 'B': '', 'C': '', 'D': ''}
    for bi, (letter, pos) in enumerate(boundaries):
        opt_start = pos + 3
        opt_end = boundaries[bi+1][1] if bi+1 < len(boundaries) else len(content)
        opts[letter] = content[opt_start:opt_end].strip()
    return stem, opts

def parse_answers_pdf(pdf_path: str) -> list[list[str]]:
    """Return 3 lists of 50 answer letters each."""
    doc = fitz.open(pdf_path)
    text = ''
    for p in range(len(doc)):
        text += doc[p].get_text() + '\n'
    tokens = re.findall(r'(?:\d+|[A-D])', text)
    pairs = []
    i = 0
    while i+1 < len(tokens):
        if tokens[i].isdigit() and tokens[i+1] in 'ABCD':
            pairs.append((int(tokens[i]), tokens[i+1]))
            i += 2
        else:
            i += 1
    # Detect paper boundaries: when qnum == 1 and prev qnum was high.
    papers = [{}, {}, {}]
    paper_idx = 0
    prev = 0
    for q, a in pairs:
        if q == 1 and prev >= 5:
            paper_idx = min(paper_idx + 1, 2)
        papers[paper_idx][q] = a
        prev = q
    return [[p.get(i, '?') for i in range(1, 51)] for p in papers]

def merge_qa(questions: list[dict], answers: list[list[str]]) -> list[dict]:
    out = []
    for q in questions:
        pi = q['paper_idx']
        idx = q['qnum'] - 1
        if 0 <= pi < len(answers) and 0 <= idx < len(answers[pi]):
            q['answer'] = answers[pi][idx]
        else:
            q['answer'] = '?'
        out.append(q)
    return out

if __name__ == '__main__':
    sessions = [
        ('115年第1次', '_raw/sec/115Q1_投資學_試題.pdf', '_raw/sec/115Q1_答案.pdf'),
        ('114年第3次', '_raw/sec/114Q3_投資學_試題.pdf', '_raw/sec/114Q3_答案.pdf'),
    ]
    all_q = []
    for label, qpdf, apdf in sessions:
        qs = parse_questions_pdf(qpdf, label)
        ans = parse_answers_pdf(apdf)
        qs = merge_qa(qs, ans)
        print(f'\n{label}: {len(qs)} questions')
        from collections import Counter
        per_paper = Counter(q['paper_idx'] for q in qs)
        for pi in sorted(per_paper.keys()):
            print(f'  paper {pi} ({PAPER_NAMES[pi]}): {per_paper[pi]} q, answers={len(ans[pi])}')
        all_q.extend(qs)
    with open('_build/sec.jsonl', 'w', encoding='utf-8') as f:
        for q in all_q:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    print(f'\nWrote {len(all_q)} → _build/sec.jsonl')
