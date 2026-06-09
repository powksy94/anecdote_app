import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=name, ar=artist, yr=year, ma=material, lo=location, st=style, fa=famous_for, im=imageUrl

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_EN = {
    "Venus de Milo":                        "Venus de Milo",
    "Winged Victory of Samothrace":         "Winged Victory of Samothrace",
    "Laocoön and His Sons":                 "Laocoön and His Sons",
    "Discobolus":                           "Discobolus",
    "Doryphoros":                           "Doryphoros",
    "Charioteer of Delphi":                 "Charioteer of Delphi",
    "Augustus of Prima Porta":              "Augustus of Prima Porta",
    "Capitoline Wolf":                      "Capitoline Wolf",
    "Artemision Bronze":                    "Artemision Bronze",
    "Hermes and the Infant Dionysus":       "Hermes and the Infant Dionysus",
    "Dying Gaul":                           "Dying Gaul",
    "Farnese Hercules":                     "Farnese Hercules",
    "Apoxyomenos":                          "Apoxyomenos",
    "Nefertiti Bust":                       "Nefertiti bust",
    "Terracotta Army":                      "Terracotta Army",
    "Easter Island Moai":                   "Moai",
    "Olmec Colossal Head":                  "Olmec colossal heads",
    "Seated Scribe":                        "Seated scribe (Louvre)",
    "Venus of Willendorf":                  "Venus of Willendorf",
    "David (Michelangelo)":                 "David (Michelangelo)",
    "Pietà":                                "Pietà (Michelangelo)",
    "Moses (Michelangelo)":                 "Moses (Michelangelo)",
    "Bacchus (Michelangelo)":               "Bacchus (Michelangelo)",
    "Dying Slave":                          "Dying Slave",
    "David (Donatello)":                    "David (Donatello)",
    "Gattamelata":                          "Equestrian statue of Gattamelata",
    "Penitent Magdalene (Donatello)":       "Mary Magdalene (Donatello)",
    "Gates of Paradise":                    "Gates of Paradise (Ghiberti)",
    "Perseus with the Head of Medusa":      "Perseus with the Head of Medusa",
    "Three Graces (Canova)":               "The Three Graces (Canova)",
    "Psyche Revived by Cupid's Kiss":       "Psyche Revived by Cupid's Kiss",
    "David (Bernini)":                      "David (Bernini)",
    "Ecstasy of Saint Teresa":              "Ecstasy of Saint Teresa",
    "Apollo and Daphne":                    "Apollo and Daphne (Bernini)",
    "The Rape of Proserpina":               "The Rape of Proserpina (Bernini)",
    "Houdon's Voltaire":                    "Seated Voltaire",
    "Lion of Lucerne":                      "Lion Monument",
    "The Thinker":                          "The Thinker",
    "The Kiss (Rodin)":                     "The Kiss (Rodin)",
    "The Burghers of Calais":               "The Burghers of Calais",
    "Gates of Hell":                        "Gates of Hell",
    "Monument to Balzac":                   "Monument to Balzac",
    "The Little Mermaid":                   "The Little Mermaid (statue)",
    "Little Dancer of Fourteen Years":      "Little Dancer of Fourteen Years",
    "The Kiss (Brancusi)":                  "The Kiss (Brâncuși)",
    "Bird in Space":                        "Bird in Space",
    "Endless Column":                       "Endless Column",
    "Sleeping Muse":                        "Sleeping Muse",
    "Unique Forms of Continuity in Space":  "Unique Forms of Continuity in Space",
    "Walking Man I":                        "Walking Man I",
    "Man Pointing":                         "Man Pointing",
    "City Square":                          "City Square (Giacometti)",
    "Reclining Figure":                     "Reclining Figure (Moore)",
    "Nuclear Energy":                       "Nuclear Energy (sculpture)",
    "Lobster Trap and Fish Tail":           "Lobster Trap and Fish Tail",
    "Bicycle Wheel":                        "Bicycle Wheel",
    "She-Goat":                             "La Chèvre (Picasso)",
    "Tilted Arc":                           "Tilted Arc",
    "Angel of the North":                   "Angel of the North",
    "Cloud Gate":                           "Cloud Gate",
    "Balloon Dog":                          "Balloon Dog",
    "Maman":                                "Maman (sculpture)",
    "The Physical Impossibility of Death":  "The Physical Impossibility of Death in the Mind of Someone Living",
    "Marsyas (Kapoor)":                     "Marsyas (Kapoor)",
    "Statue of Liberty":                    "Statue of Liberty",
    "Christ the Redeemer":                  "Christ the Redeemer",
    "Great Sphinx of Giza":                 "Great Sphinx of Giza",
    "Manneken Pis":                         "Manneken Pis",
    "Trevi Fountain":                       "Trevi Fountain",
}

