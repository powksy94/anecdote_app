import json, requests, time, os, sys
sys.stdout.reconfigure(encoding="utf-8")

# n=name, co=country, ty=type, st=status(Active/Dormant/Extinct),
# el=elevation(m), le=lastEruption, lo=location, fa=famousFor,
# im=wikipedia_image_url(None if not found)

VOLCANOES_RAW = [
    # ── EUROPE ────────────────────────────────────────────────────────────────
    {"n":"Mount Vesuvius",       "co":"Italy",          "ty":"Stratovolcano",   "st":"Active",  "el":1281, "le":"1944",       "lo":"Gulf of Naples, Campania",           "fa":"The only active volcano on mainland Europe; its 79 AD eruption buried the Roman cities of Pompeii and Herculaneum under meters of ash, preserving them in perfect detail"},
    {"n":"Mount Etna",           "co":"Italy",          "ty":"Stratovolcano",   "st":"Active",  "el":3357, "le":"2024",       "lo":"Sicily",                             "fa":"Europe's tallest and most active volcano, erupting for over 2.5 million years; the ancient Greeks believed it was the forge of Hephaestus, god of fire"},
    {"n":"Stromboli",            "co":"Italy",          "ty":"Stratovolcano",   "st":"Active",  "el":924,  "le":"2024",       "lo":"Aeolian Islands, Sicily",            "fa":"Known as the 'Lighthouse of the Mediterranean', Stromboli has erupted almost continuously for 2,000 years, shooting lava every few minutes without interruption"},
    {"n":"Campi Flegrei",        "co":"Italy",          "ty":"Caldera",         "st":"Active",  "el":458,  "le":"1538",       "lo":"West of Naples, Campania",           "fa":"A vast supervolcanic caldera 13 km wide partly beneath the Bay of Pozzuoli; scientists have raised alert levels due to recent ground uplift near a city of 3 million people"},
    {"n":"Eyjafjallajökull",     "co":"Iceland",        "ty":"Stratovolcano",   "st":"Active",  "el":1651, "le":"2010",       "lo":"Southern Iceland",                   "fa":"Its 2010 eruption caused the largest disruption to European air travel since World War II, grounding over 100,000 flights and stranding 10 million passengers"},
    {"n":"Hekla",                "co":"Iceland",        "ty":"Stratovolcano",   "st":"Active",  "el":1491, "le":"2000",       "lo":"Southern Iceland",                   "fa":"Known as the 'Gateway to Hell' in medieval Europe; the 1947 eruption began without warning and lasted 13 months, terrifying Iceland's population"},
    {"n":"Katla",                "co":"Iceland",        "ty":"Subglacial",      "st":"Active",  "el":1512, "le":"1918",       "lo":"Mýrdalsjökull glacier, Iceland",     "fa":"Lying beneath a glacier, Katla's eruptions produce catastrophic floods (jökulhlaups); it erupts every 40-80 years and is considered dangerously overdue"},
    {"n":"Krafla",               "co":"Iceland",        "ty":"Caldera",         "st":"Active",  "el":818,  "le":"1984",       "lo":"Northeast Iceland",                  "fa":"During the Krafla Fires of 1975-1984, the Krafla caldera erupted nine times; geothermal drilling here accidentally hit a magma chamber in 2009"},
    {"n":"Santorini (Thera)",    "co":"Greece",         "ty":"Caldera",         "st":"Active",  "el":567,  "le":"1950",       "lo":"Aegean Sea, Cyclades",               "fa":"The Minoan eruption around 1600 BC was one of the largest in human history; it may have inspired the Atlantis legend and contributed to the collapse of Minoan civilization"},
    {"n":"Mount Teide",          "co":"Spain",          "ty":"Stratovolcano",   "st":"Active",  "el":3715, "le":"1909",       "lo":"Tenerife, Canary Islands",           "fa":"Spain's highest peak and the world's third tallest volcanic structure from its ocean base; considered the pillar supporting the sky in ancient Guanche mythology"},
    {"n":"Laki",                 "co":"Iceland",        "ty":"Fissure Vent",    "st":"Dormant", "el":818,  "le":"1785",       "lo":"Southern Iceland",                   "fa":"The 1783 Laki eruption was one of Europe's most catastrophic; the sulfuric haze it produced caused crop failures across Europe and contributed to the famine preceding the French Revolution"},
    # ── PACIFIC RING OF FIRE — AMERICAS ───────────────────────────────────────
    {"n":"Krakatoa",             "co":"Indonesia",      "ty":"Caldera",         "st":"Active",  "el":813,  "le":"2022",       "lo":"Sunda Strait, Java Sea",             "fa":"The 1883 eruption killed over 36,000 people and was heard 5,000 km away in Australia; it caused global temperature drops and spectacular red sunsets worldwide for a year"},
    {"n":"Tambora",              "co":"Indonesia",      "ty":"Stratovolcano",   "st":"Active",  "el":2850, "le":"1967",       "lo":"Sumbawa Island, Indonesia",          "fa":"The 1815 eruption was the largest in recorded history; it caused the 'Year Without a Summer' in 1816, leading to global crop failures, famines, and the coldest temperatures in 1,500 years"},
    {"n":"Mount Pinatubo",       "co":"Philippines",    "ty":"Stratovolcano",   "st":"Active",  "el":1486, "le":"1993",       "lo":"Luzon Island, Philippines",          "fa":"The 1991 eruption was the second largest of the 20th century; it injected so much sulfur dioxide into the stratosphere that it lowered global temperatures by 0.5°C for two years"},
    {"n":"Mayon Volcano",        "co":"Philippines",    "ty":"Stratovolcano",   "st":"Active",  "el":2462, "le":"2023",       "lo":"Albay province, Luzon",              "fa":"The Philippines' most active volcano with 51 eruptions since 1616; renowned as the world's most perfect volcanic cone shape, a near-flawless symmetrical triangle"},
    {"n":"Taal Volcano",         "co":"Philippines",    "ty":"Caldera",         "st":"Active",  "el":311,  "le":"2022",       "lo":"Batangas province, Luzon",           "fa":"One of the world's smallest active volcanoes, situated on an island inside a lake, itself inside another volcanic caldera; the 2020 eruption created a volcanic lightning spectacle"},
    {"n":"Mount St. Helens",     "co":"USA",            "ty":"Stratovolcano",   "st":"Active",  "el":2549, "le":"2008",       "lo":"Washington State, Cascade Range",    "fa":"The 1980 eruption caused the largest landslide in recorded history and reduced the mountain's height by 400 m; it killed 57 people and flattened over 500 km² of forest"},
    {"n":"Mauna Loa",            "co":"USA",            "ty":"Shield Volcano",  "st":"Active",  "el":4169, "le":"2022",       "lo":"Big Island, Hawaii",                 "fa":"The world's largest active volcano by volume and area; its lava flows have covered 39% of the Big Island of Hawaii since its first recorded eruption in 1843"},
    {"n":"Kīlauea",              "co":"USA",            "ty":"Shield Volcano",  "st":"Active",  "el":1247, "le":"2024",       "lo":"Big Island, Hawaii",                 "fa":"One of the most continuously active volcanoes on Earth; its 35-year eruption (1983-2018) was the longest in Hawaiian history, adding 875 acres of new land to the Big Island"},
    {"n":"Mount Rainier",        "co":"USA",            "ty":"Stratovolcano",   "st":"Active",  "el":4392, "le":"1894",       "lo":"Washington State, Cascade Range",    "fa":"The most glaciated peak in the contiguous USA; scientists consider it one of the most dangerous volcanoes in the world due to its proximity to the Seattle-Tacoma metropolitan area"},
    {"n":"Mount Shasta",         "co":"USA",            "ty":"Stratovolcano",   "st":"Active",  "el":4322, "le":"1786",       "lo":"Northern California, Cascades",      "fa":"One of California's most iconic mountains; considered sacred by multiple Native American tribes; produces more glacial meltwater than any other peak in the contiguous USA"},
    {"n":"Yellowstone Caldera",  "co":"USA",            "ty":"Supervolcano",    "st":"Active",  "el":2805, "le":"70000 BC",   "lo":"Wyoming, Yellowstone NP",            "fa":"A supervolcano sitting on a massive magma chamber; its last full eruption 640,000 years ago ejected 1,000 km³ of material; its geothermal features power Old Faithful geyser"},
    {"n":"Popocatépetl",         "co":"Mexico",         "ty":"Stratovolcano",   "st":"Active",  "el":5426, "le":"2024",       "lo":"Central Mexico",                     "fa":"'El Popo' looms 70 km from Mexico City and is monitored 24/7 given its proximity to 25 million people; has been in renewed activity since 1994 after 70 years of dormancy"},
    {"n":"Colima",               "co":"Mexico",         "ty":"Stratovolcano",   "st":"Active",  "el":3860, "le":"2023",       "lo":"Jalisco State, Mexico",              "fa":"One of the most active volcanoes in North America, with over 40 eruptions since 1576; its twin peaks include the dormant Nevado de Colima, Mexico's fifth highest mountain"},
    {"n":"Santa María",          "co":"Guatemala",      "ty":"Stratovolcano",   "st":"Active",  "el":3772, "le":"2024",       "lo":"Quetzaltenango, Guatemala",          "fa":"After 500 years of dormancy, the 1902 eruption was one of the three largest of the 20th century; its lava dome Santiaguito has been continuously erupting since 1922"},
    {"n":"Pacaya",               "co":"Guatemala",      "ty":"Stratovolcano",   "st":"Active",  "el":2552, "le":"2021",       "lo":"Guatemala City region",              "fa":"One of the most active volcanoes in Central America and one of the most accessible for visitors; it is possible to walk to the edge of active lava flows on guided tours"},
    {"n":"Arenal",               "co":"Costa Rica",     "ty":"Stratovolcano",   "st":"Active",  "el":1670, "le":"2010",       "lo":"Alajuela province, Costa Rica",      "fa":"Considered dormant for 400 years before suddenly erupting in 1968, killing 87 people and destroying three villages; was one of the world's most active volcanoes for 42 years"},
    {"n":"Cotopaxi",             "co":"Ecuador",        "ty":"Stratovolcano",   "st":"Active",  "el":5897, "le":"2016",       "lo":"Andes, Ecuador",                     "fa":"One of the highest active volcanoes in the world, with one of Earth's few equatorial glaciers; historically its eruptions triggered devastating mudflows reaching the Pacific coast"},
    {"n":"Tungurahua",           "co":"Ecuador",        "ty":"Stratovolcano",   "st":"Active",  "el":5023, "le":"2016",       "lo":"Andes, Ecuador",                     "fa":"Known as 'The Black Giant' or 'The Throat of Fire' in Quechua; has been in near-continuous eruption since 1999, forcing repeated evacuations of the city of Baños"},
    {"n":"Villarrica",           "co":"Chile",          "ty":"Stratovolcano",   "st":"Active",  "el":2847, "le":"2015",       "lo":"Araucanía Region, Chile",            "fa":"One of South America's most active volcanoes with one of the world's few continuously active lava lakes in its summit crater; a popular ski resort operates on its slopes"},
    {"n":"Calbuco",              "co":"Chile",          "ty":"Stratovolcano",   "st":"Active",  "el":2003, "le":"2015",       "lo":"Los Lagos Region, Chile",            "fa":"Considered one of Chile's most dangerous volcanoes; the 2015 eruption surprised scientists with no warning, producing a spectacular 15 km ash column that was broadcast live worldwide"},
    {"n":"Galeras",              "co":"Colombia",       "ty":"Stratovolcano",   "st":"Active",  "el":4276, "le":"2010",       "lo":"Nariño Department, Colombia",        "fa":"One of the most active volcanoes in South America, looming over the city of Pasto; in 1993 an eruption killed nine scientists who were inside the crater conducting research"},
    {"n":"Nevado del Ruiz",      "co":"Colombia",       "ty":"Stratovolcano",   "st":"Active",  "el":5321, "le":"2023",       "lo":"Caldas-Tolima border, Colombia",    "fa":"The 1985 eruption triggered a lahar that buried the town of Armero in 45 minutes, killing 23,000 people — the third deadliest volcanic disaster in recorded history"},
    # ── PACIFIC RING OF FIRE — ASIA & OCEANIA ─────────────────────────────────
    {"n":"Mount Fuji",           "co":"Japan",          "ty":"Stratovolcano",   "st":"Active",  "el":3776, "le":"1707",       "lo":"Honshu Island, Japan",               "fa":"Japan's iconic sacred mountain and highest peak; a UNESCO World Cultural Heritage Site that has inspired art for centuries; its 1707 eruption deposited ash on the city of Edo (Tokyo)"},
    {"n":"Sakurajima",           "co":"Japan",          "ty":"Stratovolcano",   "st":"Active",  "el":1117, "le":"2024",       "lo":"Kagoshima Bay, Kyushu",              "fa":"One of Japan's most active volcanoes, erupting hundreds of times a year; a 1914 eruption connected it to the mainland and its ash regularly blankets the nearby city of Kagoshima"},
    {"n":"Mount Unzen",          "co":"Japan",          "ty":"Lava Dome",       "st":"Active",  "el":1483, "le":"1996",       "lo":"Nagasaki Prefecture, Kyushu",        "fa":"Its 1991 eruption killed 43 people including the legendary volcanologists Katia and Maurice Krafft; its 1792 collapse triggered a megatsunami that killed 14,500 people"},
    {"n":"Aso",                  "co":"Japan",          "ty":"Caldera",         "st":"Active",  "el":1592, "le":"2023",       "lo":"Kumamoto Prefecture, Kyushu",        "fa":"One of the world's largest volcanic calderas, 25 km across, with over 50,000 people living inside it; has been continuously active for 270,000 years"},
    {"n":"Mount Merapi",         "co":"Indonesia",      "ty":"Stratovolcano",   "st":"Active",  "el":2930, "le":"2023",       "lo":"Java, Indonesia",                    "fa":"The most active and most dangerous volcano in Indonesia; located near Yogyakarta with 24 million people within 100 km; its lava dome collapses repeatedly, creating deadly pyroclastic flows"},
    {"n":"Mount Semeru",         "co":"Indonesia",      "ty":"Stratovolcano",   "st":"Active",  "el":3676, "le":"2024",       "lo":"East Java, Indonesia",               "fa":"The highest volcano on Java, producing small explosions roughly every 20 minutes; in Hindu mythology it is the god-king of all mountains and the 'cosmic axis' of the Earth"},
    {"n":"Sinabung",             "co":"Indonesia",      "ty":"Stratovolcano",   "st":"Active",  "el":2460, "le":"2021",       "lo":"Sumatra, Indonesia",                 "fa":"Dormant for 400 years before suddenly erupting in 2010; has been in near-continuous eruption since 2013, repeatedly destroying villages and causing massive displacement"},
    {"n":"Kelud",                "co":"Indonesia",      "ty":"Stratovolcano",   "st":"Active",  "el":1731, "le":"2014",       "lo":"East Java, Indonesia",               "fa":"One of Java's most deadly volcanoes; the 2014 eruption launched ash 27 km into the atmosphere, disrupting flights across Indonesia and forcing 100,000 people to evacuate"},
    {"n":"Lake Toba",            "co":"Indonesia",      "ty":"Supervolcano",    "st":"Dormant", "el":905,  "le":"74000 BC",   "lo":"Sumatra, Indonesia",                 "fa":"The largest volcanic eruption in the past 25 million years; the Toba catastrophe theory suggests it caused a volcanic winter that nearly drove humanity to extinction ~74,000 years ago"},
    {"n":"Ruapehu",              "co":"New Zealand",    "ty":"Stratovolcano",   "st":"Active",  "el":2797, "le":"2007",       "lo":"North Island, New Zealand",          "fa":"The largest active volcano in New Zealand; hosts several ski fields; its crater lake is among the world's most acidic (pH near zero); a 1953 lahar caused the deadly Tangiwai rail disaster"},
    {"n":"Tongariro",            "co":"New Zealand",    "ty":"Stratovolcano",   "st":"Active",  "el":1978, "le":"2012",       "lo":"North Island, New Zealand",          "fa":"A UNESCO World Heritage Site sacred to the Māori; its Ngauruhoe vent served as Mount Doom in Peter Jackson's Lord of the Rings trilogy"},
    {"n":"White Island (Whakaari)","co":"New Zealand",  "ty":"Stratovolcano",   "st":"Active",  "el":321,  "le":"2019",       "lo":"Bay of Plenty, New Zealand",         "fa":"New Zealand's most active cone volcano; accessible to tourists until December 2019 when a sudden eruption killed 22 visitors — a tragedy that reignited debate over volcanic tourism"},
    # ── AFRICA & INDIAN OCEAN ─────────────────────────────────────────────────
    {"n":"Nyiragongo",           "co":"DR Congo",       "ty":"Stratovolcano",   "st":"Active",  "el":3470, "le":"2021",       "lo":"Virunga Mountains, DRC",             "fa":"Contains one of the world's largest active lava lakes; its lava flows unusually fast — up to 100 km/h — due to low silica content; the 2002 eruption destroyed much of the city of Goma"},
    {"n":"Nyamuragira",          "co":"DR Congo",       "ty":"Shield Volcano",  "st":"Active",  "el":3058, "le":"2024",       "lo":"Virunga Mountains, DRC",             "fa":"Africa's most active volcano, erupting roughly every two years; its lava flows have devastated large areas of Virunga National Park, home to the critically endangered mountain gorilla"},
    {"n":"Ol Doinyo Lengai",     "co":"Tanzania",       "ty":"Stratovolcano",   "st":"Active",  "el":2962, "le":"2008",       "lo":"Rift Valley, Tanzania",              "fa":"The 'Mountain of God' in Maasai; the only active volcano erupting natrocarbonatite lava — a unique black lava so cool it's almost solid on extrusion, turning white within hours of contact with air"},
    {"n":"Erta Ale",             "co":"Ethiopia",       "ty":"Shield Volcano",  "st":"Active",  "el":613,  "le":"2019",       "lo":"Afar Depression, Ethiopia",          "fa":"One of only a handful of volcanoes with a persistent lava lake; located in the Danakil Depression, one of the hottest and most remote places on Earth, continuously active for over 100 years"},
    {"n":"Piton de la Fournaise","co":"France (Réunion)","ty":"Shield Volcano", "st":"Active",  "el":2632, "le":"2024",       "lo":"Réunion Island, Indian Ocean",       "fa":"One of the world's most active volcanoes, erupting roughly every 9 months; one of the most intensively monitored, providing scientists with a unique window into shield volcano dynamics"},
    # ── CARIBBEAN ─────────────────────────────────────────────────────────────
    {"n":"Mount Pelée",          "co":"Martinique",     "ty":"Stratovolcano",   "st":"Active",  "el":1394, "le":"1932",       "lo":"Martinique, Caribbean",              "fa":"The 1902 eruption was the deadliest of the 20th century; a pyroclastic flow destroyed the city of Saint-Pierre in minutes, killing all 30,000 of its inhabitants; only two people survived"},
    {"n":"Soufrière Hills",      "co":"Montserrat",     "ty":"Stratovolcano",   "st":"Active",  "el":1050, "le":"2010",       "lo":"Montserrat, Caribbean",              "fa":"Before 1995, dormant for over 350 years; its eruption buried the island's capital Plymouth in ash — creating a modern-day Pompeii, visible and still legally off-limits to visitors"},
    {"n":"La Soufrière (SVG)",   "co":"Saint Vincent",  "ty":"Stratovolcano",   "st":"Active",  "el":1234, "le":"2021",       "lo":"Saint Vincent, Caribbean",           "fa":"Its 2021 eruption was the most explosive in the Caribbean in decades, forcing evacuation of 16,000 people; its 1902 eruption killed 1,600 people on the same day as the Mount Pelée catastrophe"},
    # ── ATLANTIC & ARCTIC ─────────────────────────────────────────────────────
    {"n":"Teide (Canary Islands)","co":"Spain",         "ty":"Stratovolcano",   "st":"Active",  "el":3715, "le":"1909",       "lo":"Tenerife, Canary Islands",           "fa":"The most-visited national park in Spain and Europe; the third largest volcanic structure on Earth from base to summit; its dark summit above the clouds appears to 'float' at sunset"},
    {"n":"Fogo",                 "co":"Cape Verde",     "ty":"Stratovolcano",   "st":"Active",  "el":2829, "le":"2014",       "lo":"Fogo Island, Cape Verde",            "fa":"The most active volcano in the Atlantic Ocean; the entire island of Fogo was built by volcanic activity; the 2014-2015 eruption destroyed two towns inside the caldera"},
    {"n":"Beerenberg",           "co":"Norway",         "ty":"Stratovolcano",   "st":"Active",  "el":2277, "le":"1985",       "lo":"Jan Mayen Island, Arctic Ocean",     "fa":"The northernmost subaerial active volcano on Earth, located on the remote Norwegian Arctic island of Jan Mayen; its peak is permanently covered in glacial ice"},
    # ── CENTRAL ASIA & MIDDLE EAST ────────────────────────────────────────────
    {"n":"Damavand",             "co":"Iran",           "ty":"Stratovolcano",   "st":"Dormant", "el":5610, "le":"5350 BC",    "lo":"Alborz Mountains, Iran",             "fa":"The highest volcano in Asia and the highest peak in the Middle East; features prominently in Persian mythology as the prison of the evil king Zahhak, chained inside by Fereydoun"},
    {"n":"Ararat",               "co":"Turkey",         "ty":"Stratovolcano",   "st":"Dormant", "el":5137, "le":"1840",       "lo":"Eastern Anatolia, Turkey",           "fa":"The national symbol of Armenia and site where Noah's Ark supposedly came to rest according to biblical tradition; the 1840 eruption destroyed the village of Ahora and killed 1,900 people"},
    # ── ANTARCTICA & POLAR ────────────────────────────────────────────────────
    {"n":"Mount Erebus",         "co":"Antarctica",     "ty":"Stratovolcano",   "st":"Active",  "el":3794, "le":"2024",       "lo":"Ross Island, Antarctica",            "fa":"The world's southernmost active volcano and one of only a handful with a persistent lava lake; named after HMS Erebus, first sighted by James Clark Ross's expedition in 1841"},
    {"n":"Deception Island",     "co":"Antarctica",     "ty":"Caldera",         "st":"Active",  "el":576,  "le":"1970",       "lo":"South Shetland Islands",             "fa":"A horseshoe-shaped caldera open to the sea; ships can sail inside the caldera itself; had research stations that were destroyed by eruptions in 1967 and 1969"},
    # ── NOTABLE OTHERS ────────────────────────────────────────────────────────
    {"n":"Olympus Mons (Mars)",  "co":"Mars",           "ty":"Shield Volcano",  "st":"Dormant", "el":21900,"le":"25 Ma",      "lo":"Tharsis Plateau, Mars",              "fa":"The largest known volcano in the solar system at 21.9 km tall and 600 km wide — nearly three times the height of Everest; discovered by Mariner 9 in 1971"},
    {"n":"Marum",                "co":"Vanuatu",        "ty":"Stratovolcano",   "st":"Active",  "el":1270, "le":"2024",       "lo":"Ambrym Island, Vanuatu",             "fa":"Contains one of the most accessible active lava lakes in the world; its twin lava lakes on Ambrym Island are continuously active and visited by adventurous volcanologists"},
    {"n":"Yasur",                "co":"Vanuatu",        "ty":"Stratovolcano",   "st":"Active",  "el":361,  "le":"2024",       "lo":"Tanna Island, Vanuatu",              "fa":"One of the world's most accessible active volcanoes; islanders have worshipped at the erupting crater for centuries; Captain James Cook noted its glow from the sea in 1774"},
    {"n":"Wrangell",             "co":"USA",            "ty":"Shield Volcano",  "st":"Active",  "el":4317, "le":"1900",       "lo":"Alaska, Wrangell-St. Elias NP",     "fa":"One of the world's largest volcanoes by volume; its summit crater contains a large geothermal hot spot that keeps it ice-free and is clearly visible from satellites"},
    {"n":"Shishaldin",           "co":"USA",            "ty":"Stratovolcano",   "st":"Active",  "el":2857, "le":"2023",       "lo":"Unimak Island, Aleutian Islands",    "fa":"The tallest peak in the Aleutian Islands with one of the most symmetrical cones of any volcano in the world; has erupted over 50 times since 1775"},
    {"n":"Augustine",            "co":"USA",            "ty":"Stratovolcano",   "st":"Active",  "el":1252, "le":"2006",       "lo":"Cook Inlet, Alaska",                 "fa":"One of Alaska's most historically active volcanoes; its 2006 eruption sent ash to 15 km altitude and was studied extensively by NASA to improve satellite detection of volcanic plumes"},
    {"n":"Nevado del Huila",     "co":"Colombia",       "ty":"Stratovolcano",   "st":"Active",  "el":5364, "le":"2012",       "lo":"Huila Department, Colombia",         "fa":"Colombia's highest peak; its rare eruptions in 2007-2008 triggered massive lahars down the Páez River, killing over 10 people and displacing tens of thousands"},
    {"n":"Láscar",               "co":"Chile",          "ty":"Stratovolcano",   "st":"Active",  "el":5592, "le":"2024",       "lo":"Atacama Desert, Chile",              "fa":"The most active volcano in the Central Andes; its 1993 eruption produced a 25 km high column visible from Buenos Aires; it rises dramatically from one of the driest places on Earth"},
    {"n":"Ojos del Salado",      "co":"Chile/Argentina","ty":"Stratovolcano",   "st":"Dormant", "el":6893, "le":"700 AD",     "lo":"Atacama, Andes border",              "fa":"The world's highest active volcano at 6,893 m and the highest peak in Chile; has a small summit crater lake — the world's highest lake — fed by snowmelt and occasional fumarolic activity"},
    {"n":"Hunga Tonga",          "co":"Tonga",          "ty":"Submarine",       "st":"Active",  "el":-150, "le":"2022",       "lo":"South Pacific Ocean, Tonga",         "fa":"The 2022 eruption was one of the most powerful in a century, generating a tsunami that circled the globe multiple times and producing a sonic boom heard 10,000 km away in Alaska"},
    {"n":"Veniaminof",           "co":"USA",            "ty":"Stratovolcano",   "st":"Active",  "el":2507, "le":"2021",       "lo":"Alaska Peninsula, Alaska",           "fa":"Has one of the largest calderas in the Aleutians; a small intracaldera cone with an active lava lake has been erupting continuously for years inside the ice-filled summit caldera"},
    {"n":"Long Valley Caldera",  "co":"USA",            "ty":"Supervolcano",    "st":"Active",  "el":2550, "le":"200 AD",     "lo":"Eastern California",                 "fa":"A supervolcano formed 760,000 years ago in an eruption 2,000 times larger than Mount St. Helens; the nearby Mammoth Mountain ski resort is built on a dormant flank vent"},
    {"n":"Avachinsky",           "co":"Russia",         "ty":"Stratovolcano",   "st":"Active",  "el":2741, "le":"2001",       "lo":"Kamchatka Peninsula, Russia",        "fa":"One of the most active volcanoes on the Kamchatka Peninsula, with over 20 eruptions in the last 250 years; looms dramatically over Petropavlovsk-Kamchatsky, Russia's most volcanically threatened city"},
    {"n":"Klyuchevskaya Sopka",  "co":"Russia",         "ty":"Stratovolcano",   "st":"Active",  "el":4754, "le":"2024",       "lo":"Kamchatka Peninsula, Russia",        "fa":"The highest active volcano in Eurasia and one of the world's most active; has erupted almost continuously since 1697; it ejects enormous quantities of lava, often visible from the International Space Station"},
    {"n":"Shiveluch",            "co":"Russia",         "ty":"Stratovolcano",   "st":"Active",  "el":3283, "le":"2024",       "lo":"Kamchatka Peninsula, Russia",        "fa":"One of the most active volcanoes on Kamchatka; its May 2023 eruption was its largest in 60 years, sending an ash cloud to 20 km altitude and depositing a thick layer of ash on villages"},
    {"n":"Pinatubo (post-1991)", "co":"Philippines",    "ty":"Stratovolcano",   "st":"Active",  "el":1486, "le":"1993",       "lo":"Luzon Island, Philippines",          "fa":"After lying dormant for 500 years, the 1991 eruption was the largest since Katmai 1912; it inspired a global response that became the template for monitoring and evacuating before major eruptions"},
]

