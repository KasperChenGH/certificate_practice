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

CJK = re.compile(r'[一-鿿]')
# 均給分 / 送分 mark a question the examiner later accepted several answers for.
# The PDFs space these characters irregularly ('均給 分'), so match tolerantly.
DISPUTE = re.compile(r'均\s*給\s*分|一律\s*給\s*分|皆\s*給\s*分|送\s*分')
DISPUTE_NUM = re.compile(r'第?\s*(\d+)\s*題?[^0-9]{0,60}?(?:均\s*給\s*分|送\s*分)')
# Some keys print a corrected answer in the grid cell itself: '51 修正為B'.
# That is still one answer, so it is applied rather than treated as disputed.
CORRECTION = re.compile(r'(\d+)\s*修正\s*為\s*\(?([A-D])\)?')
# Wording that only ever appears in an errata footnote. A block carrying any of it
# is prose even when digits and letters inside it would tokenise as answers.
PROSE = re.compile(r'公告|審閱|委員|確認|說明|備註|注意')

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


SUBJECT_RE = re.compile(r'^(?:專業)?科目\s*[：:]\s*(.+?)\s*$')


def _subject_section(lines: list[str], subject: str, pdf_path: str) -> list[str]:
    """Narrow `lines` to the one 科目 section whose heading names `subject`.

    A paper carrying several subjects restarts numbering at 1 for each, so reading
    from the top always yields the first subject. Papers with a single subject are
    returned unchanged.
    """
    marks = [(i, m.group(1)) for i, l in enumerate(lines)
             if (m := SUBJECT_RE.match(l.strip()))]
    if not marks:
        return lines
    names = list(dict.fromkeys(n for _, n in marks))
    if len(names) == 1:
        return lines

    hits = [n for n in names if subject in n]
    if len(hits) != 1:
        raise ValueError(
            f'{pdf_path}: {subject!r} matches {len(hits)} of the paper\'s subject '
            f'headings ({names}). Pass a subject string that identifies exactly one.')
    want = hits[0]

    start = next(i for i, n in marks if n == want)
    end = next((i for i, n in marks if i > start and n != want), len(lines))
    return lines[start:end]


def parse_questions_pdf(pdf_path: str, session: str, subject: str, expect: int = 50) -> list[dict]:
    """Collect `expect` questions numbered 1..expect from `subject`'s section.

    The cap matters for papers that continue into an essay section whose sub-parts
    are also numbered `N.` and would otherwise be picked up as questions.
    """
    doc = fitz.open(pdf_path)
    lines = ''.join(doc[p].get_text() + '\n' for p in range(len(doc))).split('\n')
    lines = _subject_section(lines, subject, pdf_path)

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

    Returns `(answers, disputed)`. `disputed` holds question numbers the paper's own
    errata note says accept more than one option — they cannot be represented as a
    single key, so the caller drops them rather than picking one.

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
            # "115年第2次 證券交易相關法規與實務乙科資格測驗試題解答" is the paper's
            # title, not a section label. On a single-subject paper it contains the
            # subject name too, so without this it matches before the real label and
            # the grid — which sits after that label — is never reached.
            is_title = bool(re.search(r'\d+\s*年第\s*\d+\s*次', text))
            kind = 'label' if labels and not is_title else 'grid'
            items.append((pno, b[1], b[0], kind, text, labels))
    items.sort(key=lambda t: (t[0], round(t[1], 1), t[2]))

    # A substring can match more than one section: '財務分析' appears in both
    # '證券投資與財務分析--試卷「投資學」' and '...試卷「財務分析」', which silently
    # paired one subject's questions with another subject's key. Ambiguity is an error.
    all_hits = [l for _, _, _, kind, _, labels in items if kind == 'label'
                for l in labels if subject in l]
    if len(all_hits) > 1:
        raise ValueError(
            f'{pdf_path}: {subject!r} matches {len(all_hits)} answer labels ({all_hits}). '
            'Pass a subject string that identifies exactly one of them.')

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

    grid, disputed, notes = '', set(), []
    # Joined before stripping: a corrected cell can straddle two blocks ('51 修正' /
    # '為B'), so the pattern is only visible once the blocks are back together.
    joined = ' '.join(text for _, _, _, kind, text, _ in items[matched_at + 1:]
                      if kind != 'label')
    corrections = {int(n): a for n, a in CORRECTION.findall(joined)}

    for _, _, _, kind, text, _ in items[matched_at + 1:]:
        if kind == 'label':
            break
        # Prose must not be tokenised as answers: "第36題修正為(A)(B)均給分" would
        # otherwise read as 36 -> A and overwrite the real key. But a grid can carry an
        # inline 均給分 in place of a letter, so record those numbers before deciding.
        disputed.update(int(n) for n in DISPUTE_NUM.findall(text))
        stripped = CJK.sub(' ', text)
        if re.search(r'\d+\s+[A-D]', stripped) and not PROSE.search(text):
            grid += ' ' + stripped
        elif CJK.search(text):
            notes.append(text)
        else:
            grid += ' ' + text

    for note in notes:
        if DISPUTE.search(note) and not DISPUTE_NUM.search(note):
            raise ValueError(
                f'{pdf_path}: the key carries an errata note awarding marks for more '
                f'than one option, but no question number could be read from it: {note!r}')
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
    answers.update(corrections)
    # A disputed question's printed letter is no longer the whole answer, so the
    # key is dropped rather than kept alongside the note that contradicts it.
    for n in disputed:
        answers.pop(n, None)
    expected = [n for n in range(1, max(answers) + 1) if n not in disputed] if answers else []
    if not answers or sorted(answers) != expected:
        raise ValueError(f'{pdf_path}: answer block for {subject!r} is not a gapless run from 1 '
                         f'(disputed and therefore absent: {sorted(disputed) or "none"})')
    return answers, disputed


def parse_paper(qpdf: str, apdf: str, session: str, subject: str, expect: int = 50) -> list[dict]:
    questions = parse_questions_pdf(qpdf, session, subject, expect)
    answers, disputed = parse_answers_by_subject(apdf, subject)
    if disputed:
        # The paper's own errata awards marks for more than one option on these, so
        # there is no single correct answer to key them against. Drop rather than pick.
        print(f'  !! {subject}: dropping question(s) {sorted(disputed)} — the official '
              f'errata accepts more than one option')
        questions = [q for q in questions if q['qnum'] not in disputed]
        expect -= len(disputed)
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
