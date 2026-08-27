"""Confirm build.py refuses to ship a bank with fewer explanations than it last had.

The per-option explanations were generated once and are not reproducible from the
source PDFs. carry_over_explanations re-attaches them from the existing
questions.json, which means a bank that is absent from that file — retired, then
restored — comes back bare with no error at all. That is not hypothetical: it is how
1,120 finance_ethics explanations were nearly lost.
"""
import json, io, os, shutil, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
Q = REPO / 'questions.json'
COV = REPO / 'sources' / 'explanation_coverage.json'
os.chdir(REPO)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def build(*args):
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    return subprocess.run([sys.executable, 'scripts/build.py', *args],
                          capture_output=True, text=True,
                          encoding='utf-8', errors='replace', env=env)


def strip_explanations(bank):
    d = json.loads(Q.read_text(encoding='utf-8'))
    for q in d[bank]:
        q.pop('explanations', None)
    Q.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')


q_bak, cov_bak = Q.read_bytes(), COV.read_bytes()
try:
    r = build()
    assert r.returncode == 0, r.stderr[-500:]
    print('PASS  clean build records coverage')

    baseline = json.loads(COV.read_text(encoding='utf-8'))
    assert baseline['finance_ethics'] == 1120, baseline
    print('PASS  baseline holds the real numbers:',
          ', '.join(f'{k} {v}' for k, v in sorted(baseline.items())))

    # The exact regression: the bank rebuilds fine, just without its explanations.
    strip_explanations('finance_ethics')
    r = build()
    msg = next((l for l in r.stderr.splitlines() if 'finance_ethics: 1120 -> 0' in l), '')
    assert r.returncode != 0 and msg, r.stderr[-800:]
    print('PASS  explanation loss rejected:', msg.strip())

    # An intended drop still needs saying so out loud.
    r = build('--accept-coverage-drop')
    assert r.returncode == 0, r.stderr[-500:]
    assert json.loads(COV.read_text(encoding='utf-8'))['finance_ethics'] == 0
    print('PASS  --accept-coverage-drop rewrites the baseline')

    # A bank missing from the build keeps its baseline, so retire-then-restore is safe.
    COV.write_text(json.dumps({**baseline, 'retired_bank': 42}, ensure_ascii=False),
                   encoding='utf-8')
    Q.write_bytes(q_bak)
    r = build()
    assert r.returncode == 0, r.stderr[-500:]
    assert json.loads(COV.read_text(encoding='utf-8'))['retired_bank'] == 42
    print('PASS  a retired bank keeps its baseline while absent')
finally:
    Q.write_bytes(q_bak)
    COV.write_bytes(cov_bak)
    r = build()
    print('restored; rebuild exit code', r.returncode)
