# routing

Consolidated MihoMo rule-sets, Remnawave template, and V2Ray/Xray geo-data.

## Structure

```
release/              # MihoMo rule-sets (auto-generated)
├── proxy.list        # domains → PROXY
├── direct.list       # domains → DIRECT
├── reject.list       # domains → REJECT
├── youtube.list      # domains → 📺 YouTube
├── ai.list           # domains → 🤖 AI
├── games.list        # domains → 🎮 Games
├── proxy-ip.list     # IPs → PROXY (telegram + cloudflare)
├── direct-ip.list    # IPs → DIRECT (private ranges)
├── refilter-domain.list  # RKN bypass domains (Re:filter)
├── refilter-ip.list      # RKN bypass IPs (Re:filter)
├── refilter-community.list # Services blocking Russia (Re:filter)
├── proc-games.yaml   # game process names (classical)
├── proc-torrent.yaml # torrent client process names (classical)
└── proc-ru.yaml      # Russian app process names (classical)

v2ray/                # V2Ray/Xray geo-data + routing configs (auto-generated)
├── geosite.dat       # 24 domain categories (protobuf, full)
├── geoip.dat         # 3 IP categories (protobuf, full)
├── happ/
│   ├── geosite.dat   # lite — without heavy RKN lists (for mobile)
│   ├── geoip.dat     # lite — without blocked-ru IPs (for mobile)
│   ├── default.json  # Happ routing config (lite)
│   ├── default_deeplink.txt
│   ├── full.json     # Happ routing config (full)
│   └── full_deeplink.txt
└── incy/
    ├── default.json  # INCY routing config (lite)
    ├── default_deeplink.txt
    ├── full.json     # INCY routing config (full)
    └── full_deeplink.txt
└── v2raytun/
    ├── routing.json          # V2RayTUN routing (readable)
    ├── routing_base64.txt    # Base64-encoded (for subscription header)
    └── routing_header.txt    # Ready-to-use header line

build.py              # MihoMo rule-set builder
build_dat.py          # V2Ray .dat + routing config builder
template.yaml         # Remnawave subscription template
```

## Auto-update

Everything is rebuilt daily via GitHub Actions (04:00 UTC).

Manual: **Actions → Build Rule-Sets → Run workflow**

## Local build

```bash
python3 build.py       # MihoMo rule-sets → release/
python3 build_dat.py   # V2Ray .dat files → v2ray/
```

---

## MihoMo Template

`template.yaml` — ready-to-use Remnawave subscription template.

### Proxy Groups

| Group | Default | Description |
|---|---|---|
| 🛡️ VPN | ⚡️ Auto | Main group — strategy switch |
| 📺 YouTube | VPN | Separate node for YouTube |
| 💬 Discord | VPN | Separate node for Discord |
| 🤖 AI | VPN | ChatGPT, Claude, Gemini, Midjourney… |
| 🎮 Games | DIRECT | Steam, Epic, Riot, Roblox, EfT, FaceIT |
| 🏠 RU | DIRECT | Russian sites and services |

### Routing

- **REJECT** — ads, Windows telemetry, QUIC, DoQ, IPv6
- **DIRECT** — torrents, Microsoft, Apple, Google Play, Pinterest, Twitch, RU sites
- **PROXY** — Telegram, GitHub, RKN bypass (refilter), IP-check
- **Groups** — YouTube, Discord, AI, Games via separate proxy-groups

---

## V2Ray / Xray Geo-Data

`v2ray/geosite.dat` and `v2ray/geoip.dat` — standard protobuf geo-files compatible with V2Ray, Xray, Sing-box and other clients.