HEADERS = {"User-Agent": "projet_app_annecdote/1.0 (daily-facts educational app; github.com/uzan)"}

WIKI_TITLE_OVERRIDES = {
    "Krakatoa":              "Krakatoa",
    "Santorini (Thera)":     "Santorini",
    "Mount Teide":           "Teide",
    "Teide (Canary Islands)":"Teide",
    "Kīlauea":               "Kīlauea",
    "La Soufrière (SVG)":    "La Soufrière (Saint Vincent)",
    "Soufrière Hills":       "Soufrière Hills",
    "Olympus Mons (Mars)":   "Olympus Mons",
    "Pinatubo (post-1991)":  "Mount Pinatubo",
    "White Island (Whakaari)":"Whakaari / White Island",
}

def fetch_wiki_image(volcano_name, size=500):
    title = WIKI_TITLE_OVERRIDES.get(volcano_name, volcano_name)
    for attempt in range(4):
        delay = 2 ** attempt  # 1s, 2s, 4s, 8s
        if attempt > 0:
            print(f"  [retry {attempt}] waiting {delay}s …")
            time.sleep(delay)
        try:
            r = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={"action":"query","titles":title,"prop":"pageimages",
                        "format":"json","pithumbsize":size},
                headers=HEADERS,
                timeout=15,
            )
            if not r.text.strip():
                continue  # empty response, retry
            pages = r.json()["query"]["pages"]
            page  = next(iter(pages.values()))
            return page.get("thumbnail", {}).get("source")
        except Exception as e:
            if attempt == 3:
                print(f"  [warn] {volcano_name}: {e}")
    return None

