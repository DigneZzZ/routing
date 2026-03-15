#!/usr/bin/env python3
"""
build_dat.py — Build V2Ray/Xray compatible geosite.dat and geoip.dat
from MetaCubeX and Re:filter (1andrevich) open sources.

Output:
  v2ray/geosite.dat   — domain categories (protobuf)
  v2ray/geoip.dat     — IP categories (protobuf)

Compatible with V2Ray, Xray, Sing-box, Happ and other clients
that use standard .dat geo files.

Protobuf schema (v2ray/v2fly):
  GeoSiteList { repeated GeoSite { country_code, repeated Domain { type, value } } }
  GeoIPList   { repeated GeoIP   { country_code, repeated CIDR  { ip, prefix }   } }
"""

import base64
import ipaddress
import json
import time
import urllib.request
from collections import OrderedDict
from pathlib import Path

REPO_DIR = Path(__file__).parent
OUT_DIR = REPO_DIR / "v2ray"

# ── Repository config ────────────────────────────────────────
REPO_OWNER = "DigneZzZ"
REPO_NAME = "routing"
CDN_BASE = f"https://cdn.jsdelivr.net/gh/{REPO_OWNER}/{REPO_NAME}@main/v2ray"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/v2ray"

MCX = "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo"
REFILTER = "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main"

# ── Domain types (V2Ray protobuf enum) ────────────────────────
PLAIN = 0   # substring match
REGEX = 1   # regular expression
DOMAIN = 2  # matches domain + all subdomains
FULL = 3    # exact match


# ══════════════════════════════════════════════════════════════
#   Protobuf encoder (minimal, no external dependencies)
# ══════════════════════════════════════════════════════════════

def _varint(value):
    buf = bytearray()
    while value > 0x7F:
        buf.append((value & 0x7F) | 0x80)
        value >>= 7
    buf.append(value & 0x7F)
    return bytes(buf)


def _field_varint(fnum, value):
    """Encode varint field (wire type 0)."""
    return _varint((fnum << 3) | 0) + _varint(value)


def _field_bytes(fnum, data):
    """Encode length-delimited field (wire type 2)."""
    tag = _varint((fnum << 3) | 2)
    return tag + _varint(len(data)) + data


def _field_string(fnum, value):
    return _field_bytes(fnum, value.encode("utf-8"))


# ── Geosite encoding ─────────────────────────────────────────

def _encode_domain(dtype, value):
    buf = bytearray()
    if dtype != 0:  # skip default value (proto3)
        buf += _field_varint(1, dtype)
    buf += _field_string(2, value)
    return bytes(buf)


def _encode_geosite(country_code, domains):
    buf = bytearray()
    buf += _field_string(1, country_code)
    for dtype, value in domains:
        buf += _field_bytes(2, _encode_domain(dtype, value))
    return bytes(buf)


def _encode_geosite_list(entries):
    buf = bytearray()
    for cc, domains in entries:
        buf += _field_bytes(1, _encode_geosite(cc, domains))
    return bytes(buf)


# ── GeoIP encoding ───────────────────────────────────────────

def _encode_cidr(ip_bytes, prefix):
    buf = bytearray()
    buf += _field_bytes(1, ip_bytes)
    if prefix > 0:  # skip default value (proto3)
        buf += _field_varint(2, prefix)
    return bytes(buf)


def _encode_geoip(country_code, cidrs):
    buf = bytearray()
    buf += _field_string(1, country_code)
    for ip_bytes, prefix in cidrs:
        buf += _field_bytes(2, _encode_cidr(ip_bytes, prefix))
    return bytes(buf)


def _encode_geoip_list(entries):
    buf = bytearray()
    for cc, cidrs in entries:
        buf += _field_bytes(1, _encode_geoip(cc, cidrs))
    return bytes(buf)


# ══════════════════════════════════════════════════════════════
#   Download & parsing
# ══════════════════════════════════════════════════════════════

def download(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "routing/1.0"})
            resp = urllib.request.urlopen(req, timeout=30)
            return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            if attempt == retries - 1:
                print(f"    WARN: {url.split('/')[-1]}: {e}")
                return None
            time.sleep(2)


