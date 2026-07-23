import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote
sys.stdout.reconfigure(encoding="utf-8")

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Wikipedia page title overrides for ambiguous album titles
WIKI_EN = {
    "Thriller": "Thriller (album)",
    "Rumours": "Rumours (album)",
    "Purple Rain": "Purple Rain (album)",
    "What's Going On": "What's Going On (album)",
    "Like a Prayer": "Like a Prayer (album)",
    "A Night at the Opera": "A Night at the Opera (Queen album)",
    "Bad": "Bad (album)",
    "Dangerous": "Dangerous (Michael Jackson album)",
    "HIStory": "HIStory: Past, Present and Future, Book I",
    "Legend": "Legend (Bob Marley album)",
    "Exodus": "Exodus (Bob Marley and the Wailers album)",
    "21": "21 (Adele album)",
    "25": "25 (Adele album)",
    "1989": "1989 (Taylor Swift album)",
    "Ten": "Ten (Pearl Jam album)",
    "Confessions": "Confessions (Usher album)",
    "Recovery": "Recovery (Eminem album)",
    "Blue": "Blue (Joni Mitchell album)",
    "Voodoo": "Voodoo (D'Angelo album)",
    "Arrival": "Arrival (ABBA album)",
    "Tapestry": "Tapestry (Carole King album)",
    "1984": "1984 (Van Halen album)",
    "Nation of Millions": "It Takes a Nation of Millions to Hold Us Back",
    "Doolittle": "Doolittle (album)",
    "The Bodyguard: Original Soundtrack Album": "The Bodyguard (soundtrack)",
    "A Night at the Opera": "A Night at the Opera (album)",
    "Hysteria": "Hysteria (Def Leppard album)",
    "Metallica (The Black Album)": "Metallica (album)",
    "Music Box": "Music Box (Mariah Carey album)",
    "Saturday Night Fever": "Saturday Night Fever (soundtrack)",
    "Dirty Dancing: Original Soundtrack": "Dirty Dancing (soundtrack)",
    "Titanic: Music from the Motion Picture": "Titanic: Music from the Motion Picture",
}

