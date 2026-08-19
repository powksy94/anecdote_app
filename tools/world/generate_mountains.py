import json, requests, time, os, sys
sys.stdout.reconfigure(encoding="utf-8")

# n=name, co=country, ra=range, el=elevation(m), fa=famousFor,
# fc=first ascent (year + climber, only when reliably documented, else None),
# im=wikipedia_image_url (None if not found)

MOUNTAINS_RAW = [
    # ── HIMALAYA, KARAKORAM & CENTRAL ASIA ─────────────────────────────────
    {"n":"Mount Everest","co":"Nepal, China","ra":"Himalaya","el":8849,"fa":"Earth's highest peak above sea level; its summit is made of marine limestone, a reminder that it once lay at the bottom of an ancient sea.","fc":"1953, Edmund Hillary and Tenzing Norgay"},
    {"n":"K2","co":"Pakistan, China","ra":"Karakoram","el":8611,"fa":"The second-highest mountain on Earth and widely considered the deadliest of the 8000ers, nicknamed the 'Savage Mountain' for its brutal weather.","fc":"1954, Achille Compagnoni and Lino Lacedelli"},
    {"n":"Kangchenjunga","co":"Nepal, India","ra":"Himalaya","el":8586,"fa":"The first British climbers to reach the top stopped a few meters short of the true summit, honoring a promise to the local Sikkimese who consider it sacred.","fc":"1955, Joe Brown and George Band"},
    {"n":"Lhotse","co":"Nepal, China","ra":"Himalaya","el":8516,"fa":"Connected to Everest by the South Col, its name means 'South Peak' in Tibetan; the two mountains share much of the same climbing route.","fc":"1956, Fritz Luchsinger and Ernst Reiss"},
    {"n":"Makalu","co":"Nepal, China","ra":"Himalaya","el":8485,"fa":"Its distinctive four-sided pyramid shape makes it one of the most technically demanding 8000ers to climb.","fc":"1955, Jean Couzy and Lionel Terray"},
    {"n":"Cho Oyu","co":"Nepal, China","ra":"Himalaya","el":8188,"fa":"Considered the easiest of the 8000ers to climb, its name means 'Turquoise Goddess' in Tibetan.","fc":"1954, Herbert Tichy, Joseph Joechler and Pasang Dawa Lama"},
    {"n":"Dhaulagiri","co":"Nepal","ra":"Himalaya","el":8167,"fa":"Held the title of world's highest known mountain from 1808 to 1838 before Kangchenjunga and then Everest were measured.","fc":"1960, Swiss-Austrian expedition"},
    {"n":"Manaslu","co":"Nepal","ra":"Himalaya","el":8163,"fa":"Its name comes from the Sanskrit for 'mountain of the spirit'; it is sometimes called the 'Japanese mountain' for the many Japanese expeditions that pioneered its routes.","fc":"1956, Toshio Imanishi and Gyalzen Norbu"},
    {"n":"Nanga Parbat","co":"Pakistan","ra":"Himalaya","el":8126,"fa":"Nicknamed 'Killer Mountain' after claiming dozens of lives during early 20th-century expeditions before its first successful ascent, made solo.","fc":"1953, Hermann Buhl (solo)"},
    {"n":"Annapurna","co":"Nepal","ra":"Himalaya","el":8091,"fa":"The first 8000-meter peak ever climbed, but statistically still one of the most dangerous due to a very high fatality-to-summit ratio.","fc":"1950, Maurice Herzog and Louis Lachenal"},
    {"n":"Gasherbrum I","co":"Pakistan, China","ra":"Karakoram","el":8080,"fa":"Also known as Hidden Peak because it is tucked away from view behind other Karakoram giants.","fc":"1958, Pete Schoening and Andrew Kauffman"},
    {"n":"Broad Peak","co":"Pakistan, China","ra":"Karakoram","el":8051,"fa":"Named for its wide, roughly 1.5 km long summit ridge, clearly visible from base camp near K2.","fc":"1957, Fritz Wintersteller, Marcus Schmuck, Kurt Diemberger and Hermann Buhl"},
    {"n":"Gasherbrum II","co":"Pakistan, China","ra":"Karakoram","el":8035,"fa":"Generally regarded as one of the more approachable 8000ers, making it a common choice for climbers attempting their first peak above 8000 meters.","fc":"1956, Fritz Moravec, Josef Larch and Hans Willenpart"},
    {"n":"Shishapangma","co":"China","ra":"Himalaya","el":8027,"fa":"The only 8000-meter peak located entirely within a single country, Tibet; it was the last of the 8000ers to be climbed due to Chinese access restrictions.","fc":"1964, Chinese expedition"},
    {"n":"Ama Dablam","co":"Nepal","ra":"Himalaya","el":6812,"fa":"Often called the 'Matterhorn of the Himalayas' for its dramatic pointed shape and hanging glacier, considered one of the most beautiful mountains on Earth.","fc":"1961, Mike Gill, Barry Bishop, Wally Romanes and Mike Ward"},
    {"n":"Nanda Devi","co":"India","ra":"Himalaya","el":7816,"fa":"Long the highest peak within the borders of British India; a surrounding sanctuary of peaks was considered so sacred and remote that it was closed to climbers for decades.","fc":"1936, Bill Tilman and Noel Odell"},
    {"n":"Machapuchare","co":"Nepal","ra":"Himalaya","el":6993,"fa":"Nicknamed 'Fishtail' for its twin-pronged summit; considered sacred to the god Shiva, climbing to its true top has been forbidden by the Nepalese government since a 1957 expedition stopped short of the summit by agreement.","fc":None},
    {"n":"Mount Kailash","co":"China (Tibet)","ra":"Transhimalaya","el":6638,"fa":"Considered sacred by four religions, including Hinduism and Buddhism; out of respect for that belief, no confirmed ascent to its summit has ever been made.","fc":None},
    {"n":"Muztagh Ata","co":"China","ra":"Pamir","el":7546,"fa":"Nicknamed the 'Father of Ice Mountains'; its gentle, rounded slopes make it one of the highest peaks on Earth that can be climbed on skis.","fc":"1956, Chinese-Soviet expedition"},
    {"n":"Tirich Mir","co":"Pakistan","ra":"Hindu Kush","el":7708,"fa":"The highest peak in the Hindu Kush range and outside the Himalaya-Karakoram system; local legend held its summit was home to fairies who punished trespassers.","fc":"1950, Norwegian expedition"},
    {"n":"Ismoil Somoni Peak","co":"Tajikistan","ra":"Pamir","el":7495,"fa":"The highest point in the former Soviet Union, it was renamed several times through history, once honoring Lenin and later Communism itself before its current name.","fc":"1933, Soviet expedition"},
    {"n":"Khan Tengri","co":"Kazakhstan, Kyrgyzstan","ra":"Tian Shan","el":7010,"fa":"Its marble summit pyramid catches the low sun in a deep blood-red glow, a striking effect that inspired its nickname 'Blood Mountain'.","fc":"1931, Soviet expedition"},
    {"n":"Pobeda Peak","co":"Kyrgyzstan, China","ra":"Tian Shan","el":7439,"fa":"The northernmost peak above 7000 meters on Earth, and one of the coldest and most avalanche-prone high mountains in the world.","fc":"1956, Soviet expedition"},
    {"n":"Gongga Shan","co":"China","ra":"Daxue Mountains","el":7556,"fa":"The highest peak in Sichuan province, so remote that it was misjudged for years to rival Everest in height before accurate surveys corrected the record.","fc":"1932, Richard Burdsall and Terris Moore"},
    # ── ALPS, PYRENEES & OTHER EUROPEAN RANGES ─────────────────────────────
    {"n":"Mont Blanc","co":"France, Italy","ra":"Alps","el":4808,"fa":"Western Europe's highest peak; its first ascent is credited with sparking the modern sport of mountaineering.","fc":"1786, Jacques Balmat and Michel-Gabriel Paccard"},
    {"n":"Matterhorn","co":"Switzerland, Italy","ra":"Alps","el":4478,"fa":"One of the most photographed mountains in the world; its dramatic first ascent ended in tragedy when four climbers fell to their deaths during the descent.","fc":"1865, Edward Whymper's party"},
    {"n":"Eiger","co":"Switzerland","ra":"Alps","el":3967,"fa":"Its notorious North Face, nicknamed 'Mordwand' (murder wall), was not climbed until 1938 after claiming several climbers' lives in earlier attempts.","fc":"1858, Charles Barrington"},
    {"n":"Jungfrau","co":"Switzerland","ra":"Alps","el":4158,"fa":"Home to Europe's highest railway station, built inside the mountain and reachable by a rack railway completed in 1912.","fc":"1811, Johann Rudolf Meyer and Hieronymus Meyer"},
    {"n":"Dom","co":"Switzerland","ra":"Alps","el":4545,"fa":"The highest peak located entirely within Switzerland, since taller neighbors like the Matterhorn and Monte Rosa sit on the Italian border.","fc":"1858, John Llewelyn Davies with local guides"},
    {"n":"Weisshorn","co":"Switzerland","ra":"Alps","el":4506,"fa":"Once described by a pioneering alpinist as the most beautiful mountain in the Alps for its near-perfect pyramidal shape.","fc":"1861, John Tyndall"},
    {"n":"Piz Bernina","co":"Switzerland, Italy","ra":"Alps","el":4049,"fa":"The highest peak of the Eastern Alps and the only peak above 4000 meters outside the Western Alps.","fc":"1850, Johann Coaz"},
    {"n":"Grossglockner","co":"Austria","ra":"Alps","el":3798,"fa":"Austria's highest peak; a scenic high-alpine road built in the 1930s now winds close to its base and is one of Europe's most famous mountain drives.","fc":"1800, expedition organized by Bishop Franz Xaver von Salm-Reifferscheidt"},
    {"n":"Zugspitze","co":"Germany","ra":"Alps","el":2962,"fa":"Germany's highest peak; three countries, Germany, Austria and Switzerland, are all visible from its summit on a clear day.","fc":"1820, Josef Naus"},
    {"n":"Wetterhorn","co":"Switzerland","ra":"Alps","el":3692,"fa":"Its 1854 ascent by an English lawyer is traditionally cited as the spark that ignited the 'Golden Age of Alpinism', a wave of British enthusiasm for Alpine climbing.","fc":"1854, Alfred Wills"},
    {"n":"Aneto","co":"Spain","ra":"Pyrenees","el":3404,"fa":"The highest peak of the Pyrenees, its small summit glacier is one of the last remnants of ice still clinging to the range.","fc":"1842, Platon de Tchihatchef and Jean-Pierre Sanio"},
    {"n":"Triglav","co":"Slovenia","ra":"Julian Alps","el":2864,"fa":"Slovenia's highest peak and a national symbol, featured on the country's flag and coat of arms.","fc":"1778, four Carniolan explorers commissioned by Baron Sigmund Zois"},
    {"n":"Mont Ventoux","co":"France","ra":"Provence","el":1910,"fa":"Nicknamed the 'Giant of Provence', it is famous today as one of the most feared climbs of the Tour de France cycling race.","fc":"1336, Petrarch, described in one of the earliest known accounts of mountaineering for its own sake"},
    {"n":"Galdhopiggen","co":"Norway","ra":"Jotunheimen","el":2469,"fa":"The highest peak in Scandinavia; a small summer ski resort operates near its base even at the height of summer, using a permanent snowfield.","fc":"1850, local guide Ole Petersen Flye"},
    {"n":"Gerlachovsky stit","co":"Slovakia","ra":"Carpathians","el":2655,"fa":"The highest peak of the Carpathian mountain range and of Slovakia, standing well above the rest of the surrounding High Tatras.","fc":"1834, local guide Jakub Piaseczny"},
    {"n":"Mount Kazbek","co":"Georgia","ra":"Caucasus","el":5054,"fa":"In Georgian legend this dormant volcanic peak is where Amirani, a Prometheus-like hero, was chained by the gods for stealing fire.","fc":"1868, Douglas Freshfield's expedition"},
    {"n":"Musala","co":"Bulgaria","ra":"Rila Mountains","el":2925,"fa":"The highest peak in the Balkan Peninsula, its name is believed to derive from a Persian phrase meaning 'near God'.","fc":None},
    {"n":"Corno Grande","co":"Italy","ra":"Apennines","el":2912,"fa":"The highest peak of the Apennines, home to the southernmost glacier in continental Europe, now one of the smallest ice bodies on the continent.","fc":"1573, Francesco De Marchi"},
    {"n":"Mount Olympus","co":"Greece","ra":"Olympus Range","el":2917,"fa":"Greece's highest peak, believed in ancient mythology to be the home of the twelve Olympian gods.","fc":"1913, Christos Kakkalos with Frederick Boissonnas and Daniel Baud-Bovy"},
    {"n":"Piton des Neiges","co":"France (Reunion)","ra":"Mascarene Islands","el":3070,"fa":"The highest peak of the Indian Ocean islands, its name means 'Peak of the Snows' even though snow there is exceptionally rare.","fc":None},
    {"n":"Mount Erciyes","co":"Turkey","ra":"Central Anatolia","el":3916,"fa":"A dormant volcanic peak believed to be depicted in a roughly 8000-year-old wall painting at the Neolithic settlement of Catalhoyuk, possibly the oldest known landscape artwork.","fc":None},
    # ── NORTH AMERICA ───────────────────────────────────────────────────────
    {"n":"Denali","co":"United States","ra":"Alaska Range","el":6190,"fa":"North America's highest peak; it has one of the greatest base-to-summit rises of any mountain on Earth, towering nearly 5500 meters above its surrounding plain.","fc":"1913, Hudson Stuck's expedition"},
    {"n":"Mount Logan","co":"Canada","ra":"Saint Elias Mountains","el":5959,"fa":"Canada's highest peak has such an enormous summit plateau that its true highest point was only confirmed by GPS survey in the early 1990s.","fc":"1925, Albert MacCarthy's expedition"},
    {"n":"Mount Robson","co":"Canada","ra":"Canadian Rockies","el":3954,"fa":"The highest peak in the Canadian Rockies, often shrouded in its own weather system and cloud cap even on clear days.","fc":"1913, William Foster, Curly Phillips and Conrad Kain"},
    {"n":"Mount Waddington","co":"Canada","ra":"Coast Mountains","el":4019,"fa":"The highest peak entirely within British Columbia, it went unclimbed for years after being nicknamed 'Mystery Mountain' by early surveyors.","fc":"1936, Fritz Wiessner and William P. House"},
    {"n":"Mount Assiniboine","co":"Canada","ra":"Canadian Rockies","el":3618,"fa":"Nicknamed the 'Matterhorn of the Rockies' for its strikingly similar pyramidal shape to its famous Swiss counterpart.","fc":"1901, James Outram"},
    {"n":"Grand Teton","co":"United States","ra":"Teton Range","el":4199,"fa":"Rises dramatically straight from the valley floor with no foothills, giving it one of the most striking silhouettes of any peak in the United States.","fc":"1898, William Owen, Franklin Spalding, Frank Petersen and John Shive"},
    {"n":"Longs Peak","co":"United States","ra":"Rocky Mountains","el":4346,"fa":"The highest point in Rocky Mountain National Park, its sheer east face called 'The Diamond' is one of the most celebrated big-wall climbs in the US.","fc":"1868, John Wesley Powell's expedition"},
    {"n":"Mount Whitney","co":"United States","ra":"Sierra Nevada","el":4421,"fa":"The highest peak in the contiguous United States; remarkably, it lies only about 136 km from Badwater Basin, the lowest point in North America.","fc":"1873, Charles Begole, A.H. Johnson and John Lucas"},
    {"n":"Half Dome","co":"United States","ra":"Sierra Nevada","el":2694,"fa":"This granite landmark in Yosemite Valley was long declared unclimbable until a blacksmith rigged an eyebolt ladder up its final smooth slope.","fc":"1875, George G. Anderson"},
    {"n":"Pikes Peak","co":"United States","ra":"Rocky Mountains","el":4302,"fa":"The view from its summit inspired the lyrics to 'America the Beautiful'; a cog railway has carried visitors to the top since 1891.","fc":"1820, Edwin James"},
    {"n":"Mauna Kea","co":"United States","ra":"Hawaiian Islands","el":4207,"fa":"Measured from its base on the ocean floor, it is the tallest mountain on Earth at over 10000 meters, taller than Everest, though most of it lies underwater.","fc":None},
    {"n":"Mount Katahdin","co":"United States","ra":"Appalachian Mountains","el":1606,"fa":"Marks the northern terminus of the Appalachian Trail; its Native Penobscot name means 'Greatest Mountain'.","fc":"1804, Charles Turner Jr., the first recorded non-native ascent"},
    {"n":"Mount Mitchell","co":"United States","ra":"Appalachian Mountains","el":2037,"fa":"The highest peak east of the Mississippi River is named after a scientist who died in a fall while trying to prove it was the tallest in the region.","fc":None},
    {"n":"Mount Marcy","co":"United States","ra":"Adirondack Mountains","el":1629,"fa":"New York State's highest peak; a small pond just below its summit is considered the highest source of the Hudson River.","fc":"1837, surveying expedition led by Ebenezer Emmons"},
    # ── SOUTH AMERICA ───────────────────────────────────────────────────────
    {"n":"Aconcagua","co":"Argentina","ra":"Andes","el":6961,"fa":"The highest peak outside Asia, making it one of the celebrated Seven Summits, one for each continent.","fc":"1897, Matthias Zurbriggen"},
    {"n":"Chimborazo","co":"Ecuador","ra":"Andes","el":6263,"fa":"Because Earth bulges at the equator, its summit is the point on our planet's surface farthest from the planet's center, farther than even Everest.","fc":"1880, Edward Whymper, Jean-Antoine Carrel and Louis Carrel"},
    {"n":"Huascaran","co":"Peru","ra":"Andes","el":6768,"fa":"Peru's highest peak; a catastrophic avalanche from its slopes in 1970 buried the town of Yungay below, one of the deadliest mountain disasters in history.","fc":"1932, German-Austrian expedition"},
    {"n":"Fitz Roy","co":"Argentina, Chile","ra":"Patagonian Andes","el":3405,"fa":"Its jagged granite spire is so distinctive that its silhouette became the logo of an outdoor clothing brand.","fc":"1952, Lionel Terray and Guido Magnone"},
    {"n":"Cerro Torre","co":"Argentina, Chile","ra":"Patagonian Andes","el":3128,"fa":"For decades a disputed 1959 summit claim was debated by climbers, until a widely accepted first true ascent was finally made 15 years later.","fc":"1974, Ragni di Lecco expedition"},
    {"n":"Nevado Sajama","co":"Bolivia","ra":"Andes","el":6542,"fa":"Bolivia's highest peak, an extinct volcanic cone surrounded by the world's highest forest, made up of hardy Polylepis trees growing above 4000 meters.","fc":"1939, Joseph Prem, H. Awerzger and F. Kutschera"},
    {"n":"Pico Bolivar","co":"Venezuela","ra":"Andes","el":4978,"fa":"Venezuela's highest peak carries a bronze bust of Simon Bolivar at its summit, hauled up piece by piece and installed in 1951.","fc":"1935, expedition led by Enrique Bourgoin"},
    {"n":"Mount Roraima","co":"Venezuela, Brazil, Guyana","ra":"Guiana Highlands","el":2810,"fa":"This flat-topped tepui with sheer cliffs on all sides inspired Arthur Conan Doyle's novel 'The Lost World' about a plateau where prehistoric creatures survived.","fc":"1884, Everard im Thurn's expedition"},
    {"n":"Cerro Chirripo","co":"Costa Rica","ra":"Talamanca Range","el":3820,"fa":"Costa Rica's highest peak; on an exceptionally clear day, both the Pacific Ocean and the Caribbean Sea can reportedly be seen from its summit.","fc":None},
    # ── AFRICA ──────────────────────────────────────────────────────────────
    {"n":"Kilimanjaro","co":"Tanzania","ra":"East African Rift","el":5895,"fa":"Africa's highest peak and the world's tallest free-standing mountain, rising alone from surrounding plains rather than as part of a mountain range.","fc":"1889, Hans Meyer and Ludwig Purtscheller"},
    {"n":"Mount Kenya","co":"Kenya","ra":"East African Rift","el":5199,"fa":"Despite sitting almost exactly on the equator, its higher peaks still carry glaciers, though they have shrunk dramatically in the past century.","fc":"1899, Halford Mackinder's expedition"},
    {"n":"Mount Stanley","co":"DR Congo, Uganda","ra":"Rwenzori Mountains","el":5109,"fa":"Its glacier-capped summit, Margherita Peak, sits almost on the equator in one of Africa's rainiest and most persistently cloud-covered ranges.","fc":"1906, Duke of the Abruzzi's expedition"},
    {"n":"Table Mountain","co":"South Africa","ra":"Cape Fold Belt","el":1085,"fa":"Its famously flat summit plateau is often capped by a cloud formation locals call the 'tablecloth' when moist air spills over its edge.","fc":"1503, Antonio de Saldanha, the earliest recorded ascent"},
    {"n":"Ras Dashen","co":"Ethiopia","ra":"Simien Mountains","el":4550,"fa":"Ethiopia's highest peak sits within a range so rugged early European explorers nicknamed it the 'Africa's Grand Canyon', home to rare wildlife like the gelada monkey.","fc":None},
    # ── OCEANIA & ANTARCTICA ────────────────────────────────────────────────
    {"n":"Puncak Jaya","co":"Indonesia","ra":"Sudirman Range","el":4884,"fa":"The highest island peak in the world and, remarkably, still carries small equatorial glaciers, though they are rapidly disappearing.","fc":"1962, Heinrich Harrer's expedition"},
    {"n":"Aoraki / Mount Cook","co":"New Zealand","ra":"Southern Alps","el":3724,"fa":"New Zealand's highest peak, sacred to the Maori as an ancestor figure; a rockfall and ice avalanche shortened its summit by several meters in 1991.","fc":"1894, Tom Fyfe, James Clarke and George Graham"},
    {"n":"Mount Taranaki","co":"New Zealand","ra":"Taranaki","el":2518,"fa":"This near-perfectly symmetrical volcanic cone so closely resembles Mount Fuji that filmmakers have used it as a stand-in for the Japanese peak.","fc":"1839, John Carne Bidwill"},
    {"n":"Mount Kosciuszko","co":"Australia","ra":"Snowy Mountains","el":2228,"fa":"Mainland Australia's highest peak is also one of the easiest to reach among the world's continental high points, with a walking track leading close to its summit.","fc":"1840, Paul Edmund Strzelecki"},
    {"n":"Mount Wilhelm","co":"Papua New Guinea","ra":"Bismarck Range","el":4509,"fa":"The highest peak in Papua New Guinea, occasionally dusted with frost despite lying just a few degrees south of the equator.","fc":"1938, Christian Keysser"},
    {"n":"Vinson Massif","co":"Antarctica","ra":"Sentinel Range","el":4892,"fa":"Antarctica's highest peak was not even discovered until aerial surveys in 1958, and remained unclimbed for another eight years after that.","fc":"1966, Nicholas Clinch's American expedition"},
    # ── OTHERS ──────────────────────────────────────────────────────────────
    {"n":"Mount Elbrus","co":"Russia","ra":"Caucasus","el":5642,"fa":"Europe's highest peak is a dormant volcano with twin summits; it is counted among the Seven Summits under the common definition of Europe's borders.","fc":"1829, Killar Khashirov, first recorded ascent of the east summit"},
    {"n":"Ben Nevis","co":"United Kingdom","ra":"Grampian Mountains","el":1345,"fa":"The highest peak in the British Isles; a former observatory once staffed year-round near its summit recorded some of Britain's most extreme weather.","fc":"1771, James Robertson"},
    {"n":"Mount Kinabalu","co":"Malaysia","ra":"Crocker Range","el":4095,"fa":"The highest peak between the Himalayas and New Guinea, home to thousands of plant species found nowhere else on Earth.","fc":"1851, Hugh Low"},
    {"n":"Pico de Orizaba","co":"Mexico","ra":"Trans-Mexican Volcanic Belt","el":5636,"fa":"Mexico's highest peak and North America's third-highest; its glacier-capped, near-symmetrical cone was once used as a navigational landmark by sailors far out in the Gulf of Mexico.","fc":"1848, F. Maynard and C. Reavis"},
    {"n":"Mount Sinai","co":"Egypt","ra":"Sinai Peninsula","el":2285,"fa":"Revered in Jewish, Christian and Islamic tradition as the mountain where Moses received the Ten Commandments; a monastery has stood at its base since the 6th century.","fc":None},
]

