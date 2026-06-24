import json, requests, time, os, sys
sys.stdout.reconfigure(encoding="utf-8")

# n=name, co=country/region, le=length(km), mo=mouth (where it empties),
# fa=famousFor, im=wikipedia_image_url (None if not found)

RIVERS_RAW = [
    # ── AFRIQUE ──────────────────────────────────────────────────────────────
    {"n":"Nile","co":"Egypt, Sudan, Uganda, Ethiopia","le":6650,"mo":"Mediterranean Sea","fa":"The traditionally recognized longest river on Earth; its annual floods deposited the fertile silt that allowed ancient Egyptian civilization to flourish for 3,000 years."},
    {"n":"Congo River","co":"DR Congo, Republic of the Congo","le":4700,"mo":"Atlantic Ocean","fa":"The world's deepest river, plunging past 220 m in places; it is the only major river to cross the equator twice."},
    {"n":"Niger River","co":"Guinea, Mali, Niger, Nigeria","le":4180,"mo":"Gulf of Guinea","fa":"Flows in a strange boomerang shape, bending through the Sahara before turning back toward the sea — a route that baffled European explorers for centuries."},
    {"n":"Zambezi","co":"Zambia, Zimbabwe, Mozambique","le":2574,"mo":"Indian Ocean","fa":"Plunges over Victoria Falls, twice the height of Niagara, where it sends spray visible from 20 km away — locals call it 'The Smoke That Thunders'."},
    {"n":"Limpopo River","co":"South Africa, Botswana, Mozambique","le":1750,"mo":"Indian Ocean","fa":"Immortalized by Rudyard Kipling as 'the great grey-green, greasy Limpopo River, all set about with fever-trees' in the Just So Stories."},
    {"n":"Okavango River","co":"Angola, Namibia, Botswana","le":1600,"mo":"Okavango Delta (endorheic)","fa":"One of the world's few rivers that never reaches the sea; it disperses into the Kalahari sand, creating a vast inland delta that floods opposite to the rainy season."},
    {"n":"Senegal River","co":"Guinea, Mali, Senegal, Mauritania","le":1086,"mo":"Atlantic Ocean","fa":"Marks much of the border between Senegal and Mauritania; its seasonal floods were once as vital to local farming as the Nile's were to Egypt."},
    {"n":"Orange River","co":"South Africa, Namibia","le":2200,"mo":"Atlantic Ocean","fa":"South Africa's longest river; diamonds washed down from inland deposits made its mouth one of the richest alluvial diamond fields on Earth."},
    # ── MOYEN-ORIENT ─────────────────────────────────────────────────────────
    {"n":"Tigris","co":"Turkey, Syria, Iraq","le":1900,"mo":"Shatt al-Arab (Persian Gulf)","fa":"Together with the Euphrates it cradled Mesopotamia, the 'land between two rivers' where writing, the wheel, and the first cities were invented."},
    {"n":"Euphrates","co":"Turkey, Syria, Iraq","le":2800,"mo":"Shatt al-Arab (Persian Gulf)","fa":"The longest river in Western Asia; the Book of Revelation names it as the site of the prophesied final battle of Armageddon."},
    {"n":"Jordan River","co":"Israel, Jordan, Palestine, Syria","le":251,"mo":"Dead Sea","fa":"Despite its modest length, it is one of the most fought-over rivers in history; tradition holds that Jesus was baptized in its waters."},
    # ── ASIE ─────────────────────────────────────────────────────────────────
    {"n":"Yangtze","co":"China","le":6300,"mo":"East China Sea","fa":"Asia's longest river; the Three Gorges Dam built across it is the largest power station on Earth by installed capacity."},
    {"n":"Yellow River","co":"China","le":5464,"mo":"Bohai Sea","fa":"Called 'China's Sorrow' for catastrophic floods that have killed millions throughout history; its yellow color comes from vast quantities of loess silt."},
    {"n":"Pearl River","co":"China","le":2400,"mo":"South China Sea","fa":"Its delta, anchored by Guangzhou, Shenzhen and Hong Kong, forms one of the most densely urbanized and populated regions on the planet."},
    {"n":"Mekong","co":"China, Myanmar, Laos, Thailand, Cambodia, Vietnam","le":4350,"mo":"South China Sea","fa":"Supports the world's largest inland fishery, feeding tens of millions; its Tonle Sap tributary in Cambodia reverses flow direction twice a year."},
    {"n":"Salween","co":"China, Myanmar, Thailand","le":3289,"mo":"Andaman Sea","fa":"One of the longest free-flowing rivers in Asia with no major dams; it carves a gorge alongside the Mekong and Yangtze so deep the three rivers run within 100 km of each other."},
    {"n":"Irrawaddy","co":"Myanmar","le":2170,"mo":"Andaman Sea","fa":"Myanmar's most important commercial waterway; Rudyard Kipling's poem 'Mandalay' romanticized its 'old flotilla' of steamers."},
    {"n":"Brahmaputra","co":"Tibet, India, Bangladesh","le":2900,"mo":"Bay of Bengal","fa":"One of the few major rivers considered male in local tradition (its name means 'son of Brahma'); it carries more sediment than almost any river on Earth."},
    {"n":"Ganges","co":"India, Bangladesh","le":2525,"mo":"Bay of Bengal","fa":"Hinduism's holiest river, personified as the goddess Ganga; over 400 million people live in its basin, more than any other river system."},
    {"n":"Indus","co":"China, India, Pakistan","le":3180,"mo":"Arabian Sea","fa":"Gave its name to the word 'India' itself; it nourished the Indus Valley Civilization, one of the world's first great urban cultures 4,500 years ago."},
    {"n":"Tarim River","co":"China","le":2376,"mo":"Lop Nur (endorheic)","fa":"Central Asia's longest inland river, feeding the Taklamakan Desert before vanishing into the dried salt flats of Lop Nur, once a Chinese nuclear test site."},
    # ── RUSSIE & SIBÉRIE ─────────────────────────────────────────────────────
    {"n":"Volga","co":"Russia","le":3530,"mo":"Caspian Sea","fa":"Europe's longest river and the historic heart of Russia; it never reaches the open ocean, draining instead into the landlocked Caspian Sea."},
    {"n":"Ob River","co":"Russia","le":5410,"mo":"Gulf of Ob (Arctic Ocean)","fa":"Together with its tributary the Irtysh it forms Asia's longest river system; its delta freezes for over half the year."},
    {"n":"Yenisei","co":"Russia, Mongolia","le":5539,"mo":"Kara Sea (Arctic Ocean)","fa":"Carries more water to the Arctic Ocean than any other river; geographically it marks part of the dividing line between Western and Eastern Siberia."},
    {"n":"Lena River","co":"Russia","le":4400,"mo":"Laptev Sea (Arctic Ocean)","fa":"One of the largest rivers whose entire course lies within a single country; its delta is the largest in the Arctic and a UNESCO-recognized wetland reserve."},
    {"n":"Amur River","co":"Russia, China","le":4444,"mo":"Sea of Okhotsk","fa":"Forms much of the border between Russia and China; disputes over its exact course nearly triggered a war between the two countries in 1969."},
    {"n":"Don (river)","co":"Russia","le":1870,"mo":"Sea of Azov","fa":"One of the great rivers of Russian literature and folk song; Mikhail Sholokhov's epic 'And Quiet Flows the Don' won the Nobel Prize in Literature."},
    {"n":"Ural (river)","co":"Russia, Kazakhstan","le":2428,"mo":"Caspian Sea","fa":"Traditionally marks part of the boundary between Europe and Asia, meaning it is the only river on Earth that flows between two continents along its own course."},
    {"n":"Dnieper","co":"Russia, Belarus, Ukraine","le":2200,"mo":"Black Sea","fa":"The historic backbone of medieval Kyivan Rus'; Cossack warriors once built fortified island strongholds in its rapids to resist invasions."},
    # ── EUROPE ───────────────────────────────────────────────────────────────
    {"n":"Danube","co":"Germany, Austria, Hungary, and 6 more","le":2850,"mo":"Black Sea","fa":"Flows through more countries than any other river in the world — ten in total — and inspired Johann Strauss II's waltz 'The Blue Danube'."},
    {"n":"Rhine","co":"Switzerland, Germany, Netherlands","le":1230,"mo":"North Sea","fa":"One of Europe's busiest commercial waterways; its castle-lined gorge near Lorelei has inspired legends of a siren who lured sailors to their doom."},
    {"n":"Rhône","co":"Switzerland, France","le":813,"mo":"Mediterranean Sea","fa":"Originates from a glacier in the Swiss Alps and powers a chain of nuclear plants in France that supply a significant share of the country's electricity."},
    {"n":"Seine","co":"France","le":777,"mo":"English Channel","fa":"Paris grew up on its banks and bridges; 37 bridges cross it within the city alone, more than any other river in a single city worldwide."},
    {"n":"Loire","co":"France","le":1012,"mo":"Atlantic Ocean","fa":"France's longest river; lined with hundreds of Renaissance châteaux built by French kings, it remains one of Europe's last major rivers without a large dam."},
    {"n":"Po (river)","co":"Italy","le":652,"mo":"Adriatic Sea","fa":"Italy's longest river; it has flooded so often and so destructively that engineers have built artificial levees along nearly its entire course since Roman times."},
    {"n":"Tagus","co":"Spain, Portugal","le":1038,"mo":"Atlantic Ocean","fa":"The longest river on the Iberian Peninsula; it passes beneath Lisbon's 25 de Abril Bridge, modeled on San Francisco's Golden Gate Bridge."},
    {"n":"Douro","co":"Spain, Portugal","le":897,"mo":"Atlantic Ocean","fa":"Its steep, terraced valley produces the grapes for Port wine, named after the city of Porto at the river's mouth."},
    {"n":"Ebro","co":"Spain","le":930,"mo":"Mediterranean Sea","fa":"Spain's most voluminous river; its delta is one of the largest wetlands in the western Mediterranean and a key European rice-growing region."},
    {"n":"Thames","co":"England","le":346,"mo":"North Sea","fa":"London's river for two millennia; it famously froze solid often enough in past centuries to host 'Frost Fairs' with full markets set up on the ice."},
    {"n":"Vistula","co":"Poland","le":1047,"mo":"Baltic Sea","fa":"Poland's longest and most important river; Warsaw and Kraków both grew along its banks, and it remains almost entirely free of major dams."},
    {"n":"Elbe","co":"Czech Republic, Germany","le":1094,"mo":"North Sea","fa":"For decades during the Cold War it formed part of the border between East and West Germany, and US and Soviet troops famously met at its banks in 1945."},
    {"n":"Vltava","co":"Czech Republic","le":430,"mo":"Elbe (tributary)","fa":"Prague's river, immortalized in Bedřich Smetana's symphonic poem 'Vltava', which musically traces its journey from two mountain springs to the city."},
    {"n":"Neva","co":"Russia","le":74,"mo":"Gulf of Finland (Baltic Sea)","fa":"Despite being barely 74 km long, it discharges more water than the Rhine; Peter the Great built St. Petersburg, his 'window to the West', along its banks."},
    # ── AMÉRIQUE DU NORD ─────────────────────────────────────────────────────
    {"n":"Mississippi River","co":"United States","le":3730,"mo":"Gulf of Mexico","fa":"Mark Twain piloted steamboats on it before writing 'Life on the Mississippi'; combined with the Missouri it forms the fourth-longest river system on Earth."},
    {"n":"Missouri River","co":"United States","le":3767,"mo":"Mississippi River (tributary)","fa":"North America's longest river; explorers Lewis and Clark followed it nearly to its source on their 1804 expedition to the Pacific."},
    {"n":"Colorado River","co":"United States, Mexico","le":2330,"mo":"Gulf of California","fa":"Carved the Grand Canyon over roughly 5-6 million years; so much of its water is now diverted for irrigation that it rarely reaches the sea at all."},
    {"n":"Columbia River","co":"Canada, United States","le":2000,"mo":"Pacific Ocean","fa":"North America's largest river flowing into the Pacific; its dams generate more hydroelectric power than any river system in the United States."},
    {"n":"Rio Grande","co":"United States, Mexico","le":3050,"mo":"Gulf of Mexico","fa":"Forms nearly 2,000 km of the border between the US and Mexico; so much water is drawn off upstream that its delta has at times dried up completely."},
    {"n":"Yukon River","co":"Canada, United States","le":3190,"mo":"Bering Sea","fa":"During the 1890s Klondike Gold Rush, it was the primary highway for tens of thousands of prospectors racing toward the goldfields."},
    {"n":"Mackenzie River","co":"Canada","le":4241,"mo":"Beaufort Sea (Arctic Ocean)","fa":"Canada's longest river system; it is frozen for over half the year and can carry ice floes the size of small islands during spring breakup."},
    {"n":"Saint Lawrence River","co":"Canada, United States","le":3058,"mo":"Gulf of Saint Lawrence","fa":"Drains the Great Lakes, the largest group of freshwater lakes on Earth, into the Atlantic via a seaway used by oceangoing ships."},
    # ── AMÉRIQUE DU SUD ──────────────────────────────────────────────────────
    {"n":"Amazon River","co":"Peru, Colombia, Brazil","le":6400,"mo":"Atlantic Ocean","fa":"Carries more water than the next seven largest rivers combined and discharges so much fresh water that it dilutes the ocean's salinity over 100 km offshore."},
    {"n":"Paraná River","co":"Brazil, Paraguay, Argentina","le":4880,"mo":"Río de la Plata estuary","fa":"South America's second-longest river; the Itaipu Dam built across one of its tributaries is among the most powerful hydroelectric plants on Earth."},
    {"n":"Orinoco","co":"Venezuela, Colombia","le":2140,"mo":"Atlantic Ocean","fa":"One of the longest rivers in the world that flows entirely through just two countries; it is connected to the Amazon basin by a rare natural channel, the Casiquiare."},
    {"n":"São Francisco River","co":"Brazil","le":2914,"mo":"Atlantic Ocean","fa":"Known as the 'River of National Unity', it flows entirely within Brazil through some of the country's driest backlands, sustaining millions along its banks."},
    {"n":"Tocantins River","co":"Brazil","le":2640,"mo":"Atlantic Ocean (Pará River)","fa":"One of the largest rivers entirely within Brazil; the Tucuruí Dam built across it was one of the first major hydroelectric projects in the Amazon region."},
    # ── OCÉANIE ──────────────────────────────────────────────────────────────
    {"n":"Murray River","co":"Australia","le":2508,"mo":"Indian Ocean (via Lake Alexandrina)","fa":"Australia's longest river; paddle steamers once carried wool and wheat along it before railways took over in the early 20th century."},
]

