import json, requests, time, os, sys
sys.stdout.reconfigure(encoding="utf-8")

# n=name, co=country/region, ar=area(km2), ty=type, fa=famousFor,
# im=wikipedia_image_url (None if not found)

DESERTS_RAW = [
    # ── AFRIQUE ──────────────────────────────────────────────────────────────
    {"n":"Sahara","co":"North Africa","ar":9200000,"ty":"Hot desert","fa":"The world's largest hot desert, roughly the size of the United States; was a lush savanna with lakes and hippos just 6,000 years ago before a shift in Earth's axial tilt dried it out."},
    {"n":"Kalahari Desert","co":"Botswana, Namibia, South Africa","ar":900000,"ty":"Semi-arid desert","fa":"Mostly covered in grass and scrub rather than bare sand; home to the San people, who have lived as hunter-gatherers here for over 20,000 years."},
    {"n":"Namib Desert","co":"Namibia","ar":81000,"ty":"Coastal desert","fa":"Considered the world's oldest desert at over 55 million years; its red dunes at Sossusvlei, among the tallest on Earth, meet the cold Atlantic fog that sustains desert-adapted wildlife."},
    {"n":"Skeleton Coast","co":"Namibia","ar":16845,"ty":"Coastal desert","fa":"Named for the whale bones and shipwrecks littering its shore; dense Atlantic fog has wrecked over a thousand ships against its dunes since the 15th century."},
    {"n":"Danakil Desert","co":"Ethiopia and Eritrea","ar":137600,"ty":"Hot desert","fa":"One of the hottest and lowest places on Earth; home to Erta Ale's lava lake and vast turquoise-and-yellow sulfur fields at Dallol."},
    {"n":"Chalbi Desert","co":"Kenya","ar":4500,"ty":"Hot desert","fa":"A flat, cracked-clay desert near Lake Turkana, close to where some of humanity's oldest fossil ancestors have been unearthed."},
    {"n":"Nubian Desert","co":"Sudan","ar":400000,"ty":"Hot desert","fa":"Home to over 200 ancient pyramids built by the Kingdom of Kush — more than in all of Egypt, though far less visited."},
    {"n":"Libyan Desert","co":"Libya, Egypt, Sudan","ar":1200000,"ty":"Hot desert","fa":"One of the most barren parts of the Sahara; the Libyan Desert Glass found here, formed by an ancient meteor airburst, was used in a brooch found in Tutankhamun's tomb."},
    {"n":"Western Desert of Egypt","co":"Egypt","ar":680650,"ty":"Hot desert","fa":"Covers two-thirds of Egypt; legend holds that an entire Persian army of 50,000 men vanished into its sands in 525 BC, never to be found."},
    {"n":"White Desert, Egypt","co":"Egypt","ar":300,"ty":"Chalk desert","fa":"Wind-carved chalk-white rock formations rise like mushrooms and icebergs from the sand, the eroded remains of an ancient seabed."},
    {"n":"Sinai Desert","co":"Egypt","ar":61000,"ty":"Hot desert","fa":"According to tradition, Moses received the Ten Commandments atop Mount Sinai; its granite peaks rise dramatically straight from the desert floor."},
    # ── MOYEN-ORIENT ─────────────────────────────────────────────────────────
    {"n":"Arabian Desert","co":"Saudi Arabia and the Arabian Peninsula","ar":2330000,"ty":"Hot desert","fa":"Covers most of the Arabian Peninsula; the world's largest conventional oil reserves were discovered beneath its sands in the 20th century."},
    {"n":"Rub' al Khali","co":"Saudi Arabia, Oman, UAE, Yemen","ar":650000,"ty":"Sand sea","fa":"Known as the 'Empty Quarter', the largest continuous sand sea on Earth, with dunes up to 250 m tall; explorer Wilfred Thesiger crossed it by camel in the 1940s."},
    {"n":"Syrian Desert","co":"Syria, Jordan, Iraq, Saudi Arabia","ar":500000,"ty":"Hot desert","fa":"Crossed for millennia by camel caravans linking Mesopotamia to the Mediterranean; the ancient oasis city of Palmyra grew wealthy controlling its trade routes."},
    {"n":"Negev Desert","co":"Israel","ar":13000,"ty":"Hot desert","fa":"Covers over half of Israel; ancient Nabatean engineers built sophisticated water-channeling systems here 2,000 years ago that are still studied today."},
    {"n":"Judean Desert","co":"Israel and the West Bank","ar":1300,"ty":"Hot desert","fa":"The Dead Sea Scrolls, the oldest known biblical manuscripts, were discovered hidden in caves above the Dead Sea here in 1947."},
    {"n":"Wadi Rum","co":"Jordan","ar":720,"ty":"Hot desert","fa":"Nicknamed the 'Valley of the Moon'; T.E. Lawrence based his WWI operations here, and its red sandstone canyons have stood in for Mars in several films."},
    {"n":"Dasht-e Lut","co":"Iran","ar":51800,"ty":"Salt desert","fa":"Holds the record for the hottest land surface temperature ever measured by satellite — 70.7°C — and contains the towering Lut yardangs, among the tallest sand formations on Earth."},
    {"n":"Dasht-e Kavir","co":"Iran","ar":77600,"ty":"Salt desert","fa":"A vast salt desert where a thin, deceptively solid-looking crust can collapse into deep mud beneath unwary travelers."},
    {"n":"Registan Desert","co":"Afghanistan","ar":146000,"ty":"Hot desert","fa":"Its name literally means 'place of sand'; shifting dunes here have buried and revealed ancient caravan routes for centuries."},
    # ── ASIE CENTRALE ────────────────────────────────────────────────────────
    {"n":"Karakum Desert","co":"Turkmenistan","ar":350000,"ty":"Cold winter desert","fa":"Home to the 'Door to Hell', a natural gas crater accidentally ignited by Soviet engineers in 1971 that has burned continuously ever since."},
    {"n":"Kyzylkum Desert","co":"Uzbekistan and Kazakhstan","ar":300000,"ty":"Cold winter desert","fa":"Its name means 'Red Sand'; the shrinking Aral Sea on its edge has left rusting fishing boats stranded kilometers from any water."},
    # ── ASIE DE L'EST ────────────────────────────────────────────────────────
    {"n":"Gobi Desert","co":"China and Mongolia","ar":1295000,"ty":"Cold desert","fa":"One of the few deserts cold enough for snow; the first-ever dinosaur eggs and nest fossils were discovered here in the 1920s."},
    {"n":"Taklamakan Desert","co":"China","ar":270000,"ty":"Sand desert","fa":"Its name is often translated as 'place of no return'; Bronze Age travelers with European features, mummified by the arid climate, were found along its ancient Silk Road routes."},
    {"n":"Ordos Desert","co":"China","ar":90650,"ty":"Cold desert","fa":"A rapidly expanding desert on the Mongolian Plateau where China has planted a 'Great Green Wall' of trees to halt the encroaching sand."},
    {"n":"Dzungaria Basin desert","co":"China","ar":380000,"ty":"Cold desert","fa":"Home to the last truly wild population of Przewalski's horse before 20th-century reintroduction efforts, in one of Central Asia's most isolated basins."},
    {"n":"Kumtag Desert","co":"China","ar":19500,"ty":"Sand desert","fa":"Contains 'singing dunes' that produce a deep booming sound as sand cascades down their faces — an effect studied by acousticians for over a century."},
    # ── ASIE DU SUD ──────────────────────────────────────────────────────────
    {"n":"Thar Desert","co":"India and Pakistan","ar":200000,"ty":"Hot desert","fa":"The most densely populated desert on Earth, with over 80 people per km²; its dunes host the Jaisalmer 'Golden City', built from local sandstone."},
    # ── AMÉRIQUE DU NORD ─────────────────────────────────────────────────────
    {"n":"Great Basin Desert","co":"United States","ar":492000,"ty":"Cold desert","fa":"North America's largest desert, defined by dozens of north-south mountain ranges separated by valleys that trap water with no outlet to the sea."},
    {"n":"Chihuahuan Desert","co":"United States and Mexico","ar":450000,"ty":"Hot desert","fa":"North America's largest hot desert; its gypsum dunes at White Sands, New Mexico are the largest gypsum dune field on the planet."},
    {"n":"Sonoran Desert","co":"United States and Mexico","ar":260000,"ty":"Hot desert","fa":"The only place on Earth where the saguaro cactus grows wild, some living over 150 years and reaching 12 meters tall."},
    {"n":"Mojave Desert","co":"United States","ar":124000,"ty":"Hot desert","fa":"Home to Death Valley, the hottest and driest place in North America, where ground temperatures have been recorded above 90°C."},
    {"n":"Painted Desert, Arizona","co":"United States","ar":7800,"ty":"Badlands desert","fa":"Its banded cliffs of red, orange and lavender mudstone, visible across the Petrified Forest, were laid down over 200 million years ago."},
    {"n":"Black Rock Desert, Nevada","co":"United States","ar":3142,"ty":"Hot desert","fa":"A vast, perfectly flat ancient lakebed that hosts the Burning Man festival each year and several land-speed world records."},
    # ── AMÉRIQUE DU SUD ──────────────────────────────────────────────────────
    {"n":"Atacama Desert","co":"Chile","ar":105000,"ty":"Cold coastal desert","fa":"The driest non-polar desert on Earth; some weather stations have never recorded a drop of rain, and its clear skies host the world's most powerful astronomical telescopes."},
    {"n":"Patagonian Desert","co":"Argentina","ar":673000,"ty":"Cold desert","fa":"South America's largest desert, shaped by the Andes blocking Pacific moisture; ferocious year-round winds can exceed 100 km/h."},
    {"n":"Monte Desert, Argentina","co":"Argentina","ar":460000,"ty":"Hot desert","fa":"A little-known desert ecoregion rich in cacti and shrubland, stretching along Argentina's western edge in the rain shadow of the Andes."},
    {"n":"Sechura Desert","co":"Peru","ar":33000,"ty":"Coastal desert","fa":"A foggy coastal desert kept rain-free by the cold Humboldt Current; the El Niño phenomenon occasionally floods it, briefly turning sand into wildflower fields."},
    {"n":"La Guajira Desert","co":"Colombia","ar":15000,"ty":"Coastal desert","fa":"A wind-battered desert where dunes meet the Caribbean Sea; home to the Wayuu, Colombia's largest Indigenous group, who still travel by donkey cart."},
    # ── OCÉANIE ──────────────────────────────────────────────────────────────
    {"n":"Great Victoria Desert","co":"Australia","ar":348750,"ty":"Hot desert","fa":"Australia's largest desert; its parallel sand dunes, some over 30 km long, were shaped over millions of years by steady prevailing winds."},
    {"n":"Great Sandy Desert, Australia","co":"Australia","ar":284993,"ty":"Hot desert","fa":"Crossed by Australia's longest fence-line route, the Canning Stock Route, originally built to drive cattle nearly 1,800 km to market."},
    {"n":"Simpson Desert","co":"Australia","ar":176500,"ty":"Hot desert","fa":"Contains over 1,100 parallel red sand dunes running for hundreds of kilometers, among the longest dune systems on Earth."},
    {"n":"Tanami Desert","co":"Australia","ar":184500,"ty":"Hot desert","fa":"So remote that its only road, the Tanami Track, was built in the 1940s to reach a short-lived gold rush in the middle of nowhere."},
    {"n":"Gibson Desert","co":"Australia","ar":156000,"ty":"Hot desert","fa":"Named after explorer Alfred Gibson, who died of thirst attempting to cross it in 1874 — one of the last major Australian deserts to be mapped by Europeans."},
    {"n":"Strzelecki Desert","co":"Australia","ar":80250,"ty":"Hot desert","fa":"Crossed by the legendary Birdsville Track; explorers Burke and Wills perished near its edge in 1861 after a doomed attempt to cross the continent."},
    {"n":"Pinnacles Desert","co":"Australia","ar":17,"ty":"Limestone desert","fa":"Thousands of jagged limestone spires up to 3.5 m tall rise from yellow sand, formed from ancient seashells over the past 500,000 years."},
    # ── RÉGIONS POLAIRES ─────────────────────────────────────────────────────
    {"n":"Antarctic Desert","co":"Antarctica","ar":14000000,"ty":"Polar desert","fa":"The largest desert on Earth by area — bigger than the Sahara — because deserts are defined by low precipitation, not heat; over 70% of the planet's fresh water is locked in its ice."},
    {"n":"Arctic Desert","co":"Greenland and Arctic islands","ar":2600000,"ty":"Polar desert","fa":"Despite being covered in ice and snow, the polar air holds so little moisture that some interior valleys receive less precipitation each year than the Sahara."},
]

