import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote
sys.stdout.reconfigure(encoding="utf-8")

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_EN = {
    "Mut": "Mut",
    "Bes": "Bes",
    "Min": "Min (god)",
    "Nut": "Nut (goddess)",
}

# n=name, dom=domain/role, sym=symbol, fa=fact
figures = [
    {"n":"Ra","dom":"God of the sun and creation","sym":"Sun disk, falcon head","fa":"Believed to travel across the sky by day and through the underworld by night in a solar barque"},
    {"n":"Osiris","dom":"God of the afterlife, resurrection and fertility","sym":"Crook and flail, green skin","fa":"Murdered by his brother Set and later resurrected by Isis, becoming ruler of the underworld"},
    {"n":"Isis","dom":"Goddess of magic, healing and motherhood","sym":"Throne headdress, wings","fa":"Reassembled her husband Osiris's body after his murder using powerful magic"},
    {"n":"Horus","dom":"God of the sky and kingship","sym":"Falcon, Eye of Horus","fa":"Egyptian pharaohs were believed to be his living embodiment on Earth"},
    {"n":"Set","dom":"God of chaos, storms and the desert","sym":"Was animal, was-scepter","fa":"Murdered his brother Osiris out of jealousy, becoming a symbol of chaos and disorder"},
    {"n":"Anubis","dom":"God of mummification and the afterlife","sym":"Jackal head, embalming tools","fa":"Believed to guide the weighing of souls' hearts against the feather of truth"},
    {"n":"Thoth","dom":"God of wisdom, writing and the moon","sym":"Ibis head, writing palette","fa":"Credited with inventing writing and serving as scribe of the gods"},
    {"n":"Hathor","dom":"Goddess of love, joy and motherhood","sym":"Cow horns with sun disk","fa":"Worshipped as a protector of women and often depicted nursing the pharaoh"},
    {"n":"Sekhmet","dom":"Lioness goddess of war and healing","sym":"Lioness head, sun disk","fa":"Said to have once nearly destroyed humanity in a fit of rage before being tricked into stopping"},
    {"n":"Bastet","dom":"Cat goddess of protection and the home","sym":"Cat, sistrum rattle","fa":"Cats were considered sacred in Egypt largely due to her association with them"},
    {"n":"Ptah","dom":"Creator god and patron of craftsmen","sym":"Was-scepter, mummiform body","fa":"Believed by some Egyptian traditions to have created the world simply by speaking it into existence"},
    {"n":"Amun","dom":"King of the gods, later merged with Ra as Amun-Ra","sym":"Twin plumed crown, ram","fa":"Rose from a local Theban god to become the chief deity of the Egyptian pantheon"},
    {"n":"Nut","dom":"Goddess of the sky","sym":"Star-covered body arched over the earth","fa":"Depicted as a star-covered woman arching over the earth god Geb, swallowing the sun each evening"},
    {"n":"Geb","dom":"God of the earth","sym":"Goose, green or black skin","fa":"Believed his laughter caused earthquakes"},
    {"n":"Shu","dom":"God of air and light","sym":"Ostrich feather","fa":"Believed to hold up the sky goddess Nut, separating her from the earth god Geb"},
    {"n":"Tefnut","dom":"Goddess of moisture and rain","sym":"Lioness head","fa":"Twin sister of Shu, together representing the earliest pair of gods created by Atum"},
    {"n":"Nephthys","dom":"Goddess of mourning and protection of the dead","sym":"House hieroglyph headdress","fa":"Helped her sister Isis search for and mourn the body of the slain Osiris"},
    {"n":"Sobek","dom":"Crocodile god of the Nile and fertility","sym":"Crocodile head","fa":"Worshipped near the Nile as a protector against crocodile attacks, ironically embodied by one"},
    {"n":"Khnum","dom":"Ram-headed god of creation","sym":"Potter's wheel, ram head","fa":"Believed to have molded humans and their souls out of clay on a potter's wheel"},
    {"n":"Maat","dom":"Goddess of truth, justice and cosmic order","sym":"Ostrich feather","fa":"A person's heart was weighed against her feather after death to judge their worthiness"},
    {"n":"Nefertem","dom":"God of the lotus flower, beauty and healing","sym":"Lotus flower crown","fa":"Believed to have emerged from a lotus blossom at the dawn of creation"},
    {"n":"Bes","dom":"Dwarf god protector of households and childbirth","sym":"Dwarf figure, lion mane","fa":"Unlike most Egyptian gods, he was usually shown facing forward rather than in profile"},
    {"n":"Taweret","dom":"Hippopotamus goddess protector of childbirth","sym":"Upright hippopotamus","fa":"Combined features of a hippo, lion and crocodile to ward off evil during pregnancy"},
    {"n":"Wadjet","dom":"Cobra goddess protector of Lower Egypt","sym":"Rearing cobra","fa":"Depicted on the pharaoh's crown as a protective cobra ready to strike enemies"},
    {"n":"Nekhbet","dom":"Vulture goddess protector of Upper Egypt","sym":"Vulture","fa":"Paired with Wadjet to symbolize the unification of Upper and Lower Egypt"},
    {"n":"Serqet","dom":"Scorpion goddess of protection and healing","sym":"Scorpion","fa":"Believed to protect against venomous stings and bites despite her scorpion form"},
    {"n":"Neith","dom":"Goddess of war, hunting and weaving","sym":"Bow and arrows, weaving shuttle","fa":"One of the oldest deities in the Egyptian pantheon, sometimes credited as a creator goddess"},
    {"n":"Mut","dom":"Mother goddess, wife of Amun","sym":"Vulture headdress, double crown","fa":"Her name means 'mother' in ancient Egyptian, reflecting her maternal role in the pantheon"},
    {"n":"Khonsu","dom":"God of the moon","sym":"Moon disk and crescent","fa":"Believed to govern time and the passing of months through the lunar cycle"},
    {"n":"Aten","dom":"God of the sun disk","sym":"Solar disk with rays ending in hands","fa":"Elevated by Pharaoh Akhenaten as the sole god in one of history's earliest monotheistic movements"},
    {"n":"Apophis","dom":"Serpent deity of chaos and darkness","sym":"Giant serpent","fa":"Believed to attack the sun god Ra's boat every night, requiring the other gods to fend him off"},
    {"n":"Atum","dom":"Primordial creator god","sym":"Double crown, setting sun","fa":"Believed to have created the first gods by either spitting or masturbating them into existence"},
    {"n":"Nun","dom":"Personification of the primordial waters of chaos","sym":"Endless dark water","fa":"Represented the formless waters that existed before creation, from which Atum emerged"},
    {"n":"Heka","dom":"God of magic and medicine","sym":"Two entwined serpents","fa":"Personified the very concept of magic itself, believed to predate the gods"},
    {"n":"Renenutet","dom":"Cobra goddess of the harvest and nourishment","sym":"Cobra, sheaf of grain","fa":"Worshipped at harvest time to ensure a plentiful and safe grain supply"},
    {"n":"Sopdu","dom":"Falcon god of war guarding the eastern frontier","sym":"Falcon, was-scepter","fa":"Served as a protector deity guarding Egypt's eastern border against invaders"},
    {"n":"Min","dom":"God of fertility, the desert and male virility","sym":"Raised arm holding a flail","fa":"One of the oldest Egyptian gods, worshipped since predynastic times"},
    {"n":"Seshat","dom":"Goddess of writing, measurement and record-keeping","sym":"Seven-pointed star headdress","fa":"Credited with recording the reigns of pharaohs and measuring the foundations of temples"},
    {"n":"Anhur","dom":"God of war and hunting","sym":"Spear, plumed headdress","fa":"His name means 'sky-bearer', reflecting his role as a warrior who upholds cosmic order"},
    {"n":"Wepwawet","dom":"Jackal god known as the 'opener of ways'","sym":"Jackal, mace and bow","fa":"Believed to lead the pharaoh and the dead safely on their journeys"},
    {"n":"Hapi","dom":"God of the annual Nile flood","sym":"Papyrus and lotus, blue or green skin","fa":"Worshipped for bringing the fertile floodwaters that sustained Egyptian agriculture"},
    {"n":"Meretseger","dom":"Cobra goddess protector of the Valley of the Kings","sym":"Cobra, mountain peak","fa":"Believed to punish tomb robbers with snake bites or blindness"},
    {"n":"Ammit","dom":"Devourer of the unworthy dead","sym":"Crocodile head, lion body, hippo legs","fa":"Waited beside the scales of judgment to devour the hearts of those found unworthy"},
    {"n":"Imsety","dom":"One of the Four Sons of Horus, protector of the liver","sym":"Human head, canopic jar","fa":"Guarded the liver of the deceased under the protection of the goddess Isis"},
    {"n":"Hapy (Son of Horus)","dom":"One of the Four Sons of Horus, protector of the lungs","sym":"Baboon head, canopic jar","fa":"Guarded the lungs of the deceased under the protection of the goddess Nephthys"},
    {"n":"Duamutef","dom":"One of the Four Sons of Horus, protector of the stomach","sym":"Jackal head, canopic jar","fa":"Guarded the stomach of the deceased under the protection of the goddess Neith"},
    {"n":"Qebehsenuef","dom":"One of the Four Sons of Horus, protector of the intestines","sym":"Falcon head, canopic jar","fa":"Guarded the intestines of the deceased under the protection of the goddess Serqet"},
    {"n":"Duat","dom":"The underworld realm of the dead","sym":"Twelve gates, dark river","fa":"Believed to be divided into twelve regions the sun god Ra passed through each night"},
    {"n":"Shai","dom":"God personifying fate and destiny","sym":"Shepherd's crook","fa":"Believed to determine the length and course of a person's life at their birth"},
    {"n":"Meskhenet","dom":"Goddess of childbirth and destiny","sym":"Birthing bricks","fa":"Believed to be present at every birth to help determine the child's fate"},
    {"n":"Sia","dom":"Personification of perception and understanding","sym":"Papyrus scroll","fa":"Often paired with Hu (authority) as companions who accompanied Ra"},
    {"n":"Hu","dom":"Personification of authoritative, creative speech","sym":"Royal scepter","fa":"Represented the divine utterance believed to have brought creation into being"},
    {"n":"Satis","dom":"Goddess of the Nile's cataracts and fertility","sym":"White crown with antelope horns","fa":"Believed to guard Egypt's southern border and purify the pharaoh with Nile water"},
    {"n":"Anuket","dom":"Goddess of the Nile River and its cataracts","sym":"Feathered crown, gazelle","fa":"Worshipped especially in the region around the Nile's first cataract"},
    {"n":"Sokar","dom":"Falcon-headed god of the necropolis","sym":"Falcon head, mummiform body","fa":"Closely associated with craftsmen and the funerary practices of the Memphis region"},
    {"n":"Wadj-wer","dom":"Personification of the Mediterranean Sea or great marshes","sym":"Water, fertility","fa":"Represented the fertile marshlands and sea that bordered ancient Egypt"},
    {"n":"Serapis","dom":"Syncretic god combining Osiris and the Apis bull","sym":"Grain basket crown","fa":"Deliberately created under the Ptolemaic dynasty to blend Egyptian and Greek religious traditions"},
    {"n":"Apis","dom":"Sacred bull deity linked to Ptah and later Osiris","sym":"Black and white bull","fa":"A living bull was selected by priests and worshipped as a physical incarnation of the god"},
    {"n":"Bata","dom":"Bull-associated god from Middle Egyptian mythology","sym":"Bull","fa":"Central figure in the ancient 'Tale of Two Brothers', an early example of Egyptian mythological storytelling"},
    {"n":"Nefertum","dom":"Alternate rendering of the god of the lotus and healing","sym":"Lotus blossom","fa":"Sometimes depicted as a young child seated on a lotus flower"},
    {"n":"Pakhet","dom":"Lioness goddess of the desert margins","sym":"Lioness head, claws","fa":"Worshipped as a fierce huntress goddess in the region of Beni Hasan"},
    {"n":"Menhit","dom":"Lioness warrior goddess","sym":"Lioness head, sun disk","fa":"Her name means 'she who massacres', reflecting her role as a war deity"},
    {"n":"Iah","dom":"Early god personifying the moon","sym":"Moon disk and crescent","fa":"An older lunar deity later largely absorbed into the worship of Khonsu and Thoth"},
    {"n":"Nehebkau","dom":"Serpent god associated with protection and the afterlife","sym":"Serpent, ka symbol","fa":"Believed to bind together a person's spiritual forces after death"},
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
    total = len(figures)
    found = 0
    for i, s in enumerate(figures):
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
    out = Path("assets/mythology/egyptian_mythology.json")
    out.write_text(json.dumps(figures, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    summary = "\nDone: {}/{} images -- {} figures total.\n".format(found, total, total)
    sys.stdout.buffer.write(summary.encode("utf-8"))

if __name__ == "__main__":
    main()
