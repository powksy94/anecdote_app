import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote
sys.stdout.reconfigure(encoding="utf-8")

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_EN = {
    "Ares": "Ares",
    "Iris": "Iris (mythology)",
    "Hebe": "Hebe (mythology)",
    "Circe": "Circe",
    "Echo": "Echo (mythology)",
    "Atlas": "Atlas (mythology)",
    "Chaos": "Chaos (cosmogony)",
    "Nike": "Nike (mythology)",
}

# n=name, dom=domain/role, sym=symbol, fa=fact
figures = [
    {"n":"Zeus","dom":"King of the gods, god of sky and thunder (Roman: Jupiter)","sym":"Thunderbolt, eagle, oak tree","fa":"Overthrew his father Cronus to become ruler of Mount Olympus"},
    {"n":"Hera","dom":"Queen of the gods, goddess of marriage (Roman: Juno)","sym":"Peacock, cow, pomegranate","fa":"Zeus's wife and sister, often depicted punishing his many lovers and children"},
    {"n":"Poseidon","dom":"God of the sea, earthquakes and horses (Roman: Neptune)","sym":"Trident, horse, dolphin","fa":"Could cause earthquakes by striking the ground with his trident"},
    {"n":"Hades","dom":"God of the underworld and the dead (Roman: Pluto)","sym":"Bident, cerberus, key","fa":"Ruled the underworld but rarely left it, making him one of the least depicted major gods"},
    {"n":"Demeter","dom":"Goddess of the harvest and agriculture (Roman: Ceres)","sym":"Wheat, cornucopia, torch","fa":"Her grief over her daughter Persephone's abduction was said to cause winter"},
    {"n":"Athena","dom":"Goddess of wisdom and strategic warfare (Roman: Minerva)","sym":"Owl, olive tree, aegis shield","fa":"Born fully grown and armored from Zeus's forehead"},
    {"n":"Apollo","dom":"God of music, prophecy, archery and the sun","sym":"Lyre, bow, laurel wreath","fa":"One of the few Olympians to keep the same name in both Greek and Roman mythology"},
    {"n":"Artemis","dom":"Goddess of the hunt and the moon (Roman: Diana)","sym":"Bow and arrow, stag, moon","fa":"Twin sister of Apollo, sworn to eternal virginity and protector of wild animals"},
    {"n":"Ares","dom":"God of war (Roman: Mars)","sym":"Spear, helmet, dog","fa":"Unlike the more strategic Athena, Ares embodied the brutal, chaotic aspects of war"},
    {"n":"Aphrodite","dom":"Goddess of love and beauty (Roman: Venus)","sym":"Dove, rose, seashell","fa":"Said to have been born from sea foam near the island of Cyprus"},
    {"n":"Hephaestus","dom":"God of fire and the forge (Roman: Vulcan)","sym":"Hammer, anvil, forge","fa":"The blacksmith of the gods, said to have crafted Zeus's thunderbolts"},
    {"n":"Hermes","dom":"Messenger god, god of trade and travelers (Roman: Mercury)","sym":"Winged sandals, caduceus staff","fa":"Known for his speed, he guided souls to the underworld as well as delivering messages"},
    {"n":"Dionysus","dom":"God of wine, festivity and theater (Roman: Bacchus)","sym":"Grapevine, thyrsus staff, panther","fa":"The only Olympian said to have had a mortal mother"},
    {"n":"Hestia","dom":"Goddess of the hearth and home (Roman: Vesta)","sym":"Hearth fire, kettle","fa":"Gave up her seat among the twelve Olympians to Dionysus, preferring a quiet domestic role"},
    {"n":"Persephone","dom":"Queen of the underworld, goddess of spring (Roman: Proserpina)","sym":"Pomegranate, sheaf of grain","fa":"Her yearly return from the underworld was said to bring about spring"},
    {"n":"Eros","dom":"God of love and desire (Roman: Cupid)","sym":"Bow and arrow, wings","fa":"His arrows were said to make anyone struck by them fall instantly in love"},
    {"n":"Nike","dom":"Goddess of victory","sym":"Wings, laurel wreath, palm branch","fa":"Often shown as a winged figure crowning victors, later inspiring the sportswear brand's name"},
    {"n":"Iris","dom":"Goddess of the rainbow and messenger of the gods","sym":"Rainbow, winged sandals","fa":"Served as a messenger for Hera in particular, traveling along rainbows"},
    {"n":"Hypnos","dom":"God of sleep (Roman: Somnus)","sym":"Poppy flower, horn of sleep-inducing liquid","fa":"Twin brother of Thanatos, the god of death"},
    {"n":"Thanatos","dom":"God of death","sym":"Inverted torch, butterfly","fa":"Personified peaceful death, unlike the violent death goddesses called the Keres"},
    {"n":"Nemesis","dom":"Goddess of retribution and revenge","sym":"Scale, whip, sword","fa":"Punished those who succumbed to hubris, or excessive pride against the gods"},
    {"n":"Tyche","dom":"Goddess of fortune and chance (Roman: Fortuna)","sym":"Wheel of fortune, cornucopia","fa":"Her favor was believed to be entirely unpredictable and could shift a city's fate overnight"},
    {"n":"Pan","dom":"God of the wild, shepherds and rustic music (Roman: Faunus)","sym":"Pan flute, goat legs and horns","fa":"His sudden appearance was said to cause sudden, irrational fear, giving us the word 'panic'"},
    {"n":"Hecate","dom":"Goddess of magic, crossroads and witchcraft","sym":"Twin torches, keys, dogs","fa":"Associated with the night and often depicted with three faces looking in different directions"},
    {"n":"Gaia","dom":"Primordial goddess and personification of the Earth","sym":"Earth, fruit, cornucopia","fa":"Considered the mother of the Titans and, through them, the ancestor of nearly all Greek gods"},
    {"n":"Uranus","dom":"Primordial god and personification of the sky","sym":"Starry sky","fa":"Was overthrown and castrated by his son Cronus in one of Greek mythology's most violent myths"},
    {"n":"Cronus","dom":"King of the Titans, god of time and the harvest (Roman: Saturn)","sym":"Scythe","fa":"Swallowed his own children to prevent a prophecy that one would overthrow him, but was outwitted by Zeus"},
    {"n":"Rhea","dom":"Titan goddess of fertility, mother of the Olympians","sym":"Lions, drum","fa":"Tricked Cronus by giving him a stone wrapped in cloth to swallow instead of the infant Zeus"},
    {"n":"Prometheus","dom":"Titan associated with fire and forethought","sym":"Fire, torch","fa":"Stole fire from the gods to give to humanity and was punished with eternal torment as a result"},
    {"n":"Atlas","dom":"Titan condemned to hold up the sky","sym":"Globe, celestial sphere","fa":"Punished after the Titans' war against the Olympians to bear the heavens on his shoulders forever"},
    {"n":"Helios","dom":"Titan god of the sun (Roman: Sol)","sym":"Sun chariot, radiant crown","fa":"Believed to drive a golden chariot pulling the sun across the sky each day"},
    {"n":"Selene","dom":"Titan goddess of the moon (Roman: Luna)","sym":"Crescent moon, chariot","fa":"Fell in love with the mortal Endymion, who was granted eternal sleep so she could visit him forever"},
    {"n":"Eos","dom":"Titan goddess of the dawn (Roman: Aurora)","sym":"Rosy fingers, chariot","fa":"Said to open the gates of heaven each morning to let Helios's sun chariot through"},
    {"n":"Asclepius","dom":"God of medicine and healing","sym":"Rod with a serpent coiled around it","fa":"His symbol, the Rod of Asclepius, is still used today as a medical emblem"},
    {"n":"Triton","dom":"Messenger god of the sea, son of Poseidon","sym":"Conch shell trumpet","fa":"Could calm or stir up the seas by blowing into his conch shell"},
    {"n":"Nyx","dom":"Primordial goddess and personification of night","sym":"Dark veil, chariot of black horses","fa":"One of the very first beings to exist according to Greek cosmogony, even feared by Zeus"},
    {"n":"Chaos","dom":"Primordial void from which all creation began","sym":"The void","fa":"Not a god but a formless state of nothingness that existed before the universe took shape"},
    {"n":"Heracles","dom":"Hero famed for superhuman strength (Roman: Hercules)","sym":"Lion skin, club","fa":"Completed twelve immense labors as penance, including slaying the Nemean Lion"},
    {"n":"Achilles","dom":"Hero of the Trojan War","sym":"Spear, shield","fa":"Was said to be invulnerable except for his heel, giving us the phrase 'Achilles' heel'"},
    {"n":"Odysseus","dom":"Hero and king of Ithaca (Roman: Ulysses)","sym":"Bow, ship","fa":"His ten-year journey home from the Trojan War inspired Homer's epic 'The Odyssey'"},
    {"n":"Perseus","dom":"Hero who slew the gorgon Medusa","sym":"Winged sandals, shield, sword","fa":"Used a reflective shield to safely behead Medusa without meeting her petrifying gaze"},
    {"n":"Theseus","dom":"Hero and legendary king of Athens","sym":"Sword, ball of thread","fa":"Defeated the Minotaur in the labyrinth of Crete with the help of a thread given by Ariadne"},
    {"n":"Jason","dom":"Hero who led the quest for the Golden Fleece","sym":"Golden Fleece, ship Argo","fa":"Led a crew of heroes known as the Argonauts on his famous quest"},
    {"n":"Orpheus","dom":"Legendary musician and poet","sym":"Lyre","fa":"Journeyed into the underworld to retrieve his wife Eurydice, but lost her by looking back too soon"},
    {"n":"Oedipus","dom":"Tragic king of Thebes","sym":"Crown, riddle of the Sphinx","fa":"Unknowingly fulfilled a prophecy of killing his father and marrying his mother"},
    {"n":"Aeneas","dom":"Trojan hero, legendary ancestor of the Romans","sym":"Sword, shield","fa":"His journey from fallen Troy to found the Roman people is told in Virgil's epic 'The Aeneid'"},
    {"n":"Bellerophon","dom":"Hero who tamed the winged horse Pegasus","sym":"Pegasus, golden bridle","fa":"Used Pegasus to defeat the monstrous Chimera"},
    {"n":"Atalanta","dom":"Heroine known for her speed as a huntress","sym":"Bow, running sandals","fa":"Vowed only to marry a man who could outrun her in a footrace"},
    {"n":"Icarus","dom":"Figure known for his flight and fall","sym":"Wax wings","fa":"Ignored his father Daedalus's warning and flew too close to the sun, melting his wings"},
    {"n":"Daedalus","dom":"Legendary inventor and craftsman","sym":"Wings, labyrinth","fa":"Built the labyrinth of Crete that housed the Minotaur, and later designed wings to escape it"},
    {"n":"Sisyphus","dom":"Figure condemned to eternal futile labor","sym":"Boulder","fa":"Punished by the gods to forever push a boulder up a hill, only for it to roll back down each time"},
    {"n":"Tantalus","dom":"Figure condemned to eternal, unreachable temptation","sym":"Fruit tree, water","fa":"Punished with food and water forever just out of reach, giving us the word 'tantalize'"},
    {"n":"Pandora","dom":"The first mortal woman in Greek mythology","sym":"Jar (often mistranslated as 'box')","fa":"Opened a forbidden jar releasing all evils into the world, leaving only hope trapped inside"},
    {"n":"Narcissus","dom":"Figure known for his beauty and self-obsession","sym":"Pool of water, narcissus flower","fa":"Fell in love with his own reflection and wasted away, giving us the word 'narcissism'"},
    {"n":"Echo","dom":"Mountain nymph cursed to only repeat others' words","sym":"Echo, voice","fa":"Cursed by Hera and later faded away from unrequited love for Narcissus, leaving only her voice"},
    {"n":"Pygmalion","dom":"Legendary sculptor","sym":"Ivory statue","fa":"Fell in love with a statue he carved, which the goddess Aphrodite brought to life"},
    {"n":"Midas","dom":"Legendary king granted a golden touch","sym":"Gold, donkey ears","fa":"Granted a wish that turned everything he touched to gold, which nearly caused him to starve"},
    {"n":"Arachne","dom":"Mortal weaver transformed into the first spider","sym":"Loom, spider web","fa":"Challenged Athena to a weaving contest and was transformed into a spider as punishment for her pride"},
    {"n":"Medusa","dom":"Gorgon whose gaze turned onlookers to stone","sym":"Snake hair, stone gaze","fa":"Was once a mortal woman before being transformed into a monster by Athena"},
    {"n":"Helen of Troy","dom":"Legendary figure whose abduction sparked the Trojan War","sym":"Beauty","fa":"Called 'the face that launched a thousand ships' due to the war fought over her"},
    {"n":"Cassandra","dom":"Trojan princess cursed with true but disbelieved prophecies","sym":"Prophecy, laurel","fa":"Cursed by Apollo so that no one would ever believe her accurate predictions"},
    {"n":"Ariadne","dom":"Princess who helped Theseus escape the labyrinth","sym":"Thread","fa":"Gave Theseus a ball of thread to navigate the labyrinth and later became Dionysus's wife"},
    {"n":"Circe","dom":"Sorceress skilled in potions and transformation","sym":"Wand, potion cup","fa":"Turned Odysseus's crew into pigs in Homer's 'The Odyssey'"},
    {"n":"Penelope","dom":"Wife of Odysseus, known for her loyalty","sym":"Weaving loom","fa":"Delayed remarriage for years by secretly unweaving a burial shroud she claimed to be finishing"},
    {"n":"Andromeda","dom":"Princess rescued by the hero Perseus","sym":"Chains, sea monster","fa":"Was chained to a rock as a sacrifice to a sea monster before being saved by Perseus"},
    {"n":"Europa","dom":"Princess associated with the origin of the continent's name","sym":"White bull","fa":"Was carried away by Zeus disguised as a bull, and the continent of Europe is said to be named after her"},
    {"n":"Ganymede","dom":"Trojan prince taken to serve as cupbearer to the gods","sym":"Eagle, cup","fa":"Was abducted by Zeus in the form of an eagle to become the gods' cupbearer on Olympus"},
    {"n":"Chiron","dom":"Wise centaur, teacher of many Greek heroes","sym":"Bow, medicinal herbs","fa":"Unlike most centaurs, he was known for wisdom and kindness, and tutored Achilles and Jason"},
    {"n":"Amphitrite","dom":"Goddess of the sea, wife of Poseidon","sym":"Trident, dolphin","fa":"Ruled the sea alongside Poseidon and was often depicted riding a dolphin or sea creature"},
    {"n":"Morpheus","dom":"God of dreams, son of Hypnos","sym":"Wings, poppy flowers","fa":"Could take on any human form in people's dreams, giving us the word 'morph'"},
    {"n":"Eris","dom":"Goddess of strife and discord","sym":"Golden apple","fa":"Threw a golden apple inscribed 'for the fairest' among the goddesses, indirectly sparking the Trojan War"},
    {"n":"Momus","dom":"God of satire, mockery and complaint","sym":"Mask, jester's staff","fa":"Was eventually expelled from Olympus for endlessly criticizing the other gods"},
    {"n":"Janus","dom":"Roman god of beginnings, transitions and doorways","sym":"Two faces looking opposite ways","fa":"Had no Greek equivalent and gave his name to the month of January"},
    {"n":"Terminus","dom":"Roman god of boundaries and landmarks","sym":"Boundary stone","fa":"Worshipped as the protector of property lines, with stone markers placed in his honor"},
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
    out = Path("assets/mythology/greek_mythology.json")
    out.write_text(json.dumps(figures, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    summary = "\nDone: {}/{} images -- {} figures total.\n".format(found, total, total)
    sys.stdout.buffer.write(summary.encode("utf-8"))

if __name__ == "__main__":
    main()