> **Lite versions** (`v2ray/happ/geosite.dat`, `v2ray/happ/geoip.dat`) — облегчённые .dat файлы для мобильных клиентов. Подробности в разделе [Lite vs Full](#lite-vs-full).
>
> Full: ~2.6 MB → Lite: ~500 KB (**-81%**)

### Usage

```
https://raw.githubusercontent.com/DigneZzZ/routing/main/v2ray/geosite.dat
https://raw.githubusercontent.com/DigneZzZ/routing/main/v2ray/geoip.dat
```

Or via jsDelivr CDN:
```
https://cdn.jsdelivr.net/gh/DigneZzZ/routing@main/v2ray/geosite.dat
https://cdn.jsdelivr.net/gh/DigneZzZ/routing@main/v2ray/geoip.dat
```

### geosite.dat categories (24)

| Category | Description | Routing |
|---|---|---|
| `WHITELIST` | Russian services (Yandex, VK, Sber, Gosuslugi…) | DIRECT |
| `CATEGORY-RU` | Russian domains (banks, finance) | DIRECT |
| `PRIVATE` | Local/private domains | DIRECT |
| `CATEGORY-GEOBLOCK-RU` | Blocked in Russia (needs proxy) | PROXY |
| `COMMUNITY` | Services blocking Russia (Discord, WhatsApp…) | PROXY |
| `CATEGORY-ADS` | Advertising domains | BLOCK |
| `WIN-SPY` | Windows telemetry | BLOCK |
| `TORRENT` | Torrent trackers | BLOCK |
| `YOUTUBE` | YouTube | PROXY |
| `TELEGRAM` | Telegram | PROXY |
| `GITHUB` | GitHub | PROXY |
| `STEAM` | Steam | PROXY |
| `EPICGAMES` | Epic Games | PROXY |
| `ORIGIN` | EA Games | PROXY |
| `APPLE` | Apple services | PROXY |
| `MICROSOFT` | Microsoft services | PROXY |
| `GOOGLE-PLAY` | Google Play | PROXY |
| `GOOGLE-DEEPMIND` | AI services (Gemini, ChatGPT, Claude…) | PROXY |
| `TWITCH` | Twitch | PROXY |
| `TWITCH-ADS` | Twitch ads | BLOCK |
| `PINTEREST` | Pinterest | PROXY |
| `ESCAPEFROMTARKOV` | Escape from Tarkov | PROXY |
| `FACEIT` | Faceit | PROXY |
| `RIOT` | Riot Games (LoL, Valorant) | PROXY |

### geoip.dat categories (3)

| Category | Description | Routing |
|---|---|---|
| `WHITELIST` | Russian IP ranges | DIRECT |
| `PRIVATE` | RFC1918 private ranges | DIRECT |
| `BLOCKED-RU` | IPs blocked in Russia (Re:filter) | PROXY |

### Example V2Ray/Xray config

```json
{
  "GlobalProxy": true,
  "RouteOrder": "block-proxy-direct",
  "DomainStrategy": "IPIfNonMatch",
  "DirectSites": ["geosite:private", "geosite:whitelist"],
  "DirectIp": ["geoip:private", "geoip:whitelist"],
  "ProxySites": ["geosite:category-geoblock-ru", "geosite:community"],
  "ProxyIp": ["geoip:blocked-ru"],
  "BlockSites": ["geosite:win-spy", "geosite:torrent", "geosite:category-ads"]
}
```

> With `GlobalProxy=true` the ProxySites/ProxyIp categories above are optional — unmatched traffic goes through proxy by default. The lite .dat files omit these heavy categories to reduce size.

---

## Happ / INCY Routing

Ready-to-use routing configs for **Happ** and **INCY** clients. GlobalProxy mode — everything through VPN, Russian sites direct.

### Lite vs Full

Оба варианта **функционально идентичны** — маршрутизация работает одинаково. Разница только в размере .dat файлов и способе обработки заблокированных ресурсов.

**Проблема:** Полные .dat файлы (~2.6 MB) содержат списки РКН — 81 000+ заблокированных доменов и 38 000+ IP-диапазонов. На iOS (Happ/INCY) это приводит к превышению лимитов памяти Network Extension, и приложение вылетает.

**Решение:** Lite-вариант исключает три тяжёлых категории:

| Категория | Тип | Записей | Размер | Зачем нужна |
|---|---|---|---|---|
| `CATEGORY-GEOBLOCK-RU` | geosite | ~81 000 доменов | ~1.7 MB | Домены, заблокированные РКН |
| `COMMUNITY` | geosite | ~525 доменов | ~12 KB | Сервисы, блокирующие РФ (Discord, WhatsApp…) |
| `BLOCKED-RU` | geoip | ~38 000 CIDR | ~387 KB | IP-адреса, заблокированные в РФ (Re:filter ipsum) |

**Почему это безопасно:** В конфиге стоит `GlobalProxy=true` и `RouteOrder=block-proxy-direct`. Это значит:
1. Сначала проверяются правила **BLOCK** (реклама, телеметрия, торренты)
2. Затем — явные правила **PROXY** (YouTube, Telegram, GitHub…)
3. Затем — правила **DIRECT** (российские сайты, приватные сети)
4. **Всё остальное** автоматически идёт через **PROXY**

То есть заблокированные домены/IP и так попадут в прокси по умолчанию — явные списки РКН для этого **не нужны**. Они дают лишь marginal выигрыш в скорости DNS-резолва (прямое совпадение vs fallback), но ценой 2+ MB памяти на мобильном устройстве.

| | Lite | Full |
|---|---|---|
| geosite.dat | 100 KB (22 категории, ~4 400 доменов) | 1.8 MB (24 категории, ~86 000 доменов) |
| geoip.dat | 385 KB (2 категории, ~25 000 CIDR) | 763 KB (3 категории, ~63 000 CIDR) |
| **Итого** | **~500 KB** | **~2.6 MB** |
| iOS (Happ/INCY) | ✅ Работает | ❌ Вылетает (превышение памяти) |
| Android / Desktop | ✅ Работает | ✅ Работает |

### Quick import (deeplink)

Open the deeplink on your device with Happ/INCY installed:

| Variant | Happ | INCY | .dat size |
|---|---|---|---|
| **Lite** (recommended for iOS) | [📲 Import](https://r.far.ovh/?url=happ%3A%2F%2Frouting%2Fonadd%2FeyJOYW1lIjoiRGlnbmVaelogKGxpdGUpIiwiR2xvYmFsUHJveHkiOiJ0cnVlIiwiVXNlQ2h1bmtGaWxlcyI6InRydWUiLCJSZW1vdGVEbnMiOiI4LjguOC44IiwiRG9tZXN0aWNEbnMiOiI3Ny44OC44LjgiLCJSZW1vdGVETlNUeXBlIjoiRG9IIiwiUmVtb3RlRE5TRG9tYWluIjoiaHR0cHM6Ly84LjguOC44L2Rucy1xdWVyeSIsIlJlbW90ZUROU0lQIjoiOC44LjguOCIsIkRvbWVzdGljRE5TVHlwZSI6IkRvSCIsIkRvbWVzdGljRE5TRG9tYWluIjoiaHR0cHM6Ly83Ny44OC44LjgvZG5zLXF1ZXJ5IiwiRG9tZXN0aWNETlNJUCI6Ijc3Ljg4LjguOCIsIkxhc3RVcGRhdGVkIjoiMTc3Mzk4MTQyMyIsIkRuc0hvc3RzIjp7fSwiUm91dGVPcmRlciI6ImJsb2NrLXByb3h5LWRpcmVjdCIsIkRpcmVjdFNpdGVzIjpbImdlb3NpdGU6cHJpdmF0ZSIsImdlb3NpdGU6Y2F0ZWdvcnktcnUiLCJnZW9zaXRlOndoaXRlbGlzdCIsImdlb3NpdGU6bWljcm9zb2Z0IiwiZ2Vvc2l0ZTphcHBsZSIsImdlb3NpdGU6Z29vZ2xlLXBsYXkiLCJnZW9zaXRlOmVwaWNnYW1lcyIsImdlb3NpdGU6cmlvdCIsImdlb3NpdGU6ZXNjYXBlZnJvbXRhcmtvdiIsImdlb3NpdGU6c3RlYW0iLCJnZW9zaXRlOm9yaWdpbiIsImdlb3NpdGU6dHdpdGNoIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOmZhY2VpdCJdLCJEaXJlY3RJcCI6WyJnZW9pcDpwcml2YXRlIiwiZ2VvaXA6d2hpdGVsaXN0Il0sIkJsb2NrU2l0ZXMiOlsiZ2Vvc2l0ZTp3aW4tc3B5IiwiZ2Vvc2l0ZTp0b3JyZW50IiwiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMiXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIiwiR2VvaXB1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvRGlnbmVaelovcm91dGluZ0BtYWluL3YycmF5L2hhcHAvZ2VvaXAuZGF0IiwiR2Vvc2l0ZXVybCI6Imh0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9naC9EaWduZVp6Wi9yb3V0aW5nQG1haW4vdjJyYXkvaGFwcC9nZW9zaXRlLmRhdCIsIlByb3h5U2l0ZXMiOlsiZ2Vvc2l0ZTpnaXRodWIiLCJnZW9zaXRlOnR3aXRjaC1hZHMiLCJnZW9zaXRlOnlvdXR1YmUiLCJnZW9zaXRlOnRlbGVncmFtIiwiZ2Vvc2l0ZTpnb29nbGUtZGVlcG1pbmQiXSwiUHJveHlJcCI6W119) | [📲 Import](https://r.far.ovh/?url=incy%3A%2F%2Frouting%2Fonadd%2FeyJOYW1lIjoiRGlnbmVaelogKGxpdGUpIiwiR2xvYmFsUHJveHkiOiJ0cnVlIiwiVXNlQ2h1bmtGaWxlcyI6InRydWUiLCJSZW1vdGVEbnMiOiI4LjguOC44IiwiRG9tZXN0aWNEbnMiOiI3Ny44OC44LjgiLCJSZW1vdGVETlNUeXBlIjoiRG9IIiwiUmVtb3RlRE5TRG9tYWluIjoiaHR0cHM6Ly84LjguOC44L2Rucy1xdWVyeSIsIlJlbW90ZUROU0lQIjoiOC44LjguOCIsIkRvbWVzdGljRE5TVHlwZSI6IkRvSCIsIkRvbWVzdGljRE5TRG9tYWluIjoiaHR0cHM6Ly83Ny44OC44LjgvZG5zLXF1ZXJ5IiwiRG9tZXN0aWNETlNJUCI6Ijc3Ljg4LjguOCIsIkxhc3RVcGRhdGVkIjoiMTc3Mzk4MTQyMyIsIkRuc0hvc3RzIjp7fSwiUm91dGVPcmRlciI6ImJsb2NrLXByb3h5LWRpcmVjdCIsIkRpcmVjdFNpdGVzIjpbImdlb3NpdGU6cHJpdmF0ZSIsImdlb3NpdGU6Y2F0ZWdvcnktcnUiLCJnZW9zaXRlOndoaXRlbGlzdCIsImdlb3NpdGU6bWljcm9zb2Z0IiwiZ2Vvc2l0ZTphcHBsZSIsImdlb3NpdGU6Z29vZ2xlLXBsYXkiLCJnZW9zaXRlOmVwaWNnYW1lcyIsImdlb3NpdGU6cmlvdCIsImdlb3NpdGU6ZXNjYXBlZnJvbXRhcmtvdiIsImdlb3NpdGU6c3RlYW0iLCJnZW9zaXRlOm9yaWdpbiIsImdlb3NpdGU6dHdpdGNoIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOmZhY2VpdCJdLCJEaXJlY3RJcCI6WyJnZW9pcDpwcml2YXRlIiwiZ2VvaXA6d2hpdGVsaXN0Il0sIkJsb2NrU2l0ZXMiOlsiZ2Vvc2l0ZTp3aW4tc3B5IiwiZ2Vvc2l0ZTp0b3JyZW50IiwiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMiXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIiwiR2VvaXB1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvRGlnbmVaelovcm91dGluZ0BtYWluL3YycmF5L2hhcHAvZ2VvaXAuZGF0IiwiR2Vvc2l0ZXVybCI6Imh0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9naC9EaWduZVp6Wi9yb3V0aW5nQG1haW4vdjJyYXkvaGFwcC9nZW9zaXRlLmRhdCIsIlByb3h5U2l0ZXMiOlsiZ2Vvc2l0ZTpnaXRodWIiLCJnZW9zaXRlOnR3aXRjaC1hZHMiLCJnZW9zaXRlOnlvdXR1YmUiLCJnZW9zaXRlOnRlbGVncmFtIiwiZ2Vvc2l0ZTpnb29nbGUtZGVlcG1pbmQiXSwiUHJveHlJcCI6W119) | ~500 KB |
| **Full** (all RKN lists) | [📲 Import](https://r.far.ovh/?url=happ%3A%2F%2Frouting%2Fonadd%2FeyJOYW1lIjoiRGlnbmVaelogKGZ1bGwpIiwiR2xvYmFsUHJveHkiOiJ0cnVlIiwiVXNlQ2h1bmtGaWxlcyI6InRydWUiLCJSZW1vdGVEbnMiOiI4LjguOC44IiwiRG9tZXN0aWNEbnMiOiI3Ny44OC44LjgiLCJSZW1vdGVETlNUeXBlIjoiRG9IIiwiUmVtb3RlRE5TRG9tYWluIjoiaHR0cHM6Ly84LjguOC44L2Rucy1xdWVyeSIsIlJlbW90ZUROU0lQIjoiOC44LjguOCIsIkRvbWVzdGljRE5TVHlwZSI6IkRvSCIsIkRvbWVzdGljRE5TRG9tYWluIjoiaHR0cHM6Ly83Ny44OC44LjgvZG5zLXF1ZXJ5IiwiRG9tZXN0aWNETlNJUCI6Ijc3Ljg4LjguOCIsIkxhc3RVcGRhdGVkIjoiMTc3Mzk4MTQyMyIsIkRuc0hvc3RzIjp7fSwiUm91dGVPcmRlciI6ImJsb2NrLXByb3h5LWRpcmVjdCIsIkRpcmVjdFNpdGVzIjpbImdlb3NpdGU6cHJpdmF0ZSIsImdlb3NpdGU6Y2F0ZWdvcnktcnUiLCJnZW9zaXRlOndoaXRlbGlzdCIsImdlb3NpdGU6bWljcm9zb2Z0IiwiZ2Vvc2l0ZTphcHBsZSIsImdlb3NpdGU6Z29vZ2xlLXBsYXkiLCJnZW9zaXRlOmVwaWNnYW1lcyIsImdlb3NpdGU6cmlvdCIsImdlb3NpdGU6ZXNjYXBlZnJvbXRhcmtvdiIsImdlb3NpdGU6c3RlYW0iLCJnZW9zaXRlOm9yaWdpbiIsImdlb3NpdGU6dHdpdGNoIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOmZhY2VpdCJdLCJEaXJlY3RJcCI6WyJnZW9pcDpwcml2YXRlIiwiZ2VvaXA6d2hpdGVsaXN0Il0sIkJsb2NrU2l0ZXMiOlsiZ2Vvc2l0ZTp3aW4tc3B5IiwiZ2Vvc2l0ZTp0b3JyZW50IiwiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMiXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIiwiR2VvaXB1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvRGlnbmVaelovcm91dGluZ0BtYWluL3YycmF5L2dlb2lwLmRhdCIsIkdlb3NpdGV1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvRGlnbmVaelovcm91dGluZ0BtYWluL3YycmF5L2dlb3NpdGUuZGF0IiwiUHJveHlTaXRlcyI6WyJnZW9zaXRlOmdpdGh1YiIsImdlb3NpdGU6dHdpdGNoLWFkcyIsImdlb3NpdGU6eW91dHViZSIsImdlb3NpdGU6dGVsZWdyYW0iLCJnZW9zaXRlOmdvb2dsZS1kZWVwbWluZCIsImdlb3NpdGU6Y2F0ZWdvcnktZ2VvYmxvY2stcnUiLCJnZW9zaXRlOmNvbW11bml0eSJdLCJQcm94eUlwIjpbImdlb2lwOmJsb2NrZWQtcnUiXX0%3D) | [📲 Import](https://r.far.ovh/?url=incy%3A%2F%2Frouting%2Fonadd%2FeyJOYW1lIjoiRGlnbmVaelogKGZ1bGwpIiwiR2xvYmFsUHJveHkiOiJ0cnVlIiwiVXNlQ2h1bmtGaWxlcyI6InRydWUiLCJSZW1vdGVEbnMiOiI4LjguOC44IiwiRG9tZXN0aWNEbnMiOiI3Ny44OC44LjgiLCJSZW1vdGVETlNUeXBlIjoiRG9IIiwiUmVtb3RlRE5TRG9tYWluIjoiaHR0cHM6Ly84LjguOC44L2Rucy1xdWVyeSIsIlJlbW90ZUROU0lQIjoiOC44LjguOCIsIkRvbWVzdGljRE5TVHlwZSI6IkRvSCIsIkRvbWVzdGljRE5TRG9tYWluIjoiaHR0cHM6Ly83Ny44OC44LjgvZG5zLXF1ZXJ5IiwiRG9tZXN0aWNETlNJUCI6Ijc3Ljg4LjguOCIsIkxhc3RVcGRhdGVkIjoiMTc3Mzk4MTQyMyIsIkRuc0hvc3RzIjp7fSwiUm91dGVPcmRlciI6ImJsb2NrLXByb3h5LWRpcmVjdCIsIkRpcmVjdFNpdGVzIjpbImdlb3NpdGU6cHJpdmF0ZSIsImdlb3NpdGU6Y2F0ZWdvcnktcnUiLCJnZW9zaXRlOndoaXRlbGlzdCIsImdlb3NpdGU6bWljcm9zb2Z0IiwiZ2Vvc2l0ZTphcHBsZSIsImdlb3NpdGU6Z29vZ2xlLXBsYXkiLCJnZW9zaXRlOmVwaWNnYW1lcyIsImdlb3NpdGU6cmlvdCIsImdlb3NpdGU6ZXNjYXBlZnJvbXRhcmtvdiIsImdlb3NpdGU6c3RlYW0iLCJnZW9zaXRlOm9yaWdpbiIsImdlb3NpdGU6dHdpdGNoIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOmZhY2VpdCJdLCJEaXJlY3RJcCI6WyJnZW9pcDpwcml2YXRlIiwiZ2VvaXA6d2hpdGVsaXN0Il0sIkJsb2NrU2l0ZXMiOlsiZ2Vvc2l0ZTp3aW4tc3B5IiwiZ2Vvc2l0ZTp0b3JyZW50IiwiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMiXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIiwiR2VvaXB1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvRGlnbmVaelovcm91dGluZ0BtYWluL3YycmF5L2dlb2lwLmRhdCIsIkdlb3NpdGV1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvRGlnbmVaelovcm91dGluZ0BtYWluL3YycmF5L2dlb3NpdGUuZGF0IiwiUHJveHlTaXRlcyI6WyJnZW9zaXRlOmdpdGh1YiIsImdlb3NpdGU6dHdpdGNoLWFkcyIsImdlb3NpdGU6eW91dHViZSIsImdlb3NpdGU6dGVsZWdyYW0iLCJnZW9zaXRlOmdvb2dsZS1kZWVwbWluZCIsImdlb3NpdGU6Y2F0ZWdvcnktZ2VvYmxvY2stcnUiLCJnZW9zaXRlOmNvbW11bml0eSJdLCJQcm94eUlwIjpbImdlb2lwOmJsb2NrZWQtcnUiXX0%3D) | ~2.6 MB |

**V2RayTUN:**

| [📲 Import](https://r.far.ovh/?url=v2rayTun%3A%2F%2Fimport_route%2FeyJkb21haW5TdHJhdGVneSI6IklQSWZOb25NYXRjaCIsImlkIjoiRkU0RDY2REMtMjEwQy01ODU3LUI0RkItOEE5QUJDNDIxRjI1IiwibmFtZSI6IkRpZ25lWnpaIFJvdXRpbmciLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiYmFsYW5jZXJzIjpbXSwicnVsZXMiOlt7InR5cGUiOiJmaWVsZCIsImlkIjoiNjc5OTVCMjItNTAzRC01MzUzLUE5NzQtQjU0QTZCMTMzNzAwIiwiX19uYW1lX18iOiJCbG9jayBBZHMgJiBUcmFja2VycyIsImRvbWFpbk1hdGNoZXIiOiJoeWJyaWQiLCJkb21haW4iOlsiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMtYWxsIiwiZ2Vvc2l0ZTp3aW4tc3B5IiwiZ2Vvc2l0ZTp3aW4tZXh0cmEiXSwib3V0Ym91bmRUYWciOiJibG9jayJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiJCMTI2MDYzRS1GOENDLTVDRDktQjcwNy1FOUIzOUY4MDlBNkIiLCJfX25hbWVfXyI6IkJsb2NrIFFVSUMiLCJwb3J0IjoiNDQzIiwibmV0d29yayI6InVkcCIsIm91dGJvdW5kVGFnIjoiYmxvY2sifSx7InR5cGUiOiJmaWVsZCIsImlkIjoiNUEzOEQzM0QtNUZFQS01OEFCLThDQjktNDJERDk3NTQ2QjE4IiwiX19uYW1lX18iOiJEaXJlY3QgUHJpdmF0ZSBJUHMiLCJpcCI6WyJnZW9pcDpwcml2YXRlIl0sIm91dGJvdW5kVGFnIjoiZGlyZWN0In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IkI3RDA5NEQ3LUExRDktNUVCRi1BOEFFLTJDN0U3QUY2ODU5NCIsIl9fbmFtZV9fIjoiRGlyZWN0IFByaXZhdGUgRG9tYWlucyIsImRvbWFpbk1hdGNoZXIiOiJoeWJyaWQiLCJkb21haW4iOlsiZ2Vvc2l0ZTpwcml2YXRlIl0sIm91dGJvdW5kVGFnIjoiZGlyZWN0In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IjREMkUxRTBBLTg5Q0YtNUM2Ni1BN0UyLTI0OTI3ODZBRDk1MiIsIl9fbmFtZV9fIjoiRGlyZWN0IFJVIFNlcnZpY2VzIiwiZG9tYWluTWF0Y2hlciI6Imh5YnJpZCIsImRvbWFpbiI6WyJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTphcHBsZSIsImdlb3NpdGU6bWljcm9zb2Z0IiwiZ2Vvc2l0ZTpzdGVhbSIsImdlb3NpdGU6ZXBpY2dhbWVzIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOmdvb2dsZS1wbGF5IiwiZ2Vvc2l0ZTpvcmlnaW4iLCJnZW9zaXRlOnR3aXRjaCJdLCJvdXRib3VuZFRhZyI6ImRpcmVjdCJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiJBQzBCNjMyOS0wRDJELTVFREItQTA0Ni04NUE3NzhFRkM1MDAiLCJfX25hbWVfXyI6IkRpcmVjdCBSVSBUTERzIiwiZG9tYWluTWF0Y2hlciI6Imh5YnJpZCIsImRvbWFpbiI6WyJyZWdleHA6LipcXC5ydSQiLCJyZWdleHA6LipcXC5zdSQiLCJyZWdleHA6LipcXC54bi0tcDFhaSQiXSwib3V0Ym91bmRUYWciOiJkaXJlY3QifSx7InR5cGUiOiJmaWVsZCIsImlkIjoiMDdEQ0Y1NTgtRTA0RC01NTMwLUE4RDctOEZENzhDQkQzMkFBIiwiX19uYW1lX18iOiJEaXJlY3QgUlUgSVBzIiwiaXAiOlsiZ2VvaXA6cnUiXSwib3V0Ym91bmRUYWciOiJkaXJlY3QifSx7InR5cGUiOiJmaWVsZCIsImlkIjoiODVBNkVGNjAtOEVFQS01MkYxLUFDNjMtMzhEMEUzQkVBNEVEIiwiX19uYW1lX18iOiJQcm94eSBBbGwiLCJwb3J0IjoiMC02NTUzNSIsIm91dGJvdW5kVGFnIjoicHJveHkifV19) |
|---|

> Deeplink files: [`happ/`](v2ray/happ/) · [`incy/`](v2ray/incy/) · [`v2raytun/`](v2ray/v2raytun/)

### Manual import (JSON)

Download the JSON config and import in app settings:

| Variant | Happ | INCY |
|---|---|---|
| **Lite** | [`default.json`](v2ray/happ/default.json) | [`default.json`](v2ray/incy/default.json) |
| **Full** | [`full.json`](v2ray/happ/full.json) | [`full.json`](v2ray/incy/full.json) |

### What the configs do

**Both variants share the same routing logic** (identical DirectSites, BlockSites, DNS settings):

| Rule | Categories | Action |
|---|---|---|
| **BLOCK** | win-spy, torrent, category-ads | Block telemetry, ads, torrents |
| **PROXY** | github, youtube, telegram, google-deepmind, twitch-ads | Through VPN |
| **DIRECT** | private, category-ru, whitelist, microsoft, apple, google-play, steam, epic, twitch, pinterest, riot, origin, faceit, eft | Bypass VPN |
| **DEFAULT** | Everything else (`GlobalProxy=true`) | Through VPN |

**Full variant additionally includes explicit proxy rules** (redundant, but faster DNS matching):
- `geosite:category-geoblock-ru` — 81K+ доменов, заблокированных РКН (Re:filter domains_all.lst)
- `geosite:community` — ~525 сервисов, ограничивающих доступ из РФ (Re:filter community.lst)
- `geoip:blocked-ru` — 38K+ IP-диапазонов, заблокированных в РФ (Re:filter ipsum.lst)

> **Рекомендация:** На iOS используйте **Lite** (default.json). На Android/Desktop можно использовать **Full** (full.json) для более явной маршрутизации.

---

## V2RayTUN Routing

Готовый конфиг маршрутизации для **[V2RayTUN](https://docs.v2raytun.com/)** в стандартном формате V2Ray/Xray routing JSON.

V2RayTUN использует встроенные `geosite.dat`/`geoip.dat` (стандарт v2fly), поэтому конфиг референсит стандартные категории (`geosite:category-ru`, `geoip:ru` и т.д.), а не кастомные.

### Логика маршрутизации

| Правило | Категории | Действие |
|---|---|---|
| **BLOCK** | category-ads-all, win-spy, win-extra, QUIC (UDP/443) | Блокировка рекламы/телеметрии |
| **DIRECT** | private, category-ru, apple, microsoft, steam, epicgames, pinterest, google-play, origin, twitch, `*.ru`/`*.su`/`*.рф`, geoip:ru | Мимо VPN |
| **PROXY** | Всё остальное (catch-all) | Через VPN |

### Использование

**Способ 1 — В приложении:**
Откройте V2RayTUN → Routing → Import → вставьте содержимое [`routing.json`](v2ray/v2raytun/routing.json)

**Способ 2 — Через подписку (subscription header):**
Добавьте в заголовки ответа подписки содержимое [`routing_header.txt`](v2ray/v2raytun/routing_header.txt):
```
routing: "<base64-закодированный JSON>"
```

**Способ 3 — Deeplink:**
Откройте на устройстве: [📲 Import](https://r.far.ovh/?url=v2rayTun%3A%2F%2Fimport_route%2FeyJkb21haW5TdHJhdGVneSI6IklQSWZOb25NYXRjaCIsImlkIjoiRkU0RDY2REMtMjEwQy01ODU3LUI0RkItOEE5QUJDNDIxRjI1IiwibmFtZSI6IkRpZ25lWnpaIFJvdXRpbmciLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiYmFsYW5jZXJzIjpbXSwicnVsZXMiOlt7InR5cGUiOiJmaWVsZCIsImlkIjoiNjc5OTVCMjItNTAzRC01MzUzLUE5NzQtQjU0QTZCMTMzNzAwIiwiX19uYW1lX18iOiJCbG9jayBBZHMgJiBUcmFja2VycyIsImRvbWFpbk1hdGNoZXIiOiJoeWJyaWQiLCJkb21haW4iOlsiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMtYWxsIiwiZ2Vvc2l0ZTp3aW4tc3B5IiwiZ2Vvc2l0ZTp3aW4tZXh0cmEiXSwib3V0Ym91bmRUYWciOiJibG9jayJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiJCMTI2MDYzRS1GOENDLTVDRDktQjcwNy1FOUIzOUY4MDlBNkIiLCJfX25hbWVfXyI6IkJsb2NrIFFVSUMiLCJwb3J0IjoiNDQzIiwibmV0d29yayI6InVkcCIsIm91dGJvdW5kVGFnIjoiYmxvY2sifSx7InR5cGUiOiJmaWVsZCIsImlkIjoiNUEzOEQzM0QtNUZFQS01OEFCLThDQjktNDJERDk3NTQ2QjE4IiwiX19uYW1lX18iOiJEaXJlY3QgUHJpdmF0ZSBJUHMiLCJpcCI6WyJnZW9pcDpwcml2YXRlIl0sIm91dGJvdW5kVGFnIjoiZGlyZWN0In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IkI3RDA5NEQ3LUExRDktNUVCRi1BOEFFLTJDN0U3QUY2ODU5NCIsIl9fbmFtZV9fIjoiRGlyZWN0IFByaXZhdGUgRG9tYWlucyIsImRvbWFpbk1hdGNoZXIiOiJoeWJyaWQiLCJkb21haW4iOlsiZ2Vvc2l0ZTpwcml2YXRlIl0sIm91dGJvdW5kVGFnIjoiZGlyZWN0In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IjREMkUxRTBBLTg5Q0YtNUM2Ni1BN0UyLTI0OTI3ODZBRDk1MiIsIl9fbmFtZV9fIjoiRGlyZWN0IFJVIFNlcnZpY2VzIiwiZG9tYWluTWF0Y2hlciI6Imh5YnJpZCIsImRvbWFpbiI6WyJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTphcHBsZSIsImdlb3NpdGU6bWljcm9zb2Z0IiwiZ2Vvc2l0ZTpzdGVhbSIsImdlb3NpdGU6ZXBpY2dhbWVzIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOmdvb2dsZS1wbGF5IiwiZ2Vvc2l0ZTpvcmlnaW4iLCJnZW9zaXRlOnR3aXRjaCJdLCJvdXRib3VuZFRhZyI6ImRpcmVjdCJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiJBQzBCNjMyOS0wRDJELTVFREItQTA0Ni04NUE3NzhFRkM1MDAiLCJfX25hbWVfXyI6IkRpcmVjdCBSVSBUTERzIiwiZG9tYWluTWF0Y2hlciI6Imh5YnJpZCIsImRvbWFpbiI6WyJyZWdleHA6LipcXC5ydSQiLCJyZWdleHA6LipcXC5zdSQiLCJyZWdleHA6LipcXC54bi0tcDFhaSQiXSwib3V0Ym91bmRUYWciOiJkaXJlY3QifSx7InR5cGUiOiJmaWVsZCIsImlkIjoiMDdEQ0Y1NTgtRTA0RC01NTMwLUE4RDctOEZENzhDQkQzMkFBIiwiX19uYW1lX18iOiJEaXJlY3QgUlUgSVBzIiwiaXAiOlsiZ2VvaXA6cnUiXSwib3V0Ym91bmRUYWciOiJkaXJlY3QifSx7InR5cGUiOiJmaWVsZCIsImlkIjoiODVBNkVGNjAtOEVFQS01MkYxLUFDNjMtMzhEMEUzQkVBNEVEIiwiX19uYW1lX18iOiJQcm94eSBBbGwiLCJwb3J0IjoiMC02NTUzNSIsIm91dGJvdW5kVGFnIjoicHJveHkifV19)

**Ссылки:**
```
https://raw.githubusercontent.com/DigneZzZ/routing/main/v2ray/v2raytun/routing.json
https://raw.githubusercontent.com/DigneZzZ/routing/main/v2ray/v2raytun/routing_base64.txt
```

## License

MIT