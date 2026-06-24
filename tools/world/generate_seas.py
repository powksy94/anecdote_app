import json, requests, time, os, sys
sys.stdout.reconfigure(encoding="utf-8")

# n=name, lo=location/region, ar=area(km2), oc=parent ocean / basin,
# fa=famousFor, im=wikipedia_image_url (None if not found)
# Scope: named seas only (no gulfs, bays, straits, or the 5 oceans themselves).

SEAS_RAW = [
    {"n":"Mediterranean Sea","lo":"Between Europe, Africa and Asia","ar":2500000,"oc":"Atlantic Ocean","fa":"The cradle of Western civilization — Egyptian, Phoenician, Greek and Roman fleets all sailed its waters; it is slowly shrinking as Africa drifts into Europe."},
    {"n":"Caribbean Sea","lo":"Between Central and South America","ar":2750000,"oc":"Atlantic Ocean","fa":"Home to the world's second-largest barrier reef system; pirates once used its thousands of islands and cays to hide from naval patrols for over two centuries."},
    {"n":"Red Sea","lo":"Between Africa and Arabia","ar":438000,"oc":"Indian Ocean","fa":"One of the saltiest seas on Earth and a hotspot of coral biodiversity; Egyptian tradition holds it as the sea parted by Moses in the biblical Exodus."},
    {"n":"Black Sea","lo":"Between Europe and Asia (Anatolia)","ar":436000,"oc":"Atlantic Ocean (via Mediterranean)","fa":"Its deep waters below 150 m are almost entirely oxygen-free, preserving ancient shipwrecks — including a complete 2,400-year-old Greek trading vessel found intact in 2018."},
    {"n":"Caspian Sea","lo":"Between Europe and Asia","ar":371000,"oc":"Endorheic (no outlet)","fa":"The largest enclosed body of water on Earth, bigger than Japan; despite its name and salinity it is technically the world's largest lake, with no connection to any ocean."},
    {"n":"Dead Sea","lo":"Between Israel, Jordan and the West Bank","ar":605,"oc":"Endorheic (no outlet)","fa":"The lowest point on Earth's land surface and one of the saltiest bodies of water on the planet; its density lets swimmers float effortlessly on the surface."},
    {"n":"Baltic Sea","lo":"Northern Europe","ar":377000,"oc":"Atlantic Ocean","fa":"One of the least salty seas on Earth thanks to heavy river inflow and a narrow connection to the ocean; its cold, low-oxygen depths preserve shipwrecks remarkably well."},
    {"n":"North Sea","lo":"Between Britain and continental Europe","ar":570000,"oc":"Atlantic Ocean","fa":"Beneath its waters lie some of Europe's richest oil and gas fields, discovered in the 1960s; it has also swallowed entire medieval towns lost to flooding."},
    {"n":"Sea of Japan","lo":"Between Japan, Korea and Russia","ar":978000,"oc":"Pacific Ocean","fa":"Known as the East Sea in Korea, its name remains an unresolved diplomatic dispute between Japan and Korea; it reaches depths of over 3,700 m despite being nearly enclosed by land."},
    {"n":"Yellow Sea","lo":"Between China and the Korean Peninsula","ar":380000,"oc":"Pacific Ocean","fa":"Named for the pale silt carried into it by the Yellow River, which can tint the water for kilometers offshore; it is one of the shallowest seas in the world."},
    {"n":"East China Sea","lo":"Between China, Taiwan and Japan","ar":1249000,"oc":"Pacific Ocean","fa":"One of the world's busiest shipping regions and a site of ongoing territorial disputes over the uninhabited Senkaku/Diaoyu Islands."},
    {"n":"South China Sea","lo":"Southeast Asia","ar":3500000,"oc":"Pacific Ocean","fa":"One of the most contested bodies of water on Earth, claimed in part by six different countries; over a third of global shipping passes through it each year."},
    {"n":"Coral Sea","lo":"Northeast of Australia","ar":4791000,"oc":"Pacific Ocean","fa":"Home to the Great Barrier Reef and site of the 1942 Battle of the Coral Sea, the first naval battle fought primarily by aircraft rather than ships."},
    {"n":"Tasman Sea","lo":"Between Australia and New Zealand","ar":2300000,"oc":"Pacific Ocean","fa":"Nicknamed 'The Ditch' by Australians and New Zealanders; Dutch explorer Abel Tasman was blown across it by storms in 1642 without ever realizing he'd found a new sea route."},
    {"n":"Arabian Sea","lo":"Northwest Indian Ocean","ar":3862000,"oc":"Indian Ocean","fa":"One of the ancient world's great trade highways, linking Rome, Persia, India and East Africa via the monsoon winds that reverse direction twice a year."},
    {"n":"Bering Sea","lo":"Between Russia and Alaska","ar":2261000,"oc":"Pacific Ocean","fa":"Crossed during the last Ice Age via the Bering land bridge, by which humans are believed to have first migrated into the Americas."},
    {"n":"Sargasso Sea","lo":"North Atlantic Ocean","ar":3500000,"oc":"Atlantic Ocean","fa":"The only sea on Earth with no land borders at all, defined entirely by ocean currents; it is named for the floating sargassum seaweed that drifts across its surface."},
    {"n":"Aral Sea","lo":"Kazakhstan and Uzbekistan","ar":8300,"oc":"Endorheic (no outlet)","fa":"Once the world's fourth-largest lake, it has shrunk by over 90% since the 1960s after Soviet irrigation projects diverted its feeder rivers — considered one of the worst environmental disasters in history."},
    {"n":"Adriatic Sea","lo":"Between Italy and the Balkans","ar":138000,"oc":"Mediterranean Sea","fa":"Venice was built on a lagoon at its northern tip specifically to use the sea as a natural defense against invaders."},
    {"n":"Aegean Sea","lo":"Between Greece and Turkey","ar":214000,"oc":"Mediterranean Sea","fa":"Scattered with over 1,400 islands, it cradled ancient Greek civilization; it is named, according to legend, after Aegeus, who drowned himself believing his son Theseus had died."},
    {"n":"Ionian Sea","lo":"Between Italy and Greece","ar":169000,"oc":"Mediterranean Sea","fa":"Contains Calypso Deep, the Mediterranean's deepest point at over 5,100 m, and the legendary route of Odysseus's wanderings in Homer's Odyssey."},
    {"n":"Tyrrhenian Sea","lo":"West of the Italian Peninsula","ar":275000,"oc":"Mediterranean Sea","fa":"Named after the Tyrrhenians, ancestors of the Etruscans; the volcanic island of Stromboli rises from its waters, erupting almost continuously for 2,000 years."},
    {"n":"Ross Sea","lo":"Antarctica (Pacific side)","ar":637000,"oc":"Southern Ocean","fa":"Home to the Ross Ice Shelf, a slab of floating ice the size of France; in 2017 it became the world's largest marine protected area."},
    {"n":"Weddell Sea","lo":"Antarctica (Atlantic side)","ar":2800000,"oc":"Southern Ocean","fa":"Contains some of the clearest seawater ever measured, with visibility exceeding 80 m; Ernest Shackleton's ship Endurance was crushed by its pack ice in 1915."},
    {"n":"Sea of Okhotsk","lo":"Between Russia and Japan","ar":1583000,"oc":"Pacific Ocean","fa":"Almost completely covered by sea ice every winter; it is one of the southernmost seas on Earth to freeze over so extensively."},
    {"n":"Andaman Sea","lo":"Between India, Myanmar and Thailand","ar":797700,"oc":"Indian Ocean","fa":"The 2004 Indian Ocean tsunami devastated its coastlines; its waters are also home to the nomadic Moken 'sea gypsies', who live almost entirely on boats."},
    {"n":"Java Sea","lo":"Between Indonesian islands","ar":433500,"oc":"Pacific Ocean","fa":"A shallow sea averaging just 40 m deep, sitting atop the Sunda Shelf — a stretch of land that was dry and walkable during the last Ice Age."},
    {"n":"Celebes Sea","lo":"Between Indonesia and the Philippines","ar":280000,"oc":"Pacific Ocean","fa":"Part of the biodiverse Coral Triangle; its deep basin hosts hydrothermal vents supporting ecosystems found almost nowhere else on Earth."},
    {"n":"Sulu Sea","lo":"Between the Philippines and Borneo","ar":260000,"oc":"Pacific Ocean","fa":"Once the stronghold of the Sulu Sultanate's seafaring traders and, for centuries, of pirate fleets that raided shipping across the southern Philippines."},
    {"n":"Timor Sea","lo":"Between Australia and Timor","ar":610000,"oc":"Indian Ocean","fa":"Beneath its seabed lie major oil and gas reserves whose ownership was disputed between Australia and Timor-Leste for decades before a 2018 maritime border treaty."},
    {"n":"Sea of Marmara","lo":"Turkey (between the Aegean and Black Sea)","ar":11350,"oc":"Mediterranean Sea (via Aegean)","fa":"The world's smallest sea connecting two larger seas; Istanbul straddles its strait approaches, making this one of the most strategically fought-over waterways in history."},
    {"n":"Sea of Azov","lo":"Between Russia and Ukraine","ar":39000,"oc":"Black Sea","fa":"The shallowest sea in the world, averaging just 7 m deep; it freezes over almost entirely most winters despite its relatively southern latitude."},
    {"n":"Norwegian Sea","lo":"Northeast Atlantic, off Norway","ar":1383000,"oc":"Atlantic Ocean","fa":"Warmed by the Gulf Stream's final stretch, it keeps Norway's coast ice-free far into the Arctic Circle, unlike other seas at the same latitude."},
    {"n":"Greenland Sea","lo":"Between Greenland and Svalbard","ar":1205000,"oc":"Arctic Ocean","fa":"One of the few places on Earth where deep-water formation occurs — surface water grows so cold and salty that it sinks straight to the ocean floor, driving global ocean circulation."},
    {"n":"Barents Sea","lo":"North of Norway and Russia","ar":1400000,"oc":"Arctic Ocean","fa":"Despite its Arctic location, the Gulf Stream keeps much of it ice-free year-round, making it one of the most productive fishing grounds in the world."},
    {"n":"Kara Sea","lo":"North of Siberia","ar":880000,"oc":"Arctic Ocean","fa":"Nicknamed the 'Ice Cellar' by Russian sailors for being ice-bound most of the year; the Soviet Union dumped Cold War-era nuclear waste, including reactors, into its waters."},
    {"n":"Beaufort Sea","lo":"North of Alaska and Canada","ar":476000,"oc":"Arctic Ocean","fa":"Among the fastest-warming marine regions on the planet; its summer sea ice has thinned dramatically over the past four decades."},
    {"n":"Labrador Sea","lo":"Between Canada and Greenland","ar":841000,"oc":"Atlantic Ocean","fa":"One of the world's key sites of deep-ocean water formation, where cold, dense surface water sinks and helps drive the global ocean conveyor belt."},
    {"n":"Philippine Sea","lo":"East of the Philippines","ar":5695000,"oc":"Pacific Ocean","fa":"Contains the Mariana Trench, the deepest point in any ocean on Earth at nearly 11,000 m — deep enough to submerge Mount Everest with room to spare."},
    {"n":"Solomon Sea","lo":"Between Papua New Guinea and the Solomon Islands","ar":720000,"oc":"Pacific Ocean","fa":"The site of fierce naval and air battles during WWII's Pacific campaign, including clashes near Guadalcanal that helped turn the tide of the war."},
    {"n":"Arafura Sea","lo":"Between Australia and New Guinea","ar":650000,"oc":"Pacific/Indian Ocean boundary","fa":"A shallow shelf sea averaging only 50 m deep; it was dry land during past ice ages, forming a bridge that early humans likely crossed to reach Australia."},
    {"n":"Ligurian Sea","lo":"Northwest Mediterranean, off Italy and France","ar":15000,"oc":"Mediterranean Sea","fa":"Borders the glamorous French and Italian Rivieras; it hosts one of the Mediterranean's few sanctuaries dedicated to protecting whales and dolphins."},
    {"n":"Irish Sea","lo":"Between Great Britain and Ireland","ar":46000,"oc":"Atlantic Ocean","fa":"Crossed by ferries for centuries, it is also where the world's first cross-channel radio transmission was sent by Marconi in 1898."},
    {"n":"White Sea","lo":"Northwest Russia","ar":90800,"oc":"Arctic Ocean (Barents Sea)","fa":"Freezes over for up to six months a year; Peter the Great built Russia's first naval shipyards on its shores, long before St. Petersburg existed."},
    {"n":"Sea of Galilee","lo":"Northern Israel","ar":166,"oc":"Endorheic (no outlet)","fa":"Despite its name, it is a freshwater lake, not a sea; the New Testament describes Jesus walking on its water and calming a storm upon it."},
    {"n":"Salton Sea","lo":"Southern California, United States","ar":650,"oc":"Endorheic (no outlet)","fa":"Created entirely by accident in 1905 when the Colorado River breached an irrigation canal and flooded the basin for two years; it is now rapidly shrinking and increasingly toxic."},
]

