import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote
sys.stdout.reconfigure(encoding="utf-8")

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Wikipedia page title overrides for ambiguous instrument names
WIKI_EN = {
    "Organ": "Organ (music)",
    "Recorder": "Recorder (musical instrument)",
    "Triangle": "Triangle (musical instrument)",
    "Conga": "Conga (drum)",
    "Bongo Drums": "Bongo drum",
    "Cymbals": "Cymbal",
    "Dulcimer": "Appalachian dulcimer",
    "Hang Drum": "Hang (instrument)",
    "Jaw Harp": "Jew's harp",
}

# n=name, fam=family, ep=era/origin, fa=fact
instruments = [
    {"n":"Violin","fam":"Strings","ep":"Northern Italy, early 16th century","fa":"Has just four strings but can produce an enormous range of expressive tones, central to Western classical music"},
    {"n":"Viola","fam":"Strings","ep":"Northern Italy, early 16th century","fa":"Slightly larger than a violin and tuned a fifth lower, often overlooked despite its warm tone"},
    {"n":"Cello","fam":"Strings","ep":"Italy, early 16th century","fa":"Played upright between the knees, its range is closest to the human voice"},
    {"n":"Double Bass","fam":"Strings","ep":"Italy, 15th-16th century","fa":"The largest and lowest-pitched instrument in the orchestral string family"},
    {"n":"Guitar","fam":"Strings","ep":"Spain, 15th-16th century","fa":"One of the most popular instruments in the world, central to rock, pop, blues and folk music"},
    {"n":"Classical Guitar","fam":"Strings","ep":"Spain, 19th century","fa":"Uses nylon strings and is plucked with fingers rather than a pick"},
    {"n":"Bass Guitar","fam":"Strings","ep":"United States, 1930s-1950s","fa":"Provides the low-end foundation in most modern rock, pop and jazz ensembles"},
    {"n":"Harp","fam":"Strings","ep":"Ancient Mesopotamia, before 3000 BCE","fa":"One of the oldest string instruments, with pedal harps having up to 47 strings"},
    {"n":"Banjo","fam":"Strings","ep":"West Africa, adapted in colonial America 17th-18th century","fa":"Descended from West African instruments, central to American folk and bluegrass music"},
    {"n":"Mandolin","fam":"Strings","ep":"Italy, 18th century","fa":"Has eight strings in four paired courses, common in bluegrass and Italian folk music"},
    {"n":"Ukulele","fam":"Strings","ep":"Hawaii, 1880s","fa":"A small four-stringed instrument developed in Hawaii from Portuguese instruments"},
    {"n":"Sitar","fam":"Strings","ep":"South Asia, 12th-13th century","fa":"A long-necked Indian instrument with sympathetic strings that resonate beneath the main ones"},
    {"n":"Koto","fam":"Strings","ep":"Japan, adapted from China around the 7th-8th century","fa":"A traditional Japanese zither with 13 strings, played by plucking with picks"},
    {"n":"Balalaika","fam":"Strings","ep":"Russia, late 17th century","fa":"A Russian instrument with a distinctive triangular body and three strings"},
    {"n":"Oud","fam":"Strings","ep":"Middle East, before the 9th century","fa":"A pear-shaped, fretless Middle Eastern lute considered an ancestor of the guitar"},
    {"n":"Erhu","fam":"Strings","ep":"China, Tang Dynasty era (7th-10th century)","fa":"A Chinese two-stringed bowed instrument sometimes called the 'Chinese violin'"},
    {"n":"Hurdy-Gurdy","fam":"Strings","ep":"Medieval Europe, around the 10th-11th century","fa":"Produces sound via a hand-cranked wheel rubbing against the strings like a mechanical violin bow"},
    {"n":"Charango","fam":"Strings","ep":"Andes region, 18th century","fa":"A small Andean lute traditionally made from an armadillo shell"},
    {"n":"Piano","fam":"Keyboard","ep":"Italy, around 1700","fa":"A percussion-string hybrid where hammers strike strings, invented in Italy around 1700"},
    {"n":"Harpsichord","fam":"Keyboard","ep":"Europe, 14th-15th century","fa":"Plucks its strings rather than striking them, the dominant keyboard instrument before the piano"},
    {"n":"Organ","fam":"Keyboard","ep":"Ancient Greece, 3rd century BCE","fa":"Pipe organs can have thousands of pipes and are among the largest musical instruments ever built"},
    {"n":"Accordion","fam":"Keyboard","ep":"Berlin, 1820s","fa":"Uses a hand-pumped bellows to push air through reeds, popular in folk music worldwide"},
    {"n":"Celesta","fam":"Keyboard","ep":"France, 1886","fa":"Struck metal bars give it a bell-like sound, famously used in Tchaikovsky's 'Dance of the Sugar Plum Fairy'"},
    {"n":"Clavichord","fam":"Keyboard","ep":"Europe, 14th century","fa":"A quiet Renaissance keyboard instrument that lets players control volume through touch"},
    {"n":"Synthesizer","fam":"Keyboard/Electronic","ep":"United States, 1960s","fa":"Generates sound electronically, revolutionizing music production from the 1970s onward"},
    {"n":"Flute","fam":"Woodwind","ep":"Prehistoric, oldest known examples over 40,000 years old","fa":"One of the oldest known instruments, with prehistoric bone flutes found dating back over 40,000 years"},
    {"n":"Piccolo","fam":"Woodwind","ep":"Europe, 18th century","fa":"A smaller, higher-pitched version of the flute, the highest-pitched instrument in the orchestra"},
    {"n":"Clarinet","fam":"Woodwind","ep":"Germany, early 18th century","fa":"Uses a single reed and has an unusually wide pitch range for a woodwind"},
    {"n":"Oboe","fam":"Woodwind","ep":"France, 17th century","fa":"Traditionally used to tune the rest of the orchestra before a concert"},
    {"n":"Bassoon","fam":"Woodwind","ep":"Italy, 16th-17th century","fa":"A double-reed instrument known for its deep, distinctive tone and long, folded body"},
    {"n":"Saxophone","fam":"Woodwind","ep":"Belgium, 1840s","fa":"Invented in the 1840s by Adolphe Sax, made of brass but classified as a woodwind"},
    {"n":"Recorder","fam":"Woodwind","ep":"Medieval Europe, 14th century","fa":"A simple fipple flute often used to teach music to children in schools"},
    {"n":"Bagpipes","fam":"Woodwind","ep":"Ancient Middle East, adapted across Europe by the Middle Ages","fa":"Uses a constantly filled air bag to sustain continuous sound, iconic in Scottish and Irish music"},
    {"n":"Panpipes","fam":"Woodwind","ep":"Ancient Greece and pre-Columbian Andes, independently","fa":"Made of multiple tuned pipes of different lengths bound together, found in many ancient cultures"},
    {"n":"Didgeridoo","fam":"Woodwind","ep":"Northern Australia, at least 1,000-1,500 years old","fa":"An Indigenous Australian wind instrument that can produce continuous sound through circular breathing"},
    {"n":"Shakuhachi","fam":"Woodwind","ep":"Japan, 7th-8th century","fa":"A traditional Japanese bamboo flute historically played by wandering Zen Buddhist monks"},
    {"n":"Ocarina","fam":"Woodwind","ep":"Found independently across ancient China, Mesoamerica and Africa","fa":"An ancient vessel flute shape found independently in cultures across the globe"},
    {"n":"Trumpet","fam":"Brass","ep":"Ancient Egypt, before 1500 BCE","fa":"One of the oldest brass instruments, with ancient versions found in Egyptian tombs"},
    {"n":"Trombone","fam":"Brass","ep":"Europe, 15th century","fa":"Uses a sliding tube instead of valves to change pitch, unique among common brass instruments"},
    {"n":"French Horn","fam":"Brass","ep":"Germany/France, 17th century","fa":"Its tubing can stretch over 12 feet if uncoiled, giving it a warm, mellow tone"},
    {"n":"Tuba","fam":"Brass","ep":"Germany, 1835","fa":"The largest and lowest-pitched instrument in the brass family"},
    {"n":"Cornet","fam":"Brass","ep":"France, 1820s","fa":"Similar to the trumpet but with a more conical bore, giving it a mellower tone"},
    {"n":"Euphonium","fam":"Brass","ep":"Germany, 1840s","fa":"A tenor-voiced brass instrument common in concert and military bands"},
    {"n":"Flugelhorn","fam":"Brass","ep":"Germany, early 19th century","fa":"Has a wider, conical bore than a trumpet, giving it a softer, rounder tone favored in jazz"},
    {"n":"Sousaphone","fam":"Brass","ep":"United States, 1890s","fa":"Designed to be worn wrapped around the body, named after bandleader John Philip Sousa"},
    {"n":"Drum Kit","fam":"Percussion","ep":"United States, early 20th century","fa":"Assembled in the early 20th century so one musician could play several drums and cymbals at once"},
    {"n":"Snare Drum","fam":"Percussion","ep":"Medieval Europe","fa":"Named for the wire snares stretched across its bottom head that give it a sharp, rattling sound"},
    {"n":"Timpani","fam":"Percussion","ep":"Middle East, adopted in Europe by the 15th century","fa":"Large tunable drums that can be adjusted to specific pitches during a performance"},
    {"n":"Xylophone","fam":"Percussion","ep":"Southeast Asia and Africa, independently, over 1,000 years ago","fa":"Wooden bars struck with mallets, its name comes from Greek words for 'wood' and 'sound'"},
    {"n":"Marimba","fam":"Percussion","ep":"Central America and Southern Africa, centuries old","fa":"Similar to a xylophone but with resonators beneath the bars for a deeper, richer tone"},
    {"n":"Vibraphone","fam":"Percussion","ep":"United States, 1920s","fa":"Uses motor-driven fans in its resonators to create a signature vibrato effect"},
    {"n":"Glockenspiel","fam":"Percussion","ep":"Germany, 18th century","fa":"Metal bars struck with mallets produce a bright, bell-like sound"},
    {"n":"Tambourine","fam":"Percussion","ep":"Ancient Mesopotamia","fa":"Combines a drumhead with jingling metal discs called zils around its frame"},
    {"n":"Cajon","fam":"Percussion","ep":"Peru, 18th-19th century","fa":"A box-shaped Peruvian drum played by slapping its front face while sitting on top of it"},
    {"n":"Djembe","fam":"Percussion","ep":"West Africa, 12th-13th century","fa":"A goblet-shaped West African hand drum capable of a wide range of tones"},
    {"n":"Bongo Drums","fam":"Percussion","ep":"Eastern Cuba, late 19th century","fa":"A pair of connected Afro-Cuban drums of different sizes played with the hands"},
    {"n":"Conga","fam":"Percussion","ep":"Cuba, 19th-20th century","fa":"A tall, narrow Afro-Cuban drum typically played in sets of two or three"},
    {"n":"Tabla","fam":"Percussion","ep":"South Asia, 18th century","fa":"A pair of Indian hand drums central to Hindustani classical music, each tuned differently"},
    {"n":"Steelpan","fam":"Percussion","ep":"Trinidad and Tobago, 1930s-1940s","fa":"Invented in Trinidad and Tobago from repurposed oil drums, now a national instrument"},
    {"n":"Castanets","fam":"Percussion","ep":"Ancient Mediterranean, popularized in Spain","fa":"Small hand-held clapper shells traditionally associated with Spanish flamenco dance"},
    {"n":"Triangle","fam":"Percussion","ep":"Medieval Europe, 14th century","fa":"A simple metal bar bent into a triangle, capable of surprisingly varied dynamics and tone"},
    {"n":"Cymbals","fam":"Percussion","ep":"Ancient Mesopotamia and Asia Minor, over 3,000 years ago","fa":"Metal discs that can be crashed together or struck individually with sticks"},
    {"n":"Gong","fam":"Percussion","ep":"China/Southeast Asia, over 2,000 years ago","fa":"A large metal disc used across many Asian cultures, capable of a huge dynamic range"},
    {"n":"Maracas","fam":"Percussion","ep":"Pre-Columbian Latin America","fa":"Hand-held rattles filled with seeds or beads, originating in Latin American music"},
    {"n":"Theremin","fam":"Electronic","ep":"Russia, 1920","fa":"Played without touching it, by moving hands near two antennas that control pitch and volume"},
    {"n":"Kalimba","fam":"Percussion","ep":"Southern Africa, ancient origin, modernized in the 20th century","fa":"A modern version of the African mbira, played by plucking metal tines with the thumbs"},
    {"n":"Shamisen","fam":"Strings","ep":"Japan, 16th century","fa":"A traditional Japanese three-stringed instrument played with a large plectrum called a bachi"},
    {"n":"Bouzouki","fam":"Strings","ep":"Greece, early 20th century","fa":"A long-necked Greek lute central to rebetiko and modern Greek folk music"},
    {"n":"Dulcimer","fam":"Strings","ep":"Appalachian United States, early 19th century","fa":"An Appalachian string instrument traditionally played flat on the lap or a table"},
    {"n":"Autoharp","fam":"Strings","ep":"Germany/United States, 1880s","fa":"Uses button-operated bars to mute unwanted strings, making chords easy to play"},
    {"n":"Hang Drum","fam":"Percussion","ep":"Switzerland, 2000","fa":"A modern Swiss steel instrument shaped like a UFO, played with the hands"},
    {"n":"Glass Harmonica","fam":"Percussion/Idiophone","ep":"United States, 1761","fa":"Invented by Benjamin Franklin, played by rubbing wet fingers on rotating glass bowls"},
    {"n":"Mellotron","fam":"Keyboard/Electronic","ep":"United Kingdom, 1963","fa":"Played pre-recorded tape loops of real instruments, famously used on The Beatles' 'Strawberry Fields Forever'"},
    {"n":"Kazoo","fam":"Wind/Membranophone","ep":"United States, mid-19th century","fa":"Doesn't produce sound itself but modifies the player's own humming through a vibrating membrane"},
    {"n":"Jaw Harp","fam":"Idiophone","ep":"Asia, over 2,000 years old","fa":"Held between the teeth and plucked, using the mouth as a resonating chamber"},
    {"n":"Bandoneon","fam":"Keyboard/Bellows","ep":"Germany, 1840s, adopted in Argentina","fa":"A button-operated bellows instrument essential to Argentine tango music"},
    {"n":"Lute","fam":"Strings","ep":"Middle East, adapted in Europe by the 13th century","fa":"A pear-shaped plucked instrument that was the most popular instrument in Renaissance Europe"},
    {"n":"Viola da Gamba","fam":"Strings","ep":"Spain, late 15th century","fa":"A bowed Renaissance and Baroque instrument played upright between the legs, unlike the modern cello"},
    {"n":"Zither","fam":"Strings","ep":"Central Europe, 18th century","fa":"A flat string instrument played on a table or the lap, central to Central European folk music"},
    {"n":"Harmonium","fam":"Keyboard/Bellows","ep":"France, 1840s, adopted in India in the 19th century","fa":"A pump-organ variant central to Indian classical and devotional music"},
]