sculptures = [
    # ── Antiquité égyptienne & préhistorique ────────────────────────────────
    {"n":"Nefertiti Bust","ar":"Thutmose","yr":"~1345 BC","ma":"Limestone, stucco","lo":"Neues Museum, Berlin","st":"Ancient Egyptian","fa":"Found in 1912 by a German expedition; Egypt has demanded its return ever since. The painted left eye was intentionally left blank — scholars still debate why"},
    {"n":"Seated Scribe","ar":"Unknown Egyptian","yr":"~2500 BC","ma":"Painted limestone","lo":"Louvre Museum, Paris","st":"Old Kingdom Egypt","fa":"One of the most vivid faces from the ancient world; its inlaid quartz eyes still seem alert after 4,500 years — visitors report feeling watched"},
    {"n":"Venus of Willendorf","ar":"Unknown","yr":"~25,000 BC","ma":"Limestone","lo":"Naturhistorisches Museum, Vienna","st":"Paleolithic","fa":"One of the oldest known sculptures at just 11 cm tall; its exaggerated form suggests a fertility symbol — possibly the earliest surviving work of art"},
    {"n":"Great Sphinx of Giza","ar":"Unknown Egyptian artists","yr":"~2500 BC","ma":"Limestone","lo":"Giza, Egypt","st":"Ancient Egyptian","fa":"The largest monolith statue in the world at 73 meters long; the missing nose was blamed on Napoleon's soldiers but drawings from 1737 already show it broken"},
    {"n":"Terracotta Army","ar":"Unknown Qin artisans","yr":"~210 BC","ma":"Terracotta","lo":"Xi'an, China","st":"Ancient Chinese","fa":"Over 8,000 soldiers each with a unique face; accidentally discovered in 1974 by farmers digging a well — the artisans were reportedly entombed alive to keep the secret"},
    {"n":"Easter Island Moai","ar":"Rapa Nui people","yr":"1250-1500 AD","ma":"Volcanic tuff","lo":"Easter Island, Chile","st":"Polynesian","fa":"The 1,000 moai were 'walked' upright using ropes — proven experimentally in 2012; the largest weighs 82 tonnes and was never successfully erected"},
    {"n":"Olmec Colossal Head","ar":"Olmec civilization","yr":"~900 BC","ma":"Basalt","lo":"Villahermosa, Mexico","st":"Olmec","fa":"The 17 known heads weigh up to 40 tonnes and were carved without metal tools; the nearest basalt source is 150 km away — transport remains a mystery"},
    # ── Antiquité grecque & romaine ────────────────────────────────────────
    {"n":"Venus de Milo","ar":"Unknown Greek sculptor","yr":"~100 BC","ma":"Marble","lo":"Louvre Museum, Paris","st":"Hellenistic","fa":"The most famous ancient Greek statue; its missing arms have been debated for two centuries — some believe she held a shield or an apple"},
    {"n":"Winged Victory of Samothrace","ar":"Unknown Greek sculptor","yr":"~190 BC","ma":"Marble","lo":"Louvre Museum, Paris","st":"Hellenistic","fa":"Considered the greatest surviving work of Hellenistic sculpture; Nike landing on a ship's prow, wings still spread in triumphant flight"},
    {"n":"Laocoön and His Sons","ar":"Agesander, Athenodoros, Polydorus","yr":"~25 BC","ma":"Marble","lo":"Vatican Museums","st":"Hellenistic","fa":"Called the 'prototype of human anguish in art' by Michelangelo; depicts the Trojan priest and his sons strangled by sea serpents"},
    {"n":"Discobolus","ar":"Myron","yr":"~450 BC","ma":"Bronze (lost) / Marble copy","lo":"National Museum of Rome","st":"Classical","fa":"The discus thrower frozen at the peak of his throw — one of the first works to capture dynamic movement rather than static pose"},
    {"n":"Doryphoros","ar":"Polykleitos","yr":"~440 BC","ma":"Bronze (lost) / Marble copy","lo":"National Archaeological Museum, Naples","st":"Classical","fa":"The 'Canon' — Polykleitos's mathematical ideal of perfect human proportions, so influential it was called 'The Rule' across Greece"},
    {"n":"Charioteer of Delphi","ar":"Unknown","yr":"~478 BC","ma":"Bronze","lo":"Delphi Archaeological Museum","st":"Early Classical","fa":"One of the best-preserved bronze statues from antiquity; the inlaid glass-and-copper eyes still glint as if alive after 2,500 years"},
    {"n":"Augustus of Prima Porta","ar":"Unknown Roman sculptor","yr":"~20 BC","ma":"Marble","lo":"Vatican Museums","st":"Roman Imperial","fa":"The definitive portrait of Roman imperial power; Cupid riding a dolphin at his feet hints at Augustus's divine descent from Venus"},
    {"n":"Capitoline Wolf","ar":"Unknown Etruscan/Roman","yr":"5th century BC","ma":"Bronze","lo":"Capitoline Museums, Rome","st":"Etruscan","fa":"The symbol of Rome: the she-wolf suckling Romulus and Remus; modern analysis shows the twins were added in the 15th century by Renaissance sculptors"},
    {"n":"Artemision Bronze","ar":"Unknown","yr":"~460 BC","ma":"Bronze","lo":"National Archaeological Museum, Athens","st":"Early Classical","fa":"Found at sea in 1928; scholars debate whether the arm hurls a thunderbolt (Zeus) or a trident (Poseidon) — the god's identity remains unknown"},
    {"n":"Hermes and the Infant Dionysus","ar":"Praxiteles","yr":"~330 BC","ma":"Marble","lo":"Archaeological Museum of Olympia","st":"Classical","fa":"The first major Greek sculpture showing gods with human emotion; Hermes teases the infant Dionysus with grapes — and the child reaches for them"},
    {"n":"Dying Gaul","ar":"Unknown (Pergamon school)","yr":"~230 BC","ma":"Marble (Roman copy)","lo":"Capitoline Museums, Rome","st":"Hellenistic","fa":"A powerful expression of dignity in defeat; the wounded warrior chooses to die with honor — Romantic poets wrote elegies to him"},
    {"n":"Farnese Hercules","ar":"Glycon of Athens","yr":"3rd century AD (copy)","ma":"Marble","lo":"National Archaeological Museum, Naples","st":"Roman (Hellenistic copy)","fa":"The massive hero leans exhausted on his club after the Labors; the apples of the Hesperides hidden behind his back show the final task is done"},
    {"n":"Apoxyomenos","ar":"Lysippos","yr":"~330 BC","ma":"Bronze (lost) / Marble copy","lo":"Vatican Museums","st":"Late Classical","fa":"An athlete scraping oil and dust from his arm; Lysippos introduced a new body canon — seven-and-a-half head heights — that endured for centuries"},
    # ── Renaissance ────────────────────────────────────────────────────────
    {"n":"David (Michelangelo)","ar":"Michelangelo","yr":"1501-1504","ma":"Marble","lo":"Galleria dell'Accademia, Florence","st":"Renaissance","fa":"At 5.17 meters, David is shown not after victory but before battle — tense, calculating, ready. The defining image of the Renaissance ideal of human potential"},
    {"n":"Pietà","ar":"Michelangelo","yr":"1498-1499","ma":"Marble","lo":"St. Peter's Basilica, Vatican","st":"Renaissance","fa":"Michelangelo's only signed work, completed at 24; the serenity of Mary's face holding the dead Christ has moved viewers to tears for 500 years"},
    {"n":"Moses (Michelangelo)","ar":"Michelangelo","yr":"1513-1515","ma":"Marble","lo":"San Pietro in Vincoli, Rome","st":"Renaissance","fa":"So lifelike that Michelangelo struck the knee demanding 'Why dost thou not speak?'; the horns are from a mistranslation of 'rays of light' in the Bible"},
    {"n":"Bacchus (Michelangelo)","ar":"Michelangelo","yr":"1496-1497","ma":"Marble","lo":"Bargello Museum, Florence","st":"Renaissance","fa":"Michelangelo's first large-scale work, made at 21; Bacchus's slightly tilted stance and unfocused gaze perfectly convey inebriation in stone"},
    {"n":"Dying Slave","ar":"Michelangelo","yr":"1513-1516","ma":"Marble","lo":"Louvre Museum, Paris","st":"Renaissance","fa":"Intended for Pope Julius II's tomb; the sensual figure surrenders to death — or sleep — in one of history's most serene depictions of dying"},
    {"n":"David (Donatello)","ar":"Donatello","yr":"~1440-1460","ma":"Bronze","lo":"Bargello Museum, Florence","st":"Early Renaissance","fa":"The first freestanding nude male statue since antiquity; shown after the battle — serene, hat shading a knowing smile, Goliath's head at his feet"},
    {"n":"Gattamelata","ar":"Donatello","yr":"1453","ma":"Bronze","lo":"Piazza del Santo, Padua","st":"Renaissance","fa":"The first life-size equestrian bronze since antiquity; the mercenary commander's calm face radiates authority — Donatello studied Roman imperial sculpture to achieve it"},
    {"n":"Penitent Magdalene (Donatello)","ar":"Donatello","yr":"~1453-1455","ma":"Polychrome wood","lo":"Museo dell'Opera del Duomo, Florence","st":"Late Gothic / Renaissance","fa":"Shockingly realistic: a gaunt, wild-haired woman in rags; completely unlike ideal Renaissance beauty — a direct emotional confrontation with mortality and sin"},
    {"n":"Gates of Paradise","ar":"Lorenzo Ghiberti","yr":"1425-1452","ma":"Gilded bronze","lo":"Museo dell'Opera del Duomo, Florence","st":"Renaissance","fa":"Michelangelo called them worthy of being the Gates of Paradise; 27 years of work in 10 gilded panels that established perspective relief sculpture for two centuries"},
    {"n":"Perseus with the Head of Medusa","ar":"Benvenuto Cellini","yr":"1545-1554","ma":"Bronze","lo":"Loggia dei Lanzi, Florence","st":"Mannerist","fa":"Cast in a single night in a dramatic furnace crisis Cellini described in his autobiography; Michelangelo declared it the most beautiful work in the piazza"},
    # ── Baroque ────────────────────────────────────────────────────────────
    {"n":"David (Bernini)","ar":"Gian Lorenzo Bernini","yr":"1623-1624","ma":"Marble","lo":"Borghese Gallery, Rome","st":"Baroque","fa":"Unlike Donatello's or Michelangelo's, Bernini's David is caught mid-action — the sling swings, the jaw clenches; Bernini used his own face, biting his lip"},
    {"n":"Ecstasy of Saint Teresa","ar":"Gian Lorenzo Bernini","yr":"1647-1652","ma":"Marble","lo":"Santa Maria della Vittoria, Rome","st":"Baroque","fa":"The angel's smile and Teresa's upturned face create an ambiguity between spiritual ecstasy and earthly rapture that shocked and fascinated in equal measure"},
    {"n":"Apollo and Daphne","ar":"Gian Lorenzo Bernini","yr":"1622-1625","ma":"Marble","lo":"Borghese Gallery, Rome","st":"Baroque","fa":"Bernini captured the impossible: the exact instant Daphne's fingers sprout leaves and her skin becomes bark — all in cold marble"},
    {"n":"The Rape of Proserpina","ar":"Gian Lorenzo Bernini","yr":"1621-1622","ma":"Marble","lo":"Borghese Gallery, Rome","st":"Baroque","fa":"Pluto's fingers visibly compress Proserpina's thigh — visitors refuse to believe it is stone; carved when Bernini was just 23 years old"},
    # ── XVIIe-XVIIIe siècle ────────────────────────────────────────────────
    {"n":"Three Graces (Canova)","ar":"Antonio Canova","yr":"1814-1817","ma":"Marble","lo":"V&A Museum, London / Hermitage, St. Petersburg","st":"Neoclassical","fa":"Two versions exist; when Britain and Russia both claimed ownership, Canova carved a second — the dispute over which is 'better' continues among scholars"},
    {"n":"Psyche Revived by Cupid's Kiss","ar":"Antonio Canova","yr":"1787-1793","ma":"Marble","lo":"Louvre Museum, Paris","st":"Neoclassical","fa":"The arms of Cupid form a perfect diamond; Napoleon acquired it for himself — Canova had to carve a second version for the original patron"},
    {"n":"Houdon's Voltaire","ar":"Jean-Antoine Houdon","yr":"1781","ma":"Marble","lo":"Comédie-Française, Paris","st":"Neoclassical","fa":"Carved when Voltaire was 83 and dying; the philosopher's ironic smile, hooded gaze, and enormous wig form the defining image of the Enlightenment"},
    {"n":"Lion of Lucerne","ar":"Bertel Thorvaldsen","yr":"1820-1821","ma":"Sandstone (rock relief)","lo":"Lucerne, Switzerland","st":"Neoclassical","fa":"Mark Twain called it 'the most mournful and moving piece of stone in the world'; it memorializes 786 Swiss Guards massacred defending Louis XVI in 1792"},
    # ── XIXe siècle ──────────────────────────────────────────────────────────
    {"n":"The Thinker","ar":"Auguste Rodin","yr":"1880-1902","ma":"Bronze","lo":"Musée Rodin, Paris (+ 28 casts)","st":"Realism","fa":"Originally conceived as Dante contemplating Hell for the Gates of Hell; now a universal symbol of philosophy, introspection, and human thought"},
    {"n":"The Kiss (Rodin)","ar":"Auguste Rodin","yr":"1882","ma":"Marble/Bronze","lo":"Musée Rodin, Paris","st":"Realism","fa":"The couple are frozen at the moment before their first kiss — they never actually touch. Inspired by Paolo and Francesca from Dante's Inferno"},
    {"n":"The Burghers of Calais","ar":"Auguste Rodin","yr":"1884-1889","ma":"Bronze","lo":"Calais (+ multiple casts)","st":"Realism","fa":"Rodin refused a pedestal — he wanted the six citizens at street level, among the people. The city insisted on a base; he never forgave them"},
    {"n":"Gates of Hell","ar":"Auguste Rodin","yr":"1880-1917 (unfinished)","ma":"Bronze","lo":"Musée Rodin, Paris","st":"Realism","fa":"A commission that consumed 37 years; contains over 180 figures including early versions of The Thinker and The Kiss. Never formally completed"},
    {"n":"Monument to Balzac","ar":"Auguste Rodin","yr":"1891-1898","ma":"Bronze","lo":"Boulevard du Montparnasse, Paris","st":"Expressionist","fa":"Rejected as scandalous in 1898; the novelist is a massive cloaked form — a force of nature, not a man. Now considered a proto-modern masterpiece"},
    {"n":"The Little Mermaid","ar":"Edvard Eriksen","yr":"1913","ma":"Bronze","lo":"Langelinie pier, Copenhagen","st":"Romantic","fa":"One of the world's most visited (and most attacked) sculptures — beheaded, painted, and blown up multiple times; still sits quietly on her rock"},
    {"n":"Little Dancer of Fourteen Years","ar":"Edgar Degas","yr":"1881","ma":"Bronze (original: wax)","lo":"Musée d'Orsay, Paris","st":"Impressionism","fa":"The only sculpture Degas exhibited in his lifetime; shown with real hair and a tutu, it shocked the art world — critics called it 'a wax doll' and 'a zoo specimen'"},
    # ── XXe siècle - Modernisme ──────────────────────────────────────────────
    {"n":"The Kiss (Brancusi)","ar":"Constantin Brâncuși","yr":"1907-1908","ma":"Stone","lo":"Montparnasse Cemetery, Paris","st":"Modernism","fa":"A total rejection of Rodin's sensuous style: two embracing figures reduced to geometric essentials — the lovers barely distinguishable from the block itself"},
    {"n":"Bird in Space","ar":"Constantin Brâncuși","yr":"1928","ma":"Bronze","lo":"MoMA, New York","st":"Modernism","fa":"US customs refused to classify it as art and taxed it as industrial metal; Brâncuși won the lawsuit — a landmark case for abstract art"},
    {"n":"Sleeping Muse","ar":"Constantin Brâncuși","yr":"1910","ma":"Bronze","lo":"Hirshhorn Museum, Washington D.C.","st":"Modernism","fa":"A sleeping head reduced to an oval — all features dissolved into the smooth curve of a dream; influenced a generation of abstract sculptors worldwide"},
    {"n":"Endless Column","ar":"Constantin Brâncuși","yr":"1938","ma":"Cast iron","lo":"Târgu Jiu, Romania","st":"Modernism","fa":"At 29.35 meters, his tallest work; meant to honor Romanian WWI soldiers and support the sky — he called it 'a staircase to heaven'"},
    {"n":"Bicycle Wheel","ar":"Marcel Duchamp","yr":"1913","ma":"Bicycle wheel, stool","lo":"MoMA, New York (replica)","st":"Dada","fa":"The first 'readymade' — Duchamp simply mounted a bicycle wheel on a stool. It changed the definition of art: the concept matters, not craft"},
    {"n":"Unique Forms of Continuity in Space","ar":"Umberto Boccioni","yr":"1913","ma":"Bronze","lo":"MoMA, New York","st":"Futurism","fa":"The defining work of Italian Futurism; a figure dissolving into speed and motion — it appears on the Italian 20-cent euro coin"},
    {"n":"Reclining Figure","ar":"Henry Moore","yr":"1951","ma":"Bronze","lo":"Various (multiple casts)","st":"Abstract","fa":"Moore created dozens of reclining figures throughout his life; the horizontal body echoing landscape became his signature obsession — over 30 versions in total"},
    {"n":"Nuclear Energy","ar":"Henry Moore","yr":"1967","ma":"Bronze","lo":"University of Chicago","st":"Abstract","fa":"Placed on the exact spot where the world's first nuclear reactor went critical in 1942; the form simultaneously evokes a skull, a mushroom cloud, and a cathedral dome"},
    {"n":"Lobster Trap and Fish Tail","ar":"Alexander Calder","yr":"1939","ma":"Painted steel wire, sheet aluminum","lo":"MoMA, New York","st":"Kinetic Art","fa":"The first commissioned mobile in MoMA's permanent collection; each element shifts in air currents creating an ever-changing composition — no two moments are the same"},
    {"n":"Walking Man I","ar":"Alberto Giacometti","yr":"1960","ma":"Bronze","lo":"Multiple collections","st":"Existentialism","fa":"The archetypal lone figure of post-war existential art; its elongated roughness conveys the isolation of modern existence. Sold for $104.3M in 2010"},
    {"n":"Man Pointing","ar":"Alberto Giacometti","yr":"1947","ma":"Bronze","lo":"MoMA, New York","st":"Existentialism","fa":"A solitary figure gestures into the void — Giacometti's response to the existential crisis of post-WWII Europe; sold for $141.3M at Christie's in 2015"},
    {"n":"City Square","ar":"Alberto Giacometti","yr":"1948-1949","ma":"Bronze","lo":"MoMA, New York","st":"Existentialism","fa":"Five tiny figures cross a vast plaza without interacting; the immense negative space between them defines loneliness as powerfully as any painting"},
    {"n":"She-Goat","ar":"Pablo Picasso","yr":"1950","ma":"Bronze","lo":"MoMA, New York","st":"Assemblage","fa":"The internal structure uses a palm frond, ceramic jugs, and scrap metal; Picasso found beauty in junk and cast it in bronze — the process became the meaning"},
    {"n":"Tilted Arc","ar":"Richard Serra","yr":"1981","ma":"Corten steel","lo":"Federal Plaza, New York (removed 1989)","st":"Minimalism","fa":"A 36-meter curved steel wall generated the most famous public-art controversy in American history — leading to a public hearing and its forced removal in 1989"},
    # ── Art contemporain ──────────────────────────────────────────────────────
    {"n":"Angel of the North","ar":"Antony Gormley","yr":"1998","ma":"Steel","lo":"Gateshead, UK","st":"Contemporary","fa":"With a 54-meter wingspan, wider than a Boeing 757; seen by more than one person per second — roughly 33 million people per year passing on the nearby A1 road"},
    {"n":"Cloud Gate","ar":"Anish Kapoor","yr":"2006","ma":"Stainless steel","lo":"Millennium Park, Chicago","st":"Contemporary","fa":"Nicknamed 'The Bean' by Chicagoans; 110 tonnes of steel with no visible seams — its surface reflects and distorts city and visitors in one continuous liquid mirror"},
    {"n":"Marsyas (Kapoor)","ar":"Anish Kapoor","yr":"2002","ma":"PVC membrane, steel","lo":"Tate Modern (Turbine Hall)","st":"Contemporary","fa":"A 155-meter red membrane filled the Tate's Turbine Hall; named after the satyr flayed alive by Apollo — the skin of the mythological victim stretched enormous"},
    {"n":"Balloon Dog","ar":"Jeff Koons","yr":"1994-2000","ma":"Mirror-polished steel","lo":"Multiple collections","st":"Pop Art","fa":"The Orange version sold for $58.4M in 2013, then a record for a living artist; the balloon animal elevated to monumental scale questions the nature of high art"},
    {"n":"The Physical Impossibility of Death","ar":"Damien Hirst","yr":"1991","ma":"Tiger shark, formaldehyde, glass, steel","lo":"The Met (Broad Art Foundation)","st":"YBA","fa":"A 4.3-meter tiger shark in formaldehyde; the original decayed and had to be replaced in 2006 — raising philosophical questions about what collectors actually own"},
    {"n":"Maman","ar":"Louise Bourgeois","yr":"1999","ma":"Bronze, marble, stainless steel","lo":"Tate Modern, London (+ others)","st":"Contemporary","fa":"A 9-meter spider guarding an egg sac; Bourgeois created it as a tribute to her mother: 'My best friend was my mother — as intelligent, patient, and helpful as a spider'"},
    # ── Monuments emblématiques ────────────────────────────────────────────
    {"n":"Statue of Liberty","ar":"Frédéric Auguste Bartholdi","yr":"1886","ma":"Copper (on steel frame)","lo":"Liberty Island, New York","st":"Neoclassical","fa":"A gift from France; the torch arm was displayed at the Philadelphia Centennial (1876) to raise funds — visitors paid 50 cents to climb inside"},
    {"n":"Christ the Redeemer","ar":"Paul Landowski","yr":"1931","ma":"Reinforced concrete, soapstone","lo":"Corcovado, Rio de Janeiro","st":"Art Deco","fa":"Voted one of the Seven Wonders of the Modern World; struck by lightning multiple times but considered miraculous by locals — 38 meters tall, arms spanning 28 meters"},
    {"n":"Manneken Pis","ar":"Jérôme Duquesnoy","yr":"1619","ma":"Bronze","lo":"Brussels, Belgium","st":"Baroque","fa":"The 55-cm bronze boy has over 1,000 costume changes logged in a register; cities worldwide send outfits as diplomatic gifts — the wardrobe has its own museum wing"},
    {"n":"Trevi Fountain","ar":"Nicola Salvi","yr":"1762","ma":"Travertine marble","lo":"Rome, Italy","st":"Baroque","fa":"Coins thrown in are collected nightly — roughly €1.5 million per year, donated to a charity for the poor. The 1954 film Three Coins in the Fountain started the tradition"},
    # ── Autres chefs-d'œuvre ────────────────────────────────────────────────
    {"n":"Equestrian Statue of Bartolomeo Colleoni","ar":"Andrea del Verrocchio","yr":"1480-1496","ma":"Bronze","lo":"Campo Santi Giovanni e Paolo, Venice","st":"Early Renaissance","fa":"Completed after Verrocchio's death by Alessandro Leopardi; the general's fierce expression and aggressive posture set the standard for equestrian monuments for 200 years"},
    {"n":"Rebellious Slave","ar":"Michelangelo","yr":"1513-1516","ma":"Marble","lo":"Louvre Museum, Paris","st":"Renaissance","fa":"Its unfinished state — the figure seems to struggle from the marble — sparked Michelangelo's idea of 'non-finito': the eternal prisoner of the stone he's carved from"},
    {"n":"Pietà Rondanini","ar":"Michelangelo","yr":"1552-1564 (unfinished)","ma":"Marble","lo":"Castello Sforzesco, Milan","st":"Late Renaissance","fa":"Michelangelo worked on this until six days before his death at 88; in this final vision Christ and Mary dissolve into each other — barely distinguishable as two figures"},
    {"n":"Rabbit","ar":"Jeff Koons","yr":"1986","ma":"Stainless steel","lo":"Private collection","st":"Neo-Pop","fa":"An inflatable Easter toy cast in mirror-polished steel; sold for $91.1M in 2019, setting the record for a living artist — a balloon become immortal and untouchable"},
    {"n":"Balloon Venus","ar":"Jeff Koons","yr":"2008-2012","ma":"Mirror-polished steel","lo":"Fondation Beyeler, Basel","st":"Neo-Pop","fa":"A blown-up rendering of the Venus of Willendorf; Koons fused 25,000-year-old symbolism with 21st-century spectacle — 40,000 years of fertility goddess in one shiny balloon"},
    {"n":"The Weather Project","ar":"Olafur Eliasson","yr":"2003","ma":"Monofrequency lamps, mirror foil, steel, smoke","lo":"Tate Modern (Turbine Hall)","st":"Installation","fa":"A gigantic artificial sun in the Turbine Hall; over 2 million visitors came to lie on the floor and contemplate their reflection — more than any Tate show before or since"},
    {"n":"The Kelpies","ar":"Andy Scott","yr":"2013","ma":"Steel","lo":"Falkirk, Scotland","st":"Contemporary","fa":"Two 30-meter horse-head sculptures — the largest equine sculptures in the world — celebrate the heavy horses that powered Scotland's industrial canals and fields"},
    {"n":"Olmec Wrestler","ar":"Unknown Olmec","yr":"~900-600 BC","ma":"Serpentine","lo":"National Museum of Anthropology, Mexico City","st":"Olmec","fa":"The most naturalistic human figure in pre-Columbian art; the kneeling figure's musculature and posture are so accurate they suggest life studies from actual wrestlers"},
    {"n":"Caryatid Porch","ar":"Unknown Athenian sculptor","yr":"~421-406 BC","ma":"Marble","lo":"Erechtheion, Athens Acropolis","st":"Classical Greek","fa":"Six maidens (caryatids) serve as columns on the Erechtheion; one original is in the British Museum (taken by Elgin) — Greece has demanded its return for decades"},
    {"n":"Nike Adjusting Her Sandal","ar":"Unknown","yr":"~410 BC","ma":"Marble","lo":"Acropolis Museum, Athens","st":"Classical Greek","fa":"A small relief from the Athena Nike temple; Nike bends to fasten her sandal and the thin 'wet drapery' technique reveals her form with breathtaking naturalism"},
    {"n":"Dancers (Degas)","ar":"Edgar Degas","yr":"~1890-1895","ma":"Bronze","lo":"Multiple collections","st":"Impressionism","fa":"Degas's late wax models — never intended for public view — were cast in bronze only after his death; the rough, spontaneous surfaces record his vision nearly going blind"},
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
                    if src: return src
            else:
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title)}"
                r = requests.get(url, headers=HEADERS, timeout=10)
                if r.status_code == 200:
                    src = r.json().get("thumbnail", {}).get("source")
                    if src: return src
        except Exception:
            pass
    return None

def main():
    total = len(sculptures)
    found = 0
    for i, s in enumerate(sculptures):
        title = WIKI_EN.get(s["n"], s["n"])
        img = wiki_img(title)
        s["im"] = img
        if img: found += 1
        status = "ok" if img else "xx"
        sys.stdout.buffer.write(f"  [{i+1:2}/{total}] {status} {s['n']}\n".encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)
    out = Path("assets/art/sculptures.json")
    out.write_text(json.dumps(sculptures, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    sys.stdout.buffer.write(f"\nDone: {found}/{total} images — {total} sculptures total.\n".encode("utf-8"))

if __name__ == "__main__":
    main()
