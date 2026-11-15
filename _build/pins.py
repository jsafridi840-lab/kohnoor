"""Pinterest pins: vertical 1000x1500 images + a drip-release RSS feed (Pages Function)."""
import os, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SRC, "out")
D = json.load(open(os.path.join(SRC, "data.json")))
PLACES = {p["id"]: p for p in D["PLACES"]}
REGIONS = D["REGIONS"]

# Release order: best-known first, then the rest
ORDER = ["hunza", "skardu", "fairy-meadows", "naran", "kalam", "attabad", "neelum", "deosai", "passu-khunjerab",
         "kumrat", "shogran", "malam-jabba", "chitral", "kalash", "khaplu", "shigar", "babusar", "naltar",
         "arang-kel", "ratti-gali", "mahodand", "nathia-gali", "murree", "phander", "astore-rama", "gilgit",
         "kachura", "sarfaranga", "katora-lake", "jahaz-banda", "kandol-lake", "dudipatsar", "shandur",
         "manthoka", "borith", "madyan", "bahrain", "ushu-matiltan", "utror-gabral", "kaghan", "chilas",
         "rawalakot", "muzaffarabad", "sharda", "taobat", "leepa", "miranjani", "garam-chashma", "khalti",
         "daral-lake", "gabin-jabba", "marghazar", "mingora", "swat-museum", "butkara", "udegram", "jahanabad-buddha"]
ORDER += [i for i in PLACES if i not in ORDER]

HOOKS = {"famous": "Complete travel guide", "hidden": "Hidden gem guide"}
F = lambda n, s: ImageFont.truetype(os.path.join(SRC, "fonts", n), s)


def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines


def pin_image(p):
    src = os.path.join(SRC, "img", p["id"] + ".jpg")
    im = Image.open(src).convert("RGB")
    W, H = 1000, 1500
    r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    im = im.crop((l, t, l + W, t + H))
    # bottom gradient for text
    grad = Image.new("L", (1, H))
    for y in range(H):
        grad.putpixel((0, y), int(max(0, (y - H * 0.42) / (H * 0.58)) ** 1.3 * 235))
    shade = Image.new("RGB", (W, H), (10, 22, 30))
    im = Image.composite(shade, im, grad.resize((W, H)))
    top = Image.new("L", (1, H))
    for y in range(H):
        top.putpixel((0, y), int(max(0, 1 - y / 260) * 150))
    im = Image.composite(shade, im, top.resize((W, H)))
    d = ImageDraw.Draw(im)
    # brand
    d.text((60, 52), "KOHNOOR", font=F("bricolage-grotesque-latin-800-normal.ttf", 40), fill=(255, 255, 255))
    d.text((60, 100), "Northern Pakistan Travel Guide", font=F("source-sans-3-latin-600-normal.ttf", 28), fill=(225, 235, 240))
    # tag pill
    tag = HOOKS[p["kind"]].upper()
    tf = F("source-sans-3-latin-600-normal.ttf", 30)
    tw = d.textlength(tag, font=tf)
    y = 900
    d.rounded_rectangle((60, y, 60 + tw + 44, y + 54), 27, fill=(232, 168, 56))
    d.text((82, y + 9), tag, font=tf, fill=(20, 20, 20))
    # title
    tfont = F("bricolage-grotesque-latin-800-normal.ttf", 92)
    lines = wrap(d, p["name"], tfont, 880)
    if len(lines) > 2:
        tfont = F("bricolage-grotesque-latin-800-normal.ttf", 72); lines = wrap(d, p["name"], tfont, 880)
    y += 80
    for ln in lines:
        d.text((58, y), ln, font=tfont, fill=(255, 255, 255)); y += tfont.size + 6
    y += 14
    reg = REGIONS[p["region"]]["name"]
    d.text((60, y), reg, font=F("source-sans-3-latin-600-normal.ttf", 38), fill=(232, 168, 56)); y += 70
    facts = [f"{p['alt']:,} m altitude", f"{p['hrs']} hrs from Islamabad" if p.get("hrs") else None, f"Best: {p['season']}"]
    ff = F("source-sans-3-latin-600-normal.ttf", 34)
    for fct in [x for x in facts if x]:
        d.ellipse((62, y + 14, 76, y + 28), fill=(232, 168, 56))
        d.text((92, y), fct, font=ff, fill=(240, 244, 246)); y += 48
    # footer
    d.text((60, H - 80), "Route · Costs · Weather  |  kohnoor.pages.dev", font=F("source-sans-3-latin-600-normal.ttf", 32), fill=(255, 255, 255))
    os.makedirs(os.path.join(OUT, "pins"), exist_ok=True)
    im.save(os.path.join(OUT, "pins", p["id"] + ".jpg"), quality=86, optimize=True, progressive=True)


def describe(p):
    reg = REGIONS[p["region"]]["name"]
    intro = p["intro"]
    return (f"{p['name']}, {reg}: {intro} Altitude {p['alt']:,} m, best season {p['season']}. "
            f"Route, travel time from Islamabad, costs, where to stay and live weather on KohNoor. "
            f"#Pakistan #NorthernPakistan #{p['region'].replace('-', '').title()} #TravelPakistan #VisitPakistan")[:495]


