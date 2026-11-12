#!/usr/bin/env python3
"""KohNoor static site builder. Reads data.json + content below, writes the site to ./out"""
import json, os, re, shutil, html, random, math
from datetime import date

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SRC, "out")
SITE = "https://kohnoor.pages.dev"
D = json.load(open(os.path.join(SRC, "data.json")))
REGIONS, PLACES, ESS, COSTS, PHOTOS = D["REGIONS"], D["PLACES"], D["ESSENTIALS"], D["COSTS"], D["PHOTOS"]
BYID = {p["id"]: p for p in PLACES}
e = lambda s: html.escape(str(s), quote=True)

for k, v in PHOTOS.items():
    v["src"] = f"/img/{k}.jpg"; v["thumb"] = f"/img/{k}-s.jpg"
import hashlib
ASSET_V = hashlib.md5((open(os.path.join(SRC,"assets","style.css")).read()+open(os.path.join(SRC,"assets","app.js")).read()).encode()).hexdigest()[:8]
CONTACT = json.load(open(os.path.join(SRC, "contact.json"))) if os.path.exists(os.path.join(SRC, "contact.json")) else {}
SIZES = json.load(open(os.path.join(SRC, "img_sizes.json")))
def _srcset(m):
    n, small = m.group(1), bool(m.group(2))
    ws = SIZES.get(n)
    if not ws: return m.group(0)
    if small: ws = [w for w in ws if w <= 1100]
    src = f"/img/{n}-{1100 if 1100 in ws else ws[-1]}.webp" if small else f"/img/{n}-{1920 if 1920 in ws else ws[-1]}.webp"
    sizes = "(max-width: 700px) 92vw, (max-width: 1100px) 46vw, 400px" if small else "100vw"
    return f'<img src="{src}" srcset="{", ".join(f"/img/{n}-{w}.webp {w}w" for w in ws)}" sizes="{sizes}"'
def responsive(html_): return re.sub(r'<img src="/img/([a-z0-9-]+?)(-s)?\.jpg"', _srcset, html_)
REGION_PHOTO = {"swat": "r-swat", "gb": "r-gb", "kaghan": "naran", "chitral": "chitral", "ajk": "arang-kel", "galiyat": "murree", "dir": "kumrat"}
REGION_ORDER = ["gb", "swat", "kaghan", "ajk", "chitral", "dir", "galiyat"]

# ---------------- icons ----------------
I = {
 "drop": '<path d="M12 3s6 6.4 6 11a6 6 0 0 1-12 0c0-4.6 6-11 6-11Z"/>',
 "tree": '<path d="m12 3-6 8h3l-4 6h14l-4-6h3l-6-8Z"/><path d="M12 17v4"/>',
 "landmark": '<path d="M3 21h18M5 21V10m14 11V10M9 21V10m6 11V10M3 10l9-6 9 6H3Z"/>',
 "snow": '<path d="M12 2v20M4.9 6.5l14.2 11M4.9 17.5l14.2-11"/><path d="m9 4 3 2 3-2M9 20l3-2 3 2"/>',
 "family": '<circle cx="8" cy="7" r="3"/><circle cx="17" cy="9" r="2.4"/><path d="M3 20c0-3.3 2.2-6 5-6s5 2.7 5 6M13.5 20c0-2.5 1.6-4.5 3.5-4.5s3.5 2 3.5 4.5"/>',
 "image": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="m3 16 5-5 4 4 3-3 6 6"/><circle cx="16" cy="9" r="1.6"/>',
 "check": '<path d="m5 12 4.5 4.5L19 7"/>',
 "search": '<path d="M11 19a8 8 0 1 1 0-16 8 8 0 0 1 0 16Zm10 2-4.3-4.3"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "mountain": '<path d="m3 20 6.5-11 4 6 2.5-3.5L21 20H3Z"/><path d="m8 11.6 1.5 1.4 1.5-1.2"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "wallet": '<path d="M4 7h14a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a1 1 0 0 1-1-1V7Z"/><path d="M4 7l11-3v3M16 13.5h2"/>',
 "signal": '<path d="M4 20v-3M9 20v-7M14 20V9M19 20V4"/>',
 "fuel": '<path d="M5 20V5a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v15M3 20h13M14 9h2a2 2 0 0 1 2 2v5a1.5 1.5 0 0 0 3 0V8l-3-3"/><path d="M7 8h5"/>',
 "car": '<path d="M5 16h14M6.5 16l1.4-5.2A2 2 0 0 1 9.8 9.3h4.4a2 2 0 0 1 1.9 1.5L17.5 16"/><path d="M4 16v3h2v-2M20 16v3h-2v-2"/>',
 "calendar": '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
 "route": '<circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H15a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h6.5"/>',
 "backpack": '<path d="M7 8a5 5 0 0 1 10 0v11a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1V8Z"/><path d="M10 4V3h4v1M9 13h6v4H9z"/>',
 "shield": '<path d="M12 3 5 6v6c0 4.4 3 7.6 7 9 4-1.4 7-4.6 7-9V6l-7-3Z"/><path d="m9 12 2 2 4-4"/>',
 "wifi": '<path d="M2 9a15 15 0 0 1 20 0M5.5 12.5a10 10 0 0 1 13 0M9 16a5 5 0 0 1 6 0"/><circle cx="12" cy="19.5" r="1"/>',
 "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 "pin": '<path d="M12 21s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12Z"/><circle cx="12" cy="9" r="2.5"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
}
def icon(n): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[n]}</svg>'

GEM = ('<polygon points="8,26 20,12 26,20 32,6 38,20 44,12 56,26 32,58" fill="{f}"/>'
       '<path d="M8 26 H56 M20 12 L32 58 M44 12 L32 58 M26 20 L20 26 M38 20 L44 26 M20 26 L32 58 M44 26 L32 58" stroke="{s}" stroke-width="1.4" fill="none" stroke-linejoin="round"/>'
       '<polygon points="26,20 32,6 38,20 32,27" fill="#E09A3E"/>')
def gem(f="#F5F7F6", s="#9FB4BF"): return f'<svg viewBox="0 0 64 64" aria-hidden="true">{GEM.format(f=f, s=s)}</svg>'

# topographic contour pattern for dark sections
def topo(seed=7):
    r = random.Random(seed); paths = []
    for k in range(14):
        cx, cy, base = r.uniform(0, 1200), r.uniform(0, 500), r.uniform(30, 90)
        for ring in range(5):
            rad = base + ring * 26; pts = []
            for a in range(0, 361, 12):
                t = math.radians(a); wob = 1 + 0.18 * math.sin(3 * t + k) + 0.08 * math.cos(5 * t + ring)
                pts.append(f"{cx + rad * wob * math.cos(t):.0f},{cy + rad * 0.62 * wob * math.sin(t):.0f}")
            paths.append(f'<polyline points="{" ".join(pts)}"/>')
    return f'<svg class="topo" viewBox="0 0 1200 500" preserveAspectRatio="xMidYMid slice" fill="none" stroke="#fff" stroke-width="1" aria-hidden="true">{"".join(paths)}</svg>'

# branded illustration for places without a photo
PAL = {"swat": ["#9ED0C6", "#4E9A7E", "#2E6B57", "#173F33"], "kaghan": ["#A8D4E3", "#5D9EB2", "#2D6D82", "#173F4D"],
       "gb": ["#C5D3EC", "#7F96C2", "#4A5E8E", "#24335A"], "chitral": ["#F0D2A4", "#C49159", "#895B33", "#4E331F"],
       "ajk": ["#BEDFB4", "#69A769", "#3A7345", "#1E4429"], "galiyat": ["#B7D8C3", "#5E9975", "#336A4B", "#193E2B"], "dir": ["#B4D7BD", "#59936F", "#2E6247", "#173726"]}
def art(pid, region, snow=True):
    p = PAL.get(region, PAL["swat"]); r = random.Random(sum(map(ord, pid)))
    def ridge(y, amp, n):
        d = f"M0 {y}"
        for i in range(1, n + 1):
            d += f" L{800 * i / n:.0f} {y - amp * (0.35 + r.random() * 0.65) * (1 if i % 2 else 0.45):.0f}"
        return d + " L800 400 L0 400 Z"
    sx = 120 + r.random() * 560
    return (f'<svg viewBox="0 0 800 400" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs><linearGradient id="g{pid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#0E2433"/><stop offset=".55" stop-color="{p[0]}"/><stop offset="1" stop-color="#F4F6F5"/></linearGradient></defs>'
            f'<rect width="800" height="400" fill="url(#g{pid})"/><circle cx="{sx:.0f}" cy="96" r="30" fill="#E09A3E"/>'
            f'<path d="{ridge(230, 150, 9)}" fill="{"#E8EFF3" if snow else p[1]}"/><path d="{ridge(290, 110, 11)}" fill="{p[2]}"/><path d="{ridge(350, 70, 14)}" fill="{p[3]}"/>'
            f'<g transform="translate(724 22) scale(.9)" opacity=".85">{GEM.format(f="#F5F7F6", s="#9FB4BF")}</g></svg>')

def pic(p, big=False):
    ph = PHOTOS.get(p["id"])
    if ph: return f'<img src="{ph["src"] if big else ph["thumb"]}" alt="{e(p["name"])}"' + ("" if big else ' loading="lazy"') + ' decoding="async">'
    return f'<div class="art">{art(p["id"], p["region"], p["alt"] >= 2300)}</div>' if big else art(p["id"], p["region"], p["alt"] >= 2300)

fmt = lambda n: f"{n:,}"
def first_sentence(t): return t.split(". ")[0].rstrip(".") + "."

# ---------------- layout ----------------
NAV = [("/regions/", "Destinations"), ("/interests/", "Interests"), ("/when-to-go/", "When to go"), ("/map/", "Map"), ("/itineraries/", "Itineraries"), ("/plan/", "Plan a trip"), ("/essentials/", "Essentials")]
def header(active, over, urp=None):
    MM_TOP = ["hunza","skardu","fairy-meadows","attabad","deosai","kalam","malam-jabba","mahodand","mingora","naran","shogran","babusar","neelum","arang-kel","rawalakot","chitral","kalash","kumrat","nathia-gali","murree"]
    def mega():
        cols = "".join(f'<div class="mm-col"><a class="mm-h" href="/regions/{k}/">{e(REGIONS[k]["name"])}</a>' + "".join(f'<a href="/places/{p["id"]}/">{e(p["name"])}</a>' for p in sorted([x for x in PLACES if x["region"] == k and x["kind"] == "famous"], key=lambda x: (MM_TOP.index(x["id"]) if x["id"] in MM_TOP else 99))[:5]) + '</div>' for k in REGION_ORDER)
        return f'<div class="mega"><div class="mm-in">{cols}<a class="mm-all" href="/regions/">All {len(PLACES)} destinations →</a><a class="mm-feat" href="/interests/hidden-gems/"><img src="/img/katora-lake-s.jpg" alt="" loading="lazy"><span><small>Explore</small><b>Hidden gems of the north</b></span></a></div></div>'
    links = "".join((f'<div class="dd"><a href="{u}"{" aria-current=page" if active == u else ""}>{t}</a>{mega()}</div>' if u == "/regions/" else f'<a href="{u}"{" aria-current=page" if active == u else ""}>{t}</a>') for u, t in NAV)
    return f'''<header class="site-head{' over' if over else ''}"><div class="wrap head-in">
<a class="brand" href="/" aria-label="KohNoor home">{gem()}<b>KohNoor</b><span class="ur" lang="ur">کوہِ نور</span></a>
<nav class="nav" aria-label="Main">{links}</nav>
{f'<a class="lang-sw" href="{urp}" lang="ur" hreflang="ur">اردو</a>' if urp else ''}<button class="icon-btn" data-open-search aria-label="Search places">{icon("search")}</button>
<button class="icon-btn menu-btn" aria-label="Menu" aria-expanded="false">{icon("menu")}</button>
</div></header>
<div class="search-ov" role="dialog" aria-label="Search"><div class="search-box"><label for="search-input" class="sr">Search places</label>
<input id="search-input" type="search" placeholder="Search a valley, lake or town…" autocomplete="off"><div class="search-res"></div></div></div>'''

def footer():
    regs = "".join(f'<a href="/regions/{k}/">{e(REGIONS[k]["name"])}</a>' for k in REGION_ORDER)
    top = "".join(f'<a href="/places/{i}/">{e(BYID[i]["name"])}</a>' for i in ["hunza", "skardu", "kalam", "naran", "fairy-meadows", "neelum"])
    return f'''<footer class="site-foot">{topo(3)}<div class="wrap"><div class="foot-grid">
<div><a class="brand" href="/">{gem()}<b>KohNoor</b></a><p>The jewel of the mountains: the complete, honest guide to Northern Pakistan. Places, history, live weather, trip costs and offline essentials.</p><p class="ur" lang="ur" style="font-size:18px;color:#fff">کوہِ نور — شمالی پاکستان کا مکمل رہنما</p></div>
<div><h4>Regions</h4>{regs}</div><div><h4>Top places</h4>{top}</div>
<div><h4>Plan</h4><a href="/interests/">Travel by interest</a><a href="/when-to-go/">When to go</a><a href="/gallery/">Photo gallery</a><a href="/list-your-business/">List your business</a><a href="/ur/" lang="ur">اردو</a><a href="/itineraries/">Itineraries</a><a href="/plan/">Trip cost planner</a><a href="/essentials/">Offline essentials</a><a href="/about/">About KohNoor</a></div>
</div><div class="foot-bottom"><span>© {date.today().year} KohNoor. Costs and travel times are estimates; check road status before you travel.</span><span>Weather: Open-Meteo · Photos used under free licences</span></div></div></footer>
<div class="net" role="status">You are offline · saved pages still work</div>'''

def ur_path(path):
    if path.startswith("/ur/"): return path
    if path == "/" or path in UR_PATHS: return "/ur" + path
    return None
