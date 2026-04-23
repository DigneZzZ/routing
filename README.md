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
├── ip-check.list     # domains → DIRECT (IP-check services)
├── vpndetect.list    # domains → DIRECT (VPN-detect probes)
├── proxy-ip.list     # IPs → PROXY (telegram + cloudflare)
├── direct-ip.list    # IPs → DIRECT (private ranges)
├── refilter-domain.list  # RKN bypass domains (Re:filter)
├── refilter-ip.list      # RKN bypass IPs (Re:filter)
├── refilter-community.list # Services blocking Russia (Re:filter)
├── proc-games.yaml   # game process names (classical)
├── proc-torrent.yaml # torrent client process names (classical)
└── proc-ru.yaml      # Russian app process names (classical)

v2ray/                # V2Ray/Xray geo-data + routing configs (auto-generated)
├── geosite.dat       # 26 domain categories (protobuf, full)
├── geoip.dat         # 4 IP categories (protobuf, full)
├── happ/
│   ├── geosite.dat   # lite — without heavy RKN lists (for mobile)
│   ├── geoip.dat     # lite — without blocked-ru IPs (keeps telegram)
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

template.yaml         # Remnawave subscription template
```

## Auto-update

Everything is rebuilt every 4 hours via GitHub Actions.

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
- **DIRECT** — torrents, Microsoft, Apple, Google Play, Pinterest, Twitch, RU sites, IP-check, VPN-detect
- **PROXY** — Telegram, GitHub, RKN bypass (refilter)
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

### geosite.dat categories (26)

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
| `IP-CHECK` | IP address check services (fatyzzz/max-list) | DIRECT |
| `VPNDETECT` | VPN detection probes (fatyzzz/max-list) | DIRECT |
| `ESCAPEFROMTARKOV` | Escape from Tarkov | PROXY |
| `FACEIT` | Faceit | PROXY |
| `RIOT` | Riot Games (LoL, Valorant) | PROXY |

### geoip.dat categories (4)

| Category | Description | Routing |
|---|---|---|
| `WHITELIST` | Russian IP ranges | DIRECT |
| `PRIVATE` | RFC1918 private ranges | DIRECT |
| `BLOCKED-RU` | IPs blocked in Russia (Re:filter) | PROXY |
| `TELEGRAM` | Telegram DC IPs (Loyalsoldier/geoip) | PROXY |

### Example V2Ray/Xray config

```json
{
  "GlobalProxy": true,
  "RouteOrder": "block-proxy-direct",
  "DomainStrategy": "IPIfNonMatch",
  "DirectSites": ["geosite:private", "geosite:whitelist", "geosite:ip-check", "geosite:vpndetect"],
  "DirectIp": ["geoip:private", "geoip:whitelist"],
  "ProxySites": ["geosite:category-geoblock-ru", "geosite:community"],
  "ProxyIp": ["geoip:blocked-ru", "geoip:telegram"],
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
| geosite.dat | 100 KB (24 категории, ~4 400 доменов) | 1.8 MB (26 категорий, ~86 000 доменов) |
| geoip.dat | 385 KB (3 категории, ~25 300 CIDR) | 763 KB (4 категории, ~64 000 CIDR) |
| **Итого** | **~500 KB** | **~2.6 MB** |
| iOS (Happ/INCY) | ✅ Работает | ❌ Вылетает (превышение памяти) |
| Android / Desktop | ✅ Работает | ✅ Работает |

### Quick import (deeplink)

Open the deeplink on your device with Happ/INCY installed:

| Variant | Happ | INCY | .dat size |
|---|---|---|---|
| **Lite** (recommended for iOS) | [📲 Import](https://r.far.ovh/?url=happ%3A%2F%2Frouting%2Fonadd%2FeyJOYW1lIjoiRGlnbmVaelogKGxpdGUpIiwiR2xvYmFsUHJveHkiOiJ0cnVlIiwiVXNlQ2h1bmtGaWxlcyI6ImZhbHNlIiwiUmVtb3RlRG5zIjoiOC44LjguOCIsIkRvbWVzdGljRG5zIjoiNzcuODguOC44IiwiUmVtb3RlRE5TVHlwZSI6IkRvSCIsIlJlbW90ZUROU0RvbWFpbiI6Imh0dHBzOi8vOC44LjguOC9kbnMtcXVlcnkiLCJSZW1vdGVETlNJUCI6IjguOC44LjgiLCJEb21lc3RpY0ROU1R5cGUiOiJEb0giLCJEb21lc3RpY0ROU0RvbWFpbiI6Imh0dHBzOi8vNzcuODguOC44L2Rucy1xdWVyeSIsIkRvbWVzdGljRE5TSVAiOiI3Ny44OC44LjgiLCJMYXN0VXBkYXRlZCI6IjE3NzY5NDcwNTUiLCJEbnNIb3N0cyI6e30sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6WyJnZW9zaXRlOnByaXZhdGUiLCJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTp3aGl0ZWxpc3QiLCJnZW9zaXRlOm1pY3Jvc29mdCIsImdlb3NpdGU6YXBwbGUiLCJnZW9zaXRlOmdvb2dsZS1wbGF5IiwiZ2Vvc2l0ZTplcGljZ2FtZXMiLCJnZW9zaXRlOnJpb3QiLCJnZW9zaXRlOmVzY2FwZWZyb210YXJrb3YiLCJnZW9zaXRlOnN0ZWFtIiwiZ2Vvc2l0ZTpvcmlnaW4iLCJnZW9zaXRlOnR3aXRjaCIsImdlb3NpdGU6cGludGVyZXN0IiwiZ2Vvc2l0ZTpmYWNlaXQiLCJnZW9zaXRlOmlwLWNoZWNrIiwiZ2Vvc2l0ZTp2cG5kZXRlY3QiXSwiRGlyZWN0SXAiOlsiZ2VvaXA6cHJpdmF0ZSIsImdlb2lwOndoaXRlbGlzdCJdLCJCbG9ja1NpdGVzIjpbImdlb3NpdGU6d2luLXNweSIsImdlb3NpdGU6dG9ycmVudCIsImdlb3NpdGU6Y2F0ZWdvcnktYWRzIl0sIkJsb2NrSXAiOltdLCJEb21haW5TdHJhdGVneSI6IklQSWZOb25NYXRjaCIsIkZha2VETlMiOiJmYWxzZSIsIkdlb2lwdXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL0RpZ25lWnpaL3JvdXRpbmdAbWFpbi92MnJheS9oYXBwL2dlb2lwLmRhdCIsIkdlb3NpdGV1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvRGlnbmVaelovcm91dGluZ0BtYWluL3YycmF5L2hhcHAvZ2Vvc2l0ZS5kYXQiLCJQcm94eVNpdGVzIjpbImdlb3NpdGU6Z2l0aHViIiwiZ2Vvc2l0ZTp0d2l0Y2gtYWRzIiwiZ2Vvc2l0ZTp5b3V0dWJlIiwiZ2Vvc2l0ZTp0ZWxlZ3JhbSIsImdlb3NpdGU6ZGlzY29yZCIsImdlb3NpdGU6d2hhdHNhcHAiLCJnZW9zaXRlOmdvb2dsZS1kZWVwbWluZCIsImdlb3NpdGU6Y3J5cHRvIl0sIlByb3h5SXAiOlsiZ2VvaXA6dGVsZWdyYW0iXX0%3D) | [📲 Import](https://r.far.ovh/?url=incy%3A%2F%2Frouting%2Fonadd%2FeyJOYW1lIjoiRGlnbmVaelogKGxpdGUpIiwiR2xvYmFsUHJveHkiOiJ0cnVlIiwiVXNlQ2h1bmtGaWxlcyI6ImZhbHNlIiwiUmVtb3RlRG5zIjoiOC44LjguOCIsIkRvbWVzdGljRG5zIjoiNzcuODguOC44IiwiUmVtb3RlRE5TVHlwZSI6IkRvSCIsIlJlbW90ZUROU0RvbWFpbiI6Imh0dHBzOi8vOC44LjguOC9kbnMtcXVlcnkiLCJSZW1vdGVETlNJUCI6IjguOC44LjgiLCJEb21lc3RpY0ROU1R5cGUiOiJEb0giLCJEb21lc3RpY0ROU0RvbWFpbiI6Imh0dHBzOi8vNzcuODguOC44L2Rucy1xdWVyeSIsIkRvbWVzdGljRE5TSVAiOiI3Ny44OC44LjgiLCJMYXN0VXBkYXRlZCI6IjE3NzY5NDcwNTUiLCJEbnNIb3N0cyI6e30sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6WyJnZW9zaXRlOnByaXZhdGUiLCJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTp3aGl0ZWxpc3QiLCJnZW9zaXRlOm1pY3Jvc29mdCIsImdlb3NpdGU6YXBwbGUiLCJnZW9zaXRlOmdvb2dsZS1wbGF5IiwiZ2Vvc2l0ZTplcGljZ2FtZXMiLCJnZW9zaXRlOnJpb3QiLCJnZW9zaXRlOmVzY2FwZWZyb210YXJrb3YiLCJnZW9zaXRlOnN0ZWFtIiwiZ2Vvc2l0ZTpvcmlnaW4iLCJnZW9zaXRlOnR3aXRjaCIsImdlb3NpdGU6cGludGVyZXN0IiwiZ2Vvc2l0ZTpmYWNlaXQiLCJnZW9zaXRlOmlwLWNoZWNrIiwiZ2Vvc2l0ZTp2cG5kZXRlY3QiXSwiRGlyZWN0SXAiOlsiZ2VvaXA6cHJpdmF0ZSIsImdlb2lwOndoaXRlbGlzdCJdLCJCbG9ja1NpdGVzIjpbImdlb3NpdGU6d2luLXNweSIsImdlb3NpdGU6dG9ycmVudCIsImdlb3NpdGU6Y2F0ZWdvcnktYWRzIl0sIkJsb2NrSXAiOltdLCJEb21haW5TdHJhdGVneSI6IklQSWZOb25NYXRjaCIsIkZha2VETlMiOiJmYWxzZSIsIkdlb2lwdXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL0RpZ25lWnpaL3JvdXRpbmdAbWFpbi92MnJheS9oYXBwL2dlb2lwLmRhdCIsIkdlb3NpdGV1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvRGlnbmVaelovcm91dGluZ0BtYWluL3YycmF5L2hhcHAvZ2Vvc2l0ZS5kYXQiLCJQcm94eVNpdGVzIjpbImdlb3NpdGU6Z2l0aHViIiwiZ2Vvc2l0ZTp0d2l0Y2gtYWRzIiwiZ2Vvc2l0ZTp5b3V0dWJlIiwiZ2Vvc2l0ZTp0ZWxlZ3JhbSIsImdlb3NpdGU6ZGlzY29yZCIsImdlb3NpdGU6d2hhdHNhcHAiLCJnZW9zaXRlOmdvb2dsZS1kZWVwbWluZCIsImdlb3NpdGU6Y3J5cHRvIl0sIlByb3h5SXAiOlsiZ2VvaXA6dGVsZWdyYW0iXX0%3D) | ~500 KB |
| **Full** (all RKN lists) | [📲 Import](https://r.far.ovh/?url=happ%3A%2F%2Frouting%2Fonadd%2FeyJOYW1lIjoiRGlnbmVaelogKGZ1bGwpIiwiR2xvYmFsUHJveHkiOiJ0cnVlIiwiVXNlQ2h1bmtGaWxlcyI6ImZhbHNlIiwiUmVtb3RlRG5zIjoiOC44LjguOCIsIkRvbWVzdGljRG5zIjoiNzcuODguOC44IiwiUmVtb3RlRE5TVHlwZSI6IkRvSCIsIlJlbW90ZUROU0RvbWFpbiI6Imh0dHBzOi8vOC44LjguOC9kbnMtcXVlcnkiLCJSZW1vdGVETlNJUCI6IjguOC44LjgiLCJEb21lc3RpY0ROU1R5cGUiOiJEb0giLCJEb21lc3RpY0ROU0RvbWFpbiI6Imh0dHBzOi8vNzcuODguOC44L2Rucy1xdWVyeSIsIkRvbWVzdGljRE5TSVAiOiI3Ny44OC44LjgiLCJMYXN0VXBkYXRlZCI6IjE3NzY5NDcwNTUiLCJEbnNIb3N0cyI6e30sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6WyJnZW9zaXRlOnByaXZhdGUiLCJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTp3aGl0ZWxpc3QiLCJnZW9zaXRlOm1pY3Jvc29mdCIsImdlb3NpdGU6YXBwbGUiLCJnZW9zaXRlOmdvb2dsZS1wbGF5IiwiZ2Vvc2l0ZTplcGljZ2FtZXMiLCJnZW9zaXRlOnJpb3QiLCJnZW9zaXRlOmVzY2FwZWZyb210YXJrb3YiLCJnZW9zaXRlOnN0ZWFtIiwiZ2Vvc2l0ZTpvcmlnaW4iLCJnZW9zaXRlOnR3aXRjaCIsImdlb3NpdGU6cGludGVyZXN0IiwiZ2Vvc2l0ZTpmYWNlaXQiLCJnZW9zaXRlOmlwLWNoZWNrIiwiZ2Vvc2l0ZTp2cG5kZXRlY3QiXSwiRGlyZWN0SXAiOlsiZ2VvaXA6cHJpdmF0ZSIsImdlb2lwOndoaXRlbGlzdCJdLCJCbG9ja1NpdGVzIjpbImdlb3NpdGU6d2luLXNweSIsImdlb3NpdGU6dG9ycmVudCIsImdlb3NpdGU6Y2F0ZWdvcnktYWRzIl0sIkJsb2NrSXAiOltdLCJEb21haW5TdHJhdGVneSI6IklQSWZOb25NYXRjaCIsIkZha2VETlMiOiJmYWxzZSIsIkdlb2lwdXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL0RpZ25lWnpaL3JvdXRpbmdAbWFpbi92MnJheS9nZW9pcC5kYXQiLCJHZW9zaXRldXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL0RpZ25lWnpaL3JvdXRpbmdAbWFpbi92MnJheS9nZW9zaXRlLmRhdCIsIlByb3h5U2l0ZXMiOlsiZ2Vvc2l0ZTpnaXRodWIiLCJnZW9zaXRlOnR3aXRjaC1hZHMiLCJnZW9zaXRlOnlvdXR1YmUiLCJnZW9zaXRlOnRlbGVncmFtIiwiZ2Vvc2l0ZTpkaXNjb3JkIiwiZ2Vvc2l0ZTp3aGF0c2FwcCIsImdlb3NpdGU6Z29vZ2xlLWRlZXBtaW5kIiwiZ2Vvc2l0ZTpjcnlwdG8iLCJnZW9zaXRlOmNhdGVnb3J5LWdlb2Jsb2NrLXJ1IiwiZ2Vvc2l0ZTpjb21tdW5pdHkiXSwiUHJveHlJcCI6WyJnZW9pcDpibG9ja2VkLXJ1IiwiZ2VvaXA6dGVsZWdyYW0iXX0%3D) | [📲 Import](https://r.far.ovh/?url=incy%3A%2F%2Frouting%2Fonadd%2FeyJOYW1lIjoiRGlnbmVaelogKGZ1bGwpIiwiR2xvYmFsUHJveHkiOiJ0cnVlIiwiVXNlQ2h1bmtGaWxlcyI6ImZhbHNlIiwiUmVtb3RlRG5zIjoiOC44LjguOCIsIkRvbWVzdGljRG5zIjoiNzcuODguOC44IiwiUmVtb3RlRE5TVHlwZSI6IkRvSCIsIlJlbW90ZUROU0RvbWFpbiI6Imh0dHBzOi8vOC44LjguOC9kbnMtcXVlcnkiLCJSZW1vdGVETlNJUCI6IjguOC44LjgiLCJEb21lc3RpY0ROU1R5cGUiOiJEb0giLCJEb21lc3RpY0ROU0RvbWFpbiI6Imh0dHBzOi8vNzcuODguOC44L2Rucy1xdWVyeSIsIkRvbWVzdGljRE5TSVAiOiI3Ny44OC44LjgiLCJMYXN0VXBkYXRlZCI6IjE3NzY5NDcwNTUiLCJEbnNIb3N0cyI6e30sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6WyJnZW9zaXRlOnByaXZhdGUiLCJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTp3aGl0ZWxpc3QiLCJnZW9zaXRlOm1pY3Jvc29mdCIsImdlb3NpdGU6YXBwbGUiLCJnZW9zaXRlOmdvb2dsZS1wbGF5IiwiZ2Vvc2l0ZTplcGljZ2FtZXMiLCJnZW9zaXRlOnJpb3QiLCJnZW9zaXRlOmVzY2FwZWZyb210YXJrb3YiLCJnZW9zaXRlOnN0ZWFtIiwiZ2Vvc2l0ZTpvcmlnaW4iLCJnZW9zaXRlOnR3aXRjaCIsImdlb3NpdGU6cGludGVyZXN0IiwiZ2Vvc2l0ZTpmYWNlaXQiLCJnZW9zaXRlOmlwLWNoZWNrIiwiZ2Vvc2l0ZTp2cG5kZXRlY3QiXSwiRGlyZWN0SXAiOlsiZ2VvaXA6cHJpdmF0ZSIsImdlb2lwOndoaXRlbGlzdCJdLCJCbG9ja1NpdGVzIjpbImdlb3NpdGU6d2luLXNweSIsImdlb3NpdGU6dG9ycmVudCIsImdlb3NpdGU6Y2F0ZWdvcnktYWRzIl0sIkJsb2NrSXAiOltdLCJEb21haW5TdHJhdGVneSI6IklQSWZOb25NYXRjaCIsIkZha2VETlMiOiJmYWxzZSIsIkdlb2lwdXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL0RpZ25lWnpaL3JvdXRpbmdAbWFpbi92MnJheS9nZW9pcC5kYXQiLCJHZW9zaXRldXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL0RpZ25lWnpaL3JvdXRpbmdAbWFpbi92MnJheS9nZW9zaXRlLmRhdCIsIlByb3h5U2l0ZXMiOlsiZ2Vvc2l0ZTpnaXRodWIiLCJnZW9zaXRlOnR3aXRjaC1hZHMiLCJnZW9zaXRlOnlvdXR1YmUiLCJnZW9zaXRlOnRlbGVncmFtIiwiZ2Vvc2l0ZTpkaXNjb3JkIiwiZ2Vvc2l0ZTp3aGF0c2FwcCIsImdlb3NpdGU6Z29vZ2xlLWRlZXBtaW5kIiwiZ2Vvc2l0ZTpjcnlwdG8iLCJnZW9zaXRlOmNhdGVnb3J5LWdlb2Jsb2NrLXJ1IiwiZ2Vvc2l0ZTpjb21tdW5pdHkiXSwiUHJveHlJcCI6WyJnZW9pcDpibG9ja2VkLXJ1IiwiZ2VvaXA6dGVsZWdyYW0iXX0%3D) | ~2.6 MB |

**V2RayTUN:**

| [📲 Import](https://r.far.ovh/?url=v2rayTun%3A%2F%2Fimport_route%2FeyJkb21haW5TdHJhdGVneSI6IklQSWZOb25NYXRjaCIsImlkIjoiRkU0RDY2REMtMjEwQy01ODU3LUI0RkItOEE5QUJDNDIxRjI1IiwibmFtZSI6IkRpZ25lWnpaIFJvdXRpbmciLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiYmFsYW5jZXJzIjpbXSwicnVsZXMiOlt7InR5cGUiOiJmaWVsZCIsImlkIjoiNjc5OTVCMjItNTAzRC01MzUzLUE5NzQtQjU0QTZCMTMzNzAwIiwiX19uYW1lX18iOiJCbG9jayBBZHMgJiBUcmFja2VycyIsImRvbWFpbk1hdGNoZXIiOiJoeWJyaWQiLCJkb21haW4iOlsiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMtYWxsIiwiZ2Vvc2l0ZTp3aW4tc3B5IiwiZ2Vvc2l0ZTp3aW4tZXh0cmEiXSwib3V0Ym91bmRUYWciOiJibG9jayJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiJCMTI2MDYzRS1GOENDLTVDRDktQjcwNy1FOUIzOUY4MDlBNkIiLCJfX25hbWVfXyI6IkJsb2NrIFFVSUMiLCJwb3J0IjoiNDQzIiwibmV0d29yayI6InVkcCIsIm91dGJvdW5kVGFnIjoiYmxvY2sifSx7InR5cGUiOiJmaWVsZCIsImlkIjoiNUEzOEQzM0QtNUZFQS01OEFCLThDQjktNDJERDk3NTQ2QjE4IiwiX19uYW1lX18iOiJEaXJlY3QgUHJpdmF0ZSBJUHMiLCJpcCI6WyJnZW9pcDpwcml2YXRlIl0sIm91dGJvdW5kVGFnIjoiZGlyZWN0In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IkI3RDA5NEQ3LUExRDktNUVCRi1BOEFFLTJDN0U3QUY2ODU5NCIsIl9fbmFtZV9fIjoiRGlyZWN0IFByaXZhdGUgRG9tYWlucyIsImRvbWFpbk1hdGNoZXIiOiJoeWJyaWQiLCJkb21haW4iOlsiZ2Vvc2l0ZTpwcml2YXRlIl0sIm91dGJvdW5kVGFnIjoiZGlyZWN0In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IkVFMUVEQTc4LTJCMkMtNUIzQS1CMzEyLTA0ODdGODY4NTkxQyIsIl9fbmFtZV9fIjoiUHJveHkgVGVsZWdyYW0iLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiZG9tYWluIjpbImdlb3NpdGU6dGVsZWdyYW0iXSwiaXAiOlsiZ2VvaXA6dGVsZWdyYW0iXSwib3V0Ym91bmRUYWciOiJwcm94eSJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiI4QzExQ0M5Ni0zOERELTU1Q0QtQjNGRi1FRkZBQzM4RkNERjciLCJfX25hbWVfXyI6IlByb3h5IERpc2NvcmQiLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiZG9tYWluIjpbImdlb3NpdGU6ZGlzY29yZCJdLCJvdXRib3VuZFRhZyI6InByb3h5In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IjhFNzRCMTBCLTBGQTMtNTI4RC04NERGLUJGQTYyOUU0NkMyMSIsIl9fbmFtZV9fIjoiUHJveHkgV2hhdHNBcHAiLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiZG9tYWluIjpbImdlb3NpdGU6d2hhdHNhcHAiXSwib3V0Ym91bmRUYWciOiJwcm94eSJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiIwMTk2RDUzRC1EQzZGLTVDNkEtQjg1Qi0wN0ZCRUVEQjRGODMiLCJfX25hbWVfXyI6IlByb3h5IENyeXB0byBFeGNoYW5nZXMiLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiZG9tYWluIjpbImRvbWFpbjpiaW5hbmNlLmNvbSIsImRvbWFpbjpiaW5hbmNlLm9yZyIsImRvbWFpbjpiaW5hbmNlLnVzIiwiZG9tYWluOmJpbmFuY2UubWUiLCJkb21haW46YmluYW5jZS5pbmZvIiwiZG9tYWluOmJpbmFuY2VjbnQuY29tIiwiZG9tYWluOmJuYnN0YXRpYy5jb20iLCJkb21haW46YmluYW5jZS5jbG91ZCIsImRvbWFpbjpiaW5hbmNlLmNoYXJpdHkiLCJkb21haW46YmluYW5jZS5kZXYiLCJkb21haW46YmluYW5jZS52aXNpb24iLCJkb21haW46YmluYW5jZWZ1dHVyZS5jb20iLCJkb21haW46YmlmaW5pdHkuY29tIiwiZG9tYWluOnNhZnUuaW0iLCJkb21haW46dHJ1c3R3YWxsZXQuY29tIiwiZG9tYWluOmJuYmNoYWluLm9yZyIsImRvbWFpbjpibmJjaGFpbi53b3JsZCIsImRvbWFpbjpic2NzY2FuLmNvbSIsImRvbWFpbjpieWJpdC5jb20iLCJkb21haW46YnliaXQub3JnIiwiZG9tYWluOmJ5Yml0Lm5sIiwiZG9tYWluOmJ5Yml0c2lnbnVwLmNvbSIsImRvbWFpbjpieWJpdGFwaS5jb20iLCJkb21haW46YnliaXRjZG4uY29tIiwiZG9tYWluOmJ5Yml0Z2xvYmFsLmNvbSIsImRvbWFpbjpieWNzaS5jb20iLCJkb21haW46Ynl0aWNrLmNvbSIsImRvbWFpbjpieXJlYWwuaW8iLCJkb21haW46YnliaXQuY29tLmhrIiwiZG9tYWluOmJ5Yml0LnRyIiwiZG9tYWluOmJ5Yml0Lmt6IiwiZG9tYWluOmJ5Yml0LmFlIiwiZG9tYWluOmJ5Yml0LmV1IiwiZG9tYWluOmJ5Yml0LmlkIiwiZG9tYWluOmJ5Yml0Z2VvcmdpYS5nZSIsImRvbWFpbjpieWJpdC10ci5jb20iLCJkb21haW46bWV4Yy5jb20iLCJkb21haW46bWV4Yy5jbyIsImRvbWFpbjptZXhjZ2xvYmFsLmNvbSIsImRvbWFpbjptZXhjLmlvIiwiZG9tYWluOm1vY29ydGVjaC5jb20iLCJkb21haW46b2t4LmNvbSIsImRvbWFpbjpva3guY2FiIiwiZG9tYWluOm9reC5vcmciLCJkb21haW46b2tjb2luLmNvbSIsImRvbWFpbjpva2V4LmNvbSIsImRvbWFpbjpva2V4Y24uY29tIiwiZG9tYWluOm9rbGluay5jb20iLCJkb21haW46b2tjZG4uY29tIiwiZG9tYWluOm9rYnRvdGhlbW9vbi5jb20iLCJkb21haW46Y29pbmJhc2UuY29tIiwiZG9tYWluOmNvaW5iYXNlLXN0YXRpY3MuY29tIiwiZG9tYWluOmNkbmJhc2UuaW8iLCJkb21haW46Y2ItYm4ubmV0IiwiZG9tYWluOmNvaW5iYXNlLmNsb3VkIiwiZG9tYWluOmNvaW5iYXNlLm9yZyIsImRvbWFpbjprcmFrZW4uY29tIiwiZG9tYWluOmtyYWtlbi5jbyIsImRvbWFpbjprcmFrZW5meC5jb20iLCJkb21haW46cGF5d2FyZC5jb20iLCJkb21haW46a3Vjb2luLmNvbSIsImRvbWFpbjprdWNvaW4uaW8iLCJkb21haW46a3Vjb2luLnBsdXMiLCJkb21haW46a3VtZXguY29tIiwiZG9tYWluOmdhdGUuaW8iLCJkb21haW46Z2F0ZS5hYyIsImRvbWFpbjpnYXRlaW8uY28iLCJkb21haW46Z2F0ZWlvLndzIiwiZG9tYWluOmdhdGVpbWcuY29tIiwiZG9tYWluOmdhdGV0b29sLmNvbSIsImRvbWFpbjpnYXRlZGF0YS5vcmciLCJkb21haW46aHR4LmNvbSIsImRvbWFpbjpodHguY28iLCJkb21haW46aHVvYmkuY29tIiwiZG9tYWluOmh1b2JpLnBybyIsImRvbWFpbjpodW9iaWdyb3VwLmNvbSIsImRvbWFpbjpoYmZpbGUubmV0IiwiZG9tYWluOmhiZy5jb20iLCJkb21haW46aGJkbS5jb20iLCJkb21haW46Yml0Z2V0LmNvbSIsImRvbWFpbjpiaXRnZXQuc2l0ZSIsImRvbWFpbjpiaXRnZXRhcHAuY29tIiwiZG9tYWluOmJnY2RuaW1nLmNvbSIsImRvbWFpbjpjb2luZ2Vja28uY29tIiwiZG9tYWluOmNvaW5tYXJrZXRjYXAuY29tIiwiZG9tYWluOnRyYWRpbmd2aWV3LmNvbSIsImRvbWFpbjpkZXhzY3JlZW5lci5jb20iLCJkb21haW46ZGV4dG9vbHMuaW8iLCJkb21haW46ZGVmaWxsYW1hLmNvbSIsImRvbWFpbjpibG9ja2NoYWluLmNvbSIsImRvbWFpbjpibG9ja2NoYWlyLmNvbSIsImRvbWFpbjpldGhlcnNjYW4uaW8iLCJkb21haW46cG9seWdvbnNjYW4uY29tIiwiZG9tYWluOmFyYmlzY2FuLmlvIiwiZG9tYWluOmJhc2VzY2FuLm9yZyIsImRvbWFpbjpzb2xzY2FuLmlvIiwiZG9tYWluOnRyb25zY2FuLm9yZyJdLCJvdXRib3VuZFRhZyI6InByb3h5In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IjhCNzhCM0Y0LTUzOEYtNTNEOC1BRTY2LTk4MjczODlGQzNBMiIsIl9fbmFtZV9fIjoiUHJveHkgQmFubmVkIFJVIFNpdGVzIiwiZG9tYWluTWF0Y2hlciI6Imh5YnJpZCIsImRvbWFpbiI6WyJkb21haW46dGhlaW5zLnJ1IiwiZG9tYWluOnR2cmFpbi5ydSIsImRvbWFpbjpub3ZheWFnYXpldGEucnUiLCJkb21haW46bW9zY293dGltZXMucnUiLCJkb21haW46dGhlLXZpbGxhZ2UucnUiLCJkb21haW46c25vYi5ydSIsImRvbWFpbjplY2hvLm1zay5ydSIsImRvbWFpbjpoYWJyLmNvbSIsImRvbWFpbjo0cGRhLnRvIiwiZG9tYWluOnNlYXNvbnZhci5ydSIsImRvbWFpbjpsaWIuc29jaWFsIiwiZG9tYWluOmxvc3RmaWxtLnR2IiwiZG9tYWluOmxvc3RmaWxtLmRvd25sb2FkIiwiZG9tYWluOmxvc3RmaWxtLnVubyIsImRvbWFpbjpoZHJlemthLmFnIiwiZG9tYWluOmhkcmV6a2EubWUiLCJkb21haW46cmV6a2EuYWciLCJkb21haW46a2lub3phbC50diIsImRvbWFpbjpraW5vemFsLmd1cnUiLCJkb21haW46cnV0cmFja2VyLm9yZyIsImRvbWFpbjpydXRyYWNrZXIubmV0IiwiZG9tYWluOm1lZHV6YS5pbyIsImRvbWFpbjpyZXB1YmxpYy5ydSIsImRvbWFpbjp6b25hLm1lZGlhIiwiZG9tYWluOnByb2VrdC5tZWRpYSIsImRvbWFpbjptZWRpYXpvbmEuY2EiLCJkb21haW46b3ZkLm5ld3MiLCJkb21haW46YW1uZXppYS5vcmciLCJkb21haW46bnRjLnBhcnR5IiwiZG9tYWluOmtlbW9uby5zdSIsImRvbWFpbjpqdXQuc3UiLCJkb21haW46a2FyYS5zdSIsImRvbWFpbjpraW5vLnB1YiJdLCJvdXRib3VuZFRhZyI6InByb3h5In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IjREMkUxRTBBLTg5Q0YtNUM2Ni1BN0UyLTI0OTI3ODZBRDk1MiIsIl9fbmFtZV9fIjoiRGlyZWN0IFJVIFNlcnZpY2VzIiwiZG9tYWluTWF0Y2hlciI6Imh5YnJpZCIsImRvbWFpbiI6WyJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTphcHBsZSIsImdlb3NpdGU6bWljcm9zb2Z0IiwiZ2Vvc2l0ZTpzdGVhbSIsImdlb3NpdGU6ZXBpY2dhbWVzIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOmdvb2dsZS1wbGF5IiwiZ2Vvc2l0ZTpvcmlnaW4iLCJnZW9zaXRlOnR3aXRjaCIsImRvbWFpbjphcGkuaXBpZnkub3JnIiwiZG9tYWluOmNhbGxzLm9rY2RuLnJ1IiwiZG9tYWluOmNoZWNraXAuYW1hem9uYXdzLmNvbSIsImRvbWFpbjpnb3N1c2x1Z2kucnUiLCJkb21haW46Z3N0YXRpYy5jb20iLCJkb21haW46aWZjb25maWcubWUiLCJkb21haW46aXAubWFpbC5ydSIsImRvbWFpbjppcHY0LWludGVybmV0LnlhbmRleC5uZXQiLCJkb21haW46aXB2Ni1pbnRlcm5ldC55YW5kZXgubmV0IiwiZG9tYWluOm10YWxrLmdvb2dsZS5jb20iLCJkb21haW46cHVzaHRycy5wdXNoLmhpY2xvdWQuY29tIiwiZG9tYWluOnB1c2h0cnMxLnB1c2guaGljbG91ZC5jb20iLCJkb21haW46dG9rZW4tZHJjbi5wdXNoLmRiYW5rY2xvdWQuY29tIl0sIm91dGJvdW5kVGFnIjoiZGlyZWN0In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IkFDMEI2MzI5LTBEMkQtNUVEQi1BMDQ2LTg1QTc3OEVGQzUwMCIsIl9fbmFtZV9fIjoiRGlyZWN0IFJVIFRMRHMiLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiZG9tYWluIjpbInJlZ2V4cDouKlxcLnJ1JCIsInJlZ2V4cDouKlxcLnN1JCIsInJlZ2V4cDouKlxcLnhuLS1wMWFpJCJdLCJvdXRib3VuZFRhZyI6ImRpcmVjdCJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiIwN0RDRjU1OC1FMDRELTU1MzAtQThENy04RkQ3OENCRDMyQUEiLCJfX25hbWVfXyI6IkRpcmVjdCBSVSBJUHMiLCJpcCI6WyJnZW9pcDpydSJdLCJvdXRib3VuZFRhZyI6ImRpcmVjdCJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiI4NUE2RUY2MC04RUVBLTUyRjEtQUM2My0zOEQwRTNCRUE0RUQiLCJfX25hbWVfXyI6IlByb3h5IEFsbCIsInBvcnQiOiIwLTY1NTM1Iiwib3V0Ym91bmRUYWciOiJwcm94eSJ9XX0%3D) |
|---|

> Deeplink files: [`happ/`](v2ray/happ/) · [`incy/`](v2ray/incy/) · [`v2raytun/`](v2ray/v2raytun/)

### Embedded JSON templates (no .dat needed)

Self-contained V2Ray/Xray configs with all domains and IPs inlined.
No geosite.dat or geoip.dat required — works in any V2Ray-compatible client.

| Variant | File | Description |
|---|---|---|
| **Lite** | [`config.json`](v2ray/config.json) | Core proxy (Telegram, GitHub, YouTube, AI, Crypto) + RU direct |
| **Full** | [`config_full.json`](v2ray/config_full.json) | Lite + Re:filter (all RKN-blocked domains) |

**Crypto exchanges included:** Binance, Bybit, MEXC, OKX, Coinbase, Kraken, KuCoin, Gate.io, HTX, Bitget + CoinGecko, CoinMarketCap, TradingView, DexScreener и другие агрегаторы.

> **Note:** Секция `outbounds` содержит только `direct` и `block`. Добавьте свой proxy-outbound с тегом `proxy` для работы маршрутизации.

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
| **PROXY** | github, youtube, telegram (geosite + geoip), google-deepmind, twitch-ads | Through VPN |
| **DIRECT** | private, category-ru, whitelist, microsoft, apple, google-play, steam, epic, twitch, pinterest, riot, origin, faceit, eft, ip-check, vpndetect | Bypass VPN |
| **DEFAULT** | Everything else (`GlobalProxy=true`) | Through VPN |

**Оба варианта явно гоняют Telegram через прокси по IP** (`geoip:telegram`) — помимо доменного `geosite:telegram`. Это нужно, потому что мобильные клиенты Telegram ходят прямо на DC по IP, минуя DNS, и доменного правила недостаточно.

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
| **PROXY (Telegram)** | `geosite:telegram` + `geoip:telegram` (до direct-ru, чтобы RU PoPs не уходили direct) | Через VPN |
| **DIRECT** | private, category-ru, apple, microsoft, steam, epicgames, pinterest, google-play, origin, twitch, ip-check, vpndetect, `*.ru`/`*.su`/`*.рф`, geoip:ru | Мимо VPN |
| **PROXY** | Всё остальное (catch-all) | Через VPN |

> `geoip:telegram` ссылается на кастомную категорию из нашего `v2ray/geoip.dat`. Если клиент использует встроенный v2fly geoip — правило по IP тихо игнорируется, и Telegram всё равно попадёт в прокси через `geosite:telegram` или финальный catch-all.

### Использование

**Способ 1 — В приложении:**
Откройте V2RayTUN → Routing → Import → вставьте содержимое [`routing.json`](v2ray/v2raytun/routing.json)

**Способ 2 — Через подписку (subscription header):**
Добавьте в заголовки ответа подписки содержимое [`routing_header.txt`](v2ray/v2raytun/routing_header.txt):
```
routing: "<base64-закодированный JSON>"
```

**Способ 3 — Deeplink:**
Откройте на устройстве: [📲 Import](https://r.far.ovh/?url=v2rayTun%3A%2F%2Fimport_route%2FeyJkb21haW5TdHJhdGVneSI6IklQSWZOb25NYXRjaCIsImlkIjoiRkU0RDY2REMtMjEwQy01ODU3LUI0RkItOEE5QUJDNDIxRjI1IiwibmFtZSI6IkRpZ25lWnpaIFJvdXRpbmciLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiYmFsYW5jZXJzIjpbXSwicnVsZXMiOlt7InR5cGUiOiJmaWVsZCIsImlkIjoiNjc5OTVCMjItNTAzRC01MzUzLUE5NzQtQjU0QTZCMTMzNzAwIiwiX19uYW1lX18iOiJCbG9jayBBZHMgJiBUcmFja2VycyIsImRvbWFpbk1hdGNoZXIiOiJoeWJyaWQiLCJkb21haW4iOlsiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMtYWxsIiwiZ2Vvc2l0ZTp3aW4tc3B5IiwiZ2Vvc2l0ZTp3aW4tZXh0cmEiXSwib3V0Ym91bmRUYWciOiJibG9jayJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiJCMTI2MDYzRS1GOENDLTVDRDktQjcwNy1FOUIzOUY4MDlBNkIiLCJfX25hbWVfXyI6IkJsb2NrIFFVSUMiLCJwb3J0IjoiNDQzIiwibmV0d29yayI6InVkcCIsIm91dGJvdW5kVGFnIjoiYmxvY2sifSx7InR5cGUiOiJmaWVsZCIsImlkIjoiNUEzOEQzM0QtNUZFQS01OEFCLThDQjktNDJERDk3NTQ2QjE4IiwiX19uYW1lX18iOiJEaXJlY3QgUHJpdmF0ZSBJUHMiLCJpcCI6WyJnZW9pcDpwcml2YXRlIl0sIm91dGJvdW5kVGFnIjoiZGlyZWN0In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IkI3RDA5NEQ3LUExRDktNUVCRi1BOEFFLTJDN0U3QUY2ODU5NCIsIl9fbmFtZV9fIjoiRGlyZWN0IFByaXZhdGUgRG9tYWlucyIsImRvbWFpbk1hdGNoZXIiOiJoeWJyaWQiLCJkb21haW4iOlsiZ2Vvc2l0ZTpwcml2YXRlIl0sIm91dGJvdW5kVGFnIjoiZGlyZWN0In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IkVFMUVEQTc4LTJCMkMtNUIzQS1CMzEyLTA0ODdGODY4NTkxQyIsIl9fbmFtZV9fIjoiUHJveHkgVGVsZWdyYW0iLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiZG9tYWluIjpbImdlb3NpdGU6dGVsZWdyYW0iXSwiaXAiOlsiZ2VvaXA6dGVsZWdyYW0iXSwib3V0Ym91bmRUYWciOiJwcm94eSJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiI4QzExQ0M5Ni0zOERELTU1Q0QtQjNGRi1FRkZBQzM4RkNERjciLCJfX25hbWVfXyI6IlByb3h5IERpc2NvcmQiLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiZG9tYWluIjpbImdlb3NpdGU6ZGlzY29yZCJdLCJvdXRib3VuZFRhZyI6InByb3h5In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IjhFNzRCMTBCLTBGQTMtNTI4RC04NERGLUJGQTYyOUU0NkMyMSIsIl9fbmFtZV9fIjoiUHJveHkgV2hhdHNBcHAiLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiZG9tYWluIjpbImdlb3NpdGU6d2hhdHNhcHAiXSwib3V0Ym91bmRUYWciOiJwcm94eSJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiIwMTk2RDUzRC1EQzZGLTVDNkEtQjg1Qi0wN0ZCRUVEQjRGODMiLCJfX25hbWVfXyI6IlByb3h5IENyeXB0byBFeGNoYW5nZXMiLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiZG9tYWluIjpbImRvbWFpbjpiaW5hbmNlLmNvbSIsImRvbWFpbjpiaW5hbmNlLm9yZyIsImRvbWFpbjpiaW5hbmNlLnVzIiwiZG9tYWluOmJpbmFuY2UubWUiLCJkb21haW46YmluYW5jZS5pbmZvIiwiZG9tYWluOmJpbmFuY2VjbnQuY29tIiwiZG9tYWluOmJuYnN0YXRpYy5jb20iLCJkb21haW46YmluYW5jZS5jbG91ZCIsImRvbWFpbjpiaW5hbmNlLmNoYXJpdHkiLCJkb21haW46YmluYW5jZS5kZXYiLCJkb21haW46YmluYW5jZS52aXNpb24iLCJkb21haW46YmluYW5jZWZ1dHVyZS5jb20iLCJkb21haW46YmlmaW5pdHkuY29tIiwiZG9tYWluOnNhZnUuaW0iLCJkb21haW46dHJ1c3R3YWxsZXQuY29tIiwiZG9tYWluOmJuYmNoYWluLm9yZyIsImRvbWFpbjpibmJjaGFpbi53b3JsZCIsImRvbWFpbjpic2NzY2FuLmNvbSIsImRvbWFpbjpieWJpdC5jb20iLCJkb21haW46YnliaXQub3JnIiwiZG9tYWluOmJ5Yml0Lm5sIiwiZG9tYWluOmJ5Yml0c2lnbnVwLmNvbSIsImRvbWFpbjpieWJpdGFwaS5jb20iLCJkb21haW46YnliaXRjZG4uY29tIiwiZG9tYWluOmJ5Yml0Z2xvYmFsLmNvbSIsImRvbWFpbjpieWNzaS5jb20iLCJkb21haW46Ynl0aWNrLmNvbSIsImRvbWFpbjpieXJlYWwuaW8iLCJkb21haW46YnliaXQuY29tLmhrIiwiZG9tYWluOmJ5Yml0LnRyIiwiZG9tYWluOmJ5Yml0Lmt6IiwiZG9tYWluOmJ5Yml0LmFlIiwiZG9tYWluOmJ5Yml0LmV1IiwiZG9tYWluOmJ5Yml0LmlkIiwiZG9tYWluOmJ5Yml0Z2VvcmdpYS5nZSIsImRvbWFpbjpieWJpdC10ci5jb20iLCJkb21haW46bWV4Yy5jb20iLCJkb21haW46bWV4Yy5jbyIsImRvbWFpbjptZXhjZ2xvYmFsLmNvbSIsImRvbWFpbjptZXhjLmlvIiwiZG9tYWluOm1vY29ydGVjaC5jb20iLCJkb21haW46b2t4LmNvbSIsImRvbWFpbjpva3guY2FiIiwiZG9tYWluOm9reC5vcmciLCJkb21haW46b2tjb2luLmNvbSIsImRvbWFpbjpva2V4LmNvbSIsImRvbWFpbjpva2V4Y24uY29tIiwiZG9tYWluOm9rbGluay5jb20iLCJkb21haW46b2tjZG4uY29tIiwiZG9tYWluOm9rYnRvdGhlbW9vbi5jb20iLCJkb21haW46Y29pbmJhc2UuY29tIiwiZG9tYWluOmNvaW5iYXNlLXN0YXRpY3MuY29tIiwiZG9tYWluOmNkbmJhc2UuaW8iLCJkb21haW46Y2ItYm4ubmV0IiwiZG9tYWluOmNvaW5iYXNlLmNsb3VkIiwiZG9tYWluOmNvaW5iYXNlLm9yZyIsImRvbWFpbjprcmFrZW4uY29tIiwiZG9tYWluOmtyYWtlbi5jbyIsImRvbWFpbjprcmFrZW5meC5jb20iLCJkb21haW46cGF5d2FyZC5jb20iLCJkb21haW46a3Vjb2luLmNvbSIsImRvbWFpbjprdWNvaW4uaW8iLCJkb21haW46a3Vjb2luLnBsdXMiLCJkb21haW46a3VtZXguY29tIiwiZG9tYWluOmdhdGUuaW8iLCJkb21haW46Z2F0ZS5hYyIsImRvbWFpbjpnYXRlaW8uY28iLCJkb21haW46Z2F0ZWlvLndzIiwiZG9tYWluOmdhdGVpbWcuY29tIiwiZG9tYWluOmdhdGV0b29sLmNvbSIsImRvbWFpbjpnYXRlZGF0YS5vcmciLCJkb21haW46aHR4LmNvbSIsImRvbWFpbjpodHguY28iLCJkb21haW46aHVvYmkuY29tIiwiZG9tYWluOmh1b2JpLnBybyIsImRvbWFpbjpodW9iaWdyb3VwLmNvbSIsImRvbWFpbjpoYmZpbGUubmV0IiwiZG9tYWluOmhiZy5jb20iLCJkb21haW46aGJkbS5jb20iLCJkb21haW46Yml0Z2V0LmNvbSIsImRvbWFpbjpiaXRnZXQuc2l0ZSIsImRvbWFpbjpiaXRnZXRhcHAuY29tIiwiZG9tYWluOmJnY2RuaW1nLmNvbSIsImRvbWFpbjpjb2luZ2Vja28uY29tIiwiZG9tYWluOmNvaW5tYXJrZXRjYXAuY29tIiwiZG9tYWluOnRyYWRpbmd2aWV3LmNvbSIsImRvbWFpbjpkZXhzY3JlZW5lci5jb20iLCJkb21haW46ZGV4dG9vbHMuaW8iLCJkb21haW46ZGVmaWxsYW1hLmNvbSIsImRvbWFpbjpibG9ja2NoYWluLmNvbSIsImRvbWFpbjpibG9ja2NoYWlyLmNvbSIsImRvbWFpbjpldGhlcnNjYW4uaW8iLCJkb21haW46cG9seWdvbnNjYW4uY29tIiwiZG9tYWluOmFyYmlzY2FuLmlvIiwiZG9tYWluOmJhc2VzY2FuLm9yZyIsImRvbWFpbjpzb2xzY2FuLmlvIiwiZG9tYWluOnRyb25zY2FuLm9yZyJdLCJvdXRib3VuZFRhZyI6InByb3h5In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IjhCNzhCM0Y0LTUzOEYtNTNEOC1BRTY2LTk4MjczODlGQzNBMiIsIl9fbmFtZV9fIjoiUHJveHkgQmFubmVkIFJVIFNpdGVzIiwiZG9tYWluTWF0Y2hlciI6Imh5YnJpZCIsImRvbWFpbiI6WyJkb21haW46dGhlaW5zLnJ1IiwiZG9tYWluOnR2cmFpbi5ydSIsImRvbWFpbjpub3ZheWFnYXpldGEucnUiLCJkb21haW46bW9zY293dGltZXMucnUiLCJkb21haW46dGhlLXZpbGxhZ2UucnUiLCJkb21haW46c25vYi5ydSIsImRvbWFpbjplY2hvLm1zay5ydSIsImRvbWFpbjpoYWJyLmNvbSIsImRvbWFpbjo0cGRhLnRvIiwiZG9tYWluOnNlYXNvbnZhci5ydSIsImRvbWFpbjpsaWIuc29jaWFsIiwiZG9tYWluOmxvc3RmaWxtLnR2IiwiZG9tYWluOmxvc3RmaWxtLmRvd25sb2FkIiwiZG9tYWluOmxvc3RmaWxtLnVubyIsImRvbWFpbjpoZHJlemthLmFnIiwiZG9tYWluOmhkcmV6a2EubWUiLCJkb21haW46cmV6a2EuYWciLCJkb21haW46a2lub3phbC50diIsImRvbWFpbjpraW5vemFsLmd1cnUiLCJkb21haW46cnV0cmFja2VyLm9yZyIsImRvbWFpbjpydXRyYWNrZXIubmV0IiwiZG9tYWluOm1lZHV6YS5pbyIsImRvbWFpbjpyZXB1YmxpYy5ydSIsImRvbWFpbjp6b25hLm1lZGlhIiwiZG9tYWluOnByb2VrdC5tZWRpYSIsImRvbWFpbjptZWRpYXpvbmEuY2EiLCJkb21haW46b3ZkLm5ld3MiLCJkb21haW46YW1uZXppYS5vcmciLCJkb21haW46bnRjLnBhcnR5IiwiZG9tYWluOmtlbW9uby5zdSIsImRvbWFpbjpqdXQuc3UiLCJkb21haW46a2FyYS5zdSIsImRvbWFpbjpraW5vLnB1YiJdLCJvdXRib3VuZFRhZyI6InByb3h5In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IjREMkUxRTBBLTg5Q0YtNUM2Ni1BN0UyLTI0OTI3ODZBRDk1MiIsIl9fbmFtZV9fIjoiRGlyZWN0IFJVIFNlcnZpY2VzIiwiZG9tYWluTWF0Y2hlciI6Imh5YnJpZCIsImRvbWFpbiI6WyJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTphcHBsZSIsImdlb3NpdGU6bWljcm9zb2Z0IiwiZ2Vvc2l0ZTpzdGVhbSIsImdlb3NpdGU6ZXBpY2dhbWVzIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOmdvb2dsZS1wbGF5IiwiZ2Vvc2l0ZTpvcmlnaW4iLCJnZW9zaXRlOnR3aXRjaCIsImRvbWFpbjphcGkuaXBpZnkub3JnIiwiZG9tYWluOmNhbGxzLm9rY2RuLnJ1IiwiZG9tYWluOmNoZWNraXAuYW1hem9uYXdzLmNvbSIsImRvbWFpbjpnb3N1c2x1Z2kucnUiLCJkb21haW46Z3N0YXRpYy5jb20iLCJkb21haW46aWZjb25maWcubWUiLCJkb21haW46aXAubWFpbC5ydSIsImRvbWFpbjppcHY0LWludGVybmV0LnlhbmRleC5uZXQiLCJkb21haW46aXB2Ni1pbnRlcm5ldC55YW5kZXgubmV0IiwiZG9tYWluOm10YWxrLmdvb2dsZS5jb20iLCJkb21haW46cHVzaHRycy5wdXNoLmhpY2xvdWQuY29tIiwiZG9tYWluOnB1c2h0cnMxLnB1c2guaGljbG91ZC5jb20iLCJkb21haW46dG9rZW4tZHJjbi5wdXNoLmRiYW5rY2xvdWQuY29tIl0sIm91dGJvdW5kVGFnIjoiZGlyZWN0In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IkFDMEI2MzI5LTBEMkQtNUVEQi1BMDQ2LTg1QTc3OEVGQzUwMCIsIl9fbmFtZV9fIjoiRGlyZWN0IFJVIFRMRHMiLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiZG9tYWluIjpbInJlZ2V4cDouKlxcLnJ1JCIsInJlZ2V4cDouKlxcLnN1JCIsInJlZ2V4cDouKlxcLnhuLS1wMWFpJCJdLCJvdXRib3VuZFRhZyI6ImRpcmVjdCJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiIwN0RDRjU1OC1FMDRELTU1MzAtQThENy04RkQ3OENCRDMyQUEiLCJfX25hbWVfXyI6IkRpcmVjdCBSVSBJUHMiLCJpcCI6WyJnZW9pcDpydSJdLCJvdXRib3VuZFRhZyI6ImRpcmVjdCJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiI4NUE2RUY2MC04RUVBLTUyRjEtQUM2My0zOEQwRTNCRUE0RUQiLCJfX25hbWVfXyI6IlByb3h5IEFsbCIsInBvcnQiOiIwLTY1NTM1Iiwib3V0Ym91bmRUYWciOiJwcm94eSJ9XX0%3D)

**Ссылки:**
```
https://raw.githubusercontent.com/DigneZzZ/routing/main/v2ray/v2raytun/routing.json
https://raw.githubusercontent.com/DigneZzZ/routing/main/v2ray/v2raytun/routing_base64.txt
```

## License

MIT