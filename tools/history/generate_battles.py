import json, requests, time

# n=name, da=date, lo=location, be=belligerents, re=result, fa=famous_for, im=image_url

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_OVERRIDES = {
    "Battle of the Spanish Armada":    "Spanish Armada",
    "D-Day — Battle of Normandy":      "Normandy landings",
    "Siege of Constantinople (1453)":  "Fall of Constantinople",
    "Battle of Liegnitz (1241)":       "Battle of Legnica",
    "Siege of Baghdad (1258)":         "Mongol siege of Baghdad",
    "Battle of Dan-no-ura":            "Battle of Dan-no-ura",
    "Battle of Kawanakajima (1561)":   "Battles of Kawanakajima",
    "Battle of Sekigahara":            "Battle of Sekigahara",
    "Siege of Osaka (1615)":           "Siege of Osaka",
    "Battle of Shiroyama":             "Battle of Shiroyama",
    "First Battle of Panipat":         "First Battle of Panipat",
    "Second Battle of Panipat":        "Second Battle of Panipat",
    "Third Battle of Panipat":         "Third Battle of Panipat",
    "Battle of Ayacucho":              "Battle of Ayacucho",
    "Battle of Boyacá":                "Battle of Boyacá",
    "Battle of Chacabuco":             "Battle of Chacabuco",
    "Paraguayan War — Battle of Tuyutí":"Battle of Tuyutí",
    "Battle of Omdurman":              "Battle of Omdurman",
    "Battle of Tondibi":               "Battle of Tondibi",
    "Battle of Kosovo (1389)":         "Battle of Kosovo",
    "Battle of Ankara (1402)":         "Battle of Ankara",
    "Battle of Mohács (1526)":         "Battle of Mohács",
    "Battle of Chaldiran":             "Battle of Chaldiran",
    "Siege of Malta (1565)":           "Siege of Malta",
    "Battle of the Indus (1221)":      "Battle of the Indus",
    "Battle of Mohi":                  "Battle of Mohi",
    "Battle of Kulikovo":              "Battle of Kulikovo",
    "Battle of Fei River":             "Battle of Fei River",
    "Battle of Yamen":                 "Battle of Yamen",
    "Battle of Ain Jalut":             "Battle of Ain Jalut",
    "Battle of Nagashino":             "Battle of Nagashino",
}

