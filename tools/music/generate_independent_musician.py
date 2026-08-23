import json, requests, time, os, sys
from urllib.parse import quote
sys.stdout.reconfigure(encoding="utf-8")

# n=artist/band name, gn=genre, fs=famous/signature song, fa=famousFor,
# im=Wikipedia portrait image URL

ARTISTS_RAW = [
    {"n":"Nick Drake","gn":"Folk","fs":"Pink Moon","fa":"Sold only a few thousand records during his lifetime and died at 26, but his three albums became hugely influential decades later, discovered by a new generation through a 1999 Volkswagen ad."},
    {"n":"Daniel Johnston","gn":"Lo-fi / Outsider music","fs":"True Love Will Find You in the End","fa":"Recorded his earliest songs on a home boombox while struggling with mental illness; his hand-drawn 'Hi, How Are You' frog mascot became an underground icon worn by Kurt Cobain."},
    {"n":"Jandek","gn":"Outsider folk","fs":"Naked in the Afternoon","fa":"Has released well over 100 albums since 1978 while remaining almost entirely anonymous, giving virtually no interviews and performing live for the first time only in 2004."},
    {"n":"Connie Converse","gn":"Folk","fs":"Talkin' Like You","fa":"Recorded haunting home demos in the 1950s that went completely unheard, then vanished without a trace in 1974; her music was only rediscovered and released decades later."},
    {"n":"Vashti Bunyan","gn":"Folk","fs":"Diamond Day","fa":"Her 1970 debut album sold so poorly she quit music and moved to a remote croft by horse-drawn cart; it was rediscovered by collectors decades later and led to her surprise comeback in the 2000s."},
    {"n":"Linda Perhacs","gn":"Folk","fs":"Parallelograms","fa":"A dental hygienist by day, her sole 1970 album went almost completely unnoticed until it was rediscovered by collectors in the 2000s, prompting her to resume performing forty years later."},
    {"n":"Judee Sill","gn":"Folk / Baroque pop","fs":"Jesus Was a Cross Maker","fa":"The first artist signed to David Geffen's Asylum Records, her intricate orchestral folk songs found only a small audience during her life; she died in obscurity in 1979."},
    {"n":"Karen Dalton","gn":"Folk / Blues","fs":"Something on Your Mind","fa":"A fixture of the same 1960s Greenwich Village scene as Bob Dylan, who called her his favorite singer, yet she released only two albums and remained largely unknown until a posthumous revival."},
    {"n":"Arthur Russell","gn":"Experimental / Disco","fs":"This Is How We Walk on the Moon","fa":"Moved fluidly between avant-garde composition, disco and folk-pop, leaving hundreds of unfinished recordings at his death in 1992 that have been steadily released and celebrated ever since."},
    {"n":"Sixto Rodriguez","gn":"Folk rock","fs":"Sugar Man","fa":"His early-1970s albums flopped in the US and he assumed his career was over, unaware he had become a massive, mysterious star in South Africa, a story told in the Oscar-winning documentary 'Searching for Sugar Man'."},
    {"n":"Roky Erickson","gn":"Psychedelic rock","fs":"You're Gonna Miss Me","fa":"Fronted the pioneering 13th Floor Elevators before a turbulent life including institutionalization; he continued releasing music that kept a devoted cult following for decades."},
    {"n":"Big Star","gn":"Power pop","fs":"September Gurls","fa":"Their early-1970s albums sold poorly due to distribution problems, but critics and future musicians championed them so heavily that they are now considered one of the most influential cult bands in rock history."},
    {"n":"Neutral Milk Hotel","gn":"Indie folk","fs":"In the Aeroplane Over the Sea","fa":"After the intensely acclaimed 1998 album of the same name, frontman Jeff Mangum largely disappeared from public life for over a decade, only fueling the band's cult mystique."},
    {"n":"Silver Jews","gn":"Indie rock","fs":"Random Rules","fa":"Formed by poet David Berman partly as a side project of Pavement members, it stayed a niche cult favorite for its literary, deadpan lyrics until Berman ended the band in 2009."},
    {"n":"The Shaggs","gn":"Outsider rock","fs":"My Pal Foot Foot","fa":"Three sisters pushed into a band by their father with almost no musical training recorded a single 1969 album now celebrated by musicians for its uniquely unpolished, off-kilter charm."},
    {"n":"Moondog","gn":"Experimental / Composer","fs":"Bird's Lament","fa":"A blind composer and instrument inventor who spent decades busking on New York street corners dressed as a Viking, influencing minimalist composers while remaining a public curiosity."},
    {"n":"Delia Derbyshire","gn":"Electronic","fs":"Doctor Who Theme","fa":"Created the iconic original Doctor Who theme almost entirely from tape loops and manipulated recordings at the BBC Radiophonic Workshop, years before synthesizers were widely available."},
    {"n":"Klaus Nomi","gn":"Avant-garde / New wave","fs":"Total Eclipse","fa":"A German-born countertenor who built a striking operatic new-wave persona in downtown New York before becoming one of the first public figures widely reported to have died of AIDS, in 1983."},
    {"n":"Suicide","gn":"Proto-punk / Electronic","fs":"Frankie Teardrop","fa":"Alan Vega and Martin Rev's confrontational drum-machine-and-vocals duo was so far ahead of its time that early audiences sometimes rioted, yet it became hugely influential on electronic and punk music decades later."},
    {"n":"Silver Apples","gn":"Electronic","fs":"Oscillations","fa":"Built custom oscillator rigs to make some of the earliest electronic rock music in the late 1960s, years before synthesizers became common in popular music."},
    {"n":"Captain Beefheart","gn":"Avant-garde rock","fs":"Ella Guru","fa":"His 1969 album 'Trout Mask Replica', rehearsed obsessively for months in a shared house, remains one of the most extreme and influential experiments ever released on a major record label."},
    {"n":"This Heat","gn":"Experimental rock","fs":"Sleep","fa":"Recorded in a disused meat locker they converted into a studio, their dense, unsettling collages became a touchstone for later post-punk and experimental musicians despite minimal commercial success at the time."},
    {"n":"Broadcast","gn":"Electronic / Psychedelic pop","fs":"Come On Let's Go","fa":"Fronted by the late Trish Keenan, their eerie blend of 1960s film-score atmosphere and electronic pop earned deep cult devotion long before her death in 2011 cut the band's career short."},
    {"n":"Boards of Canada","gn":"Electronic","fs":"Roygbiv","fa":"A famously reclusive Scottish duo who almost never give interviews or perform live, letting their warm, nostalgic electronic albums speak entirely for themselves."},
    {"n":"Burial","gn":"Electronic / Dubstep","fs":"Archangel","fa":"Kept his identity completely secret for years, releasing some of the most acclaimed electronic albums of the 2000s anonymously before finally confirming his name in 2008."},
    {"n":"Autechre","gn":"Experimental electronic","fs":"Gantz Graf","fa":"Known for algorithmically generated compositions of extreme complexity, the duo built one of experimental electronic music's most devoted cult followings while rarely explaining their process."},
    {"n":"Coil","gn":"Industrial / Experimental","fs":"Panic","fa":"Founded by former Throbbing Gristle collaborator John Balance, their shape-shifting, occult-tinged catalogue made them one of underground music's most influential experimental acts."},
    {"n":"Throbbing Gristle","gn":"Industrial","fs":"Hamburger Lady","fa":"Widely credited with inventing industrial music as a genre, their confrontational early performances and self-released records built a devoted underground following in the late 1970s."},
    {"n":"Merzbow","gn":"Noise","fs":"Woodpecker No. 1","fa":"Japanese noise pioneer Masami Akita has released several hundred recordings since the late 1970s, becoming the most internationally recognized figure in the harsh noise genre."},
    {"n":"Boredoms","gn":"Experimental","fs":"Super Are","fa":"Japanese noise-rock provocateurs who evolved from chaotic performance art into hypnotic, rhythm-driven epics, at one point performing with 88 drummers simultaneously."},
    {"n":"Sun Ra","gn":"Avant-garde jazz","fs":"Space Is the Place","fa":"Claimed to be from Saturn and led his self-sufficient 'Arkestra' commune for decades, pioneering Afrofuturism and electronic keyboards in jazz long before either was widely recognized."},
    {"n":"Alice Coltrane","gn":"Spiritual jazz","fs":"Journey in Satchidananda","fa":"After the death of husband John Coltrane, she developed a deeply spiritual, harp-driven jazz sound and later became a swami, recording devotional music for her own ashram."},
    {"n":"Scott Walker","gn":"Avant-garde","fs":"The Electrician","fa":"After teen-pop stardom with the Walker Brothers, he retreated into increasingly dark and dissonant solo work, becoming one of music's most radical reinventions of a former pop star."},
    {"n":"Nico","gn":"Avant-garde / Art rock","fs":"These Days","fa":"Best known as the Velvet Underground's guest vocalist, her stark solo albums built on a droning harmonium became deeply influential on later gothic and avant-garde music."},
    {"n":"Damo Suzuki","gn":"Krautrock","fs":"Vitamin C","fa":"Was discovered busking on a Munich street and joined the band Can that same night; he later toured the world performing entirely improvised vocals with local pickup bands."},
    {"n":"Faust","gn":"Krautrock","fs":"It's a Bit of a Pain","fa":"Recorded in a converted schoolhouse funded by a major label hoping for 'the German Beatles', instead producing some of the most radically experimental rock albums of the early 1970s."},
    {"n":"Neu!","gn":"Krautrock","fs":"Hallogallo","fa":"Formed after splitting from Kraftwerk, their hypnotic, motorik drumbeat became one of the most sampled and imitated rhythms in underground rock and electronic music."},
    {"n":"Popol Vuh","gn":"Ambient / Progressive","fs":"Aguirre","fa":"Best known for scoring several Werner Herzog films, their meditative, early-synthesizer-driven albums became foundational to the ambient music genre."},
    {"n":"Cluster","gn":"Electronic","fs":"Sowiesoso","fa":"Pioneers of ambient electronic music in early-1970s Germany, their gentle, textured soundscapes directly inspired Brian Eno, who later recorded albums together with the duo."},
    {"n":"Wesley Willis","gn":"Outsider music","fs":"Rock N Roll McDonald's","fa":"A Chicago artist living with schizophrenia who wrote hundreds of raw, humorous songs and famously headbutted fans as a greeting, becoming a beloved figure of the 1990s underground scene."},
    {"n":"The Legendary Stardust Cowboy","gn":"Outsider rock and roll","fs":"Paralyzed","fa":"His frantic, off-key 1968 single became an outsider-music cult classic, and he later directly inspired David Bowie's stage name Ziggy Stardust."},
    {"n":"Guided by Voices","gn":"Lo-fi indie rock","fs":"Game of Pricks","fa":"Recorded hundreds of songs on cheap home cassette equipment in an Ohio basement for years before unexpected critical acclaim in the 1990s made them indie rock's most prolific cult act."},
    {"n":"Ween","gn":"Eclectic rock","fs":"Push th' Little Daisies","fa":"Two childhood friends who recorded early albums on a four-track in a basement, building a devoted cult fanbase through wildly genre-hopping, deliberately unpolished records."},
    {"n":"Ariel Pink","gn":"Lo-fi / Psychedelic pop","fs":"Round and Round","fa":"Recorded warped, deliberately lo-fi pop albums alone on a four-track for years before being championed and signed by Animal Collective's own label."},
    {"n":"Panda Bear","gn":"Experimental pop","fs":"Bros","fa":"As a member of Animal Collective and a solo artist, his layered vocal harmonies and tape-loop production built a devoted following within experimental pop circles well before wider recognition."},
    {"n":"Grouper","gn":"Ambient / Drone","fs":"Heavy Water/I'd Rather Be Sleeping","fa":"Liz Harris records hazy, deliberately obscured songs, often layering her voice beneath thick reverb until the lyrics dissolve into pure texture and atmosphere."},
    {"n":"Julianna Barwick","gn":"Ambient / Choral","fs":"Envelop","fa":"Builds entire songs live by looping her own wordless vocals into dense, cathedral-like choirs using nothing but a loop pedal and her own voice."},
    {"n":"Colin Stetson","gn":"Experimental / Saxophone","fs":"Judges","fa":"Uses circular breathing and contact microphones to make a single saxophone sound like a full band, recording extended solo pieces in a single unedited take."},
    {"n":"DyE","gn":"Electronic","fs":"Fantasy","fa":"French producer Juan de Guillebon built a cult following on the Tigersushi label with his downtempo, eclectic sound, best known for the music video of his single 'Fantasy', which drew tens of millions of views."},
    {"n":"Aphex Twin","gn":"Experimental electronic","fs":"Windowlicker","fa":"Richard D. James built an early reputation recording tracks alone in a Cornwall bank vault, becoming one of electronic music's most influential and famously unpredictable figures."},
    {"n":"Squarepusher","gn":"Experimental electronic","fs":"Come on My Selector","fa":"Combines virtuosic jazz bass playing with frantic, glitch-heavy electronic production, building a devoted niche following for a sound rarely attempted by anyone else."},
]

