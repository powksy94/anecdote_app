import json, requests, time, os, sys
sys.stdout.reconfigure(encoding="utf-8")

# n=original/international title (displayed as-is in EN, never auto-translated),
# n_fr/n_es=official French/Spanish release title (only set when verified;
# omitted entries fall back to the original title in the app),
# di=director, co=country, y=year, du=duration(min), fa=famousFor,
# im=official poster URL (None if not found)

FILMS_RAW = [
    {"n":"Nosferatu","di":"F.W. Murnau","co":"Germany","y":1922,"du":94,"fa":"An unauthorized adaptation of Dracula so blatant that a lawsuit from Bram Stoker's estate ordered all copies destroyed; surviving prints preserved what became one of cinema's most influential horror films."},
    {"n":"The Cabinet of Dr. Caligari","n_fr":"Le Cabinet du docteur Caligari","n_es":"El gabinete del doctor Caligari","di":"Robert Wiene","co":"Germany","y":1920,"du":76,"fa":"Its jagged, painted-on sets pioneered German Expressionist cinema and influenced the visual language of horror and film noir for decades."},
    {"n":"Dracula","di":"Tod Browning","co":"United States","y":1931,"du":75,"fa":"Bela Lugosi's performance defined the modern image of the vampire and launched Universal Pictures' entire classic monster movie era."},
    {"n":"Frankenstein","di":"James Whale","co":"United States","y":1931,"du":70,"fa":"Boris Karloff's monster makeup became so iconic that it is still instantly recognizable a century later, despite Karloff receiving no line of dialogue for much of the film."},
    {"n":"Psycho","n_fr":"Psychose","n_es":"Psicosis","di":"Alfred Hitchcock","co":"United States","y":1960,"du":109,"fa":"Hitchcock bought up copies of the source novel to preserve the twist, and famously required cinemas to bar latecomers from entering once the film had started."},
    {"n":"The Birds","n_fr":"Les Oiseaux","n_es":"Los pajaros","di":"Alfred Hitchcock","co":"United States","y":1963,"du":119,"fa":"Achieved its unsettling attack scenes almost entirely with trained birds and mechanical effects, decades before CGI existed."},
    {"n":"Rosemary's Baby","n_es":"La semilla del diablo","di":"Roman Polanski","co":"United States","y":1968,"du":137,"fa":"Its slow-building paranoia about a sinister apartment building made it a template for psychological horror that trusts dread over jump scares."},
    {"n":"Night of the Living Dead","n_fr":"La Nuit des morts-vivants","n_es":"La noche de los muertos vivientes","di":"George A. Romero","co":"United States","y":1968,"du":96,"fa":"Made on a shoestring budget, it single-handedly created the modern zombie genre and its rules that countless later films would follow."},
    {"n":"The Exorcist","n_fr":"L'Exorciste","n_es":"El exorcista","di":"William Friedkin","co":"United States","y":1973,"du":122,"fa":"Reports of fainting audience members at its 1973 release turned it into a cultural phenomenon; it remains one of the few horror films nominated for the Best Picture Oscar."},
    {"n":"The Wicker Man","n_es":"El hombre de mimbre","di":"Robin Hardy","co":"United Kingdom","y":1973,"du":88,"fa":"Its folk-horror atmosphere of pagan ritual on a remote Scottish island inspired an entire subgenre that resurfaced decades later."},
    {"n":"The Texas Chain Saw Massacre","n_fr":"Massacre a la tronconneuse","n_es":"La matanza de Texas","di":"Tobe Hooper","co":"United States","y":1974,"du":83,"fa":"Despite its brutal reputation, it contains almost no on-screen gore; its terror comes largely from suggestion, sound design and relentless pacing."},
    {"n":"Suspiria","di":"Dario Argento","co":"Italy","y":1977,"du":99,"fa":"Its saturated primary-color lighting and pulsing prog-rock score by Goblin turned a ballet academy into one of horror's most visually striking nightmares."},
    {"n":"Eraserhead","di":"David Lynch","co":"United States","y":1977,"du":89,"fa":"David Lynch's surreal debut, shot over several years on a minuscule budget, became a defining work of body-horror and midnight-movie cinema."},
    {"n":"House (Hausu)","di":"Nobuhiko Obayashi","co":"Japan","y":1977,"du":88,"fa":"A haunted-house film unlike any other, mixing cartoonish special effects and dreamlike logic that made it a cult favorite decades after its release."},
    {"n":"Halloween","di":"John Carpenter","co":"United States","y":1978,"du":91,"fa":"Made for around 300,000 dollars, it became one of the most profitable independent films ever and established many conventions of the slasher genre."},
    {"n":"Alien","di":"Ridley Scott","co":"United States, United Kingdom","y":1979,"du":117,"fa":"H.R. Giger's biomechanical creature design gave science-fiction horror an entirely new visual vocabulary that is still imitated today."},
    {"n":"The Amityville Horror","n_fr":"Amityville, la maison du diable","n_es":"Terror en Amityville","di":"Stuart Rosenberg","co":"United States","y":1979,"du":117,"fa":"Based on a supposedly true haunting, its enormous commercial success sparked a decades-long franchise and debate over how much of its story was fabricated."},
    {"n":"The Shining","n_fr":"Shining","n_es":"El resplandor","di":"Stanley Kubrick","co":"United Kingdom, United States","y":1980,"du":146,"fa":"Kubrick reportedly demanded over 100 takes of some scenes; its unsettling use of the Steadicam through the Overlook Hotel's corridors became legendary."},
    {"n":"An American Werewolf in London","n_fr":"Le Loup-garou de Londres","n_es":"Un hombre lobo americano en Londres","di":"John Landis","co":"United Kingdom, United States","y":1981,"du":97,"fa":"Its transformation sequence, achieved entirely with practical makeup effects, won the very first Academy Award given for makeup."},
    {"n":"Poltergeist","di":"Tobe Hooper","co":"United States","y":1982,"du":114,"fa":"Its suburban setting made supernatural horror feel close to home, and its production was later shadowed by tabloid stories about an alleged curse."},
    {"n":"The Thing","n_es":"La cosa","di":"John Carpenter","co":"United States","y":1982,"du":109,"fa":"Its shape-shifting alien creature effects, built almost entirely with practical animatronics, are still studied by effects artists as a benchmark decades later."},
    {"n":"A Nightmare on Elm Street","n_fr":"Les Griffes de la nuit","n_es":"Pesadilla en Elm Street","di":"Wes Craven","co":"United States","y":1984,"du":91,"fa":"Its premise, that a killer could reach victims through their dreams, made sleep itself feel dangerous and launched one of horror's most recognizable villains."},
    {"n":"Evil Dead II","di":"Sam Raimi","co":"United States","y":1987,"du":84,"fa":"Blended slapstick comedy with gruesome horror so effectively that it helped define the horror-comedy genre for the decades that followed."},
    {"n":"Hellraiser","di":"Clive Barker","co":"United Kingdom","y":1987,"du":94,"fa":"Adapted by author Clive Barker from his own novella, its intricate puzzle box and Cenobite creatures introduced a distinctly gothic, S&M-tinged strain of horror."},
    {"n":"Child's Play","di":"Tom Holland","co":"United States","y":1988,"du":87,"fa":"Turned a children's toy into a horror icon, sparking a long-running franchise and renewed public unease about dolls in general."},
    {"n":"Misery","di":"Rob Reiner","co":"United States","y":1990,"du":107,"fa":"Kathy Bates won an Academy Award for playing a fan who holds an injured novelist captive, proving horror could earn top acting honors."},
    {"n":"The Silence of the Lambs","n_fr":"Le Silence des agneaux","n_es":"El silencio de los corderos","di":"Jonathan Demme","co":"United States","y":1991,"du":118,"fa":"One of only three films in history to sweep all five major Academy Awards, remarkable for a film built around a serial killer thriller."},
    {"n":"Candyman","di":"Bernard Rose","co":"United States, United Kingdom","y":1992,"du":99,"fa":"Set against Chicago's Cabrini-Green housing project, it used urban legend and social commentary to give slasher horror unusual depth."},
    {"n":"Ringu","di":"Hideo Nakata","co":"Japan","y":1998,"du":96,"fa":"Its cursed videotape premise ignited the J-horror boom and inspired a wave of American remakes throughout the 2000s."},
    {"n":"Audition","di":"Takashi Miike","co":"Japan","y":1999,"du":115,"fa":"Its slow-burn first half plays almost like a romantic drama before an infamous tonal shift that shocked festival audiences worldwide."},
    {"n":"The Blair Witch Project","n_fr":"Le Projet Blair Witch","n_es":"El proyecto de la bruja de Blair","di":"Daniel Myrick, Eduardo Sanchez","co":"United States","y":1999,"du":81,"fa":"Made for roughly 60,000 dollars and marketed as if it were real found footage, it kickstarted the modern found-footage horror genre."},
    {"n":"The Others","n_fr":"Les Autres","n_es":"Los otros","di":"Alejandro Amenabar","co":"Spain, France, United States","y":2001,"du":104,"fa":"Its fog-bound gothic mansion and slow-building dread earned it comparisons to classic ghost stories rather than modern jump-scare horror."},
    {"n":"The Devil's Backbone","n_fr":"L'Echine du diable","n_es":"El espinazo del diablo","di":"Guillermo del Toro","co":"Spain, Mexico","y":2001,"du":106,"fa":"Set during the Spanish Civil War, del Toro blended ghost story and wartime tragedy in a film he has called a spiritual sibling to Pan's Labyrinth."},
    {"n":"28 Days Later","n_fr":"28 jours plus tard","n_es":"28 dias despues","di":"Danny Boyle","co":"United Kingdom","y":2002,"du":113,"fa":"Its fast-moving, rage-infected creatures reinvented the zombie genre, replacing the traditional shambling undead with sprinting horror."},
    {"n":"Saw","di":"James Wan","co":"United States, Australia","y":2004,"du":103,"fa":"Shot in just 18 days on a tiny budget, its moral traps premise spawned one of the most commercially successful horror franchises ever made."},
    {"n":"Pan's Labyrinth","n_fr":"Le Labyrinthe de Pan","n_es":"El laberinto del fauno","di":"Guillermo del Toro","co":"Spain, Mexico","y":2006,"du":118,"fa":"Blended dark fairy tale fantasy with the horrors of fascist Spain, and remains one of the rare horror-adjacent films to win multiple Academy Awards."},
    {"n":"Rec","di":"Jaume Balaguero, Paco Plaza","co":"Spain","y":2007,"du":78,"fa":"Its found-footage format, following a news crew locked inside a quarantined apartment building, made it one of Spain's most successful horror exports."},
    {"n":"Paranormal Activity","di":"Oren Peli","co":"United States","y":2007,"du":86,"fa":"Made for around 15,000 dollars and shot largely in the director's own house, it became one of the most profitable films ever made relative to its budget."},
    {"n":"Let the Right One In","n_fr":"Morse","n_es":"Dejame entrar","di":"Tomas Alfredson","co":"Sweden","y":2008,"du":114,"fa":"A wintry, melancholy vampire story about lonely children that critics frequently rank among the greatest vampire films ever made."},
    {"n":"Drag Me to Hell","n_fr":"Jusqu'en enfer","n_es":"Arrastrame al infierno","di":"Sam Raimi","co":"United States","y":2009,"du":99,"fa":"Sam Raimi's return to horror after a decade of blockbusters brought back the gleeful, over-the-top style of his earlier Evil Dead films."},
    {"n":"Insidious","di":"James Wan","co":"United States","y":2010,"du":103,"fa":"Relied on atmosphere and sound design over graphic violence, helping usher in a new wave of PG-13-friendly studio horror."},
    {"n":"The Cabin in the Woods","n_fr":"La cabane dans les bois","n_es":"La cabana en el bosque","di":"Drew Goddard","co":"United States","y":2012,"du":95,"fa":"Written by Joss Whedon and Drew Goddard as an affectionate deconstruction of horror movie tropes, twisting the genre's own rules against itself."},
    {"n":"The Conjuring","n_fr":"Conjuring : Les Dossiers Warren","n_es":"Expediente Warren: The Conjuring","di":"James Wan","co":"United States","y":2013,"du":112,"fa":"Based on paranormal investigators Ed and Lorraine Warren, it launched one of the most successful horror franchises of the 21st century."},
    {"n":"It Follows","di":"David Robert Mitchell","co":"United States","y":2014,"du":100,"fa":"Its premise of a slow, unstoppable supernatural pursuer became widely read as an allegory, while its synth score revived a distinctly retro horror sound."},
    {"n":"The Babadook","n_fr":"Mister Babadook","di":"Jennifer Kent","co":"Australia","y":2014,"du":94,"fa":"A grieving single mother's battle with a storybook monster was embraced by critics as a rare horror film built on genuine emotional depth."},
    {"n":"Goodnight Mommy","di":"Severin Fiala, Veronika Franz","co":"Austria","y":2014,"du":99,"fa":"Its story of twin boys suspicious of their bandaged mother was Austria's official submission for the Academy Award for Best Foreign Language Film."},
    {"n":"A Girl Walks Home Alone at Night","di":"Ana Lily Amirpour","co":"United States","y":2014,"du":101,"fa":"Billed as 'the first Iranian vampire western', shot in black and white with Persian dialogue despite being filmed in California."},
    {"n":"The Witch","di":"Robert Eggers","co":"United States, Canada","y":2015,"du":92,"fa":"Its dialogue was constructed largely from 17th-century historical texts to recreate authentic Puritan New England speech."},
    {"n":"Get Out","n_es":"Dejame salir","di":"Jordan Peele","co":"United States","y":2017,"du":104,"fa":"Jordan Peele's directorial debut used horror to explore race in America and won him the Academy Award for Best Original Screenplay."},
    {"n":"Tigers Are Not Afraid","n_es":"Vuelven","di":"Issa Lopez","co":"Mexico","y":2017,"du":83,"fa":"Weaves fairy-tale imagery through the real horrors faced by children orphaned by Mexico's drug war, earning praise from Guillermo del Toro himself."},
    {"n":"Hereditary","n_fr":"Heredite","di":"Ari Aster","co":"United States","y":2018,"du":127,"fa":"Toni Collette's performance as a grieving mother unraveling was widely called one of the greatest in horror history, despite being overlooked at major awards."},
    {"n":"A Quiet Place","n_fr":"Sans un bruit","n_es":"Un lugar en silencio","di":"John Krasinski","co":"United States","y":2018,"du":90,"fa":"Built almost entirely around silence, with sound itself becoming the source of danger for its sound-hunting alien creatures."},
    {"n":"Saint Maud","di":"Rose Glass","co":"United Kingdom","y":2019,"du":84,"fa":"A hospice nurse's religious devotion curdles into obsession in this British debut that critics compared to Taxi Driver for its unreliable narration."},
    {"n":"Midsommar","di":"Ari Aster","co":"United States, Sweden","y":2019,"du":148,"fa":"Almost entirely set in broad Scandinavian daylight, it proved horror does not require darkness to unsettle an audience."},
    {"n":"The Lighthouse","n_es":"El faro","di":"Robert Eggers","co":"United States, Canada","y":2019,"du":109,"fa":"Shot in black and white on a nearly square aspect ratio, its two-hander of dueling lighthouse keepers became an instant arthouse horror classic."},
    {"n":"His House","di":"Remi Weekes","co":"United Kingdom","y":2020,"du":93,"fa":"Follows Sudanese refugees haunted by a supernatural presence in their new English home, blending trauma narrative with haunted-house horror."},
    {"n":"Talk to Me","di":"Danny Philippou, Michael Philippou","co":"Australia","y":2022,"du":95,"fa":"Made by two former YouTubers on a modest budget, it became one of A24's highest-grossing horror releases through purely word-of-mouth buzz."},
    {"n":"Obsession","di":"Curry Barker","co":"United States","y":2026,"du":108,"fa":"Curry Barker's feature directorial debut follows a shy music store worker who buys a cursed toy to win a friend's love, only for her devotion to spiral into something far darker."},
    {"n":"Backrooms","di":"Kane Parsons","co":"United States","y":2026,"du":110,"fa":"Directed by Kane Parsons at just 20 years old in his feature debut, it expanded his own viral YouTube web series adapting the 'Backrooms' creepypasta into a full studio release from A24."},
]

