# Légende des clés JSON
# n   : name (nom du minéral)
# grp : group (groupe minéralogique)
# cs  : crystal system (système cristallin)
# ha  : hardness (dureté Mohs)
# co  : color (couleur)
# lu  : luster (éclat)
# di  : discovery (date / époque de découverte)
# pr  : production (production annuelle estimée)
# us  : uses (utilisations)
# ff  : famous for (fait marquant)
# im  : image URL (ajouté par le générateur)

MINERALS = [
    # ── Native Elements ───────────────────────────────────────────────────
    {"n":"Gold","grp":"Native element","cs":"Cubic","ha":"2.5-3","co":"Golden yellow","lu":"Metallic",
     "di":"Known since ~6,000 BCE","pr":"~3,300 tonnes/year (global)",
     "us":"Jewelry, electronics, currency","ff":"One of the few elements found pure in nature; valued since prehistoric times"},

    {"n":"Silver","grp":"Native element","cs":"Cubic","ha":"2.5-3","co":"Silver-white","lu":"Metallic",
     "di":"Known since ~4,000 BCE","pr":"~27,000 tonnes/year",
     "us":"Jewelry, photography, electronics","ff":"Best electrical conductor of all elements"},

    {"n":"Copper","grp":"Native element","cs":"Cubic","ha":"2.5-3","co":"Copper-red","lu":"Metallic",
     "di":"Known since ~8,000 BCE","pr":"~22 million tonnes/year",
     "us":"Wiring, plumbing, coins","ff":"One of the first metals used by humans, over 10,000 years ago"},

    {"n":"Diamond","grp":"Native element","cs":"Cubic","ha":"10","co":"Colorless (various)","lu":"Adamantine",
     "di":"Known since ~4th century BCE (India)","pr":"~148 million carats/year (~30 tonnes)",
     "us":"Gemstones, cutting tools, abrasives","ff":"Hardest natural substance on Earth — pure carbon atoms arranged in a lattice"},

    {"n":"Graphite","grp":"Native element","cs":"Hexagonal","ha":"1-2","co":"Black to steel-grey","lu":"Metallic to dull",
     "di":"Used prehistorically; named 1789 by Abraham Werner","pr":"~1.1 million tonnes/year",
     "us":"Pencils, lubricants, electrodes, lithium-ion batteries","ff":"Allotrope of diamond — same element (carbon), completely different properties"},

    {"n":"Sulfur","grp":"Native element","cs":"Orthorhombic","ha":"1.5-2.5","co":"Bright yellow","lu":"Resinous",
     "di":"Known since antiquity (mentioned in the Bible)","pr":"~70 million tonnes/year",
     "us":"Fertilizers, gunpowder, rubber vulcanization, pharmaceuticals","ff":"Found around volcanic vents and hot springs; burns with a blue flame"},

    {"n":"Platinum","grp":"Native element","cs":"Cubic","ha":"4-4.5","co":"Silver-white","lu":"Metallic",
     "di":"Named 1748 by Antonio de Ulloa (Spanish Navy)","pr":"~190 tonnes/year",
     "us":"Jewelry, catalytic converters, lab equipment, cancer drugs","ff":"Rarer than gold — its entire annual production would fill less than one swimming pool"},

    # ── Silicates ─────────────────────────────────────────────────────────
    {"n":"Quartz","grp":"Silicate (tectosilicate)","cs":"Trigonal","ha":"7","co":"Colorless, various","lu":"Vitreous",
     "di":"Known since prehistoric times","pr":"~200 million tonnes/year (as silica sand)",
     "us":"Electronics, glass, watches, concrete","ff":"Most abundant mineral in Earth's continental crust"},

    {"n":"Amethyst","grp":"Silicate (quartz variety)","cs":"Trigonal","ha":"7","co":"Violet to purple","lu":"Vitreous",
     "di":"Known since ~2,500 BCE (ancient Egypt)","pr":"Hundreds of tonnes/year (mainly Brazil, Uruguay)",
     "us":"Gemstones, decorative objects","ff":"Purple color comes from iron impurities; historically believed to prevent intoxication"},

    {"n":"Rose Quartz","grp":"Silicate (quartz variety)","cs":"Trigonal","ha":"7","co":"Pink","lu":"Vitreous",
     "di":"Known since ~7,000 BCE (Mesopotamia)","pr":"Hundreds of tonnes/year",
     "us":"Gemstones, ornamental stone","ff":"Pink hue caused by trace amounts of titanium, iron, or manganese"},

    {"n":"Obsidian","grp":"Silicate (volcanic glass)","cs":"Amorphous","ha":"5-5.5","co":"Black to dark green","lu":"Vitreous",
     "di":"Used as tools since ~700,000 BCE (Stone Age)","pr":"Limited — no industrial mining",
     "us":"Surgical blades, arrowheads, decorative objects","ff":"Not a true mineral — a natural volcanic glass sharper than surgical steel"},

    {"n":"Feldspar (Orthoclase)","grp":"Silicate (tectosilicate)","cs":"Monoclinic","ha":"6","co":"White, pink, grey","lu":"Vitreous to pearly",
     "di":"First described 1801 by Martin Klaproth","pr":"~23 million tonnes/year (feldspar group)",
     "us":"Ceramics, glass, porcelain, dental porcelain","ff":"Most abundant mineral group on Earth's surface, forming ~60% of the crust"},

    {"n":"Muscovite Mica","grp":"Silicate (phyllosilicate)","cs":"Monoclinic","ha":"2-3","co":"Colorless, silver","lu":"Pearly",
     "di":"Used since ancient times; formally described 1850","pr":"~400,000 tonnes/year",
     "us":"Electrical insulation, windows, cosmetics, paint","ff":"Splits into perfect transparent sheets — used as 'isinglass' windows before glass was available"},

    {"n":"Biotite Mica","grp":"Silicate (phyllosilicate)","cs":"Monoclinic","ha":"2.5-3","co":"Black to dark brown","lu":"Pearly",
     "di":"Described 1847 by J.F.L. Hausmann","pr":"Included in ~400,000 tonnes/year (mica total)",
     "us":"Geological dating (K-Ar method), electronics, construction","ff":"Used for potassium-argon dating to determine the age of rocks"},

    {"n":"Olivine","grp":"Silicate (nesosilicate)","cs":"Orthorhombic","ha":"6.5-7","co":"Olive green","lu":"Vitreous",
     "di":"Known since ancient times; formally described ~1790","pr":"~8 million tonnes/year (dunite/olivine sand)",
     "us":"Refractory materials, gemstone (peridot), slag conditioner","ff":"Makes up most of Earth's mantle — also found in meteorites and on the surface of Mars"},

    {"n":"Garnet (Almandine)","grp":"Silicate (nesosilicate)","cs":"Cubic","ha":"7-7.5","co":"Deep red","lu":"Vitreous to resinous",
     "di":"Known since ~3,100 BCE (ancient Egypt)","pr":"~300,000 tonnes/year (industrial garnet)",
     "us":"Gemstones, abrasives (garnet paper), water-jet cutting","ff":"Garnet group has over 20 species; used as abrasive since the Bronze Age"},

    {"n":"Topaz","grp":"Silicate (nesosilicate)","cs":"Orthorhombic","ha":"8","co":"Colorless, blue, yellow","lu":"Vitreous",
     "di":"Known since ~1,500 BCE; prized by ancient Romans","pr":"~50,000 carats/year (gem quality)",
     "us":"Gemstones","ff":"Pure topaz is colorless — blue topaz is usually colorless topaz treated with radiation"},

    {"n":"Tourmaline","grp":"Silicate (cyclosilicate)","cs":"Trigonal","ha":"7-7.5","co":"All colors possible","lu":"Vitreous",
     "di":"Named 1703 (from Sinhalese 'turmali')","pr":"~50,000 carats/year (gem quality)",
     "us":"Gemstones, piezoelectric pressure gauges","ff":"Can display two or more colors in one crystal — watermelon tourmaline is green outside, pink inside"},

    {"n":"Emerald","grp":"Silicate (cyclosilicate, beryl)","cs":"Hexagonal","ha":"7.5-8","co":"Green","lu":"Vitreous",
     "di":"Mined since ~4,000 BCE (ancient Egypt, Sinai)","pr":"~100,000 carats/year (gem quality, Colombia)",
     "us":"Gemstones","ff":"Colored green by chromium impurities; Cleopatra's favorite gemstone"},

    {"n":"Aquamarine","grp":"Silicate (cyclosilicate, beryl)","cs":"Hexagonal","ha":"7.5-8","co":"Blue to blue-green","lu":"Vitreous",
     "di":"Known since ~300 BCE; named by ancient Romans","pr":"~50,000 carats/year (gem quality)",
     "us":"Gemstones","ff":"Blue-green color caused by iron; the name means 'water of the sea' in Latin"},

    {"n":"Talc","grp":"Silicate (phyllosilicate)","cs":"Triclinic","ha":"1","co":"White, grey, green","lu":"Waxy to pearly",
     "di":"Used since ancient times; described 1546 by Agricola","pr":"~7 million tonnes/year",
     "us":"Talcum powder, paint, ceramics, paper, plastics","ff":"Softest known mineral — hardness 1 on the Mohs scale; feels soapy to the touch"},

    {"n":"Kyanite","grp":"Silicate (nesosilicate)","cs":"Triclinic","ha":"4.5-7","co":"Blue","lu":"Vitreous to pearly",
     "di":"Described 1789 by Abraham Werner","pr":"~300,000 tonnes/year",
     "us":"High-temperature ceramics, spark plugs, refractory materials","ff":"Unusual mineral with different hardness in different directions — 4.5 along the crystal, 7 across it"},

    {"n":"Zircon","grp":"Silicate (nesosilicate)","cs":"Tetragonal","ha":"7.5","co":"Brown, red, colorless","lu":"Adamantine",
     "di":"Known since antiquity; oldest Earth crystals ~4.4 billion years old","pr":"~1.4 million tonnes/year (as zirconium ore)",
     "us":"Gemstones, ceramic glazes, nuclear fuel, refractory materials","ff":"Oldest mineral ever found on Earth — some zircon crystals are 4.4 billion years old"},

    {"n":"Labradorite","grp":"Silicate (tectosilicate, feldspar)","cs":"Triclinic","ha":"6-6.5","co":"Grey with blue-green iridescence","lu":"Vitreous",
     "di":"First described 1770, Labrador, Canada","pr":"Part of ~23 million tonnes/year (feldspar group)",
     "us":"Gemstones, decorative countertops, jewelry","ff":"Shows labradorescence — a spectacular play of iridescent colors caused by light interference"},

    {"n":"Jade (Jadeite)","grp":"Silicate (inosilicate)","cs":"Monoclinic","ha":"6.5-7","co":"Green, white, lavender","lu":"Vitreous",
     "di":"Revered in China for 5,000+ years","pr":"~500-1,000 tonnes/year (mainly Myanmar)",
     "us":"Gemstones, carvings, jewelry","ff":"Sacred in Chinese culture for over 5,000 years; not to be confused with nephrite, the other 'jade'"},

    # ── Oxides ────────────────────────────────────────────────────────────
    {"n":"Hematite","grp":"Oxide","cs":"Trigonal","ha":"5.5-6.5","co":"Steel grey to black; red streak","lu":"Metallic to dull",
     "di":"Used as red ochre pigment since ~40,000 BCE","pr":"~2.5 billion tonnes/year (as iron ore)",
     "us":"Iron ore, red pigment, jewelry","ff":"Leaves a distinctive red-brown streak; the red color of Mars comes from hematite dust"},

    {"n":"Magnetite","grp":"Oxide","cs":"Cubic","ha":"5.5-6.5","co":"Black","lu":"Metallic",
     "di":"Known since ~600 BCE (Magnesia, Greece)","pr":"Included in ~2.5 billion tonnes/year (iron ore)",
     "us":"Iron ore, compasses, magnetic recording media, ferrofluids","ff":"Natural magnet — the original compass mineral; some bacteria produce tiny magnetite crystals to navigate"},

    {"n":"Corundum","grp":"Oxide","cs":"Trigonal","ha":"9","co":"Colorless, grey, brown","lu":"Adamantine to vitreous",
     "di":"Named 1798 by Heinrich Klaproth","pr":"~3,000 tonnes/year (natural); millions of tonnes synthetic",
     "us":"Abrasives (emery), gemstones (ruby and sapphire)","ff":"Ruby and sapphire are both corundum — only iron and titanium separate a sapphire from a ruby"},

    {"n":"Ruby","grp":"Oxide (corundum variety)","cs":"Trigonal","ha":"9","co":"Red","lu":"Adamantine",
     "di":"Known since ~2,500 BCE (ancient Myanmar)","pr":"~20,000 carats/year (gem-quality natural)",
     "us":"Gemstones, lasers, bearings, scientific instruments","ff":"Red color from chromium impurities; the world's first laser (1960) used a synthetic ruby rod"},

    {"n":"Sapphire","grp":"Oxide (corundum variety)","cs":"Trigonal","ha":"9","co":"Blue (also yellow, pink, orange)","lu":"Adamantine",
     "di":"Prized since ~800 BCE (ancient Persia)","pr":"~200,000 carats/year (natural gems)",
     "us":"Gemstones, watch crystals, smartphone screens, industrial bearings","ff":"Second hardest gem after diamond; 'fancy sapphires' can be pink, yellow, or orange"},

    {"n":"Rutile","grp":"Oxide","cs":"Tetragonal","ha":"6-6.5","co":"Red-brown to black","lu":"Adamantine to metallic",
     "di":"Described 1803 by Werner & d'Andrada","pr":"~800,000 tonnes/year (as titanium ore)",
     "us":"Titanium production, white pigment (TiO₂), solar cells, welding electrodes","ff":"Provides the white pigment in white paint — covers more surface area than any other pigment"},

    {"n":"Cassiterite","grp":"Oxide","cs":"Tetragonal","ha":"6-7","co":"Brown to black","lu":"Adamantine",
     "di":"Used since ~3,500 BCE (Bronze Age, Turkey and Cornwall)","pr":"~300,000 tonnes/year (tin ore)",
     "us":"Primary tin ore (bronze, solder, tin cans)","ff":"Tin from cassiterite enabled the Bronze Age — the most important ore of tin for 5,000 years"},

    {"n":"Spinel","grp":"Oxide","cs":"Cubic","ha":"7.5-8","co":"Red, blue, black, colorless","lu":"Vitreous",
     "di":"First described 1546 by Georgius Agricola","pr":"~100,000 carats/year (gems); also synthetic",
     "us":"Gemstones, refractory ceramics, synthetic abrasives","ff":"The Black Prince's 'Ruby' in the British Crown Jewels is actually a red spinel"},

    # ── Carbonates ────────────────────────────────────────────────────────
    {"n":"Calcite","grp":"Carbonate","cs":"Trigonal","ha":"3","co":"Colorless, white, yellow","lu":"Vitreous",
     "di":"Known since ancient times; defines Mohs hardness 3","pr":"~5 billion tonnes/year (as limestone)",
     "us":"Limestone, cement, lime, antacids, paper filler","ff":"Most common carbonate mineral; when pure, splits light into double refraction (Iceland spar)"},

    {"n":"Dolomite","grp":"Carbonate","cs":"Trigonal","ha":"3.5-4","co":"White, grey, pink","lu":"Vitreous to pearly",
     "di":"Described 1791 by Déodat de Dolomieu (French geologist)","pr":"~500 million tonnes/year",
     "us":"Building stone, magnesium source, steel-making flux","ff":"The Dolomites mountains in Italy are named after this mineral; entire mountain ranges are made of it"},

    {"n":"Malachite","grp":"Carbonate","cs":"Monoclinic","ha":"3.5-4","co":"Bright green","lu":"Vitreous to silky",
     "di":"Used since ~4,000 BCE (ancient Egypt as pigment and copper ore)","pr":"Part of copper ore production",
     "us":"Gemstone, green pigment, copper ore, decorative objects","ff":"Striking banded green stone; used as pigment by ancient Egyptians for eye shadow"},

    {"n":"Azurite","grp":"Carbonate","cs":"Monoclinic","ha":"3.5-4","co":"Deep azure blue","lu":"Vitreous",
     "di":"Used since ~3,000 BCE (ancient Egypt and China)","pr":"Limited — mostly byproduct of copper mining",
     "us":"Blue pigment, gemstone, minor copper ore","ff":"Often found intergrown with malachite; one of the most important blue pigments in medieval European art"},

    {"n":"Rhodochrosite","grp":"Carbonate","cs":"Trigonal","ha":"3.5-4","co":"Rose-red to pink","lu":"Vitreous",
     "di":"Described 1813 by Hausmann","pr":"~50,000 carats/year (gemstone); also manganese ore",
     "us":"Gemstone, manganese ore, collectors' mineral","ff":"Argentina's national gemstone — the Incas believed it was condensed blood of their ancient kings"},

    {"n":"Aragonite","grp":"Carbonate","cs":"Orthorhombic","ha":"3.5-4","co":"Colorless, white","lu":"Vitreous to resinous",
     "di":"Named 1797 from Molina de Aragón, Spain","pr":"~10 million tonnes/year",
     "us":"Aquarium conditioning, gemstone, cement, pearls","ff":"Same composition as calcite but different crystal structure — pearls and coral are made of aragonite"},

    {"n":"Smithsonite","grp":"Carbonate","cs":"Trigonal","ha":"4-4.5","co":"White, blue, green, pink","lu":"Vitreous to pearly",
     "di":"Named 1832 after James Smithson (founder of the Smithsonian)","pr":"Part of ~13 million tonnes/year (zinc ore)",
     "us":"Zinc ore, gemstone","ff":"Named after James Smithson, founder of the Smithsonian Institution, who first identified it as a zinc carbonate"},

    # ── Sulfides ──────────────────────────────────────────────────────────
    {"n":"Pyrite","grp":"Sulfide","cs":"Cubic","ha":"6-6.5","co":"Pale brass-yellow","lu":"Metallic",
     "di":"Known since ancient times (Greek: pyr = fire)","pr":"~50 million tonnes/year",
     "us":"Sulfuric acid production, iron ore, formerly fire-starting","ff":"'Fool's Gold' — deceived many prospectors; also caused shipwrecks by spontaneously combusting in damp holds"},

    {"n":"Galena","grp":"Sulfide","cs":"Cubic","ha":"2.5","co":"Lead-grey","lu":"Metallic",
     "di":"Used since ~5,000 BCE (ancient Rome for pipes and paint)","pr":"~4.7 million tonnes/year (lead ore)",
     "us":"Lead ore (primary source), crystal radios, radiation shielding","ff":"Densest common mineral; the first semiconductors used in crystal radios were galena crystals"},

    {"n":"Chalcopyrite","grp":"Sulfide","cs":"Tetragonal","ha":"3.5-4","co":"Brass-yellow","lu":"Metallic",
     "di":"Named 1725; used since antiquity as copper ore","pr":"Dominant source of global ~22 million tonnes/year copper",
     "us":"Copper ore (most important worldwide)","ff":"Principal ore of copper worldwide; found in nearly every copper deposit on Earth"},

    {"n":"Sphalerite","grp":"Sulfide","cs":"Cubic","ha":"3.5-4","co":"Yellow, brown, black","lu":"Resinous to adamantine",
     "di":"Named 1847 (Greek: sphaleris = treacherous)","pr":"~13 million tonnes/year (zinc ore)",
     "us":"Zinc ore, germanium and indium source (electronics)","ff":"Primary source of zinc; also yields rare metals like indium used in smartphone touchscreens"},

    {"n":"Cinnabar","grp":"Sulfide","cs":"Trigonal","ha":"2-2.5","co":"Scarlet red","lu":"Adamantine",
     "di":"Used since ~4,000 BCE as red pigment (vermilion)","pr":"~3,000 tonnes/year (mercury ore)",
     "us":"Mercury ore, historical red pigment (vermilion)","ff":"The only significant ore of mercury; its brilliant red pigment was used in Roman frescoes — dangerously toxic"},

    {"n":"Bornite","grp":"Sulfide","cs":"Orthorhombic","ha":"3","co":"Copper-red when fresh","lu":"Metallic",
     "di":"Named 1845 after Ignaz von Born (Austrian mineralogist)","pr":"Part of ~22 million tonnes/year (copper ore)",
     "us":"Copper ore","ff":"'Peacock ore' — tarnishes to spectacular iridescent purple, blue, and green when exposed to air"},

    {"n":"Molybdenite","grp":"Sulfide","cs":"Hexagonal","ha":"1-1.5","co":"Lead-grey","lu":"Metallic",
     "di":"Described 1778 by Carl Wilhelm Scheele","pr":"~300,000 tonnes/year (molybdenum ore)",
     "us":"Molybdenum source (steel alloys for jet engines), solid lubricant","ff":"Softest metal sulfide; looks like graphite and was mistaken for it — molybdenum strengthens steel for jet engines"},

    {"n":"Stibnite","grp":"Sulfide","cs":"Orthorhombic","ha":"2","co":"Lead-grey","lu":"Metallic",
     "di":"Used since ~3,000 BCE (kohl eyeliner in ancient Egypt)","pr":"~150,000 tonnes/year (antimony ore)",
     "us":"Antimony ore, fireworks, safety matches, flame retardants","ff":"Longest natural metallic crystals — can grow to 60 cm; used as kohl eyeliner in ancient Egypt and the Middle East"},

    {"n":"Realgar","grp":"Sulfide","cs":"Monoclinic","ha":"1.5-2","co":"Red to orange-red","lu":"Resinous to adamantine",
     "di":"Used since antiquity in China and the Middle East","pr":"Minor — mainly byproduct of mining",
     "us":"Formerly in fireworks and insecticides (highly toxic arsenic content)","ff":"Breaks down in light to yellow orpiment — ancient Chinese medicine used it to repel evil spirits despite its arsenic content"},

    {"n":"Pyrrhotite","grp":"Sulfide","cs":"Hexagonal","ha":"3.5-4.5","co":"Bronze-yellow to brown","lu":"Metallic",
     "di":"Named 1868 (Greek: pyrrhos = flame-colored)","pr":"Part of nickel and copper ore production",
     "us":"Nickel and sulfur source, sometimes pentlandite host","ff":"Weakly magnetic iron sulfide — the only magnetic sulfide mineral; found in meteorites from Mars"},

    # ── Halides ───────────────────────────────────────────────────────────
    {"n":"Halite","grp":"Halide","cs":"Cubic","ha":"2.5","co":"Colorless, white, pink","lu":"Vitreous",
     "di":"Used since ~8,000 BCE (Neolithic salt trade)","pr":"~300 million tonnes/year",
     "us":"Table salt, food preservation, road de-icing, chlorine production","ff":"One of the oldest traded commodities — Roman soldiers were partly paid in salt (origin of the word 'salary')"},

    {"n":"Fluorite","grp":"Halide","cs":"Cubic","ha":"4","co":"All colors, often purple or green","lu":"Vitreous",
     "di":"Named 1546 by Georgius Agricola (Latin: fluere = to flow)","pr":"~6.5 million tonnes/year",
     "us":"Flux in steel-making, optical lenses, HF acid, fluoride in toothpaste","ff":"Defines hardness 4 on the Mohs scale; the word 'fluorescence' was coined from fluorite, which glows under UV light"},

    {"n":"Sylvite","grp":"Halide","cs":"Cubic","ha":"2","co":"Colorless, white, yellow","lu":"Vitreous",
     "di":"Described 1832 (named after Franciscus Sylvius)","pr":"~65 million tonnes/year (as potash fertilizer)",
     "us":"Potassium fertilizer (primary source), chemical feedstock","ff":"Tastes more bitter than rock salt; mined in enormous quantities to feed the world's crops"},

    # ── Phosphates ────────────────────────────────────────────────────────
    {"n":"Apatite","grp":"Phosphate","cs":"Hexagonal","ha":"5","co":"Green, blue, yellow, brown","lu":"Vitreous to resinous",
     "di":"Named 1786 by Abraham Werner (Greek: apatao = to deceive)","pr":"~260 million tonnes/year (rock phosphate)",
     "us":"Phosphate fertilizer, hydroxylapatite for bone grafts, dental enamel","ff":"Defines hardness 5 on the Mohs scale; your teeth and bones are partly made of a form of apatite"},

    {"n":"Turquoise","grp":"Phosphate","cs":"Triclinic","ha":"5-6","co":"Sky blue to blue-green","lu":"Waxy",
     "di":"Mined since ~6,000 BCE (Sinai Peninsula, Egypt)","pr":"~500-1,000 tonnes/year",
     "us":"Gemstones, decorative art, Native American jewelry","ff":"One of the oldest gemstones — mined in the Sinai by Egyptians 6,000 years ago; sacred to Native Americans"},

    {"n":"Vivianite","grp":"Phosphate","cs":"Monoclinic","ha":"1.5-2","co":"Colorless fresh, turns blue-green on exposure","lu":"Vitreous to pearly",
     "di":"Named 1817 after J.H. Vivian (British mineralogist)","pr":"Rare — minor production",
     "us":"Blue pigment, minor iron ore, collectors' mineral","ff":"Starts colorless but turns intensely blue-green on exposure to light due to iron oxidation"},

    {"n":"Pyromorphite","grp":"Phosphate","cs":"Hexagonal","ha":"3.5-4","co":"Green, yellow, brown","lu":"Resinous to adamantine",
     "di":"Named 1813 (Greek: pyr = fire, morphe = form)","pr":"Minor — mainly byproduct of lead mining",
     "us":"Lead ore, prized collector's mineral","ff":"One of the most brightly colored lead minerals; its name means 'fire form' as it takes a rounded crystal shape when heated"},

    # ── Sulfates ──────────────────────────────────────────────────────────
    {"n":"Gypsum","grp":"Sulfate","cs":"Monoclinic","ha":"2","co":"Colorless, white","lu":"Vitreous to silky",
     "di":"Used since ~5,000 BCE (ancient Egyptian plaster)","pr":"~150 million tonnes/year",
     "us":"Drywall (plasterboard), plaster of Paris, soil conditioner, cement","ff":"Defines hardness 2 on the Mohs scale; when heated it loses water and becomes plaster of Paris"},

    {"n":"Barite","grp":"Sulfate","cs":"Orthorhombic","ha":"3-3.5","co":"Colorless, white, yellow","lu":"Vitreous to resinous",
     "di":"Described 1605 (Greek: barys = heavy)","pr":"~9 million tonnes/year",
     "us":"Oil drilling mud, X-ray contrast agent, paints, sound insulation","ff":"Surprisingly heavy for a non-metallic mineral — its weight makes it ideal for oil drilling fluids to control pressure"},

    {"n":"Celestite","grp":"Sulfate","cs":"Orthorhombic","ha":"3-3.5","co":"Sky blue","lu":"Vitreous",
     "di":"Named 1798 (Latin: caelestis = heavenly, for its blue color)","pr":"~350,000 tonnes/year (strontium ore)",
     "us":"Strontium production, fireworks (red color), metal alloys","ff":"Primary source of strontium — gives fireworks and emergency flares their brilliant crimson-red color"},

    {"n":"Anhydrite","grp":"Sulfate","cs":"Orthorhombic","ha":"3-3.5","co":"Colorless, blue, grey","lu":"Vitreous to pearly",
     "di":"Named 1804 by Abraham Werner (Greek: an-hydor = waterless)","pr":"Part of ~150 million tonnes/year (sulfate minerals)",
     "us":"Cement additive, soil conditioner, filler in paper and paint","ff":"Chemically identical to gypsum without water; slowly absorbs water from air and expands, causing buildings to crack"},

    # ── Tungstates ────────────────────────────────────────────────────────
    {"n":"Scheelite","grp":"Tungstate","cs":"Tetragonal","ha":"4.5-5","co":"White, yellow, orange","lu":"Adamantine",
     "di":"Named 1821 after Carl Wilhelm Scheele (discoverer of tungsten)","pr":"Part of ~86,000 tonnes/year (tungsten ore)",
     "us":"Tungsten source for light bulb filaments, cutting tools, armor-piercing ammunition","ff":"Fluoresces brilliant blue-white under ultraviolet light; miners use UV lamps to locate it in the dark"},

    {"n":"Wolframite","grp":"Tungstate","cs":"Monoclinic","ha":"4-4.5","co":"Black to dark brown","lu":"Submetallic",
     "di":"Named 1845 (origin of the symbol W for tungsten)","pr":"Part of ~86,000 tonnes/year (tungsten ore)",
     "us":"Tungsten ore, vibration motors in phones, armor-piercing projectiles","ff":"'Conflict mineral' — mined in war zones; the tiny vibration motor in your phone likely contains tungsten from this mineral"},

    # ── Borates ───────────────────────────────────────────────────────────
    {"n":"Borax","grp":"Borate","cs":"Monoclinic","ha":"2-2.5","co":"White","lu":"Vitreous to resinous",
     "di":"Used since ~4th century BCE (China and Tibet)","pr":"~3.6 million tonnes/year",
     "us":"Detergent booster, glass production, ceramics, soldering flux","ff":"Mined extensively in Death Valley — the famous 20-mule team wagons hauled borax out of the California desert"},

    {"n":"Ulexite","grp":"Borate","cs":"Triclinic","ha":"2.5","co":"White","lu":"Silky (fibrous)",
     "di":"Named 1850 after Georg Ludwig Ulex (German chemist)","pr":"Part of ~3.6 million tonnes/year (boron minerals)",
     "us":"Boron source, optical fiber experiments","ff":"Known as 'TV rock' — its parallel fibers transmit images like fiber optics; you can read text through a piece"},

    # ── Hydroxides ────────────────────────────────────────────────────────
    {"n":"Goethite","grp":"Hydroxide (iron oxyhydroxide)","cs":"Orthorhombic","ha":"5-5.5","co":"Yellow-brown to red-brown","lu":"Adamantine to dull",
     "di":"Named 1806 after Johann Wolfgang von Goethe","pr":"Part of ~2.5 billion tonnes/year (iron ore)",
     "us":"Yellow ochre pigment, iron ore, rust patina on weathered steel","ff":"One of the most widespread iron minerals; 'yellow ochre' used in cave paintings 40,000 years ago is goethite"},

    # ── Oxides (gem varieties) ─────────────────────────────────────────────
    {"n":"Alexandrite","grp":"Oxide (chrysoberyl variety)","cs":"Orthorhombic","ha":"8.5","co":"Green in daylight, red under incandescent light","lu":"Vitreous",
     "di":"Discovered 1830 in the Ural Mountains (named for Tsar Alexander II)","pr":"Very rare — <1,000 carats/year (natural)",
     "us":"Gemstones (highly prized collector's stone)","ff":"Changes color from green to red depending on the light source — rarer than diamonds; a 1-carat natural alexandrite can cost more than a diamond"},

    {"n":"Chrysoberyl","grp":"Oxide","cs":"Orthorhombic","ha":"8.5","co":"Yellow-green to green","lu":"Vitreous",
     "di":"Named 1790 by Abraham Werner","pr":"~50,000 carats/year (including cat's-eye)",
     "us":"Gemstones, abrasives","ff":"Third hardest natural gem after diamond and corundum; cat's-eye chrysoberyl shows a moving line of light (chatoyancy)"},

    # ── Mineraloids ───────────────────────────────────────────────────────
    {"n":"Opal","grp":"Mineraloid (hydrated silica)","cs":"Amorphous","ha":"5.5-6.5","co":"White to black with play of color","lu":"Vitreous to resinous",
     "di":"Used since ~4,000 BCE; named by Pliny the Elder (~50 CE)","pr":"~500 tonnes/year (mainly Australia ~95%)",
     "us":"Gemstones, collectors' mineral","ff":"Play-of-color called 'opalescence' is caused by diffraction of light through tiny silica spheres stacked in perfect layers"},

    # ── Additional sulfides ────────────────────────────────────────────────
    {"n":"Chalcocite","grp":"Sulfide","cs":"Monoclinic","ha":"2.5-3","co":"Lead-grey to black","lu":"Metallic",
     "di":"Named 1845 (Greek: chalkos = copper)","pr":"Part of ~22 million tonnes/year (copper ore)",
     "us":"High-grade copper ore (79.8% copper by weight)","ff":"One of the most profitable copper ores; a supergene mineral formed near the surface when descending fluids enrich copper deposits"},

    {"n":"Wulfenite","grp":"Molybdate","cs":"Tetragonal","ha":"2.75-3","co":"Orange-red to yellow","lu":"Resinous to adamantine",
     "di":"Named 1845 after Franz X. von Wulfen (Austrian mineralogist)","pr":"Minor — mainly collectors' mineral",
     "us":"Minor molybdenum ore, highly prized collectors' mineral","ff":"Some of the most aesthetically striking crystals in mineralogy — thin orange tablets described as 'stained glass windows in stone'"},

    # ── Additional silicates ───────────────────────────────────────────────
    {"n":"Rhodonite","grp":"Silicate (inosilicate)","cs":"Triclinic","ha":"5.5-6.5","co":"Pink to red with black veins","lu":"Vitreous",
     "di":"Named 1819 (Greek: rhodon = rose)","pr":"~10,000 tonnes/year (ornamental)",
     "us":"Gemstone, ornamental stone, manganese ore","ff":"Pink color from manganese; the black veins are manganese oxide dendrites — Russia designated it as the national gemstone"},

    {"n":"Chrysocolla","grp":"Silicate (phyllosilicate)","cs":"Amorphous","ha":"2.5-3.5","co":"Blue-green","lu":"Vitreous to earthy",
     "di":"Named ~300 BCE by Theophrastus (Greek: chrysos = gold, kolla = glue)","pr":"Byproduct of copper mining",
     "us":"Gemstone, minor copper ore","ff":"Often confused with turquoise; Queen Cleopatra reportedly wore chrysocolla jewelry — Plutarch called her 'the chrysocolla woman'"},

    {"n":"Sugilite","grp":"Silicate (cyclosilicate)","cs":"Hexagonal","ha":"6-6.5","co":"Vivid purple","lu":"Waxy to vitreous",
     "di":"Discovered 1944 by Ken-ichi Sugi (Japanese petrologist)","pr":"Very rare — <100 kg/year",
     "us":"Gemstone","ff":"One of the few truly purple gemstones; discovered only in 1944 and available in gem quality only since the 1970s"},

    {"n":"Tanzanite","grp":"Silicate (sorosilicate, zoisite)","cs":"Orthorhombic","ha":"6.5","co":"Violet-blue","lu":"Vitreous",
     "di":"Discovered 1967 near Mount Kilimanjaro, Tanzania","pr":"~2-3 million carats/year",
     "us":"Gemstones","ff":"Found only near Mount Kilimanjaro, Tanzania — geologists say conditions for its formation were so rare it will never be found elsewhere"},

    {"n":"Peridot (Olivine)","grp":"Silicate (nesosilicate)","cs":"Orthorhombic","ha":"6.5-7","co":"Olive to lime green","lu":"Vitreous",
     "di":"Mined since ~1,500 BCE (Zabargad Island, Red Sea)","pr":"~50,000 carats/year (gem quality)",
     "us":"Gemstones","ff":"One of few gems that forms in only one color; ancient Egyptians called it the 'gem of the sun' and believed it protected against evil"},

    {"n":"Iolite","grp":"Silicate (cyclosilicate, cordierite)","cs":"Orthorhombic","ha":"7-7.5","co":"Violet-blue","lu":"Vitreous",
     "di":"Used by Vikings ~1,000 CE as polarizing lens","pr":"~50,000 carats/year (gem quality)",
     "us":"Gemstones, engineering ceramics (heat-resistant cordierite)","ff":"Viking compass stone — its polarizing effect helped Norse sailors navigate by sky light even on overcast days"},

    {"n":"Spessartine Garnet","grp":"Silicate (nesosilicate)","cs":"Cubic","ha":"7-7.5","co":"Orange to red-orange","lu":"Vitreous to resinous",
     "di":"Named 1832 from the Spessart region, Bavaria, Germany","pr":"Part of ~300,000 tonnes/year (industrial garnet)",
     "us":"Gemstones, abrasives","ff":"The 'mandarin garnet' variety from Namibia displays an intense orange glow; manganese gives it its vivid color"},

    {"n":"Vesuvianite","grp":"Silicate (sorosilicate)","cs":"Tetragonal","ha":"6-7","co":"Green, brown, yellow","lu":"Vitreous to resinous",
     "di":"Named 1795 by Abraham Werner after Mount Vesuvius","pr":"Limited — mostly ornamental and collectors' mineral",
     "us":"Gemstone, ornamental stone","ff":"First found in the lavas of Mount Vesuvius, ejected during the same eruption that buried Pompeii in 79 AD"},
]
