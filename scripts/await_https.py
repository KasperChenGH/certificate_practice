"""Wait for GitHub to issue the TLS certificate, then turn on Enforce HTTPS.

GitHub requests a Let's Encrypt certificate on its own once its DNS check sees the
domain pointing at Pages. That check reads public resolvers, so it cannot pass until
their caches expire — nothing here can hurry it, only watch for it.

Enforcing HTTPS before the certificate exists fails, which is why this waits rather
than setting it up front.

    python scripts/await_https.py [--minutes 90] [--no-enable]
"""
from __future__ import annotations
import argparse, json, subprocess, sys, io, time
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
REPO = 'KasperChenGH/certificate_practice'


def api(*args: str) -> dict | None:
    r = subprocess.run(['gh', 'api', *args], capture_output=True, text=True,
                       encoding='utf-8', errors='replace', timeout=60)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def stamp() -> str:
    return datetime.now().strftime('%H:%M:%S')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--minutes', type=int, default=90)
    ap.add_argument('--no-enable', action='store_true',
                    help='report readiness but do not change the setting')
    args = ap.parse_args()

    deadline = time.time() + args.minutes * 60
    poked = False
    while time.time() < deadline:
        pages = api(f'repos/{REPO}/pages') or {}
        cert = (pages.get('https_certificate') or {}).get('state')
        health = (api(f'repos/{REPO}/pages/health') or {}).get('domain') or {}
        print(f'[{stamp()}] dns_ok={health.get("is_pointed_to_github_pages_ip")} '
              f'served={health.get("is_served_by_pages")} '
              f'cert={cert or "pending"} '
              f'enforced={pages.get("https_enforced")}', flush=True)

        if cert == 'approved':
            if pages.get('https_enforced'):
                print(f'[{stamp()}] HTTPS already enforced. Done.', flush=True)
                return 0
            if args.no_enable:
                print(f'[{stamp()}] Certificate ready. Enable with:\n'
                      f'  gh api -X PUT repos/{REPO}/pages -F https_enforced=true', flush=True)
                return 0
            subprocess.run(['gh', 'api', '-X', 'PUT', f'repos/{REPO}/pages',
                            '-F', 'https_enforced=true'],
                           capture_output=True, text=True, timeout=60)
            after = api(f'repos/{REPO}/pages') or {}
            ok = after.get('https_enforced')
            print(f'[{stamp()}] Enforce HTTPS set -> {ok}', flush=True)
            return 0 if ok else 1

        # Once DNS looks right to GitHub but no certificate has appeared, re-saving the
        # domain re-triggers the request. Worth exactly one attempt.
        if health.get('is_pointed_to_github_pages_ip') and not poked:
            subprocess.run(['gh', 'api', '-X', 'PUT', f'repos/{REPO}/pages',
                            '-f', 'cname=certifications.courses'],
                           capture_output=True, text=True, timeout=60)
            print(f'[{stamp()}] DNS check passed; re-saved the domain to request the '
                  f'certificate', flush=True)
            poked = True

        time.sleep(120)

    print(f'[{stamp()}] Gave up after {args.minutes} min. Certificate still pending; '
          f're-run this or check scripts/check_domain.py later.', flush=True)
    return 1


if __name__ == '__main__':
    sys.exit(main())
