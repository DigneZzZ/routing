#!/usr/bin/env python3
"""
build.py — скачивает текстовые списки доменов/IP из открытых источников,
объединяет в 7 компактных rule-set'ов (формат: text для mihomo).

Итоговые файлы:
  release/proxy.list      — домены → PROXY (telegram, github, refilter, banned)
  release/direct.list     — домены → DIRECT (RU, microsoft, apple, torrent...)
  release/reject.list     — домены → REJECT (ads, win-spy)
  release/youtube.list    — домены → 📺 YouTube
  release/ai.list         — домены → 🤖 AI
  release/games.list      — домены → 🎮 Игры (steam, epic, riot, eft...)
  release/proxy-ip.list   — IP → PROXY (telegram, cloudflare)
  release/direct-ip.list  — IP → DIRECT (private, RU)
"""

import os
import sys
import urllib.request
import time
from pathlib import Path
from collections import OrderedDict

REPO_DIR = Path(__file__).parent
RELEASE_DIR = REPO_DIR / "release"
SRC_DIR = REPO_DIR / "src"

# ─── Источники ───────────────────────────────────────────────
# Формат: (имя, url) — скачиваем text/list из MetaCubeX и legiz

MCX = "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo"
REFILTER = "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main"

SOURCES = {
    # === PROXY домены ===
    "proxy": {
        "behavior": "domain",
        "sources": [
            ("telegram",    f"{MCX}/geosite/telegram.list"),
            ("github",      f"{MCX}/geosite/github.list"),
        ],
        "extra_domains": [
            # ru-banned (заблокированные РКН)
            "+.habr.com", "+.kemono.su", "+.jut.su", "+.namecheap.com",
            "+.theins.ru", "+.tvrain.ru", "+.novayagazeta.ru", "+.moscowtimes.ru",
            "+.webhook.site", "+.kara.su", "+.the-village.ru", "+.snob.ru",
            "+.echo.msk.ru",
            # хостинги / сервисы
            "+.openode.xyz", "+.royalehosting.net", "+.alfahost.io", "+.alfahost.pro",
            "+.betterstack.com", "+.sshid.io", "+.vdsina.com", "+.hostzealot.com",
            "+.kamatera.com", "+.coinify.com", "+.ngrok-free.dev", "+.arkoselabs.com",
            "+.4pda.to", "+.autodesk.com", "+.qwant.com",
            # twitch ads (через прокси для фикса битрейта)
            "+.ads.twitch.tv",
        ]
    },

    # === DIRECT домены ===
    "direct": {
        "behavior": "domain",
        "sources": [
            ("category-ru", f"{MCX}/geosite/category-ru.list"),
            ("microsoft",   f"{MCX}/geosite/microsoft.list"),
            ("apple",       f"{MCX}/geosite/apple.list"),
            ("google-play", f"{MCX}/geosite/google-play.list"),
            ("twitch",      f"{MCX}/geosite/twitch.list"),
            ("pinterest",   f"{MCX}/geosite/pinterest.list"),
            ("private",     f"{MCX}/geosite/private.list"),
        ],
        "extra_domains": []
    },

    # === REJECT домены ===
    "reject": {
        "behavior": "domain",
        "sources": [
            ("category-ads", f"{MCX}/geosite/category-ads-all.list"),
            ("win-spy",      f"{MCX}/geosite/win-spy.list"),
        ],
        "extra_domains": []
    },

    # === YouTube домены ===
    "youtube": {
        "behavior": "domain",
        "sources": [
            ("youtube", f"{MCX}/geosite/youtube.list"),
        ],
        "extra_domains": []
    },

    # === AI домены ===
    "ai": {
        "behavior": "domain",
        "sources": [
            ("category-ai", f"{MCX}/geosite/category-ai-!cn.list"),
        ],
        "extra_domains": [
            "+.openai.com", "+.chatgpt.com", "+.anthropic.com", "+.claude.ai",
            "+.gemini.google.com", "+.aistudio.google.com",
            "+.perplexity.ai", "+.midjourney.com", "+.huggingface.co",
            "+.deepl.com", "+.grammarly.com", "+.notion.so",
            "+.elevenlabs.io", "+.civitai.com", "+.stability.ai",
            "+.replicate.com", "+.runway.ml", "+.leonardo.ai",
            "+.luma.ai", "+.poe.com", "+.character.ai",
            "+.together.ai", "+.cohere.ai", "+.topaz.io",
        ]
    },

    # === Games домены ===
    "games": {
        "behavior": "domain",
        "sources": [
            ("steam",       f"{MCX}/geosite/steam.list"),
            ("epicgames",   f"{MCX}/geosite/epicgames.list"),
            ("origin",      f"{MCX}/geosite/origin.list"),
            ("escapefromtarkov", f"{MCX}/geosite/escapefromtarkov.list"),
            ("faceit",      f"{MCX}/geosite/faceit.list"),
        ],
        "extra_domains": [
            # Riot Games (нет отдельного .list)
            "+.riotgames.com", "+.leagueoflegends.com", "+.valorant.com",
            "+.riotcdn.net", "+.lolstatic.com", "+.lolesports.com",
            # Roblox
            "+.roblox.com", "+.rbxcdn.com", "+.roblox.net",
            "+.rbxcdn.net", "+.robloxdev.com",
        ]
    },

    # === PROXY IP ===
    "proxy-ip": {
        "behavior": "ipcidr",
        "sources": [
            ("telegram-ip",  f"{MCX}/geoip/telegram.list"),
            ("cloudflare-ip", f"{MCX}/geoip/cloudflare.list"),
        ],
        "extra_domains": []
    },

    # === DIRECT IP ===
    "direct-ip": {
        "behavior": "ipcidr",
        "sources": [
            ("private-ip", f"{MCX}/geoip/private.list"),
        ],
        "extra_domains": []
    },
}

