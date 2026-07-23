import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote
sys.stdout.reconfigure(encoding="utf-8")

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_EN = {
    "Thriller": "Thriller (album)",
    "Rumours": "Rumours (album)",
    "Bridge Over Troubled Water": "Bridge Over Troubled Water (song)",
    "Tapestry": "Tapestry (Carole King album)",
    "Graceland": "Graceland (album)",
    "The Bodyguard": "The Bodyguard (soundtrack)",
    "21": "21 (Adele album)",
    "25": "25 (Adele album)",
    "Uptown Funk": "Uptown Funk",
    "Rolling in the Deep": "Rolling in the Deep",
    "Shallow": "Shallow (Lady Gaga and Bradley Cooper song)",
    "We Are the World": "We Are the World",
    "Rehab": "Rehab (song)",
    "Waterloo": "Waterloo (ABBA song)",
    "Euphoria": "Euphoria (Loreen song)",
    "Tattoo": "Tattoo (Loreen song)",
    "Zitti e Buoni": "Zitti e Buoni",
    "Take On Me": "Take On Me",
    "Sledgehammer": "Sledgehammer (song)",
}

# n=title, ar=artist, aw=award, yr=year, fa=context/why notable
awards = [
    {"n":"Thriller","ar":"Michael Jackson","aw":"Grammy Award for Album of the Year","yr":1984,"fa":"Also won 6 other Grammys that night, an 8-award haul that remains a record for a single ceremony"},
    {"n":"Rumours","ar":"Fleetwood Mac","aw":"Grammy Award for Album of the Year","yr":1978,"fa":"Won despite the band members going through simultaneous breakups during recording"},
    {"n":"Bridge Over Troubled Water","ar":"Simon & Garfunkel","aw":"Grammy Award for Album of the Year","yr":1971,"fa":"The duo's final studio album together, also winning Record and Song of the Year that night"},
    {"n":"Tapestry","ar":"Carole King","aw":"Grammy Award for Album of the Year","yr":1972,"fa":"Made King one of the first women to win the Grammy for Album of the Year"},
    {"n":"Graceland","ar":"Paul Simon","aw":"Grammy Award for Album of the Year","yr":1987,"fa":"Blended South African musical styles with Simon's songwriting, sparking debate over its production during apartheid"},
    {"n":"The Bodyguard","ar":"Whitney Houston","aw":"Grammy Award for Album of the Year","yr":1994,"fa":"Remains the best-selling soundtrack album of all time"},
    {"n":"Jagged Little Pill","ar":"Alanis Morissette","aw":"Grammy Award for Album of the Year","yr":1996,"fa":"Made Morissette the youngest woman to win Album of the Year at the time"},
    {"n":"The Miseducation of Lauryn Hill","ar":"Lauryn Hill","aw":"Grammy Award for Album of the Year","yr":1999,"fa":"Made Hill the first woman to win five Grammys in a single night"},
    {"n":"21","ar":"Adele","aw":"Grammy Award for Album of the Year","yr":2012,"fa":"The album swept all six categories it was nominated in that year"},
    {"n":"25","ar":"Adele","aw":"Grammy Award for Album of the Year","yr":2017,"fa":"Made Adele the first artist to win Album of the Year twice for consecutive studio albums"},
    {"n":"When We All Fall Asleep, Where Do We Go?","ar":"Billie Eilish","aw":"Grammy Award for Album of the Year","yr":2020,"fa":"Made Eilish, at 18, the youngest person to win Album of the Year"},
    {"n":"Speakerboxxx/The Love Below","ar":"OutKast","aw":"Grammy Award for Album of the Year","yr":2004,"fa":"Remains one of the only hip-hop albums ever to win Album of the Year"},
    {"n":"Rolling in the Deep","ar":"Adele","aw":"Grammy Award for Record of the Year","yr":2012,"fa":"Became one of the best-selling singles of the 2010s worldwide"},
    {"n":"Uptown Funk","ar":"Mark Ronson featuring Bruno Mars","aw":"Grammy Award for Record of the Year","yr":2016,"fa":"Spent 14 weeks at number one on the Billboard Hot 100"},
    {"n":"We Are the World","ar":"USA for Africa","aw":"Grammy Award for Record of the Year and Song of the Year","yr":1986,"fa":"Recorded by dozens of major artists in one night to raise funds for famine relief in Africa"},
    {"n":"Shallow","ar":"Lady Gaga and Bradley Cooper","aw":"Grammy Award for Best Song Written for Visual Media","yr":2019,"fa":"Written for the film 'A Star Is Born', also won the Academy Award for Best Original Song"},
    {"n":"Rehab","ar":"Amy Winehouse","aw":"Grammy Award for Record of the Year and Song of the Year","yr":2008,"fa":"Winehouse also won Best New Artist that same night, a rare triple win"},
    {"n":"Fallin'","ar":"Alicia Keys","aw":"Grammy Award for Song of the Year","yr":2002,"fa":"Part of a five-Grammy sweep for Keys' debut album that year"},
    {"n":"Waterloo","ar":"ABBA","aw":"Eurovision Song Contest winner","yr":1974,"fa":"The win launched ABBA's international career after representing Sweden"},
    {"n":"Ne partez pas sans moi","ar":"Celine Dion","aw":"Eurovision Song Contest winner","yr":1988,"fa":"Dion won representing Switzerland despite being Canadian, as Eurovision rules did not require nationality to match"},
    {"n":"Rise Like a Phoenix","ar":"Conchita Wurst","aw":"Eurovision Song Contest winner","yr":2014,"fa":"Wurst's win for Austria became a widely discussed moment for LGBTQ visibility in Europe"},
    {"n":"Euphoria","ar":"Loreen","aw":"Eurovision Song Contest winner","yr":2012,"fa":"One of the highest-scoring Eurovision winners of the modern voting era"},
    {"n":"Tattoo","ar":"Loreen","aw":"Eurovision Song Contest winner","yr":2023,"fa":"Made Loreen the first woman and only the second act ever to win Eurovision twice"},
    {"n":"Zitti e Buoni","ar":"Maneskin","aw":"Eurovision Song Contest winner","yr":2021,"fa":"The Italian rock band's win led to a major surge in their international popularity"},
    {"n":"Molitva","ar":"Marija Serifovic","aw":"Eurovision Song Contest winner","yr":2007,"fa":"Won representing Serbia in the country's first Eurovision entry as an independent nation"},
    {"n":"Hard Rock Hallelujah","ar":"Lordi","aw":"Eurovision Song Contest winner","yr":2006,"fa":"The first hard rock and monster-costumed act ever to win Eurovision, representing Finland"},
    {"n":"Take On Me","ar":"a-ha","aw":"MTV Video Music Award for Best New Artist in a Video","yr":1986,"fa":"Its pioneering pencil-sketch animation style became one of the most recognized music videos ever made"},
    {"n":"Sledgehammer","ar":"Peter Gabriel","aw":"MTV Video Music Award for Video of the Year","yr":1987,"fa":"Won a record nine VMAs in a single night for its stop-motion animation techniques"},
    {"n":"Single Ladies (Put a Ring on It)","ar":"Beyonce","aw":"MTV Video Music Award for Video of the Year","yr":2009,"fa":"Its simple choreography became one of the most imitated dance routines in pop culture"},
    {"n":"Formation","ar":"Beyonce","aw":"MTV Video Music Award for Video of the Year","yr":2016,"fa":"Addressed themes of Black identity and Southern heritage in its visuals"},
    {"n":"Bad Guy","ar":"Billie Eilish","aw":"MTV Video Music Award for Video of the Year","yr":2019,"fa":"Part of a breakout year that also saw Eilish sweep the top Grammy categories"},
    {"n":"The Beatles","ar":"The Beatles","aw":"Rock and Roll Hall of Fame induction","yr":1988,"fa":"Inducted in the Hall of Fame's third year of existence"},
    {"n":"Elvis Presley","ar":"Elvis Presley","aw":"Rock and Roll Hall of Fame induction","yr":1986,"fa":"One of the 10 inaugural inductees in the Hall of Fame's very first class"},
    {"n":"Chuck Berry","ar":"Chuck Berry","aw":"Rock and Roll Hall of Fame induction","yr":1986,"fa":"Also part of the inaugural 1986 induction class"},
    {"n":"Aretha Franklin","ar":"Aretha Franklin","aw":"Rock and Roll Hall of Fame induction","yr":1987,"fa":"The first woman ever inducted into the Rock and Roll Hall of Fame"},
    {"n":"Queen","ar":"Queen","aw":"Rock and Roll Hall of Fame induction","yr":2001,"fa":"Inducted by Metallica's James Hetfield, who cited their influence on hard rock"},
    {"n":"Nirvana","ar":"Nirvana","aw":"Rock and Roll Hall of Fame induction","yr":2014,"fa":"Became eligible and inducted in their first year of eligibility, 25 years after their debut release"},
    {"n":"Madonna","ar":"Madonna","aw":"Rock and Roll Hall of Fame induction","yr":2008,"fa":"Inducted in her first year of eligibility"},
    {"n":"ABBA","ar":"ABBA","aw":"Rock and Roll Hall of Fame induction","yr":2010,"fa":"Inducted decades after the group's initial breakup and reunion-free years"},
    {"n":"Tina Turner","ar":"Tina Turner","aw":"Rock and Roll Hall of Fame induction (solo)","yr":2021,"fa":"Inducted a second time as a solo artist, having already entered with Ike & Tina Turner in 1991"},
    {"n":"Bob Marley","ar":"Bob Marley","aw":"Rock and Roll Hall of Fame induction","yr":1994,"fa":"The first reggae artist ever inducted into the Hall of Fame"},
    {"n":"Michael Jackson","ar":"Michael Jackson","aw":"Rock and Roll Hall of Fame induction (solo)","yr":2001,"fa":"Inducted separately as a solo artist after already entering with the Jackson 5 in 1997"},
    {"n":"Whitney Houston","ar":"Whitney Houston","aw":"Rock and Roll Hall of Fame induction","yr":2020,"fa":"Inducted in her first year of eligibility"},
    {"n":"Beyonce","ar":"Beyonce","aw":"Grammy record for most wins by any artist","yr":2023,"fa":"Surpassed the previous all-time record for total career Grammy wins"},
    {"n":"Beethoven's Ninth Symphony","ar":"Ludwig van Beethoven","aw":"Grammy Hall of Fame induction","yr":1998,"fa":"One of many classical works later added to the Grammy Hall of Fame honoring historically significant recordings"},
    {"n":"Rapper's Delight","ar":"The Sugarhill Gang","aw":"Grammy Hall of Fame induction","yr":2013,"fa":"Recognized as one of the first hip-hop songs to reach a mainstream audience"},
    {"n":"Respect","ar":"Aretha Franklin","aw":"Grammy Hall of Fame induction","yr":1987,"fa":"Franklin's version became an anthem for both civil rights and feminism"},
    {"n":"Like a Rolling Stone","ar":"Bob Dylan","aw":"Grammy Hall of Fame induction","yr":1999,"fa":"Frequently cited by critics as one of the greatest songs ever recorded"},
    {"n":"Billie Jean","ar":"Michael Jackson","aw":"Grammy Hall of Fame induction","yr":2004,"fa":"Its music video was among the first by a Black artist given heavy rotation on MTV"},
    {"n":"Purple Rain","ar":"Prince","aw":"Academy Award for Best Original Song Score","yr":1985,"fa":"Won for the film of the same name, one of the few pop artists to win this Academy Award category"},
    {"n":"Falling Slowly","ar":"Glen Hansard and Marketa Irglova","aw":"Academy Award for Best Original Song","yr":2008,"fa":"Written for the low-budget Irish film 'Once', a rare independent film win in this category"},
    {"n":"My Heart Will Go On","ar":"Celine Dion","aw":"Academy Award for Best Original Song","yr":1998,"fa":"Written for the film Titanic, became one of the best-selling singles of the 1990s"},
    {"n":"Let It Go","ar":"Idina Menzel","aw":"Academy Award for Best Original Song","yr":2014,"fa":"Written for Disney's 'Frozen', became a global cultural phenomenon among children's songs"},
    {"n":"Bridge Over Troubled Water (song)","ar":"Simon & Garfunkel","aw":"Grammy Award for Song of the Year","yr":1971,"fa":"Considered one of the duo's defining songs, later covered by numerous other artists"},
    {"n":"Kendrick Lamar's DAMN.","ar":"Kendrick Lamar","aw":"Pulitzer Prize for Music","yr":2018,"fa":"Made Lamar the first artist outside classical or jazz music to win the Pulitzer Prize for Music"},
    {"n":"Bob Dylan's Body of Work","ar":"Bob Dylan","aw":"Nobel Prize in Literature","yr":2016,"fa":"Made Dylan the first musician ever to win the Nobel Prize in Literature"},
    {"n":"Freddie Mercury and Queen","ar":"Queen","aw":"Brit Award for Outstanding Contribution to Music","yr":1990,"fa":"Recognized for the band's decades-long impact on British popular music"},
    {"n":"Adele's Brit Sweep","ar":"Adele","aw":"Brit Award for British Album of the Year","yr":2012,"fa":"Adele's '21' won at the Brits the same year it dominated the Grammys"},
    {"n":"Amy Winehouse's Brit Win","ar":"Amy Winehouse","aw":"Brit Award for British Female Solo Artist","yr":2007,"fa":"Part of a run of British and American awards recognizing 'Back to Black'"},
    {"n":"Harry Styles' Brit Sweep","ar":"Harry Styles","aw":"Brit Award for Album of the Year","yr":2023,"fa":"His album 'Harry's House' also topped charts in multiple countries simultaneously"},
    {"n":"Ed Sheeran's Brit Record","ar":"Ed Sheeran","aw":"Brit Award for British Male Solo Artist","yr":2015,"fa":"One of several Brit wins across Sheeran's career for his chart-topping albums"},
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
    total = len(awards)
    found = 0
    for i, s in enumerate(awards):
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
    out = Path("assets/music/music_awards.json")
    out.write_text(json.dumps(awards, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    summary = "\nDone: {}/{} images -- {} awards total.\n".format(found, total, total)
    sys.stdout.buffer.write(summary.encode("utf-8"))

if __name__ == "__main__":
    main()