def fetch_commons_image(query, size=500):
    try:
        r = requests.get(
            "https://commons.wikimedia.org/w/api.php",
            params={"action":"query","generator":"search","gsrsearch":query,
                    "gsrnamespace":6,"prop":"imageinfo","iiprop":"url",
                    "iiurlwidth":size,"format":"json","gsrlimit":5},
            headers=HEADERS, timeout=15,
        )
        if not r.text.strip():
            return None
        pages = r.json().get("query", {}).get("pages", {})
        for page in sorted(pages.values(), key=lambda p: p.get("index", 99)):
            info = page.get("imageinfo", [])
            if info:
                url = info[0].get("thumburl") or info[0].get("url")
                if url and ".svg" not in url.lower():
                    return url
    except Exception:
        pass
    return None

output_path = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../../assets/science/volcanoes.json")
)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Load existing JSON to preserve already-fetched images
existing_images = {}
if os.path.exists(output_path):
    with open(output_path, encoding="utf-8") as f:
        for entry in json.load(f):
            if entry.get("im"):
                existing_images[entry["n"]] = entry["im"]
    print(f"Loaded {len(existing_images)} existing images from cache.\n")

volcanoes = []
missing = sum(1 for v in VOLCANOES_RAW if not existing_images.get(v["n"]))
print(f"{missing} volcano(es) need image fetching.\n")
fetch_idx = 0
for i, v in enumerate(VOLCANOES_RAW, 1):
    name = v["n"]
    if existing_images.get(name):
        im = existing_images[name]
        print(f"[{i:2}/{len(VOLCANOES_RAW)}] {name} (cached)")
    else:
        fetch_idx += 1
        print(f"[{i:2}/{len(VOLCANOES_RAW)}] Fetching image for {name} …")
        im = fetch_wiki_image(name)
        if im is None:
            im = fetch_commons_image(f"{name} volcano")
            if im:
                print(f"  [commons] found")
        if fetch_idx < missing:
            time.sleep(1.0)  # 1s between new fetches
    volcanoes.append({**v, "im": im})

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(volcanoes, f, ensure_ascii=False, separators=(",", ":"))

fetched = sum(1 for v in volcanoes if v["im"])
print(f"\nDone -- {len(volcanoes)} volcanoes, {fetched} with images -> {output_path}")