def en_path(path): return path[3:] if path.startswith("/ur/") else path
def page(path, title, desc, body, active="", over=False, og=None, body_attr="", jsonld=None, lang="en"):
    og = og or "/assets/og-default.jpg"
    brand = "کوہِ نور" if lang == "ur" else "KohNoor"
    full = title if title.startswith("KohNoor") or title.startswith("کوہِ نور") else f"{title} | {brand}"
    enp, urp = en_path(path), ur_path(en_path(path))
    alts = (f'<link rel="alternate" hreflang="en" href="{SITE}{enp}"><link rel="alternate" hreflang="ur" href="{SITE}{urp}"><link rel="alternate" hreflang="x-default" href="{SITE}{enp}">') if urp else ""
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    doc = f'''<!DOCTYPE html>
<html lang="{lang}" dir="{'rtl' if lang == 'ur' else 'ltr'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="msvalidate.01" content="63E67156202205CA85D99A9BBF952FAC">
<title>{e(full)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{SITE}{path}">{alts}
<meta property="og:type" content="website"><meta property="og:site_name" content="KohNoor"><meta property="og:title" content="{e(full)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{SITE}{path}"><meta property="og:image" content="{SITE}{og}">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#0E2433">
<link rel="manifest" href="/manifest.webmanifest"><link rel="icon" href="/assets/icon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/icon-180.png">
<link rel="preload" href="/assets/fonts/bricolage-grotesque-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/style.css?v={ASSET_V}">{ld}</head>
<body{body_attr}>{header_ur(active, over, enp) if lang == "ur" else header(active, over, urp)}<main id="main">{body}</main>{footer_ur() if lang == "ur" else footer()}
<script src="/assets/data.js?v={ASSET_V}" defer></script><script src="/assets/app.js?v={ASSET_V}" defer></script></body></html>'''
    dest = os.path.join(OUT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "w").write(responsive(doc))

def card(p, dark=False, near_km=None):
    hid = ('<span class="badge hidden">Hidden</span>' if p["kind"] == "hidden" else "") + (f'<span class="badge">≈ {near_km:.0f} km away</span>' if near_km is not None else "")
    return f'''<a class="card" href="/places/{p["id"]}/" data-months="{p["months"]}"><div class="pic">{pic(p)}<div class="badges">{hid}</div></div>
<div class="body"><span class="region">{e(REGIONS[p["region"]]["name"])}</span><h3>{e(p["name"])}</h3><p>{e(first_sentence(p["intro"]))}</p>
<div class="meta"><span>{icon("mountain")}{fmt(p["alt"])} m</span><span>{icon("clock")}{e(p["hrs"])} h</span><span class="price" data-price="{p["id"]}"></span></div></div></a>'''

def hero(img_html, kicker, title, ur="", lede="", crumbs="", extra="", short=False, credit=""):
    return f'''<section class="hero{' short' if short else ''}">{img_html}<div class="wrap in">{f'<div class="crumbs">{crumbs}</div>' if crumbs else ''}<span class="kicker">{kicker}</span><h1>{title}</h1>{f'<span class="ur" lang="ur">{ur}</span>' if ur else ''}{f'<p class="lede">{lede}</p>' if lede else ''}{extra}</div>{f'<span class="credit">{e(credit)}</span>' if credit else ''}</section>'''

# ---------------- content: itineraries ----------------
ITINS = [
 {"id": "swat-4-days", "title": "Swat Valley in 4 days", "from": "Islamabad", "days": 4, "best": "Apr–Oct", "budget": "From Rs 25k pp", "region": "swat", "photo": "kalam",
  "intro": "The easiest mountain trip from Islamabad: Buddhist history around Mingora, riverside towns, and the pine forests and lakes above Kalam.",
  "plan": [("Islamabad to Mingora", "Drive the M-1 and Swat Expressway (4–5 h). Afternoon at the Swat Museum and Butkara stupa, evening in Mingora bazaar.", ["mingora", "swat-museum", "butkara"]),
           ("Up the valley to Kalam", "Leave early. Trout lunch in Madyan, tea stop in Bahrain, reach Kalam by afternoon and walk into the Ushu forest.", ["madyan", "bahrain", "kalam"]),
           ("Mahodand Lake by jeep", "Full-day jeep trip through Ushu and Matiltan to Mahodand Lake (June–September). Back in Kalam for the night.", ["ushu-matiltan", "mahodand"]),
           ("Back to Islamabad", "Start by 7 am. Optional detour to Malam Jabba if the day allows.", ["malam-jabba"])]},
 {"id": "naran-weekend", "title": "Naran & Kaghan long weekend", "from": "Islamabad", "days": 3, "best": "Jun–Sep", "budget": "From Rs 22k pp", "region": "kaghan", "photo": "naran",
  "intro": "Lakes of folklore, high meadows and the road to Babusar Pass, done as a three-day summer escape.",
  "plan": [("Islamabad to Naran", "Hazara Motorway to Mansehra, then Balakot and Kaghan (6–7 h). Evening walk along the Kunhar.", ["kaghan", "naran"]),
           ("Saif-ul-Malook, Lulusar and Babusar", "Early jeep to Lake Saif-ul-Malook, then drive up past Lulusar Lake to Babusar Top (open about June–October).", ["naran", "babusar"]),
           ("Return via Shogran (optional)", "Head back down the valley. With time, take the jeep from Kiwai up to Shogran and Siri Paye.", ["shogran"])]},
 {"id": "hunza-skardu-8-days", "title": "Hunza & Skardu: the classic north", "from": "Islamabad", "days": 8, "best": "May–Oct", "budget": "From Rs 70k pp", "region": "gb", "photo": "hunza",
  "intro": "The big one: over Babusar to the Karakoram Highway, the forts of Hunza and the Chinese border, then the lakes and cold desert of Baltistan.",
  "plan": [("Islamabad to Naran", "Long first day via the Hazara Motorway and Kaghan Valley.", ["naran"]),
           ("Over Babusar to Gilgit", "Cross Babusar Top (summer only), descend to Chilas and follow the Indus to Gilgit.", ["babusar", "chilas", "gilgit"]),
           ("Gilgit to Hunza", "Short drive past Rakaposhi viewpoint. Afternoon at Baltit and Altit forts, sunset from Eagle's Nest.", ["hunza"]),
           ("Attabad, Passu and Khunjerab", "Boat on Attabad Lake, photos at the Passu Cones, then up to Khunjerab Pass on the China border.", ["attabad", "passu-khunjerab"]),
           ("Hunza to Skardu", "Back through Gilgit and along the Indus gorge to Skardu (about 6–7 h).", ["skardu"]),
           ("Skardu lakes and Shigar", "Shangrila and Upper Kachura lakes in the morning, Shigar Fort and the cold desert in the afternoon.", ["skardu", "shigar"]),
           ("Deosai Plains", "Full-day jeep trip to Deosai and Sheosar Lake (July–September).", ["deosai"]),
           ("Fly home", "Morning flight Skardu–Islamabad (weather permitting), or two days back by road.", [])]},
 {"id": "neelum-4-days", "title": "Neelum Valley in 4 days", "from": "Islamabad", "days": 4, "best": "Apr–Oct", "budget": "From Rs 24k pp", "region": "ajk", "photo": "arang-kel",
  "intro": "Green, quiet Kashmir along the Neelum River, from Keran's riverbanks to the storybook village of Arang Kel.",
  "plan": [("Islamabad to Keran", "Via Murree and Muzaffarabad, then up the Neelum road to Keran.", ["muzaffarabad", "neelum"]),
           ("Sharda and Kel", "Morning at the Sharda ruins, continue to Kel for the night.", ["neelum"]),
           ("Arang Kel", "Cable car across the river and a steep walk up to the meadow village. Sunset over the valley.", ["arang-kel"]),
           ("Back to Islamabad", "A long drive back. In July–September, add a day for Ratti Gali Lake by jeep from Dowarian.", ["ratti-gali"])]},
 {"id": "chitral-kalash-6-days", "title": "Chitral & the Kalash valleys", "from": "Islamabad", "days": 6, "best": "May–Oct", "budget": "From Rs 45k pp", "region": "chitral", "photo": "chitral",
  "intro": "Through the Lowari Tunnel to Chitral under Tirich Mir, and into the Kalash valleys with their own faith, dress and festivals.",
  "plan": [("Islamabad to Dir", "Swat Expressway to Chakdara, then up to Dir for the night.", []),
           ("Lowari Tunnel to Chitral", "Through the tunnel and down to Chitral. Evening at the Shahi Mosque and the fort.", ["chitral"]),
           ("Bumburet, Kalash", "Drive to Bumburet. Kalasha Dur museum and village walks with a local guide.", ["kalash"]),
           ("Rumbur or Garam Chashma", "Quieter Rumbur valley, or the hot springs at Garam Chashma.", ["kalash", "chitral"]),
           ("Chitral to Dir (or Kumrat)", "Return through the tunnel. In summer, turn off at Thall for a night in Kumrat.", ["kumrat"]),
           ("Back to Islamabad", "Down through Chakdara and the Swat Expressway.", [])]},
 {"id": "murree-galiyat-2-days", "title": "Murree & Galiyat family weekend", "from": "Islamabad", "days": 2, "best": "All year", "budget": "From Rs 12k pp", "region": "galiyat", "photo": "murree",
  "intro": "The closest mountains to the capital: Mall Road, pine forest walks and the Pipeline Track, without long drives.",
  "plan": [("Murree", "Mall Road, Kashmir Point and the Patriata chairlift.", ["murree"]),
           ("Nathia Gali and Ayubia", "Walk the flat Pipeline Track from Dunga Gali to Ayubia, then drive home.", ["nathia-gali"])]},
]

# ---------------- builders ----------------
def build_home():
    feat = ["hunza", "skardu", "kalam", "naran", "fairy-meadows", "attabad", "neelum", "kumrat"]
    tiles = []
    for i, k in enumerate(REGION_ORDER):
        r = REGIONS[k]; n = sum(1 for p in PLACES if p["region"] == k)
        cls = "big" if i == 0 else ("wide" if i in (3, 6) else "")
        tiles.append(f'<a class="tile {cls}" href="/regions/{k}/"><img src="/img/{REGION_PHOTO[k]}{"" if i in (0, 3, 6) else "-s"}.jpg" alt="" loading="lazy"><div class="t"><h3>{e(r["name"])}</h3><span>{n} destinations</span></div></a>')
    seasons = [("Spring · Mar–Apr", "Blossom season", "Apricot and cherry blossom in Hunza and Skardu.", "hunza", "/regions/gb/"),
               ("Summer · Jun–Sep", "High meadows & lakes", "Babusar, Deosai and the jeep lakes open up.", "naran", "/regions/kaghan/"),
               ("Autumn · Oct–Nov", "Gold valleys", "Poplars turn gold in Hunza, Ghizer and Skardu.", "passu-khunjerab", "/places/phander/"),
               ("Winter · Dec–Feb", "Snow & skiing", "Malam Jabba, Murree and Nathia Gali under snow.", "malam-jabba", "/places/malam-jabba/")]
    sea = "".join(f'<a class="season" href="{u}"><img src="/img/{ph}-s.jpg" alt="" loading="lazy"><div class="t"><small>{s}</small><h3>{t}</h3><p>{d}</p></div></a>' for s, t, d, ph, u in seasons)
    hidden = [p for p in PLACES if p["kind"] == "hidden"]
    itin = "".join(itin_card(x) for x in ITINS[:3])
    body = hero('<img src="/img/home.jpg" alt="Hunza Valley in autumn" fetchpriority="high">', "Northern Pakistan travel guide",
                "Every valley. Every road. One guide.", "شمالی پاکستان کا مکمل رہنما",
                "From the forts of Hunza to the lakes of Swat: places and their history, live weather, real trip costs from Islamabad, Peshawar and Lahore, and offline essentials for where the signal ends.",
                extra=f'''<div class="hero-search"><button data-open-search>{icon("search")}Where do you want to go?</button></div>
<div class="chips">{"".join(f'<a class="chip" href="/interests/{t["slug"]}/">{icon(t["icon"])}{e(t["name"])}</a>' for t in THEMES[:6])}</div>''', credit="Hunza Valley in autumn")
    body += f'''<div class="strip"><div class="wrap"><div><b>{len(PLACES)}</b><span>destinations, famous and hidden</span></div><div><b>{len(REGIONS)}</b><span>regions, from Murree to Khunjerab</span></div><div><b>Live</b><span>weather for every place</span></div><div><b>Offline</b><span>works where the signal ends</span></div></div></div>
<section class="block"><div class="wrap"><div class="sec-head"><div><span class="kicker">Choose your trip</span><h2>Travel the north your way</h2><p>Start with what you love. Every interest page lists the places that fit, with season, travel time and cost.</p></div><a class="more" href="/interests/">All interests →</a></div><div class="interests">{"".join(theme_card(t) for t in THEMES)}</div></div></section>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">Where to go</span><h2>Seven regions, one north</h2><p>Each region page has its history, quick facts and every place we cover there.</p></div><a class="more" href="/regions/">All destinations →</a></div><div class="mosaic">{"".join(tiles)}</div></div></section>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">Explore the map</span><h2>Every place, one map</h2><p>Gold pins are the famous names, green pins the hidden places. Tap any pin for its guide.</p></div><a class="more" href="/map/">Full-screen map →</a></div>{map_box()}</div></section>
<section class="block dark alt-sec">{topo(4)}<div class="wrap" style="position:relative"><div class="sec-head"><div><span class="kicker">How high you go</span><h2>From 980 m to the roof of the KKH</h2><p>The altitude of the places you can drive or hike to. Above about 2,500 m, go slowly and drink plenty of water.</p></div></div>{alt_chart()}</div></section>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">Top destinations</span><h2>The great names of the north</h2></div><a class="more" href="/regions/">See all {len(PLACES)} →</a></div><div class="grid">{"".join(card(BYID[i]) for i in feat)}</div></div></section>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">In season</span><h2>Best right now: <span data-now-month></span></h2><p>Places at their best this month, with a budget price per person for two nights from Islamabad.</p></div></div><div class="grid" id="best-now"></div></div></section>
<section class="block"><div class="wrap"><div class="sec-head"><div><span class="kicker">Plan your trip</span><h2>Tools for the road</h2></div></div><div class="tools">
<a class="tool-card" href="/plan/"><span class="ico">{icon("wallet")}</span><h3>Trip cost planner</h3><p>Fuel, coach, hotel, food and jeep costs from Islamabad, Peshawar or Lahore, for your group.</p><b>Estimate a trip →</b></a>
<a class="tool-card" href="/itineraries/"><span class="ico">{icon("route")}</span><h3>Ready itineraries</h3><p>Day-by-day plans from a 2-day Murree weekend to 8 days across Hunza and Skardu.</p><b>Pick a route →</b></a>
<a class="tool-card" href="/essentials/"><span class="ico">{icon("shield")}</span><h3>Offline essentials</h3><p>Emergency numbers, altitude sickness, mountain driving and which network works where.</p><b>Save for offline →</b></a>
</div></div></section>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">Four seasons</span><h2>When to go</h2></div></div><div class="seasons">{sea}</div></div></section>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">Itineraries</span><h2>Routes that work</h2></div><a class="more" href="/itineraries/">All itineraries →</a></div><div class="grid">{itin}</div></div></section>
<section class="block dark">{topo(11)}<div class="wrap" style="position:relative"><div class="sec-head"><div><span class="kicker">Hidden places</span><h2>Beyond the famous names</h2><p>Quiet lakes and meadows with far fewer visitors. Information is thinner here, so travel with a local guide.</p></div></div><div class="grid">{"".join(card(p) for p in hidden[:8])}</div><a class="btn" style="margin-top:30px" href="/interests/hidden-gems/">See all {len(hidden)} hidden places →</a></div></section>
<section class="block tight"><div class="wrap"><div class="why">
<div>{icon("wallet")}<h3>Honest costs</h3><p>Real fuel, coach, hotel and jeep prices from Islamabad, Peshawar and Lahore.</p></div>
<div>{icon("sun")}<h3>Live weather</h3><p>Current conditions and a 5-day forecast on every place page.</p></div>
<div>{icon("wifi")}<h3>Works offline</h3><p>Pages you open are saved for valleys with no signal.</p></div>
<div>{icon("check")}<h3>Free, no booking push</h3><p>A guide, not a tour shop: plan your own trip your own way.</p></div>
</div></div></section>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">Questions</span><h2>Before you go</h2></div><a class="more" href="/when-to-go/">Best time calendar →</a></div>{faq_html(FAQ)}</div></section>
<section class="block"><div class="wrap"><div class="cta">{topo(5)}<div style="position:relative"><span class="kicker">Works offline</span><h2>Keep KohNoor on your phone</h2><p>Install it like an app. Pages you open are saved, so the guide, your packing list and emergency numbers still work in the mountains.</p></div>
<div class="steps" style="position:relative"><div><b>Android:</b> Chrome menu → Add to Home screen</div><div><b>iPhone:</b> Safari share → Add to Home Screen</div><div><b>Tip:</b> open your destinations once while you have signal</div></div></div></div></section>'''
    ld = {"@context": "https://schema.org", "@type": "WebSite", "name": "KohNoor", "url": SITE + "/", "description": "The complete travel guide to Northern Pakistan.",
          "potentialAction": {"@type": "SearchAction", "target": SITE + "/plan/?place={search_term_string}", "query-input": "required name=search_term_string"}}
    ld = [ld, faq_ld(FAQ)]
    page("/", "KohNoor — The complete travel guide to Northern Pakistan",
         "Plan trips to Hunza, Skardu, Swat, Naran, Neelum, Chitral and more: places and history, live weather, trip costs from Islamabad, Peshawar and Lahore, itineraries and offline essentials.",
         body, over=True, jsonld=ld)

