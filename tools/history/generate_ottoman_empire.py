import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=name, dy=historical era (not dynasty, all 36 belong to the single House of Osman),
# rs=reign start (year), re=reign end (year), ni=nickname (optional), fa=famous for,
# hn=historical note (optional), im=imageUrl
#
# Content is written in ENGLISH (source language for the app's translation pipeline, see
# content_loader.dart).

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Overrides where the name doesn't map cleanly to its Wikipedia article title.
WIKI_EN = {
    "Osman I": "Osman I",
    "Murad I": "Murad I",
    "Bayezid I": "Bayezid I",
    "Mehmed I": "Mehmed I",
    "Murad II": "Murad II",
    "Mehmed II": "Mehmed II",
    "Bayezid II": "Bayezid II",
    "Selim I": "Selim I",
    "Suleiman I": "Suleiman the Magnificent",
    "Selim II": "Selim II",
    "Murad III": "Murad III",
    "Mehmed III": "Mehmed III",
    "Ahmed I": "Ahmed I",
    "Mustafa I": "Mustafa I",
    "Osman II": "Osman II",
    "Murad IV": "Murad IV",
    "Ibrahim": "Ibrahim (Ottoman sultan)",
    "Mehmed IV": "Mehmed IV",
    "Suleiman II": "Suleiman II (Ottoman sultan)",
    "Ahmed II": "Ahmed II",
    "Mustafa II": "Mustafa II",
    "Ahmed III": "Ahmed III",
    "Mahmud I": "Mahmud I",
    "Osman III": "Osman III",
    "Mustafa III": "Mustafa III",
    "Abdul Hamid I": "Abdul Hamid I",
    "Selim III": "Selim III",
    "Mustafa IV": "Mustafa IV",
    "Mahmud II": "Mahmud II",
    "Abdulmejid I": "Abdulmejid I",
    "Abdulaziz": "Abdulaziz",
    "Murad V": "Murad V",
    "Abdul Hamid II": "Abdul Hamid II",
    "Mehmed V": "Mehmed V",
    "Mehmed VI": "Mehmed VI",
}

