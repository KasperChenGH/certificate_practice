"""Merge all explanation outputs (pilot + 14 chunks) into questions.json.
Adds an `explanations` field to each question.
Idempotent: safe to re-run after partial completion.
"""
from __future__ import annotations
import json, os, sys, io, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(REPO, '_expl_work')

def load_jsonl(path):
    with open(path, encoding='utf-8') as f:
        return [json.loads(l) for l in f if l.strip()]

# Collect all explanations
all_expl = {}  # id -> {A,B,C,D}
sources = []

pilot = os.path.join(WORK, 'pilot_output.jsonl')
if os.path.exists(pilot):
    rows = load_jsonl(pilot)
    sources.append(('pilot', len(rows)))
    for r in rows:
        all_expl[r['id']] = r['explanations']

for path in sorted(glob.glob(os.path.join(WORK, 'chunks', 'chunk_*_output.jsonl'))):
    rows = load_jsonl(path)
    sources.append((os.path.basename(path), len(rows)))
    for r in rows:
        all_expl[r['id']] = r['explanations']

for name, n in sources:
    print(f'  {name}: {n}')
print(f'Total unique explanations: {len(all_expl)}')

# Merge into questions.json
data = json.load(open(os.path.join(REPO, 'questions.json'), encoding='utf-8'))
covered = missing = 0
for topic, qs in data.items():
    for q in qs:
        if q['id'] in all_expl:
            q['explanations'] = all_expl[q['id']]
            covered += 1
        else:
            missing += 1

print(f'Covered: {covered}, missing: {missing}')

# Write back
with open(os.path.join(REPO, 'questions.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
sz = os.path.getsize(os.path.join(REPO, 'questions.json'))
print(f'questions.json: {sz} bytes ({sz/1024:.1f} KB)')

if missing:
    print(f'\n⚠ {missing} questions have no explanation. List of missing IDs:')
    for topic, qs in data.items():
        for q in qs:
            if 'explanations' not in q:
                print(f'  {q["id"]}')