def itin_card(x):
    return f'''<a class="card" href="/itineraries/{x["id"]}/"><div class="pic"><img src="/img/{x["photo"]}-s.jpg" alt="" loading="lazy"><div class="badges"><span class="badge">{x["days"]} days</span></div></div>
<div class="body"><span class="region">{e(REGIONS[x["region"]]["name"])}</span><h3>{e(x["title"])}</h3><p>{e(x["intro"])}</p><div class="meta"><span>{icon("calendar")}{x["best"]}</span><span class="price">{x["budget"]}</span></div></div></a>'''

def build_regions():
    cards = "".join(f'''<a class="card" href="/regions/{k}/"><div class="pic"><img src="/img/{REGION_PHOTO[k]}-s.jpg" alt="" loading="lazy"></div><div class="body"><h3>{e(REGIONS[k]["name"])}</h3><p>{e(REGIONS[k]["lede"])}</p><div class="meta"><span>{icon("pin")}{sum(1 for p in PLACES if p["region"] == k)} destinations</span></div></div></a>''' for k in REGION_ORDER)
    body = hero('<img src="/img/r-gb.jpg" alt="">', "Destinations", "Where to go in the north", "منزلیں", "Seven regions, from the hill stations near Islamabad to the Karakoram on the China border.", short=True)
    body += f'<section class="block"><div class="wrap"><div class="grid">{cards}</div></div></section>'
    body += f'<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">A–Z</span><h2>All {len(PLACES)} destinations</h2></div></div><div class="grid">{"".join(card(p) for p in sorted(PLACES, key=lambda p: (p["kind"] != "famous", p["name"])))}</div></div></section>'
    page("/regions/", "Destinations in Northern Pakistan", "All regions and destinations of Northern Pakistan: Gilgit-Baltistan, Swat, Kaghan, Azad Kashmir, Chitral, Dir and Galiyat.", body, active="/regions/", over=True)
    for k in REGION_ORDER:
        r = REGIONS[k]; ps = [p for p in PLACES if p["region"] == k]; ps.sort(key=lambda p: p["kind"] != "famous")
        facts = "".join(f"<dt>{e(a)}</dt><dd>{e(b)}</dd>" for a, b in r["facts"].items())
        body = hero(f'<img src="/img/{REGION_PHOTO[k]}.jpg" alt="">', "Region", e(r["name"]), e(r["ur"]), e(r["lede"]), crumbs='<a href="/">Home</a> › <a href="/regions/">Destinations</a>', short=True)
        body += f'''<div class="wrap"><div class="layout"><div class="prose"><h2>About the region</h2>{"".join(f"<p>{e(t)}</p>" for t in r["about"])}<h2>A short history</h2>{"".join(f"<p>{e(t)}</p>" for t in r["history"])}</div>
<aside><div class="card-box"><h3>Quick facts</h3><dl class="kv">{facts}</dl></div></aside></div></div>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">Map</span><h2>{e(r["name"])} on the map</h2></div></div>{map_box(region=k)}</div></section>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">{len(ps)} destinations</span><h2>Places in {e(r["name"])}</h2></div></div><div class="grid">{"".join(card(p) for p in ps)}</div></div></section>'''
        ld = {"@context": "https://schema.org", "@type": "TouristDestination", "name": r["name"], "description": r["lede"], "url": f"{SITE}/regions/{k}/",
              "includesAttraction": [{"@type": "TouristAttraction", "name": p["name"], "url": f"{SITE}/places/{p['id']}/"} for p in ps]}
        page(f"/regions/{k}/", f"{r['name']} travel guide", r["lede"], body, active="/regions/", over=True, og=f"/img/{REGION_PHOTO[k]}.jpg", jsonld=ld)

def build_places():
    for p in PLACES:
        r = REGIONS[p["region"]]; ph = PHOTOS.get(p["id"])
        months = "".join(f'<span class="m{v}" title="{m}">{m[:3]}</span>' for v, m in zip(p["months"], ["January","February","March","April","May","June","July","August","September","October","November","December"]))
        d = COSTS["delta"][p["route"]]
        def hrs(add):
            m = re.match(r"^(\d+(?:\.\d+)?)(?:–(\d+(?:\.\d+)?))?(.*)$", p["hrs"])
            if not m: return f'{p["hrs"]} h from Islamabad, {"+" if add > 0 else "−"}{abs(add)} h'
            fx = lambda v: f"{max(1, float(v) + add):g}"
            return f'{fx(m.group(1))}{("–" + fx(m.group(2))) if m.group(2) else ""}{m.group(3)} h'
        rows = [("Islamabad", p["km"], p["hrs"] + " h"), ("Peshawar", max(30, p["km"] + d["psh"]), hrs(d["pshH"])), ("Lahore", max(30, p["km"] + d["lhr"]), hrs(d["lhrH"]))]
        dist = "".join(f'<tr><td>{a}</td><td class="num">≈ {fmt(b)} km</td><td class="num">{e(c)}</td></tr>' for a, b, c in rows)
        fly = f'<p class="note">✈ {e(COSTS["flights"][p["fly"]])}</p>' if p.get("fly") and p["fly"] in COSTS["flights"] else ""
        near = nearest(p, 4)
        tags = "".join(f'<a class="chip" href="/interests/{t["slug"]}/">{icon(t["icon"])}{e(t["name"])}</a>' for t in THEMES_OF.get(p["id"], []))
        bbox = f'{p["lon"]-0.08:.3f}%2C{p["lat"]-0.05:.3f}%2C{p["lon"]+0.08:.3f}%2C{p["lat"]+0.05:.3f}'
        hidden_alert = '<div class="alert"><b>Less verified place.</b> Information is thinner than for famous spots. Go with a local guide and ask in the nearest town about the route.</div>' if p["kind"] == "hidden" else ""
        body = hero(pic(p, True), ("Hidden place · " if p["kind"] == "hidden" else "") + e(r["name"]), e(p["name"]), e(p["ur"]), e(p["intro"]),
                    crumbs=f'<a href="/">Home</a> › <a href="/regions/{p["region"]}/">{e(r["name"])}</a>', credit=(ph or {}).get("credit", ""))
        body += f'''<nav class="subnav" aria-label="On this page"><div class="wrap"><a href="#overview">Overview</a><a href="#todo">Things to do</a><a href="#history">History</a><a href="#getting-there">Getting there</a><a href="#costs">Costs</a><a href="#packing">What to pack</a><a href="#stay">Stay & eat</a><a href="#map">Map</a></div></nav>
<div class="wrap"><div class="glance">
<div>{icon("mountain")}<span><small>Altitude</small><b>≈ {fmt(p["alt"])} m</b></span></div>
<div>{icon("clock")}<span><small>From Islamabad</small><b>{e(p["hrs"])} h</b></span></div>
<div>{icon("wallet")}<span><small>Budget trip</small><b data-price="{p["id"]}">—</b></span></div>
<div>{icon("signal")}<span><small>Mobile signal</small><b>{e(p["network"])}</b></span></div>
</div>
<div class="layout"><div class="prose">
<h2 id="overview">Overview</h2><p class="lead">{e(p["intro"])}</p>{f'<div class="chips light tags">{tags}</div>' if tags else ''}
<div id="closed-now" class="alert closed" hidden><b><span data-now-month></span>: usually closed or not advised.</b> Snow or weather normally blocks this place now. Best season: {e(p["season"])}.</div>{hidden_alert}
<div class="card-box"><h3>When to go</h3><div class="months">{months}</div><div class="legend"><span><i class="m2"></i>Best</span><span><i class="m1"></i>Possible</span><span><i class="m0"></i>Closed or not advised</span></div></div>
<h2 id="todo">Top things to do</h2><ol class="top">{"".join(f"<li>{e(t)}</li>" for t in p["todo"])}</ol>
<h2 id="history">History</h2><p>{e(p["history"])}</p>
<h2 id="getting-there">Getting there</h2><p>{e(p["reach"])}</p>
<div class="table"><table><thead><tr><th>From</th><th style="text-align:right">Distance</th><th style="text-align:right">Drive time</th></tr></thead><tbody>{dist}</tbody></table></div>{fly}
<h2 id="costs">Trip cost</h2><div class="card-box" id="calc"><p class="note">Loading the cost planner…</p></div>
<h2 id="packing">What to pack</h2><div class="card-box" id="packs"></div>
<h2 id="stay">Where to stay & eat</h2><p><b>Stay:</b> {e(p["stay"])}</p><p><b>Food:</b> {e(p["food"])}</p>
<h2>Good to know</h2><ul>{"".join(f"<li>{e(t)}</li>" for t in p["tips"])}</ul>
<h2 id="map">Map</h2><iframe class="map" loading="lazy" title="Map of {e(p["name"])}" src="https://www.openstreetmap.org/export/embed.html?bbox={bbox}&amp;layer=mapnik&amp;marker={p["lat"]}%2C{p["lon"]}"></iframe>
<p class="note">Location is approximate. <a href="https://www.google.com/maps/search/?api=1&amp;query={p["lat"]},{p["lon"]}" rel="noopener">Open in Google Maps</a></p>
</div>
<aside><div class="sticky"><div class="card-box" id="wx"><h3>Weather now</h3><p class="note">Loading live weather…</p></div>
<div class="card-box"><h3>Quick facts</h3><dl class="kv"><dt>Best season</dt><dd>{e(p["season"])}</dd><dt>Vehicle</dt><dd>{e(p["vehicle"])}</dd><dt>Fuel & cash</dt><dd>{e(p["fuel"])}</dd><dt>Signal</dt><dd>{e(p["network"])}</dd></dl></div>
<div class="card-box"><h3>Road status</h3><p style="margin:0;font-size:15.5px">Roads in the north change with weather. Ask local police or your hotel before you set out, especially after rain or snow.</p></div></div></aside>
</div></div>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">Nearby</span><h2>Closest places to {e(p["name"])}</h2><p>Straight-line distance; road distance is longer in the mountains.</p></div><a class="more" href="/regions/{p["region"]}/">All of {e(r["name"])} →</a></div><div class="grid g4">{"".join(card(x, near_km=dk) for dk, x in near)}</div></div></section>'''
        ld = [{"@context": "https://schema.org", "@type": "TouristAttraction", "name": p["name"], "description": p["intro"], "url": f"{SITE}/places/{p['id']}/",
               "image": SITE + (ph["src"] if ph else "/assets/og-default.jpg"), "geo": {"@type": "GeoCoordinates", "latitude": p["lat"], "longitude": p["lon"], "elevation": p["alt"]},
               "containedInPlace": {"@type": "Place", "name": r["name"] + ", Pakistan"}},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                  {"@type": "ListItem", "position": 2, "name": r["name"], "item": f"{SITE}/regions/{p['region']}/"},
                  {"@type": "ListItem", "position": 3, "name": p["name"], "item": f"{SITE}/places/{p['id']}/"}]}]
        desc = f'{p["name"]} travel guide: {first_sentence(p["intro"])} Best season, how to get there from Islamabad, Peshawar and Lahore, trip cost, live weather and what to pack.'
        page(f'/places/{p["id"]}/', f'{p["name"]} travel guide', desc[:300], body, active="/regions/", over=True,
             og=ph["src"] if ph else None, body_attr=f' data-place="{p["id"]}"', jsonld=ld)