HEADERS = {"User-Agent": "projet_app_annecdote/1.0 (daily-facts educational app; github.com/uzan)"}

WIKI_TITLE_OVERRIDES = {
    "White Sea": "White Sea",
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
    os.path.join(os.path.dirname(__file__), "../../assets/world/seas.json")
)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

existing_images = {}
if os.path.exists(output_path):
    with open(output_path, encoding="utf-8") as f:
        for entry in json.load(f):
            if entry.get("im"):
                existing_images[entry["n"]] = entry["im"]
    print(f"Loaded {len(existing_images)} existing images from cache.\n")

missing = sum(1 for s in SEAS_RAW if not existing_images.get(s["n"]))
print(f"{missing} sea(s) need image fetching.\n")
fetch_idx = 0
seas = []
for i, s in enumerate(SEAS_RAW, 1):
    name = s["n"]
    if existing_images.get(name):
        im = existing_images[name]
        print(f"[{i:2}/{len(SEAS_RAW)}] {name} (cached)")
    else:
        fetch_idx += 1
        print(f"[{i:2}/{len(SEAS_RAW)}] Fetching image for {name} ...")
        im = fetch_wiki_image(name)
        if im is None:
            im = fetch_commons_image(f"{name}")
            if im:
                print("  [commons] found")
        if im:
            print(f"  found: {im[:90]}")
        if fetch_idx < missing:
            time.sleep(1.2)
    seas.append({**s, "im": im})

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(seas, f, ensure_ascii=False, separators=(",", ":"))

fetched = sum(1 for s in seas if s["im"])
print(f"\nDone -- {len(seas)} seas, {fetched} with images -> {output_path}")