HEADERS = {"User-Agent": "projet_app_annecdote/1.0 (daily-facts educational app; github.com/uzan)"}

# Disambiguation overrides for names that risk colliding with an unrelated
# Wikipedia page (a city, a person, a generic word) — chosen up front this
# time instead of trusting the raw name, after the volcano/sculpture/mission
# mismatches found in the previous session.
WIKI_TITLE_OVERRIDES = {
    "Rub' al Khali":                 "Rub' al Khali",
    "Western Desert of Egypt":       "Western Desert (Egypt)",
    "White Desert, Egypt":           "White Desert (Egypt)",
    "Dzungaria Basin desert":        "Dzungaria",
    "Painted Desert, Arizona":       "Painted Desert (Arizona)",
    "Black Rock Desert, Nevada":     "Black Rock Desert (Nevada)",
    "Monte Desert, Argentina":       "Monte Desert",
    "Great Sandy Desert, Australia": "Great Sandy Desert",
    "Antarctic Desert":              "Polar desert",
    "Arctic Desert":                 "Polar desert",
}

def fetch_wiki_image(name, size=500):
    title = WIKI_TITLE_OVERRIDES.get(name, name)
    for attempt in range(3):
        if attempt > 0:
            time.sleep(2 ** attempt)
        try:
            r = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={"action":"query","titles":title,"prop":"pageimages",
                        "format":"json","pithumbsize":size},
                headers=HEADERS, timeout=12,
            )
            if not r.text.strip():
                continue
            pages = r.json()["query"]["pages"]
            page  = next(iter(pages.values()))
            return page.get("thumbnail", {}).get("source")
        except Exception:
            pass
    return None