def build_itins():
    body = hero('<img src="/img/hunza.jpg" alt="">', "Itineraries", "Routes that work", "سفر کے منصوبے", "Day-by-day plans with realistic drive times, from a weekend in the Galiyat to eight days across Hunza and Skardu.", short=True)
    body += f'<section class="block"><div class="wrap"><div class="grid">{"".join(itin_card(x) for x in ITINS)}</div></div></section>'
    page("/itineraries/", "Northern Pakistan itineraries", "Day-by-day itineraries for Swat, Naran, Hunza, Skardu, Neelum, Chitral and Murree, with drive times, best months and budgets.", body, active="/itineraries/", over=True)
    for x in ITINS:
        days = ""
        for i, (t, d, stops) in enumerate(x["plan"], 1):
            st = "".join(f'<a href="/places/{s}/">{e(BYID[s]["name"])}</a>' for s in dict.fromkeys(stops))
            days += f'<div class="day"><span class="n">Day {i}</span><div><h3>{e(t)}</h3><p>{e(d)}</p>{f"<div class=stops>{st}</div>" if st else ""}</div></div>'
        meta = f'<div class="itin-meta"><span>{x["days"]} days</span><span>From {x["from"]}</span><span>Best: {x["best"]}</span><span>{x["budget"]}</span></div>'
        body = hero(f'<img src="/img/{x["photo"]}.jpg" alt="">', "Itinerary · " + e(REGIONS[x["region"]]["name"]), e(x["title"]), lede=e(x["intro"]), crumbs='<a href="/">Home</a> › <a href="/itineraries/">Itineraries</a>', extra=meta, short=True)
        body += f'''<div class="wrap"><div class="layout"><div class="prose"><h2>Day by day</h2>{days}<div class="alert">Drive times are for good weather. In the north, keep a spare day for landslides, snow or cancelled flights.</div></div>
<aside><div class="sticky"><div class="card-box"><h3>Budget</h3><p style="margin:0">{x["budget"]} for a budget trip by coach and simple hotels. Use the <a href="/plan/?place={next((s for _, _, ss in x["plan"] for s in ss), "hunza")}">trip cost planner</a> for your own group.</p></div>
<div class="card-box"><h3>Before you go</h3><p style="margin:0 0 8px">Pack for the highest point on the route and save the <a href="/essentials/">offline essentials</a>.</p></div></div></aside></div></div>'''
        page(f"/itineraries/{x['id']}/", x["title"], x["intro"], body, active="/itineraries/", over=True, og=f"/img/{x['photo']}.jpg")

def build_plan():
    body = hero('<img src="/img/kaghan.jpg" alt="">', "Plan a trip", "What will my trip cost?", "سفر کا خرچ", "Pick a destination and your group. We estimate transport, hotel, food and jeep costs from Islamabad, Peshawar or Lahore, plus a packing list for the month you travel.", short=True)
    body += f'''<div class="wrap"><div class="layout"><div class="prose">
<div class="card-box"><div class="controls" style="max-width:420px"><label for="plan-place">Destination<select id="plan-place"></select></label></div><a id="plan-link" href="/regions/">Read the guide →</a></div>
<h2>Cost estimate</h2><div class="card-box" id="calc"></div><h2>What to pack</h2><div class="card-box" id="packs"></div></div>
<aside><div class="sticky"><div class="card-box"><h3>How we estimate</h3><dl class="kv"><dt>Petrol</dt><dd>Rs {COSTS["petrol"]}/litre</dd><dt>Car</dt><dd>{COSTS["kmPerLitre"]} km/litre</dd><dt>Coach</dt><dd>≈ Rs {COSTS["coachPerKm"]}/km</dd><dt>Hotel</dt><dd>Rs {fmt(COSTS["hotel"]["budget"])} / {fmt(COSTS["hotel"]["mid"])} / {fmt(COSTS["hotel"]["luxury"])} per room night</dd><dt>Food</dt><dd>Rs {fmt(COSTS["food"]["budget"])} / {fmt(COSTS["food"]["mid"])} / {fmt(COSTS["food"]["luxury"])} per person per day</dd></dl><p class="note">Rates as of {e(COSTS["updated"])}. Prices change with fuel rates, season and demand.</p></div></div></aside></div></div>'''
    page("/plan/", "Trip cost planner for Northern Pakistan", "Estimate the cost of a trip to Hunza, Skardu, Swat, Naran and 40 more places from Islamabad, Peshawar or Lahore, with a month-by-month packing list.", body, active="/plan/", over=True)

def build_essentials():
    E = ESS
    extra = [("Permits & checkposts", ["Carry your CNIC at all times; checkposts are common on the KKH and near the Line of Control.", "Foreign visitors should carry their passport and visa; some areas near borders need a No Objection Certificate (NOC). Check with a registered tour operator.", "Trekking to K2 base camp and some restricted peaks needs permits and a licensed operator."]),
             ("Respect & etiquette", ["Dress modestly, especially in villages.", "Ask before photographing people, and never photograph women without permission.", "Do not photograph military or security posts.", "Leave sacred places, graves and Kalash shrines undisturbed."]),
             ("Travel responsibly", ["Carry your rubbish back; many valleys have no waste collection.", "Use local guides, jeeps and guesthouses so money stays in the valley.", "Do not swim in glacier rivers: they are fast and freezing.", "Never feed or approach wildlife, especially bears in Deosai."])]
    sec = "".join(f'<h2>{t}</h2><ul>{"".join(f"<li>{e(i)}</li>" for i in L)}</ul>' for t, L in extra)
    body = hero('<img src="/img/kaghan.jpg" alt="">', "Works offline", "Offline essentials", "ضروری معلومات", "Emergency numbers, altitude sickness, mountain driving and more. Saved on your phone once you open it.", short=True)
    body += f'''<div class="wrap"><div class="layout"><div class="prose">
<h2>Emergency numbers</h2><div class="table"><table><thead><tr><th>Service</th><th style="text-align:right">Number</th></tr></thead><tbody>{"".join(f'<tr><td>{e(a)}</td><td class="num">{e(b)}</td></tr>' for a, b in E["numbers"])}</tbody></table></div>
<h2>Altitude sickness</h2><ul>{"".join(f"<li>{e(t)}</li>" for t in E["altitude"])}</ul>
<h2>Mountain driving</h2><ul>{"".join(f"<li>{e(t)}</li>" for t in E["road"])}</ul>
<h2>Packing list</h2><ul>{"".join(f"<li>{e(t)}</li>" for t in E["packing"])}</ul>
<h2>Which mobile network works</h2><div class="table"><table><thead><tr><th>Area</th><th>Usually works</th></tr></thead><tbody>{"".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in E["network"])}</tbody></table></div>
{sec}</div>
<aside><div class="sticky"><div class="card-box"><h3>Save for offline</h3><p style="margin:0 0 10px">On Android, open the Chrome menu and choose <b>Add to Home screen</b>. On iPhone, use Safari's share button and <b>Add to Home Screen</b>.</p><p class="note" id="offline-state"></p></div></div></aside></div></div>'''
    page("/essentials/", "Offline travel essentials for Northern Pakistan", "Emergency numbers, altitude sickness advice, mountain driving tips, permits, etiquette and mobile network coverage for Northern Pakistan.", body, active="/essentials/", over=True)

def build_about():
    body = hero('<img src="/img/passu-khunjerab.jpg" alt="">', "About", "The jewel of the mountains", "کوہِ نور", "Why KohNoor exists, and how we put the guide together.", short=True)
    body += f'''<div class="wrap"><div class="layout"><div class="prose">
<h2>Why KohNoor</h2><p class="lead">Koh means mountain and Noor means light. KohNoor is a free guide to the mountains of Northern Pakistan, built so that anyone can plan a trip with confidence: where to go, when, how to get there, what it costs and what to pack.</p>
<p>We cover {len(PLACES)} destinations across {len(REGIONS)} regions, from the hill stations near Islamabad to the Khunjerab Pass on the China border, with famous names first and quieter hidden places marked as such.</p>
<h2>How we work</h2><ul><li><b>Weather</b> is live from Open-Meteo and saved on your phone for offline use.</li><li><b>Costs</b> are estimates built from fuel prices, coach fares and typical hotel rates as of {e(COSTS["updated"])}. They change with season and demand.</li><li><b>Altitudes, distances and drive times</b> are approximate. Mountain roads change with weather, so always check before you travel.</li><li><b>Hidden places</b> have less verified information. Travel there with a local guide.</li><li><b>Photos</b> are real photos of each place, used under free licences. Places without a suitable photo show a KohNoor illustration instead of a photo of somewhere else.</li></ul>
<h2>Coming next</h2><ul><li>Urdu version of every page</li><li>Live road reports from travellers</li><li>More hidden places, valley by valley</li></ul></div>
<aside><div class="sticky"><div class="card-box"><h3>KohNoor in numbers</h3><dl class="kv"><dt>Destinations</dt><dd>{len(PLACES)}</dd><dt>Regions</dt><dd>{len(REGIONS)}</dd><dt>Itineraries</dt><dd>{len(ITINS)}</dd><dt>With real photos</dt><dd>{sum(1 for p in PLACES if p["id"] in PHOTOS)}</dd></dl></div></div></aside></div></div>'''
    page("/about/", "About KohNoor", "KohNoor is a free, honest travel guide to Northern Pakistan: how the guide works, where the data comes from and what is coming next.", body, active="/about/", over=True)

# ---------------- interests, calendar, gallery, FAQ ----------------
THEMES = [
 {"slug": "lakes", "name": "Lakes", "icon": "drop", "photo": "mahodand", "title": "Best lakes in Northern Pakistan",
  "lede": "Turquoise glacier lakes, forest-ringed pools and high-altitude mirrors, from roadside Attabad to Katora at 3,500 m.",
  "ids": ["naran", "attabad", "mahodand", "kachura", "phander", "kandol-lake", "daral-lake", "katora-lake", "borith", "khalti", "dudipatsar", "ratti-gali", "rawalakot", "astore-rama", "utror-gabral", "shandur"]},
 {"slug": "meadows-and-valleys", "name": "Meadows & valleys", "icon": "tree", "photo": "kumrat", "title": "Green meadows and valleys of the north",
  "lede": "Pine forests, flower meadows and wooden villages: the softer, greener side of the mountains.",
  "ids": ["fairy-meadows", "kumrat", "jahaz-banda", "arang-kel", "shogran", "naltar", "kalam", "ushu-matiltan", "gabin-jabba", "neelum", "leepa", "taobat", "deosai", "marghazar"]},
 {"slug": "treks-and-hikes", "name": "Treks & hikes", "icon": "route", "photo": "fairy-meadows", "title": "Treks and day hikes in Northern Pakistan",
  "lede": "From the flat Pipeline Track in Galiyat to the walk up to Fairy Meadows under Nanga Parbat.",
  "ids": ["fairy-meadows", "nathia-gali", "miranjani", "arang-kel", "jahaz-banda", "katora-lake", "kandol-lake", "daral-lake", "dudipatsar", "ratti-gali", "passu-khunjerab"]},
 {"slug": "history-and-culture", "name": "History & culture", "icon": "landmark", "photo": "butkara", "title": "History and culture in Northern Pakistan",
  "lede": "Gandhara stupas in Swat, the forts of Hunza and Baltistan, rock carvings on the Indus and the living Kalash culture.",
  "ids": ["swat-museum", "butkara", "udegram", "jahanabad-buddha", "mingora", "marghazar", "hunza", "shigar", "khaplu", "skardu", "chitral", "kalash", "chilas", "sharda", "gilgit"]},
 {"slug": "family-trips", "name": "Easy family trips", "icon": "family", "photo": "murree", "title": "Easy family trips in the northern hills",
  "lede": "Good roads, plenty of hotels and short drives: places that work with children and grandparents.",
  "ids": ["murree", "nathia-gali", "malam-jabba", "mingora", "madyan", "bahrain", "kalam", "kaghan", "naran", "shogran", "rawalakot", "muzaffarabad", "neelum", "attabad", "hunza", "skardu"]},
 {"slug": "snow-and-winter", "name": "Snow & winter", "icon": "snow", "photo": "naltar", "title": "Snow and winter trips in Pakistan",
  "lede": "Skiing at Malam Jabba and Naltar, snowy Galiyat weekends and frozen lakes in Ghizer.",
  "ids": ["malam-jabba", "murree", "nathia-gali", "miranjani", "naltar", "kalam", "hunza", "skardu", "khalti"]},
 {"slug": "jeep-adventures", "name": "Jeep adventures", "icon": "car", "photo": "deosai", "title": "Jeep adventures in the north",
  "lede": "Rough tracks to high plains and hidden lakes, best done with a local driver.",
  "ids": ["deosai", "mahodand", "kumrat", "shandur", "naltar", "fairy-meadows", "ratti-gali", "taobat", "leepa", "sarfaranga", "utror-gabral", "gabin-jabba", "astore-rama", "kandol-lake"]},
 {"slug": "hidden-gems", "name": "Hidden gems", "icon": "pin", "photo": "katora-lake", "title": "Hidden places in Northern Pakistan",
  "lede": "Quiet lakes, meadows and valleys with far fewer visitors. Information is thinner, so travel with a local guide.", "ids": None},
]
for t in THEMES:
    if t["ids"] is None: t["ids"] = [p["id"] for p in PLACES if p["kind"] == "hidden"]
    t["ids"] = [i for i in t["ids"] if i in BYID]
