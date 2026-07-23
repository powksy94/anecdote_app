import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote
sys.stdout.reconfigure(encoding="utf-8")

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Wikipedia page title overrides for ambiguous names
WIKI_EN = {
    "Nirvana": "Nirvana (band)",
}

# n=name, gn=genre, fa=famous_for, wl=warning_level ("red"/"orange", optional), wi=warning_text (optional)
legends = [
    {"n":"Elvis Presley","gn":"Rock and Roll","fa":"Known as 'The King', helped bring rock and roll into the mainstream in the 1950s",
     "wl":"orange","wi":"Began a relationship with his future wife Priscilla when she was 14 and he was 24; they married once she turned 21"},
    {"n":"The Beatles","gn":"Rock/Pop","fa":"Best-selling band in history, redefined popular music and studio recording"},
    {"n":"Michael Jackson","gn":"Pop","fa":"'King of Pop', Thriller remains the best-selling album of all time",
     "wl":"red","wi":"Faced multiple child sexual abuse allegations throughout his career; settled civil suits and was acquitted in a 2005 criminal trial"},
    {"n":"Bob Marley","gn":"Reggae","fa":"Brought reggae music to a worldwide audience, icon of peace and unity"},
    {"n":"Freddie Mercury","gn":"Rock","fa":"Queen's frontman, wrote 'Bohemian Rhapsody' and one of rock's greatest live performers"},
    {"n":"Madonna","gn":"Pop","fa":"'Queen of Pop', best-selling female recording artist of all time"},
    {"n":"David Bowie","gn":"Rock/Glam","fa":"Constant reinvention through personas like Ziggy Stardust, hugely influential on music and fashion",
     "wl":"orange","wi":"Several women have described underage sexual encounters with him in the 1970s; he was never criminally charged"},
    {"n":"Jimi Hendrix","gn":"Rock","fa":"Widely regarded as the greatest electric guitarist in music history"},
    {"n":"Prince","gn":"Funk/Pop","fa":"Multi-instrumentalist known for genre-blending and his album 'Purple Rain'"},
    {"n":"Whitney Houston","gn":"Pop/R&B","fa":"One of the best-selling music artists of all time, legendary vocal range"},
    {"n":"Aretha Franklin","gn":"Soul","fa":"'Queen of Soul', first woman inducted into the Rock and Roll Hall of Fame"},
    {"n":"Ray Charles","gn":"Soul/Blues","fa":"Pioneer of soul music, blended gospel, blues and jazz"},
    {"n":"Chuck Berry","gn":"Rock and Roll","fa":"Often called 'the father of rock and roll' for his guitar riffs and showmanship",
     "wl":"orange","wi":"Convicted in 1962 under the Mann Act for transporting a minor across state lines"},
    {"n":"Elton John","gn":"Pop/Rock","fa":"Flamboyant piano showman, one of the best-selling music artists in history"},
    {"n":"Stevie Wonder","gn":"Motown/Soul","fa":"Blind musical prodigy who became a Motown legend and multi-instrumentalist"},
    {"n":"Bob Dylan","gn":"Folk/Rock","fa":"Songwriter awarded the Nobel Prize in Literature in 2016"},
    {"n":"Johnny Cash","gn":"Country","fa":"'The Man in Black', known for his deep voice and songs about hardship and redemption"},
    {"n":"Louis Armstrong","gn":"Jazz","fa":"Pioneering jazz trumpeter and singer who helped popularize jazz worldwide"},
    {"n":"Ella Fitzgerald","gn":"Jazz","fa":"'The First Lady of Song', renowned for her vocal range and scat singing"},
    {"n":"Miles Davis","gn":"Jazz","fa":"Influential trumpeter who pushed jazz through multiple stylistic revolutions",
     "wl":"orange","wi":"Publicly admitted to physically abusing several of his partners, including Cicely Tyson and Frances Taylor"},
    {"n":"James Brown","gn":"Funk/Soul","fa":"'The Godfather of Soul', legendary energetic stage performances",
     "wl":"orange","wi":"Convicted multiple times for domestic violence against his wives"},
    {"n":"Tina Turner","gn":"Rock/Soul","fa":"'Queen of Rock 'n' Roll', known for her powerful voice and stage presence"},
    {"n":"ABBA","gn":"Pop","fa":"Swedish pop group, one of the best-selling music acts in history"},
    {"n":"Led Zeppelin","gn":"Rock","fa":"Pioneers of hard rock and heavy metal in the late 1960s and 1970s"},
    {"n":"Pink Floyd","gn":"Progressive Rock","fa":"Known for concept albums like 'The Dark Side of the Moon'"},
    {"n":"The Rolling Stones","gn":"Rock","fa":"One of the longest-running and most successful rock bands in history"},
    {"n":"Nirvana","gn":"Grunge","fa":"Brought grunge and alternative rock into the mainstream with 'Nevermind'"},
    {"n":"AC/DC","gn":"Hard Rock","fa":"Australian band known for high-energy hard rock anthems"},
    {"n":"Fleetwood Mac","gn":"Rock","fa":"Known for the album 'Rumours', one of the best-selling albums ever"},
    {"n":"Marvin Gaye","gn":"Motown/Soul","fa":"Motown star known for 'What's Going On', blending soul with social commentary"},
    {"n":"Diana Ross","gn":"Motown/Pop","fa":"Lead singer of The Supremes, went on to a hugely successful solo career"},
    {"n":"Janis Joplin","gn":"Blues Rock","fa":"Powerful blues-rock voice of the late 1960s counterculture"},
    {"n":"Jim Morrison","gn":"Rock","fa":"Frontman of The Doors, known for poetic and provocative lyrics",
     "wl":"orange","wi":"Arrested and convicted for indecent exposure during a 1969 concert in Miami"},
    {"n":"Bee Gees","gn":"Disco/Pop","fa":"Defined the disco era with the soundtrack to 'Saturday Night Fever'"},
    {"n":"Eric Clapton","gn":"Blues Rock","fa":"Guitar legend, the only three-time inductee into the Rock and Roll Hall of Fame"},
    {"n":"B.B. King","gn":"Blues","fa":"'King of the Blues', famous for his guitar named Lucille"},
    {"n":"Etta James","gn":"Blues/Soul","fa":"Famous for the classic song 'At Last', blended blues, soul and jazz"},
    {"n":"Nina Simone","gn":"Jazz/Soul","fa":"Blended jazz, soul and classical music with powerful civil rights activism"},
    {"n":"Frank Sinatra","gn":"Jazz/Pop","fa":"'Chairman of the Board', one of the most influential vocalists of the 20th century"},
    {"n":"Sam Cooke","gn":"Soul","fa":"Pioneer of soul music, often called 'the King of Soul'"},
    {"n":"Little Richard","gn":"Rock and Roll","fa":"Flamboyant pioneer whose piano playing shaped early rock and roll"},
    {"n":"Bruce Springsteen","gn":"Rock","fa":"'The Boss', known for anthemic songs about American working-class life"},
    {"n":"U2","gn":"Rock","fa":"Irish rock band known for anthemic sound and social activism"},
    {"n":"Amy Winehouse","gn":"Soul/Jazz","fa":"Brought a retro soul sound back into the mainstream with 'Back to Black'"},
    {"n":"Celia Cruz","gn":"Salsa","fa":"'Queen of Salsa', one of the most influential Latin artists of the 20th century"},
    {"n":"Ike Turner","gn":"Rock and Roll","fa":"Co-created 'Rocket 88', often cited as one of the first rock and roll records",
     "wl":"red","wi":"Widely documented for years of severe domestic violence against his then-wife Tina Turner"},
    {"n":"Tupac Shakur","gn":"Hip-Hop","fa":"One of the best-selling hip-hop artists, known for socially conscious and confrontational lyrics",
     "wl":"orange","wi":"Convicted in 1995 of first-degree sexual abuse related to a 1993 incident"},
    {"n":"The Notorious B.I.G.","gn":"Hip-Hop","fa":"Landmark East Coast rapper whose debut album shaped 1990s hip-hop"},
    {"n":"Jay-Z","gn":"Hip-Hop","fa":"One of the best-selling hip-hop artists and a major music industry entrepreneur"},
    {"n":"Eminem","gn":"Hip-Hop","fa":"Best-selling hip-hop artist of all time, known for rapid, technical rap delivery"},
    {"n":"Dr. Dre","gn":"Hip-Hop","fa":"Producer and rapper who popularized G-funk and launched several major careers",
     "wl":"orange","wi":"Publicly apologized decades later for a well-documented 1991 assault on journalist Dee Barnes; also accused of abuse by former partner Michel'le"},
    {"n":"Kanye West","gn":"Hip-Hop","fa":"Influential producer-rapper known for reshaping hip-hop production several times over his career",
     "wl":"orange","wi":"Made widely condemned antisemitic public statements in 2022, resulting in the loss of several major business partnerships"},
    {"n":"Missy Elliott","gn":"Hip-Hop","fa":"Pioneering female rapper-producer known for innovative music videos"},
    {"n":"Queen Latifah","gn":"Hip-Hop","fa":"Pioneering female rapper who later became a successful actress"},
    {"n":"Dolly Parton","gn":"Country","fa":"One of the most successful country artists in history, also a noted philanthropist"},
    {"n":"Willie Nelson","gn":"Country","fa":"Country music icon known for outlaw country and decades-long songwriting career"},
    {"n":"Garth Brooks","gn":"Country","fa":"One of the best-selling solo artists in US history"},
    {"n":"Shania Twain","gn":"Country/Pop","fa":"Best-selling female country artist of all time"},
    {"n":"BTS","gn":"K-Pop","fa":"South Korean group that became one of the best-selling acts in music history"},
    {"n":"Psy","gn":"K-Pop","fa":"His single 'Gangnam Style' was the first YouTube video to reach 1 billion views"},
    {"n":"Carlos Santana","gn":"Latin Rock","fa":"Guitarist who blended rock with Latin American rhythms"},
    {"n":"Gloria Estefan","gn":"Latin Pop","fa":"Helped bring Latin pop and dance music to mainstream US audiences"},
    {"n":"Shakira","gn":"Latin Pop","fa":"One of the best-selling Latin music artists, known for blending pop with Latin rhythms"},
    {"n":"Julio Iglesias","gn":"Latin Pop","fa":"One of the best-selling recording artists in history, especially across Latin America and Europe"},
    {"n":"Daft Punk","gn":"Electronic","fa":"French duo known for pioneering dance-pop production and elaborate robot personas"},
    {"n":"Giorgio Moroder","gn":"Electronic/Disco","fa":"Pioneer of electronic disco production, dubbed 'the father of disco'"},
    {"n":"Fatboy Slim","gn":"Electronic","fa":"Helped popularize big beat electronic music in the 1990s"},
    {"n":"Jimmy Page","gn":"Rock","fa":"Led Zeppelin's guitarist and producer, renowned for his riff-writing",
     "wl":"orange","wi":"Widely reported to have had a relationship with a 14-year-old, Lori Mattix, in the mid-1970s"},
    {"n":"Ozzy Osbourne","gn":"Heavy Metal","fa":"Black Sabbath frontman known as 'the Godfather of Heavy Metal'"},
    {"n":"Metallica","gn":"Heavy Metal","fa":"One of the best-selling heavy metal bands, pioneers of thrash metal"},
    {"n":"Bon Jovi","gn":"Rock","fa":"Known for anthemic rock hits like 'Livin' on a Prayer'"},
    {"n":"Aerosmith","gn":"Rock","fa":"One of the best-selling American rock bands in history",
     "wl":"orange","wi":"Frontman Steven Tyler has written about a relationship with a minor, Julia Holcomb, in the 1970s, for which his family reportedly sought legal guardianship of her"},
    {"n":"George Michael","gn":"Pop","fa":"Wham! and solo star known for his soulful voice and songwriting"},
    {"n":"Cyndi Lauper","gn":"Pop","fa":"1980s pop icon known for 'Girls Just Want to Have Fun'"},
    {"n":"Mariah Carey","gn":"Pop/R&B","fa":"Holds the record for most number-one singles by a solo artist in the US"},
    {"n":"Beyoncé","gn":"Pop/R&B","fa":"One of the most awarded artists in Grammy history"},
    {"n":"Rihanna","gn":"Pop/R&B","fa":"One of the best-selling music artists, also built a major beauty and fashion business"},
    {"n":"Lady Gaga","gn":"Pop","fa":"Known for genre-blending pop music and elaborate theatrical performances"},
    {"n":"Earth, Wind & Fire","gn":"Funk/Soul","fa":"Blended funk, soul, jazz and R&B into a signature horn-driven sound"},
    {"n":"Sly and the Family Stone","gn":"Funk","fa":"Pioneering interracial, mixed-gender funk band of the late 1960s"},
    {"n":"Muddy Waters","gn":"Blues","fa":"Often called 'the father of modern Chicago blues'"},
    {"n":"Robert Johnson","gn":"Blues","fa":"Delta blues guitarist whose legend inspired the 'crossroads' myth about his skill"},
    {"n":"John Lee Hooker","gn":"Blues","fa":"Influential blues guitarist known for his distinctive one-chord boogie style"},
    {"n":"Woody Guthrie","gn":"Folk","fa":"Wrote 'This Land Is Your Land', a major influence on American folk music"},
    {"n":"Joan Baez","gn":"Folk","fa":"Folk singer known for her role in the civil rights and anti-war movements"},
    {"n":"Simon & Garfunkel","gn":"Folk Rock","fa":"Duo known for harmonized folk-rock hits like 'The Sound of Silence'"},
    {"n":"Donna Summer","gn":"Disco","fa":"'Queen of Disco', helped define the sound of the disco era"},
    {"n":"Gloria Gaynor","gn":"Disco","fa":"Known for the disco anthem 'I Will Survive'"},
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
    total = len(legends)
    found = 0
    for i, s in enumerate(legends):
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
    out = Path("assets/music/music_legends.json")
    out.write_text(json.dumps(legends, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    flagged = sum(1 for l in legends if "wl" in l)
    summary = "\nDone: {}/{} images -- {} legends total, {} flagged.\n".format(found, total, total, flagged)
    sys.stdout.buffer.write(summary.encode("utf-8"))

if __name__ == "__main__":
    main()
