# routing

Наборы правил маршрутизации для **mihomo** (Clash.Meta), **Xray/V2Ray**,
**Happ**, **INCY** и **V2RayTUN**. Пересобираются автоматически из открытых
источников (MetaCubeX, Re:filter, legiz-ru, fatyzzz/max-list).

Группы: **VPN · YouTube · Discord · AI · Games**

> Этот репозиторий содержит только результат сборки. Скрипты — в
> [`DigneZzZ/routing-build`](https://github.com/DigneZzZ/routing-build).

---

## Что выбрать

| Устройство | mihomo | Xray / V2Ray |
|---|---|---|
| iPhone, слабое устройство | [`template-mobile.yaml`](template-mobile.yaml) | [`config-ios.json`](v2ray/config-ios.json) |
| Телефон | [`template-mobile.yaml`](template-mobile.yaml) | [`config-mobile.json`](v2ray/config-mobile.json) |
| Телефон, нужен весь реестр РКН | [`template-mobile-full.yaml`](template-mobile-full.yaml) | [`config-mobile-full.json`](v2ray/config-mobile-full.json) |
| Компьютер | [`template-lite.yaml`](template-lite.yaml) | [`config.json`](v2ray/config.json) |
| Компьютер, весь реестр РКН | [`template.yaml`](template.yaml) | [`config_full.json`](v2ray/config_full.json) |

**lite и full отличаются не только размером.** В full входит выжимка из
реестра РКН, и только благодаря ей работает правило «все российские домены —
напрямую»: без неё оно отправило бы напрямую и те ~19 000 заблокированных
сайтов в зоне `.ru`, которые после этого просто не открылись бы. Поэтому в
lite такого правила нет — неизвестный `.ru` идёт через прокси: медленнее, но
работает всегда. Крупные российские сервисы в обоих профилях идут напрямую.

**Мобильные профили отличаются не только объёмом.** В них нет process-правил
(`find-process-mode: off`), поэтому mihomo не делает поиск процесса на каждое
соединение, а все rule-provider'ы подключены в формате `mrs` — скомпилированном
двоичном дереве вместо текста, который ядро держит в памяти построчно.

Вместо `direct` они подключают `direct-core` — тот же набор, но вместо
`geosite:apple` и `geosite:microsoft` в нём короткие списки реально
используемых доменов. В апстримных категориях 3 201 запись, и 2 146 из них —
защитные регистрации торговых марок вроде `applecoronavirus.com`,
`12diasderegalosdeitunes.hn` и `applepaysupplies.berlin`. Ни одно устройство
их не открывает, а место в конфиге они занимают. Если такой домен всё же
понадобится, он просто пойдёт через прокси.

Почему это важно: iOS даёт сетевому расширению **50 MiB на весь процесс**, и
превышение — это не замедление, а мгновенное завершение. Android жёсткого
лимита не имеет, но lmkd убивает VPN-сервис тем охотнее, чем он крупнее.

**`config-ios.json` — отдельная история.** iOS даёт сетевому расширению 50 MiB
на весь процесс, поэтому этот профиль не несёт ничего, что не обязано там быть:
локальные сети, российские сайты, которые не пускают иностранный IP (банки,
госуслуги, связь, транспорт, маркетплейсы), Apple, Microsoft и Google Play.
Всё остальное — игры, Twitch, Pinterest, длинный хвост `geosite:category-ru` —
идёт через прокси и прекрасно там работает. 170 доменов и 15 подсетей вместо
1 297: около 0.1 MiB против 0.7 MiB. Полный список опубликован как
`direct-ios.list`, если захотите собрать свой профиль.

**Последнее правило — «всё остальное в прокси».** Значит, правило «в прокси»
выше по списку меняет исход только там, где ниже стоит DIRECT-правило на тот
же домен. Из 597 доменов проксируемых категорий таких ровно 33 —
`gemini.gstatic.com` под пробником `gstatic.com`, `ads.twitch.tv` под
`twitch.tv`. Остальные 564 повторяли то, что и так делает последнее правило,
и в JSON-конфигах их больше нет. Маршрутизация от этого не изменилась: сборка
прогоняет каждую запись каждого опубликованного набора через готовый профиль и
падает, если хоть одна попала не туда.

---

## Базовый URL

```
https://cdn.jsdelivr.net/gh/DigneZzZ/routing@main/release/<файл>          # jsDelivr, обычно доступнее из РФ
https://raw.githubusercontent.com/DigneZzZ/routing/main/release/<файл>
```

---

## Наборы правил

| Файл | Формат | Записей | .list | .mrs | Назначение |
|---|---|---|---|---|---|
| `reject` | domain · list · mrs | 1,228 | 26.7 KB | 10.9 KB | реклама и телеметрия → REJECT |
| `proxy` | domain · list · mrs | 154 | 3.2 KB | 1.7 KB | Telegram, GitHub, WhatsApp, заблокированные РКН сайты → VPN |
| `discord` | domain · list · mrs | 28 | 0.6 KB | 0.4 KB | Discord → своя группа |
| `ai` | domain · list · mrs | 184 | 3.4 KB | 1.9 KB | ChatGPT, Claude, Gemini, Copilot и другие → VPN |
| `youtube` | domain · list · mrs | 176 | 2.7 KB | 1.3 KB | YouTube → своя группа |
| `crypto` | domain · list · mrs | 96 | 1.4 KB | 0.9 KB | криптобиржи и агрегаторы → VPN |
| `ip-check` | domain · list · mrs | 13 | 0.4 KB | 0.3 KB | сервисы проверки IP → DIRECT (показывают реальный IP) |
| `games` | domain · list · mrs | 116 | 2.4 KB | 1.4 KB | Steam, Epic, Riot, Roblox, EFT → своя группа |
| `direct` | domain · list · mrs | 3,226 | 58.1 KB | 29.8 KB | российские сервисы, Microsoft, Apple, Google Play, Twitch → DIRECT |
| `direct-core` | domain · list · mrs | 1,147 | 17.9 KB | 9.3 KB | то же самое для телефонов: без «парковочных» доменов Apple и Microsoft |
| `direct-ios` | domain · list · mrs | 155 | 2.3 KB | 1.3 KB | минимальный DIRECT: банки, госуслуги, связь, Apple, Microsoft, Google Play |
| `direct-ip` | ipcidr · list · mrs | 18 | 0.3 KB | 0.2 KB | приватные и служебные сети → DIRECT |
| `proxy-ip` | ipcidr · list · mrs | 7 | 0.2 KB | 0.1 KB | CIDR, которые нужно увести из-под geoip:ru → VPN |
| `proxy-ip-full` | ipcidr · list · mrs | 1,612 | 25.8 KB | 6.2 KB | полный набор Telegram / Cloudflare / Discord CIDR |
| `ru-ip` | ipcidr · list · mrs | 25,113 | 435.8 KB | 116.5 KB | российские IP → DIRECT |
| `refilter-domain` | domain · list · mrs | 21,987 | 384.6 KB | 171.8 KB | реестр РКН, только то, что перекрывает DIRECT-правила |
| `refilter-domain-full` | domain · list · mrs | 74,396 | 1295.6 KB | 523.1 KB | полный реестр РКН (нужен только при direct-by-default) |
| `refilter-ip` | ipcidr · list · mrs | 1,120 | 18.7 KB | 2.7 KB | IP из реестра РКН, попадающие в geoip:ru |
| `refilter-ip-full` | ipcidr · list · mrs | 24,961 | 420.0 KB | 49.1 KB | полный IP-реестр РКН |
| `vpndetect` | domain · list · mrs | 13 | 0.4 KB | 0.3 KB |  |
| `refilter-community` | domain · list · mrs | 16 | 0.4 KB | 0.2 KB |  |
| `proc-games` | classical · yaml | 86 | 2.8 KB | — | процессы игровых лаунчеров → DIRECT (десктоп) |
| `proc-torrent` | classical · yaml | 89 | 2.9 KB | — | процессы торрент-клиентов → DIRECT (десктоп) |
| `proc-ru` | classical · yaml | 526 | 18.5 KB | — | Android-пакеты российских приложений (опционально) |

Каждый доменный и IP-набор публикуется в двух форматах: текстовый `.list` и
скомпилированный `.mrs`. **На телефоне используйте `.mrs`** — текстовый
провайдер разбирается построчно и так же и хранится в памяти.

Наборы не пересекаются: домен попадает ровно в один из них, в порядке
приоритета правил. Поэтому `reject` не содержит того, что есть в `proxy`, а
`direct` — того, что уже забрали `proxy`, `ai`, `youtube` или `crypto`.

### Почему `refilter-domain` меньше, чем реестр

Все шаблоны здесь работают по принципу «прокси по умолчанию» (`MATCH,VPN` в
mihomo, `port 0-65535 → proxy` в Xray). Заблокированный домен, который не
попадает ни под одно DIRECT-правило, и так уходит в прокси — держать его в
списке незачем. Остаются только записи, которые действительно перекрывают
DIRECT: домены в российских TLD и поддомены сервисов из `direct`. Это
сокращает набор с ~81 000 записей до ~22 000 без единого изменения в
маршрутизации.

Полные наборы — `refilter-domain-full` и `refilter-ip-full` — нужны только
если у вас обратная схема — «напрямую по умолчанию».

---

## mihomo

Шаблон подписки — один из четырёх файлов. Возьмите тот, что подходит под
устройство, и подставьте его URL в Remnawave:

| Файл | Для кого | Правил загрузится | Реестр РКН |
|---|---|---|---|
| [`template-mobile.yaml`](template-mobile.yaml) | телефон, облегчённый | 28 KB | нет |
| [`template-mobile-full.yaml`](template-mobile-full.yaml) | телефон, полный | 319 KB | да |
| [`template.yaml`](template.yaml) | компьютер, полный | 345 KB | да |
| [`template-lite.yaml`](template-lite.yaml) | компьютер, облегчённый | 54 KB | нет |

Мобильные варианты не просто меньше: в них выключен `find-process-mode`,
поэтому mihomo не ищет процесс на каждое соединение, а все наборы правил
подключены в формате `.mrs` — скомпилированном дереве вместо текста, который
ядро разбирает построчно и так же хранит. Для телефона это разница между
50 КБ и 2 МБ загруженных правил.

`template.yaml` — полный десктопный вариант: имя сохранено, чтобы уже
работающие подписки продолжили получать тот же состав правил.

Если собираете конфиг сами, наборы подключаются так:

```yaml
rule-providers:
  proxy:   { type: http, behavior: domain, format: mrs, interval: 86400, url: "https://cdn.jsdelivr.net/gh/DigneZzZ/routing@main/release/proxy.mrs",   path: ./rs/proxy.mrs }
  direct:  { type: http, behavior: domain, format: mrs, interval: 86400, url: "https://cdn.jsdelivr.net/gh/DigneZzZ/routing@main/release/direct.mrs",  path: ./rs/direct.mrs }
  reject:  { type: http, behavior: domain, format: mrs, interval: 86400, url: "https://cdn.jsdelivr.net/gh/DigneZzZ/routing@main/release/reject.mrs",  path: ./rs/reject.mrs }
  ai:      { type: http, behavior: domain, format: mrs, interval: 86400, url: "https://cdn.jsdelivr.net/gh/DigneZzZ/routing@main/release/ai.mrs",      path: ./rs/ai.mrs }
  youtube: { type: http, behavior: domain, format: mrs, interval: 86400, url: "https://cdn.jsdelivr.net/gh/DigneZzZ/routing@main/release/youtube.mrs", path: ./rs/youtube.mrs }
```

Порядок правил в шаблонах не случаен, и менять его местами не стоит:

```yaml
rules:
  - RULE-SET,direct-ip,DIRECT,no-resolve
  - RULE-SET,reject,REJECT-DROP
  - RULE-SET,proxy,🛡️ VPN
  - RULE-SET,ai,🤖 AI
  - RULE-SET,youtube,📺 YouTube
  - RULE-SET,discord,💬 Discord
  - RULE-SET,crypto,🛡️ VPN
  - RULE-SET,ip-check,DIRECT        # после прокси-сервисов, см. ниже
  - RULE-SET,refilter-d,🛡️ VPN      # перед direct, иначе бесполезен
  - RULE-SET,games,🎮 Игры
  - RULE-SET,direct,DIRECT
  - MATCH,🛡️ VPN
```

`ip-check` стоит после прокси-сервисов намеренно. Источник детекта VPN
перечисляет там же `gstatic.com` и `mtalk.google.com`; если поставить набор
выше, вместе с сервисами проверки IP на прямое соединение уедут Gemini и
Google-push.

---

## V2Ray / Xray

### Самодостаточные конфиги

Все домены встроены в конфиг, `geosite.dat` не нужен.

| Конфиг | Размер | Правил | Для кого |
|---|---|---|---|
| [`config-ios.json`](v2ray/config-ios.json) | 5 KB | 179 | iOS — минимальный, только необходимое |
| [`config-mobile.json`](v2ray/config-mobile.json) | 31 KB | 1,291 | iOS и Android — рекомендуемый |
| [`config-mobile-full.json`](v2ray/config-mobile-full.json) | 587 KB | 24,421 | Android и мощные iOS: + реестр РКН |
| [`config.json`](v2ray/config.json) | 124 KB | 3,397 | десктоп |
| [`config_full.json`](v2ray/config_full.json) | 929 KB | 26,527 | десктоп: + реестр РКН |

> В `outbounds` есть только `direct` и `block`. Добавьте свой outbound с тегом
> `proxy` — без него Xray отбросит соединения (не пустит их напрямую).

### geosite.dat / geoip.dat

```
https://cdn.jsdelivr.net/gh/DigneZzZ/routing@main/v2ray/geosite.dat        # 605.9 KB — с реестром РКН
https://cdn.jsdelivr.net/gh/DigneZzZ/routing@main/v2ray/geoip.dat          # 786.8 KB
https://cdn.jsdelivr.net/gh/DigneZzZ/routing@main/v2ray/happ/geosite.dat   # 157.0 KB — без реестра, для телефонов
https://cdn.jsdelivr.net/gh/DigneZzZ/routing@main/v2ray/happ/geoip.dat     # 775.9 KB
```

Файлы стандартные (protobuf v2ray/v2fly), подходят для V2Ray, Xray, sing-box и
других клиентов. **Ссылка на несуществующую категорию — фатальная ошибка
загрузки конфига**, а не тихий пропуск, поэтому список ниже собран чтением
самих файлов.

<details>
<summary>Категории geosite.dat</summary>

| Категория | Записей | Есть в mobile-файле |
|---|---|---|
| `geosite:category-geoblock-ru` | 21,987 | нет |
| `geosite:apple` | 1,788 | да |
| `geosite:whitelist` | 1,092 | да |
| `geosite:category-ru` | 1,092 | да |
| `geosite:category-ads` | 910 | да |
| `geosite:microsoft` | 736 | да |
| `geosite:win-spy` | 327 | да |
| `geosite:ai` | 193 | да |
| `geosite:youtube` | 177 | да |
| `geosite:private` | 122 | да |
| `geosite:crypto` | 96 | да |
| `geosite:ru-core` | 81 | да |
| `geosite:github` | 64 | да |
| `geosite:steam` | 60 | да |
| `geosite:pinterest` | 52 | да |
| `geosite:microsoft-core` | 49 | да |
| `geosite:banned-ru` | 46 | да |
| `geosite:twitch` | 34 | да |
| `geosite:epicgames` | 30 | да |
| `geosite:discord` | 28 | да |
| `geosite:ai-core` | 25 | да |
| `geosite:google-deepmind` | 25 | да |
| `geosite:telegram` | 21 | да |
| `geosite:apple-core` | 18 | да |
| `geosite:hosting` | 14 | да |
| `geosite:torrent` | 13 | да |
| `geosite:whatsapp` | 13 | да |
| `geosite:origin` | 9 | да |
| `geosite:vpndetect` | 9 | да |
| `geosite:riot` | 8 | да |
| `geosite:google-play` | 8 | да |
| `geosite:ip-check` | 6 | да |
| `geosite:roblox` | 5 | да |
| `geosite:twitch-ads` | 4 | да |
| `geosite:escapefromtarkov` | 3 | да |
| `geosite:faceit` | 2 | да |

</details>

<details>
<summary>Категории geoip.dat</summary>

| Категория | CIDR | Есть в mobile-файле |
|---|---|---|
| `geoip:ru` | 25,113 | да |
| `geoip:whitelist` | 25,113 | да |
| `geoip:blocked-ru` | 1,120 | нет |
| `geoip:private` | 18 | да |
| `geoip:telegram` | 12 | да |

`geoip:whitelist` — прежнее имя для `geoip:ru`, оставлено для конфигов,
импортированных до переименования. В mobile-файле его нет: дублировать 25 000
подсетей ради алиаса — лишние 400 KB на устройстве, которое качает этот файл
каждый день.

</details>

### Пример конфига с .dat

```json
{
  "routing": {
    "domainStrategy": "AsIs",
    "domainMatcher": "hybrid",
    "rules": [
      { "type": "field", "ip": ["geoip:private"], "outboundTag": "direct" },
      { "type": "field", "domain": ["geosite:telegram", "geosite:youtube",
                                    "geosite:ai", "geosite:crypto"],
        "outboundTag": "proxy" },
      { "type": "field", "domain": ["geosite:category-ru", "geosite:apple",
                                    "geosite:microsoft"],
        "outboundTag": "direct" },
      { "type": "field", "ip": ["geoip:ru"], "outboundTag": "direct" },
      { "type": "field", "port": "0-65535", "outboundTag": "proxy" }
    ]
  }
}
```

---

## Happ / INCY

Режим GlobalProxy: всё идёт через VPN, кроме явных DIRECT-правил.

### Импорт по ссылке

| Вариант | Happ | INCY |
|---|---|---|
| **Lite** (рекомендуется) | [📲 Импорт](https://r.far.ovh/?url=happ%3A%2F%2Frouting%2Fonadd%2FeyJOYW1lIjoiRGlnbmVaelogKGxpdGUpIiwiR2xvYmFsUHJveHkiOiJ0cnVlIiwiVXNlQ2h1bmtGaWxlcyI6ImZhbHNlIiwiUmVtb3RlRG5zIjoiOC44LjguOCIsIkRvbWVzdGljRG5zIjoiNzcuODguOC44IiwiUmVtb3RlRE5TVHlwZSI6IkRvSCIsIlJlbW90ZUROU0RvbWFpbiI6Imh0dHBzOi8vOC44LjguOC9kbnMtcXVlcnkiLCJSZW1vdGVETlNJUCI6IjguOC44LjgiLCJEb21lc3RpY0ROU1R5cGUiOiJEb0giLCJEb21lc3RpY0ROU0RvbWFpbiI6Imh0dHBzOi8vNzcuODguOC44L2Rucy1xdWVyeSIsIkRvbWVzdGljRE5TSVAiOiI3Ny44OC44LjgiLCJMYXN0VXBkYXRlZCI6IjIwMjYtMDktMjUiLCJEbnNIb3N0cyI6e30sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6WyJnZW9zaXRlOnByaXZhdGUiLCJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTptaWNyb3NvZnQiLCJnZW9zaXRlOmFwcGxlIiwiZ2Vvc2l0ZTpnb29nbGUtcGxheSIsImdlb3NpdGU6dHdpdGNoIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOnN0ZWFtIiwiZ2Vvc2l0ZTplcGljZ2FtZXMiLCJnZW9zaXRlOm9yaWdpbiIsImdlb3NpdGU6ZXNjYXBlZnJvbXRhcmtvdiIsImdlb3NpdGU6ZmFjZWl0IiwiZ2Vvc2l0ZTpyaW90IiwiZ2Vvc2l0ZTpyb2Jsb3giLCJnZW9zaXRlOmlwLWNoZWNrIiwiZ2Vvc2l0ZTp2cG5kZXRlY3QiXSwiRGlyZWN0SXAiOlsiZ2VvaXA6cHJpdmF0ZSIsImdlb2lwOnJ1Il0sIkJsb2NrU2l0ZXMiOlsiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMiLCJnZW9zaXRlOndpbi1zcHkiLCJnZW9zaXRlOnRvcnJlbnQiXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIiwiR2VvaXB1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvRGlnbmVaelovcm91dGluZ0BtYWluL3YycmF5L2hhcHAvZ2VvaXAuZGF0IiwiR2Vvc2l0ZXVybCI6Imh0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9naC9EaWduZVp6Wi9yb3V0aW5nQG1haW4vdjJyYXkvaGFwcC9nZW9zaXRlLmRhdCIsIlByb3h5U2l0ZXMiOlsiZ2Vvc2l0ZTp0ZWxlZ3JhbSIsImdlb3NpdGU6Z2l0aHViIiwiZ2Vvc2l0ZTpkaXNjb3JkIiwiZ2Vvc2l0ZTp3aGF0c2FwcCIsImdlb3NpdGU6YmFubmVkLXJ1IiwiZ2Vvc2l0ZTpob3N0aW5nIiwiZ2Vvc2l0ZTp0d2l0Y2gtYWRzIiwiZ2Vvc2l0ZTp5b3V0dWJlIiwiZ2Vvc2l0ZTphaSIsImdlb3NpdGU6Y3J5cHRvIl0sIlByb3h5SXAiOlsiZ2VvaXA6dGVsZWdyYW0iXX0%3D) | [📲 Импорт](https://r.far.ovh/?url=incy%3A%2F%2Frouting%2Fonadd%2FeyJOYW1lIjoiRGlnbmVaelogKGxpdGUpIiwiR2xvYmFsUHJveHkiOiJ0cnVlIiwiVXNlQ2h1bmtGaWxlcyI6ImZhbHNlIiwiUmVtb3RlRG5zIjoiOC44LjguOCIsIkRvbWVzdGljRG5zIjoiNzcuODguOC44IiwiUmVtb3RlRE5TVHlwZSI6IkRvSCIsIlJlbW90ZUROU0RvbWFpbiI6Imh0dHBzOi8vOC44LjguOC9kbnMtcXVlcnkiLCJSZW1vdGVETlNJUCI6IjguOC44LjgiLCJEb21lc3RpY0ROU1R5cGUiOiJEb0giLCJEb21lc3RpY0ROU0RvbWFpbiI6Imh0dHBzOi8vNzcuODguOC44L2Rucy1xdWVyeSIsIkRvbWVzdGljRE5TSVAiOiI3Ny44OC44LjgiLCJMYXN0VXBkYXRlZCI6IjIwMjYtMDktMjUiLCJEbnNIb3N0cyI6e30sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6WyJnZW9zaXRlOnByaXZhdGUiLCJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTptaWNyb3NvZnQiLCJnZW9zaXRlOmFwcGxlIiwiZ2Vvc2l0ZTpnb29nbGUtcGxheSIsImdlb3NpdGU6dHdpdGNoIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOnN0ZWFtIiwiZ2Vvc2l0ZTplcGljZ2FtZXMiLCJnZW9zaXRlOm9yaWdpbiIsImdlb3NpdGU6ZXNjYXBlZnJvbXRhcmtvdiIsImdlb3NpdGU6ZmFjZWl0IiwiZ2Vvc2l0ZTpyaW90IiwiZ2Vvc2l0ZTpyb2Jsb3giLCJnZW9zaXRlOmlwLWNoZWNrIiwiZ2Vvc2l0ZTp2cG5kZXRlY3QiXSwiRGlyZWN0SXAiOlsiZ2VvaXA6cHJpdmF0ZSIsImdlb2lwOnJ1Il0sIkJsb2NrU2l0ZXMiOlsiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMiLCJnZW9zaXRlOndpbi1zcHkiLCJnZW9zaXRlOnRvcnJlbnQiXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIiwiR2VvaXB1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvRGlnbmVaelovcm91dGluZ0BtYWluL3YycmF5L2hhcHAvZ2VvaXAuZGF0IiwiR2Vvc2l0ZXVybCI6Imh0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9naC9EaWduZVp6Wi9yb3V0aW5nQG1haW4vdjJyYXkvaGFwcC9nZW9zaXRlLmRhdCIsIlByb3h5U2l0ZXMiOlsiZ2Vvc2l0ZTp0ZWxlZ3JhbSIsImdlb3NpdGU6Z2l0aHViIiwiZ2Vvc2l0ZTpkaXNjb3JkIiwiZ2Vvc2l0ZTp3aGF0c2FwcCIsImdlb3NpdGU6YmFubmVkLXJ1IiwiZ2Vvc2l0ZTpob3N0aW5nIiwiZ2Vvc2l0ZTp0d2l0Y2gtYWRzIiwiZ2Vvc2l0ZTp5b3V0dWJlIiwiZ2Vvc2l0ZTphaSIsImdlb3NpdGU6Y3J5cHRvIl0sIlByb3h5SXAiOlsiZ2VvaXA6dGVsZWdyYW0iXX0%3D) |
| **Full** (весь реестр РКН) | [📲 Импорт](https://r.far.ovh/?url=happ%3A%2F%2Frouting%2Fonadd%2FeyJOYW1lIjoiRGlnbmVaelogKGZ1bGwpIiwiR2xvYmFsUHJveHkiOiJ0cnVlIiwiVXNlQ2h1bmtGaWxlcyI6ImZhbHNlIiwiUmVtb3RlRG5zIjoiOC44LjguOCIsIkRvbWVzdGljRG5zIjoiNzcuODguOC44IiwiUmVtb3RlRE5TVHlwZSI6IkRvSCIsIlJlbW90ZUROU0RvbWFpbiI6Imh0dHBzOi8vOC44LjguOC9kbnMtcXVlcnkiLCJSZW1vdGVETlNJUCI6IjguOC44LjgiLCJEb21lc3RpY0ROU1R5cGUiOiJEb0giLCJEb21lc3RpY0ROU0RvbWFpbiI6Imh0dHBzOi8vNzcuODguOC44L2Rucy1xdWVyeSIsIkRvbWVzdGljRE5TSVAiOiI3Ny44OC44LjgiLCJMYXN0VXBkYXRlZCI6IjIwMjYtMDktMjUiLCJEbnNIb3N0cyI6e30sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6WyJnZW9zaXRlOnByaXZhdGUiLCJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTptaWNyb3NvZnQiLCJnZW9zaXRlOmFwcGxlIiwiZ2Vvc2l0ZTpnb29nbGUtcGxheSIsImdlb3NpdGU6dHdpdGNoIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOnN0ZWFtIiwiZ2Vvc2l0ZTplcGljZ2FtZXMiLCJnZW9zaXRlOm9yaWdpbiIsImdlb3NpdGU6ZXNjYXBlZnJvbXRhcmtvdiIsImdlb3NpdGU6ZmFjZWl0IiwiZ2Vvc2l0ZTpyaW90IiwiZ2Vvc2l0ZTpyb2Jsb3giLCJnZW9zaXRlOmlwLWNoZWNrIiwiZ2Vvc2l0ZTp2cG5kZXRlY3QiXSwiRGlyZWN0SXAiOlsiZ2VvaXA6cHJpdmF0ZSIsImdlb2lwOnJ1Il0sIkJsb2NrU2l0ZXMiOlsiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMiLCJnZW9zaXRlOndpbi1zcHkiLCJnZW9zaXRlOnRvcnJlbnQiXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIiwiR2VvaXB1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvRGlnbmVaelovcm91dGluZ0BtYWluL3YycmF5L2dlb2lwLmRhdCIsIkdlb3NpdGV1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvRGlnbmVaelovcm91dGluZ0BtYWluL3YycmF5L2dlb3NpdGUuZGF0IiwiUHJveHlTaXRlcyI6WyJnZW9zaXRlOnRlbGVncmFtIiwiZ2Vvc2l0ZTpnaXRodWIiLCJnZW9zaXRlOmRpc2NvcmQiLCJnZW9zaXRlOndoYXRzYXBwIiwiZ2Vvc2l0ZTpiYW5uZWQtcnUiLCJnZW9zaXRlOmhvc3RpbmciLCJnZW9zaXRlOnR3aXRjaC1hZHMiLCJnZW9zaXRlOnlvdXR1YmUiLCJnZW9zaXRlOmFpIiwiZ2Vvc2l0ZTpjcnlwdG8iLCJnZW9zaXRlOmNhdGVnb3J5LWdlb2Jsb2NrLXJ1Il0sIlByb3h5SXAiOlsiZ2VvaXA6dGVsZWdyYW0iLCJnZW9pcDpibG9ja2VkLXJ1Il19) | [📲 Импорт](https://r.far.ovh/?url=incy%3A%2F%2Frouting%2Fonadd%2FeyJOYW1lIjoiRGlnbmVaelogKGZ1bGwpIiwiR2xvYmFsUHJveHkiOiJ0cnVlIiwiVXNlQ2h1bmtGaWxlcyI6ImZhbHNlIiwiUmVtb3RlRG5zIjoiOC44LjguOCIsIkRvbWVzdGljRG5zIjoiNzcuODguOC44IiwiUmVtb3RlRE5TVHlwZSI6IkRvSCIsIlJlbW90ZUROU0RvbWFpbiI6Imh0dHBzOi8vOC44LjguOC9kbnMtcXVlcnkiLCJSZW1vdGVETlNJUCI6IjguOC44LjgiLCJEb21lc3RpY0ROU1R5cGUiOiJEb0giLCJEb21lc3RpY0ROU0RvbWFpbiI6Imh0dHBzOi8vNzcuODguOC44L2Rucy1xdWVyeSIsIkRvbWVzdGljRE5TSVAiOiI3Ny44OC44LjgiLCJMYXN0VXBkYXRlZCI6IjIwMjYtMDktMjUiLCJEbnNIb3N0cyI6e30sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6WyJnZW9zaXRlOnByaXZhdGUiLCJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTptaWNyb3NvZnQiLCJnZW9zaXRlOmFwcGxlIiwiZ2Vvc2l0ZTpnb29nbGUtcGxheSIsImdlb3NpdGU6dHdpdGNoIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOnN0ZWFtIiwiZ2Vvc2l0ZTplcGljZ2FtZXMiLCJnZW9zaXRlOm9yaWdpbiIsImdlb3NpdGU6ZXNjYXBlZnJvbXRhcmtvdiIsImdlb3NpdGU6ZmFjZWl0IiwiZ2Vvc2l0ZTpyaW90IiwiZ2Vvc2l0ZTpyb2Jsb3giLCJnZW9zaXRlOmlwLWNoZWNrIiwiZ2Vvc2l0ZTp2cG5kZXRlY3QiXSwiRGlyZWN0SXAiOlsiZ2VvaXA6cHJpdmF0ZSIsImdlb2lwOnJ1Il0sIkJsb2NrU2l0ZXMiOlsiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMiLCJnZW9zaXRlOndpbi1zcHkiLCJnZW9zaXRlOnRvcnJlbnQiXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIiwiR2VvaXB1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvRGlnbmVaelovcm91dGluZ0BtYWluL3YycmF5L2dlb2lwLmRhdCIsIkdlb3NpdGV1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvRGlnbmVaelovcm91dGluZ0BtYWluL3YycmF5L2dlb3NpdGUuZGF0IiwiUHJveHlTaXRlcyI6WyJnZW9zaXRlOnRlbGVncmFtIiwiZ2Vvc2l0ZTpnaXRodWIiLCJnZW9zaXRlOmRpc2NvcmQiLCJnZW9zaXRlOndoYXRzYXBwIiwiZ2Vvc2l0ZTpiYW5uZWQtcnUiLCJnZW9zaXRlOmhvc3RpbmciLCJnZW9zaXRlOnR3aXRjaC1hZHMiLCJnZW9zaXRlOnlvdXR1YmUiLCJnZW9zaXRlOmFpIiwiZ2Vvc2l0ZTpjcnlwdG8iLCJnZW9zaXRlOmNhdGVnb3J5LWdlb2Jsb2NrLXJ1Il0sIlByb3h5SXAiOlsiZ2VvaXA6dGVsZWdyYW0iLCJnZW9pcDpibG9ja2VkLXJ1Il19) |

### Импорт файлом

| Вариант | Happ | INCY |
|---|---|---|
| **Lite** | [`default.json`](v2ray/happ/default.json) | [`default.json`](v2ray/incy/default.json) |
| **Full** | [`full.json`](v2ray/happ/full.json) | [`full.json`](v2ray/incy/full.json) |

### Что делают конфиги

| Порядок | Категории | Куда |
|---|---|---|
| **BLOCK** | `category-ads`, `win-spy`, `torrent` | блокировка |
| **PROXY** | `telegram`, `github`, `discord`, `whatsapp`, `banned-ru`, `hosting`, `twitch-ads`, `youtube`, `ai`, `crypto` + `geoip:telegram` | через VPN |
| **DIRECT** | `private`, `category-ru`, `microsoft`, `apple`, `google-play`, `twitch`, `pinterest`, `steam`, `epicgames`, `origin`, `escapefromtarkov`, `faceit`, `riot`, `roblox`, `ip-check`, `vpndetect` + `geoip:private`, `geoip:ru` | напрямую |
| **DEFAULT** | всё остальное | через VPN |

Full дополнительно подключает `geosite:category-geoblock-ru` и
`geoip:blocked-ru` и ссылается на полные `.dat`; lite берёт файлы из
`v2ray/happ/`.

Telegram проксируется и по домену, и по IP: мобильные клиенты Telegram ходят
на дата-центры по адресу, минуя DNS.

---

## V2RayTUN

V2RayTUN использует встроенные `geosite.dat`/`geoip.dat` (стандарт v2fly),
поэтому конфиг ссылается только на стандартные категории, а свои списки
встроены прямо в правила.

**Способ 1 — в приложении:** Routing → Import → вставьте содержимое
[`routing.json`](v2ray/v2raytun/routing.json).

**Способ 2 — заголовком подписки:** добавьте в заголовки ответа строку из
[`routing_header.txt`](v2ray/v2raytun/routing_header.txt):

```
routing: "<base64>"
```

**Способ 3 — deeplink:** [📲 Импорт](https://r.far.ovh/?url=v2rayTun%3A%2F%2Fimport_route%2FeyJkb21haW5TdHJhdGVneSI6IkFzSXMiLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiaWQiOiJGRTRENjZEQy0yMTBDLTU4NTctQjRGQi04QTlBQkM0MjFGMjUiLCJuYW1lIjoiRGlnbmVaelogUm91dGluZyIsImJhbGFuY2VycyI6W10sInJ1bGVzIjpbeyJ0eXBlIjoiZmllbGQiLCJpZCI6IjY3OTk1QjIyLTUwM0QtNTM1My1BOTc0LUI1NEE2QjEzMzcwMCIsIl9fbmFtZV9fIjoiQmxvY2sgQWRzICYgVHJhY2tlcnMiLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiZG9tYWluIjpbImdlb3NpdGU6Y2F0ZWdvcnktYWRzLWFsbCIsImdlb3NpdGU6d2luLXNweSJdLCJvdXRib3VuZFRhZyI6ImJsb2NrIn0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IjVBMzhEMzNELTVGRUEtNThBQi04Q0I5LTQyREQ5NzU0NkIxOCIsIl9fbmFtZV9fIjoiRGlyZWN0IFByaXZhdGUgSVBzIiwiaXAiOlsiZ2VvaXA6cHJpdmF0ZSJdLCJvdXRib3VuZFRhZyI6ImRpcmVjdCJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiJCN0QwOTRENy1BMUQ5LTVFQkYtQThBRS0yQzdFN0FGNjg1OTQiLCJfX25hbWVfXyI6IkRpcmVjdCBQcml2YXRlIERvbWFpbnMiLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiZG9tYWluIjpbImdlb3NpdGU6cHJpdmF0ZSJdLCJvdXRib3VuZFRhZyI6ImRpcmVjdCJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiJBNTYzMDZCNi1CQUIxLTUyNUQtQUZBOC1CNkFEQkYxQ0JBODYiLCJfX25hbWVfXyI6IkRpcmVjdCBCaXRUb3JyZW50IiwicHJvdG9jb2wiOlsiYml0dG9ycmVudCJdLCJvdXRib3VuZFRhZyI6ImRpcmVjdCJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiIyMjBCQUIzRS02QjBGLTUzNUYtOUU4RS1DMDA2MjZGNDZCMzkiLCJfX25hbWVfXyI6IlByb3h5IFRlbGVncmFtIC8gRGlzY29yZCAvIFdoYXRzQXBwIiwiZG9tYWluTWF0Y2hlciI6Imh5YnJpZCIsImRvbWFpbiI6WyJnZW9zaXRlOnRlbGVncmFtIiwiZ2Vvc2l0ZTpkaXNjb3JkIiwiZ2Vvc2l0ZTp3aGF0c2FwcCIsImdlb3NpdGU6Z2l0aHViIl0sIm91dGJvdW5kVGFnIjoicHJveHkifSx7InR5cGUiOiJmaWVsZCIsImlkIjoiQzZERTE4NDItM0NCOC01QTVCLThDRkItMDExOUE1MTcyOEZDIiwiX19uYW1lX18iOiJQcm94eSBZb3VUdWJlIiwiZG9tYWluTWF0Y2hlciI6Imh5YnJpZCIsImRvbWFpbiI6WyJnZW9zaXRlOnlvdXR1YmUiXSwib3V0Ym91bmRUYWciOiJwcm94eSJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiI3RkU4OUVGMy04N0NGLTU5MzgtQkU2Qy02MEJFQTEwRDhGOEUiLCJfX25hbWVfXyI6IlByb3h5IEFJIiwiZG9tYWluTWF0Y2hlciI6Imh5YnJpZCIsImRvbWFpbiI6WyJkb21haW46Y29waWxvdC5taWNyb3NvZnQuY29tIiwiZG9tYWluOmdpdGh1YmNvcGlsb3QuY29tIl0sIm91dGJvdW5kVGFnIjoicHJveHkifSx7InR5cGUiOiJmaWVsZCIsImlkIjoiOEI3OEIzRjQtNTM4Ri01M0Q4LUFFNjYtOTgyNzM4OUZDM0EyIiwiX19uYW1lX18iOiJQcm94eSBCYW5uZWQgUlUgU2l0ZXMiLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiZG9tYWluIjpbImRvbWFpbjplY2hvLm1zay5ydSIsImRvbWFpbjpqdXQuc3UiLCJkb21haW46a2FyYS5zdSIsImRvbWFpbjprZW1vbm8uc3UiLCJkb21haW46bW9zY293dGltZXMucnUiLCJkb21haW46bm92YXlhZ2F6ZXRhLnJ1IiwiZG9tYWluOnJlcHVibGljLnJ1IiwiZG9tYWluOnNlYXNvbnZhci5ydSIsImRvbWFpbjpzbm9iLnJ1IiwiZG9tYWluOnRoZS12aWxsYWdlLnJ1IiwiZG9tYWluOnRoZWlucy5ydSIsImRvbWFpbjp0dnJhaW4ucnUiXSwib3V0Ym91bmRUYWciOiJwcm94eSJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiIyM0FGMDkzOS05N0FCLTU2OUEtOTg5NS0yM0Q2OEY4MzRDNDkiLCJfX25hbWVfXyI6IkRpcmVjdCBJUC1jaGVjayBFbmRwb2ludHMiLCJkb21haW5NYXRjaGVyIjoiaHlicmlkIiwiZG9tYWluIjpbImRvbWFpbjphcGkuaXBpZnkub3JnIiwiZG9tYWluOmNhbGxzLm9rY2RuLnJ1IiwiZG9tYWluOmNoZWNraXAuYW1hem9uYXdzLmNvbSIsImRvbWFpbjpnb3N1c2x1Z2kucnUiLCJkb21haW46Z3N0YXRpYy5jb20iLCJkb21haW46aWZjb25maWcubWUiLCJkb21haW46aXAubWFpbC5ydSIsImRvbWFpbjppcHY0LWludGVybmV0LnlhbmRleC5uZXQiLCJkb21haW46aXB2Ni1pbnRlcm5ldC55YW5kZXgubmV0IiwiZG9tYWluOm10YWxrLmdvb2dsZS5jb20iLCJkb21haW46cHVzaHRycy5wdXNoLmhpY2xvdWQuY29tIiwiZG9tYWluOnB1c2h0cnMxLnB1c2guaGljbG91ZC5jb20iLCJkb21haW46dG9rZW4tZHJjbi5wdXNoLmRiYW5rY2xvdWQuY29tIl0sIm91dGJvdW5kVGFnIjoiZGlyZWN0In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IjREMkUxRTBBLTg5Q0YtNUM2Ni1BN0UyLTI0OTI3ODZBRDk1MiIsIl9fbmFtZV9fIjoiRGlyZWN0IFJVIFNlcnZpY2VzIiwiZG9tYWluTWF0Y2hlciI6Imh5YnJpZCIsImRvbWFpbiI6WyJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTphcHBsZSIsImdlb3NpdGU6bWljcm9zb2Z0IiwiZ2Vvc2l0ZTpzdGVhbSIsImdlb3NpdGU6ZXBpY2dhbWVzIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOmdvb2dsZS1wbGF5IiwiZ2Vvc2l0ZTpvcmlnaW4iLCJnZW9zaXRlOnR3aXRjaCJdLCJvdXRib3VuZFRhZyI6ImRpcmVjdCJ9LHsidHlwZSI6ImZpZWxkIiwiaWQiOiJBQzBCNjMyOS0wRDJELTVFREItQTA0Ni04NUE3NzhFRkM1MDAiLCJfX25hbWVfXyI6IkRpcmVjdCBSVSBUTERzIiwiZG9tYWluTWF0Y2hlciI6Imh5YnJpZCIsImRvbWFpbiI6WyJkb21haW46cnUiLCJkb21haW46c3UiLCJkb21haW46bW9zY293IiwiZG9tYWluOnhuLS1wMWFpIiwiZG9tYWluOnhuLS1wMWFjZiIsImRvbWFpbjp4bi0tODBhc2VoZGIiLCJkb21haW46eG4tLWMxYXZnIiwiZG9tYWluOnhuLS04MGFzd2ciLCJkb21haW46eG4tLTgwYWR4aGtzIiwiZG9tYWluOnhuLS1kMWFjajNiIl0sIm91dGJvdW5kVGFnIjoiZGlyZWN0In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6IjA3RENGNTU4LUUwNEQtNTUzMC1BOEQ3LThGRDc4Q0JEMzJBQSIsIl9fbmFtZV9fIjoiRGlyZWN0IFJVIElQcyIsImlwIjpbImdlb2lwOnJ1Il0sIm91dGJvdW5kVGFnIjoiZGlyZWN0In0seyJ0eXBlIjoiZmllbGQiLCJpZCI6Ijg1QTZFRjYwLThFRUEtNTJGMS1BQzYzLTM4RDBFM0JFQTRFRCIsIl9fbmFtZV9fIjoiUHJveHkgQWxsIiwicG9ydCI6IjAtNjU1MzUiLCJvdXRib3VuZFRhZyI6InByb3h5In1dfQ%3D%3D)

```
https://raw.githubusercontent.com/DigneZzZ/routing/main/v2ray/v2raytun/routing.json
https://raw.githubusercontent.com/DigneZzZ/routing/main/v2ray/v2raytun/routing_base64.txt
```

---

## Состав репозитория

```
.gitignore                                           0 KB
release/manifest.json                                3 KB
release/proc-games.yaml                              3 KB
release/proc-ru.yaml                                18 KB
release/proc-torrent.yaml                            3 KB
template-lite.yaml                                   8 KB
template-mobile-full.yaml                            9 KB
template-mobile.yaml                                 8 KB
template.yaml                                       10 KB
v2ray/config-ios.json                                5 KB
v2ray/config-mobile-full.json                      587 KB
v2ray/config-mobile.json                            31 KB
v2ray/config.json                                  124 KB
v2ray/config_full.json                             929 KB
v2ray/geoip.dat                                    787 KB
v2ray/geosite.dat                                  606 KB
v2ray/happ/default.json                              2 KB
v2ray/happ/default_deeplink.txt                      2 KB
v2ray/happ/full.json                                 2 KB
v2ray/happ/full_deeplink.txt                         2 KB
v2ray/happ/geoip.dat                               776 KB
v2ray/happ/geosite.dat                             157 KB
v2ray/incy/default.json                              2 KB
v2ray/incy/default_deeplink.txt                      2 KB
v2ray/incy/full.json                                 2 KB
v2ray/incy/full_deeplink.txt                         2 KB
v2ray/v2raytun/routing.json                          4 KB
v2ray/v2raytun/routing_base64.txt                    4 KB
v2ray/v2raytun/routing_deeplink.txt                  4 KB
v2ray/v2raytun/routing_header.txt                    4 KB
```

Всё пересобирается автоматически два раза в сутки через GitHub Actions.
Наборы правил обновляются в клиентах раз в сутки (`interval: 86400`), так что
чаще собирать нечего.

---

## License

Списки принадлежат их авторам. Сборка — MIT.
