"""Minimal DNS-over-UDP client — just enough to read A, AAAA, CNAME, and NS.

`socket.getaddrinfo` answers from the OS cache, which lags a DNS change by up to the
old record's TTL. That made check_domain.py report records as unchanged minutes after
they had in fact been updated. Querying the zone's own nameservers gives the truth
immediately, so the two can be reported separately.

The standard library has no DNS client and this repo has no third-party dependencies,
hence the ~60 lines below.
"""
from __future__ import annotations
import socket, struct

A, NS, CNAME, AAAA = 1, 2, 5, 28
PUBLIC_RESOLVER = '8.8.8.8'


def _skip_name(buf: bytes, off: int) -> int:
    """Advance past a (possibly compressed) domain name."""
    while True:
        n = buf[off]
        if n == 0:
            return off + 1
        if n & 0xC0 == 0xC0:        # pointer: two bytes, no continuation
            return off + 2
        off += 1 + n


def _read_name(buf: bytes, off: int) -> str:
    labels: list[str] = []
    hops = 0
    while True:
        n = buf[off]
        if n == 0:
            break
        if n & 0xC0 == 0xC0:        # follow compression pointer
            hops += 1
            if hops > 16:           # malformed packet; refuse to loop
                break
            off = struct.unpack('>H', buf[off:off + 2])[0] & 0x3FFF
            continue
        labels.append(buf[off + 1:off + 1 + n].decode('ascii', 'replace'))
        off += 1 + n
    return '.'.join(labels)


def query(name: str, qtype: int, server: str = PUBLIC_RESOLVER,
          timeout: float = 5.0) -> list[str]:
    """Return the record values for `name`/`qtype` as answered by `server`."""
    header = struct.pack('>HHHHHH', 0x2A2A, 0x0100, 1, 0, 0, 0)
    qname = b''.join(bytes([len(l)]) + l.encode('ascii')
                     for l in name.rstrip('.').split('.')) + b'\x00'
    packet = header + qname + struct.pack('>HH', qtype, 1)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        sock.sendto(packet, (server, 53))
        buf, _ = sock.recvfrom(4096)

    ancount = struct.unpack('>H', buf[6:8])[0]
    off = _skip_name(buf, len(header)) + 4       # past the echoed question
    out: list[str] = []
    for _ in range(ancount):
        off = _skip_name(buf, off)
        rtype, _rclass, _ttl, rdlen = struct.unpack('>HHIH', buf[off:off + 10])
        off += 10
        rdata_at, off = off, off + rdlen
        if rtype == A and rdlen == 4:
            out.append(socket.inet_ntop(socket.AF_INET, buf[rdata_at:off]))
        elif rtype == AAAA and rdlen == 16:
            out.append(socket.inet_ntop(socket.AF_INET6, buf[rdata_at:off]))
        elif rtype in (CNAME, NS):
            out.append(_read_name(buf, rdata_at))
    return out


def authoritative_servers(domain: str) -> list[str]:
    """Nameserver IPs for `domain`, so a zone can be read without cache lag."""
    ips = []
    for host in query(domain, NS):
        try:
            ips.append(socket.gethostbyname(host))
        except socket.gaierror:
            pass
    return ips