HEADERS = {"User-Agent": "projet_app_annecdote/1.0 (daily-facts educational app; github.com/uzan)"}

import re

def _words(s):
    return set(re.findall(r"[a-z0-9]+", s.lower())) - {"the", "a", "an", "of", "in", "on"}

def wiki_pageimage(page_title, size=400):
    for attempt in range(4):
        try:
            r = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={"action":"query","titles":page_title,"prop":"pageimages",
                        "format":"json","pithumbsize":size,"redirects":1},
                headers=HEADERS, timeout=12,
            )
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 10))
                time.sleep(max(wait, 10))
                continue
            if not r.text.strip():
                return None
            pages = r.json().get("query", {}).get("pages", {})
            page = next(iter(pages.values()))
            if "missing" in page:
                return None
            return page.get("thumbnail", {}).get("source")
        except Exception:
            time.sleep(2)
    return None


# Titles whose bare name resolves to something other than this specific film
# on Wikipedia (a novel, the general subject/holiday, a franchise overview
# page, or another well-known topic) -- for these, go straight to a
# disambiguated title instead of risking the wrong page's image. No free-text
# Commons fallback is used: it repeatedly returned unrelated images (a 1925
# film's poster matched via "poster" keyword overlap alone) with no reliable
# way to validate relevance, so a missing poster is safer than a wrong one.
TITLE_OVERRIDES = {
    "Dracula": "Dracula (1931 film)",
    "Frankenstein": "Frankenstein (1931 film)",
    "The Thing": "The Thing (1982 film)",
    "Misery": "Misery (film)",
    "Saw": "Saw (2004 film)",
    "The Others": "The Others (2001 film)",
    "Poltergeist": "Poltergeist (1982 film)",
    "Halloween": "Halloween (1978 film)",
    "Candyman": "Candyman (1992 film)",
    "The Witch": "The Witch (2015 film)",
    "Talk to Me": "Talk to Me (2022 film)",
    "Obsession": "Obsession (2026 film)",
    "Backrooms": "Backrooms (film)",
    "His House": "His House (film)",
    "Get Out": "Get Out (film)",
    "Audition": "Audition (1999 film)",
    "Child's Play": "Child's Play (1988 film)",
    "Rec": "REC (film)",
    "Saint Maud": "Saint Maud (film)",
    "Hereditary": "Hereditary (film)",
}