HEADERS = {"User-Agent": "projet_app_annecdote/1.0 (daily-facts educational app; github.com/uzan)"}

WIKI_TITLE_OVERRIDES = {
    "Mount Stanley":       "Mount Stanley",
    "Mount Kenya":         "Mount Kenya",
    "Ben Nevis":           "Ben Nevis",
    "Longs Peak":          "Longs Peak",
    "Half Dome":           "Half Dome",
    "Dom":                 "Dom (mountain)",
    "Musala":              "Musala",
    "Gerlachovsky stit":   "Gerlachovsky stit",
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
    os.path.join(os.path.dirname(__file__), "../../assets/world/mountains.json")
)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

existing_images = {}
if os.path.exists(output_path):
    with open(output_path, encoding="utf-8") as f:
        for entry in json.load(f):
            if entry.get("im"):
                existing_images[entry["n"]] = entry["im"]
    print(f"Loaded {len(existing_images)} existing images from cache.\n")

missing = sum(1 for m in MOUNTAINS_RAW if not existing_images.get(m["n"]))
print(f"{missing} mountain(s) need image fetching.\n")
fetch_idx = 0
mountains = []
for i, m in enumerate(MOUNTAINS_RAW, 1):
    name = m["n"]
    if existing_images.get(name):
        im = existing_images[name]
        print(f"[{i:2}/{len(MOUNTAINS_RAW)}] {name} (cached)")
    else:
        fetch_idx += 1
        print(f"[{i:2}/{len(MOUNTAINS_RAW)}] Fetching image for {name} ...")
        im = fetch_wiki_image(name)
        if im is None:
            im = fetch_commons_image(f"{name} mountain")
            if im:
                print("  [commons] found")
        if im:
            print(f"  found: {im[:90]}")
        if fetch_idx < missing:
            time.sleep(1.2)
    mountains.append({**m, "im": im})

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(mountains, f, ensure_ascii=False, separators=(",", ":"))

fetched = sum(1 for m in mountains if m["im"])
print(f"\nDone -- {len(mountains)} mountains, {fetched} with images -> {output_path}")
