import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=name, rs=reign start (year, negative for BCE), re=reign end (year, negative for BCE),
# fa=famous for, hn=historical note (optional), im=imageUrl
#
# Content is written in ENGLISH (source language for the app's translation pipeline, see
# content_loader.dart).

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Direct image URL overrides, for entries whose Wikipedia infobox image doesn't fit the
# map-or-portrait rule (Qing dynasty's own infobox image is a flag, not a map or portrait).
IMAGE_OVERRIDES = {
    "Qing": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/cf/Portrait_of_the_Kangxi_Emperor_in_Court_Dress.jpg/500px-Portrait_of_the_Kangxi_Emperor_in_Court_Dress.jpg",
}

# Overrides where the name doesn't map cleanly to its Wikipedia article title.
WIKI_EN = {
    "Xia": "Xia dynasty",
    "Shang": "Shang dynasty",
    "Zhou": "Zhou dynasty",
    "Qin": "Qin dynasty",
    "Han": "Han dynasty",
    "Jin": "Jin dynasty (266-420)",
    "Sui": "Sui dynasty",
    "Tang": "Tang dynasty",
    "Song": "Song dynasty",
    "Yuan": "Yuan dynasty",
    "Ming": "Ming dynasty",
    "Qing": "Qing dynasty",
}

records = [
    {"n": 'Xia', "rs": -2070, "re": -1600,
     "fa": "Traditionally regarded as China's first dynasty, credited with founding hereditary rule and early flood-control engineering, though its existence as an organized state remains unconfirmed by direct archaeological inscriptions.",
     "hn": 'Unlike every dynasty that followed it, no Xia-era writing has ever been found; everything known about it comes from texts written centuries later, which is why some historians treat it as part legend.'},

    {"n": 'Shang', "rs": -1600, "re": -1046,
     "fa": 'The first Chinese dynasty confirmed by direct archaeological evidence, famous for elaborate bronze ritual vessels and oracle bones, inscribed turtle shells and ox bones used to divine the future and record the earliest known Chinese writing.',
     "hn": None},

    {"n": 'Zhou', "rs": -1046, "re": -256,
     "fa": "The longest-lasting dynasty in Chinese history at roughly 800 years, it introduced the Mandate of Heaven, the idea that a ruler's right to govern depends on just rule and can be withdrawn, a concept that shaped Chinese political thought for three millennia.",
     "hn": 'Its later centuries fractured into the Warring States period, when the Zhou king still held nominal authority even as regional lords fought near-constant wars around him.'},

    {"n": 'Qin', "rs": -221, "re": -206,
     "fa": "Lasted only 15 years but permanently unified China's warring kingdoms for the first time under Qin Shi Huang, who standardized writing, currency, and weights, and connected regional defensive walls into what became the Great Wall.",
     "hn": 'Qin Shi Huang was buried with an entire army of over 8,000 life-sized terracotta soldiers meant to protect him in the afterlife, undiscovered until farmers stumbled on it in 1974.'},

    {"n": 'Han', "rs": -206, "re": 220,
     "fa": 'Opened the Silk Road trade route to Central Asia and the Mediterranean world, and made Confucianism the official state philosophy, a combination that shaped Chinese identity so deeply that the majority ethnic group in China still calls itself the Han people.',
     "hn": None},

    {"n": 'Jin', "rs": 265, "re": 420,
     "fa": 'Briefly reunified China after the chaos following the Han collapse, but spent most of its existence as the Eastern Jin ruling only the south after losing the north to invasion, a period still notable for major advances in calligraphy and painting.',
     "hn": None},

    {"n": 'Sui', "rs": 581, "re": 618,
     "fa": 'Reunified China after nearly four centuries of division and built the Grand Canal, an engineering project over a thousand miles long linking the north and south that remains the longest canal system in the world.',
     "hn": 'Its ambitious public works and costly foreign wars exhausted the population so badly that, like the Qin before it, the dynasty collapsed within decades despite its lasting achievements.'},

    {"n": 'Tang', "rs": 618, "re": 907,
     "fa": "Widely regarded as a golden age of Chinese civilization, with its capital Chang'an becoming one of the largest and most cosmopolitan cities on Earth, open to merchants, monks, and diplomats from across Asia and the Middle East.",
     "hn": "It produced China's only female emperor, Wu Zetian, who ruled in her own right for 15 years after rising from a concubine to seize the throne."},

    {"n": 'Song', "rs": 960, "re": 1279,
     "fa": 'A period of extraordinary technological innovation that gave the world the magnetic compass, gunpowder weapons, movable-type printing, and the first government-issued paper money, even as the dynasty struggled militarily against northern neighbors.',
     "hn": None},

    {"n": 'Yuan', "rs": 1271, "re": 1368,
     "fa": "Founded by the Mongol ruler Kublai Khan after his grandfather Genghis Khan's conquests, it was the first dynasty to rule all of China under a foreign, non-Chinese ruling house, and hosted the Venetian traveler Marco Polo at its court.",
     "hn": None},

    {"n": 'Ming', "rs": 1368, "re": 1644,
     "fa": "Built the Forbidden City in Beijing as the imperial palace and sent Admiral Zheng He on seven massive naval expeditions as far as East Africa decades before Europe's age-of-exploration voyages, before later turning inward and restricting foreign contact.",
     "hn": None},

    {"n": 'Qing', "rs": 1644, "re": 1912,
     "fa": "China's last imperial dynasty and the second to be founded by a non-Han people, the Manchus, it collapsed in 1912 when six-year-old Emperor Puyi abdicated, ending over two thousand years of Chinese imperial rule.",
     "hn": None},
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
        name = s["n"]
        if name in IMAGE_OVERRIDES:
            img = IMAGE_OVERRIDES[name]
        else:
            title = WIKI_EN.get(name, name)
            img = wiki_img(title)
        s["im"] = img
        if img:
            found += 1
        status = "ok" if img else "xx"
        sys.stdout.buffer.write((f"  [{i+1:2}/{total}] {status} {name}" + chr(10)).encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)

    out = Path("assets/history/chinese_dynasties.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(records, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    sys.stdout.buffer.write((chr(10) + f"Done: {found}/{total} images found -- {total} dynasties total." + chr(10)).encode("utf-8"))


if __name__ == "__main__":
    main()
