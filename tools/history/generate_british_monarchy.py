import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=name, dy=house/dynasty, rs=reign start (year), re=reign end (year, null if still
# reigning), ni=nickname (optional), fa=famous for, hn=historical note (optional),
# im=imageUrl
#
# Content is written in ENGLISH (source language for the app's translation pipeline, see
# content_loader.dart).

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Overrides where the name doesn't map cleanly to its Wikipedia article title.
WIKI_EN = {
    "Edmund I": "Edmund I",
    "Edgar the Peaceful": "Edgar, King of England",
    "Harold II Godwinson": "Harold Godwinson",
    "William II Rufus": "William II of England",
    "Henry I": "Henry I of England",
    "Stephen": "Stephen, King of England",
    "Henry II": "Henry II of England",
    "John": "John, King of England",
    "Henry III": "Henry III of England",
    "Henry IV": "Henry IV of England",
    "Henry V": "Henry V of England",
    "Henry VI": "Henry VI of England",
    "Richard III": "Richard III of England",
    "Henry VII": "Henry VII of England",
    "Jane Grey": "Lady Jane Grey",
    "James I": "James VI and I",
    "Charles I": "Charles I of England",
    "Charles II": "Charles II of England",
    "James II": "James II of England",
    "William III and Mary II": "William III of England",
    "Anne": "Anne, Queen of Great Britain",
    "George I": "George I of Great Britain",
    "George II": "George II of Great Britain",
    "Victoria": "Queen Victoria",
}

records = [
    {"n": 'Alfred the Great', "dy": 'House of Wessex', "rs": 871, "re": 899, "ni": 'The Great',
     "fa": 'United the Anglo-Saxon kingdoms against Viking invasion and is generally regarded by historians as the first King of England.',
     "hn": "A later legend claims he once burned a batch of cakes while hiding from the Vikings in a peasant woman's hut, distracted by his military troubles; the story only appears in writing more than a century after his death."},

    {"n": 'Edward the Elder', "dy": 'House of Wessex', "rs": 899, "re": 924, "ni": None,
     "fa": "Continued his father Alfred's reconquest of Viking-held territory and extended West Saxon control over most of England south of the Humber.",
     "hn": None},

    {"n": 'Æthelstan', "dy": 'House of Wessex', "rs": 924, "re": 939, "ni": None,
     "fa": 'Became the first king to rule a genuinely unified Kingdom of England after his decisive victory at the Battle of Brunanburh against a combined Scottish and Viking army.',
     "hn": None},

    {"n": 'Edmund I', "dy": 'House of Wessex', "rs": 939, "re": 946, "ni": None,
     "fa": "Recaptured territory lost to Viking rule in the Midlands, restoring much of his predecessor Æthelstan's unified kingdom.",
     "hn": 'He was stabbed to death at a royal feast while trying to pull an outlaw off one of his own officers, dying at just 25 years old.'},

    {"n": 'Eadred', "dy": 'House of Wessex', "rs": 946, "re": 955, "ni": None,
     "fa": 'Finally crushed Viking rule in Northumbria for good, ending the independent Viking Kingdom of York.',
     "hn": None},

    {"n": 'Eadwig', "dy": 'House of Wessex', "rs": 955, "re": 959, "ni": 'All-Fair',
     "fa": 'His short and chaotic reign was overshadowed by conflict with the church and nobility that eventually split his kingdom.',
     "hn": 'According to a near-contemporary account, churchmen found him missing from his own coronation feast and had to drag him back after discovering him in bed with a noblewoman and her daughter.'},

    {"n": 'Edgar the Peaceful', "dy": 'House of Wessex', "rs": 959, "re": 975, "ni": 'The Peaceful',
     "fa": 'Presided over a period of stability and church reform so settled that he reportedly had himself rowed on a river by eight tributary kings as a show of dominance.',
     "hn": None},

    {"n": 'Edward the Martyr', "dy": 'House of Wessex', "rs": 975, "re": 978, "ni": 'The Martyr',
     "fa": "Ruled for less than three years before being murdered at Corfe Castle, probably on the orders of his stepmother's faction to clear the way for her own son.",
     "hn": None},

    {"n": 'Æthelred the Unready', "dy": 'House of Wessex', "rs": 978, "re": 1016, "ni": 'The Unready',
     "fa": "His nickname is a pun on his name meaning 'noble counsel' combined with 'unraed', meaning poorly advised; his reign was marked by repeated Viking raids he tried to buy off with tribute known as Danegeld.",
     "hn": None},

    {"n": 'Edmund Ironside', "dy": 'House of Wessex', "rs": 1016, "re": 1016, "ni": 'Ironside',
     "fa": 'Fought a fierce defensive campaign against the invading Danish king Cnut and briefly split England with him by treaty before dying only months into his reign.',
     "hn": None},

    {"n": 'Cnut the Great', "dy": 'House of Denmark', "rs": 1016, "re": 1035, "ni": 'The Great',
     "fa": 'A Danish king who conquered England and ruled a North Sea empire spanning Denmark, Norway, and England simultaneously.',
     "hn": 'A famous legend has him ordering the incoming tide to halt to prove to flattering courtiers that even a king has no power over nature, not to show off his own power as the story is often misremembered.'},

    {"n": 'Edward the Confessor', "dy": 'House of Wessex', "rs": 1042, "re": 1066, "ni": 'The Confessor',
     "fa": 'Founded Westminster Abbey, which has hosted nearly every English coronation since, and his death without a clear heir triggered the succession crisis that led directly to the Norman Conquest.',
     "hn": None},

    {"n": 'Harold II Godwinson', "dy": 'House of Wessex', "rs": 1066, "re": 1066, "ni": None,
     "fa": 'The last Anglo-Saxon King of England, he defeated an invading Norwegian army at Stamford Bridge only to march south and lose both the Battle of Hastings and his life weeks later.',
     "hn": 'The Bayeux Tapestry famously depicts him being struck in the eye by an arrow, though historians still debate whether that figure is really him.'},

    {"n": 'William the Conqueror', "dy": 'House of Normandy', "rs": 1066, "re": 1087, "ni": 'The Conqueror',
     "fa": 'Defeated King Harold II at the Battle of Hastings and became the first Norman king of England, fundamentally reshaping English law, land ownership, and language.',
     "hn": 'He commissioned the Domesday Book, an exhaustive survey of nearly every landholding in England, largely to work out exactly how much he could tax.'},

    {"n": 'William II Rufus', "dy": 'House of Normandy', "rs": 1087, "re": 1100, "ni": 'Rufus',
     "fa": 'Ruled as an unpopular, hard-fisted king mostly remembered today for the mysterious circumstances of his death.',
     "hn": 'He was killed by an arrow while hunting in the New Forest; the shooter fled the country immediately afterward, and his younger brother Henry, who benefited most from his death, was crowned king within days.'},

    {"n": 'Henry I', "dy": 'House of Normandy', "rs": 1100, "re": 1135, "ni": 'Beauclerc',
     "fa": 'Strengthened royal administration and the treasury during a relatively stable reign, but his careful succession planning was undone by a single shipwreck.',
     "hn": "His only legitimate son and heir drowned when the White Ship sank off the Normandy coast in 1120, triggering the succession crisis that led to a civil war known as the Anarchy after Henry's death."},

    {"n": 'Stephen', "dy": 'House of Blois', "rs": 1135, "re": 1154, "ni": None,
     "fa": 'His contested claim to the throne against his cousin Matilda plunged England into a prolonged civil war later known simply as the Anarchy.',
     "hn": None},

    {"n": 'Henry II', "dy": 'House of Plantagenet', "rs": 1154, "re": 1189, "ni": None,
     "fa": 'Built a vast cross-Channel Angevin Empire stretching from Scotland to the Pyrenees and reformed English common law in ways still felt today.',
     "hn": 'His famous outburst asking who would rid him of his troublesome priest was taken literally by four knights, who murdered Archbishop Thomas Becket inside Canterbury Cathedral; Henry performed public penance for the killing.'},

    {"n": 'Richard I', "dy": 'House of Plantagenet', "rs": 1189, "re": 1199, "ni": 'The Lionheart',
     "fa": 'Spent most of his reign abroad leading the Third Crusade and was later captured and held for ransom on his way home, with England footing an enormous bill to free him.',
     "hn": 'He is estimated to have spent only around six months of his ten-year reign actually in England.'},

    {"n": 'John', "dy": 'House of Plantagenet', "rs": 1199, "re": 1216, "ni": 'Lackland',
     "fa": "Lost most of his family's territory in France and was forced by rebellious barons to sign Magna Carta in 1215, limiting royal power for the first time in writing.",
     "hn": None},

    {"n": 'Henry III', "dy": 'House of Plantagenet', "rs": 1216, "re": 1272, "ni": None,
     "fa": 'Became king at just nine years old and later rebuilt Westminster Abbey in its current Gothic form, though his reign was repeatedly disrupted by baronial revolts.',
     "hn": None},

    {"n": 'Edward I', "dy": 'House of Plantagenet', "rs": 1272, "re": 1307, "ni": 'Longshanks',
     "fa": 'Conquered Wales and waged relentless war against Scotland, earning the nickname Hammer of the Scots; he also expelled the entire Jewish population from England in 1290.',
     "hn": None},

    {"n": 'Edward II', "dy": 'House of Plantagenet', "rs": 1307, "re": 1327, "ni": None,
     "fa": 'Was deposed by his own wife and her lover after years of military failure and conflict with the nobility over his close favorites.',
     "hn": 'A gruesome legend claims he was killed with a red-hot poker, a story that only appeared years after his death and is now considered almost certainly a myth; most historians believe he was simply suffocated.'},

    {"n": 'Edward III', "dy": 'House of Plantagenet', "rs": 1327, "re": 1377, "ni": None,
     "fa": "Launched the Hundred Years' War by claiming the French throne and founded the prestigious Order of the Garter, England's highest order of chivalry.",
     "hn": None},

    {"n": 'Richard II', "dy": 'House of Plantagenet', "rs": 1377, "re": 1399, "ni": None,
     "fa": "Became king at age ten and famously faced down the Peasants' Revolt in person at just 14, but was later deposed and probably murdered by his own cousin Henry Bolingbroke.",
     "hn": None},

    {"n": 'Henry IV', "dy": 'House of Lancaster', "rs": 1399, "re": 1413, "ni": None,
     "fa": 'Seized the throne from his cousin Richard II, becoming the first Lancastrian king and spending much of his reign defending his legitimacy against rebellions.',
     "hn": None},

    {"n": 'Henry V', "dy": 'House of Lancaster', "rs": 1413, "re": 1422, "ni": None,
     "fa": "Won a stunning victory against a far larger French army at the Battle of Agincourt in 1415, a triumph still remembered as one of English history's greatest military upsets.",
     "hn": None},

    {"n": 'Henry VI', "dy": 'House of Lancaster', "rs": 1422, "re": 1461, "ni": None,
     "fa": "Became king as a nine-month-old infant and lost nearly all of England's territory in France as an adult, while recurring bouts of mental illness helped trigger the Wars of the Roses.",
     "hn": "He founded both Eton College and King's College, Cambridge, institutions that still exist today, during the rare calmer periods of his reign."},

    {"n": 'Edward IV', "dy": 'House of York', "rs": 1461, "re": 1483, "ni": None,
     "fa": 'Seized the throne from the Lancastrians during the Wars of the Roses and briefly lost it again before reclaiming it, ruling for most of two decades.',
     "hn": None},

    {"n": 'Edward V', "dy": 'House of York', "rs": 1483, "re": 1483, "ni": None,
     "fa": 'Reigned for less than three months as a 12-year-old before vanishing into the Tower of London along with his younger brother; neither boy was ever seen alive again.',
     "hn": 'Their fate, known to history as the mystery of the Princes in the Tower, remains unsolved, with their uncle Richard III the most commonly suspected culprit.'},

    {"n": 'Richard III', "dy": 'House of York', "rs": 1483, "re": 1485, "ni": None,
     "fa": 'The last English king to die in battle, killed at Bosworth Field fighting the eventual Henry VII; his short reign remains overshadowed by the disappearance of his two young nephews.',
     "hn": 'His remains were lost for over 500 years until archaeologists found his skeleton, its spine curved by scoliosis, beneath a Leicester city council car park in 2012.'},

    {"n": 'Henry VII', "dy": 'House of Tudor', "rs": 1485, "re": 1509, "ni": None,
     "fa": 'Ended the Wars of the Roses by defeating Richard III at Bosworth and founded the Tudor dynasty, then spent his reign carefully rebuilding the royal treasury.',
     "hn": 'He was famously thrifty, personally reviewing and initialing royal account books to keep tabs on spending.'},

    {"n": 'Henry VIII', "dy": 'House of Tudor', "rs": 1509, "re": 1547, "ni": None,
     "fa": 'Married six times and broke England away from the Catholic Church after the Pope refused to annul his first marriage, creating the Church of England.',
     "hn": 'Two of his wives were beheaded, one died after childbirth, two marriages were annulled, and the last wife outlived him, a sequence English schoolchildren still memorize as divorced, beheaded, died, divorced, beheaded, survived.'},

    {"n": 'Edward VI', "dy": 'House of Tudor', "rs": 1547, "re": 1553, "ni": None,
     "fa": 'Became king at just nine years old and pushed England further toward Protestantism during his short reign before dying of illness at 15.',
     "hn": None},

    {"n": 'Jane Grey', "dy": 'House of Tudor', "rs": 1553, "re": 1553, "ni": 'The Nine Days Queen',
     "fa": 'Was proclaimed queen as part of a failed plot to keep the throne Protestant and away from her Catholic cousin Mary, only to be deposed just nine days later.',
     "hn": "She was beheaded the following year at just 16 or 17 years old after her father's involvement in a separate rebellion made her too dangerous to keep alive."},

    {"n": 'Mary I', "dy": 'House of Tudor', "rs": 1553, "re": 1558, "ni": 'Bloody Mary',
     "fa": "England's first undisputed queen regnant, she tried to reverse the country's break from Catholicism and had roughly 280 Protestant dissenters burned at the stake during her reign.",
     "hn": None},

    {"n": 'Elizabeth I', "dy": 'House of Tudor', "rs": 1558, "re": 1603, "ni": 'The Virgin Queen',
     "fa": 'Never married, in part to preserve her independence as a ruler, and presided over a golden age of English exploration and literature along with the defeat of the Spanish Armada in 1588.',
     "hn": 'Her refusal to name an heir for most of her reign left England in genuine uncertainty about the succession right up until her death.'},

    {"n": 'James I', "dy": 'House of Stuart', "rs": 1603, "re": 1625, "ni": None,
     "fa": 'Already King of Scotland, he inherited the English throne too and united the two crowns under one monarch for the first time, and commissioned the King James Bible translation still read today.',
     "hn": None},

    {"n": 'Charles I', "dy": 'House of Stuart', "rs": 1625, "re": 1649, "ni": None,
     "fa": 'His conflicts with Parliament over money and religion triggered the English Civil War; he was tried for treason and became the only English monarch ever executed.',
     "hn": "He was beheaded on a scaffold built outside his own Banqueting House in London, reportedly wearing two shirts so the cold wouldn't make him shiver and look afraid."},

    {"n": 'Charles II', "dy": 'House of Stuart', "rs": 1660, "re": 1685, "ni": None,
     "fa": 'Restored the monarchy after eleven years of republican rule under Oliver Cromwell, and reigned through both the Great Plague of London and the Great Fire of 1666.',
     "hn": 'He fathered at least a dozen acknowledged illegitimate children but no legitimate heir, which eventually passed the throne to his brother.'},

    {"n": 'James II', "dy": 'House of Stuart', "rs": 1685, "re": 1688, "ni": None,
     "fa": 'His open Catholicism and authoritarian style alarmed Parliament so badly that he was deposed within three years in what became known as the Glorious Revolution.',
     "hn": None},

    {"n": 'William III and Mary II', "dy": 'House of Orange-Stuart', "rs": 1689, "re": 1702, "ni": None,
     "fa": "Invited to take the throne jointly after James II's overthrow, they accepted a Bill of Rights that permanently limited royal power in favor of Parliament.",
     "hn": 'Mary died of smallpox in 1694, after which William continued to reign alone until his own death in 1702.'},

    {"n": 'Anne', "dy": 'House of Stuart', "rs": 1702, "re": 1714, "ni": None,
     "fa": 'The last Stuart monarch, she oversaw the 1707 Act of Union that formally merged the kingdoms of England and Scotland into a single Kingdom of Great Britain.',
     "hn": 'She endured at least seventeen pregnancies without a single child surviving her, leaving the throne to pass to a distant German relative after her death.'},

    {"n": 'George I', "dy": 'House of Hanover', "rs": 1714, "re": 1727, "ni": None,
     "fa": 'A German prince invited to the throne as the nearest Protestant relative of the childless Queen Anne, he spoke little English and relied heavily on his ministers to govern.',
     "hn": None},

    {"n": 'George II', "dy": 'House of Hanover', "rs": 1727, "re": 1760, "ni": None,
     "fa": 'Remains the last British monarch to personally lead troops into battle, commanding his army at the Battle of Dettingen in 1743.',
     "hn": None},

    {"n": 'George III', "dy": 'House of Hanover', "rs": 1760, "re": 1820, "ni": None,
     "fa": 'Reigned during the loss of the American colonies in the Revolutionary War and suffered recurring bouts of severe mental illness later in life, long attributed to the blood disorder porphyria though the diagnosis remains disputed.',
     "hn": 'During one episode he reportedly tried to shake hands with a tree, mistaking it for the King of Prussia.'},

    {"n": 'George IV', "dy": 'House of Hanover', "rs": 1820, "re": 1830, "ni": None,
     "fa": 'Ruled as Prince Regent for nearly a decade while his father was incapacitated before finally becoming king himself, known for his extravagant taste and the flamboyant Royal Pavilion he built in Brighton.',
     "hn": None},

    {"n": 'William IV', "dy": 'House of Hanover', "rs": 1830, "re": 1837, "ni": 'The Sailor King',
     "fa": 'Spent years as a young man serving as a working naval officer before becoming king relatively late in life, and oversaw the Reform Act of 1832 that expanded voting rights.',
     "hn": 'He had ten children with longtime partner Dorothea Jordan, none of whom could inherit the throne since the couple never married.'},

    {"n": 'Victoria', "dy": 'House of Hanover', "rs": 1837, "re": 1901, "ni": None,
     "fa": 'Reigned for 63 years, the longest of any British monarch until Elizabeth II surpassed her, presiding over the British Empire at its territorial height and giving her name to an entire era.',
     "hn": 'She married her first cousin Prince Albert and wore black in mourning for him for the remaining 40 years of her life after his death.'},

    {"n": 'Edward VII', "dy": 'House of Saxe-Coburg and Gotha', "rs": 1901, "re": 1910, "ni": None,
     "fa": 'Waited almost 60 years as Prince of Wales, the longest wait for the throne in British history up to that point, before finally becoming king at 59.',
     "hn": None},

    {"n": 'George V', "dy": 'House of Windsor', "rs": 1910, "re": 1936, "ni": None,
     "fa": "Reigned through the First World War and changed his family's name from the German-sounding Saxe-Coburg and Gotha to the thoroughly English Windsor in 1917 amid wartime anti-German sentiment.",
     "hn": None},

    {"n": 'Edward VIII', "dy": 'House of Windsor', "rs": 1936, "re": 1936, "ni": None,
     "fa": 'Reigned for less than a year before voluntarily abdicating to marry the twice-divorced American Wallis Simpson, becoming the only British monarch ever to give up the throne by choice.',
     "hn": None},

    {"n": 'George VI', "dy": 'House of Windsor', "rs": 1936, "re": 1952, "ni": None,
     "fa": "Took the throne reluctantly after his brother's abdication and led the country through the Second World War despite a severe stammer he worked for years to overcome.",
     "hn": None},

    {"n": 'Elizabeth II', "dy": 'House of Windsor', "rs": 1952, "re": 2022, "ni": None,
     "fa": "Became Britain's longest-reigning monarch, serving for 70 years through fifteen prime ministers, from Winston Churchill to Liz Truss, and the transformation of the British Empire into the Commonwealth.",
     "hn": "She acceded to the throne while on a visit to Kenya, learning of her father's death from a newspaper reporter rather than official channels."},

    {"n": 'Charles III', "dy": 'House of Windsor', "rs": 2022, "re": None, "ni": None,
     "fa": 'Became king at 73, the oldest person ever to accede to the British throne, after waiting longer as heir apparent than any previous Prince of Wales in history.',
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

    out = Path("assets/history/british_monarchy.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(records, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    sys.stdout.buffer.write((chr(10) + f"Done: {found}/{total} images found -- {total} monarchs total." + chr(10)).encode("utf-8"))


if __name__ == "__main__":
    main()