def parse_domain_entry(line):
    """Parse a single line into (domain_type, value) or None."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    # Strip inline comments
    for sep in (" #", "\t#"):
        if sep in line:
            line = line.split(sep)[0].strip()

    # Mihomo rule format: DOMAIN-SUFFIX,domain.com
    upper = line.upper()
    if upper.startswith("DOMAIN-SUFFIX,"):
        return (DOMAIN, line.split(",", 1)[1].strip())
    if upper.startswith("DOMAIN-KEYWORD,"):
        return (PLAIN, line.split(",", 1)[1].strip())
    if upper.startswith("DOMAIN,"):
        return (FULL, line.split(",", 1)[1].strip())

    # Skip non-domain rules
    if upper.startswith(("IP-CIDR", "PROCESS", "SRC-", "DST-", "RULE-SET",
                         "MATCH", "GEOIP", "GEOSITE", "AND", "OR", "NOT")):
        return None

    # V2Ray text list format
    if line.startswith("full:"):
        return (FULL, line[5:])
    if line.startswith("regexp:") or line.startswith("regex:"):
        return (REGEX, line.split(":", 1)[1])
    if line.startswith("domain:"):
        return (DOMAIN, line[7:])
    if line.startswith("+."):
        return (DOMAIN, line[2:])
    if line.startswith("."):
        return (DOMAIN, line[1:])

    # Skip things that look like CIDR
    if "/" in line:
        parts = line.split("/")
        if len(parts) == 2 and parts[1].isdigit():
            return None

    # Default: treat as domain (subdomain match)
    return (DOMAIN, line)


def parse_ip_entry(line):
    """Parse a CIDR line into (ip_bytes, prefix) or None."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if " #" in line:
        line = line.split(" #")[0].strip()

    # Mihomo format: IP-CIDR,addr/prefix,no-resolve
    upper = line.upper()
    if upper.startswith(("IP-CIDR6,", "IP-CIDR,")):
        line = line.split(",", 1)[1].strip()
        if "," in line:
            line = line.split(",")[0].strip()

    try:
        net = ipaddress.ip_network(line.strip(), strict=False)
        return (net.network_address.packed, net.prefixlen)
    except ValueError:
        return None


def load_domains(urls, extra):
    """Download domain sources and merge with extras, deduplicated."""
    domains = []
    seen = set()
    for url in urls:
        text = download(url)
        if not text:
            continue
        count = 0
        for raw_line in text.split("\n"):
            parsed = parse_domain_entry(raw_line)
            if parsed and parsed not in seen:
                seen.add(parsed)
                domains.append(parsed)
                count += 1
        print(f"    + {url.split('/')[-1]}: {count}")
    for entry in extra:
        parsed = parse_domain_entry(entry)
        if parsed and parsed not in seen:
            seen.add(parsed)
            domains.append(parsed)
    if extra:
        print(f"    + inline: {len(extra)}")
    return domains


def load_cidrs(urls):
    """Download IP sources and parse CIDRs."""
    cidrs = []
    seen = set()
    for url in urls:
        text = download(url)
        if not text:
            continue
        count = 0
        for raw_line in text.split("\n"):
            parsed = parse_ip_entry(raw_line)
            if parsed and parsed not in seen:
                seen.add(parsed)
                cidrs.append(parsed)
                count += 1
        print(f"    + {url.split('/')[-1]}: {count}")
    return cidrs


# ══════════════════════════════════════════════════════════════
#   Source definitions
# ══════════════════════════════════════════════════════════════