# n=title, ar=artist, yr=year, sa=estimated worldwide sales, fa=famous_for
albums = [
    {"n":"Thriller","ar":"Michael Jackson","yr":1982,"sa":"over 70 million copies","fa":"Best-selling album of all time, won a record 8 Grammy Awards"},
    {"n":"The Dark Side of the Moon","ar":"Pink Floyd","yr":1973,"sa":"over 45 million copies","fa":"Stayed on the Billboard 200 chart for over 900 weeks"},
    {"n":"Abbey Road","ar":"The Beatles","yr":1969,"sa":"over 30 million copies","fa":"The Beatles' last recorded album, famous for its zebra-crossing cover"},
    {"n":"Back in Black","ar":"AC/DC","yr":1980,"sa":"over 50 million copies","fa":"One of the best-selling albums in history, recorded after the death of singer Bon Scott"},
    {"n":"Rumours","ar":"Fleetwood Mac","yr":1977,"sa":"over 40 million copies","fa":"Written amid the band members' breakups, became one of the best-selling albums ever"},
    {"n":"Nevermind","ar":"Nirvana","yr":1991,"sa":"over 30 million copies","fa":"Brought grunge into the mainstream, led by the single 'Smells Like Teen Spirit'"},
    {"n":"Purple Rain","ar":"Prince","yr":1984,"sa":"over 25 million copies","fa":"Soundtrack to Prince's film of the same name, blended rock, funk and pop"},
    {"n":"Bad","ar":"Michael Jackson","yr":1987,"sa":"over 45 million copies","fa":"First album in history to produce five number-one singles on the Billboard Hot 100"},
    {"n":"Dangerous","ar":"Michael Jackson","yr":1991,"sa":"over 32 million copies","fa":"Blended new jack swing with pop, produced the hit 'Black or White'"},
    {"n":"Songs in the Key of Life","ar":"Stevie Wonder","yr":1976,"sa":"over 10 million copies","fa":"A double album widely considered one of the greatest of all time"},
    {"n":"What's Going On","ar":"Marvin Gaye","yr":1971,"sa":"modest sales at release, several million since","fa":"A concept album addressing war, poverty and social injustice"},
    {"n":"Pet Sounds","ar":"The Beach Boys","yr":1966,"sa":"modest initial sales, over 1 million since","fa":"Pioneered studio production techniques that influenced generations of artists despite underperforming at release"},
    {"n":"Led Zeppelin IV","ar":"Led Zeppelin","yr":1971,"sa":"over 37 million copies","fa":"Contains 'Stairway to Heaven', one of the most played rock songs in history"},
    {"n":"Appetite for Destruction","ar":"Guns N' Roses","yr":1987,"sa":"over 30 million copies","fa":"Best-selling debut album of all time in the United States"},
    {"n":"The Wall","ar":"Pink Floyd","yr":1979,"sa":"over 30 million copies","fa":"A rock opera later adapted into a feature film"},
    {"n":"Hotel California","ar":"Eagles","yr":1976,"sa":"over 40 million copies","fa":"Its title track is one of the most iconic rock songs ever recorded"},
    {"n":"Born in the U.S.A.","ar":"Bruce Springsteen","yr":1984,"sa":"over 30 million copies","fa":"Produced seven top-10 singles, a record for a rock album"},
    {"n":"Born to Run","ar":"Bruce Springsteen","yr":1975,"sa":"over 6 million copies","fa":"The album that made Springsteen a national star in the US"},
    {"n":"Like a Prayer","ar":"Madonna","yr":1989,"sa":"over 15 million copies","fa":"Blended pop with gospel choirs and sparked controversy for its religious imagery"},
    {"n":"Off the Wall","ar":"Michael Jackson","yr":1979,"sa":"over 20 million copies","fa":"Marked Jackson's transition into a solo disco-pop superstar"},
    {"n":"HIStory","ar":"Michael Jackson","yr":1995,"sa":"over 20 million copies","fa":"A double album pairing greatest hits with new material"},
    {"n":"Sgt. Pepper's Lonely Hearts Club Band","ar":"The Beatles","yr":1967,"sa":"over 30 million copies","fa":"Considered one of the first concept albums in rock history"},
    {"n":"Blue","ar":"Joni Mitchell","yr":1971,"sa":"modest sales, several million since release","fa":"A deeply confessional folk album ranked among the greatest ever made"},
    {"n":"Kind of Blue","ar":"Miles Davis","yr":1959,"sa":"over 5 million copies","fa":"The best-selling jazz album of all time"},
    {"n":"Are You Experienced","ar":"The Jimi Hendrix Experience","yr":1967,"sa":"several million copies","fa":"Redefined the possibilities of the electric guitar"},
    {"n":"Exodus","ar":"Bob Marley and the Wailers","yr":1977,"sa":"several million copies","fa":"Named 'Album of the Century' by Time magazine in 1999"},
    {"n":"Legend","ar":"Bob Marley and the Wailers","yr":1984,"sa":"over 30 million copies","fa":"A greatest-hits compilation and the best-selling reggae album ever"},
    {"n":"21","ar":"Adele","yr":2011,"sa":"over 30 million copies","fa":"One of the best-selling albums of the 21st century, won 6 Grammy Awards"},
    {"n":"25","ar":"Adele","yr":2015,"sa":"over 22 million copies","fa":"Sold over 3 million copies in the US in its first week alone"},
    {"n":"Random Access Memories","ar":"Daft Punk","yr":2013,"sa":"over 4 million copies","fa":"Won Album of the Year at the Grammys, revived interest in live disco instrumentation"},
    {"n":"The Miseducation of Lauryn Hill","ar":"Lauryn Hill","yr":1998,"sa":"over 19 million copies","fa":"Blended hip-hop, soul and reggae, swept the Grammy Awards"},
    {"n":"Innervisions","ar":"Stevie Wonder","yr":1973,"sa":"several million copies","fa":"A socially conscious album recorded almost entirely by Wonder himself"},
    {"n":"Automatic for the People","ar":"R.E.M.","yr":1992,"sa":"over 18 million copies","fa":"A reflective, acoustic-leaning album that became a career high point"},
    {"n":"1989","ar":"Taylor Swift","yr":2014,"sa":"over 14 million copies","fa":"Marked Swift's full transition from country to pop, won Album of the Year"},
    {"n":"Nation of Millions","ar":"Public Enemy","yr":1988,"sa":"modest sales, over 1 million since","fa":"A landmark politically charged hip-hop album"},
    {"n":"Illmatic","ar":"Nas","yr":1994,"sa":"modest sales, roughly 2 million since","fa":"Widely considered one of the greatest hip-hop albums ever released"},
    {"n":"The Chronic","ar":"Dr. Dre","yr":1992,"sa":"over 3 million copies","fa":"Popularized G-funk and reshaped West Coast hip-hop"},
    {"n":"Ready to Die","ar":"The Notorious B.I.G.","yr":1994,"sa":"over 4 million copies","fa":"A landmark East Coast hip-hop debut album"},
    {"n":"The Marshall Mathers LP","ar":"Eminem","yr":2000,"sa":"over 35 million copies","fa":"One of the best-selling hip-hop albums ever, won Best Rap Album at the Grammys"},
    {"n":"The Eminem Show","ar":"Eminem","yr":2002,"sa":"over 27 million copies","fa":"Best-selling album worldwide in 2002"},
    {"n":"Recovery","ar":"Eminem","yr":2010,"sa":"over 7 million copies","fa":"Best-selling album worldwide in 2010"},
    {"n":"Confessions","ar":"Usher","yr":2004,"sa":"over 10 million copies","fa":"One of the best-selling R&B albums of the 2000s"},
    {"n":"Voodoo","ar":"D'Angelo","yr":2000,"sa":"modest sales, roughly 2 million since","fa":"A critically acclaimed neo-soul album years in the making"},
    {"n":"OK Computer","ar":"Radiohead","yr":1997,"sa":"over 8 million copies","fa":"A genre-defying album often cited as one of the greatest of the 1990s"},
    {"n":"Doolittle","ar":"Pixies","yr":1989,"sa":"modest sales, gold-certified in the US","fa":"Highly influential on the alternative rock movement of the 1990s despite modest initial sales"},
    {"n":"Rocket to Russia","ar":"Ramones","yr":1977,"sa":"modest sales, never charted highly","fa":"A defining record of the punk rock movement despite low initial commercial impact"},
    {"n":"London Calling","ar":"The Clash","yr":1979,"sa":"over 5 million copies","fa":"Blended punk with reggae, ska and rockabilly influences"},
    {"n":"Tapestry","ar":"Carole King","yr":1971,"sa":"over 25 million copies","fa":"One of the best-selling albums by a female singer-songwriter"},
    {"n":"Bridge Over Troubled Water","ar":"Simon & Garfunkel","yr":1970,"sa":"over 25 million copies","fa":"The duo's final studio album and their biggest commercial success"},
    {"n":"Bat Out of Hell","ar":"Meat Loaf","yr":1977,"sa":"over 43 million copies","fa":"One of the best-selling albums ever, blended rock with theatrical storytelling"},
    {"n":"Jagged Little Pill","ar":"Alanis Morissette","yr":1995,"sa":"over 33 million copies","fa":"Best-selling studio album ever by a female Canadian artist"},
    {"n":"Come Away with Me","ar":"Norah Jones","yr":2002,"sa":"over 27 million copies","fa":"Won Album of the Year at the Grammys, blended jazz, pop and folk"},
    {"n":"Come On Over","ar":"Shania Twain","yr":1997,"sa":"over 40 million copies","fa":"Best-selling studio album by a female artist in country music history"},
    {"n":"The Bodyguard: Original Soundtrack Album","ar":"Whitney Houston","yr":1992,"sa":"over 45 million copies","fa":"Best-selling soundtrack album of all time, featuring 'I Will Always Love You'"},
    {"n":"Falling into You","ar":"Celine Dion","yr":1996,"sa":"over 32 million copies","fa":"Won the Grammy for Album of the Year"},
    {"n":"Let's Talk About Love","ar":"Celine Dion","yr":1997,"sa":"over 31 million copies","fa":"Features 'My Heart Will Go On' from the film Titanic"},
    {"n":"A Night at the Opera","ar":"Queen","yr":1975,"sa":"over 6 million copies","fa":"Home to 'Bohemian Rhapsody', one of the most celebrated rock songs ever written"},
    {"n":"(What's the Story) Morning Glory?","ar":"Oasis","yr":1995,"sa":"over 22 million copies","fa":"One of the best-selling albums in UK chart history"},
    {"n":"Achtung Baby","ar":"U2","yr":1991,"sa":"over 18 million copies","fa":"Marked a reinvention of U2's sound with industrial and electronic influences"},
    {"n":"The Joshua Tree","ar":"U2","yr":1987,"sa":"over 25 million copies","fa":"Propelled U2 to global superstardom, won Album of the Year at the Grammys"},
    {"n":"1984","ar":"Van Halen","yr":1984,"sa":"over 10 million copies","fa":"Features the synthesizer-driven hit 'Jump'"},
    {"n":"Hysteria","ar":"Def Leppard","yr":1987,"sa":"over 25 million copies","fa":"Took nearly three years to record, produced seven hit singles"},
    {"n":"Slippery When Wet","ar":"Bon Jovi","yr":1986,"sa":"over 28 million copies","fa":"The album that turned Bon Jovi into a global arena-rock act"},
    {"n":"Metallica (The Black Album)","ar":"Metallica","yr":1991,"sa":"over 30 million copies","fa":"Brought thrash metal into the mainstream, one of the best-selling albums of the SoundScan era"},
    {"n":"Master of Puppets","ar":"Metallica","yr":1986,"sa":"over 6 million copies","fa":"Widely regarded as one of the greatest heavy metal albums ever recorded"},
    {"n":"Ten","ar":"Pearl Jam","yr":1991,"sa":"over 13 million copies","fa":"A defining album of the early 1990s grunge movement"},
    {"n":"Tragic Kingdom","ar":"No Doubt","yr":1995,"sa":"over 16 million copies","fa":"Blended ska, pop and rock, launched Gwen Stefani to stardom"},
    {"n":"Hybrid Theory","ar":"Linkin Park","yr":2000,"sa":"over 30 million copies","fa":"Best-selling debut album of the 2000s in the United States"},
    {"n":"Music Box","ar":"Mariah Carey","yr":1993,"sa":"over 28 million copies","fa":"Features 'Hero' and 'Without You', among Carey's best-known ballads"},
    {"n":"Cracked Rear View","ar":"Hootie & the Blowfish","yr":1994,"sa":"over 21 million copies","fa":"One of the best-selling debut albums in US history"},
    {"n":"No Fences","ar":"Garth Brooks","yr":1990,"sa":"over 20 million copies","fa":"Features 'Friends in Low Places', a defining country anthem of the 1990s"},
    {"n":"Confessions on a Dance Floor","ar":"Madonna","yr":2005,"sa":"over 10 million copies","fa":"A continuous dance-mixed album that revitalized Madonna's chart success"},
    {"n":"Saturday Night Fever","ar":"Various Artists / Bee Gees","yr":1977,"sa":"over 40 million copies","fa":"Defined the disco era and remained the best-selling soundtrack for over a decade"},
    {"n":"Dirty Dancing: Original Soundtrack","ar":"Various Artists","yr":1987,"sa":"over 32 million copies","fa":"One of the best-selling film soundtracks of the 1980s"},
    {"n":"Titanic: Music from the Motion Picture","ar":"James Horner / Celine Dion","yr":1997,"sa":"over 30 million copies","fa":"One of the best-selling orchestral film soundtracks ever released"},
    {"n":"Voulez-Vous","ar":"ABBA","yr":1979,"sa":"over 6 million copies","fa":"Includes the disco hit 'Gimme! Gimme! Gimme! (A Man After Midnight)'"},
    {"n":"Arrival","ar":"ABBA","yr":1976,"sa":"over 8 million copies","fa":"Includes the group's signature hit 'Dancing Queen'"},
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
    total = len(albums)
    found = 0
    for i, s in enumerate(albums):
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
    out = Path("assets/music/albums.json")
    out.write_text(json.dumps(albums, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    summary = "\nDone: {}/{} images -- {} albums total.\n".format(found, total, total)
    sys.stdout.buffer.write(summary.encode("utf-8"))

if __name__ == "__main__":
    main()
