#!/usr/bin/env python3
"""Update README.md: wrap deeplinks through r.far.ovh redirect service.

Idempotent — safe to run after every build. Replaces the Quick import
section and V2RayTUN Способ 3 deeplink with redirect-wrapped URLs so
they render as clickable https:// links on GitHub.
"""
import re
from urllib.parse import quote

REDIRECT = "https://r.far.ovh/?url="


def read_dl(path):
    with open(path) as f:
        return f.read().strip()


def wrap(deeplink):
    """Wrap a custom-scheme deeplink through the redirect service."""
    return REDIRECT + quote(deeplink, safe='')


# ── Read raw deeplinks from generated files ───────────────────
happ_lite = wrap(read_dl('v2ray/happ/default_deeplink.txt'))
happ_full = wrap(read_dl('v2ray/happ/full_deeplink.txt'))
incy_lite = wrap(read_dl('v2ray/incy/default_deeplink.txt'))
incy_full = wrap(read_dl('v2ray/incy/full_deeplink.txt'))
v2raytun  = wrap(read_dl('v2ray/v2raytun/routing_deeplink.txt'))

# ── Build replacement sections ────────────────────────────────
QUICK_IMPORT = (
    '### Quick import (deeplink)\n'
    '\n'
    'Open the deeplink on your device with Happ/INCY installed:\n'
    '\n'
    '| Variant | Happ | INCY | .dat size |\n'
    '|---|---|---|---|\n'
    f'| **Lite** (recommended for iOS) | [\U0001F4F2 Import]({happ_lite}) | [\U0001F4F2 Import]({incy_lite}) | ~500 KB |\n'
    f'| **Full** (all RKN lists) | [\U0001F4F2 Import]({happ_full}) | [\U0001F4F2 Import]({incy_full}) | ~2.6 MB |\n'
    '\n'
    '**V2RayTUN:**\n'
    '\n'
    f'| [\U0001F4F2 Import]({v2raytun}) |\n'
    '|---|\n'
    '\n'
    '> Deeplink files: [`happ/`](v2ray/happ/) \u00b7 [`incy/`](v2ray/incy/) \u00b7 [`v2raytun/`](v2ray/v2raytun/)'
)

V2RAYTUN_DL = f'**Способ 3 — Deeplink:**\nОткройте на устройстве: [\U0001F4F2 Import]({v2raytun})'

# ── Apply replacements ────────────────────────────────────────
with open('README.md') as f:
    content = f.read()

# 1) Replace the Quick import section (from ### Quick import to ### Manual import)
content = re.sub(
    r'### Quick import \(deeplink\).*?(?=### Manual import)',
    QUICK_IMPORT + '\n\n',
    content,
    flags=re.DOTALL,
)

# 2) Replace V2RayTUN Способ 3 deeplink
content = re.sub(
    r'\*\*Способ 3 — Deeplink:\*\*\n[^\n]*\[📲 Import\]\([^\)]+\)',
    V2RAYTUN_DL,
    content,
)

with open('README.md', 'w') as f:
    f.write(content)
print("OK: README updated with redirect-wrapped deeplinks")