GEOSITE = OrderedDict([
    # ── Direct / whitelist ────────────────────────────────────
    ("WHITELIST", {
        "urls": [f"{MCX}/geosite/category-ru.list"],
        "extra": [
            "+.yandex.ru", "+.yandex.com", "+.ya.ru", "+.yandex.net",
            "+.vk.com", "+.vkontakte.ru", "+.vk.me", "+.userapi.com",
            "+.mail.ru", "+.ok.ru", "+.odnoklassniki.ru",
            "+.sberbank.ru", "+.sber.ru", "+.online.sberbank.ru",
            "+.tinkoff.ru", "+.tbank.ru",
            "+.gosuslugi.ru", "+.mos.ru",
            "+.wildberries.ru", "+.wb.ru",
            "+.ozon.ru", "+.ozon.com",
            "+.avito.ru", "+.cian.ru",
            "+.ria.ru", "+.rbc.ru", "+.lenta.ru",
            "+.rutube.ru", "+.ivi.ru", "+.kinopoisk.ru",
            "+.1c.ru", "+.1cfresh.com",
            "+.2gis.com", "+.2gis.ru",
            "+.nalog.gov.ru", "+.pfr.gov.ru",
            "+.cbr.ru", "+.gazprombank.ru",
            "+.vtb.ru", "+.alfabank.ru", "+.raiffeisen.ru",
            "+.megafon.ru", "+.mts.ru", "+.beeline.ru", "+.tele2.ru",
            "+.rostelecom.ru", "+.rt.ru",
            "+.mvideo.ru", "+.dns-shop.ru", "+.eldorado.ru",
            "+.cdek.ru", "+.pochta.ru", "+.russianpost.ru",
            "+.rzd.ru", "+.aeroflot.ru", "+.s7.ru",
            "+.lamoda.ru", "+.sportmaster.ru",
            "+.hh.ru", "+.superjob.ru",
            "+.drom.ru", "+.auto.ru",
            "+.apteka.ru", "+.zdravcity.ru",
            "+.kaspersky.ru", "+.drweb.ru",
            "+.mos.ru", "+.moscow.ru",
        ],
    }),
    ("CATEGORY-RU", {
        "urls": [f"{MCX}/geosite/category-ru.list"],
        "extra": [],
    }),
    ("PRIVATE", {
        "urls": [f"{MCX}/geosite/private.list"],
        "extra": [],
    }),

    # ── Blocked in Russia (needs proxy) ──────────────────────
    ("CATEGORY-GEOBLOCK-RU", {
        "urls": [f"{REFILTER}/domains_all.lst"],
        "extra": [],
    }),
    ("COMMUNITY", {
        "urls": [f"{REFILTER}/community.lst"],
        "extra": [],
    }),

    # ── Block categories ─────────────────────────────────────
    ("CATEGORY-ADS", {
        "urls": [f"{MCX}/geosite/category-ads-all.list"],
        "extra": [],
    }),
    ("WIN-SPY", {
        "urls": [f"{MCX}/geosite/win-spy.list"],
        "extra": [],
    }),
    ("TORRENT", {
        "urls": [],
        "extra": [
            "+.rutracker.org", "+.rutracker.net", "+.rutor.info", "+.rutor.is",
            "+.nnm-club.me", "+.thepiratebay.org", "+.1337x.to", "+.rarbg.to",
            "+.nyaa.si", "+.torrentgalaxy.to", "+.yts.mx",
            "+.limetorrents.info", "+.fitgirl-repacks.site",
            "+.kinozal.tv", "+.kinozal.guru",
            "+.pornolab.net", "+.tapochek.net", "+.uniondht.org",
            "+.tracker.opentrackr.org", "+.tracker.openbittorrent.com",
        ],
    }),

    # ── Service categories ───────────────────────────────────
    ("YOUTUBE", {
        "urls": [f"{MCX}/geosite/youtube.list"],
        "extra": [],
    }),
    ("TELEGRAM", {
        "urls": [f"{MCX}/geosite/telegram.list"],
        "extra": [],
    }),
    ("GITHUB", {
        "urls": [f"{MCX}/geosite/github.list"],
        "extra": [],
    }),
    ("STEAM", {
        "urls": [f"{MCX}/geosite/steam.list"],
        "extra": [],
    }),
    ("EPICGAMES", {
        "urls": [f"{MCX}/geosite/epicgames.list"],
        "extra": [],
    }),
    ("ORIGIN", {
        "urls": [f"{MCX}/geosite/origin.list"],
        "extra": [],
    }),
    ("APPLE", {
        "urls": [f"{MCX}/geosite/apple.list"],
        "extra": [],
    }),
    ("MICROSOFT", {
        "urls": [f"{MCX}/geosite/microsoft.list"],
        "extra": [],
    }),
    ("GOOGLE-PLAY", {
        "urls": [f"{MCX}/geosite/google-play.list"],
        "extra": [],
    }),
    ("GOOGLE-DEEPMIND", {
        "urls": [],
        "extra": [
            "+.ai.google.dev", "+.aistudio.google.com",
            "+.bard.google.com", "+.gemini.google.com",
            "+.makersuite.google.com", "+.generativelanguage.googleapis.com",
            "+.deepmind.com", "+.deepmind.google",
            "+.openai.com", "+.chatgpt.com", "+.chat.openai.com",
            "+.anthropic.com", "+.claude.ai",
            "+.perplexity.ai", "+.midjourney.com",
            "+.huggingface.co", "+.stability.ai",
        ],
    }),
    ("TWITCH", {
        "urls": [f"{MCX}/geosite/twitch.list"],
        "extra": [],
    }),
    ("TWITCH-ADS", {
        "urls": [],
        "extra": [
            "+.ads.twitch.tv",
            "+.gql.twitch.tv",
            "+.playlist.ttvnw.net",
            "+.static-cdn.jtvnw.net",
            "+.usher.ttvnw.net",
        ],
    }),
    ("PINTEREST", {
        "urls": [f"{MCX}/geosite/pinterest.list"],
        "extra": [],
    }),
    ("ESCAPEFROMTARKOV", {
        "urls": [f"{MCX}/geosite/escapefromtarkov.list"],
        "extra": [],
    }),
    ("FACEIT", {
        "urls": [],
        "extra": ["+.faceit.com", "+.faceit-cdn.net"],
    }),
    ("RIOT", {
        "urls": [],
        "extra": [
            "+.riotgames.com", "+.leagueoflegends.com", "+.valorant.com",
            "+.riotcdn.net", "+.lolstatic.com", "+.lolesports.com",
            "+.riotpnt.com", "+.playvalorant.com",
        ],
    }),
])