# Re:filter lists — скачиваем как текст напрямую из 1andrevich/Re-filter-lists
REFILTER_LISTS = OrderedDict([
    ("refilter-domain", {
        "url": f"{REFILTER}/domains_all.lst",
        "behavior": "domain",
    }),
    ("refilter-ip", {
        "url": f"{REFILTER}/ipsum.lst",
        "behavior": "ipcidr",
    }),
    ("refilter-community", {
        "url": f"{REFILTER}/community.lst",
        "behavior": "domain",
    }),
])

# Classical YAML (process-based rules) — download and sanitize (strip comments)
CLASSICAL_YAML = {
    "proc-games":   "https://raw.githubusercontent.com/roscomvpn/custom-category/release/mihomo/games.yaml",
    "proc-torrent": "https://raw.githubusercontent.com/legiz-ru/mihomo-rule-sets/main/other/torrent-clients.yaml",
    "proc-ru":      "https://raw.githubusercontent.com/roscomvpn/custom-category/release/mihomo/ru-apps.yaml",
}


def download(url, retries=3):
    """Download URL content as text."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "routing/1.0"})
            resp = urllib.request.urlopen(req, timeout=30)
            return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            if attempt == retries - 1:
                print(f"  WARN: failed to download {url}: {e}")
                return None
            time.sleep(2)


def parse_list(text):
    """Parse a .list file into clean domain/IP entries."""
    entries = set()
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Normalize: some lists have comments after domains
        if " #" in line:
            line = line.split(" #")[0].strip()
        if "\t" in line:
            line = line.split("\t")[0].strip()
        if line:
            entries.add(line)
    return entries


def build():
    """Main build process."""
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    SRC_DIR.mkdir(parents=True, exist_ok=True)

    stats = {}

    for name, config in SOURCES.items():
        print(f"\n▸ Building {name}.list")
        all_entries = set()

        # Download and merge all sources
        for src_name, url in config["sources"]:
            text = download(url)
            if text:
                entries = parse_list(text)
                print(f"  + {src_name}: {len(entries)} entries")
                all_entries.update(entries)
            else:
                print(f"  ! {src_name}: skipped (download failed)")

        # Add extra static entries
        for entry in config.get("extra_domains", []):
            all_entries.add(entry)

        if config.get("extra_domains"):
            print(f"  + inline: {len(config['extra_domains'])} entries")

        # Sort and deduplicate
        sorted_entries = sorted(all_entries, key=lambda x: x.lstrip("+.").lower())

        # Write output
        out_path = RELEASE_DIR / f"{name}.list"
        with open(out_path, "w") as f:
            f.write(f"# {name} — auto-generated, do not edit\n")
            f.write(f"# entries: {len(sorted_entries)}\n")
            for entry in sorted_entries:
                f.write(f"{entry}\n")

        stats[name] = len(sorted_entries)
        print(f"  → {out_path.name}: {len(sorted_entries)} entries total")

    # Download Re:filter lists (text format)
    print(f"\n▸ Downloading Re:filter lists")
    for name, config in REFILTER_LISTS.items():
        text = download(config["url"])
        if text:
            entries = parse_list(text)
            # For domain lists: add +. prefix for subdomain matching
            if config["behavior"] == "domain":
                normalized = set()
                for entry in entries:
                    if entry.startswith(("DOMAIN", "IP-CIDR", "+.", ".")):
                        normalized.add(entry)
                    else:
                        normalized.add(f"+.{entry}")
                entries = normalized
            sorted_entries = sorted(entries, key=lambda x: x.lstrip("+.").lower())
            out_path = RELEASE_DIR / f"{name}.list"
            with open(out_path, "w") as f:
                f.write(f"# {name} — auto-generated from Re:filter\n")
                f.write(f"# source: 1andrevich/Re-filter-lists\n")
                f.write(f"# entries: {len(sorted_entries)}\n")
                for entry in sorted_entries:
                    f.write(f"{entry}\n")
            stats[name] = len(sorted_entries)
            print(f"  OK  {name}.list ({len(sorted_entries)} entries)")
        else:
            print(f"  WARN: failed to download {name}")

    # Download and sanitize classical YAML files (strip comments to hide source)
    print(f"\n▸ Downloading classical YAML files")
    for name, url in CLASSICAL_YAML.items():
        text = download(url)
        if text:
            # Strip comments and empty lines, keep only payload entries
            lines = []
            in_payload = False
            for line in text.split("\n"):
                stripped = line.strip()
                if stripped == "payload:":
                    lines.append("payload:")
                    in_payload = True
                    continue
                if in_payload and stripped.startswith("- "):
                    # Remove inline comments
                    rule = stripped
                    if " #" in rule:
                        rule = rule.split(" #")[0].rstrip()
                    lines.append(f"  {rule}")
            out_path = RELEASE_DIR / f"{name}.yaml"
            with open(out_path, "w") as f:
                f.write("\n".join(lines) + "\n")
            print(f"  OK  {name}.yaml ({len([l for l in lines if l.startswith('  -')])} rules)")
        else:
            print(f"  WARN: failed to download {name}")

    # Summary
    print("\n" + "=" * 50)
    print("  Build complete")
    print("=" * 50)
    total = sum(stats.values())
    for name, count in stats.items():
        print(f"  {name}.list: {count} entries")
    print(f"  ---")
    print(f"  Total: {total} entries in {len(stats)} files")


if __name__ == "__main__":
    build()