THEMES_OF = {}
for t in THEMES:
    for i in t["ids"]: THEMES_OF.setdefault(i, []).append(t)

FAQ = [
 ("When is the best time to visit Northern Pakistan?", "May to October for most places. June to September is the only window for high passes and lakes such as Babusar Top, Deosai, Fairy Meadows and the jeep lakes above Kalam. Hunza and Skardu are lovely in April for blossom and in late October for autumn colours. Murree, Nathia Gali and Malam Jabba get snow from December to February."),
 ("How much does a trip to the north cost?", "A budget road trip costs roughly Rs 15,000 to 25,000 per person for a long weekend in Swat, Naran or Neelum, and Rs 60,000 or more for a week in Hunza and Skardu. Use the trip cost planner for an estimate from Islamabad, Peshawar or Lahore for your group size and hotel level."),
 ("Is it safe to travel to Gilgit-Baltistan and Swat?", "The main tourist routes see large numbers of domestic and foreign visitors every summer. The biggest real risks are road conditions, landslides after rain and altitude. Check road status before you set out, carry your CNIC or passport for checkposts, and follow local advice near the Line of Control."),
 ("Do I need a 4x4 to visit the north?", "No for the main towns: an ordinary car reaches Mingora, Kalam, Naran, Gilgit, Hunza, Skardu, Chitral and Neelum. Local jeeps are needed for places like Fairy Meadows, Deosai, Mahodand, Kumrat and Ratti Gali, and you can hire them on the spot."),
 ("Which mobile network works best in the mountains?", "SCOM and Zong usually have the widest coverage in Gilgit-Baltistan and Azad Kashmir; Jazz and Telenor work in most towns. Expect no signal in high valleys, so save pages offline before you go."),
 ("Can I use KohNoor without internet?", "Yes. Install it from your browser menu and open your destinations once while you have signal. Pages you opened, your packing list and the emergency numbers then keep working offline."),
]

def faq_html(items):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in items) + '</div>'
def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def theme_card(t):
    return f'<a class="interest" href="/interests/{t["slug"]}/"><img src="/img/{t["photo"]}-s.jpg" alt="" loading="lazy"><span class="ico">{icon(t["icon"])}</span><div class="t"><h3>{e(t["name"])}</h3><small>{len(t["ids"])} places</small></div></a>'

def build_interests():
    body = hero('<img src="/img/fairy-meadows.jpg" alt="Nanga Parbat at sunrise">', "Interests", "Travel the north your way", "دلچسپی کے مطابق",
                "Lakes, meadows, treks, history, family trips, snow and jeep tracks: pick what you love and see every place that fits.", short=True, credit="Sunrise on Nanga Parbat")
    body += f'<section class="block"><div class="wrap"><div class="interests">{"".join(theme_card(t) for t in THEMES)}</div></div></section>'
    page("/interests/", "Things to do in Northern Pakistan by interest", "Browse Northern Pakistan by interest: lakes, meadows, treks and hikes, history and culture, family trips, snow and winter, jeep adventures and hidden places.", body, active="/interests/", over=True)
    for t in THEMES:
        ps = [BYID[i] for i in t["ids"]]
        others = "".join(f'<a class="chip" href="/interests/{o["slug"]}/">{e(o["name"])}</a>' for o in THEMES if o is not t)
        body = hero(f'<img src="/img/{t["photo"]}.jpg" alt="">', "Interests", e(t["title"]), lede=e(t["lede"]), crumbs='<a href="/">Home</a> › <a href="/interests/">Interests</a>', short=True, credit=PHOTOS.get(t["photo"], {}).get("credit", ""))
        body += f'''<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">{len(ps)} places</span><h2>{e(t["name"])}</h2></div></div><div class="grid">{"".join(card(p) for p in ps)}</div>
<div class="chips light" style="margin-top:34px"><span class="lbl">More interests:</span>{others}</div></div></section>'''
        ld = {"@context": "https://schema.org", "@type": "ItemList", "name": t["title"], "itemListElement": [{"@type": "ListItem", "position": n + 1, "url": f"{SITE}/places/{p['id']}/", "name": p["name"]} for n, p in enumerate(ps)]}
        page(f'/interests/{t["slug"]}/', t["title"], f'{t["title"]}: {t["lede"]} With best season, travel time, cost and live weather for each place.'[:300], body, active="/interests/", over=True, jsonld=ld)

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
def build_when():
    rows = []
    for k in REGION_ORDER:
        rows.append(f'<tr class="rg"><th colspan="13">{e(REGIONS[k]["name"])}</th></tr>')
        for p in [x for x in PLACES if x["region"] == k]:
            rows.append(f'<tr><th><a href="/places/{p["id"]}/">{e(p["name"])}</a></th>' + "".join(f'<td class="m{v}" title="{MONTHS[i]}: {["closed or not advised","possible","best"][int(v)]}"></td>' for i, v in enumerate(p["months"])) + '</tr>')
    seasons = [("Spring", "Mar–Apr", "Blossom in Hunza, Skardu and Swat. Upper valleys still under snow.", "hunza"),
               ("Summer", "Jun–Sep", "Everything opens: Babusar, Deosai, Fairy Meadows and the jeep lakes. Busy on weekends.", "naran"),
               ("Autumn", "Oct–Nov", "Golden poplars in Hunza, Ghizer and Skardu. Clear skies, cold nights.", "phander"),
               ("Winter", "Dec–Feb", "Snow in Murree, Galiyat and Malam Jabba. Most high places closed.", "malam-jabba")]
    sea = "".join(f'<a class="season" href="/places/{ph}/"><img src="/img/{ph}-s.jpg" alt="" loading="lazy"><div class="t"><small>{b}</small><h3>{a}</h3><p>{c}</p></div></a>' for a, b, c, ph in seasons)
    body = hero('<img src="/img/phander.jpg" alt="Phander Lake in autumn">', "Best time to visit", "When to go, month by month", "کب جائیں",
                "Every destination on one calendar: green is the best time, amber is possible, grey means snow or weather usually closes it.", short=True, credit="Phander Lake in autumn")
    body += f'''<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">Four seasons</span><h2>The year in the mountains</h2></div></div><div class="seasons">{sea}</div></div></section>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">Calendar</span><h2>All {len(PLACES)} places by month</h2><p>This month is highlighted. Tap a place for weather, costs and how to get there.</p></div></div>
<div class="legend big"><span><i class="m2"></i>Best</span><span><i class="m1"></i>Possible</span><span><i class="m0"></i>Closed or not advised</span></div>
<div class="cal-wrap"><table class="cal"><thead><tr><th>Place</th>{"".join(f"<th data-m='{i}'>{m}</th>" for i, m in enumerate(MONTHS))}</tr></thead><tbody>{"".join(rows)}</tbody></table></div></div></section>'''
    page("/when-to-go/", "Best time to visit Northern Pakistan, month by month", "Month-by-month calendar for 57 places in Northern Pakistan: when Hunza, Skardu, Swat, Naran, Neelum, Fairy Meadows and Deosai are open and at their best.", body, active="/when-to-go/", over=True)

def build_gallery():
    items = "".join(f'<a class="g-item" href="/places/{p["id"]}/"><img src="/img/{p["id"]}-s.jpg" alt="{e(p["name"])}" loading="lazy"><span><b>{e(p["name"])}</b><small>{e(PHOTOS[p["id"]]["credit"])}</small></span></a>' for p in PLACES if p["id"] in PHOTOS)
    body = hero('<img src="/img/passu-khunjerab.jpg" alt="Passu Cones">', "Gallery", "The north in pictures", "تصویریں", "A photo of every destination in the guide. Tap any picture to open its travel guide.", short=True, credit="Passu Cones")
    body += f'<section class="block tight"><div class="wrap"><div class="gallery">{items}</div><p class="note" style="margin-top:24px">Photos are used under free licences. Wikimedia Commons photos are credited to their authors under the licence shown (CC BY-SA or public domain).</p></div></section>'
    page("/gallery/", "Photo gallery of Northern Pakistan", "Photos of every destination in Northern Pakistan: Hunza, Skardu, Swat, Naran, Neelum, Chitral, Fairy Meadows, Deosai and hidden lakes and meadows.", body, over=True)

def nearest(p, n=4):
    from math import radians, sin, cos, asin, sqrt
    def dist(a, b):
        la1, lo1, la2, lo2 = map(radians, (a["lat"], a["lon"], b["lat"], b["lon"]))
        return 6371 * 2 * asin(sqrt(sin((la2 - la1) / 2) ** 2 + cos(la1) * cos(la2) * sin((lo2 - lo1) / 2) ** 2))
    return sorted([(dist(p, x), x) for x in PLACES if x["id"] != p["id"]], key=lambda t: t[0])[:n]

# ---------------- Urdu version ----------------
URP = {}
for f in sorted(os.listdir(os.path.join(SRC, "ur"))):
    if f.startswith("places"): URP.update(json.load(open(os.path.join(SRC, "ur", f))))
URS = json.load(open(os.path.join(SRC, "ur", "site.json")))
UR_PATHS = {"/map/", "/regions/", "/interests/", "/when-to-go/", "/essentials/", "/list-your-business/"} | {f"/regions/{k}/" for k in REGION_ORDER} | {f"/places/{p['id']}/" for p in PLACES if p["id"] in URP} | {f"/interests/{t['slug']}/" for t in THEMES}
UMON = ["جنوری","فروری","مارچ","اپریل","مئی","جون","جولائی","اگست","ستمبر","اکتوبر","نومبر","دسمبر"]
def urfirst(t): return t.split("۔")[0].strip() + "۔"
NAV_UR = [("/ur/regions/", "منزلیں"), ("/ur/interests/", "دلچسپیاں"), ("/ur/when-to-go/", "کب جائیں"), ("/ur/map/", "نقشہ"), ("/ur/essentials/", "ضروری معلومات"), ("/ur/list-your-business/", "اپنا کاروبار شامل کریں")]
def header_ur(active, over, enp="/"):
    links = "".join(f'<a href="{u}"{" aria-current=page" if active == u else ""}>{t}</a>' for u, t in NAV_UR)
    return f'''<header class="site-head{' over' if over else ''}"><div class="wrap head-in">
<a class="brand" href="/ur/" aria-label="کوہِ نور ہوم">{gem()}<b class="ur-brand">کوہِ نور</b></a>
<nav class="nav" aria-label="مینو">{links}</nav>
<a class="lang-sw" href="{enp}" lang="en" hreflang="en">English</a>
<button class="icon-btn" data-open-search aria-label="تلاش">{icon("search")}</button>
<button class="icon-btn menu-btn" aria-label="مینو" aria-expanded="false">{icon("menu")}</button>
</div></header>
<div class="search-ov" role="dialog" aria-label="تلاش"><div class="search-box"><label for="search-input" class="sr">جگہ تلاش کریں</label>
<input id="search-input" type="search" placeholder="وادی، جھیل یا شہر تلاش کریں…" autocomplete="off"><div class="search-res"></div></div></div>'''
def footer_ur():
    regs = "".join(f'<a href="/ur/regions/{k}/">{e(REGIONS[k]["ur"])}</a>' for k in REGION_ORDER)
    top = "".join(f'<a href="/ur/places/{i}/">{e(BYID[i]["ur"])}</a>' for i in ["hunza", "skardu", "kalam", "naran", "fairy-meadows", "neelum"])
    return f'''<footer class="site-foot">{topo(3)}<div class="wrap"><div class="foot-grid">
<div><a class="brand" href="/ur/">{gem()}<b class="ur-brand">کوہِ نور</b></a><p>پہاڑوں کا ہیرا: شمالی پاکستان کا مکمل اور دیانتدار رہنما۔ جگہیں، تاریخ، لائیو موسم، سفر کا خرچ اور آف لائن معلومات۔</p></div>
<div><h4>علاقے</h4>{regs}</div><div><h4>مشہور جگہیں</h4>{top}</div>
<div><h4>منصوبہ</h4><a href="/ur/interests/">دلچسپی کے مطابق سفر</a><a href="/ur/when-to-go/">کب جائیں</a><a href="/ur/essentials/">ضروری معلومات</a><a href="/ur/list-your-business/">اپنا کاروبار شامل کریں</a><a href="/">English</a></div>
</div><div class="foot-bottom"><span>© {date.today().year} کوہِ نور۔ خرچ اور سفر کا وقت اندازاً ہیں؛ سفر سے پہلے سڑک کی صورتحال معلوم کریں۔</span><span>موسم: Open-Meteo · تصاویر آزاد لائسنس کے تحت</span></div></div></footer>
<div class="net" role="status">آپ آف لائن ہیں · محفوظ صفحات چلتے رہیں گے</div>'''

def card_ur(p, near_km=None):
    u = URP.get(p["id"], {})
    hid = ('<span class="badge hidden">چھپی جگہ</span>' if p["kind"] == "hidden" else "") + (f'<span class="badge">تقریباً {near_km:.0f} کلومیٹر</span>' if near_km is not None else "")
    return f'''<a class="card" href="/ur/places/{p["id"]}/" data-months="{p["months"]}"><div class="pic">{pic(p)}<div class="badges">{hid}</div></div>
<div class="body"><span class="region">{e(REGIONS[p["region"]]["ur"])}</span><h3>{e(p["ur"])}</h3><p>{e(urfirst(u.get("intro", "")))}</p>
<div class="meta"><span>{icon("mountain")}{fmt(p["alt"])} میٹر</span><span>{icon("clock")}{e(p["hrs"])} گھنٹے</span><span class="price" data-price="{p["id"]}"></span></div></div></a>'''