GEOIP = OrderedDict([
    ("WHITELIST", {"urls": [f"{MCX}/geoip/ru.list"]}),
    ("PRIVATE", {"urls": [f"{MCX}/geoip/private.list"]}),
    ("BLOCKED-RU", {"urls": [f"{REFILTER}/ipsum.lst"]}),
])

# Categories excluded from lite builds (redundant when GlobalProxy=true)
LITE_EXCLUDE_GEOSITE = {"CATEGORY-GEOBLOCK-RU", "COMMUNITY"}
LITE_EXCLUDE_GEOIP = {"BLOCKED-RU"}


# ══════════════════════════════════════════════════════════════
#   Main build
# ══════════════════════════════════════════════════════════════

def build():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ── Build geosite.dat ─────────────────────────────────────
    print("=" * 55)
    print("  Building geosite.dat")
    print("=" * 55)

    geosite_entries = []
    total_domains = 0

    for tag, config in GEOSITE.items():
        print(f"\n  [{tag}]")
        domains = load_domains(config["urls"], config["extra"])
        if domains:
            geosite_entries.append((tag, domains))
            total_domains += len(domains)
            print(f"    = {len(domains)} domains")
        else:
            print(f"    SKIP (no data)")

    geosite_data = _encode_geosite_list(geosite_entries)
    geosite_path = OUT_DIR / "geosite.dat"
    geosite_path.write_bytes(geosite_data)
    print(f"\n  geosite.dat: {len(geosite_entries)} categories, "
          f"{total_domains} domains, {len(geosite_data):,} bytes")

    # ── Build geoip.dat ───────────────────────────────────────
    print("\n" + "=" * 55)
    print("  Building geoip.dat")
    print("=" * 55)

    geoip_entries = []
    total_cidrs = 0

    for tag, config in GEOIP.items():
        print(f"\n  [{tag}]")
        cidrs = load_cidrs(config["urls"])
        if cidrs:
            geoip_entries.append((tag, cidrs))
            total_cidrs += len(cidrs)
            print(f"    = {len(cidrs)} CIDRs")
        else:
            print(f"    SKIP (no data)")

    geoip_data = _encode_geoip_list(geoip_entries)
    geoip_path = OUT_DIR / "geoip.dat"
    geoip_path.write_bytes(geoip_data)
    print(f"\n  geoip.dat: {len(geoip_entries)} categories, "
          f"{total_cidrs} CIDRs, {len(geoip_data):,} bytes")

    # ── Build lite .dat files (for Happ/INCY — no heavy proxy lists) ──
    print("\n" + "=" * 55)
    print("  Building lite .dat files (mobile clients)")
    print("=" * 55)

    lite_geosite = [(cc, doms) for cc, doms in geosite_entries
                    if cc not in LITE_EXCLUDE_GEOSITE]
    lite_geoip = [(cc, cidrs) for cc, cidrs in geoip_entries
                  if cc not in LITE_EXCLUDE_GEOIP]

    lite_gs_data = _encode_geosite_list(lite_geosite)
    lite_gi_data = _encode_geoip_list(lite_geoip)

    happ_dir = OUT_DIR / "happ"
    happ_dir.mkdir(parents=True, exist_ok=True)
    (happ_dir / "geosite.dat").write_bytes(lite_gs_data)
    (happ_dir / "geoip.dat").write_bytes(lite_gi_data)

    lite_gs_cats = len(lite_geosite)
    lite_gs_doms = sum(len(d) for _, d in lite_geosite)
    lite_gi_cats = len(lite_geoip)
    lite_gi_cids = sum(len(c) for _, c in lite_geoip)
    print(f"  Excluded geosite: {', '.join(sorted(LITE_EXCLUDE_GEOSITE))}")
    print(f"  Excluded geoip:   {', '.join(sorted(LITE_EXCLUDE_GEOIP))}")
    print(f"  happ/geosite.dat: {lite_gs_cats} categories, "
          f"{lite_gs_doms} domains, {len(lite_gs_data):,} bytes")
    print(f"  happ/geoip.dat:   {lite_gi_cats} categories, "
          f"{lite_gi_cids} CIDRs, {len(lite_gi_data):,} bytes")

    # ── Generate routing configs ────────────────────────────────
    generate_routing_configs()

    # ── Summary ───────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  V2Ray dat build complete")
    print("=" * 55)
    print(f"  v2ray/geosite.dat       ({len(geosite_data):,} bytes)")
    print(f"  v2ray/geoip.dat         ({len(geoip_data):,} bytes)")
    print(f"  v2ray/happ/geosite.dat  ({len(lite_gs_data):,} bytes)")
    print(f"  v2ray/happ/geoip.dat    ({len(lite_gi_data):,} bytes)")
    print(f"  v2ray/happ/  default.json (lite) + full.json")
    print(f"  v2ray/incy/  default.json (lite) + full.json")
    print(f"  v2ray/v2raytun/routing.json + routing_base64.txt + deeplink")


