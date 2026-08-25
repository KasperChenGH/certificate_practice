"""Exercise apply_stem_overrides' two failure modes and its happy path."""
import importlib.util, json, sys, io
from pathlib import Path

REPO = Path(r'C:\Users\User\Desktop\certificate_practice')
spec = importlib.util.spec_from_file_location('b', REPO / 'scripts' / 'build.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)          # build.py rebinds sys.stdout; restore it below
sys.stdout = io.TextIOWrapper(sys.__stdout__.buffer, encoding='utf-8', errors='replace')

OVR = json.loads((REPO / 'sources' / 'stem_overrides.json').read_text(encoding='utf-8'))
WAS = OVR['futures-503']['was']
NEW = OVR['futures-503']['stem']


def q(qid, stem):
    return {'id': qid, 'stem': stem, 'options': {'A': 'x'}, 'answer': 'A'}


# 1. Happy path: the override applies and nothing is left dangling.
data = {'futures': [q('futures-503', WAS), q('other-1', '一般題目')]}
b.apply_stem_overrides(data)
assert data['futures'][0]['stem'] == NEW, 'override not applied'
print('PASS  override applied, stem is now self-contained')

# 2. Idempotent: running again on already-rewritten data is a no-op, not an error.
b.apply_stem_overrides(data)
assert data['futures'][0]['stem'] == NEW
print('PASS  re-running on already-overridden data is a no-op')

# 3. An un-overridden cross-reference is a hard error.
data = {'futures': [q('futures-503', WAS), q('new-99', '承上題,則下列何者正確?')]}
try:
    b.apply_stem_overrides(data)
    print('FAIL  a dangling cross-reference was allowed through')
except ValueError as e:
    assert 'new-99' in str(e), e
    print('PASS  dangling cross-reference rejected:', str(e).splitlines()[0])

# 4. If the parsed stem drifts from the recorded original, refuse to rewrite.
data = {'futures': [q('futures-503', '完全不同的題目文字')]}
try:
    b.apply_stem_overrides(data)
    print('FAIL  override applied to a stem it does not match')
except ValueError as e:
    assert 'no longer matches' in str(e), e
    print('PASS  drifted stem rejected rather than silently rewritten')

# 5. An override pointing at a question that is not in the build is an error.
data = {'futures': [q('other-1', '一般題目')]}
try:
    b.apply_stem_overrides(data)
    print('FAIL  missing override target ignored')
except ValueError as e:
    assert 'not in the build' in str(e), e
    print('PASS  missing override target rejected')
