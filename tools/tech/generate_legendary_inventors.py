import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=name, inv=best-known invention(s), cc=ISO2 country code(s) ("/"-joined when several),
# yr=lifespan (birth-death, or "YYYY-" if still living; None if undocumented, the app then shows a
# localized note), fa=fact, im=imageUrl (portrait fetched from Wikipedia)
#
# Content is written in ENGLISH (source language for the app's translation pipeline, see
# content_loader.dart), with no em/en dash as a separator in the fact text.
# Angle: the person's life, not the invention itself. Facts already told in Great inventions
# (Edison vs Swan, Bell vs Gray and Meucci, Gutenberg and Fust, Tesla's war of the currents...)
# must not be repeated here.
# Excluded on purpose: Leonardo da Vinci (Famous artists), Marconi (Nobel prize), Babbage (Great
# inventions and Pioneer women).

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (https://powksy.com/daily-facts)"}

# Overrides where the name doesn't map cleanly to its Wikipedia article title.
WIKI_EN = {
    "Kōkichi Mikimoto": "Kokichi Mikimoto",
    "Alexander Popov": "Alexander Stepanovich Popov",
    "Lewis Latimer": "Lewis Howard Latimer",
}

records = [
    {"n": "Thomas Edison", "inv": "Phonograph, light bulb, motion picture camera", "cc": "US", "yr": "1847-1931",
     "fa": "Thomas Edison held a record 1,093 U.S. patents, many of them from his lab in Menlo Park, New Jersey, which he ran as an \"invention factory\". He did it while mostly deaf. Decades later, Henry Ford had the Menlo Park lab rebuilt from photographs and surviving materials in his museum in Michigan."},

    {"n": "Nikola Tesla", "inv": "Alternating current motor", "cc": "RS/US", "yr": "1856-1943",
     "fa": "Nikola Tesla spent his last ten years living in rooms 3327 and 3328 of the New Yorker Hotel, broke and feeding pigeons from his window. He wrote of loving one white pigeon in particular. Two days after he died there in January 1943, the U.S. Office of Alien Property seized all his belongings, even though he was an American citizen."},

    {"n": "Zhang Heng", "inv": "Seismoscope", "cc": "CN", "yr": "78-139",
     "fa": "In 132 AD, the Chinese astronomer Zhang Heng presented the Han court with a bronze vessel ringed by eight dragons, each holding a ball above an open-mouthed toad. When the ground shook, a ball dropped. According to the historical record, it once signaled an earthquake nobody in the capital had felt, and a messenger later confirmed a quake far to the west."},

    {"n": "Benjamin Franklin", "inv": "Lightning rod, Franklin stove, bifocals", "cc": "US", "yr": "1706-1790",
     "fa": "Benjamin Franklin never patented his inventions. When the governor of Pennsylvania offered him a lucrative patent on his stove, he declined, writing in his autobiography that since we enjoy great advantages from the inventions of others, we should be glad of an opportunity to serve others by any invention of ours."},

    {"n": "Louis Braille", "inv": "Braille", "cc": "FR", "yr": "1809-1852",
     "fa": "At three, Louis Braille hurt his eye with an awl while playing in his father's leather workshop, and he was blind in both eyes by five. At a school for the blind in Paris, he discovered \"night writing\", a raised-dot code designed by an army officer, and improved it. By 15, he had created the system that bears his name."},

    {"n": "Garrett Morgan", "inv": "Safety hood, three-position traffic signal", "cc": "US", "yr": "1877-1963",
     "fa": "In 1916, an explosion trapped workers in a tunnel being dug under Lake Erie for Cleveland's water supply. Garrett Morgan and his brother went in wearing the safety hood he had patented, and helped bring men out. In 1923, he patented a traffic signal and later sold the rights to General Electric for $40,000."},

    {"n": "Tanaka Hisashige", "inv": "Myriad year clock", "cc": "JP", "yr": "1799-1881",
     "fa": "Nicknamed \"the Thomas Edison of Japan\", Tanaka Hisashige designed in 1851 a clock that took him more than three years to assemble, ran for a whole year on one winding, and kept both Western and traditional Japanese time. In his seventies, he founded an engineering works that later became part of Toshiba, which still owns the clock."},

    {"n": "Hero of Alexandria", "inv": "Aeolipile, coin-operated dispenser", "cc": "EG", "yr": "c. 10-70 AD",
     "fa": "In the first century AD, the engineer Hero of Alexandria described a machine that dispensed a fixed amount of water when a coin was dropped in a slot: the coin tipped a lever that opened a valve, then slid off and let it close. He also designed temple doors that opened by themselves when a fire was lit on the altar."},

    {"n": "Ole Kirk Christiansen", "inv": "LEGO", "cc": "DK", "yr": "1891-1958",
     "fa": "Ole Kirk Christiansen was a carpenter in the Danish village of Billund. In 1924, two of his sons, playing with matches, burned down the family home and workshop. During the Depression, he turned to making wooden toys, and in 1949 his company launched its first plastic interlocking bricks, the start of LEGO."},

    {"n": "Alexander Graham Bell", "inv": "Telephone, photophone", "cc": "GB/US", "yr": "1847-1922",
     "fa": "Alexander Graham Bell didn't consider the telephone his greatest invention. Shortly before his death, he said that honor went to the photophone, a device he demonstrated in 1880 that sent speech on a beam of light. He was so excited about it that he reportedly wanted to name his second daughter Photophone."},

    {"n": "Ibn al-Haytham", "inv": "Camera obscura studies, Book of Optics", "cc": "IQ", "yr": "c. 965-c. 1040",
     "fa": "Ibn al-Haytham told the Fatimid caliph in Cairo he could regulate the Nile's floods, then had to admit the plan was impossible. Legend has it he feigned madness to escape the caliph's anger and spent years under house arrest. During that time he wrote his Book of Optics, which gave one of the first clear explanations of the camera obscura."},

    {"n": "George Stephenson", "inv": "Steam locomotive, railway engineering", "cc": "GB", "yr": "1781-1848",
     "fa": "George Stephenson grew up in a family where neither parent could read, and he worked at coal mines as a teenager. Still illiterate at 17 or 18, he paid for night school out of his own wages. He went on to build the Liverpool and Manchester Railway, and his son's Rocket won the famous Rainhill locomotive trials in 1829."},

    {"n": "Isambard Kingdom Brunel", "inv": "Great Western Railway, steamships", "cc": "GB", "yr": "1806-1859",
     "fa": "In 1843, while performing a magic trick for his children, engineer Isambard Kingdom Brunel accidentally swallowed a gold half-sovereign coin, which lodged in his windpipe for weeks. Doctors failed to remove it, so he designed a hinged board, had himself strapped to it and turned upside down, and the coin finally came out."},

    {"n": "James Dyson", "inv": "Bagless cyclonic vacuum cleaner", "cc": "GB", "yr": "1947-",
     "fa": "Inspired by the cyclone a sawmill used to separate sawdust from the air, James Dyson spent about five years building 5,127 prototypes of a bagless vacuum cleaner. Major manufacturers turned the idea down, so he set up his own company, and his Dual Cyclone became the fastest-selling vacuum cleaner ever made in the UK."},

    {"n": "Christopher Cockerell", "inv": "Hovercraft", "cc": "GB", "yr": "1910-1999",
     "fa": "In 1955, Christopher Cockerell tested his hovercraft idea at home with an empty cat food tin inside a coffee tin, blowing air into the gap between them and measuring the lift on kitchen scales. Four years later, his full-size SR.N1 crossed the English Channel, on the 50th anniversary of Louis Blériot's first flight across it."},

    {"n": "John Logie Baird", "inv": "Mechanical television", "cc": "GB", "yr": "1888-1946",
     "fa": "On January 26, 1926, in a workshop above a café in Soho, London, John Logie Baird gave the world's first public demonstration of live television to members of the Royal Institution. His first test images showed the head of a ventriloquist's dummy. Most of his guests were reportedly unimpressed, yet the BBC adopted his system for its first television service in 1930."},

    {"n": "Werner von Siemens", "inv": "Pointer telegraph, dynamo, electric railway", "cc": "DE", "yr": "1816-1892",
     "fa": "In 1847, Werner von Siemens founded a small company with a mechanic named Johann Georg Halske to build his improved pointer telegraph. He went on to develop the dynamo, which turned motion into electricity on an industrial scale. In 1879, his firm ran the world's first electric railway powered from an external source at a Berlin exhibition, and the company still bears his name."},

    {"n": "Konrad Zuse", "inv": "Z3, first working programmable computer", "cc": "DE", "yr": "1910-1995",
     "fa": "Konrad Zuse quit his job and built his first mechanical computer, the Z1, in his parents' Berlin living room, with friends helping out. In 1941, his Z3 became the first working programmable computer, reading its programs from discarded movie film. Allied bombing destroyed both machines in 1943, and he rebuilt the Z1 decades later for a Berlin museum."},

    {"n": "Leon Theremin", "inv": "Theremin", "cc": "RU", "yr": "1896-1993",
     "fa": "Leon Theremin invented the first electronic instrument played without being touched. Later, working in a secret Soviet prison lab, he is believed to have developed \"The Thing\", a bug hidden in a carved wooden Great Seal that Soviet schoolchildren gave the U.S. ambassador in Moscow in 1945. With no battery or wires, it went undetected for about seven years."},

    {"n": "Pavel Yablochkov", "inv": "Yablochkov candle (arc lamp)", "cc": "RU", "yr": "1847-1894",
     "fa": "Russian engineer Pavel Yablochkov patented his \"electric candle\" in Paris in 1876: two carbon rods placed side by side, which made arc lighting simple and reliable. For the 1878 World's Fair, 64 of his lamps lit up the Avenue de l'Opéra in Paris, one of the first electric street lighting systems in the world."},

    {"n": "Alexander Popov", "inv": "Radio receiver, lightning detector", "cc": "RU", "yr": "1859-1906",
     "fa": "On May 7, 1895, physicist Alexander Popov demonstrated a radio receiver in St. Petersburg, designed to detect distant lightning by its radio noise. Russia and Bulgaria still celebrate Radio Day on that date. Historians note, however, that his device only received signals, and that he didn't send messages by radio until later."},

    {"n": "László Bíró", "inv": "Ballpoint pen", "cc": "HU/AR", "yr": "1899-1985",
     "fa": "As a journalist in Budapest, László Bíró noticed that newspaper ink dried fast and didn't smudge, and set out to make a pen that could use it. Fleeing to Argentina in 1943, he patented his ballpoint pen there. Argentina celebrates its Inventors' Day on his birthday, September 29, though it was Marcel Bich who later made a fortune with the Bic."},

    {"n": "Ernő Rubik", "inv": "Rubik's Cube", "cc": "HU", "yr": "1944-",
     "fa": "In 1974, Ernő Rubik, a young architecture teacher in Budapest, built a wooden cube of small blocks to help his students think about moving objects in space. After scrambling it, he needed about a month to solve it himself. He patented it in Hungary as the \"Magic Cube\" before it went on to become one of the best-selling toys in history."},

    {"n": "Sakichi Toyoda", "inv": "Automatic loom", "cc": "JP", "yr": "1867-1930",
     "fa": "Sakichi Toyoda's 1897 power loom stopped automatically when a thread broke, an idea now at the heart of Toyota's production methods. In 1929, his son sold the patent rights of his automatic loom to the British firm Platt Brothers for 100,000 pounds. The family's loom company later created a car department, which became Toyota Motor in 1937."},

    {"n": "Momofuku Ando", "inv": "Instant noodles", "cc": "JP", "yr": "1910-2007",
     "fa": "At 48, Momofuku Ando developed instant ramen alone in a small workshop behind his house in Osaka, launching Chicken Ramen in 1958. In 1971, he followed with Cup Noodles, designed for foreigners who ate noodles with a fork. In 2005, he even created a vacuum-packed version for a Japanese astronaut on the Space Shuttle."},

    {"n": "Kōkichi Mikimoto", "inv": "Cultured pearls", "cc": "JP", "yr": "1858-1954",
     "fa": "After many failures, Kōkichi Mikimoto produced the first semi-round cultured pearl on July 11, 1893, and perfectly round ones followed in 1917. When he visited Thomas Edison in 1927, the American inventor was so impressed that he reportedly called cultured pearls one of the wonders of the world."},

    {"n": "Jagadish Chandra Bose", "inv": "Millimeter-wave radio experiments", "cc": "IN", "yr": "1858-1937",
     "fa": "In a public demonstration in Kolkata in the mid-1890s, physicist Jagadish Chandra Bose sent invisible waves through walls to ring a bell and ignite a small heap of gunpowder at a distance. He worked with wavelengths of just a few millimeters, a pioneering step toward microwaves, and chose not to patent his radio work."},

    {"n": "Alberto Santos-Dumont", "inv": "14-bis airplane, Demoiselle", "cc": "BR", "yr": "1873-1932",
     "fa": "On November 12, 1906, the Brazilian Alberto Santos-Dumont flew his 14-bis airplane 220 meters in Paris, the first officially verified powered flight in Europe. His friend Louis Cartier designed a wristwatch for him so he could check the time without letting go of the controls, and the Cartier Santos is still sold today."},

    {"n": "Narcís Monturiol", "inv": "Ictíneo submarines", "cc": "ES", "yr": "1819-1885",
     "fa": "After seeing a coral diver die off the Catalan coast, Narcís Monturiol designed a submarine to make the work safer. His hand-cranked Ictíneo dived in Barcelona's harbor in 1859, and its successor, Ictíneo II, used a chemical engine that also produced oxygen for the crew. His company went bankrupt, and creditors took the submarine."},

    {"n": "Juan de la Cierva", "inv": "Autogiro", "cc": "ES", "yr": "1895-1936",
     "fa": "In January 1923, Spanish engineer Juan de la Cierva's autogiro flew near Madrid, with a free-spinning rotor that kept it airborne at low speed, a key step toward the helicopter. Ironically, he died in an ordinary airplane: in December 1936, the airliner he was traveling in crashed while taking off from Croydon in thick fog."},

    {"n": "Lewis Latimer", "inv": "Improved carbon filament manufacturing", "cc": "US", "yr": "1848-1928",
     "fa": "The son of parents who had escaped slavery, Lewis Latimer taught himself technical drawing by watching draftsmen and buying secondhand books. At a Boston patent firm, he drafted drawings for Alexander Graham Bell's telephone application, then patented an improved way to manufacture the carbon filaments inside light bulbs."},

    {"n": "Granville Woods", "inv": "Induction telegraph for moving trains", "cc": "US", "yr": "1856-1910",
     "fa": "Granville Woods patented a system in 1887 that let moving trains communicate with stations by telegraph. Thomas Edison sued him, claiming he had invented it first, and Woods won. Newspapers of the time nicknamed him \"the Black Edison\", and accounts say Edison then offered him a position, which Woods declined."},

    {"n": "Isaac Singer", "inv": "Singer sewing machine", "cc": "US", "yr": "1811-1875",
     "fa": "Before making sewing machines, Isaac Singer toured as an actor with a traveling theater troupe. He patented his improved machine in 1851, and his company sold it on installments, a few dollars down and the rest monthly, an idea usually credited to his partner Edward Clark. In his will, Singer acknowledged 22 children."},

    {"n": "King C. Gillette", "inv": "Disposable safety razor blade", "cc": "US", "yr": "1855-1932",
     "fa": "Experts at MIT reportedly told King Gillette that a thin, cheap, disposable steel blade was impossible to make. Engineer William Nickerson proved them wrong, but the first year of sales, 1903, brought in just 51 blades and 168 razors. Gillette, oddly enough, hoped to be remembered as a social reformer opposed to capitalism."},

    {"n": "Reginald Fessenden", "inv": "Voice radio transmission", "cc": "CA", "yr": "1866-1932",
     "fa": "Canadian inventor Reginald Fessenden is famous for what may have been the first radio broadcast of voice and music, on Christmas Eve 1906, playing \"O Holy Night\" on the violin. But historians found no newspaper report of it at the time, and he only described it decades later, so many now doubt it ever happened."},

    {"n": "David Unaipon", "inv": "Improved sheep shearing handpiece", "cc": "AU", "yr": "1872-1967",
     "fa": "Ngarrindjeri inventor, preacher and writer David Unaipon patented an improved sheep shearing tool in 1909, but could only afford a provisional patent and never profited when similar designs spread. In 1914, he drew on the boomerang to sketch ideas for a helicopter. He now appears on Australia's 50 dollar banknote."},

    {"n": "Jang Yeong-sil", "inv": "Self-striking water clock, rain gauge", "cc": "KR", "yr": None,
     "fa": "Born into the lowest class of Joseon Korea, Jang Yeong-sil was promoted to royal official by King Sejong for his engineering talent. He built Korea's first self-striking water clock in 1434 and its first rain gauge in 1441. According to some accounts, his career ended in 1442 when a royal sedan chair he had built broke, and his later life went unrecorded."},

    {"n": "George Westinghouse", "inv": "Railway air brake", "cc": "US", "yr": "1846-1914",
     "fa": "George Westinghouse was in his early twenties when he patented his railway air brake in 1869, letting a single engineer stop an entire train. It eventually became mandatory on American trains. He accumulated hundreds of patents, and later backed Nikola Tesla's alternating current against Thomas Edison."},

    {"n": "Christiaan Huygens", "inv": "Pendulum clock", "cc": "NL", "yr": "1629-1695",
     "fa": "In 1656, Dutch scientist Christiaan Huygens built the first successful pendulum clock, cutting a clock's typical error from around 15 minutes a day to around 15 seconds. He was also an astronomer: the year before, using a telescope he had designed himself, he discovered Titan, Saturn's largest moon."},
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
        time.sleep(2.5)

    out = Path("assets/tech/legendary_inventors.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(records, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    sys.stdout.buffer.write((chr(10) + f"Done: {found}/{total} images found." + chr(10)).encode("utf-8"))


if __name__ == "__main__":
    main()