# ══════════════════════════════════════════════════════════════
#   Routing JSON configs for Happ / INCY
# ══════════════════════════════════════════════════════════════

# Base config (shared between lite and full)
_BASE_CONFIG = {
    "Name": "DigneZzZ",
    "GlobalProxy": "true",
    "UseChunkFiles": "true",
    "RemoteDns": "8.8.8.8",
    "DomesticDns": "77.88.8.8",
    "RemoteDNSType": "DoH",
    "RemoteDNSDomain": "https://8.8.8.8/dns-query",
    "RemoteDNSIP": "8.8.8.8",
    "DomesticDNSType": "DoH",
    "DomesticDNSDomain": "https://77.88.8.8/dns-query",
    "DomesticDNSIP": "77.88.8.8",
    "LastUpdated": "",
    "DnsHosts": {},
    "RouteOrder": "block-proxy-direct",
    "DirectSites": [
        "geosite:private",
        "geosite:category-ru",
        "geosite:whitelist",
        "geosite:microsoft",
        "geosite:apple",
        "geosite:google-play",
        "geosite:epicgames",
        "geosite:riot",
        "geosite:escapefromtarkov",
        "geosite:steam",
        "geosite:origin",
        "geosite:twitch",
        "geosite:pinterest",
        "geosite:faceit",
    ],
    "DirectIp": [
        "geoip:private",
        "geoip:whitelist",
    ],
    "BlockSites": [
        "geosite:win-spy",
        "geosite:torrent",
        "geosite:category-ads",
    ],
    "BlockIp": [],
    "DomainStrategy": "IPIfNonMatch",
    "FakeDNS": "false",
}