def build_urdu():
    tiles = []
    for i, k in enumerate(REGION_ORDER):
        n = sum(1 for p in PLACES if p["region"] == k); cls = "big" if i == 0 else ("wide" if i in (3, 6) else "")
        tiles.append(f'<a class="tile {cls}" href="/ur/regions/{k}/"><img src="/img/{REGION_PHOTO[k]}{"" if i in (0, 3, 6) else "-s"}.jpg" alt="" loading="lazy"><div class="t"><h3>{e(REGIONS[k]["ur"])}</h3><span>{n} منزلیں</span></div></a>')
    feat = ["hunza", "skardu", "kalam", "naran", "fairy-meadows", "attabad", "neelum", "kumrat"]
    hidden = [p for p in PLACES if p["kind"] == "hidden"]
    th = URS["themes"]
    icards = "".join(f'<a class="interest" href="/ur/interests/{t["slug"]}/"><img src="/img/{t["photo"]}-s.jpg" alt="" loading="lazy"><span class="ico">{icon(t["icon"])}</span><div class="t"><h3>{e(th[t["slug"]][0])}</h3><small>{len(t["ids"])} جگہیں</small></div></a>' for t in THEMES)
    faq = URS["faq"]
    body = hero('<img src="/img/home.jpg" alt="خزاں میں وادیٔ ہنزہ" fetchpriority="high">', "شمالی پاکستان کا سفری رہنما", "ہر وادی، ہر راستہ، ایک رہنما۔", "",
                "ہنزہ کے قلعوں سے سوات کی جھیلوں تک: جگہیں اور ان کی تاریخ، لائیو موسم، اسلام آباد، پشاور اور لاہور سے سفر کا اصل خرچ، اور سگنل ختم ہونے کی جگہوں کے لیے آف لائن معلومات۔",
                extra=f'''<div class="hero-search"><button data-open-search>{icon("search")}کہاں جانا چاہتے ہیں؟</button></div>
<div class="chips">{"".join(f'<a class="chip" href="/ur/interests/{t["slug"]}/">{icon(t["icon"])}{e(th[t["slug"]][0])}</a>' for t in THEMES[:6])}</div>''', credit="خزاں میں وادیٔ ہنزہ")
    body += f'''<div class="strip"><div class="wrap"><div><b>{len(PLACES)}</b><span>مشہور اور چھپی منزلیں</span></div><div><b>{len(REGIONS)}</b><span>علاقے، مری سے خنجراب تک</span></div><div><b>لائیو</b><span>ہر جگہ کا موسم</span></div><div><b>آف لائن</b><span>سگنل کے بغیر بھی چلتا ہے</span></div></div></div>
<section class="block"><div class="wrap"><div class="sec-head"><div><span class="kicker">اپنا سفر چنیں</span><h2>اپنی پسند کے مطابق شمال دیکھیں</h2><p>جو پسند ہو اس سے شروع کریں۔ ہر صفحے پر موزوں جگہیں، موسم، سفر کا وقت اور خرچ موجود ہے۔</p></div><a class="more" href="/ur/interests/">تمام دلچسپیاں ←</a></div><div class="interests">{icards}</div></div></section>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">کہاں جائیں</span><h2>سات علاقے، ایک شمال</h2></div><a class="more" href="/ur/regions/">تمام منزلیں ←</a></div><div class="mosaic">{"".join(tiles)}</div></div></section>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">نقشہ</span><h2>ہر جگہ، ایک نقشہ</h2><p>سنہری نشان مشہور جگہیں ہیں اور سبز نشان چھپی جگہیں۔ کسی بھی نشان پر ٹیپ کریں۔</p></div><a class="more" href="/ur/map/">پورا نقشہ ←</a></div>{map_box(lang="ur")}</div></section>
<section class="block dark alt-sec">{topo(4)}<div class="wrap" style="position:relative"><div class="sec-head"><div><span class="kicker">کتنی بلندی</span><h2>980 میٹر سے شاہراہِ قراقرم کی چھت تک</h2><p>ان جگہوں کی بلندی جہاں گاڑی یا پیدل پہنچا جا سکتا ہے۔ تقریباً 2,500 میٹر سے اوپر آہستہ چلیں اور خوب پانی پئیں۔</p></div></div>{alt_chart("ur")}</div></section>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">مشہور منزلیں</span><h2>شمال کے بڑے نام</h2></div></div><div class="grid">{"".join(card_ur(BYID[i]) for i in feat)}</div></div></section>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">موسم کے مطابق</span><h2>اس وقت بہترین: <span data-now-month></span></h2></div></div><div class="grid" id="best-now"></div></div></section>
<section class="block dark">{topo(11)}<div class="wrap" style="position:relative"><div class="sec-head"><div><span class="kicker">چھپی جگہیں</span><h2>مشہور ناموں سے آگے</h2><p>کم سیاحوں والی پُرسکون جھیلیں اور چراگاہیں۔ یہاں معلومات کم ہیں، اس لیے مقامی گائیڈ کے ساتھ سفر کریں۔</p></div></div><div class="grid">{"".join(card_ur(p) for p in hidden[:8])}</div><a class="btn" style="margin-top:30px" href="/ur/interests/hidden-gems/">تمام {len(hidden)} چھپی جگہیں دیکھیں ←</a></div></section>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">سوالات</span><h2>جانے سے پہلے</h2></div><a class="more" href="/ur/when-to-go/">موسم کا کیلنڈر ←</a></div>{faq_html(faq)}</div></section>'''
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": "کوہِ نور", "url": SITE + "/ur/", "inLanguage": "ur"}, faq_ld(faq)]
    page("/ur/", "کوہِ نور — شمالی پاکستان کا مکمل سفری رہنما", "ہنزہ، سکردو، سوات، ناران، نیلم، چترال اور مزید کے سفر کی منصوبہ بندی: جگہیں اور تاریخ، لائیو موسم، اسلام آباد، پشاور اور لاہور سے سفر کا خرچ اور آف لائن معلومات۔", body, over=True, jsonld=ld, lang="ur")

    # regions
    cards = "".join(f'''<a class="card" href="/ur/regions/{k}/"><div class="pic"><img src="/img/{REGION_PHOTO[k]}-s.jpg" alt="" loading="lazy"></div><div class="body"><h3>{e(REGIONS[k]["ur"])}</h3><p>{e(URS["regions"][k]["lede"])}</p><div class="meta"><span>{icon("pin")}{sum(1 for p in PLACES if p["region"] == k)} منزلیں</span></div></div></a>''' for k in REGION_ORDER)
    body = hero('<img src="/img/r-gb.jpg" alt="">', "منزلیں", "شمال میں کہاں جائیں", "", "سات علاقے، اسلام آباد کے قریب پہاڑی مقامات سے چین کی سرحد پر قراقرم تک۔", short=True)
    body += f'<section class="block"><div class="wrap"><div class="grid">{cards}</div></div></section><section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">تمام</span><h2>تمام {len(PLACES)} منزلیں</h2></div></div><div class="grid">{"".join(card_ur(p) for p in sorted(PLACES, key=lambda p: (p["kind"] != "famous")))}</div></div></section>'
    page("/ur/regions/", "شمالی پاکستان کی منزلیں", "شمالی پاکستان کے تمام علاقے اور منزلیں: گلگت بلتستان، سوات، کاغان، آزاد کشمیر، چترال، دیر اور گلیات۔", body, active="/ur/regions/", over=True, lang="ur")
    for k in REGION_ORDER:
        r = REGIONS[k]; ru = URS["regions"][k]; ps = sorted([p for p in PLACES if p["region"] == k], key=lambda p: p["kind"] != "famous")
        facts = "".join(f"<dt>{e(a)}</dt><dd>{e(b)}</dd>" for a, b in ru["facts"])
        body = hero(f'<img src="/img/{REGION_PHOTO[k]}.jpg" alt="">', "علاقہ", e(r["ur"]), "", e(ru["lede"]), crumbs='<a href="/ur/">ہوم</a> › <a href="/ur/regions/">منزلیں</a>', short=True)
        body += f'''<div class="wrap"><div class="layout"><div class="prose"><h2>علاقے کا تعارف</h2>{"".join(f"<p>{e(t)}</p>" for t in ru["about"])}<h2>مختصر تاریخ</h2>{"".join(f"<p>{e(t)}</p>" for t in ru["history"])}</div>
<aside><div class="card-box"><h3>اہم معلومات</h3><dl class="kv">{facts}</dl></div></aside></div></div>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">نقشہ</span><h2>{e(r["ur"])} نقشے پر</h2></div></div>{map_box(region=k, lang="ur")}</div></section>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">{len(ps)} منزلیں</span><h2>{e(r["ur"])} کی جگہیں</h2></div></div><div class="grid">{"".join(card_ur(p) for p in ps)}</div></div></section>'''
        page(f"/ur/regions/{k}/", f'{r["ur"]} سفری رہنما', ru["lede"][:300], body, active="/ur/regions/", over=True, lang="ur")

    # places
    for p in PLACES:
        u = URP.get(p["id"])
        if not u: continue
        r = REGIONS[p["region"]]; ph = PHOTOS.get(p["id"])
        months = "".join(f'<span class="m{v}" title="{m}">{m}</span>' for v, m in zip(p["months"], UMON))
        bbox = f'{p["lon"]-0.08:.3f}%2C{p["lat"]-0.05:.3f}%2C{p["lon"]+0.08:.3f}%2C{p["lat"]+0.05:.3f}'
        d = COSTS["delta"][p["route"]]
        rows = [("اسلام آباد", p["km"]), ("پشاور", max(30, p["km"] + d["psh"])), ("لاہور", max(30, p["km"] + d["lhr"]))]
        dist = "".join(f'<tr><td>{a}</td><td class="num">تقریباً {fmt(b)} کلومیٹر</td></tr>' for a, b in rows)
        tags = "".join(f'<a class="chip" href="/ur/interests/{t["slug"]}/">{icon(t["icon"])}{e(URS["themes"][t["slug"]][0])}</a>' for t in THEMES_OF.get(p["id"], []))
        hidden_alert = '<div class="alert"><b>کم تصدیق شدہ جگہ۔</b> یہاں کی معلومات مشہور جگہوں سے کم ہیں۔ مقامی گائیڈ کے ساتھ جائیں اور قریبی قصبے میں راستے کا پوچھ لیں۔</div>' if p["kind"] == "hidden" else ""
        near = nearest(p, 4)
        body = hero(pic(p, True), ("چھپی جگہ · " if p["kind"] == "hidden" else "") + e(r["ur"]), e(p["ur"]), "", e(u["intro"]),
                    crumbs=f'<a href="/ur/">ہوم</a> › <a href="/ur/regions/{p["region"]}/">{e(r["ur"])}</a>', credit=(ph or {}).get("credit", ""))
        body += f'''<nav class="subnav" aria-label="اس صفحے پر"><div class="wrap"><a href="#overview">تعارف</a><a href="#todo">کیا کریں</a><a href="#history">تاریخ</a><a href="#getting-there">کیسے پہنچیں</a><a href="#costs">خرچ</a><a href="#packing">کیا ساتھ لے جائیں</a><a href="#stay">رہائش اور کھانا</a><a href="#map">نقشہ</a></div></nav>
<div class="wrap"><div class="glance">
<div>{icon("mountain")}<span><small>بلندی</small><b>تقریباً {fmt(p["alt"])} میٹر</b></span></div>
<div>{icon("clock")}<span><small>اسلام آباد سے</small><b>{e(p["hrs"])} گھنٹے</b></span></div>
<div>{icon("wallet")}<span><small>کم خرچ سفر</small><b data-price="{p["id"]}">—</b></span></div>
<div>{icon("signal")}<span><small>موبائل سگنل</small><b>{e(u["network"])}</b></span></div>
</div>
<div class="layout"><div class="prose">
<h2 id="overview">تعارف</h2><p class="lead">{e(u["intro"])}</p>{f'<div class="chips light tags">{tags}</div>' if tags else ''}
<div id="closed-now" class="alert closed" hidden><b><span data-now-month></span>: عموماً بند یا جانا مناسب نہیں۔</b> اس موسم میں برف یا خراب موسم عموماً راستہ بند رکھتا ہے۔ بہترین موسم: {e(u["season"])}۔</div>{hidden_alert}
<div class="card-box"><h3>کب جائیں</h3><div class="months">{months}</div><div class="legend"><span><i class="m2"></i>بہترین</span><span><i class="m1"></i>ممکن</span><span><i class="m0"></i>بند یا مناسب نہیں</span></div></div>
<h2 id="todo">کیا کریں</h2><ol class="top">{"".join(f"<li>{e(t)}</li>" for t in u["todo"])}</ol>
<h2 id="history">تاریخ</h2><p>{e(u["history"])}</p>
<h2 id="getting-there">کیسے پہنچیں</h2><p>{e(u["reach"])}</p>
<div class="table"><table><thead><tr><th>کہاں سے</th><th>فاصلہ</th></tr></thead><tbody>{dist}</tbody></table></div>
<h2 id="costs">سفر کا خرچ</h2><div class="card-box" id="calc"><p class="note">خرچ کا کیلکولیٹر لوڈ ہو رہا ہے…</p></div>
<h2 id="packing">کیا ساتھ لے جائیں</h2><div class="card-box" id="packs"></div>
<h2 id="stay">رہائش اور کھانا</h2><p><b>رہائش:</b> {e(u["stay"])}</p><p><b>کھانا:</b> {e(u["food"])}</p>
<h2>اہم مشورے</h2><ul>{"".join(f"<li>{e(t)}</li>" for t in u["tips"])}</ul>
<h2 id="map">نقشہ</h2><iframe class="map" loading="lazy" title="{e(p["ur"])} کا نقشہ" src="https://www.openstreetmap.org/export/embed.html?bbox={bbox}&amp;layer=mapnik&amp;marker={p["lat"]}%2C{p["lon"]}"></iframe>
<p class="note">مقام اندازاً ہے۔ <a href="https://www.google.com/maps/search/?api=1&amp;query={p["lat"]},{p["lon"]}" rel="noopener">گوگل میپس میں کھولیں</a></p>
</div>
<aside><div class="sticky"><div class="card-box" id="wx"><h3>موسم ابھی</h3><p class="note">لائیو موسم لوڈ ہو رہا ہے…</p></div>
<div class="card-box"><h3>اہم معلومات</h3><dl class="kv"><dt>بہترین موسم</dt><dd>{e(u["season"])}</dd><dt>گاڑی</dt><dd>{e(u["vehicle"])}</dd><dt>پیٹرول اور نقد</dt><dd>{e(u["fuel"])}</dd><dt>سگنل</dt><dd>{e(u["network"])}</dd></dl></div>
<div class="card-box"><h3>سڑک کی صورتحال</h3><p style="margin:0;font-size:15.5px">شمال کی سڑکیں موسم کے ساتھ بدلتی ہیں۔ نکلنے سے پہلے مقامی پولیس یا اپنے ہوٹل سے پوچھیں، خاص طور پر بارش یا برف کے بعد۔</p></div></div></aside>
</div></div>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">قریبی جگہیں</span><h2>{e(p["ur"])} کے قریب ترین مقامات</h2><p>سیدھا فاصلہ؛ پہاڑوں میں سڑک کا فاصلہ زیادہ ہوتا ہے۔</p></div></div><div class="grid g4">{"".join(card_ur(x, near_km=dk) for dk, x in near)}</div></div></section>'''
        ld = {"@context": "https://schema.org", "@type": "TouristAttraction", "name": p["ur"], "alternateName": p["name"], "description": u["intro"], "url": f"{SITE}/ur/places/{p['id']}/", "inLanguage": "ur",
              "image": SITE + (ph["src"] if ph else "/assets/og-default.jpg"), "geo": {"@type": "GeoCoordinates", "latitude": p["lat"], "longitude": p["lon"]}}
        page(f'/ur/places/{p["id"]}/', f'{p["ur"]} سفری رہنما', f'{p["ur"]}: {urfirst(u["intro"])} بہترین موسم، اسلام آباد، پشاور اور لاہور سے راستہ، سفر کا خرچ، لائیو موسم اور سامان کی فہرست۔'[:300], body,
             active="/ur/regions/", over=True, og=ph["src"] if ph else None, body_attr=f' data-place="{p["id"]}"', jsonld=ld, lang="ur")

    # interests
    body = hero('<img src="/img/fairy-meadows.jpg" alt="">', "دلچسپیاں", "اپنی پسند کا شمال", "", "جھیلیں، چراگاہیں، ٹریک، تاریخ، خاندانی سفر، برف اور جیپ کے راستے: جو پسند ہو چنیں اور موزوں تمام جگہیں دیکھیں۔", short=True)
    body += f'<section class="block"><div class="wrap"><div class="interests">{icards}</div></div></section>'
    page("/ur/interests/", "دلچسپی کے مطابق شمالی پاکستان", "جھیلیں، چراگاہیں، ٹریک، تاریخ و ثقافت، خاندانی سفر، برف، جیپ ایڈونچر اور چھپی جگہیں۔", body, active="/ur/interests/", over=True, lang="ur")
    for t in THEMES:
        nm, title, lede = th[t["slug"]]
        others = "".join(f'<a class="chip" href="/ur/interests/{o["slug"]}/">{e(th[o["slug"]][0])}</a>' for o in THEMES if o is not t)
        body = hero(f'<img src="/img/{t["photo"]}.jpg" alt="">', "دلچسپیاں", e(title), lede=e(lede), crumbs='<a href="/ur/">ہوم</a> › <a href="/ur/interests/">دلچسپیاں</a>', short=True)
        body += f'<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">{len(t["ids"])} جگہیں</span><h2>{e(nm)}</h2></div></div><div class="grid">{"".join(card_ur(BYID[i]) for i in t["ids"])}</div><div class="chips light" style="margin-top:34px"><span class="lbl">مزید:</span>{others}</div></div></section>'
        page(f'/ur/interests/{t["slug"]}/', title, f"{title}: {lede}"[:300], body, active="/ur/interests/", over=True, lang="ur")

    # when to go
    rows = []
    for k in REGION_ORDER:
        rows.append(f'<tr class="rg"><th colspan="13">{e(REGIONS[k]["ur"])}</th></tr>')
        for p in [x for x in PLACES if x["region"] == k]:
            rows.append(f'<tr><th><a href="/ur/places/{p["id"]}/">{e(p["ur"])}</a></th>' + "".join(f'<td class="m{v}" title="{UMON[i]}"></td>' for i, v in enumerate(p["months"])) + '</tr>')
    body = hero('<img src="/img/phander.jpg" alt="">', "جانے کا بہترین وقت", "کب جائیں، مہینہ بہ مہینہ", "", "تمام منزلیں ایک کیلنڈر پر: سبز بہترین وقت ہے، پیلا ممکن، اور سرمئی کا مطلب ہے برف یا موسم عموماً راستہ بند رکھتا ہے۔", short=True)
    body += f'''<section class="block tight"><div class="wrap"><div class="legend big"><span><i class="m2"></i>بہترین</span><span><i class="m1"></i>ممکن</span><span><i class="m0"></i>بند یا مناسب نہیں</span></div>
<div class="cal-wrap"><table class="cal"><thead><tr><th>جگہ</th>{"".join(f"<th data-m='{i}'>{m}</th>" for i, m in enumerate(UMON))}</tr></thead><tbody>{"".join(rows)}</tbody></table></div></div></section>'''
    page("/ur/when-to-go/", "شمالی پاکستان جانے کا بہترین وقت، مہینہ بہ مہینہ", "شمالی پاکستان کی 57 جگہوں کا ماہانہ کیلنڈر: ہنزہ، سکردو، سوات، ناران، نیلم، فیری میڈوز اور دیوسائی کب کھلے اور بہترین ہوتے ہیں۔", body, active="/ur/when-to-go/", over=True, lang="ur")

    # essentials
    E = URS["essentials"]
    body = hero('<img src="/img/kaghan.jpg" alt="">', "آف لائن بھی", "ضروری معلومات", "", "ہنگامی نمبر، بلندی کی بیماری، پہاڑی ڈرائیونگ اور مزید۔ ایک بار کھولنے کے بعد فون میں محفوظ۔", short=True)
    body += f'''<div class="wrap"><div class="layout"><div class="prose">
<h2>ہنگامی نمبر</h2><div class="table"><table><thead><tr><th>سروس</th><th>نمبر</th></tr></thead><tbody>{"".join(f'<tr><td>{e(a)}</td><td class="num">{e(b)}</td></tr>' for a, b in E["numbers"])}</tbody></table></div>
<h2>بلندی کی بیماری</h2><ul>{"".join(f"<li>{e(t)}</li>" for t in E["altitude"])}</ul>
<h2>پہاڑی ڈرائیونگ</h2><ul>{"".join(f"<li>{e(t)}</li>" for t in E["road"])}</ul>
<h2>کون سا موبائل نیٹ ورک چلتا ہے</h2><div class="table"><table><thead><tr><th>علاقہ</th><th>عموماً چلتا ہے</th></tr></thead><tbody>{"".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in E["network"])}</tbody></table></div>
<h2>پرمٹ اور چوکیاں</h2><ul>{"".join(f"<li>{e(t)}</li>" for t in E["permits"])}</ul>
<h2>آداب</h2><ul>{"".join(f"<li>{e(t)}</li>" for t in E["etiquette"])}</ul></div>
<aside><div class="sticky"><div class="card-box"><h3>آف لائن محفوظ کریں</h3><p style="margin:0">اینڈرائیڈ پر کروم مینو کھولیں اور <b>Add to Home screen</b> چنیں۔ آئی فون پر سفاری کے شیئر بٹن سے <b>Add to Home Screen</b>۔</p><p class="note" id="offline-state"></p></div></div></aside></div></div>'''
    page("/ur/essentials/", "شمالی پاکستان کے سفر کی ضروری معلومات", "ہنگامی نمبر، بلندی کی بیماری، پہاڑی ڈرائیونگ، پرمٹ، آداب اور موبائل نیٹ ورک کی کوریج۔", body, active="/ur/essentials/", over=True, lang="ur")

