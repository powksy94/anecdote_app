import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=invention name, inv=inventor(s) credited (None if anonymous), cc=ISO2 country code(s) of the
# inventor(s) ("/"-joined when several), yr=year, fa=fact,
# wk=Wikipedia article title of the INVENTION (image source, not the inventor's portrait)
#
# Content in ENGLISH, no em/en dash as a separator in the fact text.
# Scope: only inventions and discoveries born from an accident or a mistake (sorting rule decided
# on 2026-10-29). Everyday objects designed on purpose go to "Everyday objects".
# Excluded on purpose: penicillin and X-rays (same discovery story already told in Medical
# anecdotes), and well-known legends that sources don't support (potato chips, chocolate chip
# cookie, Dom Perignon, stainless steel scrap heap, Bari and chemotherapy, Goodyear's stove...).


HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

records = [
    {"n": "Viagra", "inv": "Pfizer researchers", "cc": "GB", "yr": "1998",
     "wk": "Sildenafil",
     "fa": "At Pfizer's research site in Sandwich, England, sildenafil was being tested as a treatment for angina, a heart condition, and the results were disappointing. But volunteers noticed an unexpected side effect, and some reportedly refused to hand back their leftover pills. In 1998, it was approved as Viagra, the first oral treatment for erectile dysfunction."},

    {"n": "The microwave oven", "inv": "Percy Spencer", "cc": "US", "yr": "1945",
     "wk": "Microwave oven",
     "fa": "Engineer Percy Spencer was working near a magnetron, a radar component, when he noticed that a candy bar in his pocket had melted. He was not the first to notice the effect, but he was the first to investigate it: he held popcorn kernels near the device and watched them pop. The first commercial microwave oven stood almost 1.8 meters tall and weighed about 340 kg."},

    {"n": "Post-it notes", "inv": "Spencer Silver & Art Fry", "cc": "US", "yr": "1968",
     "wk": 'Arthur Fry',
     "fa": "In 1968, 3M chemist Spencer Silver was trying to make a super-strong glue and produced a weak one instead, which the company saw as useless. Years later, his colleague Art Fry was fed up with bookmarks slipping out of his hymnal at choir practice, and he realized Silver's glue was perfect for them. Post-it notes launched nationwide in 1980."},

    {"n": "Velcro", "inv": "George de Mestral", "cc": "CH", "yr": "1941",
     "wk": "Hook-and-loop fastener",
     "fa": "After a hunting trip in 1941, Swiss engineer George de Mestral found burdock burrs stuck to his clothes and his dog's fur. Under a microscope, he saw tiny hooks catching on loops. It took him years to reproduce the idea, since cotton wore out too quickly and he had to switch to nylon. The name comes from the French \"velours\" and \"crochet\", velvet and hook."},

    {"n": "Saccharin", "inv": "Constantin Fahlberg", "cc": "DE", "yr": "1879",
     "wk": "Saccharin",
     "fa": "Chemist Constantin Fahlberg spilled an experimental compound on his hands in a lab at Johns Hopkins, then forgot about it. At dinner, he bit into a roll and found it remarkably sweet. He co-published the discovery with his lab head, Ira Remsen, but later patented it alone as \"Fahlberg's saccharin\", which left Remsen furious."},

    {"n": "Teflon", "inv": "Roy Plunkett", "cc": "US", "yr": "1938",
     "wk": "Polytetrafluoroethylene",
     "fa": "On April 6, 1938, DuPont chemist Roy Plunkett opened a cylinder of gas that seemed empty, yet it still weighed too much. Inside, the gas had turned into a slippery white powder. Its first major use was secret: during World War II, it coated valves and seals at the Manhattan Project's uranium plant, under a code name."},

    {"n": "Laminated safety glass", "inv": "Édouard Bénédictus", "cc": "FR", "yr": "1903",
     "wk": "Laminated glass",
     "fa": "In 1903, French chemist Édouard Bénédictus dropped a glass flask that had once held cellulose nitrate. It cracked but kept its shape, held together by a thin film the dried liquid had left inside. He went on to sandwich that material between two sheets of glass, and patented the result in 1909 under the name Triplex."},

    {"n": "The inkjet printer", "inv": "Ichiro Endo", "cc": "JP", "yr": "1977",
     "wk": "Inkjet printing",
     "fa": "At Canon, a hot soldering iron accidentally touched the needle of a syringe filled with ink, and droplets spurted from the tip. Engineer Ichiro Endo realized that heating ink to form a tiny bubble could place a dot on paper. Canon filed its patent in 1977, while John Vaught at HP was inventing the same process at about the same time."},

    {"n": 'Mauve, the first synthetic dye', "inv": 'William Perkin', "cc": 'GB', "yr": '1856',
     "wk": 'Mauveine',
     "fa": 'During the 1856 Easter holiday, 18-year-old William Perkin tried to make quinine, the malaria drug, in a makeshift lab at home in London. Instead he got a dark sludge, and while cleaning it up, he noticed a striking purple color. He patented it that same year: mauve, one of the first synthetic dyes, which made him rich.'},

    {"n": 'Super Glue', "inv": 'Harry Coover', "cc": 'US', "yr": '1942',
     "wk": 'Cyanoacrylate',
     "fa": 'In 1942, Harry Coover was looking for a clear plastic for gun sights and dismissed cyanoacrylate because it stuck to everything. Around 1951, at Eastman Kodak, his team stumbled on it again while working on heat-resistant materials for jet canopies. This time he saw the point, and it went on sale in 1958.'},

    {"n": 'Polyethylene', "inv": 'Eric Fawcett & Reginald Gibson', "cc": 'GB', "yr": '1933',
     "wk": 'Polyethylene',
     "fa": "In 1933, chemists Eric Fawcett and Reginald Gibson at ICI in England found a mysterious waxy solid inside their high-pressure vessel. A tiny leak had let oxygen in, which triggered the reaction. That accident gave birth to the world's most common plastic, used today in everything from bags to bottles."},

    {"n": 'Gore-Tex', "inv": 'Bob Gore', "cc": 'US', "yr": '1969',
     "wk": 'Waterproof fabric',
     "fa": 'In 1969, Bob Gore was slowly stretching heated rods of PTFE, the material of Teflon, and every one of them snapped. Out of frustration, he gave one a sudden, hard yank, and it stretched to many times its length without breaking. The new airy material, waterproof yet breathable, became Gore-Tex.'},

    {"n": 'Scotchgard', "inv": 'Patsy Sherman & Samuel Smith', "cc": 'US', "yr": '1953',
     "wk": "Patsy O'Connell Sherman",
     "fa": "In 1953, at 3M, a few drops of an experimental chemical splashed onto an assistant's canvas shoe. Chemist Patsy Sherman and her team noticed that, try as they might, they couldn't wash it off, and the spot stayed clean. Sherman and her colleague Samuel Smith turned it into Scotchgard, the stain-repellent fabric protector."},

    {"n": 'Silly Putty', "inv": 'James Wright', "cc": 'US', "yr": '1943',
     "wk": 'Silly Putty',
     "fa": 'During World War II, General Electric engineer James Wright was looking for a cheap synthetic rubber and mixed boric acid with silicone oil. The result bounced and stretched but was useless as rubber. A few years later, a marketing consultant named Peter Hodgson packed it into plastic eggs and sold it as a toy for Easter 1950.'},

    {"n": 'Aspartame', "inv": 'James Schlatter', "cc": 'US', "yr": '1965',
     "wk": 'Aspartame',
     "fa": 'In December 1965, chemist James Schlatter was working on a treatment for stomach ulcers at G.D. Searle when he got a small amount of a compound on his hand without noticing. According to popular accounts, he then licked his finger to pick up a sheet of paper and found it remarkably sweet. It became aspartame.'},

    {"n": 'Sucralose', "inv": 'Leslie Hough & Shashikant Phadnis', "cc": 'GB/IN', "yr": '1976',
     "wk": 'Sucralose',
     "fa": 'In London, researcher Shashikant Phadnis was working with Professor Leslie Hough on chlorinated sugars. The popular story says he misheard a request to "test" a compound as "taste" it. Whatever the reason, his own recollection is that he tasted the compounds, and many were sweet. The pair published the sweetener in Nature in 1976.'},

    {"n": 'Cyclamate', "inv": 'Michael Sveda', "cc": 'US', "yr": '1937',
     "wk": 'Cyclamate',
     "fa": 'In 1937, graduate student Michael Sveda was working on fever-reducing compounds at the University of Illinois. While smoking, he noticed that his cigarette, or his fingers, tasted sweet, depending on the account. The compound became the sweetener cyclamate, widely used in diet sodas until the U.S. banned it in 1970.'},

    {"n": 'Artificial silk', "inv": 'Hilaire de Chardonnet', "cc": 'FR', "yr": '1884',
     "wk": 'Artificial silk',
     "fa": 'Working in his darkroom, French count Hilaire de Chardonnet knocked over a bottle of nitrocellulose. Cleaning it up, he noticed the thickened liquid formed long, thin strands that looked like silk. His "Chardonnet silk" was a hit at the 1889 Paris Exposition, but it was so flammable that some garments reportedly caught fire near a lit cigarette.'},

    {"n": 'Hair regrowth with minoxidil', "inv": 'Upjohn researchers', "cc": 'US', "yr": '1988',
     "wk": 'Minoxidil',
     "fa": 'Minoxidil was first developed as a blood pressure drug. In clinical trials, patients started growing hair in unexpected places, and Upjohn dismissed it at first as a harmless side effect. Once word got out, volunteers flooded the company asking to join hair loss trials, and the drug was approved against baldness in 1988 as Rogaine.'},

    {"n": 'Cisplatin', "inv": 'Barnett Rosenberg', "cc": 'US', "yr": '1965',
     "wk": 'Cisplatin',
     "fa": "In 1965, biophysicist Barnett Rosenberg was studying whether an electric field affects bacteria, using platinum electrodes. The bacteria stopped dividing and grew into long filaments, but the field wasn't the cause: the supposedly inert platinum had reacted with the solution. The compound responsible, cisplatin, became a major cancer drug."},

    {"n": 'LSD', "inv": 'Albert Hofmann', "cc": 'CH', "yr": '1943',
     "wk": 'Lysergic acid diethylamide',
     "fa": 'Albert Hofmann first made LSD at Sandoz in Basel in 1938, then set it aside. On April 16, 1943, he accidentally absorbed a tiny amount and felt strange effects. Three days later, he deliberately took a dose about twelve times what is now known to be active, and rode home by bicycle, since wartime restrictions kept cars off the streets.'},

    {"n": 'The implantable pacemaker', "inv": 'Wilson Greatbatch', "cc": 'US', "yr": '1956',
     "wk": 'Artificial cardiac pacemaker',
     "fa": 'In 1956, engineer Wilson Greatbatch was building a device to record heart sounds when he installed a resistor of the wrong value. The circuit began pulsing at a steady, heartbeat-like rhythm. He realized it could keep a failing heart in time, and the first implantable pacemaker based on his design followed a few years later.'},

    {"n": 'The Slinky', "inv": 'Richard James', "cc": 'US', "yr": '1943',
     "wk": 'Slinky',
     "fa": 'In 1943, naval engineer Richard James was working on springs to steady ship instruments when one fell off his desk and kept tumbling across the floor. He turned it into a toy. At its first demonstration in a Philadelphia department store in 1945, all 400 units sold out in 90 minutes, at a dollar each.'},

    {"n": 'Play-Doh', "inv": 'Noah & Joe McVicker', "cc": 'US', "yr": '1956',
     "wk": 'Plasticine',
     "fa": 'Play-Doh started out as a putty for cleaning soot off wallpaper, a product that was dying as homes switched away from coal heating. Nursery school teacher Kay Zufall found her pupils loved modeling with it, and suggested selling it as a toy and calling it Play-Doh. The McVickers relaunched it in 1956.'},

    {"n": 'The friction match', "inv": 'John Walker', "cc": 'GB', "yr": '1826',
     "wk": 'Match',
     "fa": 'In 1826, English chemist John Walker of Stockton-on-Tees was preparing a mixture when a stick dipped in it caught fire as it scraped on his hearth. He began selling the first friction matches the following year. Friends urged him to patent the idea, but he refused, and other producers soon copied it.'},

    {"n": 'The Super Soaker', "inv": 'Lonnie Johnson', "cc": 'US', "yr": '1982',
     "wk": 'Super Soaker',
     "fa": "In 1982, engineer Lonnie Johnson, who worked on NASA's Galileo mission to Jupiter, was building a heat pump that used water instead of Freon. A test sent a powerful stream of water across the room, and he saw a toy in it. It reached stores in 1990 as the Power Drencher, was renamed Super Soaker a year later, and became one of the best-selling toys ever."},

    {"n": 'Bubble Wrap', "inv": 'Alfred Fielding & Marc Chavannes', "cc": 'US/CH', "yr": '1957',
     "wk": 'Bubble Wrap (brand)',
     "fa": 'In 1957, engineers Alfred Fielding and Marc Chavannes sealed two plastic shower curtains together to create a trendy textured wallpaper. Nobody wanted it, and greenhouse insulation flopped too. Success only came when IBM used it to protect its new 1401 computer during shipping, and Bubble Wrap found its true calling.'},

    {"n": 'The smoke detector', "inv": 'Walter Jaeger', "cc": 'CH', "yr": '1930s',
     "wk": 'Smoke detector',
     "fa": "In the late 1930s, Swiss physicist Walter Jaeger was trying to build a sensor for poison gas, and it wasn't sensitive enough. Frustrated, he lit a cigarette, and the meter on his device suddenly registered a drop in current: it was detecting smoke. His accident was one of the steps toward the modern smoke detector."},

    {"n": 'Radioactivity', "inv": 'Henri Becquerel', "cc": 'FR', "yr": '1896',
     "wk": 'Radioactive decay',
     "fa": 'Henri Becquerel thought uranium salts needed sunlight to give off rays. In March 1896, cloudy weather stopped his experiment, so he put the salts and a wrapped photographic plate in a drawer. When he developed the plate anyway, it showed sharp, dark silhouettes: the uranium was emitting radiation all by itself.'},

    {"n": 'Cosmic microwave background', "inv": 'Arno Penzias & Robert Wilson', "cc": 'US', "yr": '1964',
     "wk": 'Cosmic microwave background',
     "fa": 'At Bell Labs, Arno Penzias and Robert Wilson kept picking up a faint hiss in their giant horn antenna, coming from every direction. They even evicted pigeons and cleaned out their droppings, but the noise remained. It turned out to be the afterglow of the Big Bang, and it won them the 1978 Nobel Prize in Physics.'},

    {"n": 'Pulsars', "inv": 'Jocelyn Bell Burnell', "cc": 'GB', "yr": '1967',
     "wk": 'Pulsar',
     "fa": 'In 1967, PhD student Jocelyn Bell noticed a strange bit of "scruff" on her radio telescope\'s chart paper: a pulse repeating about every 1.3 seconds. The team half-jokingly labeled it LGM-1, for "Little Green Men". It was the first pulsar, a spinning dead star. The 1974 Nobel Prize went to her supervisor, not to her.'},

    {"n": 'Corn flakes', "inv": 'John Harvey & Will Keith Kellogg', "cc": 'US', "yr": '1894',
     "wk": 'Corn flakes',
     "fa": 'At their health sanitarium in Battle Creek, Michigan, the Kellogg brothers left a batch of boiled wheat standing too long. When they rolled it anyway, it came out as flakes instead of a sheet of dough, and patients liked them once baked. Will Keith Kellogg later applied the idea to corn, giving the world corn flakes.'},

    {"n": 'Wheaties', "inv": 'Washburn Crosby Company', "cc": 'US', "yr": '1921',
     "wk": 'Wheaties',
     "fa": 'According to its maker, Wheaties began in 1921 when a Minneapolis health clinician spilled bran gruel on a hot stove, and it crisped into flakes. It took more than 36 attempts to make the flakes sturdy enough for a box. A company-wide contest named the cereal, and its radio jingle was among the first ever broadcast.'},

    {"n": 'The Popsicle', "inv": 'Frank Epperson', "cc": 'US', "yr": '1905',
     "wk": 'Ice pop',
     "fa": "As the story goes, in 1905, 11-year-old Frank Epperson left a cup of fruit soda with a stirring stick on his porch overnight, and it froze solid. Years later he sold his frozen pops at an amusement park, and patented them in 1924. He first called them Epsicles, but his children's name won: Pop's 'sicles, or Popsicles."},

    {"n": 'Glass-ceramic', "inv": 'Donald Stookey', "cc": 'US', "yr": '1953',
     "wk": 'CorningWare',
     "fa": 'In 1953, Corning chemist Donald Stookey put a piece of glass in a furnace that malfunctioned and overheated it to about 900 °C. Expecting a ruined sample, he reached for it with tongs and dropped it, and it bounced instead of shattering. He had created the first glass-ceramic, later used to make CorningWare cookware.'},

    {"n": 'Electromagnetism', "inv": 'Hans Christian Ørsted', "cc": 'DK', "yr": '1820',
     "wk": 'Electromagnetism',
     "fa": "In 1820, during a lecture in Copenhagen, physicist Hans Christian Ørsted noticed that a compass needle twitched when he switched on an electric current nearby. The movement was so slight his audience reportedly didn't notice. It was the first evidence that electricity and magnetism are linked, the basis of every electric motor."},

    {"n": 'Modern chewing gum', "inv": 'Thomas Adams', "cc": 'US', "yr": '1870s',
     "wk": 'Chewing gum',
     "fa": "In the 1870s, inventor Thomas Adams tried for more than a year to turn chicle, a tree sap brought by exiled Mexican leader Santa Anna, into a cheap substitute for rubber. It wouldn't harden properly. Adams then remembered that people liked chewing it, and launched Adams New York Gum instead."},

    {"n": 'Saran wrap', "inv": 'Ralph Wiley', "cc": 'US', "yr": '1933',
     "wk": 'Plastic wrap',
     "fa": "In 1933, Ralph Wiley, a college student washing glassware part-time in a Dow Chemical lab, found a vial coated in residue he simply couldn't scrub off. The stubborn film became Saran, first sprayed on fighter planes to protect them from salty sea spray, then sold as a kitchen food wrap from 1949."},

    {"n": 'Cat litter', "inv": 'Edward Lowe', "cc": 'US', "yr": '1947',
     "wk": 'Cat litter',
     "fa": "In January 1947, in Michigan, Edward Lowe's neighbor asked him for sand for her cat's box, because her sand pile had frozen. He suggested an absorbent clay instead, one he had been unsuccessfully trying to sell as chicken nesting litter. It worked so well that he bagged it, named it Kitty Litter, and gave it away until people would pay."},
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
        title = s.pop("wk")
        img = wiki_img(title)
        s["im"] = img
        if img:
            found += 1
        status = "ok" if img else "xx"
        sys.stdout.buffer.write((f"  [{i+1:2}/{total}] {status} {title}" + chr(10)).encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)

    out = Path("assets/tech/accidental_inventions.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(records, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    sys.stdout.buffer.write((chr(10) + f"Done: {found}/{total} images found." + chr(10)).encode("utf-8"))


if __name__ == "__main__":
    main()
