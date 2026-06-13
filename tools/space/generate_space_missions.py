import json, requests, time

# n=name, ag=agency, ds=destination, la=launch_year, du=duration,
# st=status(Success/Failure/Ongoing/Partial), fa=famous_for, im=image_url

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_OVERRIDES = {
    "Sputnik 1": "Sputnik 1",
    "Vostok 1": "Vostok 1",
    "Apollo 13": "Apollo 13",
    "Voyager 1": "Voyager 1",
    "Voyager 2": "Voyager 2",
    "Hubble Space Telescope": "Hubble Space Telescope",
    "James Webb Space Telescope": "James Webb Space Telescope",
    "International Space Station": "International Space Station",
    "Challenger STS-51-L": "Space Shuttle Challenger disaster",
    "Columbia STS-107": "Space Shuttle Columbia disaster",
    "Tiangong-3": "Tiangong space station",
    "SpaceX Crew Dragon Demo-2": "Crew Dragon Demo-2",
    "Phoenix": "Phoenix (spacecraft)",
    "Artemis I": "Artemis 1",
    "JWST First Images": "James Webb Space Telescope",
    "Chandrayaan-3": "Chandrayaan-3",
}

missions_raw = [
    # ── PREMIERS PAS DANS L'ESPACE ────────────────────────────────────────
    {"n":"Sputnik 1","ag":"Soviet Union","ds":"Earth orbit","la":1957,"du":"92 days","st":"Success","fa":"First artificial satellite ever launched, triggering the Space Race and proving orbital mechanics"},
    {"n":"Explorer 1","ag":"NASA","ds":"Earth orbit","la":1958,"du":"12 years","st":"Success","fa":"First US satellite; discovered the Van Allen radiation belts surrounding Earth"},
    {"n":"Vostok 1","ag":"Soviet Union","ds":"Earth orbit","la":1961,"du":"108 minutes","st":"Success","fa":"Yuri Gagarin became the first human in space, completing one orbit around Earth"},
    {"n":"Mercury-Atlas 6 (Friendship 7)","ag":"NASA","ds":"Earth orbit","la":1962,"du":"4h 55m","st":"Success","fa":"John Glenn became the first American to orbit Earth, completing three orbits"},
    {"n":"Voskhod 2","ag":"Soviet Union","ds":"Earth orbit","la":1965,"du":"26 hours","st":"Success","fa":"Alexei Leonov performed the first spacewalk in history, floating in space for 12 minutes"},
    {"n":"Apollo 8","ag":"NASA","ds":"Moon","la":1968,"du":"6 days","st":"Success","fa":"First crewed mission to orbit the Moon; the iconic Earthrise photograph was taken during this mission"},
    {"n":"Apollo 11","ag":"NASA","ds":"Moon","la":1969,"du":"8 days","st":"Success","fa":"Neil Armstrong and Buzz Aldrin became the first humans to walk on the Moon on July 20, 1969"},
    {"n":"Apollo 13","ag":"NASA","ds":"Moon (aborted)","la":1970,"du":"6 days","st":"Partial","fa":"Oxygen tank explosion forced the crew to use the lunar module as a lifeboat — called a 'successful failure'"},
    {"n":"Apollo 17","ag":"NASA","ds":"Moon","la":1972,"du":"12 days","st":"Success","fa":"Last crewed Moon landing; astronauts collected a record 110 kg of lunar samples"},
    {"n":"Luna 9","ag":"Soviet Union","ds":"Moon","la":1966,"du":"3 days","st":"Success","fa":"First spacecraft to achieve a soft landing on the Moon and transmit photos from the lunar surface"},
    {"n":"Luna 16","ag":"Soviet Union","ds":"Moon","la":1970,"du":"11 days","st":"Success","fa":"First robotic mission to collect and return lunar samples to Earth automatically"},
    # ── SYSTÈME SOLAIRE INTÉRIEUR ─────────────────────────────────────────
    {"n":"Mariner 4","ag":"NASA","ds":"Mars","la":1964,"du":"8 months","st":"Success","fa":"First spacecraft to provide close-up images of Mars, revealing a cratered, Moon-like surface"},
    {"n":"Viking 1","ag":"NASA","ds":"Mars","la":1975,"du":"6 years","st":"Success","fa":"First spacecraft to successfully land on Mars; conducted the first biology experiments on another planet"},
    {"n":"Mars Pathfinder","ag":"NASA","ds":"Mars","la":1996,"du":"83 days","st":"Success","fa":"Delivered Sojourner, the first Mars rover; demonstrated airbag landing system now used by future missions"},
    {"n":"Mars Global Surveyor","ag":"NASA","ds":"Mars","la":1996,"du":"9 years","st":"Success","fa":"Mapped the entire Martian surface and discovered evidence of past water flow and a weak magnetic field"},
    {"n":"Spirit","ag":"NASA","ds":"Mars","la":2003,"du":"6 years","st":"Success","fa":"Designed for 90 days, operated for 6 years; discovered silica deposits indicating past presence of water"},
    {"n":"Opportunity","ag":"NASA","ds":"Mars","la":2003,"du":"15 years","st":"Success","fa":"Designed for 90 days, operated 15 years — the longest-running Mars rover; found clear evidence of ancient water"},
    {"n":"Mars Reconnaissance Orbiter","ag":"NASA","ds":"Mars","la":2005,"du":"Ongoing","st":"Ongoing","fa":"Highest-resolution Mars camera ever; found evidence of seasonal liquid water flows on Martian slopes"},
    {"n":"Phoenix","ag":"NASA","ds":"Mars","la":2007,"du":"5 months","st":"Success","fa":"First mission to directly confirm water ice near the Martian north pole by digging into the soil"},
    {"n":"Curiosity","ag":"NASA","ds":"Mars","la":2011,"du":"Ongoing","st":"Ongoing","fa":"Still operational after 13+ years; confirmed Mars once had conditions suitable for microbial life"},
    {"n":"MAVEN","ag":"NASA","ds":"Mars","la":2013,"du":"Ongoing","st":"Ongoing","fa":"Revealed that solar wind stripped away Mars's ancient atmosphere, explaining how it lost its oceans"},
    {"n":"InSight","ag":"NASA","ds":"Mars","la":2018,"du":"4 years","st":"Success","fa":"Detected over 1,300 marsquakes and measured Mars's internal structure for the first time"},
    {"n":"Perseverance","ag":"NASA","ds":"Mars","la":2020,"du":"Ongoing","st":"Ongoing","fa":"Collected rock samples for future Earth return; deployed Ingenuity helicopter — first powered flight on another planet"},
    {"n":"Mars Climate Orbiter","ag":"NASA","ds":"Mars","la":1998,"du":"9 months","st":"Failure","fa":"Lost due to a metric/imperial unit mismatch between teams — one of the most embarrassing NASA failures"},
    {"n":"Venera 7","ag":"Soviet Union","ds":"Venus","la":1970,"du":"35 minutes","st":"Success","fa":"First spacecraft to successfully land on another planet and transmit data from the surface of Venus"},
    {"n":"Magellan","ag":"NASA","ds":"Venus","la":1989,"du":"4 years","st":"Success","fa":"Mapped 98% of Venus's surface using radar, revealing thousands of volcanoes and lava plains"},
    {"n":"Mariner 10","ag":"NASA","ds":"Mercury & Venus","la":1973,"du":"1 year","st":"Success","fa":"First spacecraft to visit two planets in one mission; photographed 45% of Mercury's surface"},
    {"n":"MESSENGER","ag":"NASA","ds":"Mercury","la":2004,"du":"11 years","st":"Success","fa":"First spacecraft to orbit Mercury; found water ice in permanently shadowed polar craters"},
    {"n":"Parker Solar Probe","ag":"NASA","ds":"Sun","la":2018,"du":"Ongoing","st":"Ongoing","fa":"The fastest human-made object ever (692,000 km/h); has flown through the Sun's corona"},
    {"n":"SOHO","ag":"ESA/NASA","ds":"Sun","la":1995,"du":"Ongoing","st":"Ongoing","fa":"Has been observing the Sun for 30 years; discovered over 4,000 comets as a side mission"},
    # ── SYSTÈME SOLAIRE EXTÉRIEUR ─────────────────────────────────────────
    {"n":"Voyager 1","ag":"NASA","ds":"Interstellar space","la":1977,"du":"Ongoing","st":"Ongoing","fa":"The farthest human-made object from Earth; first to enter interstellar space in 2012, still transmitting"},
    {"n":"Voyager 2","ag":"NASA","ds":"Interstellar space","la":1977,"du":"Ongoing","st":"Ongoing","fa":"Only spacecraft to fly past all four outer planets; still operational in interstellar space"},
    {"n":"Pioneer 10","ag":"NASA","ds":"Jupiter / beyond","la":1972,"du":"31 years","st":"Success","fa":"First spacecraft to pass through the asteroid belt and fly by Jupiter; carried the Pioneer plaque"},
    {"n":"Galileo","ag":"NASA","ds":"Jupiter","la":1989,"du":"14 years","st":"Success","fa":"Discovered strong evidence for a liquid water ocean beneath Europa's icy crust"},
    {"n":"Cassini-Huygens","ag":"NASA/ESA","ds":"Saturn","la":1997,"du":"20 years","st":"Success","fa":"13 years orbiting Saturn; Huygens probe landed on Titan, discovering methane lakes and hydrocarbon rain"},
    {"n":"Juno","ag":"NASA","ds":"Jupiter","la":2011,"du":"Ongoing","st":"Ongoing","fa":"Orbiting Jupiter's poles, revealing its complex atmospheric structure and massive polar cyclones"},
    {"n":"New Horizons","ag":"NASA","ds":"Pluto / Kuiper Belt","la":2006,"du":"Ongoing","st":"Ongoing","fa":"First mission to fly by Pluto (2015), revealing a heart-shaped glacier and complex geology"},
    {"n":"Huygens probe","ag":"ESA","ds":"Titan (Saturn moon)","la":1997,"du":"72 minutes on surface","st":"Success","fa":"First landing in the outer solar system; transmitted images of a methane lake shoreline on Titan"},
    # ── ASTÉROÏDES ET COMÈTES ─────────────────────────────────────────────
    {"n":"Rosetta / Philae","ag":"ESA","ds":"Comet 67P","la":2004,"du":"12 years","st":"Success","fa":"First mission to orbit a comet; Philae lander became the first to land on a comet nucleus in 2014"},
    {"n":"Deep Impact","ag":"NASA","ds":"Comet Tempel 1","la":2005,"du":"6 months","st":"Success","fa":"Deliberately crashed an impactor into a comet to study its composition — caused a huge explosion"},
    {"n":"Hayabusa","ag":"JAXA","ds":"Asteroid Itokawa","la":2003,"du":"7 years","st":"Partial","fa":"First mission to return samples from an asteroid; suffered multiple failures but still returned 1,500 grains"},
    {"n":"Hayabusa2","ag":"JAXA","ds":"Asteroid Ryugu","la":2014,"du":"6 years","st":"Success","fa":"Collected samples from beneath Ryugu's surface and returned them to Earth in 2020"},
    {"n":"OSIRIS-REx","ag":"NASA","ds":"Asteroid Bennu","la":2016,"du":"Ongoing","st":"Success","fa":"Collected a record 250g sample from asteroid Bennu and returned it to Earth in 2023"},
    {"n":"DART","ag":"NASA","ds":"Asteroid Dimorphos","la":2021,"du":"10 months","st":"Success","fa":"First planetary defense mission; deliberately crashed into Dimorphos and successfully changed its orbit"},
    # ── TÉLESCOPES SPATIAUX ───────────────────────────────────────────────
    {"n":"Hubble Space Telescope","ag":"NASA/ESA","ds":"Earth orbit","la":1990,"du":"Ongoing","st":"Ongoing","fa":"Revolutionized astronomy over 35 years; determined the universe's expansion rate and age (~13.8 billion years)"},
    {"n":"James Webb Space Telescope","ag":"NASA/ESA/CSA","ds":"L2 point","la":2021,"du":"Ongoing","st":"Ongoing","fa":"Most powerful space telescope ever built; can observe the first galaxies formed after the Big Bang"},
    {"n":"Kepler Space Telescope","ag":"NASA","ds":"Earth-trailing orbit","la":2009,"du":"9 years","st":"Success","fa":"Discovered over 2,600 confirmed exoplanets, revolutionizing our understanding of planetary systems"},
    {"n":"Spitzer Space Telescope","ag":"NASA","ds":"Earth-trailing orbit","la":2003,"du":"16 years","st":"Success","fa":"Infrared telescope that revealed the first light spectrum of exoplanet atmospheres"},
    {"n":"Chandra X-ray Observatory","ag":"NASA","ds":"Earth orbit","la":1999,"du":"Ongoing","st":"Ongoing","fa":"Observes X-rays from black holes, neutron stars and supernova remnants invisible to optical telescopes"},
    {"n":"TESS","ag":"NASA","ds":"HEO orbit","la":2018,"du":"Ongoing","st":"Ongoing","fa":"Searching the entire sky for exoplanets orbiting nearby bright stars; found over 5,000 candidates"},
    # ── STATIONS SPATIALES ────────────────────────────────────────────────
    {"n":"Mir","ag":"Soviet Union / Russia","ds":"Earth orbit","la":1986,"du":"15 years","st":"Success","fa":"First modular space station; hosted international cosmonauts and proved long-duration human spaceflight"},
    {"n":"International Space Station","ag":"NASA/Roscosmos/ESA/JAXA/CSA","ds":"Earth orbit","la":1998,"du":"Ongoing","st":"Ongoing","fa":"Largest structure ever assembled in space; continuously inhabited since November 2000 by 270+ astronauts"},
    {"n":"Tiangong-3","ag":"CNSA","ds":"Earth orbit","la":2021,"du":"Ongoing","st":"Ongoing","fa":"China's permanent space station; completed and operational by 2022 as China's independent orbital outpost"},
    # ── MISSIONS COMMERCIALES ET NOUVELLES GÉNÉRATIONS ────────────────────
    {"n":"SpaceX Crew Dragon Demo-2","ag":"NASA/SpaceX","ds":"ISS","la":2020,"du":"64 days","st":"Success","fa":"First crewed commercial spacecraft to reach the ISS; ended US dependence on Russian Soyuz for astronaut transport"},
    {"n":"Artemis I","ag":"NASA","ds":"Moon","la":2022,"du":"25 days","st":"Success","fa":"First uncrewed test of the Orion capsule around the Moon, paving the way for the return of humans to the Moon"},
    {"n":"JWST First Images","ag":"NASA/ESA/CSA","ds":"L2 point","la":2022,"du":"Ongoing","st":"Ongoing","fa":"Released the deepest infrared image of the universe ever taken — showing galaxies formed 13 billion years ago"},
    {"n":"Chandrayaan-3","ag":"ISRO","ds":"Moon south pole","la":2023,"du":"14 days","st":"Success","fa":"India became the first country to land near the lunar south pole and 4th nation to land on the Moon"},
    {"n":"BepiColombo","ag":"ESA/JAXA","ds":"Mercury","la":2018,"du":"Ongoing","st":"Ongoing","fa":"Joint ESA-JAXA mission to Mercury using gravity assists from Venus and Mercury; arrival expected 2025"},
    {"n":"Europa Clipper","ag":"NASA","ds":"Jupiter / Europa","la":2024,"du":"Ongoing","st":"Ongoing","fa":"Will perform 49 close flybys of Europa to assess whether its subsurface ocean could support life"},
    {"n":"Dragonfly","ag":"NASA","ds":"Titan","la":2028,"du":"Planned","st":"Ongoing","fa":"Rotorcraft lander that will fly to dozens of sites on Titan to search for chemical life signatures"},
    {"n":"Lunar Gateway","ag":"NASA/ESA/JAXA/CSA","ds":"Moon orbit","la":2025,"du":"Planned","st":"Ongoing","fa":"First permanent space station in lunar orbit; will serve as staging point for Moon and Mars missions"},
    # ── ÉCHECS NOTABLES ───────────────────────────────────────────────────
    {"n":"Challenger STS-51-L","ag":"NASA","ds":"Earth orbit","la":1986,"du":"73 seconds","st":"Failure","fa":"Broke apart 73 seconds after launch due to O-ring failure; all 7 crew members were lost"},
    {"n":"Columbia STS-107","ag":"NASA","ds":"Earth orbit","la":2003,"du":"16 days","st":"Failure","fa":"Disintegrated on re-entry due to foam damage on the wing; all 7 astronauts were lost"},
    {"n":"Mars Polar Lander","ag":"NASA","ds":"Mars","la":1999,"du":"N/A","st":"Failure","fa":"Contact lost during landing; a software error likely caused premature engine shutdown before touchdown"},
]

def fetch_wikipedia_image(name):
    wiki_title = WIKI_OVERRIDES.get(name, name)
    try:
        r = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={"action":"query","titles":wiki_title,"prop":"pageimages",
                    "format":"json","pithumbsize":500,"redirects":1},
            headers=HEADERS, timeout=8
        )
        if r.status_code != 200:
            return None
        for page in r.json().get("query",{}).get("pages",{}).values():
            src = page.get("thumbnail",{}).get("source")
            if src:
                return src
        return None
    except Exception:
        return None

print(f"Fetching images for {len(missions_raw)} missions...")
result = []
for i, m in enumerate(missions_raw):
    img = fetch_wikipedia_image(m["n"])
    m["im"] = img
    result.append(m)
    status = "ok" if img else "x"
    print(f"  [{i+1}/{len(missions_raw)}] {status} {m['n']}")
    time.sleep(0.25)

import os
os.makedirs("assets/space", exist_ok=True)
with open("assets/space/missions.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, separators=(',',':'))

found = sum(1 for m in result if m["im"])
print(f"\n{len(result)} missions generees. Images: {found}/{len(result)}.")
