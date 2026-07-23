import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote
sys.stdout.reconfigure(encoding="utf-8")

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_EN = {}

# n=name, loc=location, at=approximate attendance, fa=fact
festivals = [
    {"n":"Woodstock","loc":"United States","at":"around 400,000 attendees","fa":"The 1969 festival became a defining symbol of the counterculture era"},
    {"n":"Coachella","loc":"United States","at":"around 125,000 per weekend","fa":"Held annually in the California desert, one of the most-livestreamed music festivals in the world"},
    {"n":"Glastonbury Festival","loc":"United Kingdom","at":"around 210,000 attendees","fa":"One of the largest greenfield festivals in the world, held on a farm since 1970"},
    {"n":"Tomorrowland","loc":"Belgium","at":"around 400,000 across two weekends","fa":"One of the largest electronic dance music festivals in the world"},
    {"n":"Lollapalooza","loc":"United States","at":"around 400,000 over four days","fa":"Originally a touring festival in the early 1990s before becoming an annual Chicago event"},
    {"n":"Burning Man","loc":"United States","at":"around 80,000 attendees","fa":"A week-long art and music gathering in the Nevada desert culminating in the burning of a giant wooden effigy"},
    {"n":"Ultra Music Festival","loc":"United States","at":"around 165,000 over three days","fa":"A major electronic dance music festival held annually in Miami"},
    {"n":"Roskilde Festival","loc":"Denmark","at":"around 130,000 attendees","fa":"One of Europe's largest music festivals, run by a non-profit foundation supporting humanitarian causes"},
    {"n":"Rock in Rio","loc":"Brazil","at":"over 1 million cumulative attendees in its record 1985 edition","fa":"One of the largest music festivals in the world by attendance since its 1985 debut"},
    {"n":"Fuji Rock Festival","loc":"Japan","at":"around 120,000 attendees","fa":"Japan's largest outdoor music festival, held in the mountains of Niigata Prefecture"},
    {"n":"Isle of Wight Festival","loc":"United Kingdom","at":"an estimated 600,000-700,000 in 1970","fa":"Its 1970 edition remains among the largest gatherings in music history"},
    {"n":"Reading and Leeds Festivals","loc":"United Kingdom","at":"around 170,000 combined","fa":"Twin festivals held simultaneously in two UK cities with the same lineup"},
    {"n":"Bonnaroo","loc":"United States","at":"around 80,000 attendees","fa":"Held on a large farm in Tennessee, known for its eclectic mix of genres"},
    {"n":"Primavera Sound","loc":"Spain","at":"around 250,000 total attendance","fa":"A Barcelona festival known for its indie, alternative and electronic lineups"},
    {"n":"Sziget Festival","loc":"Hungary","at":"around 450,000 over the week","fa":"Held on an island in the Danube River in Budapest, one of Europe's biggest festivals"},
    {"n":"Montreux Jazz Festival","loc":"Switzerland","at":"around 250,000 over the festival run","fa":"One of the most prestigious jazz festivals in the world since 1967, later expanding beyond jazz"},
    {"n":"New Orleans Jazz Fest","loc":"United States","at":"around 475,000 over two weekends","fa":"Celebrates the music and culture of New Orleans, running for two weekends every spring"},
    {"n":"South by Southwest (SXSW)","loc":"United States","at":"several hundred thousand including public events","fa":"Combines music, film and interactive media in Austin, Texas, launching many artists' careers"},
    {"n":"Austin City Limits Festival","loc":"United States","at":"around 450,000 over two weekends","fa":"Named after the long-running television music program of the same name"},
    {"n":"Download Festival","loc":"United Kingdom","at":"around 111,000 attendees","fa":"A major rock and heavy metal festival held at the Donington Park racing circuit"},
    {"n":"Wacken Open Air","loc":"Germany","at":"around 85,000 attendees, its official capacity","fa":"The world's largest heavy metal festival, held in a small German village since 1990"},
    {"n":"Exit Festival","loc":"Serbia","at":"around 200,000 over the week","fa":"Began in 2000 as a student protest movement before becoming a major European festival"},
    {"n":"Electric Daisy Carnival (EDC)","loc":"United States","at":"over 400,000 across three nights","fa":"One of the largest electronic dance music festivals, known for its elaborate stage productions"},
    {"n":"Essence Festival","loc":"United States","at":"several hundred thousand over the weekend","fa":"Celebrates Black culture and music, held annually in New Orleans"},
    {"n":"Afropunk Festival","loc":"United States","at":"tens of thousands annually","fa":"Began as a documentary film project before becoming a celebration of Black alternative culture"},
    {"n":"Vieilles Charrues Festival","loc":"France","at":"around 280,000 attendees","fa":"One of the largest music festivals in France, held in the Brittany countryside"},
    {"n":"Eurockeennes","loc":"France","at":"around 100,000 attendees","fa":"A major French rock festival held on a peninsula near Belfort"},
    {"n":"Hellfest","loc":"France","at":"around 180,000 over the weekend","fa":"One of Europe's biggest metal and hard rock festivals, held in Clisson"},
    {"n":"Benicassim Festival","loc":"Spain","at":"tens of thousands annually","fa":"A seaside Spanish festival known for combining indie music with beach camping"},
    {"n":"Fusion Festival","loc":"Germany","at":"around 70,000 attendees","fa":"A non-commercial German festival known for its lack of sponsorship branding on site"},
    {"n":"Splendour in the Grass","loc":"Australia","at":"around 40,000 attendees","fa":"One of Australia's largest contemporary music festivals"},
    {"n":"Byron Bay Bluesfest","loc":"Australia","at":"tens of thousands over the Easter weekend","fa":"A long-running festival celebrating blues and roots music over the Easter weekend"},
    {"n":"WOMAD","loc":"United Kingdom","at":"tens of thousands, varies by host country","fa":"Stands for 'World of Music, Arts and Dance', co-founded by Peter Gabriel to celebrate global music"},
    {"n":"Cropredy Festival","loc":"United Kingdom","at":"around 20,000 attendees","fa":"An English folk-rock festival founded by the band Fairport Convention"},
    {"n":"Cambridge Folk Festival","loc":"United Kingdom","at":"around 14,000 attendees","fa":"One of the longest-running folk festivals in the world, since 1965"},
    {"n":"Newport Folk Festival","loc":"United States","at":"around 10,000 attendees, capped by venue size","fa":"Famous for Bob Dylan's controversial 1965 performance with an electric guitar"},
    {"n":"Newport Jazz Festival","loc":"United States","at":"around 10,000 attendees, capped by venue size","fa":"Founded in 1954, one of the earliest and most influential outdoor jazz festivals"},
    {"n":"Monterey Pop Festival","loc":"United States","at":"an estimated 200,000 including non-ticketed crowds","fa":"The 1967 festival launched the careers of Jimi Hendrix and Janis Joplin in the US"},
    {"n":"Altamont Free Concert","loc":"United States","at":"around 300,000 attendees","fa":"A 1969 event marred by violence, often cited as marking the end of the 1960s counterculture era"},
    {"n":"Live Aid","loc":"United Kingdom / United States","at":"around 172,000 combined across both venues","fa":"A 1985 dual-venue benefit concert watched by an estimated 1.9 billion people on television"},
    {"n":"Farm Aid","loc":"United States","at":"tens of thousands annually","fa":"An annual benefit concert founded in 1985 to raise awareness for American family farmers"},
    {"n":"Latitude Festival","loc":"United Kingdom","at":"around 40,000 attendees","fa":"Combines music with comedy, theatre, and literature in the English countryside"},
    {"n":"TRNSMT Festival","loc":"United Kingdom","at":"around 50,000 per day","fa":"A Scottish music festival held in Glasgow's Glasgow Green park"},
    {"n":"Pinkpop Festival","loc":"Netherlands","at":"around 60,000 attendees","fa":"One of the oldest annually held pop festivals in the world, since 1970"},
    {"n":"Lowlands Festival","loc":"Netherlands","at":"around 55,000 attendees, its official capacity","fa":"A major Dutch festival known for its eclectic and adventurous lineup"},
    {"n":"Nos Alive","loc":"Portugal","at":"around 200,000 over the event","fa":"A Lisbon riverside festival known for blending major international headliners with local acts"},
    {"n":"Way Out West","loc":"Sweden","at":"around 30,000 attendees","fa":"A Gothenburg festival known for its fully vegetarian food policy"},
    {"n":"Sonar Festival","loc":"Spain","at":"around 120,000 attendees","fa":"A Barcelona festival focused on electronic music and digital art"},
    {"n":"Mawazine","loc":"Morocco","at":"several million over the full event, among the largest free festivals in the world","fa":"One of the largest music festivals in Africa, held in Rabat"},
    {"n":"Cape Town International Jazz Festival","loc":"South Africa","at":"around 34,000 attendees","fa":"Known as 'Africa's Grandest Gathering', held annually in Cape Town"},
    {"n":"Summer Sonic","loc":"Japan","at":"around 230,000 combined across both cities","fa":"A major Japanese festival held simultaneously in Tokyo and Osaka"},
    {"n":"Clockenflap","loc":"Hong Kong","at":"tens of thousands over the weekend","fa":"Hong Kong's largest outdoor music and arts festival"},
    {"n":"Head in the Clouds","loc":"United States","at":"tens of thousands annually","fa":"A festival celebrating Asian and Asian-American artists across genres"},
    {"n":"Osheaga","loc":"Canada","at":"around 135,000 over the weekend","fa":"A major Montreal festival held on an island in the St. Lawrence River"},
    {"n":"Squamish Valley Music Festival","loc":"Canada","at":"tens of thousands annually","fa":"A Canadian festival held against the backdrop of the Coast Mountains"},
    {"n":"Vive Latino","loc":"Mexico","at":"around 220,000 over the weekend","fa":"One of the largest Spanish-language rock and pop festivals in the world"},
    {"n":"Corona Capital","loc":"Mexico","at":"around 195,000 over the weekend","fa":"A major Mexico City festival known for booking international headliners"},
    {"n":"Lollapalooza Argentina","loc":"Argentina","at":"around 300,000 over the weekend","fa":"The South American edition of the Lollapalooza brand, held in Buenos Aires"},
    {"n":"Rock al Parque","loc":"Colombia","at":"around 350,000 over the weekend","fa":"One of the largest free outdoor rock festivals in the world, held in Bogota"},
    {"n":"Vina del Mar Festival","loc":"Chile","at":"around 15,000 per night in-venue, watched by millions on TV","fa":"One of the longest-running and most-watched music festivals in Latin America"},
    {"n":"Meredith Music Festival","loc":"Australia","at":"around 13,000 attendees, capped by venue size","fa":"A boutique Australian festival held on a natural amphitheater called the Supernatural Amphitheatre"},
    {"n":"Falls Festival","loc":"Australia","at":"tens of thousands across venues","fa":"A New Year's Eve music festival held across multiple Australian coastal towns"},
    {"n":"Open'er Festival","loc":"Poland","at":"around 140,000 over the event","fa":"Held at a former military airfield in Gdynia, one of Poland's biggest music festivals"},
    {"n":"Snowbombing","loc":"Austria","at":"around 8,000 attendees","fa":"A festival combining snowboarding and skiing with live music performances on a mountain"},
    {"n":"Electric Forest","loc":"United States","at":"around 45,000 attendees","fa":"Held in a forest in Michigan known for elaborate light installations among the trees"},
    {"n":"Firefly Music Festival","loc":"United States","at":"around 90,000 attendees","fa":"Held in a wooded state park in Delaware"},
    {"n":"Governors Ball","loc":"United States","at":"around 180,000 over the weekend","fa":"An annual festival held on Randall's Island in New York City"},
    {"n":"Panorama Music Festival","loc":"United States","at":"tens of thousands over the weekend","fa":"A New York City festival known for blending music with art installations"},
    {"n":"Ozzfest","loc":"United States","at":"tens of thousands per tour stop","fa":"A touring heavy metal festival founded by Ozzy and Sharon Osbourne in 1996"},
    {"n":"Warped Tour","loc":"United States","at":"tens of thousands per tour stop","fa":"A long-running touring festival that helped launch many punk and pop-punk bands"},
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
    total = len(festivals)
    found = 0
    for i, s in enumerate(festivals):
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
    out = Path("assets/music/music_festivals.json")
    out.write_text(json.dumps(festivals, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    summary = "\nDone: {}/{} images -- {} festivals total.\n".format(found, total, total)
    sys.stdout.buffer.write(summary.encode("utf-8"))

if __name__ == "__main__":
    main()
