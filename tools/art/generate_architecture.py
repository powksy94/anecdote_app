import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=name, ac=architect, yr=year, lo=location, st=style, co=country, fa=famous_for, im=imageUrl

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_EN = {
    "Colosseum":                    "Colosseum",
    "Parthenon":                    "Parthenon",
    "Pantheon (Rome)":              "Pantheon, Rome",
    "Hagia Sophia":                 "Hagia Sophia",
    "Angkor Wat":                   "Angkor Wat",
    "Notre-Dame de Paris":          "Notre-Dame de Paris",
    "Chartres Cathedral":           "Chartres Cathedral",
    "Westminster Abbey":            "Westminster Abbey",
    "Basilica di San Marco":        "St Mark's Basilica",
    "Florence Cathedral":           "Florence Cathedral",
    "Mezquita de Córdoba":          "Mosque-Cathedral of Córdoba",
    "Alhambra":                     "Alhambra",
    "Mont Saint-Michel":            "Mont Saint-Michel",
    "Château de Chambord":          "Château de Chambord",
    "Château de Chenonceau":        "Château de Chenonceau",
    "Neuschwanstein Castle":        "Neuschwanstein Castle",
    "Taj Mahal":                    "Taj Mahal",
    "Angkor Wat":                   "Angkor Wat",
    "Karnak Temple":                "Karnak",
    "Abu Simbel":                   "Abu Simbel temples",
    "Forbidden City":               "Forbidden City",
    "Potala Palace":                "Potala Palace",
    "Borobudur":                    "Borobudur",
    "Paro Taktsang":                "Tiger's Nest",
    "Shwedagon Pagoda":             "Shwedagon Pagoda",
    "Petra Treasury":               "Al-Khazneh",
    "Stonehenge":                   "Stonehenge",
    "Machu Picchu":                 "Machu Picchu",
    "Chichen Itza":                 "Chichen Itza",
    "Kinkaku-ji":                   "Kinkakuji",
    "Topkapi Palace":               "Topkapi Palace",
    "Versailles Palace":            "Palace of Versailles",
    "St. Peter's Basilica":         "St. Peter's Basilica",
    "Panthéon (Paris)":             "Panthéon, Paris",
    "Eiffel Tower":                 "Eiffel Tower",
    "Big Ben":                      "Big Ben",
    "St Paul's Cathedral":          "St Paul's Cathedral",
    "Arc de Triomphe":              "Arc de Triomphe",
    "Sacré-Cœur":                   "Sacré-Cœur, Paris",
    "Brooklyn Bridge":              "Brooklyn Bridge",
    "Flatiron Building":            "Flatiron Building",
    "Empire State Building":        "Empire State Building",
    "Chrysler Building":            "Chrysler Building",
    "Sagrada Família":              "Sagrada Família",
    "Casa Batlló":                  "Casa Batlló",
    "La Pedrera":                   "Casa Milà",
    "Fallingwater":                 "Fallingwater",
    "Guggenheim New York":          "Solomon R. Guggenheim Museum",
    "Seagram Building":             "Seagram Building",
    "Sydney Opera House":           "Sydney Opera House",
    "Louvre Pyramid":               "Louvre Pyramid",
    "Pompidou Centre":              "Centre Georges Pompidou",
    "Bauhaus Dessau":               "Bauhaus Dessau",
    "Villa Savoye":                 "Villa Savoye",
    "Barcelona Pavilion":           "Barcelona Pavilion",
    "Farnsworth House":             "Farnsworth House",
    "Salk Institute":               "Salk Institute for Biological Studies",
    "Sydney Harbour Bridge":        "Sydney Harbour Bridge",
    "Guggenheim Bilbao":            "Guggenheim Museum Bilbao",
    "Burj Khalifa":                 "Burj Khalifa",
    "The Shard":                    "The Shard",
    "Burj Al Arab":                 "Burj Al Arab",
    "Petronas Towers":              "Petronas Towers",
    "Lotus Temple":                 "Lotus Temple",
    "Walt Disney Concert Hall":     "Walt Disney Concert Hall",
    "Heydar Aliyev Center":         "Heydar Aliyev Center",
    "CCTV Headquarters":            "CCTV Headquarters",
    "TWA Flight Center":            "TWA Hotel",
    "CN Tower":                     "CN Tower",
    "Tokyo Skytree":                "Tokyo Skytree",
    "Shanghai Tower":               "Shanghai Tower",
    "One World Trade Center":       "One World Trade Center",
    "Millau Viaduct":               "Millau Viaduct",
    "Eden Project":                 "Eden Project",
    "Reichstag (Foster)":           "Reichstag building",
    "Harpa Concert Hall":           "Harpa (concert hall)",
    "Museum of the Future (Dubai)": "Museum of the Future",
    "National Museum of Qatar":     "National Museum of Qatar",
}