# Variants: (filename, geo URLs, ProxySites, ProxyIp)
ROUTING_VARIANTS = {
    "default": {
        "label": "lite",
        "Geoipurl": f"{CDN_BASE}/happ/geoip.dat",
        "Geositeurl": f"{CDN_BASE}/happ/geosite.dat",
        "ProxySites": [
            "geosite:github",
            "geosite:twitch-ads",
            "geosite:youtube",
            "geosite:telegram",
            "geosite:google-deepmind",
        ],
        "ProxyIp": [],
    },
    "full": {
        "label": "full",
        "Geoipurl": f"{CDN_BASE}/geoip.dat",
        "Geositeurl": f"{CDN_BASE}/geosite.dat",
        "ProxySites": [
            "geosite:github",
            "geosite:twitch-ads",
            "geosite:youtube",
            "geosite:telegram",
            "geosite:google-deepmind",
            "geosite:category-geoblock-ru",
            "geosite:community",
        ],
        "ProxyIp": [
            "geoip:blocked-ru",
        ],
    },
}


def generate_routing_configs():
    """Generate Happ and INCY routing JSON configs + deeplinks."""
    print("\n" + "=" * 55)
    print("  Generating routing configs")
    print("=" * 55)

    ts = str(int(time.time()))

    for client in ("happ", "incy"):
        client_dir = OUT_DIR / client
        client_dir.mkdir(parents=True, exist_ok=True)

        for fname, variant in ROUTING_VARIANTS.items():
            config = dict(_BASE_CONFIG)
            config["Name"] = f"DigneZzZ ({variant['label']})"
            config["LastUpdated"] = ts
            config["Geoipurl"] = variant["Geoipurl"]
            config["Geositeurl"] = variant["Geositeurl"]
            config["ProxySites"] = variant["ProxySites"]
            config["ProxyIp"] = variant["ProxyIp"]

            # Write JSON
            json_path = client_dir / f"{fname}.json"
            with open(json_path, "w") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"  {client}/{fname}.json [{variant['label']}]")

            # Generate deeplink
            json_compact = json.dumps(config, separators=(",", ":"), ensure_ascii=False)
            b64 = base64.b64encode(json_compact.encode()).decode()
            deeplink = f"{client}://routing/onadd/{b64}"

            dl_path = client_dir / f"{fname}_deeplink.txt"
            dl_path.write_text(deeplink)
            print(f"  {client}/{fname}_deeplink.txt ({len(b64)} chars)")

    # ── V2RayTUN routing config ───────────────────────────────
    generate_v2raytun_config()


# ══════════════════════════════════════════════════════════════
#   V2RayTUN routing config (standard V2Ray/Xray JSON format)
# ══════════════════════════════════════════════════════════════

# V2RayTUN uses built-in geosite.dat/geoip.dat (v2fly/v2ray-core standard),
# so we reference standard category names, not our custom ones.
# V2RayTUN requires UUID "id" on root and every rule, plus "__name__" labels.
# Rules with "domain" field also need "domainMatcher": "hybrid".

def _v2raytun_uuid(name: str) -> str:
    """Deterministic UUID-5 so IDs are stable across builds."""
    import uuid
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"v2raytun.routing.{name}")).upper()

