import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote
sys.stdout.reconfigure(encoding="utf-8")

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_EN = {
    "Sif": "Sif",
    "Ran": "Ran (goddess)",
    "Var": "Var (goddess)",
    "Vor": "Vor (goddess)",
    "Syn": "Syn (goddess)",
    "Eir": "Eir",
}

# n=name, dom=domain/role, sym=symbol, fa=fact
figures = [
    {"n":"Odin","dom":"All-father, god of wisdom, war and the dead","sym":"Spear Gungnir, two ravens, eight-legged horse","fa":"Sacrificed one of his eyes at Mimir's well in exchange for wisdom"},
    {"n":"Thor","dom":"God of thunder and protector of mankind","sym":"Hammer Mjolnir, belt of strength","fa":"His hammer Mjolnir always returned to his hand after being thrown"},
    {"n":"Loki","dom":"Trickster god associated with mischief and chaos","sym":"Shapeshifting, fire","fa":"Could shapeshift into animals and was eventually bound in punishment for causing Baldur's death"},
    {"n":"Frigg","dom":"Goddess of marriage, motherhood and foresight","sym":"Spindle, falcon cloak","fa":"Odin's wife, said to know everyone's fate but never reveal it"},
    {"n":"Freyja","dom":"Goddess of love, beauty, war and death","sym":"Necklace Brisingamen, cat-drawn chariot","fa":"Received half of all warriors who died in battle, with Odin receiving the other half"},
    {"n":"Freyr","dom":"God of fertility, prosperity and good harvests","sym":"Golden boar, ship Skidbladnir","fa":"Owned a ship that could fold up small enough to fit in a pocket"},
    {"n":"Baldur","dom":"God of light, beauty and purity","sym":"Light, radiance","fa":"His death, engineered by Loki, was said to help trigger the events of Ragnarok"},
    {"n":"Tyr","dom":"God of law, justice and heroic glory","sym":"Sword, one hand","fa":"Sacrificed his hand to bind the monstrous wolf Fenrir"},
    {"n":"Heimdall","dom":"Watchman of the gods","sym":"Horn Gjallarhorn, golden teeth","fa":"Guards the rainbow bridge Bifrost and will sound his horn to signal the start of Ragnarok"},
    {"n":"Njord","dom":"God of the sea, wind and wealth","sym":"Ship, coastal winds","fa":"Father of Freyr and Freyja, associated with safe sea travel and fishing"},
    {"n":"Idun","dom":"Goddess who guards the apples of youth","sym":"Golden apples","fa":"Her apples were said to keep the gods eternally youthful"},
    {"n":"Bragi","dom":"God of poetry and eloquence","sym":"Harp, runes carved on his tongue","fa":"Said to have runes carved onto his tongue at birth, granting him poetic skill"},
    {"n":"Hel","dom":"Ruler of the underworld realm of the same name","sym":"Half-living, half-corpse appearance","fa":"Depicted as half beautiful woman and half decaying corpse, ruling over those who die of sickness or age"},
    {"n":"Vidar","dom":"God of vengeance and silence","sym":"Thick shoe, sword","fa":"Fated to avenge Odin's death at Ragnarok by killing the wolf Fenrir"},
    {"n":"Skadi","dom":"Goddess of winter, mountains and skiing","sym":"Bow, skis","fa":"Chose her husband among the gods by looking only at their feet"},
    {"n":"Sif","dom":"Goddess associated with the earth and harvest","sym":"Golden hair","fa":"Her golden hair, said to represent wheat fields, was cut off by Loki as a prank"},
    {"n":"Ullr","dom":"God of hunting, skiing and archery","sym":"Bow, skis, shield","fa":"Was said to be so swift on skis that no one could catch him"},
    {"n":"Aegir","dom":"God or giant ruling over the sea","sym":"Cauldron, sea foam","fa":"Known for hosting legendary feasts for the gods deep beneath the waves"},
    {"n":"Ran","dom":"Goddess of the sea who collects the drowned","sym":"Fishing net","fa":"Said to use a net to drag sailors down to her underwater hall"},
    {"n":"Forseti","dom":"God of justice and reconciliation","sym":"Golden hall, scales","fa":"Presided over a hall where disputes among gods and men were peacefully settled"},
    {"n":"Vali","dom":"God born specifically to avenge Baldur's death","sym":"Bow and arrow","fa":"Grew to full size in a single day in order to avenge his brother Baldur"},
    {"n":"Sigurd","dom":"Legendary hero and dragon-slayer","sym":"Sword Gram","fa":"Slew the dragon Fafnir and gained the ability to understand the speech of birds after tasting its blood"},
    {"n":"Ragnar Lodbrok","dom":"Legendary Viking king and hero","sym":"Shield, longship","fa":"A legendary figure whose sagas mix historical raids with myth and legend"},
    {"n":"Volund","dom":"Legendary master smith","sym":"Forge, wings","fa":"Crafted a pair of wings to escape captivity after being enslaved by a cruel king"},
    {"n":"Norns","dom":"Female beings who shape the fate of gods and men","sym":"Well of Urd, weaving thread","fa":"The three Norns were said to weave the threads of fate at the base of the world tree Yggdrasil"},
    {"n":"Valkyries","dom":"Female figures who choose who dies and lives in battle","sym":"Winged helmet, spear","fa":"Carried chosen slain warriors to Odin's hall of Valhalla"},
    {"n":"Yggdrasil","dom":"The immense world tree connecting the nine realms","sym":"Ash tree","fa":"Its roots and branches were believed to connect all nine worlds of Norse cosmology"},
    {"n":"Valhalla","dom":"Odin's majestic hall for slain warriors","sym":"Golden hall, shields as roof tiles","fa":"Said to have a roof made of interlocking shields, housing warriors preparing for Ragnarok"},
    {"n":"Asgard","dom":"The realm of the Aesir gods","sym":"Golden fortress","fa":"Connected to the human realm of Midgard by the rainbow bridge Bifrost"},
    {"n":"Midgard","dom":"The realm of humans in Norse cosmology","sym":"Earth","fa":"Believed to be encircled by the vast sea serpent Jormungandr"},
    {"n":"Ragnarok","dom":"The prophesied end of the world and the gods","sym":"Twilight of the gods","fa":"A foretold final battle in which most of the major gods, including Odin and Thor, were fated to die"},
    {"n":"Bifrost","dom":"The burning rainbow bridge linking Asgard and Midgard","sym":"Rainbow","fa":"Guarded constantly by the god Heimdall against intruders"},
    {"n":"Aesir","dom":"The principal tribe of gods, including Odin and Thor","sym":"Asgard","fa":"Once warred with the Vanir gods before eventually making peace and merging pantheons"},
    {"n":"Vanir","dom":"A tribe of gods associated with fertility and prosperity","sym":"Fertility, nature","fa":"Includes Freyr and Freyja, who joined the Aesir in Asgard after the Aesir-Vanir war"},
    {"n":"Mimir","dom":"Being renowned for wisdom, keeper of a sacred well","sym":"Well of wisdom","fa":"Odin consulted his severed, preserved head for counsel even after Mimir's death"},
    {"n":"Dwarves (Norse)","dom":"Master craftsmen dwelling underground","sym":"Forge, precious metals","fa":"Said to have crafted many of the gods' greatest treasures, including Thor's hammer Mjolnir"},
    {"n":"Elves (Norse)","dom":"Supernatural beings associated with light or darkness","sym":"Light, nature","fa":"Divided into light elves living in the sky and dark elves living underground"},
    {"n":"Jotnar","dom":"A race of giants often in conflict with the gods","sym":"Mountains, ice, fire","fa":"Many gods, including Odin, had giant ancestry despite the frequent conflict between the two groups"},
    {"n":"Ymir","dom":"The primordial giant from whom the world was made","sym":"Primordial ice and fire","fa":"His body was said to have been used by the gods to create the earth, sky and sea"},
    {"n":"Buri","dom":"The first god, ancestor of the Aesir","sym":"Ice, primordial cow","fa":"Said to have been licked out of a block of salty ice by a primordial cow named Audhumla"},
    {"n":"Audhumla","dom":"The primordial cow who nourished the first beings","sym":"Cow, salty ice","fa":"Fed the giant Ymir with her milk while licking the first god, Buri, free from ice"},
    {"n":"Nott","dom":"Personification of night","sym":"Dark chariot","fa":"Rides across the sky each night in a chariot pulled by a horse named Hrimfaxi"},
    {"n":"Dagr","dom":"Personification of day","sym":"Bright chariot","fa":"Rides across the sky each day in a chariot pulled by a shining horse named Skinfaxi"},
    {"n":"Sol","dom":"Goddess who guides the sun's chariot","sym":"Sun chariot","fa":"Constantly pursued across the sky by a wolf who is fated to catch her at Ragnarok"},
    {"n":"Mani","dom":"God who guides the moon's chariot","sym":"Moon chariot","fa":"Brother of Sol, also pursued eternally by a wolf across the heavens"},
    {"n":"Kvasir","dom":"Being born from the gods' collective wisdom","sym":"Mead of poetry","fa":"His blood was brewed into the legendary Mead of Poetry, said to grant the gift of poetry to whoever drinks it"},
    {"n":"Angrboda","dom":"Giantess, mother of several of Loki's monstrous children","sym":"Iron forest","fa":"Mother of Fenrir, Jormungandr and Hel with Loki"},
    {"n":"Gerd","dom":"Giantess who became Freyr's wife","sym":"Radiant beauty","fa":"Freyr fell so deeply in love with her that he traded away his magic sword to win her hand"},
    {"n":"Nanna","dom":"Goddess associated with Baldur, his devoted wife","sym":"Grief, funeral pyre","fa":"Died of grief and was placed on the same funeral pyre as her husband Baldur"},
    {"n":"Hodr","dom":"Blind god who unknowingly killed Baldur","sym":"Mistletoe dart","fa":"Was tricked by Loki into throwing a mistletoe dart that killed his brother Baldur"},
    {"n":"Brokkr and Eitri","dom":"Dwarven brothers renowned as master smiths","sym":"Forge, bellows","fa":"Crafted Thor's hammer Mjolnir in a wager against Loki, despite his repeated sabotage attempts"},
    {"n":"Sindri","dom":"Legendary dwarven craftsman","sym":"Forge","fa":"Sometimes named as one of the dwarven smiths behind the gods' greatest treasures"},
    {"n":"Brynhildr","dom":"Legendary shieldmaiden and former Valkyrie","sym":"Shield, ring of fire","fa":"Was placed in an enchanted sleep surrounded by fire until the hero Sigurd rescued her"},
    {"n":"Starkad","dom":"Legendary warrior granted an unnaturally long life","sym":"Sword","fa":"Cursed to commit three great evil deeds in exchange for three lifetimes of a normal man"},
    {"n":"Helgi Hundingsbane","dom":"Legendary hero and saga protagonist","sym":"Sword","fa":"His saga tells of his love for the Valkyrie Sigrun and his eventual death and reincarnation"},
    {"n":"Fjalar and Galar","dom":"Dwarven brothers who killed the wise being Kvasir","sym":"Mead vessels","fa":"Drained Kvasir's blood and mixed it with honey to create the legendary Mead of Poetry"},
    {"n":"Surt","dom":"Fire giant destined to battle the gods at Ragnarok","sym":"Flaming sword","fa":"Prophesied to set the entire world ablaze with his sword at the end of Ragnarok"},
    {"n":"Vafthrudnir","dom":"Wise giant who competed with Odin in a contest of knowledge","sym":"Ancient wisdom","fa":"Engaged Odin in a deadly quiz contest, wagering his own head on the outcome"},
    {"n":"Suttung","dom":"Giant who guarded the Mead of Poetry","sym":"Mountain vault","fa":"Hid the Mead of Poetry inside a mountain, guarded by his daughter Gunnlod"},
    {"n":"Gunnlod","dom":"Giantess who guarded the Mead of Poetry","sym":"Mead vessel","fa":"Was tricked by Odin, who seduced her to steal the Mead of Poetry"},
    {"n":"Ottar","dom":"Mortal man aided by the goddess Freyja","sym":"Boar disguise","fa":"Was magically disguised as a boar by Freyja so he could safely learn about his ancestry"},
    {"n":"Hyndla","dom":"Giantess and seeress consulted about lineage and fate","sym":"Cave dwelling","fa":"Recited long genealogies of legendary heroes when questioned by Freyja"},
    {"n":"Gullveig","dom":"Mysterious figure whose burning triggered the Aesir-Vanir war","sym":"Fire, gold","fa":"Her repeated burning and rebirth is said to have sparked the first war between the two tribes of gods"},
    {"n":"Skirnir","dom":"Freyr's messenger and servant","sym":"Freyr's magic sword","fa":"Was sent to woo the giantess Gerd on Freyr's behalf, using threats and magic to win her over"},
    {"n":"Nerthus","dom":"Ancient earth goddess linked to fertility","sym":"Sacred wagon","fa":"Worshipped with a sacred wagon procession, later thought to be an earlier form of the god Njord"},
    {"n":"Var","dom":"Goddess who witnesses oaths and agreements","sym":"Binding contracts","fa":"Believed to punish anyone who broke a sworn oath or promise"},
    {"n":"Vor","dom":"Goddess of wisdom and careful observation","sym":"All-seeing awareness","fa":"Said to be so wise and attentive that nothing could be hidden from her"},
    {"n":"Syn","dom":"Goddess who guards doors and defends against false claims","sym":"Locked door","fa":"Invoked in legal disputes to help deny false accusations"},
    {"n":"Lofn","dom":"Goddess associated with permission to marry","sym":"Union of lovers","fa":"Said to help lovers overcome obstacles and gain permission to wed"},
    {"n":"Sjofn","dom":"Goddess who inspires love and affection","sym":"Heart, affection","fa":"Believed to turn people's thoughts and hearts toward love"},
    {"n":"Gefjon","dom":"Goddess associated with plowing and the land","sym":"Plow, oxen","fa":"Said to have plowed a piece of Sweden so deeply it broke away to form the island of Zealand"},
    {"n":"Eir","dom":"Goddess associated with healing and medicine","sym":"Herbs, healing hands","fa":"Regarded as the best of healers among the goddesses"},
    {"n":"Snotra","dom":"Goddess of wisdom, self-control and good manners","sym":"Refined conduct","fa":"Represented gentleness and prudent behavior among the Norse goddesses"},
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
    out = Path("assets/mythology/norse_mythology.json")
    out.write_text(json.dumps(figures, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    summary = "\nDone: {}/{} images -- {} figures total.\n".format(found, total, total)
    sys.stdout.buffer.write(summary.encode("utf-8"))

if __name__ == "__main__":
    main()