battles_raw = [
    # ── ANTIQUITÉ ─────────────────────────────────────────────────────────
    {"n":"Battle of Marathon","da":"490 BC","lo":"Marathon, Greece","be":"Athens & Plataea vs Persia","re":"Greek victory","fa":"10,000 Athenians defeated 25,000 Persians; a runner allegedly ran 40km to Athens to announce victory — inspiring the modern marathon"},
    {"n":"Battle of Thermopylae","da":"480 BC","lo":"Thermopylae, Greece","be":"300 Spartans & Greek allies vs Persia","re":"Persian victory","fa":"King Leonidas and 300 Spartans held off the Persian army for 3 days, becoming one of history's most celebrated last stands"},
    {"n":"Battle of Salamis","da":"480 BC","lo":"Straits of Salamis, Greece","be":"Greece vs Persia","re":"Greek victory","fa":"The Greek fleet destroyed the Persian navy, ending the Persian invasion and saving Western civilization according to many historians"},
    {"n":"Battle of Gaugamela","da":"331 BC","lo":"Gaugamela, Persia (Iraq)","be":"Macedonia vs Persia","re":"Macedonian victory","fa":"Alexander the Great defeated Darius III despite being outnumbered 5 to 1, effectively ending the Achaemenid Persian Empire"},
    {"n":"Battle of Cannae","da":"216 BC","lo":"Cannae, Italy","be":"Carthage vs Rome","re":"Carthaginian victory","fa":"Hannibal's double envelopment destroyed 70,000 Romans — still studied as the most perfect tactical encirclement in military history"},
    {"n":"Battle of Zama","da":"202 BC","lo":"Zama, Tunisia","be":"Rome vs Carthage","re":"Roman victory","fa":"Scipio Africanus defeated Hannibal, ending the Second Punic War and establishing Rome as the dominant Mediterranean power"},
    {"n":"Battle of Alesia","da":"52 BC","lo":"Alise-Sainte-Reine, Gaul","be":"Rome vs Gaul","re":"Roman victory","fa":"Caesar besieged 80,000 Gauls while simultaneously holding off a 250,000-strong relief army — ending Gallic independence"},
    {"n":"Battle of Actium","da":"31 BC","lo":"Gulf of Actium, Greece","be":"Octavian vs Antony & Cleopatra","re":"Octavian's victory","fa":"This naval battle ended the Roman Republic and established the Roman Empire under Augustus Caesar"},
    {"n":"Battle of Teutoburg Forest","da":"9 AD","lo":"Teutoburg Forest, Germany","be":"Germanic tribes vs Rome","re":"Germanic victory","fa":"Three Roman legions (20,000 men) were completely annihilated, halting Roman expansion into Germania permanently"},
    {"n":"Battle of Adrianople","da":"378 AD","lo":"Adrianople, Turkey","be":"Visigoths vs Roman Empire","re":"Visigoth victory","fa":"Emperor Valens was killed and the Roman army destroyed — marking the beginning of the fall of the Western Roman Empire"},
    {"n":"Battle of Fei River","da":"383 AD","lo":"Fei River, China","be":"Eastern Jin vs Former Qin","re":"Eastern Jin victory","fa":"An army of 80,000 defeated a force of 800,000 — the decisive battle that preserved Chinese culture south of the Yangtze"},
    # ── MOYEN ÂGE — EUROPE ───────────────────────────────────────────────
    {"n":"Battle of Tours","da":"732","lo":"Tours, France","be":"Frankish forces vs Umayyad Caliphate","re":"Frankish victory","fa":"Charles Martel stopped the Muslim advance into Western Europe, a pivotal moment in the shaping of Christian Europe"},
    {"n":"Battle of Hastings","da":"1066","lo":"Hastings, England","be":"Normans vs Anglo-Saxons","re":"Norman victory","fa":"William the Conqueror defeated King Harold II — transforming English language, culture and law through Norman influence"},
    {"n":"Battle of Manzikert","da":"1071","lo":"Manzikert, Turkey","be":"Seljuk Turks vs Byzantine Empire","re":"Seljuk victory","fa":"The crushing Byzantine defeat opened Anatolia to Turkish settlement, eventually leading to the fall of the Byzantine Empire"},
    {"n":"Battle of Hattin","da":"1187","lo":"Hattin, Israel","be":"Saladin vs Crusaders","re":"Muslim victory","fa":"Saladin's decisive victory led to the recapture of Jerusalem and effectively ended the First Kingdom of Jerusalem"},
    {"n":"Battle of Crécy","da":"1346","lo":"Crécy, France","be":"England vs France","re":"English victory","fa":"English longbowmen destroyed the French cavalry charge — the first major battle of the Hundred Years War"},
    {"n":"Battle of Agincourt","da":"1415","lo":"Agincourt, France","be":"England vs France","re":"English victory","fa":"Henry V's longbowmen devastated the French cavalry — immortalized by Shakespeare in Henry V"},
    {"n":"Siege of Constantinople (1453)","da":"1453","lo":"Constantinople (Istanbul)","be":"Ottoman Empire vs Byzantine Empire","re":"Ottoman victory","fa":"The 1,000-year Byzantine Empire fell to Mehmed II; the fall ended the Middle Ages and triggered the Renaissance"},
    {"n":"Battle of Bosworth Field","da":"1485","lo":"Bosworth, England","be":"Henry Tudor vs Richard III","re":"Tudor victory","fa":"Richard III was killed — the last English king to die in battle — ending the Wars of the Roses and starting the Tudor dynasty"},
    # ── MOYEN ÂGE — ASIE ────────────────────────────────────────────────
    {"n":"Battle of Talas","da":"751","lo":"Talas River, Kyrgyzstan","be":"Tang China vs Abbasid Caliphate","re":"Arab victory","fa":"The only clash between Tang China and the Islamic Caliphate; Arab victory spread Islam into Central Asia and ended Chinese westward expansion"},
    {"n":"Battle of Kosovo (1389)","da":"1389","lo":"Kosovo Polje, Serbia","be":"Ottoman Empire vs Serbian Principality","re":"Ottoman victory","fa":"Prince Lazar was killed; Serbia fell under Ottoman rule for nearly 500 years — Kosovo remains a symbol of Serbian national identity"},
    {"n":"Battle of Ankara (1402)","da":"1402","lo":"Ankara, Turkey","be":"Mongol Empire vs Ottoman Empire","re":"Mongol victory","fa":"Timur defeated and captured Sultan Bayezid I — the only Ottoman sultan ever taken prisoner, nearly collapsing the empire"},
    {"n":"Battle of Ain Jalut","da":"1260","lo":"Ain Jalut, Palestine","be":"Mamluk Sultanate vs Mongol Empire","re":"Mamluk victory","fa":"The first time the Mongol advance was permanently halted — a pivotal moment that saved Islam and stopped Mongol western expansion"},
    {"n":"Siege of Baghdad (1258)","da":"1258","lo":"Baghdad, Iraq","be":"Mongol Empire vs Abbasid Caliphate","re":"Mongol victory","fa":"Hulagu Khan destroyed the Islamic Golden Age's capital, massacring up to 800,000 people and destroying the Grand Library of Baghdad"},
    {"n":"Battle of Yamen","da":"1279","lo":"Yamen, China","be":"Yuan Mongols vs Song China","re":"Mongol victory","fa":"The last Song loyalists fought their final battle; the prime minister jumped into the sea with the child emperor, ending Chinese resistance"},
    {"n":"Battle of Kulikovo","da":"1380","lo":"Don River, Russia","be":"Grand Duchy of Moscow vs Golden Horde","re":"Russian victory","fa":"Dmitry Donskoy's first victory over the Mongols; sparked Russian national identity and began the long decline of Mongol power in Russia"},
    # ── MONGOLIE / ASIE CENTRALE ─────────────────────────────────────────
    {"n":"Battle of Liegnitz (1241)","da":"1241","lo":"Liegnitz, Poland","be":"Mongol Empire vs Polish-German forces","re":"Mongol victory","fa":"The Mongols annihilated a combined Polish-German army; only Ögedei Khan's death prevented a full-scale invasion of Western Europe"},
    {"n":"Battle of Mohi","da":"1241","lo":"Mohi, Hungary","be":"Mongol Empire vs Kingdom of Hungary","re":"Mongol victory","fa":"Batu Khan destroyed the Hungarian army, killing up to half the country's population — Hungary never fully recovered"},
    {"n":"Battle of the Indus (1221)","da":"1221","lo":"Indus River, Pakistan","be":"Mongol Empire vs Khwarazmian Empire","re":"Mongol victory","fa":"Genghis Khan cornered Jalal ad-Din on the Indus river banks, ending the Khwarazmian Empire — the path to Persia lay open"},
    # ── JAPON FÉODAL ─────────────────────────────────────────────────────
    {"n":"Battle of Dan-no-ura","da":"1185","lo":"Shimonoseki Strait, Japan","be":"Minamoto vs Taira clan","re":"Minamoto victory","fa":"The final naval battle of the Genpei War; the child emperor Antoku drowned as the Taira clan was destroyed, ending samurai civil war"},
    {"n":"Battle of Nagashino","da":"1575","lo":"Nagashino, Japan","be":"Oda Nobunaga vs Takeda Katsuyori","re":"Oda victory","fa":"Nobunaga's volley fire with 3,000 arquebusiers annihilated Takeda's legendary cavalry — revolutionizing Japanese warfare"},
    {"n":"Battle of Sekigahara","da":"1600","lo":"Sekigahara, Japan","be":"Tokugawa Ieyasu vs Ishida Mitsunari","re":"Tokugawa victory","fa":"The decisive battle that unified Japan; the Tokugawa shogunate ruled for 265 years of relative peace until 1868"},
    {"n":"Battle of Shiroyama","da":"1877","lo":"Shiroyama, Japan","be":"Imperial Japan vs Satsuma samurai","re":"Imperial victory","fa":"Saigo Takamori's last stand with 500 samurai against 30,000 soldiers — the final battle of the samurai era in Japan"},
    {"n":"Battle of Kawanakajima (1561)","da":"1561","lo":"Kawanakajima, Japan","be":"Uesugi Kenshin vs Takeda Shingen","re":"Inconclusive","fa":"The most famous clash of Japan's two greatest rivals; legend says Kenshin personally attacked Shingen during the chaos"},
    # ── INDE ─────────────────────────────────────────────────────────────
    {"n":"First Battle of Panipat","da":"1526","lo":"Panipat, India","be":"Babur vs Ibrahim Lodi","re":"Mughal victory","fa":"Babur's use of artillery and firearms defeated a larger force, founding the Mughal Empire that would rule India for 300 years"},
    {"n":"Second Battle of Panipat","da":"1556","lo":"Panipat, India","be":"Mughals vs Hemu","re":"Mughal victory","fa":"Akbar's regent Bairam Khan defeated Hindu king Hemu despite numerical inferiority, saving the Mughal Empire from collapse"},
    {"n":"Third Battle of Panipat","da":"1761","lo":"Panipat, India","be":"Afghan Durrani vs Maratha Confederacy","re":"Afghan victory","fa":"The Marathas' greatest defeat — 40,000-100,000 killed including their leadership, ending their pan-Indian ambitions permanently"},
    {"n":"Battle of Assaye","da":"1803","lo":"Assaye, India","be":"British East India Company vs Maratha Confederacy","re":"British victory","fa":"Wellington called it 'the bloodiest battle I ever saw'; despite huge losses, Britain broke Maratha power in western India"},
    # ── AMÉRIQUE DU SUD ───────────────────────────────────────────────────
    {"n":"Battle of Boyacá","da":"1819","lo":"Boyacá, Colombia","be":"Bolívar's forces vs Spanish royalists","re":"Patriot victory","fa":"Simón Bolívar liberated New Granada (Colombia) in a decisive 2-hour battle — the turning point of South American independence"},
    {"n":"Battle of Chacabuco","da":"1817","lo":"Chacabuco, Chile","be":"San Martín's forces vs Spanish royalists","re":"Patriot victory","fa":"San Martín's crossing of the Andes led to this surprise victory — liberating Chile from Spanish rule within days"},
    {"n":"Battle of Ayacucho","da":"1824","lo":"Ayacucho, Peru","be":"Grand Colombia vs Spain","re":"Patriot victory","fa":"The final battle of South American independence; Spain surrendered its last mainland South American territory"},
    {"n":"Paraguayan War — Battle of Tuyutí","da":"1866","lo":"Tuyutí, Paraguay","be":"Paraguay vs Triple Alliance","re":"Allied victory","fa":"Largest land battle in South American history; Paraguay lost 60% of its population in the war — one of history's most devastating conflicts"},
    # ── AFRIQUE SUB-SAHARIENNE ────────────────────────────────────────────
    {"n":"Battle of Tondibi","da":"1591","lo":"Tondibi, Mali","be":"Morocco vs Songhai Empire","re":"Moroccan victory","fa":"Moroccan muskets destroyed the Songhai cavalry — ending the last great West African empire and reshaping trans-Saharan trade routes"},
    {"n":"Battle of Isandlwana","da":"1879","lo":"Isandlwana, South Africa","be":"Zulu Kingdom vs Britain","re":"Zulu victory","fa":"20,000 Zulu warriors armed mainly with spears defeated a British force equipped with rifles — the worst British defeat in colonial Africa"},
    {"n":"Battle of Adwa","da":"1896","lo":"Adwa, Ethiopia","be":"Ethiopia vs Italy","re":"Ethiopian victory","fa":"Ethiopia became the only African nation to defeat a European colonial power — preserving its independence and inspiring pan-African movements"},
    {"n":"Battle of Omdurman","da":"1898","lo":"Omdurman, Sudan","be":"Britain & Egypt vs Mahdist Sudan","re":"British victory","fa":"Kitchener's forces killed 11,000 Mahdists in 5 hours; Winston Churchill charged with the 21st Lancers in the last British cavalry charge"},
    # ── EMPIRE OTTOMAN ────────────────────────────────────────────────────
    {"n":"Battle of Mohács (1526)","da":"1526","lo":"Mohács, Hungary","be":"Ottoman Empire vs Kingdom of Hungary","re":"Ottoman victory","fa":"Suleiman the Magnificent destroyed the Hungarian army in 2 hours; King Louis II drowned fleeing — opening Central Europe to Ottoman rule"},
    {"n":"Battle of Chaldiran","da":"1514","lo":"Chaldiran, Turkey","be":"Ottoman Empire vs Safavid Persia","re":"Ottoman victory","fa":"Selim I's artillery crushed the Safavid cavalry; the battle fixed the Sunni-Shia border that still roughly defines Iran-Turkey today"},
    {"n":"Siege of Malta (1565)","da":"1565","lo":"Malta","be":"Knights of Malta vs Ottoman Empire","re":"Christian victory","fa":"5,000 Knights of Malta and Maltese held off 40,000 Ottomans for 4 months — halting Ottoman western Mediterranean expansion"},
    {"n":"Battle of Lepanto","da":"1571","lo":"Gulf of Patras, Greece","be":"Holy League vs Ottoman Empire","re":"Holy League victory","fa":"The largest naval battle of the 16th century halted Ottoman naval expansion in the Mediterranean; Cervantes fought and lost his hand here"},
    # ── ÈRE MODERNE — EUROPE ────────────────────────────────────────────
    {"n":"Battle of the Spanish Armada","da":"1588","lo":"English Channel","be":"England vs Spain","re":"English victory","fa":"The Armada's destruction established English naval supremacy and helped Protestantism survive in northern Europe"},
    {"n":"Battle of Vienna","da":"1683","lo":"Vienna, Austria","be":"Holy Roman Empire & Poland vs Ottoman Empire","re":"European victory","fa":"The last great Ottoman advance into Europe was repelled — beginning the long Ottoman decline; croissants were allegedly invented to celebrate"},
    {"n":"Battle of Blenheim","da":"1704","lo":"Blenheim, Bavaria","be":"England & Austria vs France & Bavaria","re":"Allied victory","fa":"Marlborough and Eugene of Savoy's masterpiece; ended French dominance of Europe for the first time in generations"},
    {"n":"Battle of Poltava","da":"1709","lo":"Poltava, Ukraine","be":"Russia vs Sweden","re":"Russian victory","fa":"Peter the Great's decisive victory over Charles XII ended Swedish dominance in Northern Europe and confirmed Russia as a major power"},
    {"n":"Battle of Plassey","da":"1757","lo":"Plassey, India","be":"British East India Company vs Nawab of Bengal","re":"British victory","fa":"Robert Clive's victory through bribery laid the foundation for British colonial rule over India"},
    # ── RÉVOLUTIONS ET NAPOLÉON ──────────────────────────────────────────
    {"n":"Battle of Saratoga","da":"1777","lo":"Saratoga, New York","be":"American Colonies vs Britain","re":"American victory","fa":"The pivotal American victory convinced France to enter the Revolutionary War on the American side — turning the tide of the war"},
    {"n":"Battle of Trafalgar","da":"1805","lo":"Cape Trafalgar, Spain","be":"Britain vs France & Spain","re":"British victory","fa":"Nelson's fleet destroyed the Franco-Spanish navy but Nelson was killed; Britain gained unchallenged naval supremacy for a century"},
    {"n":"Battle of Austerlitz","da":"1805","lo":"Austerlitz, Czech Republic","be":"France vs Austria & Russia","re":"French victory","fa":"Napoleon's greatest tactical victory — lured the Allies into a trap by deliberately weakening his right flank"},
    {"n":"Battle of Borodino","da":"1812","lo":"Borodino, Russia","be":"France vs Russia","re":"Pyrrhic French victory","fa":"The bloodiest day of the Napoleonic Wars — 70,000 casualties; Russia's refusal to surrender despite the loss doomed Napoleon"},
    {"n":"Battle of Waterloo","da":"1815","lo":"Waterloo, Belgium","be":"France vs Britain & Prussia","re":"Allied victory","fa":"Napoleon's final defeat ended his rule and the Napoleonic Wars — 'Waterloo' became synonymous with final, crushing defeat"},
    # ── XIXe SIÈCLE ──────────────────────────────────────────────────────
    {"n":"Battle of San Jacinto","da":"1836","lo":"Texas","be":"Texas vs Mexico","re":"Texan victory","fa":"Sam Houston's 18-minute battle defeated Santa Anna and secured Texas independence — fought to cries of 'Remember the Alamo!'"},
    {"n":"Battle of Balaclava","da":"1854","lo":"Balaclava, Crimea","be":"Britain & allies vs Russia","re":"Inconclusive","fa":"The disastrous Charge of the Light Brigade — 600 cavalrymen charged into Russian artillery due to a misunderstood order"},
    {"n":"Battle of Gettysburg","da":"1863","lo":"Gettysburg, Pennsylvania","be":"Union vs Confederacy","re":"Union victory","fa":"The bloodiest battle of the Civil War (50,000 casualties) — Pickett's Charge failed catastrophically; the Confederacy never recovered"},
    {"n":"Battle of Sedan","da":"1870","lo":"Sedan, France","be":"Prussia vs France","re":"Prussian victory","fa":"Napoleon III was captured — ending the Second Empire; Prussia proclaimed the German Empire in Versailles' Hall of Mirrors"},
    {"n":"Battle of Little Bighorn","da":"1876","lo":"Montana, USA","be":"Lakota & Cheyenne vs US Army","re":"Native American victory","fa":"General Custer's entire command was annihilated — 'Custer's Last Stand' became America's most famous military disaster"},
    {"n":"Battle of Isandlwana","da":"1879","lo":"Isandlwana, South Africa","be":"Zulu Kingdom vs Britain","re":"Zulu victory","fa":"20,000 Zulu warriors armed mainly with spears defeated a British force equipped with rifles — the worst British defeat in colonial Africa"},
    {"n":"Battle of Tsushima","da":"1905","lo":"Tsushima Strait, Japan","be":"Japan vs Russia","re":"Japanese victory","fa":"Japan destroyed the entire Russian Baltic Fleet in 45 minutes — the first time an Asian power defeated a European great power in modern times"},
    # ── PREMIÈRE GUERRE MONDIALE ─────────────────────────────────────────
    {"n":"Battle of the Marne","da":"1914","lo":"Marne River, France","be":"France & Britain vs Germany","re":"Allied victory","fa":"'The Miracle of the Marne' — taxis of Paris rushed 6,000 soldiers to halt the German advance, saving Paris and forcing trench warfare"},
    {"n":"Battle of Gallipoli","da":"1915","lo":"Gallipoli, Turkey","be":"Allies vs Ottoman Empire","re":"Ottoman victory","fa":"The disastrous amphibious assault cost 130,000 lives; its failure shaped Australian and New Zealand national identity (ANZAC Day)"},
    {"n":"Battle of Verdun","da":"1916","lo":"Verdun, France","be":"France vs Germany","re":"French victory","fa":"The longest battle of WWI (10 months, 700,000 casualties) — 'The Meatgrinder' became the symbol of the war's futility"},
    {"n":"Battle of the Somme","da":"1916","lo":"Somme, France","be":"Britain & France vs Germany","re":"Inconclusive","fa":"60,000 British casualties on the first day alone — the bloodiest day in British military history"},
    {"n":"Battle of Jutland","da":"1916","lo":"North Sea","be":"Britain vs Germany","re":"Inconclusive","fa":"The largest naval battle of WWI; though Germany inflicted more damage, Britain retained control of the North Sea"},
    {"n":"Battle of Passchendaele","da":"1917","lo":"Flanders, Belgium","be":"Britain & allies vs Germany","re":"Allied victory","fa":"300,000 casualties fighting through mud so thick soldiers drowned — soldiers called it 'The Battle of the Mud'"},
    {"n":"Battle of the Argonne Forest","da":"1918","lo":"Argonne, France","be":"USA & France vs Germany","re":"Allied victory","fa":"The largest battle in American history — 1.2 million US troops; Sergeant Alvin York single-handedly captured 132 Germans"},
    # ── SECONDE GUERRE MONDIALE ──────────────────────────────────────────
    {"n":"Battle of Britain","da":"1940","lo":"Britain / English Channel","be":"Britain vs Germany (Luftwaffe)","re":"British victory","fa":"The RAF's victory over the Luftwaffe prevented a German invasion; Churchill said 'Never was so much owed by so many to so few'"},
    {"n":"Battle of Midway","da":"1942","lo":"Midway Atoll, Pacific","be":"USA vs Japan","re":"American victory","fa":"The US sank 4 Japanese carriers while losing 1 — the pivotal Pacific battle that permanently shifted naval power to the United States"},
    {"n":"Battle of El Alamein","da":"1942","lo":"El Alamein, Egypt","be":"Britain & allies vs Germany & Italy","re":"Allied victory","fa":"Montgomery's defeat of Rommel's Africa Korps; Churchill said 'Before Alamein we never had a victory; after Alamein we never had a defeat'"},
    {"n":"Battle of Stalingrad","da":"1942","lo":"Stalingrad, Soviet Union","be":"Soviet Union vs Germany","re":"Soviet victory","fa":"The largest and bloodiest battle in history (2 million casualties); Field Marshal Paulus surrendered — the turning point of WWII"},
    {"n":"Battle of Kursk","da":"1943","lo":"Kursk, Soviet Union","be":"Soviet Union vs Germany","re":"Soviet victory","fa":"The largest tank battle in history; after Kursk, Germany was never able to launch a major offensive on the Eastern Front again"},
    {"n":"D-Day — Battle of Normandy","da":"1944","lo":"Normandy, France","be":"Allies vs Germany","re":"Allied victory","fa":"The largest amphibious operation in history — 156,000 troops landed on 5 beaches; opened the Western Front that defeated Nazi Germany"},
    {"n":"Battle of the Bulge","da":"1944","lo":"Ardennes, Belgium","be":"USA & allies vs Germany","re":"Allied victory","fa":"Germany's last major offensive — 'Nuts!' replied General McAuliffe to a German surrender demand; 76,000 American casualties"},
    {"n":"Battle of Iwo Jima","da":"1945","lo":"Iwo Jima, Pacific","be":"USA vs Japan","re":"American victory","fa":"The iconic flag-raising photo was taken here; 26,000 US and 22,000 Japanese casualties — one of the bloodiest Pacific battles"},
    {"n":"Battle of Berlin","da":"1945","lo":"Berlin, Germany","be":"Soviet Union vs Germany","re":"Soviet victory","fa":"The final battle of WWII in Europe — 360,000 Soviet and 100,000 German casualties; Hitler committed suicide as Soviets entered the city"},
    {"n":"Battle of Okinawa","da":"1945","lo":"Okinawa, Japan","be":"USA vs Japan","re":"American victory","fa":"The bloodiest Pacific battle — 12,000 Americans, 110,000 Japanese and 100,000 Okinawan civilians died; prompted use of atomic bombs"},
    # ── APRÈS 1945 ────────────────────────────────────────────────────────
    {"n":"Battle of Inchon","da":"1950","lo":"Inchon, South Korea","be":"UN forces vs North Korea","re":"UN victory","fa":"MacArthur's surprise amphibious landing behind enemy lines reversed the Korean War — considered one of history's greatest military gambles"},
    {"n":"Battle of Dien Bien Phu","da":"1954","lo":"Dien Bien Phu, Vietnam","be":"Viet Minh vs France","re":"Vietnamese victory","fa":"The decisive battle ended French colonialism in Indochina — the only time a guerrilla army defeated a Western colonial power in pitched battle"},
    {"n":"Six-Day War","da":"1967","lo":"Middle East","be":"Israel vs Egypt, Jordan, Syria","re":"Israeli victory","fa":"Israel defeated three Arab armies in 6 days, tripling its territory — one of the most rapid military victories of the 20th century"},
    {"n":"Battle of Hue","da":"1968","lo":"Hue, Vietnam","be":"USA & South Vietnam vs North Vietnam","re":"US/South Vietnamese recapture","fa":"The deadliest battle of the Vietnam War for the US Marines; the Tet Offensive shocked American public opinion and turned the tide against the war"},
    {"n":"Battle of Mogadishu","da":"1993","lo":"Mogadishu, Somalia","be":"USA vs Somali militias","re":"US tactical withdrawal","fa":"'Black Hawk Down' — US forces lost 18 soldiers and 2 helicopters; the battle led the US to withdraw from Somalia"},
    {"n":"Battle of Fallujah","da":"2004","lo":"Fallujah, Iraq","be":"USA & Iraq vs insurgents","re":"US/Iraqi victory","fa":"The largest urban combat operation since Hue in 1968; 95 US deaths, 800+ insurgents killed in door-to-door fighting"},
]

def fetch_wikipedia_image(name):
    wiki_title = WIKI_OVERRIDES.get(name, name)
    try:
        r = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={"action":"query","titles":wiki_title,"prop":"pageimages",
                    "format":"json","pithumbsize":500,"redirects":1},
            headers=HEADERS, timeout=8
        )
        if r.status_code != 200:
            return None
        for page in r.json().get("query",{}).get("pages",{}).values():
            src = page.get("thumbnail",{}).get("source")
            if src:
                return src
        return None
    except Exception:
        return None

print(f"Fetching images for {len(battles_raw)} battles...")
result = []
for i, b in enumerate(battles_raw):
    img = fetch_wikipedia_image(b["n"])
    b["im"] = img
    result.append(b)
    status = "ok" if img else "x"
    print(f"  [{i+1}/{len(battles_raw)}] {status} {b['n']}")
    time.sleep(0.25)

import os
os.makedirs("assets/history", exist_ok=True)
with open("assets/history/battles.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, separators=(',',':'))

found = sum(1 for b in result if b["im"])
print(f"\n{len(result)} batailles generees. Images: {found}/{len(result)}.")
