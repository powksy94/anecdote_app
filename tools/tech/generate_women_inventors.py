import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=name, inv=invention, cc=ISO2 country code(s) ("/"-joined when several), yr=lifespan (birth-death,
# or "YYYY-" if still living; None if undocumented, the app then shows a localized note),
# ctx=era/social context (None when no reliable documented context exists, the app then hides the
# line), fa=fact, im=imageUrl
#
# Content is written in ENGLISH (source language for the app's translation pipeline, see
# content_loader.dart), with no em/en dash as a separator in the fact text.
# Excluded on purpose: women already in pioneerWoman (Ada Lovelace, Hedy Lamarr, Marie Curie,
# Katherine Johnson...).

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Overrides where the name doesn't map cleanly to its Wikipedia article title.
WIKI_EN = {
    "Mary Anderson": "Mary Anderson (inventor)",
    "Margaret Knight": "Margaret E. Knight",
    "Barbe-Nicole Clicquot": "Madame Clicquot Ponsardin",
    "Elizabeth Magie": "Lizzie Magie",
    "Maria the Jewess": "Mary the Jewess",
    "Mary Phelps Jacob": "Caresse Crosby",
    "Margaret Hamilton": "Margaret Hamilton (software engineer)",
    "Elizabeth Feinler": "Elizabeth J. Feinler",
    "Adele Goldberg": "Adele Goldberg (computer scientist)",
    "Katharine Blodgett": "Katharine Burr Blodgett",
    "Maria Beasley": "Maria E. Beasley",
}

records = [
    {"n": "Mary Anderson", "inv": "Windshield wiper", "cc": "US", "yr": "1866-1953",
     "ctx": "When she patented her wiper in 1903, American women still couldn't vote nationwide: that right only arrived in 1920, the very year her patent expired.",
     "fa": "On a trip to New York, Mary Anderson noticed that a streetcar driver had to keep stopping to clear the sleet from his windshield. She patented a hand-operated wiper in 1903, but a Canadian firm told her it had no commercial value. Her patent expired in 1920, and Cadillac made wipers standard in 1922. She never earned a cent from them."},

    {"n": "Stephanie Kwolek", "inv": "Kevlar", "cc": "US", "yr": "1923-2014",
     "ctx": "Female chemists were rare in the 1940s, and the wartime labor shortage had opened doors for women in research. Even so, DuPont took 15 years to give her a promotion.",
     "fa": "In 1965, DuPont chemist Stephanie Kwolek made a cloudy, runny polymer solution that most colleagues would have thrown away. The technician refused to spin it at first, afraid it would ruin his machine. When she finally persuaded him, the fibers tested far stronger than expected, and Kevlar went on to protect police officers and soldiers."},

    {"n": "Josephine Cochrane", "inv": "Dishwasher", "cc": "US", "yr": "1839-1913",
     "ctx": "In the 19th century, married women often had little control over their own property, which discouraged them from inventing and patenting under their own names.",
     "fa": "According to the popular story, Josephine Cochrane was a wealthy Illinois socialite fed up with servants chipping her fine china after dinner parties. She patented a dishwashing machine in 1886, and what began as a way to protect her plates became her livelihood after she was widowed. Her company later became part of the lineage of KitchenAid."},

    {"n": "Margaret Knight", "inv": "Flat-bottomed paper bag machine", "cc": "US", "yr": "1838-1914",
     "ctx": "Throughout the 19th century, women received less than 1% of all U.S. patents, so a woman claiming authorship of a complex industrial machine faced open disbelief.",
     "fa": "Every paper grocery bag owes its square bottom to Margaret Knight's machine. When a machinist named Charles Annan saw her design and patented it first, she took him to court. His defense was that a woman could never have designed something so complex. Her drawings and diaries proved otherwise, and she received the patent in 1871."},

    {"n": "Bette Nesmith Graham", "inv": "Liquid Paper", "cc": "US", "yr": "1924-1980",
     "ctx": "In the 1950s, IBM's fast new electric typewriters caused more typos, and their carbon ribbons made errors much harder to erase than before.",
     "fa": "A secretary and single mother in Texas, Bette Nesmith Graham started covering her typing errors with white tempera paint in a nail polish bottle. It grew into Liquid Paper, which she sold to Gillette in 1979 for $47.5 million. Her son, Michael Nesmith, had meanwhile found his own fame as a member of the Monkees."},

    {"n": "Melitta Bentz", "inv": "Paper coffee filter", "cc": "DE", "yr": "1873-1950",
     "ctx": "German women only gained the right to vote in 1918, ten years after she registered her filter.",
     "fa": "Tired of bitter coffee full of grounds, the Dresden housewife Melitta Bentz punched holes in a brass pot and lined it with blotting paper from her son's school notebook. She registered the filter in 1908 and started the business in a room of the family apartment. The company still carries her name today."},

    {"n": "Grace Hopper", "inv": "The first compiler", "cc": "US", "yr": "1906-1992",
     "ctx": "Hopper was among the few women with a doctorate when she earned her Yale mathematics PhD in 1934. To join the Navy in 1943, she needed an exemption for being under the minimum weight.",
     "fa": "In 1952, U.S. Navy mathematician Grace Hopper completed A-0, an early compiler that turned instructions into machine code. Colleagues told her that computers couldn't write their own programs, and it took about two years for the idea to be accepted. Her work paved the way for programming languages that read like English."},

    {"n": "Sophie Wilson", "inv": "ARM instruction set", "cc": "GB", "yr": "1957-",
     "ctx": None,
     "fa": "At Acorn Computers, Sophie Wilson designed a processor's instruction set and simulated it in just 808 lines of BBC BASIC. When the first ARM chip arrived in 1985, a faulty board left it with no power connected, and it ran anyway on leakage current. That extreme frugality later made ARM the chip inside mobile phones, a result she herself has called an accident."},

    {"n": "Lynn Conway", "inv": "VLSI chip design methods", "cc": "US", "yr": "1938-2024",
     "ctx": "The U.S. Supreme Court only ruled in 2020 that federal law protects transgender workers from being fired, the same year IBM apologized to her.",
     "fa": "IBM fired Lynn Conway in 1968 after she revealed her plans to transition. She rebuilt her career under a new identity and, at Xerox PARC in the 1970s, developed with Carver Mead the methods that made modern chip design possible. IBM formally apologized to her in 2020, 52 years later."},

    {"n": "Marion Donovan", "inv": "Waterproof diaper cover", "cc": "US", "yr": "1917-1998",
     "ctx": "In the 1940s, babies wore cloth diapers under rubber pants notorious for causing rashes. Donovan later earned a Yale architecture degree in 1958, one of only three women in her class.",
     "fa": "Fed up with soaked bedding, Marion Donovan cut up a shower curtain to make a waterproof diaper cover called the Boater. Manufacturers turned it down, so she made it herself, and it became a hit at Saks Fifth Avenue. She sold the rights in 1951 for $1 million, yet paper companies then dismissed her disposable diaper idea as unnecessary."},

    {"n": 'Maria the Jewess', "inv": 'Bain-marie', "cc": 'EG', "yr": 'c. 1st-3rd century AD',
     "ctx": "Almost everything known about her comes from the later alchemist Zosimos of Panopolis, and even her dates are uncertain.",
     "fa": 'Long before any cookbook, the Alexandrian alchemist Maria the Jewess is credited with a double-walled heating vessel that gave gentle, even heat. French cooks still use her name for it today: the bain-marie, or "Mary\'s bath". She is also linked to the kerotakis, a device for heating substances and collecting their vapors.'},

    {"n": 'Barbe-Nicole Clicquot', "inv": 'Riddling table', "cc": 'FR', "yr": '1777-1866',
     "ctx": None,
     "fa": 'Widowed at 27, Barbe-Nicole Ponsardin persuaded her father-in-law to let her run the family wine business. In 1816, helped by her cellar master, she invented the riddling table, which clears the sediment out of champagne. She had already produced the first known vintage champagne in 1810, and the house still carries her title: Veuve Clicquot, "the widow Clicquot".'},

    {"n": 'Margarete Steiff', "inv": 'Stuffed toy animals', "cc": 'DE', "yr": '1847-1909',
     "ctx": None,
     "fa": 'Polio left Margarete Steiff using a wheelchair for most of her life, yet she became a seamstress and an entrepreneur. Around 1880, she sewed small felt elephants from a magazine pattern meant for pincushions, and children took them as toys. Her company grew from there, and in 1902 her nephew Richard designed its famous jointed plush bear.'},

    {"n": 'Hertha Ayrton', "inv": 'Electric arc lamp improvements', "cc": 'GB', "yr": '1854-1923',
     "ctx": "When she submitted her work on the electric arc, the Royal Society wouldn't let her present it, and a man read her paper in her place.",
     "fa": 'Hertha Ayrton worked out why arc lamps hissed and flickered: oxygen was reaching the carbon rods. She went on to register 26 patents, and during World War I she designed a fan to clear poison gas from the trenches. More than 100,000 were issued to British troops, although their effectiveness in combat is disputed.'},

    {"n": 'Ángela Ruiz Robles', "inv": 'Mechanical encyclopedia', "cc": 'ES', "yr": '1895-1975',
     "ctx": None,
     "fa": 'Spanish teacher Ángela Ruiz Robles wanted to lighten her students\' schoolbags. In 1949, she patented a "mechanical encyclopedia" that displayed learning material at the press of a button, now seen as a forerunner of the e-book. She never found funding to manufacture it, and her prototype sits in a museum in A Coruña.'},

    {"n": 'Mária Telkes', "inv": 'Solar heating and desalination', "cc": 'HU/US', "yr": '1900-1995',
     "ctx": None,
     "fa": 'Nicknamed the "Sun Queen", the Budapest-born scientist developed a solar still during World War II that turned seawater into drinking water for people adrift in lifeboats. In 1948, her heat storage system warmed the Dover Sun House in Massachusetts, a home heated by the sun that was designed and financed by women too.'},

    {"n": 'Elsie MacGill', "inv": 'Maple Leaf Trainer aircraft', "cc": 'CA', "yr": '1905-1980',
     "ctx": "Polio struck her around the time she finished her studies, and she was told she would probably spend her life in a wheelchair.",
     "fa": 'Canadian engineer Elsie MacGill designed the Maple Leaf Trainer II in 1938 and became chief aeronautical engineer at Canadian Car and Foundry, reportedly the first woman in the world to hold such a position. During World War II, she oversaw production of over 1,400 Hawker Hurricane fighters, and a 1942 American comic book nicknamed her the "Queen of the Hurricanes".'},

    {"n": 'Yvonne Brill', "inv": 'Hydrazine resistojet thruster', "cc": 'CA/US', "yr": '1924-2013',
     "ctx": None,
     "fa": 'Canadian-born rocket scientist Yvonne Brill invented a thruster that uses electricity to heat a single propellant, hydrazine, helping keep satellites in their orbits. When she died in 2013, the New York Times obituary opened with her beef stroganoff and her skills as a mother. After a public outcry, it was edited to put her career first.'},

    {"n": 'Karen Spärck Jones', "inv": 'Inverse document frequency', "cc": 'GB', "yr": '1935-2007',
     "ctx": None,
     "fa": 'In 1972, British computer scientist Karen Spärck Jones published a simple idea: the rarer a word is across documents, the more it tells you about the ones containing it. Known as inverse document frequency, it became a pillar of modern search. As she said in 2007, pretty much every web engine uses those principles.'},

    {"n": 'Tu Youyou', "inv": 'Artemisinin extraction', "cc": 'CN', "yr": '1930-',
     "ctx": None,
     "fa": "During a secret Chinese military project, Tu Youyou's team screened hundreds of herbal remedies in search of a malaria treatment. A text from around 340 AD advised soaking sweet wormwood in cold water, and that hint led her to a gentler extraction method. She shared the 2015 Nobel Prize in Medicine despite having no doctorate or medical degree."},

    {"n": 'Sumita Mitra', "inv": 'Nanocomposite dental filling', "cc": 'IN/US', "yr": '1949-',
     "ctx": None,
     "fa": 'Kolkata-educated chemist Sumita Mitra joined 3M in 1978 and created the first dental filling material to include nanoparticles, later sold as Filtek. Hundreds of millions of tooth restorations have been made with these products. She joined the National Inventors Hall of Fame in 2018.'},

    {"n": 'Beatrice Shilling', "inv": 'RAE restrictor', "cc": 'GB', "yr": '1909-1990',
     "ctx": None,
     "fa": 'Spitfire engines could cut out when pilots pushed into a dive. Engineer Beatrice "Tilly" Shilling, who also raced motorcycles at Brooklands at over 100 mph, fixed it with a small brass restrictor, a simple stopgap in the fuel system. Pilots gratefully nicknamed it "Miss Shilling\'s orifice".'},

    {"n": 'Joan Curran', "inv": 'Window radar countermeasure', "cc": 'GB', "yr": '1916-1999',
     "ctx": None,
     "fa": 'Welsh physicist Joan Curran developed Window, a technique of dropping strips that swamp enemy radar, known today as chaff. Before D-Day, bombers dropped it over the Straits of Dover to create the false image of an invasion fleet on German screens. Air forces around the world still use the same principle.'},

    {"n": 'Henrietta Vansittart', "inv": 'Lowe-Vansittart propeller', "cc": 'GB', "yr": '1833-1883',
     "ctx": "Her 1868 British patent was among the first granted to a woman in her own name.",
     "fa": 'Henrietta Vansittart assisted her father, screw propeller inventor James Lowe, and carried on his work after he died. Her Lowe-Vansittart propeller was trialled by the Admiralty on HMS Druid in 1869 and won a first-class diploma in 1871. She also became one of the first women to present an engineering paper in Britain.'},

    {"n": 'Sarah Guppy', "inv": 'Bridge construction patent', "cc": 'GB', "yr": '1770-1852',
     "ctx": None,
     "fa": 'In 1811, Sarah Guppy of Bristol patented a method for building bridges and railroads without arches, the first of her inventions. She is often wrongly credited with designing the Clifton Suspension Bridge, but its trust and engineers have shown that her patent had no influence on it.'},

    {"n": 'Elizabeth Magie', "inv": "The Landlord's Game", "cc": 'US', "yr": '1866-1948',
     "ctx": None,
     "fa": 'In 1904, Elizabeth Magie patented a board game designed to show the dangers of monopolies. Thirty years later, Charles Darrow sold a version as his own invention, called Monopoly. Parker Brothers bought her patent for just $500 with no royalties, and her role was only rediscovered decades later, during a lawsuit in the 1970s.'},

    {"n": 'Alice Ball', "inv": 'Injectable leprosy treatment', "cc": 'US', "yr": '1892-1916',
     "ctx": None,
     "fa": 'As a young chemist in Hawaii, Alice Ball found a way to make chaulmoogra oil usable for treating leprosy. She died in 1916 before publishing her findings, and Arthur Dean, the chemistry head at her college, published the method as the "Dean Method". A colleague restored her credit in 1922 by calling it the "Ball Method".'},

    {"n": 'Patricia Bath', "inv": 'Laserphaco probe', "cc": 'US', "yr": '1942-2019',
     "ctx": None,
     "fa": 'Ophthalmologist Patricia Bath designed a device that uses a laser to break apart cataracts through a tiny incision. She filed the patent in 1986, and when it was issued in 1988, she became the first Black woman physician to receive a U.S. medical patent.'},

    {"n": 'Marie Van Brittan Brown', "inv": 'Home security system', "cc": 'US', "yr": '1922-1999',
     "ctx": None,
     "fa": 'A nurse in Queens, New York, Marie Van Brittan Brown developed a home security system with her husband Albert: peepholes, a sliding camera, a television monitor, two-way microphones and an emergency button. Patented in 1969, it never reached the market, but dozens of later patents have cited it.'},

    {"n": 'Ruth Handler', "inv": 'Barbie doll', "cc": 'US', "yr": '1916-2002',
     "ctx": None,
     "fa": 'On a trip to Europe, Ruth Handler bought a German doll named Lilli for her daughter Barbara. By her own account, colleagues at Mattel told her a doll with breasts could never be made, but she persisted, and Barbie launched in 1959. After her own breast cancer, she went on to create Nearly Me, a more realistic breast prosthesis.'},

    {"n": 'Mary Phelps Jacob', "inv": 'Backless brassiere', "cc": 'US', "yr": '1892-1970',
     "ctx": None,
     "fa": 'By her own account, Mary Phelps Jacob improvised a bra from two handkerchiefs and some ribbon before a party. She patented it in 1914, then sold the patent to the Warner Brothers Corset Company for $1,500. It later made Warner far more than that.'},

    {"n": 'Margaret Hamilton', "inv": 'Apollo flight software', "cc": 'US', "yr": '1936-2026',
     "ctx": None,
     "fa": "Margaret Hamilton led the team writing the onboard flight software for NASA's moon missions. During the Apollo 11 landing, alarms flashed because the computer was overloaded, but its priority system dropped lesser tasks and kept the essential ones running. She received the Presidential Medal of Freedom in 2016."},

    {"n": 'Radia Perlman', "inv": 'Spanning Tree Protocol', "cc": 'US', "yr": '1951-',
     "ctx": None,
     "fa": 'Network engineer Radia Perlman invented the Spanning Tree Protocol, which stops data from looping endlessly around a network. She even summed it up in a poem, "Algorhyme", adapted from Joyce Kilmer\'s "Trees". Journalists call her the "Mother of the Internet", a title she dislikes, insisting that many people built it.'},

    {"n": 'Katharine Blodgett', "inv": 'Non-reflective glass', "cc": 'US', "yr": '1898-1979',
     "ctx": "In 1918, she became the first woman scientist at General Electric's research laboratory.",
     "fa": 'In the late 1930s, Katharine Blodgett developed a coating that made glass virtually invisible by cancelling reflections. GE never commercialized it because it wiped off too easily, but her work led to nonreflective glass for submarine periscopes, spy cameras and film lenses during World War II.'},

    {"n": 'Virginia Apgar', "inv": 'Apgar score', "cc": 'US', "yr": '1909-1974',
     "ctx": None,
     "fa": "In 1952, Columbia anesthesiologist Virginia Apgar presented a simple way to assess a newborn: heart rate, breathing, muscle tone, reflexes and color, each scored one and five minutes after birth. It's still used in delivery rooms, so almost everyone reading this has an Apgar score, whether they know it or not."},

    {"n": 'Lillian Gilbreth', "inv": 'Kitchen design', "cc": 'US', "yr": '1878-1972',
     "ctx": None,
     "fa": 'Engineer and psychologist Lillian Gilbreth applied efficiency studies to the home, and is credited with the foot-pedal trash can and the shelves inside refrigerator doors. She managed this as a mother of 12: when her husband died in 1924, she carried on their work alone while raising 11 children under 19.'},

    {"n": 'Beulah Louise Henry', "inv": 'Bobbinless sewing machine', "cc": 'US', "yr": '1887-1973',
     "ctx": None,
     "fa": 'Nicknamed "Lady Edison", Beulah Henry held about 49 patents and is credited with as many as 110 inventions, despite having no training in mechanics or engineering. Her first patent, in 1912, covered a vacuum ice cream freezer. She later created a bobbinless sewing machine.'},

    {"n": 'Maria Beasley', "inv": 'Barrel-hooping machine', "cc": 'US', "yr": 'c. 1836-1913',
     "ctx": None,
     "fa": 'Maria Beasley held about fifteen U.S. patents. Her most lucrative was a machine that hooped barrels by the thousand each day, reportedly bringing in $20,000 a year in royalties. In 1880, she also patented an improved life raft with guard rails, a clear step up from the flat rafts of the previous decade.'},

    {"n": 'Elizabeth Feinler', "inv": 'ARPANET directory and WHOIS', "cc": 'US', "yr": '1931-',
     "ctx": None,
     "fa": "Before web browsers, finding anything on the early Internet went through Jake Feinler's team at the Network Information Center. Her group built the first WHOIS name server and suggested the top-level domains we still use, such as .com, .org and .gov, which the developer community then approved."},

    {"n": 'Adele Goldberg', "inv": 'Smalltalk', "cc": 'US', "yr": '1945-',
     "ctx": None,
     "fa": 'At Xerox PARC, computer scientist Adele Goldberg helped develop Smalltalk. By her own account, when Steve Jobs asked to see it in 1979, she refused, suspecting Apple would take the technology. Xerox management overruled her, and accounts of that famous visit still contradict one another.'},

    {"n": "Veronica Bekoe", "inv": "Veronica Bucket", "cc": "GH", "yr": None,
     "ctx": None,
     "fa": "Working in a public health laboratory in Ghana, biologist Veronica Bekoe devised a simple bucket with a tap for handwashing with running water, used mainly in schools and hospitals. During COVID-19, demand shot up in homes, workplaces, churches and mosques. She had given up on patenting it, finding the process too bureaucratic."},

    {"n": "Nzambi Matee", "inv": "Recycled plastic bricks", "cc": "KE", "yr": "1992-",
     "ctx": None,
     "fa": "In Nairobi, Nzambi Matee founded Gjenge Makers, which mixes sand with plastic waste that recyclers can't process to make paving bricks. Her company says they are five to seven times stronger than concrete, and the United Nations Environment Programme named her a Young Champion of the Earth in 2020."},

    {"n": "Johanna Döbereiner", "inv": "Bacterial nitrogen fixation for soybeans", "cc": "BR", "yr": "1924-2000",
     "ctx": None,
     "fa": "While most soybean farming relied on heavy nitrogen fertilizer, Brazilian agronomist Johanna Döbereiner showed that certain bacteria could do the job instead. Her ideas were resisted at first, but they became the basis of Brazil's soybean farming, saving the country an estimated billion dollars a year in fertilizer."},
]


def wiki_img(title: str) -> str | None:
    for attempt in range(2):
        try:
            if attempt == 0:
                url = (f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages"
                       f"&format=json&titles={quote(title)}&pithumbsize=500")
                r = requests.get(url, headers=HEADERS, timeout=10)
                pages = r.json().get("query", {}).get("pages", {})
                for page in pages.values():
                    src = page.get("thumbnail", {}).get("source")
                    if src:
                        return src
            else:
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title)}"
                r = requests.get(url, headers=HEADERS, timeout=10)
                if r.status_code == 200:
                    src = r.json().get("thumbnail", {}).get("source")
                    if src:
                        return src
        except Exception:
            pass
    return None


def main():
    total = len(records)
    found = 0
    for i, s in enumerate(records):
        title = WIKI_EN.get(s["n"], s["n"])
        img = wiki_img(title)
        s["im"] = img
        if img:
            found += 1
        status = "ok" if img else "xx"
        sys.stdout.buffer.write((f"  [{i+1:2}/{total}] {status} {s['n']}" + chr(10)).encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)

    out = Path("assets/tech/women_inventors.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(records, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    sys.stdout.buffer.write((chr(10) + f"Done: {found}/{total} images found." + chr(10)).encode("utf-8"))


if __name__ == "__main__":
    main()
