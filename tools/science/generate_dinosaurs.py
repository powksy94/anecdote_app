import json, requests, time

# n=name, pe=period, di=diet, le=length(m), we=weight(kg), yr=discovery_year,
# dc=describer, fa=famous_for, im=phylopic_image_url(None if not found)

dinosaurs_raw = [
    # ── CRÉTACÉ — CARNIVORES ──────────────────────────────────────────────
    {"n":"Tyrannosaurus rex","pe":"Late Cretaceous (68-66 Ma)","di":"Carnivore","le":12.0,"we":8000,"yr":1902,"dc":"Henry Fairfield Osborn","fa":"One of the largest land predators ever, with the most powerful bite force of any terrestrial animal"},
    {"n":"Spinosaurus","pe":"Late Cretaceous (99-93 Ma)","di":"Piscivore","le":14.0,"we":7400,"yr":1915,"dc":"Ernst Stromer","fa":"Longest carnivorous dinosaur known, semi-aquatic and a specialist fish hunter in North Africa"},
    {"n":"Giganotosaurus","pe":"Late Cretaceous (99-97 Ma)","di":"Carnivore","le":12.5,"we":6800,"yr":1995,"dc":"Coria & Salgado","fa":"One of the largest meat-eating dinosaurs, rivalling T. rex in size, from Patagonia, Argentina"},
    {"n":"Carcharodontosaurus","pe":"Late Cretaceous (99-94 Ma)","di":"Carnivore","le":12.0,"we":6000,"yr":1925,"dc":"Ernst Stromer","fa":"Named for its shark-like teeth, one of the apex predators of North Africa alongside Spinosaurus"},
    {"n":"Carnotaurus","pe":"Late Cretaceous (72-69 Ma)","di":"Carnivore","le":8.5,"we":1500,"yr":1985,"dc":"José Bonaparte","fa":"Unique among theropods for its two horn-like crests above its eyes and extremely short arms"},
    {"n":"Velociraptor","pe":"Late Cretaceous (75-71 Ma)","di":"Carnivore","le":2.0,"we":15,"yr":1923,"dc":"Henry Fairfield Osborn","fa":"A feathered pack hunter with a lethal retractable claw; far smaller than its Jurassic Park depiction"},
    {"n":"Deinonychus","pe":"Early Cretaceous (115-108 Ma)","di":"Carnivore","le":3.4,"we":73,"yr":1969,"dc":"John Ostrom","fa":"Its discovery revolutionized paleontology by proving dinosaurs were active, warm-blooded animals"},
    {"n":"Utahraptor","pe":"Early Cretaceous (126-125 Ma)","di":"Carnivore","le":6.0,"we":500,"yr":1993,"dc":"James Kirkland","fa":"The largest known dromaeosaurid, with a sickle claw 24 cm long — the real-size 'Jurassic Park raptor'"},
    {"n":"Troodon","pe":"Late Cretaceous (77-66 Ma)","di":"Omnivore","le":2.4,"we":50,"yr":1856,"dc":"Joseph Leidy","fa":"Had the largest brain-to-body ratio of any known dinosaur, possibly comparable to modern birds"},
    {"n":"Baryonyx","pe":"Early Cretaceous (130-125 Ma)","di":"Piscivore","le":8.5,"we":2000,"yr":1986,"dc":"Charig & Milner","fa":"Found with fish scales in its stomach — the first direct evidence of piscivory in a large theropod"},
    {"n":"Oviraptor","pe":"Late Cretaceous (75-71 Ma)","di":"Omnivore","le":1.8,"we":35,"yr":1924,"dc":"Henry Fairfield Osborn","fa":"Falsely accused of egg theft for 70 years; the eggs it was found with were actually its own"},
    {"n":"Therizinosaurus","pe":"Late Cretaceous (70-68 Ma)","di":"Herbivore","le":10.0,"we":5000,"yr":1954,"dc":"Maleev","fa":"Had the longest claws of any known animal — up to 1 metre — despite being a plant eater"},
    {"n":"Dilophosaurus","pe":"Early Jurassic (196-183 Ma)","di":"Carnivore","le":6.0,"we":400,"yr":1954,"dc":"Samuel Welles","fa":"First large theropod of the Jurassic; the twin cranial crests likely served for display or species recognition"},
    {"n":"Microraptor","pe":"Early Cretaceous (125-120 Ma)","di":"Carnivore","le":0.9,"we":1,"yr":2000,"dc":"Xu Xing","fa":"Had four wings — one pair on its arms and one on its legs — and could likely glide between trees"},
    # ── CRÉTACÉ — HERBIVORES ─────────────────────────────────────────────
    {"n":"Triceratops","pe":"Late Cretaceous (68-66 Ma)","di":"Herbivore","le":9.0,"we":12000,"yr":1889,"dc":"Othniel Charles Marsh","fa":"Its three horns and massive frill made it one of the most iconic herbivores; it co-existed with T. rex"},
    {"n":"Ankylosaurus","pe":"Late Cretaceous (68-66 Ma)","di":"Herbivore","le":9.0,"we":6000,"yr":1908,"dc":"Barnum Brown","fa":"Walking fortress: armoured from head to tail with a bone-shattering club at the end of its tail"},
    {"n":"Parasaurolophus","pe":"Late Cretaceous (76-73 Ma)","di":"Herbivore","le":10.0,"we":2500,"yr":1922,"dc":"William Arthur Parks","fa":"Its hollow tube-like crest could amplify sound to communicate across long distances through forests"},
    {"n":"Pachycephalosaurus","pe":"Late Cretaceous (70-66 Ma)","di":"Herbivore","le":4.5,"we":450,"yr":1943,"dc":"Brown & Schlaikjer","fa":"Its skull dome was up to 25 cm thick — possibly used for head-butting rivals during mating season"},
    {"n":"Maiasaura","pe":"Late Cretaceous (76-75 Ma)","di":"Herbivore","le":9.0,"we":4000,"yr":1979,"dc":"Horner & Makela","fa":"First dinosaur proven to care for its young in nests — its name means 'good mother lizard'"},
    {"n":"Styracosaurus","pe":"Late Cretaceous (75-74 Ma)","di":"Herbivore","le":5.5,"we":2700,"yr":1913,"dc":"Lawrence Lambe","fa":"Its spectacular frill bore six long spikes; one of the most ornate skull arrangements in the dinosaur world"},
    {"n":"Edmontosaurus","pe":"Late Cretaceous (73-66 Ma)","di":"Herbivore","le":13.0,"we":4000,"yr":1917,"dc":"Lawrence Lambe","fa":"One of the largest hadrosaurs, found with mummified skin preserving scale impressions and tissue"},
    {"n":"Protoceratops","pe":"Late Cretaceous (75-71 Ma)","di":"Herbivore","le":1.8,"we":180,"yr":1923,"dc":"Granger & Gregory","fa":"Found in the Gobi Desert — including the famous 'Fighting Dinosaurs' fossil locked in combat with Velociraptor"},
    {"n":"Psittacosaurus","pe":"Early Cretaceous (126-101 Ma)","di":"Herbivore","le":2.0,"we":20,"yr":1923,"dc":"Henry Fairfield Osborn","fa":"Most species-rich dinosaur genus with 11 species; fossils show quill-like structures on its tail"},
    {"n":"Iguanodon","pe":"Early Cretaceous (140-110 Ma)","di":"Herbivore","le":10.0,"we":3000,"yr":1825,"dc":"Gideon Mantell","fa":"Second dinosaur ever named; its thumb spike was initially mistaken for a horn on its nose"},
    # ── JURASSIQUE — CARNIVORES ───────────────────────────────────────────
    {"n":"Allosaurus","pe":"Late Jurassic (155-145 Ma)","di":"Carnivore","le":9.5,"we":2000,"yr":1877,"dc":"Othniel Charles Marsh","fa":"Apex predator of the Late Jurassic, hunting sauropods; may have hunted in packs like modern wolves"},
    {"n":"Ceratosaurus","pe":"Late Jurassic (153-148 Ma)","di":"Carnivore","le":7.0,"we":700,"yr":1884,"dc":"Othniel Charles Marsh","fa":"Had a prominent horn on its nose and bony ridges above each eye — unique among Jurassic theropods"},
    {"n":"Megalosaurus","pe":"Middle Jurassic (166-164 Ma)","di":"Carnivore","le":6.0,"we":700,"yr":1824,"dc":"William Buckland","fa":"First dinosaur ever formally named and described, in England in 1824 — the beginning of dinosaur science"},
    {"n":"Compsognathus","pe":"Late Jurassic (150-148 Ma)","di":"Carnivore","le":1.0,"we":2.5,"yr":1859,"dc":"Johann Wagner","fa":"Long thought to be the smallest dinosaur, about the size of a chicken; found with a lizard in its stomach"},
    {"n":"Ornitholestes","pe":"Late Jurassic (154-153 Ma)","di":"Carnivore","le":2.0,"we":12,"yr":1903,"dc":"Henry Fairfield Osborn","fa":"Small agile predator thought to have hunted early birds and lizards in the forests of the Jurassic"},
    # ── JURASSIQUE — HERBIVORES ───────────────────────────────────────────
    {"n":"Brachiosaurus","pe":"Late Jurassic (154-153 Ma)","di":"Herbivore","le":26.0,"we":56000,"yr":1903,"dc":"Elmer Riggs","fa":"One of the tallest dinosaurs with front legs longer than its back legs, reaching 13 metres in height"},
    {"n":"Brontosaurus","pe":"Late Jurassic (156-151 Ma)","di":"Herbivore","le":22.0,"we":17000,"yr":1879,"dc":"Othniel Charles Marsh","fa":"Declared invalid for 112 years before being re-validated as a distinct genus in 2015"},
    {"n":"Diplodocus","pe":"Late Jurassic (154-152 Ma)","di":"Herbivore","le":27.0,"we":14000,"yr":1878,"dc":"Othniel Charles Marsh","fa":"One of the longest dinosaurs known; it likely used its whip-like tail to produce a supersonic crack"},
    {"n":"Stegosaurus","pe":"Late Jurassic (155-150 Ma)","di":"Herbivore","le":9.0,"we":5000,"yr":1877,"dc":"Othniel Charles Marsh","fa":"The iconic double row of plates on its back may have been used for thermoregulation or display"},
    {"n":"Apatosaurus","pe":"Late Jurassic (152-151 Ma)","di":"Herbivore","le":21.0,"we":20000,"yr":1877,"dc":"Othniel Charles Marsh","fa":"Confused with Brontosaurus for a century; one of the most massive animals ever to walk on land"},
    {"n":"Camarasaurus","pe":"Late Jurassic (155-145 Ma)","di":"Herbivore","le":18.0,"we":18000,"yr":1877,"dc":"Edward Drinker Cope","fa":"Most common sauropod of the Morrison Formation; its large nasal openings suggest a keen sense of smell"},
    {"n":"Camptosaurus","pe":"Late Jurassic (155-145 Ma)","di":"Herbivore","le":7.9,"we":874,"yr":1879,"dc":"Othniel Charles Marsh","fa":"Could walk on two or four legs and was likely a key prey animal for Allosaurus"},
    # ── TRIAS ────────────────────────────────────────────────────────────
    {"n":"Eoraptor","pe":"Late Triassic (231 Ma)","di":"Omnivore","le":1.0,"we":10,"yr":1993,"dc":"Paul Sereno","fa":"One of the earliest known dinosaurs, found in Argentina — a small window into the very origin of the group"},
    {"n":"Herrerasaurus","pe":"Late Triassic (235-228 Ma)","di":"Carnivore","le":6.0,"we":350,"yr":1963,"dc":"Osvaldo Reig","fa":"Among the earliest true dinosaurs; its anatomy shows the rapid diversification at the dawn of the group"},
    {"n":"Plateosaurus","pe":"Late Triassic (214-204 Ma)","di":"Herbivore","le":10.0,"we":4000,"yr":1837,"dc":"Hermann von Meyer","fa":"One of the first large dinosaurs; found in great numbers across Europe suggesting herd behaviour"},
    {"n":"Coelophysis","pe":"Late Triassic (213-203 Ma)","di":"Carnivore","le":3.0,"we":20,"yr":1889,"dc":"Edward Drinker Cope","fa":"Found in mass graves of hundreds of individuals at Ghost Ranch, New Mexico — evidence of herding"},
    # ── GÉANTS ET RECORDS ─────────────────────────────────────────────────
    {"n":"Argentinosaurus","pe":"Late Cretaceous (96-92 Ma)","di":"Herbivore","le":35.0,"we":70000,"yr":1993,"dc":"Bonaparte & Coria","fa":"Possibly the heaviest land animal ever known, weighing up to 70 tonnes — heavier than 10 African elephants"},
    {"n":"Patagotitan","pe":"Late Cretaceous (101-98 Ma)","di":"Herbivore","le":37.0,"we":69000,"yr":2014,"dc":"Carballido et al.","fa":"The largest dinosaur whose size has been scientifically confirmed — its femur alone is 2.4 metres long"},
    {"n":"Quetzalcoatlus","pe":"Late Cretaceous (68-66 Ma)","di":"Carnivore","le":None,"we":250,"yr":1971,"dc":"Douglas Lawson","fa":"The largest flying animal ever known with a wingspan up to 11 metres — the size of a small aircraft"},
    {"n":"Spinosaurus aegyptiacus","pe":"Late Cretaceous (99-93 Ma)","di":"Piscivore","le":15.0,"we":7500,"yr":1915,"dc":"Ernst Stromer","fa":"Recent discoveries show it was primarily aquatic with dense bones for buoyancy control, unlike any other theropod"},
    # ── NOTABLES ET ORIGINAUX ─────────────────────────────────────────────
    {"n":"Archaeopteryx","pe":"Late Jurassic (150-148 Ma)","di":"Carnivore","le":0.5,"we":1,"yr":1861,"dc":"Christian Erich Hermann von Meyer","fa":"The missing link between dinosaurs and birds — it had feathers and wings but also teeth and a bony tail"},
    {"n":"Dimetrodon","pe":"Early Permian (295-272 Ma)","di":"Carnivore","le":3.0,"we":250,"yr":1878,"dc":"Edward Drinker Cope","fa":"Often mistaken for a dinosaur but actually predated them by 40 million years — closer to mammals"},
    {"n":"Irritator","pe":"Early Cretaceous (110 Ma)","di":"Piscivore","le":8.0,"we":1000,"yr":1996,"dc":"Martill et al.","fa":"Named after the irritation felt by scientists when they discovered the skull had been fraudulently altered by dealers"},
    {"n":"Dracorex hogwartsia","pe":"Late Cretaceous (66 Ma)","di":"Herbivore","le":3.0,"we":200,"yr":2006,"dc":"Robert Bakker","fa":"Named after Hogwarts from Harry Potter; its dragon-like skull with spikes inspired the school's name"},
    {"n":"Buitreraptor","pe":"Late Cretaceous (90 Ma)","di":"Carnivore","le":1.5,"we":3,"yr":2005,"dc":"Makovicky et al.","fa":"Proves dromaeosaurids originated in Gondwana and later spread north, reversing the assumed migration"},
    {"n":"Nodosaurus","pe":"Early Cretaceous (110-100 Ma)","di":"Herbivore","le":6.0,"we":1900,"yr":1889,"dc":"Othniel Charles Marsh","fa":"First ankylosaur ever discovered; its armour consisted of nodes and plates embedded directly in its skin"},
    {"n":"Sauropelta","pe":"Early Cretaceous (130-112 Ma)","di":"Herbivore","le":5.0,"we":1500,"yr":1970,"dc":"John Ostrom","fa":"Had large shoulder spikes that may have been used for defence against predators like Deinonychus"},
    {"n":"Gallimimus","pe":"Late Cretaceous (70 Ma)","di":"Omnivore","le":6.0,"we":440,"yr":1972,"dc":"Osmolska et al.","fa":"One of the fastest dinosaurs, estimated at up to 50 km/h, resembling a large modern ostrich in build"},
    {"n":"Pachyrhinosaurus","pe":"Late Cretaceous (73-69 Ma)","di":"Herbivore","le":8.0,"we":4000,"yr":1950,"dc":"Charles Sternberg","fa":"Had a thick bony mass on its nose instead of a horn — the function is still debated by palaeontologists"},
    {"n":"Corythosaurus","pe":"Late Cretaceous (77-75 Ma)","di":"Herbivore","le":9.0,"we":4000,"yr":1914,"dc":"Barnum Brown","fa":"Its hollow helmet-shaped crest was used as a resonating chamber to produce loud calls to attract mates"},
    {"n":"Lambeosaurus","pe":"Late Cretaceous (76-75 Ma)","di":"Herbivore","le":15.0,"we":5600,"yr":1923,"dc":"William Arthur Parks","fa":"Had a distinctive hatchet-shaped crest; the largest known hadrosaur, exceeding T. rex in length"},
    {"n":"Spinops","pe":"Late Cretaceous (75 Ma)","di":"Herbivore","le":6.0,"we":2000,"yr":2011,"dc":"Farke et al.","fa":"Stored in museum drawers for 100 years before being properly described — a warning about museum collections"},
    {"n":"Wuerhosaurus","pe":"Early Cretaceous (132-130 Ma)","di":"Herbivore","le":8.0,"we":4000,"yr":1973,"dc":"Dong Zhiming","fa":"One of the last known stegosaurids — proof that the group survived into the Cretaceous in Asia"},
    {"n":"Yutyrannus","pe":"Early Cretaceous (125 Ma)","di":"Carnivore","le":9.0,"we":1414,"yr":2012,"dc":"Xu Xing et al.","fa":"The largest feathered animal ever known; its discovery confirmed that even large tyrannosaurids had feathers"},
    {"n":"Sinosauropteryx","pe":"Early Cretaceous (124 Ma)","di":"Carnivore","le":1.0,"we":0.5,"yr":1996,"dc":"Ji & Ji","fa":"First non-avian dinosaur found with feathers, also the first whose colour was scientifically determined (rusty orange)"},
    {"n":"Tsintaosaurus","pe":"Late Cretaceous (84-71 Ma)","di":"Herbivore","le":10.0,"we":3000,"yr":1958,"dc":"Young","fa":"Had a forward-pointing crest that gave it the nickname 'unicorn dinosaur' — unique in the hadrosaur family"},
    {"n":"Alxasaurus","pe":"Early Cretaceous (112 Ma)","di":"Herbivore","le":4.0,"we":380,"yr":1993,"dc":"Russell & Dong","fa":"One of the earliest therizinosaurs, confirming that this bizarre group descended from carnivorous ancestors"},
    {"n":"Magyarosaurus","pe":"Late Cretaceous (70-66 Ma)","di":"Herbivore","le":6.0,"we":900,"yr":1932,"dc":"von Huene","fa":"A dwarf sauropod that evolved on an ancient island — island dwarfism reduced it to the size of a horse"},
    {"n":"Heterodontosaurus","pe":"Early Jurassic (201-190 Ma)","di":"Omnivore","le":1.2,"we":2.3,"yr":1962,"dc":"Crompton & Charig","fa":"Had three types of teeth — incisors, canines and molars — uniquely varied dentition for any dinosaur"},
    {"n":"Amargasaurus","pe":"Early Cretaceous (130-126 Ma)","di":"Herbivore","le":9.0,"we":7000,"yr":1991,"dc":"Bonaparte & Salgado","fa":"Had two rows of tall neural spines along its neck and back, possibly forming a sail or skin-covered crest"},
    {"n":"Kosmoceratops","pe":"Late Cretaceous (76 Ma)","di":"Herbivore","le":5.0,"we":1200,"yr":2010,"dc":"Scott Sampson et al.","fa":"Had 15 horns — more than any other dinosaur — including two that curved forward like bull horns"},
    {"n":"Scelidosaurus","pe":"Early Jurassic (196-183 Ma)","di":"Herbivore","le":4.0,"we":270,"yr":1858,"dc":"Richard Owen","fa":"One of the earliest armoured dinosaurs, a key ancestor linking ankylosaurs and stegosaurs"},
]

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Mapping pour les noms dont le titre Wikipedia diffère du nom scientifique
WIKI_OVERRIDES = {
    "Tyrannosaurus rex":      "Tyrannosaurus rex",
    "Spinosaurus aegyptiacus":"Spinosaurus",
    "Dracorex hogwartsia":    "Dracorex",
}

