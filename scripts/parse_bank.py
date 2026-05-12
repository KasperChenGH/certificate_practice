"""
Parse a SFI question bank PDF using PyMuPDF (no OCR needed).
Layout: each question = answer marker `(N)` at left, qnum on same row at next x,
then stem + (1)opt1(2)opt2(3)opt3(4)opt4 spanning multiple lines.

PyMuPDF reports line bboxes whose y0 differs slightly between fonts on the same
visual row — so we cluster lines into ROWS by proximity, then sort within row by x.
"""
from __future__ import annotations
import fitz, re, json, os, sys, io

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ANSWER_RE = re.compile(r'^\((\d)\)\s*$')
QNUM_RE = re.compile(r'^(\d+)\s*$')
QNUM_PREFIX_RE = re.compile(r'^(\d+)\s+')  # for items like "10 下列何者..."
OPT_SPLIT = re.compile(r'\((\d)\)')

def collect_lines(page: fitz.Page) -> list[dict]:
    out = []
    for b in page.get_text('dict')['blocks']:
        for ln in b.get('lines', []):
            if not ln['spans']: continue
            text = ''.join(s['text'] for s in ln['spans']).strip()
            if not text: continue
            out.append({
                'y': ln['bbox'][1],
                'y_bottom': ln['bbox'][3],
                'x': ln['bbox'][0],
                'text': text,
            })
    return out

def cluster_rows(lines: list[dict], row_tol: float = 5.0) -> list[list[dict]]:
    """Group lines whose y-centers are within row_tol points into the same row."""
    if not lines: return []
    items = sorted(lines, key=lambda l: l['y'])
    rows = [[items[0]]]
    for ln in items[1:]:
        # use y_bottom of the current cluster's leading line as reference
        last_row = rows[-1]
        ref_y = min(r['y'] for r in last_row)
        if abs(ln['y'] - ref_y) <= row_tol:
            last_row.append(ln)
        else:
            rows.append([ln])
    for r in rows:
        r.sort(key=lambda l: l['x'])
    return rows

def parse_page(page: fitz.Page) -> list[dict]:
    lines = collect_lines(page)
    rows = cluster_rows(lines)
    # Now find rows whose first item is an answer marker at left margin
    questions = []
    i = 0
    while i < len(rows):
        row = rows[i]
        first = row[0]
        m = ANSWER_RE.match(first['text'])
        if not m or first['x'] > 85:
            i += 1
            continue
        answer = m.group(1)
        # qnum: any other item in this row matching `\d+` (standalone)
        # OR a leading `\d+ ` prefix on a longer text item.
        qnum = None
        rest_of_row_text = []
        for item in row[1:]:
            qm = QNUM_RE.match(item['text'])
            if qm and qnum is None:
                qnum = int(qm.group(1))
                continue
            pm = QNUM_PREFIX_RE.match(item['text'])
            if pm and qnum is None:
                qnum = int(pm.group(1))
                # keep the rest of this item's text after the qnum prefix
                stripped = item['text'][pm.end():]
                if stripped:
                    rest_of_row_text.append(stripped)
                continue
            rest_of_row_text.append(item['text'])
        # If qnum still None, check next row's leftmost item
        if qnum is None and i+1 < len(rows):
            nxt = rows[i+1]
            for item in nxt:
                qm = QNUM_RE.match(item['text'])
                if qm:
                    qnum = int(qm.group(1))
                    break
                pm = QNUM_PREFIX_RE.match(item['text'])
                if pm:
                    qnum = int(pm.group(1))
                    break
        # content: rest_of_row_text plus all subsequent rows until next answer-row
        content_parts = list(rest_of_row_text)
        j = i + 1
        while j < len(rows):
            r = rows[j]
            r_first = r[0]
            # is this an answer row?
            if ANSWER_RE.match(r_first['text']) and r_first['x'] <= 85:
                break
            # otherwise pull all text from this row, skipping any pure-qnum item
            # and stripping a `\d+ ` prefix from the leftmost text item.
            row_strs = []
            stripped_prefix_yet = False
            for k, item in enumerate(r):
                t = item['text']
                if QNUM_RE.match(t):
                    continue  # standalone qnum, skip
                if not stripped_prefix_yet:
                    pm = QNUM_PREFIX_RE.match(t)
                    if pm:
                        t = t[pm.end():]
                        stripped_prefix_yet = True
                row_strs.append(t)
            content_parts.append(''.join(row_strs))
            j += 1
        content = ''.join(content_parts).strip()
        questions.append({
            'qnum': qnum,
            'answer': answer,
            'content': content,
        })
        i = j
    return questions

def split_stem_options(content: str) -> tuple[str, list[str]]:
    """Split into stem + 4 options. Option markers (1)(2)(3)(4) must appear in order;
    any later (N) inside an option's text is treated as literal."""
    # Find positions of option markers (1),(2),(3),(4) in ORDER.
    cursor = 0
    boundaries = []  # list of (n, start_idx) where start_idx is position of '(' in content
    for expected in '1234':
        target = f'({expected})'
        idx = content.find(target, cursor)
        if idx < 0:
            break
        boundaries.append((expected, idx))
        cursor = idx + len(target)
    if not boundaries:
        return content.strip(' ，。、'), ['', '', '', '']
    stem = content[:boundaries[0][1]].strip(' ，。、')
    opts = ['', '', '', '']
    for bi, (n, pos) in enumerate(boundaries):
        opt_start = pos + 3  # after '(N)'
        opt_end = boundaries[bi+1][1] if bi+1 < len(boundaries) else len(content)
        opts[int(n)-1] = content[opt_start:opt_end].strip(' ，。、')
    return stem, opts

def parse_pdf(pdf_path: str, category: str, out_jsonl: str,
              page_range: tuple[int,int] | None = None) -> list[dict]:
    doc = fitz.open(pdf_path)
    n = len(doc)
    start, end = (0, n)
    if page_range:
        start = page_range[0]
        end = page_range[1] if page_range[1] else n
    os.makedirs('_build', exist_ok=True)
    questions = []
    for pno in range(start, end):
        page = doc[pno]
        page_qs = parse_page(page)
        for q in page_qs:
            stem, opts = split_stem_options(q['content'])
            entry = {
                'category': category,
                'qnum': q['qnum'],
                'answer': q['answer'],
                'stem': stem,
                'options': opts,
                'page': pno + 1,
            }
            questions.append(entry)
    with open(out_jsonl, 'w', encoding='utf-8') as f:
        for q in questions:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    print(f'Wrote {len(questions)} questions → {out_jsonl}', flush=True)
    return questions

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('pdf')
    p.add_argument('category')
    p.add_argument('out')
    p.add_argument('--start', type=int, default=0)
    p.add_argument('--end', type=int, default=None)
    a = p.parse_args()
    parse_pdf(a.pdf, a.category, a.out,
              page_range=(a.start, a.end))
