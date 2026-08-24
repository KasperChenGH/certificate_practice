"""Parse a single-subject SFI exam paper (50 multiple-choice questions) + its answer PDF.

`parse_sec.py` handles the 證券高業 PDFs, which concatenate three papers and whose
answer PDF is one sequential block per paper. The papers in `sources/papers/` are
different: each 試題 PDF holds one subject, but each 答案 PDF holds the answer keys
for *every* subject in that session's exam. Picking the wrong block would silently
attach a valid-looking but wrong key to every question, so the block is selected by
its printed subject label rather than by position.

Answer PDFs lay out, top to bottom: a session title, then for each subject a label
line ("期貨交易法規試題解答") followed by a grid of number/letter pairs. Labels and
grids are extracted with coordinates and matched by vertical order, so the mapping
from subject to key is read off the document instead of assumed.

Papers whose answer PDF puts two subjects side by side in one two-column grid
(證券投資分析人員) are NOT supported — `parse_answers_by_subject` raises rather than
guess. See `sources/papers/README.md`.
"""
from __future__ import annotations
import fitz, re, sys, io

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

QSTART_RE = re.compile(r'^(\d+)\.(?:\s+(.*))?$')
LABEL_RE = re.compile(r'(試題解答|試題答案)\s*$')

HEADER_RES = [
    re.compile(r'^\d{2,3}\s*年第\d+\s*次'),
    re.compile(r'^專業科目'),
    re.compile(r'^請填應試號碼'),
    re.compile(r'^※\s*注意'),
    re.compile(r'^第\s*\d+\s*頁'),
    re.compile(r'^\(\s*\d+\s*\)'),
]


def _is_header(s: str) -> bool:
    if any(r.match(s) for r in HEADER_RES):
        return True
    if re.fullmatch(r'\d{1,3}', s):
        return True
    if '反面尚有試題' in s or '以下空白' in s or '試題隨卷繳回' in s:
        return True
    if '單一選擇題' in s and len(s) > 20:
        return True
    return False


def parse_questions_pdf(pdf_path: str, session: str, subject: str, expect: int = 50) -> list[dict]:
    """Collect `expect` questions numbered 1..expect, then stop.

    The cap matters for papers that continue into an essay section whose sub-parts
    are also numbered `N.` and would otherwise be picked up as questions.
    """
    doc = fitz.open(pdf_path)
    lines = ''.join(doc[p].get_text() + '\n' for p in range(len(doc))).split('\n')

    raw: list[dict] = []
    cur: dict | None = None
    for line in lines:
        s = line.strip()
        if not s or _is_header(s):
            continue
        mq = QSTART_RE.match(s)
        if mq:
            qn = int(mq.group(1))
            # Stop at the first number that restarts or overruns the expected range.
            if qn > expect or (cur and qn <= cur['qnum']):
                break
            if cur:
                raw.append(cur)
            cur = {'qnum': qn, 'lines': [(mq.group(2) or '').strip()]}
            continue
        if cur:
            cur['lines'].append(s)
    if cur:
        raw.append(cur)

    out = []
    for rq in raw:
        content = re.sub(r'\d{2,3}\s*年第\d+\s*次.*$', '', ''.join(rq['lines']))
        stem, opts = _split_stem_options(content)
        out.append({
            'qnum': rq['qnum'], 'session': session, 'subject': subject,
            'stem': stem, 'options': opts,
        })
    return out


def _split_stem_options(content: str) -> tuple[str, dict]:
    cursor, bounds = 0, []
    for letter in 'ABCD':
        idx = content.find(f'({letter})', cursor)
        if idx < 0:
            break
        bounds.append((letter, idx))
        cursor = idx + 3
    opts = {'A': '', 'B': '', 'C': '', 'D': ''}
    if not bounds:
        return content.strip(), opts
    for i, (letter, pos) in enumerate(bounds):
        end = bounds[i + 1][1] if i + 1 < len(bounds) else len(content)
        opts[letter] = content[pos + 3:end].strip()
    return content[:bounds[0][1]].strip(), opts


def parse_answers_by_subject(pdf_path: str, subject: str) -> dict[int, str]:
    """Return {question number: answer letter} for the block labelled `subject`.

    Raises if the label is missing, if two labels share a line (a side-by-side
    two-column key that cannot be split by vertical position), or if the matched
    block does not yield a gapless run starting at 1.
    """
    doc = fitz.open(pdf_path)
    items = []  # (page, y, x, kind, text)
    for pno in range(len(doc)):
        for b in doc[pno].get_text('blocks'):
            text = re.sub(r'\s+', ' ', b[4]).strip()
            if not text:
                continue
            labels = [m.strip() for m in re.findall(r'[^\s]*?(?:試題解答|試題答案)', text)]
            kind = 'label' if labels else 'grid'
            items.append((pno, b[1], b[0], kind, text, labels))
    items.sort(key=lambda t: (t[0], round(t[1], 1), t[2]))

    matched_at = None
    for i, (_, _, _, kind, text, labels) in enumerate(items):
        if kind != 'label':
            continue
        hits = [l for l in labels if subject in l]
        if not hits:
            continue
        if len(labels) > 1:
            raise ValueError(
                f'{pdf_path}: label line carries {len(labels)} subjects ({labels}); '
                'the key is laid out in side-by-side columns and cannot be split by '
                'vertical position. Refusing to guess.')
        matched_at = i
        break
    if matched_at is None:
        raise ValueError(f'{pdf_path}: no answer block labelled with {subject!r}')

    grid = ''
    for _, _, _, kind, text, _ in items[matched_at + 1:]:
        if kind == 'label':
            break
        grid += ' ' + text
    if not grid.strip():
        raise ValueError(f'{pdf_path}: subject {subject!r} label found but no grid follows it')

    toks = re.findall(r'\d+|[A-D]', grid)
    answers: dict[int, str] = {}
    i = 0
    while i + 1 < len(toks):
        if toks[i].isdigit() and toks[i + 1] in 'ABCD':
            answers[int(toks[i])] = toks[i + 1]
            i += 2
        else:
            i += 1
    if not answers or sorted(answers) != list(range(1, max(answers) + 1)):
        raise ValueError(f'{pdf_path}: answer block for {subject!r} is not a gapless run from 1')
    return answers


def parse_paper(qpdf: str, apdf: str, session: str, subject: str, expect: int = 50) -> list[dict]:
    questions = parse_questions_pdf(qpdf, session, subject, expect)
    answers = parse_answers_by_subject(apdf, subject)
    if len(questions) != expect:
        raise ValueError(f'{qpdf}: parsed {len(questions)} questions, expected {expect}')
    missing = [q['qnum'] for q in questions if q['qnum'] not in answers]
    if missing:
        raise ValueError(f'{qpdf}: no answer for question numbers {missing}')
    blank = [q['qnum'] for q in questions
             if not q['stem'] or not all(q['options'].get(k) for k in 'ABCD')]
    if blank:
        raise ValueError(f'{qpdf}: empty stem or option in question numbers {blank}')
    for q in questions:
        q['answer'] = answers[q['qnum']]
    return questions