def fetch_wikipedia_image(name):
    """Fetches a Wikipedia thumbnail URL for a given dinosaur name."""
    wiki_title = WIKI_OVERRIDES.get(name, name)
    try:
        r = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "titles": wiki_title,
                "prop": "pageimages",
                "format": "json",
                "pithumbsize": 500,
                "redirects": 1,
            },
            headers=HEADERS,
            timeout=8
        )
        if r.status_code != 200:
            return None
        pages = r.json().get("query", {}).get("pages", {})
        for page in pages.values():
            thumb = page.get("thumbnail", {}).get("source")
            if thumb:
                return thumb
        return None
    except Exception:
        return None

print(f"Fetching PhyloPic images for {len(dinosaurs_raw)} dinosaurs...")
result = []
for i, d in enumerate(dinosaurs_raw):
    img = fetch_wikipedia_image(d["n"])
    d["im"] = img
    result.append(d)
    status = "ok" if img else "x"
    print(f"  [{i+1}/{len(dinosaurs_raw)}] {status} {d['n']}")
    time.sleep(0.3)

import os
os.makedirs("assets/science", exist_ok=True)
with open("assets/science/dinosaurs.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, separators=(',', ':'))

found = sum(1 for d in result if d["im"])
print(f"\n{len(result)} dinosaures générés. Images trouvées : {found}/{len(result)}.")