def build_business():
    c = CONTACT
    wa = f'https://wa.me/{c["whatsapp"]}?text=' + "Assalam%20o%20Alaikum%2C%20I%20want%20to%20list%20my%20business%20on%20KohNoor" if c.get("whatsapp") else ""
    btns = (f'<a class="btn" href="{wa}" rel="noopener">WhatsApp</a> ' if wa else "") + (f'<a class="btn ghost" href="mailto:{c["email"]}?subject=KohNoor%20listing">{e(c["email"])}</a>' if c.get("email") else "")
    for lang in ("en", "ur"):
        U_ = lang == "ur"
        tiers = ([("مفت بنیادی لسٹنگ", "اپنی جگہ کے صفحے پر نام، علاقہ اور رابطہ۔", ["کاروبار کا نام اور قسم", "فون یا واٹس ایپ", "گوگل میپس لنک"]),
                  ("نمایاں لسٹنگ", "صفحے کے اوپر تصویر اور واٹس ایپ بٹن کے ساتھ۔", ["تصاویر اور مختصر تعارف", "براہِ راست واٹس ایپ بٹن", "متعلقہ جگہوں کے صفحات پر نمایاں"]),
                  ("سپانسر شپ", "علاقے یا دلچسپی کے صفحات پر برانڈ کی موجودگی۔", ["علاقے کے صفحے پر بینر", "سوشل میڈیا پر ذکر", "ماہانہ کارکردگی رپورٹ"])] if U_ else
                 [("Free basic listing", "Your name, area and contact on the place page.", ["Business name and type", "Phone or WhatsApp", "Google Maps link"]),
                  ("Featured listing", "At the top of the page with a photo and a WhatsApp button.", ["Photos and a short description", "Direct WhatsApp button", "Shown on nearby place pages"]),
                  ("Sponsorship", "Brand presence on region or interest pages.", ["Banner on a region page", "Mention on our social channels", "Monthly performance report"])])
        who = (["ہوٹل اور گیسٹ ہاؤس", "جیپ اور گاڑی کرائے پر", "ٹور آپریٹر اور گائیڈ", "کیمپ سائٹس", "ریسٹورنٹ اور کیفے", "دستکاری اور مقامی دکانیں"] if U_ else
               ["Hotels and guesthouses", "Jeep and car hire", "Tour operators and guides", "Campsites", "Restaurants and cafés", "Handicraft and local shops"])
        tier_html = "".join(f'<div class="tier"><h3>{e(a)}</h3><p>{e(b)}</p><ul>{"".join(f"<li>{icon(chr(99)+chr(104)+chr(101)+chr(99)+chr(107))}{e(x)}</li>" for x in L)}</ul></div>' for a, b, L in tiers)
        contact_html = btns if btns else ('<p class="note">رابطے کی تفصیل جلد شامل کی جائے گی۔</p>' if U_ else '<p class="note">Contact details coming soon.</p>')
        T_ = (lambda a, b: b if U_ else a)
        body = hero('<img src="/img/hunza.jpg" alt="">', T_("For local businesses", "مقامی کاروبار کے لیے"), T_("List your business on KohNoor", "اپنا کاروبار کوہِ نور پر شامل کریں"), "",
                    T_("Reach travellers while they plan their trip: hotels, jeep drivers, guides and camps in every valley of the north.", "مسافروں تک اس وقت پہنچیں جب وہ سفر کی منصوبہ بندی کر رہے ہوں: شمال کی ہر وادی کے ہوٹل، جیپ ڈرائیور، گائیڈ اور کیمپ۔"), short=True,
                    extra=f'<div class="hero-cta">{btns}</div>' if btns else "")
        body += f'''<section class="block"><div class="wrap"><div class="sec-head"><div><span class="kicker">{T_("Who it is for", "کس کے لیے")}</span><h2>{T_("Built for the people who make the north work", "شمال کے سفر کو ممکن بنانے والوں کے لیے")}</h2></div></div>
<div class="chips light">{"".join(f'<span class="chip">{e(w)}</span>' for w in who)}</div></div></section>
<section class="block tight"><div class="wrap"><div class="sec-head"><div><span class="kicker">{T_("Options", "پیکجز")}</span><h2>{T_("Ways to be seen", "نظر آنے کے طریقے")}</h2><p>{T_("Prices depend on the place and season. Send us a message and we will reply with details.", "قیمت جگہ اور موسم کے مطابق ہے۔ ہمیں پیغام بھیجیں، ہم تفصیل کے ساتھ جواب دیں گے۔")}</p></div></div><div class="tiers">{tier_html}</div></div></section>
<section class="block tight"><div class="wrap"><div class="cta">{topo(5)}<div style="position:relative"><span class="kicker">{T_("Get in touch", "رابطہ کریں")}</span><h2>{T_("Tell us about your business", "اپنے کاروبار کے بارے میں بتائیں")}</h2><p>{T_("Send your business name, place, type and a few photos. We only list real businesses that we can verify.", "کاروبار کا نام، جگہ، قسم اور چند تصاویر بھیجیں۔ ہم صرف وہ اصل کاروبار شامل کرتے ہیں جن کی تصدیق کر سکیں۔")}</p></div><div style="position:relative">{contact_html}</div></div></div></section>'''
        page(("/ur" if U_ else "") + "/list-your-business/", T_("List your business on KohNoor", "اپنا کاروبار کوہِ نور پر شامل کریں"),
             T_("Hotels, guesthouses, jeep hire, tour operators and camps in Northern Pakistan: get listed on KohNoor and reach travellers planning their trip.", "شمالی پاکستان کے ہوٹل، گیسٹ ہاؤس، جیپ، ٹور آپریٹر اور کیمپ: کوہِ نور پر شامل ہوں اور سفر کی منصوبہ بندی کرنے والے مسافروں تک پہنچیں۔"),
             body, active=("/ur/list-your-business/" if U_ else ""), over=True, lang=lang)