HEADERS = {"User-Agent": "projet_app_annecdote/1.0 (daily-facts educational app; github.com/uzan)"}

# Disambiguation overrides chosen up front to dodge name collisions
# (a city, a country, a person, or a too-generic word) before fetching.
WIKI_TITLE_OVERRIDES = {
    "Niger River":            "Niger River",
    "Jordan River":           "Jordan River",
    "Don (river)":            "Don (river)",
    "Ural (river)":           "Ural (river)",
    "Po (river)":             "Po (river)",
    "Orange River":           "Orange River",
    "Murray River":           "Murray River",
    "Vltava":                 "Vltava",
    "Neva":                   "Neva River",
    "Tarim River":            "Tarim River",
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
    os.path.join(os.path.dirname(__file__), "../../assets/world/rivers.json")
)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

existing_images = {}
if os.path.exists(output_path):
    with open(output_path, encoding="utf-8") as f:
        for entry in json.load(f):
            if entry.get("im"):
                existing_images[entry["n"]] = entry["im"]
    print(f"Loaded {len(existing_images)} existing images from cache.\n")

missing = sum(1 for r in RIVERS_RAW if not existing_images.get(r["n"]))
print(f"{missing} river(s) need image fetching.\n")
fetch_idx = 0
rivers = []
for i, r in enumerate(RIVERS_RAW, 1):
    name = r["n"]
    if existing_images.get(name):
        im = existing_images[name]
        print(f"[{i:2}/{len(RIVERS_RAW)}] {name} (cached)")
    else:
        fetch_idx += 1
        print(f"[{i:2}/{len(RIVERS_RAW)}] Fetching image for {name} ...")
        im = fetch_wiki_image(name)
        if im is None:
            im = fetch_commons_image(f"{name} river")
            if im:
                print("  [commons] found")
        if im:
            print(f"  found: {im[:90]}")
        if fetch_idx < missing:
            time.sleep(1.2)
    rivers.append({**r, "im": im})

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(rivers, f, ensure_ascii=False, separators=(",", ":"))

fetched = sum(1 for r in rivers if r["im"])
print(f"\nDone -- {len(rivers)} rivers, {fetched} with images -> {output_path}")