HEADERS = {"User-Agent": "projet_app_annecdote/1.0 (daily-facts educational app; github.com/uzan)"}

def rest_summary_image(page_title):
    try:
        r = requests.get(
            "https://en.wikipedia.org/api/rest_v1/page/summary/" + quote(page_title),
            headers=HEADERS, timeout=12,
        )
        if r.status_code != 200:
            return None
        data = r.json()
        if data.get("type") == "disambiguation":
            return None
        return data.get("thumbnail", {}).get("source")
    except Exception:
        return None

def wiki_pageimage(page_title, size=500):
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
            im = page.get("thumbnail", {}).get("source")
            if im:
                return im
            return rest_summary_image(page.get("title", page_title))
        except Exception:
            time.sleep(2)
    return None

# Names that resolve to something other than the artist on plain Wikipedia
# (a common word, an animal, another band/person) -- these need an explicit
# disambiguated title. No free-text Commons fallback is used at all: it
# repeatedly matched wrong subjects (a real panda for "Panda Bear", a grouper
# fish for "Grouper", an unrelated painting for "Suicide") with no reliable
# way to validate relevance, so a missing image is safer than a wrong one.
NAME_OVERRIDES = {
    "Suicide": "Suicide (band)",
    "This Heat": "This Heat (band)",
    "Panda Bear": "Panda Bear (musician)",
    "Grouper": "Grouper (musician)",
    "Cluster": "Cluster (band)",
    "Coil": "Coil (band)",
    "Nico": "Nico",
    "Faust": "Faust (band)",
    "Burial": "Burial (musician)",
    "Nick Drake": "Nick Drake",
}