def build_llms():
    lines = ["# KohNoor", "", "> KohNoor (kohnoor.pages.dev) is a free, independent travel guide to Northern Pakistan: Gilgit-Baltistan, Swat, Kaghan & Naran, Azad Kashmir, Chitral, Dir & Kumrat and Murree & Galiyat. Every place page gives history, best season by month, how to get there from Islamabad, Peshawar and Lahore, an estimated trip cost, live weather, a packing list and travel tips. Available in English and Urdu.", "",
             "Costs are estimates based on current fuel, coach, hotel and food rates; travel times are approximate. Road conditions in the mountains change with weather.", "", "## Main pages", "",
             f"- [Destinations]({SITE}/regions/): all {len(PLACES)} places in {len(REGIONS)} regions", f"- [When to go]({SITE}/when-to-go/): month-by-month calendar for every place",
             f"- [Interests]({SITE}/interests/): lakes, meadows, treks, history, family trips, snow, jeep adventures, hidden places", f"- [Itineraries]({SITE}/itineraries/): day-by-day routes", f"- [Trip cost planner]({SITE}/plan/)", f"- [Essentials]({SITE}/essentials/): emergency numbers, altitude sickness, permits, mobile networks", f"- [Urdu version]({SITE}/ur/)", "", "## Regions", ""]
    lines += [f"- [{REGIONS[k]['name']}]({SITE}/regions/{k}/): {REGIONS[k]['lede']}" for k in REGION_ORDER]
    lines += ["", "## Places", ""] + [f"- [{p['name']}]({SITE}/places/{p['id']}/): {first_sentence(p['intro'])} Best season: {p['season']}. About {p['hrs']} h from Islamabad." for p in PLACES]
    open(os.path.join(OUT, "llms.txt"), "w").write("\n".join(lines) + "\n")
    full = ["# KohNoor — full guide text", ""]
    for p in PLACES:
        full += [f"## {p['name']} ({REGIONS[p['region']]['name']})", f"URL: {SITE}/places/{p['id']}/", f"Altitude: about {p['alt']} m. From Islamabad: about {p['km']} km, {p['hrs']} h. Best season: {p['season']}. Vehicle: {p['vehicle']}. Mobile signal: {p['network']}.", "", p["intro"], "", "History: " + p["history"], "", "Things to do: " + "; ".join(p["todo"]) + ".", "", "Getting there: " + p["reach"], "", "Stay: " + p["stay"] + " Food: " + p["food"], "", "Tips: " + " ".join(p["tips"]), ""]
    open(os.path.join(OUT, "llms-full.txt"), "w").write("\n".join(full))

# ---------------- graphics: altitude infographic, maps ----------------
ALT_PICKS = [("mingora", None), ("chitral", None), ("kalam", None), ("skardu", None), ("murree", None), ("hunza", None), ("attabad", None), ("malam-jabba", None),
             ("mahodand", None), ("fairy-meadows", None), ("katora-lake", None), ("ratti-gali", None), ("deosai", None), ("babusar", None), ("passu-khunjerab", 4690)]
def alt_chart(lang="en"):
    W, H, top, base = 1200, 460, 70, 400
    pts = []
    for i, (pid, alt) in enumerate(ALT_PICKS):
        p = BYID[pid]; a = alt or p["alt"]
        x = 50 + i * (W - 100) / (len(ALT_PICKS) - 1); y = base - (a / 5000) * (base - top)
        nm = ("خنجراب پاس" if lang == "ur" else "Khunjerab Pass") if alt else (p["ur"] if lang == "ur" else p["name"].split(" (")[0].split(" &")[0])
        pts.append((x, y, a, nm, pid))
    rnd = random.Random(7); d = f"M0 {base + 40} L0 {pts[0][1] + 30:.0f}"
    for i, (x, y, *_) in enumerate(pts):
        if i:
            px, py = pts[i - 1][0], pts[i - 1][1]; mx = (px + x) / 2; dip = max(py, y) + 18 + rnd.random() * 34
            d += f" L{mx - 14:.0f} {dip:.0f} L{mx + 9:.0f} {dip - 10:.0f}"
        d += f" L{x - 9:.0f} {y + 8:.0f} L{x:.0f} {y:.0f} L{x + 9:.0f} {y + 8:.0f}"
    d += f" L{W} {pts[-1][1] + 40:.0f} L{W} {base + 40} Z"
    back = f"M0 {base + 40} " + " ".join(f"L{x:.0f} {base - (base - top) * (0.35 + 0.55 * rnd.random()):.0f}" for x in range(0, W + 1, 60)) + f" L{W} {base + 40} Z"
    grid = "".join(f'<line x1="0" x2="{W}" y1="{base - (m / 5000) * (base - top):.0f}" y2="{base - (m / 5000) * (base - top):.0f}" class="g"/><text x="8" y="{base - (m / 5000) * (base - top) - 6:.0f}" class="gl">{fmt(m)} {"میٹر" if lang == "ur" else "m"}</text>' for m in (1000, 2000, 3000, 4000))
    y25 = base - (2500 / 5000) * (base - top)
    band = f'<line x1="0" x2="{W}" y1="{y25:.0f}" y2="{y25:.0f}" class="warn"/><text x="{W - 8}" y="{y25 - 7:.0f}" text-anchor="end" class="wl">{"2,500 میٹر سے اوپر بلندی کی بیماری ممکن" if lang == "ur" else "Above 2,500 m: altitude sickness possible"}</text>'
    pre = "/ur" if lang == "ur" else ""
    caps = "".join(f'<path d="M{x - 9:.0f} {y + 8:.0f} L{x:.0f} {y:.0f} L{x + 9:.0f} {y + 8:.0f} L{x + 5:.0f} {y + 13:.0f} L{x + 1:.0f} {y + 9:.0f} L{x - 4:.0f} {y + 14:.0f} Z" fill="#F4F6F5"/>' for x, y, a, *_ in pts if a >= 3200)
    marks = "".join(f'<a href="{pre}/places/{pid}/"><line x1="{x:.0f}" x2="{x:.0f}" y1="{y:.0f}" y2="{y - 26:.0f}" class="st"/><circle cx="{x:.0f}" cy="{y:.0f}" r="6.5" class="dot"/><text x="{x:.0f}" y="{y - 46:.0f}" text-anchor="middle" class="nm">{e(nm)}</text><text x="{x:.0f}" y="{y - 31:.0f}" text-anchor="middle" class="al">{fmt(a)} {"میٹر" if lang == "ur" else "m"}</text></a>' for x, y, a, nm, pid in pts)
    return f'''<div class="alt-wrap"><svg class="alt-chart" viewBox="0 0 {W} {H}" role="img" aria-label="{"منزلوں کی بلندی" if lang == "ur" else "Altitude of destinations"}"><defs>
<linearGradient id="altg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E6B57"/><stop offset="1" stop-color="#0E2433"/></linearGradient>
<linearGradient id="snowg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".22" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="ridge"><path d="{d}"/></clipPath></defs>
<path d="{back}" fill="#21465E" opacity=".35"/>{grid}{band}<path d="{d}" fill="url(#altg)"/>
{caps}{marks}</svg></div>'''

def map_box(region=None, lang="en", tall=False, filters=False):
    chips = ""
    if filters:
        lab = (lambda k: REGIONS[k]["ur"]) if lang == "ur" else (lambda k: REGIONS[k]["name"])
        chips = f'<div class="map-filters"><button class="chip on" data-filter="all">{"سب" if lang == "ur" else "All"}</button>' + "".join(f'<button class="chip" data-filter="{k}">{e(lab(k))}</button>' for k in REGION_ORDER) + f'<button class="chip" data-filter="hidden">{"چھپی جگہیں" if lang == "ur" else "Hidden places"}</button></div>'
    legend = f'<div class="map-legend"><span><i class="lg-f"></i>{"مشہور" if lang == "ur" else "Famous"}</span><span><i class="lg-h"></i>{"چھپی جگہ" if lang == "ur" else "Hidden"}</span></div>'
    return f'{chips}<div class="kmap-wrap"><div class="kmap{" tall" if tall else ""}" data-region="{region or ""}" role="region" aria-label="{"نقشہ" if lang == "ur" else "Map of destinations"}"><div class="kmap-load">{"نقشہ لوڈ ہو رہا ہے…" if lang == "ur" else "Loading map…"}</div></div>{legend}</div>'

def build_maps():
    for lang in ("en", "ur"):
        U_ = lang == "ur"
        body = hero('<img src="/img/r-gb.jpg" alt="">', "نقشہ" if U_ else "Map", "شمال کا نقشہ" if U_ else "Map of the north", "", ("تمام منزلیں ایک نقشے پر۔ کسی بھی نشان پر ٹیپ کریں اور اس جگہ کا رہنما کھولیں۔" if U_ else f"All {len(PLACES)} destinations on one map. Tap a pin to open its guide."), short=True)
        body += f'<section class="block tight"><div class="wrap">{map_box(lang=lang, tall=True, filters=True)}</div></section>'
        page(("/ur" if U_ else "") + "/map/", "شمالی پاکستان کا نقشہ" if U_ else "Map of Northern Pakistan destinations",
             ("شمالی پاکستان کی تمام 57 منزلوں کا انٹرایکٹو نقشہ۔" if U_ else "Interactive map of 57 destinations in Northern Pakistan: Hunza, Skardu, Swat, Naran, Neelum, Chitral, Fairy Meadows and hidden lakes."),
             body, active=("/ur/map/" if U_ else "/map/"), over=True, lang=lang)

def build_misc():
    body = hero('<img src="/img/naltar.jpg" alt="">', "Lost in the mountains", "This page is off the map", lede="The page you were looking for does not exist. Try searching for a place instead.", extra=f'<div class="hero-search"><button data-open-search>{icon("search")}Search a valley, lake or town</button></div>', short=True)
    page("/404.html", "Page not found", "This page does not exist.", body, over=True)
    body = hero('<img src="/img/kaghan.jpg" alt="">', "Offline", "You are offline", lede="This page has not been saved yet. Pages you opened before still work, and the essentials are always saved.", extra='<p style="margin-top:20px"><a class="btn" href="/essentials/">Open offline essentials</a></p>', short=True)
    page("/offline/", "Offline", "You are offline.", body, over=True)

def build_assets():
    A = os.path.join(OUT, "assets"); os.makedirs(os.path.join(A, "fonts"), exist_ok=True)
    for f in ["style.css", "app.js"]: shutil.copy(os.path.join(SRC, "assets", f), A)
    for f in os.listdir(os.path.join(SRC, "fonts")):
        if f.endswith(".woff2"): shutil.copy(os.path.join(SRC, "fonts", f), os.path.join(A, "fonts"))
    for f in os.listdir(os.path.join(SRC, "brand")): shutil.copy(os.path.join(SRC, "brand", f), A)
    shutil.copytree(os.path.join(SRC, "img"), os.path.join(OUT, "img"), dirs_exist_ok=True)
    client = {"regions": {k: {"name": REGIONS[k]["name"]} for k in REGION_ORDER},
              "costs": COSTS,
              "places": [{**{k: p[k] for k in ["id","name","ur","region","kind","alt","km","hrs","route","months","jeep","fly","lat","lon","season","vehicle","network","stay","reach"]},
                          "intro": first_sentence(p["intro"]), "region_name": REGIONS[p["region"]]["name"], "region_ur": REGIONS[p["region"]]["ur"], "thumb": PHOTOS.get(p["id"], {}).get("thumb")} for p in PLACES]}
    open(os.path.join(A, "data.js"), "w").write("window.KN=" + json.dumps(client, ensure_ascii=False, separators=(",", ":")) + ";")
    json.dump({"name": "KohNoor — Northern Pakistan Travel Guide", "short_name": "KohNoor", "start_url": "/", "scope": "/", "display": "standalone",
               "background_color": "#0E2433", "theme_color": "#0E2433", "description": "The complete travel guide to Northern Pakistan.",
               "icons": [{"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"},
                         {"src": "/assets/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]},
              open(os.path.join(OUT, "manifest.webmanifest"), "w"), indent=1)
    core = ["/", "/essentials/", "/plan/", "/offline/", "/assets/style.css", "/assets/app.js", "/assets/data.js", "/assets/icon.svg",
            "/assets/fonts/bricolage-grotesque-latin-800-normal.woff2", "/assets/fonts/source-sans-3-latin-400-normal.woff2", "/img/kaghan.jpg"]
    open(os.path.join(OUT, "sw.js"), "w").write(f"""// KohNoor service worker
const V='kohnoor-v4', CORE={json.dumps(core)};
self.addEventListener('install',e=>e.waitUntil(caches.open(V).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{{
  const u=new URL(e.request.url); if(e.request.method!=='GET'||u.origin!==location.origin) return;
  if(e.request.mode==='navigate'){{ e.respondWith(fetch(e.request).then(r=>{{const c=r.clone();caches.open(V).then(x=>x.put(e.request,c));return r;}}).catch(()=>caches.match(e.request).then(r=>r||caches.match('/offline/')))); return; }}
  e.respondWith(caches.match(e.request).then(hit=>{{const net=fetch(e.request).then(r=>{{const c=r.clone();caches.open(V).then(x=>x.put(e.request,c));return r;}}).catch(()=>hit); return hit||net;}}));
}});
""")
    urls = ["/", "/map/", "/regions/", "/interests/", "/when-to-go/", "/gallery/", "/itineraries/", "/plan/", "/essentials/", "/about/"] + [f"/interests/{t['slug']}/" for t in THEMES] + ["/list-your-business/", "/ur/"] + sorted("/ur" + u for u in UR_PATHS) + [f"/regions/{k}/" for k in REGION_ORDER] + [f"/places/{p['id']}/" for p in PLACES] + [f"/itineraries/{x['id']}/" for x in ITINS]
    open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{date.today()}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    open(os.path.join(OUT, "_headers"), "w").write("/assets/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n/img/*\n  Cache-Control: public, max-age=2592000\n/assets/*\n  Cache-Control: public, max-age=86400\n/sw.js\n  Cache-Control: no-cache\n")
    return len(urls)

if __name__ == "__main__":
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    n = build_assets()
    build_home(); build_regions(); build_places(); build_itins(); build_plan(); build_essentials(); build_about(); build_interests(); build_when(); build_gallery(); build_urdu(); build_maps(); build_business(); build_llms(); build_misc()
    print("pages in sitemap:", n)