def fetch_poster(title, year):
    variants = [TITLE_OVERRIDES[title]] if title in TITLE_OVERRIDES \
        else [title, f"{title} (film)", f"{title} ({year} film)"]
    for variant in variants:
        im = wiki_pageimage(variant)
        if im:
            return im
        time.sleep(0.6)
    return None

output_path = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../../assets/cinema/horror_films.json")
)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

existing_images = {}
if os.path.exists(output_path):
    with open(output_path, encoding="utf-8") as f:
        for entry in json.load(f):
            if entry.get("im"):
                existing_images[entry["n"]] = entry["im"]
    print(f"Loaded {len(existing_images)} existing images from cache.\n")

missing = sum(1 for m in FILMS_RAW if not existing_images.get(m["n"]))
print(f"{missing} film(s) need a poster.\n")
fetch_idx = 0
films = []
for i, m in enumerate(FILMS_RAW, 1):
    name = m["n"]
    if existing_images.get(name):
        im = existing_images[name]
        print(f"[{i:2}/{len(FILMS_RAW)}] {name} (cached)")
    else:
        fetch_idx += 1
        print(f"[{i:2}/{len(FILMS_RAW)}] Fetching poster for {name} ({m['y']}) ...")
        im = fetch_poster(name, m["y"])
        if im:
            print(f"  found: {im[:90]}")
        if fetch_idx < missing:
            time.sleep(1.2)
    films.append({**m, "im": im})

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(films, f, ensure_ascii=False, separators=(",", ":"))

fetched = sum(1 for m in films if m["im"])
print(f"\nDone -- {len(films)} films, {fetched} with posters -> {output_path}")