def fetch_artist_image(name):
    title = NAME_OVERRIDES.get(name, name)
    im = wiki_pageimage(title)
    if im is None and title == name:
        im = wiki_pageimage(f"{name} (musician)")
    return im

output_path = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../../assets/music/independent_musicians.json")
)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

existing_images = {}
if os.path.exists(output_path):
    with open(output_path, encoding="utf-8") as f:
        for entry in json.load(f):
            if entry.get("im"):
                existing_images[entry["n"]] = entry["im"]
    print(f"Loaded {len(existing_images)} existing images from cache.\n")

missing = sum(1 for a in ARTISTS_RAW if not existing_images.get(a["n"]))
print(f"{missing} artist(s) need an image.\n")
fetch_idx = 0
artists = []
for i, a in enumerate(ARTISTS_RAW, 1):
    name = a["n"]
    if existing_images.get(name):
        im = existing_images[name]
        print(f"[{i:2}/{len(ARTISTS_RAW)}] {name} (cached)")
    else:
        fetch_idx += 1
        print(f"[{i:2}/{len(ARTISTS_RAW)}] Fetching image for {name} ...")
        im = fetch_artist_image(name)
        if im:
            print(f"  found: {im[:90]}")
        if fetch_idx < missing:
            time.sleep(1.2)
    artists.append({**a, "im": im})

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(artists, f, ensure_ascii=False, separators=(",", ":"))

fetched = sum(1 for a in artists if a["im"])
print(f"\nDone -- {len(artists)} artists, {fetched} with images -> {output_path}")