architecture = [
    # ── Antiquité ─────────────────────────────────────────────────────────────
    {"n":"Stonehenge","ac":"Unknown (Neolithic people)","yr":"~3000-1500 BC","lo":"Wiltshire, England","st":"Prehistoric","co":"United Kingdom","fa":"The largest stones weigh 25 tonnes and came from Wales 320 km away; the midsummer sunrise aligns perfectly through the heel stone - proving deliberate astronomical planning"},
    {"n":"Karnak Temple","ac":"Various pharaohs over 2,000 years","yr":"~2055-100 BC","lo":"Luxor, Egypt","st":"Ancient Egyptian","co":"Egypt","fa":"The largest religious complex ever built; the Hypostyle Hall has 134 columns - some 23 meters tall and 10 people wide - built over 2,000 years by successive pharaohs"},
    {"n":"Abu Simbel","ac":"Unknown (Ramesses II reign)","yr":"~1264-1244 BC","lo":"Aswan, Egypt","st":"Ancient Egyptian","co":"Egypt","fa":"Carved directly into a cliff face; twice a year the rising sun illuminates the inner sanctum and the face of Ramesses II - a feat of solar engineering 3,300 years old"},
    {"n":"Parthenon","ac":"Ictinus, Callicrates","yr":"447-432 BC","lo":"Athens, Greece","st":"Classical Greek","co":"Greece","fa":"Contains no perfectly straight lines - every column leans inward and bulges slightly to correct optical illusions; the technique is called entasis"},
    {"n":"Pantheon (Rome)","ac":"Apollodorus of Damascus (attr.)","yr":"125 AD","lo":"Rome, Italy","st":"Roman","co":"Italy","fa":"Its concrete dome (43.3 m diameter) was the world's largest for 1,300 years; the oculus at the top is still the only source of light inside"},
    {"n":"Colosseum","ac":"Unknown Roman architects","yr":"70-80 AD","lo":"Rome, Italy","st":"Roman","co":"Italy","fa":"Could hold 50,000-80,000 spectators; the retractable velarium was operated by 1,000 sailors using 240 masts - an engineering system not replicated until the 20th century"},
    {"n":"Petra Treasury","ac":"Nabataean architects","yr":"~1st century BC","lo":"Petra, Jordan","st":"Nabataean","co":"Jordan","fa":"Carved entirely from a rose-red sandstone cliff face; the city channels and cisterns sustained 30,000 inhabitants in the desert - the water engineering rivals the famous façade"},
    {"n":"Machu Picchu","ac":"Unknown Inca architects","yr":"~1450","lo":"Cusco Region, Peru","st":"Inca","co":"Peru","fa":"Built without mortar using ashlar technique: stones cut so precisely they lock together perfectly; rediscovered by Hiram Bingham in 1911 - locals had never forgotten it"},
    {"n":"Chichen Itza","ac":"Maya architects","yr":"~600-900 AD","lo":"Yucatán, Mexico","st":"Maya","co":"Mexico","fa":"On the spring equinox, a shadow serpent slithers down the pyramid's corner for 3 hours 22 minutes - a deliberate solar alignment embedded in the architecture"},
    # ── Moyen Âge - Religion & Pouvoir ────────────────────────────────────────
    {"n":"Hagia Sophia","ac":"Isidore of Miletus, Anthemius of Tralles","yr":"537 AD","lo":"Istanbul, Turkey","st":"Byzantine","co":"Turkey","fa":"Its 32-meter dome seemed to float on light - a ring of 40 windows creates the illusion of the dome hovering; converted from church to mosque, then museum, then mosque again"},
    {"n":"Angkor Wat","ac":"Unknown Khmer architects","yr":"1113-1150","lo":"Siem Reap, Cambodia","st":"Khmer","co":"Cambodia","fa":"The world's largest religious complex at 402 acres; the only major monument oriented to the west - possibly a funerary temple for king Suryavarman II"},
    {"n":"Borobudur","ac":"Gunadharma (attr.)","yr":"~750-850 AD","lo":"Central Java, Indonesia","st":"Buddhist","co":"Indonesia","fa":"The world's largest Buddhist monument; its 2,672 relief panels, read in sequence, tell the entire Buddhist Mahayana cosmology - the world's longest stone narrative"},
    {"n":"Notre-Dame de Paris","ac":"Maurice de Sully (initiator)","yr":"1163-1345","lo":"Paris, France","st":"Gothic","co":"France","fa":"The first building to use flying buttresses, spreading the style across Europe; the 2019 fire and ongoing restoration drew worldwide attention"},
    {"n":"Chartres Cathedral","ac":"Unknown","yr":"1194-1220","lo":"Chartres, France","st":"Gothic","co":"France","fa":"Built in just 26 years after a fire; its 176 stained-glass windows (10,000 m² of glass) still use pigment formulas that modern science cannot fully replicate"},
    {"n":"Westminster Abbey","ac":"Henry de Reyns (Gothic rebuild)","yr":"960 AD (rebuilt 1245)","lo":"London, UK","st":"Gothic","co":"United Kingdom","fa":"Every English monarch since 1066 has been crowned here; over 3,300 people are buried within its walls including Darwin, Newton, and Chaucer"},
    {"n":"Basilica di San Marco","ac":"Unknown Byzantine architects","yr":"828-1071 AD","lo":"Venice, Italy","st":"Byzantine","co":"Italy","fa":"Its mosaics cover 8,000 m² of interior surfaces; built to house the stolen relics of Saint Mark - Venetian merchants smuggled the body out of Alexandria in 828 AD"},
    {"n":"Florence Cathedral","ac":"Arnolfo di Cambio, Brunelleschi (dome)","yr":"1296-1436","lo":"Florence, Italy","st":"Gothic / Renaissance","co":"Italy","fa":"The dome went uncovered for 140 years - nobody knew how to build it; Brunelleschi invented an entirely new structural system to close it, keeping the method secret"},
    {"n":"Alhambra","ac":"Muhammad III, Yusuf I","yr":"1238-1358","lo":"Granada, Spain","st":"Moorish / Nasrid","co":"Spain","fa":"The stalactite ceilings (muqarnas) create the illusion of infinity; every surface is covered in geometric patterns and Arabic calligraphy - Islamic art at its supreme peak"},
    {"n":"Mezquita de Córdoba","ac":"Abd al-Rahman I","yr":"785-987 AD","lo":"Córdoba, Spain","st":"Moorish","co":"Spain","fa":"The forest of 856 striped double arches is an optical wonder; a Christian cathedral was built inside it in 1523 - a unique layering of civilizations in one building"},
    {"n":"Shwedagon Pagoda","ac":"Unknown (attr. Mon people)","yr":"~1450 (rebuilt)","lo":"Yangon, Myanmar","st":"Buddhist","co":"Myanmar","fa":"The 99-meter gilded stupa is covered in 27 tonnes of gold leaf and 4,531 diamonds; it enshrines eight sacred hairs of the Buddha and draws millions of pilgrims"},
    {"n":"Paro Taktsang","ac":"Unknown Bhutanese architects","yr":"1692","lo":"Paro Valley, Bhutan","st":"Dzong (Himalayan)","co":"Bhutan","fa":"The 'Tiger's Nest' monastery clings to a 900-meter granite cliff; legend says Guru Rinpoche flew to this site on a tigress - monks have lived here for over 300 years"},
    {"n":"Potala Palace","ac":"Unknown Tibetan architects","yr":"1645-1694","lo":"Lhasa, Tibet (China)","st":"Tibetan","co":"China","fa":"Built at 3,700 meters altitude; the red wall and white walls each have distinct structural and spiritual meaning - it contains 1,000 rooms and 10,000 shrines"},
    {"n":"Kinkaku-ji","ac":"Ashikaga Yoshimitsu","yr":"1397 (rebuilt 1955)","lo":"Kyoto, Japan","st":"Muromachi","co":"Japan","fa":"The top two floors are covered in pure gold leaf; a novice monk burned it down in 1950 out of obsession - an event immortalized in Mishima's famous novel"},
    {"n":"Topkapi Palace","ac":"Unknown Ottoman architects","yr":"1459-1465","lo":"Istanbul, Turkey","st":"Ottoman","co":"Turkey","fa":"Housed up to 4,000 people and governed the Ottoman Empire for 400 years; the Harem contained up to 300 women and a complex hierarchy enforced by eunuch guards"},
    {"n":"Neuschwanstein Castle","ac":"Eduard Riedel, Georg von Dollmann","yr":"1869-1886","lo":"Schwangau, Bavaria, Germany","st":"Romanesque Revival","co":"Germany","fa":"Commissioned by 'Mad King' Ludwig II, who died before completion; it inspired Sleeping Beauty Castle - over 60 million visitors have come to see the fantasy made real"},
    {"n":"Mont Saint-Michel","ac":"Various abbots","yr":"~966 (abbey)","lo":"Normandy, France","st":"Romanesque / Gothic","co":"France","fa":"Built on a tidal island that becomes completely surrounded by sea; the abbey seems to float at high tide - it is both a fortress and a spiritual ascent in stone"},
    {"n":"Château de Chambord","ac":"Domenico da Cortona (attr.)","yr":"1519-1547","lo":"Loir-et-Cher, France","st":"French Renaissance","co":"France","fa":"Its double-helix staircase - two spirals that intertwine but never meet - is attributed to Leonardo da Vinci; the 440 rooms were never all furnished at once"},
    {"n":"Château de Chenonceau","ac":"Philibert de l'Orme (bridge)","yr":"1514-1576","lo":"Chenonceaux, France","st":"French Renaissance","co":"France","fa":"Spans the Cher River entirely on a bridge; passed between two rival royal mistresses - Diane de Poitiers and Catherine de Medici - and shows both women's tastes"},
    # ── Versailles & Baroque ───────────────────────────────────────────────────
    {"n":"Versailles Palace","ac":"Louis Le Vau, Jules Hardouin-Mansart","yr":"1661-1710","lo":"Versailles, France","st":"Baroque","co":"France","fa":"The Hall of Mirrors uses 357 mirrors; Louis XIV moved his entire court here - 20,000 people including servants - to control the French nobility through proximity"},
    {"n":"St. Peter's Basilica","ac":"Michelangelo, Maderno, Bernini","yr":"1506-1626","lo":"Vatican City","st":"Renaissance / Baroque","co":"Vatican","fa":"Michelangelo designed the dome at 71, knowing he would never see it built; its nave holds 60,000 people - it remained the world's largest church for 1,300 years"},
    {"n":"St Paul's Cathedral","ac":"Christopher Wren","yr":"1675-1710","lo":"London, UK","st":"Baroque","co":"United Kingdom","fa":"Wren completed 51 London churches after the Great Fire of 1666; St Paul's dome has a 'whispering gallery' - a word spoken at the wall can be heard across the full diameter"},
    {"n":"Panthéon (Paris)","ac":"Jacques-Germain Soufflot","yr":"1758-1790","lo":"Paris, France","st":"Neoclassical","co":"France","fa":"Originally a church, converted to a secular mausoleum; Foucault's pendulum - proving Earth's rotation - was suspended from its dome in 1851 in a dramatic public experiment"},
    # ── XIXe siècle ───────────────────────────────────────────────────────────
    {"n":"Eiffel Tower","ac":"Gustave Eiffel","yr":"1889","lo":"Paris, France","st":"Iron Structure","co":"France","fa":"Built for the 1889 World's Fair as a temporary structure; Parisians hated it ('the iron asparagus') - saved only because it served as a radio tower from 1900"},
    {"n":"Big Ben","ac":"Charles Barry, Augustus Pugin","yr":"1859","lo":"London, UK","st":"Gothic Revival","co":"United Kingdom","fa":"'Big Ben' refers only to the 13.7-tonne bell inside the tower; officially called the Elizabeth Tower - it has been silent only twice since 1859 for world wars"},
    {"n":"Arc de Triomphe","ac":"Jean Chalgrin","yr":"1806-1836","lo":"Paris, France","st":"Neoclassical","co":"France","fa":"Napoleon commissioned it after Austerlitz but died before completion; 12 avenues radiate from it - navigating the roundabout has no rules and produces 2 accidents daily"},
    {"n":"Brooklyn Bridge","ac":"John Roebling, Washington Roebling","yr":"1869-1883","lo":"New York, USA","st":"Gothic Revival / Engineering","co":"USA","fa":"John Roebling died designing it; his son Washington was paralyzed by caisson disease during construction; his wife Emily supervised the final decade of building"},
    {"n":"Sacré-Cœur","ac":"Paul Abadie","yr":"1875-1914","lo":"Paris, France","st":"Romano-Byzantine","co":"France","fa":"Built as expiation for the sins of France after the 1870 war; its travertine stone bleaches whiter when it rains - the more it ages, the whiter it becomes"},
    {"n":"Flatiron Building","ac":"Daniel Burnham","yr":"1902","lo":"New York, USA","st":"Beaux-Arts","co":"USA","fa":"Its 6-meter-wide prow at 23rd Street created wind tunnels so strong that police repeatedly moved gawking crowds - giving rise to the expression '23 skidoo'"},
    # ── Art Déco & Modernisme précoce ────────────────────────────────────────
    {"n":"Empire State Building","ac":"Shreve, Lamb & Harmon","yr":"1930-1931","lo":"New York, USA","st":"Art Deco","co":"USA","fa":"Built in 410 days at a rate of 4.5 floors per week; it reclaimed New York's tallest title after 9/11 and has been struck by lightning over 100 times annually"},
    {"n":"Chrysler Building","ac":"William Van Alen","yr":"1929-1930","lo":"New York, USA","st":"Art Deco","co":"USA","fa":"A race for the world's tallest: Van Alen secretly assembled a 38-meter spire inside the building and raised it in 90 minutes to win by 3 meters"},
    {"n":"Sagrada Família","ac":"Antoni Gaudí","yr":"1882-ongoing","lo":"Barcelona, Spain","st":"Catalan Modernism","co":"Spain","fa":"Under construction for over 140 years; Gaudí is buried in its crypt; the building is funded entirely by entrance fees - no public money, no sponsors"},
    {"n":"Casa Batlló","ac":"Antoni Gaudí","yr":"1904-1906","lo":"Barcelona, Spain","st":"Catalan Modernism","co":"Spain","fa":"The façade tiles ripple like dragon scales and the roof resembles its spine; every element - from door handles to staircase shapes - was personally designed by Gaudí"},
    {"n":"La Pedrera","ac":"Antoni Gaudí","yr":"1906-1912","lo":"Barcelona, Spain","st":"Catalan Modernism","co":"Spain","fa":"No straight lines or angles anywhere; the undulating stone facade and warrior-helmet chimneys are a UNESCO World Heritage site - Gaudí called it 'a quarry'"},
    # ── Modernisme international ──────────────────────────────────────────────
    {"n":"Bauhaus Dessau","ac":"Walter Gropius","yr":"1925-1926","lo":"Dessau, Germany","st":"Bauhaus / Modernism","co":"Germany","fa":"The most influential architecture school building ever built; its corner glass curtain wall - revolutionary in 1926 - inspired every office building of the 20th century"},
    {"n":"Villa Savoye","ac":"Le Corbusier","yr":"1928-1931","lo":"Poissy, France","st":"International Style","co":"France","fa":"The manifesto of modern architecture in built form: pilotis, roof garden, ribbon windows, free facade, free plan - Le Corbusier's Five Points all realized at once"},
    {"n":"Barcelona Pavilion","ac":"Ludwig Mies van der Rohe","yr":"1929 (rebuilt 1986)","lo":"Barcelona, Spain","st":"International Style","co":"Spain","fa":"Built for only six months, then demolished; so influential it was rebuilt 60 years later; its 'less is more' aesthetic - marble walls, water pool, one chair - became a manifesto"},
    {"n":"Fallingwater","ac":"Frank Lloyd Wright","yr":"1935-1939","lo":"Mill Run, Pennsylvania, USA","st":"Organic Modernism","co":"USA","fa":"Wright designed it in 2 hours the morning the client came to check progress; built over a waterfall rather than beside it - the owner wept when he saw the drawings"},
    {"n":"Guggenheim New York","ac":"Frank Lloyd Wright","yr":"1943-1959","lo":"New York, USA","st":"Organic Modernism","co":"USA","fa":"16 years from design to opening; 700 artists petitioned against it; the spiral ramp gallery was completely unprecedented - and is still debated as an exhibition space"},
    {"n":"Seagram Building","ac":"Ludwig Mies van der Rohe","yr":"1956-1958","lo":"New York, USA","st":"International Style","co":"USA","fa":"The first fully glass-and-steel tower; Mies left an empty plaza between building and street - a radical act that inspired NYC's zoning laws and spawned the public plaza"},
    {"n":"Farnsworth House","ac":"Ludwig Mies van der Rohe","yr":"1945-1951","lo":"Plano, Illinois, USA","st":"International Style","co":"USA","fa":"A single room of glass and steel suspended above the floodplain; the client sued Mies for cost overruns and privacy violations - the lawsuit became a legal landmark"},
    {"n":"Salk Institute","ac":"Louis Kahn","yr":"1959-1965","lo":"La Jolla, California, USA","st":"Brutalism / Modernism","co":"USA","fa":"Jonas Salk asked Kahn to design 'a lab worthy of Picasso'; the central plaza with its stone channel directing water to the Pacific sunset is considered perfect architectural composition"},
    {"n":"Sydney Opera House","ac":"Jørn Utzon","yr":"1959-1973","lo":"Sydney, Australia","st":"Expressionist Modernism","co":"Australia","fa":"The 'sails' are all segments of the same sphere (radius 75.2 m); Utzon resigned before completion and never saw the finished building - he never returned to Australia"},
    {"n":"TWA Flight Center","ac":"Eero Saarinen","yr":"1962","lo":"New York (JFK), USA","st":"Expressionist Modernism","co":"USA","fa":"Designed to evoke flight itself - two curved concrete shells like wings; decommissioned in 2001, it became the TWA Hotel in 2019, preserving the architecture intact"},
    {"n":"Louvre Pyramid","ac":"I.M. Pei","yr":"1989","lo":"Paris, France","st":"Modernism","co":"France","fa":"Commissioned amid furious opposition from Paris; it contains exactly 673 glass panes - not 666, despite what Dan Brown wrote in The Da Vinci Code"},
    {"n":"Pompidou Centre","ac":"Renzo Piano, Richard Rogers","yr":"1977","lo":"Paris, France","st":"High-Tech / Inside-Out","co":"France","fa":"All structural elements - pipes, ducts, escalators - are color-coded and exposed on the exterior; the building turned architecture inside-out and horrified Paris"},
    {"n":"Sydney Harbour Bridge","ac":"John Bradfield, Ralph Freeman","yr":"1923-1932","lo":"Sydney, Australia","st":"Steel Arch","co":"Australia","fa":"Called 'The Coathanger' by Sydneysiders; its pylons look structural but are hollow decoration - the steel arch does all the work"},
    # ── Architecture contemporaine ────────────────────────────────────────────
    {"n":"Guggenheim Bilbao","ac":"Frank Gehry","yr":"1997","lo":"Bilbao, Spain","st":"Deconstructivism","co":"Spain","fa":"The 'Bilbao Effect': the museum transformed a declining industrial city into a global cultural destination, generating $2.4B economic impact in its first decade"},
    {"n":"Burj Khalifa","ac":"Adrian Smith (SOM)","yr":"2004-2010","lo":"Dubai, UAE","st":"Neo-Futurist","co":"UAE","fa":"At 828 meters, the world's tallest building; the spire top is visible from 95 km away; water and sewage must be trucked out - no city sewer reaches that altitude"},
    {"n":"The Shard","ac":"Renzo Piano","yr":"2009-2012","lo":"London, UK","st":"Neo-Futurist","co":"United Kingdom","fa":"At 309 meters, the tallest building in Western Europe; 11,000 glass panels, each unique - no two are the same size"},
    {"n":"Burj Al Arab","ac":"Tom Wright (WS Atkins)","yr":"1994-1999","lo":"Dubai, UAE","st":"Neo-Futurist","co":"UAE","fa":"Shaped like a billowing sail on an artificial island; self-declared 7-star hotel - the helipad hosts tennis matches and helicopter pads above the Arabian Gulf"},
    {"n":"Petronas Towers","ac":"César Pelli","yr":"1992-1998","lo":"Kuala Lumpur, Malaysia","st":"Postmodern","co":"Malaysia","fa":"Tallest buildings in the world at completion (452 m); the floor plan is based on an eight-pointed Islamic star - a homage to Malaysia's Muslim culture"},
    {"n":"Walt Disney Concert Hall","ac":"Frank Gehry","yr":"1987-2003","lo":"Los Angeles, USA","st":"Deconstructivism","co":"USA","fa":"The stainless-steel panels were so reflective they concentrated heat on nearby apartments; they had to be sanded to a matte finish after opening"},
    {"n":"Heydar Aliyev Center","ac":"Zaha Hadid","yr":"2007-2012","lo":"Baku, Azerbaijan","st":"Parametric","co":"Azerbaijan","fa":"No straight lines or sharp angles anywhere - the building flows from ground to roof as one continuous surface; Zaha Hadid's defining statement of parametric architecture"},
    {"n":"CCTV Headquarters","ac":"Rem Koolhaas, Ole Scheeren (OMA)","yr":"2004-2012","lo":"Beijing, China","st":"Deconstructivism","co":"China","fa":"Two leaning towers connected at the top forming a loop; the connection was bolted at 2 AM to minimize thermal expansion - a structural engineering first"},
    {"n":"Lotus Temple","ac":"Fariborz Sahba","yr":"1979-1986","lo":"New Delhi, India","st":"Expressionist","co":"India","fa":"Open to all religions; its 27 marble-clad petals float above 9 reflective pools; one of the most visited buildings in the world with over 100 million visitors"},
    {"n":"CN Tower","ac":"John Andrews, WZMH Architects","yr":"1973-1976","lo":"Toronto, Canada","st":"Modernism","co":"Canada","fa":"At 553 meters, it was the world's tallest free-standing structure for 34 years; the glass floor lets you see 113 floors straight down - 1.5 billion people have visited"},
    {"n":"Tokyo Skytree","ac":"Nikken Sekkei","yr":"2006-2012","lo":"Tokyo, Japan","st":"Neo-Futurist","co":"Japan","fa":"At 634 meters, the world's tallest tower; its design is based on traditional Japanese castle architecture adapted for extreme earthquake resistance"},
    {"n":"Shanghai Tower","ac":"Gensler","yr":"2008-2015","lo":"Shanghai, China","st":"Neo-Futurist","co":"China","fa":"Its spiraling form reduces wind loads by nearly a quarter compared to a rectangular building - a shape that emerged from aerodynamic testing, not aesthetic choice"},
    {"n":"One World Trade Center","ac":"David Childs (SOM)","yr":"2006-2014","lo":"New York, USA","st":"Neo-Futurist","co":"USA","fa":"At exactly 1,776 feet (541 m) - the year of American independence; built on the site of the Twin Towers, its foundation walls survived 9/11 and were incorporated"},
    {"n":"Millau Viaduct","ac":"Norman Foster, Michel Virlogeux","yr":"2001-2004","lo":"Millau, France","st":"High-Tech Engineering","co":"France","fa":"The tallest bridge in the world at 343 meters (higher than the Eiffel Tower); on foggy days, cars appear to drive through clouds - a surreal and regular occurrence"},
    {"n":"Eden Project","ac":"Nicholas Grimshaw","yr":"1998-2001","lo":"Cornwall, UK","st":"High-Tech / Geodesic","co":"United Kingdom","fa":"The world's largest indoor rainforest, built in a former clay pit; the biome hexagons are inflated ETFE foil cushions, not glass - each weighing less than air"},
    {"n":"Reichstag (Foster)","ac":"Norman Foster","yr":"1994-1999 (renovation)","lo":"Berlin, Germany","st":"Contemporary","co":"Germany","fa":"Foster added a glass cupola where Nazis had removed it; the spiral ramp lets visitors walk above the parliament chamber - transparency over the politicians, literally"},
    {"n":"Harpa Concert Hall","ac":"Henning Larsen, Olafur Eliasson","yr":"2007-2011","lo":"Reykjavík, Iceland","st":"Contemporary","co":"Iceland","fa":"Its honeycomb glass façade was designed by artist Olafur Eliasson; the building reflects the harbor, sky, and Northern Lights - a different building every hour"},
    {"n":"Museum of the Future (Dubai)","ac":"Shaun Killa (Killa Design)","yr":"2017-2022","lo":"Dubai, UAE","st":"Futurist","co":"UAE","fa":"A torus-shaped building with no straight lines; the Arabic calligraphy cut into its skin serves as both decoration and the structural window system - form and text in one"},
    {"n":"National Museum of Qatar","ac":"Jean Nouvel","yr":"2010-2019","lo":"Doha, Qatar","st":"Deconstructivism","co":"Qatar","fa":"Inspired by the desert rose crystal; 539 interlocking disc shapes that seem to have crystallized from the ground - the tallest disc reaches 40 meters across"},
    {"n":"Forbidden City","ac":"Kuai Xiang (chief architect)","yr":"1406-1420","lo":"Beijing, China","st":"Ming Dynasty","co":"China","fa":"The world's largest palace complex at 72 hectares; 9,999 rooms (one short of the 10,000 of heaven); 1 million workers built it over 14 years"},
    {"n":"Taj Mahal","ac":"Ustad Ahmad Lahauri","yr":"1632-1653","lo":"Agra, India","st":"Mughal","co":"India","fa":"Built by Shah Jahan as a mausoleum for Mumtaz Mahal; the white marble changes color with the light - pink at dawn, white at noon, golden at sunset"},
    {"n":"Golden Gate Bridge","ac":"Joseph Strauss, Charles Ellis","yr":"1933-1937","lo":"San Francisco, USA","st":"Art Deco Suspension","co":"USA","fa":"The 'International Orange' color was originally a primer coat; the architect loved it and kept it. The bridge is repainted continuously - a crew never stops"},
    {"n":"MAXXI Museum","ac":"Zaha Hadid","yr":"2003-2010","lo":"Rome, Italy","st":"Deconstructivism","co":"Italy","fa":"Zaha Hadid's first completed building in Italy; concrete circulation ramps seem to pour through the galleries like flowing lava - visitor paths become part of the architecture"},
    {"n":"Suzhou Museum","ac":"I.M. Pei","yr":"2003-2006","lo":"Suzhou, China","st":"Contemporary","co":"China","fa":"Pei's final major work, designed for his ancestral home city at age 85; traditional whitewashed walls and water gardens in perfect dialogue with a modern geometry"},
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
    total = len(architecture)
    found = 0
    for i, s in enumerate(architecture):
        title = WIKI_EN.get(s["n"], s["n"])
        img = wiki_img(title)
        s["im"] = img
        if img: found += 1
        status = "ok" if img else "xx"
        sys.stdout.buffer.write(f"  [{i+1:2}/{total}] {status} {s['n']}\n".encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)
    out = Path("assets/art/architecture.json")
    out.write_text(json.dumps(architecture, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    sys.stdout.buffer.write(f"\nDone: {found}/{total} images - {total} buildings total.\n".encode("utf-8"))

if __name__ == "__main__":
    main()