def build_pins():
    items = []
    for i in ORDER:
        p = PLACES[i]
        pin_image(p)
        items.append({"id": i, "title": f"{p['name']} Travel Guide: Route, Costs & Best Time",
                      "link": f"https://kohnoor.pages.dev/places/{i}/", "img": f"https://kohnoor.pages.dev/pins/{i}.jpg",
                      "desc": describe(p)})
    js = "export const PINS = " + json.dumps(items, ensure_ascii=False) + ";\n"
    os.makedirs(os.path.join(SRC, "functions"), exist_ok=True)
    open(os.path.join(SRC, "functions", "_pins.js"), "w").write(js)
    print("pins:", len(items))


if __name__ == "__main__":
    build_pins()


# ---------- Design B (region boards): cream title panel on top, photo below ----------
REGION_BOARDS = {
    "swat": "Swat Valley Travel Guide",
    "gb": "Gilgit-Baltistan: Hunza, Skardu & Fairy Meadows",
    "kaghan": "Naran Kaghan Valley Travel",
    "ajk": "Azad Kashmir & Neelum Valley Travel",
    "chitral": "Chitral & Kalash Valley Travel",
    "galiyat": "Murree, Nathia Gali & Galiyat",
    "dir": "Kumrat Valley & Dir Travel",
}


def pin_image_b(p):
    W, H = 1000, 1500
    cream, ink, gold = (247, 242, 232), (18, 38, 48), (196, 132, 30)
    im = Image.new("RGB", (W, H), cream)
    ph = Image.open(os.path.join(SRC, "img", p["id"] + ".jpg")).convert("RGB")
    PW, PH = 1000, 1060
    r = max(PW / ph.width, PH / ph.height)
    ph = ph.resize((round(ph.width * r), round(ph.height * r)), Image.LANCZOS)
    l, t = (0 if p['id'] == 'kalash' else (ph.width - PW) // 2), max(0, (ph.height - PH) // 2)
    im.paste(ph.crop((l, t, l + PW, t + PH)), (0, H - PH))
    d = ImageDraw.Draw(im)
    d.text((60, 48), "KOHNOOR  ·  NORTHERN PAKISTAN TRAVEL GUIDE", font=F("source-sans-3-latin-700-normal.ttf" if os.path.exists(os.path.join(SRC, "fonts", "source-sans-3-latin-700-normal.ttf")) else "source-sans-3-latin-600-normal.ttf", 28), fill=gold)
    tfont = F("bricolage-grotesque-latin-800-normal.ttf", 104)
    lines = wrap(d, p["name"], tfont, 880)
    if len(lines) > 1:
        tfont = F("bricolage-grotesque-latin-800-normal.ttf", 76); lines = wrap(d, p["name"], tfont, 880)
    if len(lines) > 2:
        tfont = F("bricolage-grotesque-latin-800-normal.ttf", 62); lines = wrap(d, p["name"], tfont, 880)
    block = len(lines) * (tfont.size + 4) + 60
    y = 100 + max(0, (300 - block) // 2)
    for ln in lines:
        d.text((56, y), ln, font=tfont, fill=ink); y += tfont.size + 4
    sub = "Hidden gem: how to get there" if p["kind"] == "hidden" else "Things to do, route & costs"
    sf = F("source-sans-3-latin-600-normal.ttf", 36); line2 = sub + "  ·  " + REGIONS[p["region"]]["name"]
    if d.textlength(line2, font=sf) > 890: line2 = sub
    d.text((60, y + 12), line2, font=sf, fill=(70, 86, 94))
    # info chip on photo
    chip = f"{p['alt']:,} m  ·  Best: {p['season'].split('(')[0].strip()}"
    cf = F("source-sans-3-latin-600-normal.ttf", 30)
    cw = d.textlength(chip, font=cf)
    d.rounded_rectangle((40, H - 110, 40 + cw + 48, H - 50), 30, fill=(255, 255, 255))
    d.text((64, H - 101), chip, font=cf, fill=ink)
    os.makedirs(os.path.join(OUT, "pins", "b"), exist_ok=True)
    im.save(os.path.join(OUT, "pins", "b", p["id"] + ".jpg"), quality=86, optimize=True, progressive=True)


def describe_b(p):
    reg = REGIONS[p["region"]]["name"]
    todo = "; ".join(p.get("todo", [])[:3])
    return (f"Planning a trip to {p['name']} in {reg}? Top things to do: {todo}. "
            f"Best time: {p['season']}. Full route from Islamabad, budget, hotels and live weather on KohNoor.")[:495]


def build_pins_b():
    boards = {}
    for i in ORDER:
        p = PLACES[i]
        pin_image_b(p)
        boards.setdefault(p["region"], []).append({
            "id": i, "title": f"Things to Do in {p['name']}, Pakistan"[:100],
            "link": f"https://kohnoor.pages.dev/places/{i}/", "img": f"https://kohnoor.pages.dev/pins/b/{i}.jpg",
            "desc": describe_b(p)})
    js = "export const BOARDS = " + json.dumps(boards, ensure_ascii=False) + ";\n"
    open(os.path.join(SRC, "functions", "_pins_b.js"), "w").write(js)
    print("pins B:", sum(len(v) for v in boards.values()))