def wiki_img(title):
    for attempt in range(2):
        try:
            if attempt == 0:
                url = ("https://en.wikipedia.org/w/api.php?action=query&prop=pageimages"
                       "&format=json&titles=" + quote(title) + "&pithumbsize=500")
                r = requests.get(url, headers=HEADERS, timeout=10)
                pages = r.json().get("query", {}).get("pages", {})
                for page in pages.values():
                    src = page.get("thumbnail", {}).get("source")
                    if src:
                        return src
            else:
                url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + quote(title)
                r = requests.get(url, headers=HEADERS, timeout=10)
                if r.status_code == 200:
                    src = r.json().get("thumbnail", {}).get("source")
                    if src:
                        return src
        except Exception:
            pass
    return None

def main():
    total = len(instruments)
    found = 0
    for i, s in enumerate(instruments):
        title = WIKI_EN.get(s["n"], s["n"])
        img = wiki_img(title)
        s["im"] = img
        if img:
            found += 1
        status = "ok" if img else "xx"
        line = "  [{:2}/{}] {} {}\n".format(i + 1, total, status, s["n"])
        sys.stdout.buffer.write(line.encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)
    out = Path("assets/music/instruments.json")
    out.write_text(json.dumps(instruments, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    summary = "\nDone: {}/{} images -- {} instruments total.\n".format(found, total, total)
    sys.stdout.buffer.write(summary.encode("utf-8"))

if __name__ == "__main__":
    main()