V2RAYTUN_ROUTING = {
    "domainStrategy": "IPIfNonMatch",
    "id": _v2raytun_uuid("root"),
    "name": "DigneZzZ Routing",
    "domainMatcher": "hybrid",
    "balancers": [],
    "rules": [
        # ── BLOCK: ads, telemetry, trackers ──────────────────
        {
            "type": "field",
            "id": _v2raytun_uuid("block-ads"),
            "__name__": "Block Ads & Trackers",
            "domainMatcher": "hybrid",
            "domain": [
                "geosite:category-ads-all",
                "geosite:win-spy",
                "geosite:win-extra",
            ],
            "outboundTag": "block",
        },
        # ── BLOCK: QUIC (forces HTTP/2 for better proxy compat)
        {
            "type": "field",
            "id": _v2raytun_uuid("block-quic"),
            "__name__": "Block QUIC",
            "port": "443",
            "network": "udp",
            "outboundTag": "block",
        },
        # ── DIRECT: private/local networks ───────────────────
        {
            "type": "field",
            "id": _v2raytun_uuid("direct-private-ip"),
            "__name__": "Direct Private IPs",
            "ip": ["geoip:private"],
            "outboundTag": "direct",
        },
        {
            "type": "field",
            "id": _v2raytun_uuid("direct-private-domain"),
            "__name__": "Direct Private Domains",
            "domainMatcher": "hybrid",
            "domain": ["geosite:private"],
            "outboundTag": "direct",
        },
        # ── DIRECT: Russian sites and services ───────────────
        {
            "type": "field",
            "id": _v2raytun_uuid("direct-ru-services"),
            "__name__": "Direct RU Services",
            "domainMatcher": "hybrid",
            "domain": [
                "geosite:category-ru",
                "geosite:apple",
                "geosite:microsoft",
                "geosite:steam",
                "geosite:epicgames",
                "geosite:pinterest",
                "geosite:google-play",
                "geosite:origin",
                "geosite:twitch",
            ],
            "outboundTag": "direct",
        },
        {
            "type": "field",
            "id": _v2raytun_uuid("direct-ru-tlds"),
            "__name__": "Direct RU TLDs",
            "domainMatcher": "hybrid",
            "domain": [
                "regexp:.*\\.ru$",
                "regexp:.*\\.su$",
                "regexp:.*\\.xn--p1ai$",
            ],
            "outboundTag": "direct",
        },
        {
            "type": "field",
            "id": _v2raytun_uuid("direct-ru-ip"),
            "__name__": "Direct RU IPs",
            "ip": ["geoip:ru"],
            "outboundTag": "direct",
        },
        # ── PROXY: everything else ───────────────────────────
        {
            "type": "field",
            "id": _v2raytun_uuid("proxy-all"),
            "__name__": "Proxy All",
            "port": "0-65535",
            "outboundTag": "proxy",
        },
    ],
}


def generate_v2raytun_config():
    """Generate V2RayTUN routing JSON + base64-encoded header value."""
    print("\n" + "=" * 55)
    print("  Generating V2RayTUN routing config")
    print("=" * 55)

    tun_dir = OUT_DIR / "v2raytun"
    tun_dir.mkdir(parents=True, exist_ok=True)

    # Write readable JSON
    json_path = tun_dir / "routing.json"
    with open(json_path, "w") as f:
        json.dump(V2RAYTUN_ROUTING, f, indent=2, ensure_ascii=False)
    print(f"  v2raytun/routing.json")

    # Write base64-encoded (for subscription header)
    json_compact = json.dumps(V2RAYTUN_ROUTING, separators=(",", ":"), ensure_ascii=False)
    b64 = base64.b64encode(json_compact.encode()).decode()

    b64_path = tun_dir / "routing_base64.txt"
    b64_path.write_text(b64)
    print(f"  v2raytun/routing_base64.txt ({len(b64)} chars)")

    # Write ready-to-use header line
    header_path = tun_dir / "routing_header.txt"
    header_path.write_text(f'routing: "{b64}"')
    print(f"  v2raytun/routing_header.txt")

    # Write deeplink (v2rayTun://import_route/<base64>)
    deeplink = f"v2rayTun://import_route/{b64}"
    dl_path = tun_dir / "routing_deeplink.txt"
    dl_path.write_text(deeplink)
    print(f"  v2raytun/routing_deeplink.txt")


if __name__ == "__main__":
    build()
