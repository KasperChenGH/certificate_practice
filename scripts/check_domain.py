"""Check whether certifications.courses is correctly pointed at GitHub Pages.

    python scripts/check_domain.py [--domain certifications.courses]

Reports the zone's own nameservers separately from public resolvers. That distinction
matters: after a DNS change the authoritative answer is correct immediately, while
caches keep serving the old records until the previous TTL expires. Conflating the two
makes finished work look unfinished.

Exit status 0 once the authoritative records are right, GitHub has issued a
certificate, and HTTPS serves the site.
"""
from __future__ import annotations
import argparse, ssl, sys, io, json, subprocess
from pathlib import Path
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import URLError, HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dnsq

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Published GitHub Pages addresses for an apex domain.
GH_A = {'185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153'}
GH_AAAA = {'2606:50c0:8000::153', '2606:50c0:8001::153',
           '2606:50c0:8002::153', '2606:50c0:8003::153'}
REPO = 'KasperChenGH/certificate_practice'

OK, TODO, WARN, INFO = '  OK  ', ' TODO ', ' WARN ', '  --  '


class _NoRedirect(HTTPRedirectHandler):
    """Report the first response instead of following it.

    A forwarding service answers with a redirect; following it would hide the Server
    header that identifies who is actually holding the domain.
    """
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(url: str, follow: bool = False):
    opener = build_opener() if follow else build_opener(_NoRedirect)
    try:
        with opener.open(Request(url, headers={'User-Agent': 'check_domain'}),
                         timeout=20) as r:
            return r.status, r.headers, r.read(4000)
    except HTTPError as e:
        return e.code, e.headers, b''
    except (URLError, ssl.SSLError, TimeoutError, OSError) as e:
        return None, getattr(e, 'reason', e), b''


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--domain', default='certifications.courses')
    args = ap.parse_args()
    d = args.domain
    todo = 0

    print(f'Checking {d}\n' + '-' * 66)

    # ---- the zone itself: what the registrar has actually saved ----------------
    try:
        ns = dnsq.authoritative_servers(d)
        auth_a = set(dnsq.query(d, dnsq.A, ns[0]))
        auth_aaaa = set(dnsq.query(d, dnsq.AAAA, ns[0]))
    except Exception as e:
        print(f'[{WARN}] could not reach the authoritative nameservers ({e})')
        auth_a, auth_aaaa = set(), set()

    if auth_a == GH_A:
        print(f'[{OK}] apex A records correct at the registrar (all four)')
    elif auth_a & GH_A:
        print(f'[{WARN}] apex partially set: {sorted(auth_a)}')
        print(f'          missing {sorted(GH_A - auth_a)}, stale {sorted(auth_a - GH_A)}')
        todo += 1
    else:
        print(f'[{TODO}] apex A records are {sorted(auth_a) or "unset"}, not GitHub')
        print(f'          set them to: {", ".join(sorted(GH_A))}')
        todo += 1

    if auth_aaaa and not auth_aaaa <= GH_AAAA:
        print(f'[{WARN}] apex AAAA records are {sorted(auth_aaaa)}, not GitHub — remove them')
        todo += 1

    # ---- caches: how much of the internet has caught up ------------------------
    try:
        public = set(dnsq.query(d, dnsq.A))
        if public == GH_A:
            print(f'[{OK}] public resolvers have caught up')
        elif public & GH_A:
            print(f'[{INFO}] public resolvers partly caught up: {sorted(public)}')
        else:
            print(f'[{INFO}] public resolvers still cache {sorted(public)} — '
                  f'propagation only, nothing to do')
    except Exception:
        pass

    # ---- registrar forwarding, which pins the apex A record --------------------
    # Only meaningful while the A records are still wrong. Once they point at GitHub,
    # forwarding cannot intercept anything, and asking the OS resolver here would just
    # re-report a stale cache as a live problem.
    if auth_a != GH_A:
        _status, hdrs, _body = fetch(f'http://{d}/')
        server = hdrs.get('server', '') if hasattr(hdrs, 'get') else ''
        if server.startswith('DPS'):
            print(f'[{TODO}] registrar forwarding is still ON (server: {server})')
            print( '          it pins the apex A record; delete the forwarding entry')
            todo += 1

    # ---- GitHub's side ---------------------------------------------------------
    try:
        raw = subprocess.run(['gh', 'api', f'repos/{REPO}/pages'],
                             capture_output=True, text=True, timeout=30)
        if raw.returncode == 0:
            p = json.loads(raw.stdout)
            cert = (p.get('https_certificate') or {}).get('state')
            print(f'[{INFO}] Pages: cname={p.get("cname")} status={p.get("status")} '
                  f'cert={cert or "not issued yet"} '
                  f'https_enforced={p.get("https_enforced")}')
            if p.get('cname') != d:
                print(f'[{TODO}] Pages custom domain is not {d}')
                todo += 1
            if cert == 'approved' and not p.get('https_enforced'):
                print(f'[{TODO}] certificate ready — enable HTTPS:')
                print(f'          gh api -X PUT repos/{REPO}/pages -F https_enforced=true')
                todo += 1
            elif cert != 'approved':
                print(f'[{INFO}] GitHub issues the certificate automatically once its DNS '
                      f'check passes — minutes to an hour after propagation')
    except Exception as e:
        print(f'[{WARN}] could not read the Pages API ({e})')

    # ---- does GitHub serve this site for this hostname? ------------------------
    # Pinned to a GitHub IP so this answers even while caches point elsewhere.
    served = False
    try:
        out = subprocess.run(
            ['curl', '-s', '--max-time', '25', '--resolve', f'{d}:80:185.199.108.153',
             f'http://{d}/'], capture_output=True, text=True,
            encoding='utf-8', errors='replace')
        served = 'questions.json' in out.stdout
    except Exception:
        pass
    print(f'[{OK if served else WARN}] GitHub Pages '
          f'{"serves this site" if served else "does not yet serve this site"} for {d}')
    if not served:
        todo += 1

    # ---- the real user-facing test ---------------------------------------------
    status, info, body = fetch(f'https://{d}/', follow=True)
    if status == 200 and b'questions.json' in body:
        print(f'[{OK}] https://{d}/ serves the site')
    elif status is None:
        print(f'[{INFO}] https://{d}/ not reachable yet ({info}) — expected until the '
              f'certificate is issued')
        todo += 1
    else:
        print(f'[{WARN}] https://{d}/ returned {status} but not this site')
        if auth_a == GH_A:
            print( '          if this machine still shows an old IP, flush its DNS cache:')
            print( '          Windows: ipconfig /flushdns   macOS: sudo killall -HUP mDNSResponder')
        todo += 1

    print('-' * 66)
    print('All done.' if not todo else f'{todo} item(s) outstanding.')
    return 0 if not todo else 1


if __name__ == '__main__':
    sys.exit(main())