records = [
    {"n": 'Osman I', "dy": 'Foundation', "rs": 1299, "re": 1323, "ni": 'Osman Gazi',
     "fa": 'Founded a small Turkish principality in northwestern Anatolia that his descendants would grow into an empire spanning three continents and lasting over six centuries.',
     "hn": None},

    {"n": 'Orhan', "dy": 'Foundation', "rs": 1323, "re": 1362, "ni": None,
     "fa": 'Captured the Byzantine city of Bursa and made it his capital, then became the first Ottoman ruler to cross into Europe, establishing a foothold in the Balkans that would never be relinquished.',
     "hn": None},

    {"n": 'Murad I', "dy": 'Foundation', "rs": 1362, "re": 1389, "ni": None,
     "fa": 'Expanded Ottoman territory deep into the Balkans and was the first ruler to adopt the title Sultan, but was assassinated by a Serbian knight just after winning the decisive Battle of Kosovo.',
     "hn": None},

    {"n": 'Bayezid I', "dy": 'Foundation', "rs": 1389, "re": 1402, "ni": 'The Thunderbolt',
     "fa": 'Expanded the empire rapidly enough to besiege Constantinople itself, but his overconfidence led to catastrophic defeat and capture by the Central Asian conqueror Timur at the Battle of Ankara.',
     "hn": 'He died in captivity less than a year later, and the empire nearly collapsed entirely during the decade-long civil war between his sons that followed.'},

    {"n": 'Mehmed I', "dy": 'Rise', "rs": 1413, "re": 1421, "ni": 'The Restorer',
     "fa": "Reunified the Ottoman state after winning a bitter civil war against his own brothers that followed Bayezid I's catastrophic defeat, earning his epithet as the empire's second founder.",
     "hn": None},

    {"n": 'Murad II', "dy": 'Rise', "rs": 1421, "re": 1444, "ni": None,
     "fa": 'Twice voluntarily abdicated the throne to his young son Mehmed II to retire to a life of contemplation, only to be called back both times by crises he alone seemed able to resolve.',
     "hn": None},

    {"n": 'Mehmed II', "dy": 'Rise', "rs": 1444, "re": 1446, "ni": 'The Conqueror',
     "fa": 'Captured Constantinople in 1453 at just 21 years old, ending the thousand-year Byzantine Empire and transforming the Ottoman state into a true empire with the city as its new capital.',
     "hn": None},

    {"n": 'Bayezid II', "dy": 'Rise', "rs": 1481, "re": 1512, "ni": 'The Just',
     "fa": 'Welcomed tens of thousands of Jewish and Muslim refugees expelled from Spain in 1492, sending the Ottoman navy to help transport them, and was eventually forced to abdicate in favor of his son Selim.',
     "hn": None},

    {"n": 'Selim I', "dy": 'Rise', "rs": 1512, "re": 1520, "ni": 'The Grim',
     "fa": "Nearly doubled the size of the empire in an eight-year reign by conquering Persia's borderlands and the entire Mamluk Sultanate of Egypt and the Levant, becoming the first Ottoman sultan to claim the title of Caliph.",
     "hn": None},

    {"n": 'Suleiman I', "dy": 'Classical Age', "rs": 1520, "re": 1566, "ni": 'The Magnificent',
     "fa": 'Presided over the empire at its territorial and cultural peak across a 46-year reign, codifying Ottoman law, capturing Belgrade and Rhodes, and besieging Vienna, while Ottoman naval power came to dominate the Mediterranean.',
     "hn": None},

    {"n": 'Selim II', "dy": 'Transformation', "rs": 1566, "re": 1574, "ni": 'The Blond',
     "fa": 'Conquered Cyprus from Venice, but then watched the Ottoman fleet get destroyed at the Battle of Lepanto just months later, the first major naval defeat in Ottoman history, though the empire kept Cyprus anyway.',
     "hn": None},

    {"n": 'Murad III', "dy": 'Transformation', "rs": 1574, "re": 1595, "ni": None,
     "fa": 'Oversaw significant territorial gains against Persia but is remembered largely for his enormous harem, reportedly fathering over 100 children.',
     "hn": None},

    {"n": 'Mehmed III', "dy": 'Transformation', "rs": 1595, "re": 1603, "ni": None,
     "fa": 'Had all nineteen of his brothers strangled with a silk cord on the night of his accession to eliminate rival claimants, a mass execution so shocking it turned public opinion against the centuries-old practice of royal fratricide.',
     "hn": None},

    {"n": 'Ahmed I', "dy": 'Transformation', "rs": 1603, "re": 1617, "ni": None,
     "fa": 'Built the Blue Mosque in Istanbul and ended the Ottoman tradition of executing royal brothers, replacing it with a system of confining potential heirs to a secluded palace apartment known as the Kafes, or cage.',
     "hn": None},

    {"n": 'Mustafa I', "dy": 'Transformation', "rs": 1617, "re": 1618, "ni": 'The Mad',
     "fa": 'Became the first prince to experience the new Kafes system, but having spent his entire life confined with no preparation for rule, he proved unfit to govern and was deposed twice in barely a year combined on the throne.',
     "hn": None},

    {"n": 'Osman II', "dy": 'Transformation', "rs": 1618, "re": 1622, "ni": None,
     "fa": 'Tried to curb the power of the elite Janissary soldiers and was overthrown and strangled by them in 1622, becoming the first Ottoman sultan ever killed by his own troops.',
     "hn": None},

    {"n": 'Murad IV', "dy": 'Transformation', "rs": 1623, "re": 1640, "ni": None,
     "fa": "Banned coffee, tobacco, and alcohol across the empire on pain of death and reportedly patrolled Istanbul's streets in disguise at night to personally catch and execute violators.",
     "hn": None},

    {"n": 'Ibrahim', "dy": 'Transformation', "rs": 1640, "re": 1648, "ni": 'The Mad',
     "fa": 'Had spent years in the Kafes in constant fear of execution by his brother before taking the throne, and his increasingly erratic rule, including a reported obsession with sable fur, ended when the Janissaries deposed and executed him.',
     "hn": None},

    {"n": 'Mehmed IV', "dy": 'Transformation', "rs": 1648, "re": 1687, "ni": 'The Hunter',
     "fa": "Became sultan at age six and reigned for nearly 40 years, but his reign is best remembered for the disastrous second Ottoman siege of Vienna in 1683, a defeat that marked the start of the empire's long retreat from Central Europe.",
     "hn": None},

    {"n": 'Suleiman II', "dy": 'Transformation', "rs": 1687, "re": 1691, "ni": None,
     "fa": 'Spent nearly his entire adult life confined in the Kafes before taking the throne at 45, inheriting a difficult war against an alliance of European powers.',
     "hn": None},

    {"n": 'Ahmed II', "dy": 'Transformation', "rs": 1691, "re": 1695, "ni": None,
     "fa": 'Ruled during continued military setbacks in the long war against the Holy League and died after a brief, largely unremarkable reign.',
     "hn": None},

    {"n": 'Mustafa II', "dy": 'Transformation', "rs": 1695, "re": 1703, "ni": None,
     "fa": 'Led his armies personally in campaigns against Austria but was ultimately deposed after a military and tax revolt known as the Edirne Event, after which he retired from public life entirely.',
     "hn": None},

    {"n": 'Ahmed III', "dy": 'Old Regime', "rs": 1703, "re": 1730, "ni": None,
     "fa": "Presided over the Tulip Era, a period of relative peace defined by lavish gardens, poetry, and the introduction of the Ottoman Empire's first printing press, before a popular revolt over the court's extravagance forced his abdication.",
     "hn": None},

    {"n": 'Mahmud I', "dy": 'Old Regime', "rs": 1730, "re": 1754, "ni": None,
     "fa": "Took the throne immediately after the revolt that toppled his uncle and spent his reign stabilizing the empire's finances and military after the excesses of the Tulip Era.",
     "hn": None},

    {"n": 'Osman III', "dy": 'Old Regime', "rs": 1754, "re": 1757, "ni": None,
     "fa": "Reportedly disliked the sound of women's shoes clicking on palace floors so much that he had carpets laid everywhere and required female staff to wear felt-soled footwear during his short reign.",
     "hn": None},

    {"n": 'Mustafa III', "dy": 'Old Regime', "rs": 1757, "re": 1774, "ni": None,
     "fa": 'Tried to modernize the Ottoman military along European lines but was unable to prevent a disastrous war with Russia that ended in one of the most humiliating treaties in Ottoman history.',
     "hn": None},

    {"n": 'Abdul Hamid I', "dy": 'Old Regime', "rs": 1774, "re": 1789, "ni": None,
     "fa": "Inherited and had to sign the Treaty of Kucuk Kaynarca, which ceded Crimea's independence from Ottoman control and gave Russia the right to intervene on behalf of Orthodox Christians within the empire, a clause later used repeatedly to justify Russian meddling.",
     "hn": None},

    {"n": 'Selim III', "dy": 'Decline and Modernization', "rs": 1789, "re": 1807, "ni": None,
     "fa": 'Launched sweeping military and administrative reforms called the Nizam-i Cedid to modernize the Ottoman army along European lines, provoking a Janissary revolt that deposed him and, a year later, had him assassinated.',
     "hn": 'He remains the only Ottoman sultan known to have been killed by a sword rather than strangulation, the traditional method reserved for royalty.'},

    {"n": 'Mustafa IV', "dy": 'Decline and Modernization', "rs": 1807, "re": 1808, "ni": None,
     "fa": "Came to power through the revolt that deposed his reformist cousin Selim III, then was himself overthrown within a year by soldiers trying to restore Selim, having ordered Selim's murder as they stormed the palace.",
     "hn": None},

    {"n": 'Mahmud II', "dy": 'Decline and Modernization', "rs": 1808, "re": 1839, "ni": 'The Reformer',
     "fa": 'Destroyed the centuries-old Janissary corps in a single bloody day in 1826, known as the Auspicious Incident, after they revolted against his attempt to modernize the army, clearing the way for sweeping Westernizing reforms.',
     "hn": None},

    {"n": 'Abdulmejid I', "dy": 'Decline and Modernization', "rs": 1839, "re": 1861, "ni": None,
     "fa": "Launched the Tanzimat reforms, a sweeping program that granted equal legal rights to non-Muslim subjects and modernized the empire's administration, education, and finances along European lines.",
     "hn": None},

    {"n": 'Abdulaziz', "dy": 'Decline and Modernization', "rs": 1861, "re": 1876, "ni": None,
     "fa": "Built the Ottoman Empire's first modern ironclad navy, among the largest in the world at the time, but ran the treasury into bankruptcy doing it and was deposed amid an economic crisis.",
     "hn": 'He was found dead in his palace apartment days after his deposition, officially ruled a suicide, though persistent rumors of murder have never been fully resolved.'},

    {"n": 'Murad V', "dy": 'Decline and Modernization', "rs": 1876, "re": 1876, "ni": None,
     "fa": "Reigned for just 93 days, the shortest of any Ottoman sultan, before being deposed due to a severe mental breakdown triggered by witnessing his uncle's violent overthrow and death just before his own accession.",
     "hn": None},

    {"n": 'Abdul Hamid II', "dy": 'Decline and Modernization', "rs": 1876, "re": 1909, "ni": 'The Red Sultan',
     "fa": "The last sultan to wield genuine personal power, he suspended the empire's first constitution within two years of taking the throne and ruled through an extensive secret police network before being deposed by the Young Turk movement.",
     "hn": None},

    {"n": 'Mehmed V', "dy": 'Constitutional Era', "rs": 1909, "re": 1918, "ni": None,
     "fa": "Installed as a largely ceremonial constitutional monarch after his brother's deposition, he had little real authority as the Young Turk government led the empire into a disastrous alliance with Germany in the First World War.",
     "hn": None},

    {"n": 'Mehmed VI', "dy": 'Constitutional Era', "rs": 1918, "re": 1922, "ni": None,
     "fa": 'Became the 36th and final Ottoman sultan as the empire collapsed after its defeat in the First World War, and left the country aboard a British warship in 1922 after the Turkish parliament formally abolished the sultanate.',
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
        title = WIKI_EN.get(name, name)
        img = wiki_img(title)
        s["im"] = img
        if img:
            found += 1
        status = "ok" if img else "xx"
        sys.stdout.buffer.write((f"  [{i+1:2}/{total}] {status} {name}" + chr(10)).encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)

    out = Path("assets/history/ottoman_empire.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(records, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    sys.stdout.buffer.write((chr(10) + f"Done: {found}/{total} images found -- {total} sultans total." + chr(10)).encode("utf-8"))


if __name__ == "__main__":
    main()
