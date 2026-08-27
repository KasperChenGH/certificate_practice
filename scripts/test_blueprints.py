"""Confirm build.py rejects a blueprint that does not match the data."""
import json, io, shutil, subprocess, sys, os
from pathlib import Path

REPO = Path(r'C:\Users\User\Desktop\certificate_practice')
SRC = REPO / 'sources' / 'exam_blueprints.json'
BAK = SRC.with_suffix('.json.testbak')
os.chdir(REPO)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def build():
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    return subprocess.run([sys.executable, 'scripts/build.py'],
                          capture_output=True, text=True,
                          encoding='utf-8', errors='replace', env=env)


def mutate(fn):
    d = json.loads(SRC.read_text(encoding='utf-8'))
    fn(d)
    SRC.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')


shutil.copy(SRC, BAK)
try:
    # baseline
    r = build()
    assert r.returncode == 0, r.stderr[-500:]
    print('PASS  clean blueprint builds')

    # 1. subject name that matches no question
    mutate(lambda d: d['futures']['subjects'][0].__setitem__('subject', '期貨交易法規TYPO'))
    r = build()
    msg = next((l for l in r.stderr.splitlines() if 'no questions whose subject' in l), '')
    assert r.returncode != 0 and msg, r.stderr[-500:]
    print('PASS  unknown subject rejected:', msg.strip()[:96])
    shutil.copy(BAK, SRC)

    # 2. section asking for more questions than exist
    mutate(lambda d: d['sitca']['subjects'][0].__setitem__('count', 500))
    r = build()
    msg = next((l for l in r.stderr.splitlines() if 'asks for' in l), '')
    assert r.returncode != 0 and msg, r.stderr[-500:]
    print('PASS  oversized section rejected:', msg.strip()[:96])
    shutil.copy(BAK, SRC)

    # 3. blueprint naming a bank that does not exist
    mutate(lambda d: d.__setitem__('no_such_bank', {'exam': 'x', 'subjects': []}))
    r = build()
    msg = next((l for l in r.stderr.splitlines() if 'no bank named' in l), '')
    assert r.returncode != 0 and msg, r.stderr[-500:]
    print('PASS  unknown bank rejected:', msg.strip()[:96])
    shutil.copy(BAK, SRC)

    # 4. a draw enlarged until its pool can no longer vary the paper. 382 questions
    #    fills a 200-question section, so the old have<count check passes it.
    mutate(lambda d: d['futures']['subjects'][0].__setitem__('count', 200))
    r = build()
    msg = next((l for l in r.stderr.splitlines() if '期貨交易法規' in l and 'draws' in l), '')
    assert r.returncode != 0 and msg, r.stderr[-800:]
    print('PASS  newly thin subject rejected:', msg.strip()[:96])
    shutil.copy(BAK, SRC)

    # 5. _thin_ok is what makes the known-thin subjects build; drop one and it fails.
    mutate(lambda d: d['_thin_ok'].remove('sitca/投信投顧相關法規'))
    r = build()
    msg = next((l for l in r.stderr.splitlines() if '投信投顧相關法規' in l and 'draws' in l), '')
    assert r.returncode != 0 and msg, r.stderr[-800:]
    print('PASS  un-listing a thin subject rejected:', msg.strip()[:96])
    shutil.copy(BAK, SRC)

    # 6. the ratios reach blueprints.json, so thinness is inspectable not folklore.
    r = build()
    bp = json.loads((REPO / 'blueprints.json').read_text(encoding='utf-8'))
    assert bp['sitca']['coverage']['ratio'] == 1.94, bp['sitca']['coverage']
    assert bp['futures']['coverage']['subjects']['期貨交易法規']['ratio'] > 3
    print('PASS  coverage ratios recorded in blueprints.json')
finally:
    shutil.copy(BAK, SRC)
    BAK.unlink()
    r = build()
    print('restored; rebuild exit code', r.returncode)
