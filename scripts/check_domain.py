"""Check whether certifications.courses is correctly pointed at GitHub Pages.

Run it after changing DNS at the registrar, and again a few minutes later. It reports
what still needs doing rather than just failing.

    python scripts/check_domain.py [--domain certifications.courses]

Exit status 0 when the apex resolves to GitHub and HTTPS serves the site.
"""
from __future__ import annotations
import argparse, socket, ssl, sys, io, json, subprocess
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Published GitHub Pages addresses for an apex domain.
GH_A = {'185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153'}
GH_AAAA = {'2606:50c0:8000::153', '2606:50c0:8001::153',
           '2606:50c0:8002::153', '2606:50c0:8003::153'}
REPO = 'KasperChenGH/certificate_practice'

OK, BAD, WARN = '  OK  ', ' TODO ', ' WARN '


def resolve(host: str, family) -> set[str]:
    try:
        return {r[4][0] for r in socket.getaddrinfo(host, None, family)}
    except socket.gaierror:
        return set()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--domain', default='certifications.courses')
    args = ap.parse_args()
    d = args.domain
    problems = 0

    print(f'Checking {d}\n' + '-' * 60)

    a = resolve(d, socket.AF_INET)
    if a == GH_A:
        print(f'[{OK}] apex A records point at GitHub Pages')
    elif a & GH_A:
        print(f'[{WARN}] apex partially updated: {sorted(a)}')
        print(f'          missing: {sorted(GH_A - a)}  stale: {sorted(a - GH_A)}')
        problems += 1
    else:
        print(f'[{BAD}] apex A records are {sorted(a) or "unset"}, not GitHub')
        print(f'          replace them with: {", ".join(sorted(GH_A))}')
        problems += 1

    aaaa = resolve(d, socket.AF_INET6)
    if aaaa and aaaa <= GH_AAAA:
        print(f'[{OK}] apex AAAA records point at GitHub Pages')
    elif aaaa:
        print(f'[{WARN}] apex AAAA records are {sorted(aaaa)}, not GitHub (remove or fix)')
        problems += 1
    else:
        print(f'[{WARN}] no AAAA records (optional; IPv6 visitors fall back to IPv4)')

    www = resolve('www.' + d, socket.AF_INET)
    if www and (www == GH_A or www <= GH_A):
        print(f'[{OK}] www resolves to GitHub Pages')
    elif www:
        print(f'[{WARN}] www resolves to {sorted(www)}, not GitHub')
    else:
        print(f'[{WARN}] www does not resolve (optional)')

    # What GitHub thinks
    try:
        raw = subprocess.run(['gh', 'api', f'repos/{REPO}/pages'],
                             capture_output=True, text=True, timeout=30)
        if raw.returncode == 0:
            p = json.loads(raw.stdout)
            cert = (p.get('https_certificate') or {}).get('state')
            print(f'[  --  ] GitHub Pages: cname={p.get("cname")} status={p.get("status")} '
                  f'cert={cert} https_enforced={p.get("https_enforced")}')
            if p.get('cname') != d:
                print(f'[{BAD}] Pages custom domain is not {d}')
                problems += 1
            if cert == 'approved' and not p.get('https_enforced'):
                print(f'[{BAD}] certificate is ready — turn on Enforce HTTPS:')
                print(f'          gh api -X PUT repos/{REPO}/pages -F https_enforced=true')
                problems += 1
    except Exception as e:
        print(f'[{WARN}] could not read the Pages API ({e})')

    # Does it actually serve?
    for scheme in ('http', 'https'):
        url = f'{scheme}://{d}/'
        try:
            req = Request(url, headers={'User-Agent': 'check_domain'})
            with urlopen(req, timeout=15) as r:
                body = r.read(4000).decode('utf-8', 'replace')
                served = '金融證照練習' in body or 'questions.json' in body
                print(f'[{OK if served else WARN}] {url} -> {r.status} '
                      f'{"(our site)" if served else "(something else is answering)"}')
                if not served:
                    problems += 1
        except HTTPError as e:
            print(f'[{WARN}] {url} -> HTTP {e.code}')
        except (URLError, ssl.SSLError, TimeoutError) as e:
            reason = getattr(e, 'reason', e)
            print(f'[{BAD}] {url} unreachable: {reason}')
            problems += 1

    print('-' * 60)
    print('All good.' if not problems else f'{problems} item(s) still to do.')
    return 0 if not problems else 1


if __name__ == '__main__':
    sys.exit(main())
