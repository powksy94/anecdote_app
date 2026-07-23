import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote
sys.stdout.reconfigure(encoding="utf-8")

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_EN = {
    "Naga": "Naga",
    "Oni": "Oni",
    "Kappa": "Kappa (folklore)",
    "Djinn": "Jinn",
    "Roc": "Roc (mythology)",
    "Golem": "Golem",
    "Scylla": "Scylla",
}

# n=name, origin=culture/origin, fa=fact, df=defeated by / fate in myth
creatures = [
    {"n":"Cerberus","origin":"Greek mythology","fa":"A three-headed dog that guards the gates of the underworld, preventing the dead from leaving","df":"Briefly subdued (not killed) by Heracles during his twelfth labor, then returned to the underworld"},
    {"n":"Hydra","origin":"Greek mythology","fa":"A multi-headed serpent that grew two new heads for every one cut off, defeated by Heracles","df":"Slain by Heracles, who had his nephew Iolaus cauterize each neck stump to stop new heads regrowing"},
    {"n":"Chimera","origin":"Greek mythology","fa":"A fire-breathing creature combining the parts of a lion, goat and serpent","df":"Slain by the hero Bellerophon while riding the winged horse Pegasus"},
    {"n":"Pegasus","origin":"Greek mythology","fa":"A winged horse born from the blood of the slain gorgon Medusa","df":"Not an antagonist — served as Bellerophon's loyal mount rather than being defeated"},
    {"n":"Minotaur","origin":"Greek mythology","fa":"A half-man, half-bull creature imprisoned in a labyrinth on the island of Crete","df":"Slain by the hero Theseus, who found his way out of the labyrinth using Ariadne's thread"},
    {"n":"Sphinx (Greek)","origin":"Greek mythology","fa":"Posed a riddle to travelers near Thebes and devoured anyone who failed to answer correctly","df":"Killed herself in despair after Oedipus correctly solved her riddle"},
    {"n":"Cyclops","origin":"Greek mythology","fa":"A race of one-eyed giants, one of whom was blinded by Odysseus to escape his cave","df":"The cyclops Polyphemus was blinded by Odysseus and his men, who escaped clinging beneath his sheep"},
    {"n":"Centaur","origin":"Greek mythology","fa":"A creature with the upper body of a human and the lower body of a horse","df":"Many were killed by the Lapiths in the legendary battle known as the Centauromachy"},
    {"n":"Harpy","origin":"Greek mythology","fa":"A winged creature with a woman's face and a bird's body, associated with storm winds","df":"Driven away by Zetes and Calais, the winged sons of Boreas, during the voyage of the Argonauts"},
    {"n":"Gorgons","origin":"Greek mythology","fa":"A trio of monstrous sisters with snakes for hair, of whom Medusa was the only mortal one","df":"Medusa, the only mortal Gorgon, was beheaded by Perseus; her immortal sisters were never defeated"},
    {"n":"Satyr","origin":"Greek mythology","fa":"A woodland spirit with the legs of a goat, often depicted in the retinue of Dionysus","df":"Not an antagonist in Greek myth — a companion of Dionysus rather than a foe to be defeated"},
    {"n":"Nymph","origin":"Greek mythology","fa":"A nature spirit typically bound to a specific tree, river or mountain","df":"Not an antagonist — nymphs were nature spirits, not monsters to be defeated"},
    {"n":"Scylla","origin":"Greek mythology","fa":"A six-headed sea monster who preyed on sailors passing through a narrow strait, opposite Charybdis","df":"Never defeated in myth — Odysseus sacrificed six of his crew to her rather than confront her directly"},
    {"n":"Charybdis","origin":"Greek mythology","fa":"A monstrous whirlpool that swallowed the sea three times a day, giving rise to the phrase 'between Scylla and Charybdis'","df":"Never defeated — Odysseus survived only by steering his ship away from her and closer to Scylla"},
    {"n":"Fenrir","origin":"Norse mythology","fa":"A monstrous wolf destined to kill Odin during the events of Ragnarok","df":"Prophesied to kill Odin at Ragnarok before being slain in turn by Odin's son Vidar"},
    {"n":"Jormungandr","origin":"Norse mythology","fa":"A giant sea serpent so large it encircles the entire world, biting its own tail","df":"Prophesied to be killed by Thor at Ragnarok, though Thor also dies from the serpent's venom"},
    {"n":"Sleipnir","origin":"Norse mythology","fa":"Odin's eight-legged horse, said to be the fastest steed in all the nine worlds","df":"Not an antagonist — served faithfully as Odin's mount rather than being defeated"},
    {"n":"Garm","origin":"Norse mythology","fa":"A monstrous hound that guards the gates of the underworld realm of Hel","df":"Prophesied to kill and be killed by the god Tyr in single combat at Ragnarok"},
    {"n":"Nidhogg","origin":"Norse mythology","fa":"A dragon that gnaws eternally at the roots of the world tree Yggdrasil","df":"Never defeated in surviving Norse texts — said to continue gnawing at Yggdrasil's roots even after Ragnarok"},
    {"n":"Kraken","origin":"Scandinavian folklore","fa":"A gigantic sea monster said to be large enough to be mistaken for an island","df":"No fixed myth of defeat — a maritime legend meant to explain ships lost at sea"},
    {"n":"Draugr","origin":"Norse mythology","fa":"An undead creature said to guard its burial mound and treasures with supernatural strength","df":"Sagas describe heroes such as Grettir the Strong wrestling and beheading draugar to end their curse"},
    {"n":"Kitsune","origin":"Japanese folklore","fa":"A fox spirit believed to gain an additional tail for every hundred years it lives, up to nine","df":"Rarely 'defeated' — stories usually end with the fox spirit being outwitted or revealed rather than killed"},
    {"n":"Oni","origin":"Japanese folklore","fa":"A horned, ogre-like demon often depicted carrying a large iron club","df":"Famously defeated by the folk hero Momotaro (Peach Boy) and his animal companions"},
    {"n":"Kappa","origin":"Japanese folklore","fa":"A water-dwelling creature said to lure people into rivers, with a water-filled dish atop its head","df":"Traditionally beaten by tricking it into bowing, spilling the life-giving water from the dish on its head"},
    {"n":"Tengu","origin":"Japanese folklore","fa":"A bird-like spirit associated with mountains, often depicted with a long red nose","df":"Not typically an enemy to be defeated — often portrayed as a strict but fair teacher of warriors"},
    {"n":"Baku","origin":"Japanese folklore","fa":"A dream-eating spirit believed to devour the nightmares of sleeping people","df":"Benevolent by nature — not an antagonist in folklore"},
    {"n":"Qilin","origin":"Chinese mythology","fa":"A gentle hoofed creature said to appear only during times of great peace or the birth of a wise ruler","df":"Benevolent omen creature — never portrayed as a foe to be defeated"},
    {"n":"Chinese Dragon","origin":"Chinese mythology","fa":"Unlike Western dragons, typically seen as a benevolent symbol of power, strength and good fortune","df":"Generally benevolent in Chinese tradition — rarely an antagonist requiring defeat"},
    {"n":"Fenghuang","origin":"Chinese mythology","fa":"A mythical bird often compared to the Western phoenix, symbolizing harmony between yin and yang","df":"Benevolent symbolic bird — not portrayed as an enemy"},
    {"n":"Naga","origin":"Hindu and Buddhist mythology","fa":"A serpent deity often depicted as half-human, half-snake, guarding treasures and sacred sites","df":"The serpent Kaliya was subdued (not killed) by the young god Krishna, who danced upon its many heads"},
    {"n":"Garuda","origin":"Hindu mythology","fa":"A giant bird-like being and mount of the god Vishnu, enemy of serpents and nagas","df":"Not defeated — traditionally depicted as the natural predator and conqueror of nagas, not the other way around"},
    {"n":"Rakshasa","origin":"Hindu mythology","fa":"A shapeshifting demon known for disrupting religious rituals and preying on humans","df":"The demon king Ravana, greatest of the rakshasas, was slain by the god-prince Rama in the epic Ramayana"},
    {"n":"Apsara","origin":"Hindu and Buddhist mythology","fa":"A celestial female spirit known for beauty and skill in music and dance","df":"Benevolent celestial beings — not portrayed as adversaries"},
    {"n":"Yeti","origin":"Himalayan folklore","fa":"An ape-like creature said to roam the high snowy peaks of the Himalayas","df":"No myth of defeat — remains an unconfirmed cryptid said to still roam remote mountains today"},
    {"n":"Bunyip","origin":"Aboriginal Australian folklore","fa":"A creature said to lurk in swamps, billabongs and waterholes across Australia","df":"No myth of defeat — functions as a cautionary folklore figure warning people away from dangerous waters"},
    {"n":"Thunderbird","origin":"Native American folklore","fa":"A giant bird believed to create thunder with the beat of its wings and lightning from its eyes","df":"Generally a powerful benevolent or neutral spirit — not typically portrayed as defeated"},
    {"n":"Wendigo","origin":"Algonquian folklore","fa":"A malevolent, emaciated spirit associated with winter, famine and insatiable hunger","df":"Folklore describes it being destroyed by fire or by a shaman skilled enough to overpower its curse"},
    {"n":"Chupacabra","origin":"Latin American folklore","fa":"A creature blamed for mysterious livestock deaths, first reported in Puerto Rico in the 1990s","df":"No myth of defeat — a modern cryptid never definitively caught or confirmed"},
    {"n":"Anansi","origin":"West African (Akan) folklore","fa":"A clever spider trickster known for outwitting more powerful beings through cunning","df":"Almost always the victor in his own tales rather than a defeated antagonist"},
    {"n":"Djinn","origin":"Middle Eastern and Islamic folklore","fa":"A supernatural being made of smokeless fire, capable of good or evil and free will","df":"Traditionally bound or trapped by powerful magic, such as being sealed inside a lamp or bottle, rather than killed"},
    {"n":"Roc","origin":"Middle Eastern folklore","fa":"A giant bird of prey said to be large enough to carry off elephants, featured in the Sinbad tales","df":"Never defeated in the Sinbad tales — the sailor Sinbad escapes it rather than confronting it directly"},
    {"n":"Manticore","origin":"Persian folklore","fa":"A creature with the body of a lion, a human face and a tail that could fire venomous spines","df":"No single widely recorded myth of defeat has survived"},
    {"n":"Simurgh","origin":"Persian mythology","fa":"A benevolent, wise bird-like creature said to have lived long enough to see the world destroyed three times","df":"Benevolent guide figure in Persian epics — not portrayed as an enemy"},
    {"n":"Golem","origin":"Jewish folklore","fa":"A being formed from clay or mud and animated through mystical means to protect a community","df":"The Golem of Prague was deactivated by Rabbi Loew, who removed the sacred shem from its mouth"},
    {"n":"Leviathan","origin":"Biblical and Near Eastern mythology","fa":"A massive sea monster described in the Book of Job as an untamable force of chaos","df":"Jewish eschatology holds that Leviathan is destined to be slain by God at the end of days"},
    {"n":"Basilisk","origin":"European medieval folklore","fa":"A serpent king said to be capable of killing with a single glance or its venomous breath","df":"Said to be killed by a rooster's crow, or destroyed by being shown its own deadly reflection"},
    {"n":"Cockatrice","origin":"European medieval folklore","fa":"A dragon-like creature said to hatch from a rooster's egg incubated by a serpent or toad","df":"Folklore holds it could be killed by the crow of a rooster or the scent of a weasel"},
    {"n":"Wyvern","origin":"European medieval folklore","fa":"A two-legged, winged dragon variant common in medieval heraldry","df":"No single defeat myth — mainly a heraldic symbol rather than a creature in a specific narrative"},
    {"n":"Griffin","origin":"European and Near Eastern folklore","fa":"A creature with the body of a lion and the head and wings of an eagle, said to guard treasure","df":"Typically portrayed as a powerful guardian rather than a foe that gets defeated"},
    {"n":"Unicorn","origin":"European medieval folklore","fa":"A horse-like creature with a single horn, believed to be tamed only by a pure-hearted maiden","df":"Not killed in legend — traditionally only ever captured, and only by a virgin maiden"},
    {"n":"Phoenix","origin":"Greek and Egyptian mythology","fa":"A bird said to periodically burst into flame and be reborn from its own ashes","df":"Cannot be permanently defeated — it dies in flame only to be reborn from its own ashes"},
    {"n":"Mermaid","origin":"Found across many maritime cultures","fa":"A half-human, half-fish being appearing in the folklore of coastal cultures worldwide","df":"Not typically an antagonist — usually a figure to be encountered or fallen in love with, not defeated"},
    {"n":"Siren","origin":"Greek mythology","fa":"A creature whose enchanting song was said to lure sailors to shipwreck on rocky shores","df":"Odysseus survived them not by defeat but by having his crew's ears plugged and himself bound to the mast"},
    {"n":"Selkie","origin":"Scottish and Irish folklore","fa":"A seal that can shed its skin to transform into a human on land","df":"Not an antagonist — often a tragic romantic figure bound to a human by hiding its sealskin"},
    {"n":"Kelpie","origin":"Scottish folklore","fa":"A shape-shifting water spirit said to appear as a horse and drown those who ride it","df":"Folklore holds it can be tamed and controlled if a human manages to slip a bridle onto it"},
    {"n":"Banshee","origin":"Irish folklore","fa":"A female spirit whose mournful wail was said to foretell an impending death in the family","df":"Not an antagonist to be defeated — an omen figure rather than a foe"},
    {"n":"Leprechaun","origin":"Irish folklore","fa":"A small, mischievous fairy shoemaker said to guard a hidden pot of gold","df":"Tales describe humans catching one to demand his gold, though the leprechaun usually tricks his way free"},
    {"n":"Troll","origin":"Scandinavian folklore","fa":"A being ranging from small and mischievous to giant and dangerous, often said to turn to stone in sunlight","df":"Many folktales describe trolls being defeated simply by delaying them until sunrise turns them to stone"},
    {"n":"Werewolf","origin":"European folklore","fa":"A human said to transform into a wolf, often tied to the cycle of the full moon","df":"Later folklore and fiction established silver weapons as the traditional means of killing a werewolf"},
    {"n":"Vampire","origin":"European folklore","fa":"An undead being said to sustain itself by drinking the blood of the living","df":"Traditionally destroyed with a wooden stake through the heart, sunlight, or decapitation"},
    {"n":"Will-o'-the-wisp","origin":"European folklore","fa":"A ghostly light said to lead travelers astray from safe paths at night, especially in marshes","df":"Not defeated — folklore advises simply avoiding or ignoring its light rather than confronting it"},
    {"n":"Dryad","origin":"Greek mythology","fa":"A tree nymph believed to live and die alongside the specific tree she inhabited","df":"Not an antagonist — tied peacefully to her tree rather than opposed by any hero"},
    {"n":"Naiad","origin":"Greek mythology","fa":"A water nymph presiding over springs, streams and fountains","df":"Not an antagonist in Greek myth"},
    {"n":"Faun","origin":"Roman mythology","fa":"A woodland spirit similar to the Greek satyr, with the legs and horns of a goat","df":"Not an antagonist — a peaceful nature spirit in Roman tradition"},
    {"n":"Loch Ness Monster","origin":"Scottish folklore","fa":"A creature reputedly living in Loch Ness, Scotland, first widely reported in the 1930s","df":"No myth of defeat — an unconfirmed modern cryptid still occasionally 'sighted' today"},
    {"n":"Bigfoot","origin":"North American folklore","fa":"A large, ape-like creature reportedly sighted across forested regions of North America","df":"No myth of defeat — an unconfirmed modern cryptid rather than a monster from an ancient tale"},
    {"n":"Yowie","origin":"Australian Aboriginal folklore","fa":"An ape-like creature said to inhabit the remote bushland of Australia","df":"No myth of defeat — remains an unconfirmed cryptid in modern folklore"},
    {"n":"Baba Yaga's Hut Guardians","origin":"Slavic folklore","fa":"Fearsome spirits associated with the witch Baba Yaga's chicken-legged hut deep in the forest","df":"Heroines such as Vasilisa typically escape by completing impossible tasks rather than defeating the guardians"},
    {"n":"Rusalka","origin":"Slavic folklore","fa":"A water spirit believed to be the restless soul of a woman who died near or in water","df":"Not typically defeated — folklore describes appeasing or avoiding her rather than fighting her"},
    {"n":"Domovoi","origin":"Slavic folklore","fa":"A household spirit believed to protect a family's home if treated with respect","df":"Benevolent household guardian — not portrayed as an antagonist"},
    {"n":"Tikbalang","origin":"Philippine folklore","fa":"A creature with the body of a man and the head of a horse, said to lead travelers astray in the forest","df":"Said to be tamed by plucking one of the three magic hairs from its mane"},
    {"n":"Aswang","origin":"Philippine folklore","fa":"A shapeshifting creature blamed in folklore for various nocturnal terrors and disappearances","df":"Traditionally repelled using garlic, salt, or holy religious items, similar to European vampire lore"},
    {"n":"Popobawa","origin":"East African (Zanzibar) folklore","fa":"A shapeshifting, bat-like spirit tied to a wave of reported nighttime disturbances in the 1990s","df":"No myth of defeat — tied to a modern wave of folklore panic rather than an ancient hero's tale"},
    {"n":"Tokoloshe","origin":"Southern African (Zulu) folklore","fa":"A small, mischievous and sometimes malevolent water spirit said to cause trouble at night","df":"Traditionally warded off by raising one's bed on bricks, keeping the short spirit from reaching sleepers"},
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
    total = len(creatures)
    found = 0
    for i, s in enumerate(creatures):
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
    out = Path("assets/mythology/mythological_creatures.json")
    out.write_text(json.dumps(creatures, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    summary = "\nDone: {}/{} images -- {} creatures total.\n".format(found, total, total)
    sys.stdout.buffer.write(summary.encode("utf-8"))

if __name__ == "__main__":
    main()