def fetch_commons_image(query, size=500):
    try:
        r = requests.get(
            "https://commons.wikimedia.org/w/api.php",
            params={"action":"query","generator":"search","gsrsearch":query,
                    "gsrnamespace":6,"prop":"imageinfo","iiprop":"url",
                    "iiurlwidth":size,"format":"json","gsrlimit":5},
            headers=HEADERS, timeout=15,
        )
        if not r.text.strip():
            return None
        pages = r.json().get("query", {}).get("pages", {})
        for page in sorted(pages.values(), key=lambda p: p.get("index", 99)):
            info = page.get("imageinfo", [])
            if info:
                url = info[0].get("thumburl") or info[0].get("url")
                if url and ".svg" not in url.lower():
                    return url
    except Exception:
        pass
    return None

output_path = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../../assets/world/deserts.json")
)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

existing_images = {}
if os.path.exists(output_path):
    with open(output_path, encoding="utf-8") as f:
        for entry in json.load(f):
            if entry.get("im"):
                existing_images[entry["n"]] = entry["im"]
    print(f"Loaded {len(existing_images)} existing images from cache.\n")

missing = sum(1 for d in DESERTS_RAW if not existing_images.get(d["n"]))
print(f"{missing} desert(s) need image fetching.\n")
fetch_idx = 0
deserts = []
for i, d in enumerate(DESERTS_RAW, 1):
    name = d["n"]
    if existing_images.get(name):
        im = existing_images[name]
        print(f"[{i:2}/{len(DESERTS_RAW)}] {name} (cached)")
    else:
        fetch_idx += 1
        print(f"[{i:2}/{len(DESERTS_RAW)}] Fetching image for {name} ...")
        im = fetch_wiki_image(name)
        if im is None:
            im = fetch_commons_image(f"{name} desert")
            if im:
                print("  [commons] found")
        if im:
            print(f"  found: {im[:90]}")
        if fetch_idx < missing:
            time.sleep(0.8)
    deserts.append({**d, "im": im})

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(deserts, f, ensure_ascii=False, separators=(",", ":"))

fetched = sum(1 for d in deserts if d["im"])
print(f"\nDone -- {len(deserts)} deserts, {fetched} with images -> {output_path}")
