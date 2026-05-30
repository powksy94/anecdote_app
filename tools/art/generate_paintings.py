import json, requests, time, os

# n=title, ar=artist, yr=year, me=medium, st=style/movement, mu=museum, fa=famous_for, im=image_url

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_OVERRIDES = {
    "Mona Lisa": "Mona Lisa",
    "The Starry Night": "The Starry Night",
    "The Scream": "The Scream",
    "Girl with a Pearl Earring": "Girl with a Pearl Earring",
    "The Last Supper": "The Last Supper (Leonardo)",
    "The Birth of Venus": "The Birth of Venus",
    "Las Meninas": "Las Meninas",
    "The Persistence of Memory": "The Persistence of Memory",
    "American Gothic": "American Gothic",
    "Nighthawks": "Nighthawks (painting)",
    "A Sunday on La Grande Jatte": "A Sunday on La Grande Jatte",
    "The Night Watch": "The Night Watch",
    "Guernica": "Guernica",
    "The Creation of Adam": "The Creation of Adam",
    "The Raft of the Medusa": "The Raft of the Medusa",
    "Liberty Leading the People": "Liberty Leading the People",
    "Saturn Devouring His Son": "Saturn Devouring His Son",
    "The Third of May 1808": "The Third of May 1808",
    "Les Demoiselles d'Avignon": "Les Demoiselles d'Avignon",
    "The Garden of Earthly Delights": "The Garden of Earthly Delights",
    "The Hunters in the Snow": "Hunters in the Snow",
    "The Tower of Babel": "The Tower of Babel (Bruegel)",
    "A Bar at the Folies-Bergère": "A Bar at the Folies-Bergère",
    "Le Déjeuner sur l'herbe": "Le Déjeuner sur l'herbe",
    "Bal du moulin de la Galette": "Bal du moulin de la Galette",
    "The Anatomy Lesson of Dr. Nicolaes Tulp": "The Anatomy Lesson of Dr. Nicolaes Tulp",
    "The Laughing Cavalier": "The Laughing Cavalier",
    "Christina's World": "Christina's World",
    "Campbell's Soup Cans": "Campbell's Soup Cans",
    "Marilyn Diptych": "Marilyn Diptych",
    "Whaam!": "Whaam!",
    "Napoleon Crossing the Alps": "Napoleon Crossing the Alps",
    "The Descent from the Cross": "The Descent from the Cross (Rubens)",
    "View of Toledo": "View of Toledo (painting)",
    "The Sistine Madonna": "Sistine Madonna",
    "Judith Beheading Holofernes": "Judith Beheading Holofernes (Caravaggio)",
    "Primavera": "Primavera (Botticelli)",
    "The Annunciation": "Annunciation (Fra Angelico, San Marco)",
    "The Surrender of Breda": "The Surrender of Breda",
    "The Three Graces": "The Three Graces (Rubens)",
    "Washington Crossing the Delaware": "Washington Crossing the Delaware",
    "Impression, Sunrise": "Impression, Sunrise",
    "Starry Night over the Rhône": "Starry Night over the Rhône",
    "The Potato Eaters": "The Potato Eaters",
    "The Sleeping Gypsy": "The Sleeping Gypsy",
    "The Kiss": "The Kiss (Klimt)",
    "The Dance": "The Dance (Matisse)",
    "The School of Athens": "The School of Athens",
    "Girl Before a Mirror": "Girl Before a Mirror",
    "Mont Sainte-Victoire": "Mont Sainte-Victoire (Cézanne)",
    "Olympia": "Olympia (Manet)",
    "The Large Bathers": "The Large Bathers (Cézanne)",
    "The Bedroom": "The Bedroom (van Gogh, 1889, Chicago)",
    "Sunflowers": "Sunflowers (Van Gogh series)",
    "Wheat Field with Crows": "Wheatfield with Crows",
    "The Dream": "The Dream (Rousseau)",
}

paintings_raw = [
    # ── RENAISSANCE ITALIENNE ────────────────────────────────────────────
    {"n":"Mona Lisa","ar":"Leonardo da Vinci","yr":"1503-1519","me":"Oil on poplar","st":"High Renaissance","mu":"Louvre Museum, Paris","fa":"The most visited painting in the world; her enigmatic smile and use of sfumato have fascinated viewers for 500 years"},
    {"n":"The Last Supper","ar":"Leonardo da Vinci","yr":"1495-1498","me":"Tempera on gesso","st":"High Renaissance","mu":"Santa Maria delle Grazie, Milan","fa":"Depicts the moment Jesus announces one of his apostles will betray him; used pioneering perspective to center all attention on Christ"},
    {"n":"The Birth of Venus","ar":"Sandro Botticelli","yr":"1484-1486","me":"Tempera on canvas","st":"Early Renaissance","mu":"Uffizi Gallery, Florence","fa":"One of the first large-scale paintings of a nude since antiquity; Venus emerges from the sea on a giant shell"},
    {"n":"Primavera","ar":"Sandro Botticelli","yr":"1477-1482","me":"Tempera on panel","st":"Early Renaissance","mu":"Uffizi Gallery, Florence","fa":"One of the most discussed works of Western art; its mysterious allegorical meaning has been debated for centuries"},
    {"n":"The Creation of Adam","ar":"Michelangelo","yr":"1508-1512","me":"Fresco","st":"High Renaissance","mu":"Sistine Chapel, Vatican","fa":"The iconic image of God and Adam nearly touching fingers is one of the most reproduced artworks in history"},
    {"n":"The School of Athens","ar":"Raphael","yr":"1509-1511","me":"Fresco","st":"High Renaissance","mu":"Apostolic Palace, Vatican","fa":"Depicts the greatest philosophers of antiquity gathered together; Plato and Aristotle walk at the center"},
    {"n":"The Sistine Madonna","ar":"Raphael","yr":"1512","me":"Oil on canvas","st":"High Renaissance","mu":"Gemäldegalerie, Dresden","fa":"Famous for its two cherubs (putti) at the bottom — the most reproduced detail in art history, now a universal cultural icon"},
    {"n":"The Annunciation","ar":"Fra Angelico","yr":"1438-1445","me":"Fresco","st":"Early Renaissance","mu":"Museo di San Marco, Florence","fa":"The purest expression of early Renaissance spirituality; painted in a monk's cell to inspire daily meditation"},
    # ── MANIÉRISME ET BAROQUE ─────────────────────────────────────────────
    {"n":"The Night Watch","ar":"Rembrandt van Rijn","yr":"1642","me":"Oil on canvas","st":"Dutch Golden Age","mu":"Rijksmuseum, Amsterdam","fa":"The largest and most famous work of the Dutch Golden Age; a revolutionary militia portrait showing dramatic movement and light"},
    {"n":"The Anatomy Lesson of Dr. Nicolaes Tulp","ar":"Rembrandt van Rijn","yr":"1632","me":"Oil on canvas","st":"Dutch Golden Age","mu":"Mauritshuis, The Hague","fa":"Rembrandt's first major commission; a groundbreaking group portrait showing a public dissection — science meets art"},
    {"n":"Girl with a Pearl Earring","ar":"Johannes Vermeer","yr":"1665","me":"Oil on canvas","st":"Dutch Golden Age","mu":"Mauritshuis, The Hague","fa":"Called the 'Mona Lisa of the North'; the girl's identity and the pearl's authenticity have been debated for centuries"},
    {"n":"The Milkmaid","ar":"Johannes Vermeer","yr":"1657-1658","me":"Oil on canvas","st":"Dutch Golden Age","mu":"Rijksmuseum, Amsterdam","fa":"A masterwork of everyday domestic life elevated to the sublime; Vermeer's extraordinary light effects make the milk seem to pour in slow motion"},
    {"n":"Las Meninas","ar":"Diego Velázquez","yr":"1656","me":"Oil on canvas","st":"Spanish Baroque","mu":"Museo del Prado, Madrid","fa":"One of art history's most analyzed works; the complex composition questions the nature of representation and the role of the artist"},
    {"n":"The Surrender of Breda","ar":"Diego Velázquez","yr":"1635","me":"Oil on canvas","st":"Spanish Baroque","mu":"Museo del Prado, Madrid","fa":"Depicts a rare moment of nobility in war — the victorious Spanish general prevents his soldiers from humiliating the defeated Dutch"},
    {"n":"View of Toledo","ar":"El Greco","yr":"1596-1600","me":"Oil on canvas","st":"Mannerism","mu":"Metropolitan Museum of Art, New York","fa":"The only pure landscape El Greco painted; its dramatic sky and distorted city inspired the Expressionists 300 years later"},
    {"n":"Judith Beheading Holofernes","ar":"Caravaggio","yr":"1598-1599","me":"Oil on canvas","st":"Baroque","mu":"Galleria Nazionale d'Arte Antica, Rome","fa":"Caravaggio's shocking realism shows Judith's determined expression as she beheads the tyrant — revolutionary in its visceral power"},
    {"n":"The Descent from the Cross","ar":"Peter Paul Rubens","yr":"1612-1614","me":"Oil on panel","st":"Flemish Baroque","mu":"Cathedral of Our Lady, Antwerp","fa":"Rubens's masterpiece; the dynamic composition and emotional intensity made it the most influential altarpiece of the 17th century"},
    {"n":"The Three Graces","ar":"Peter Paul Rubens","yr":"1630-1635","me":"Oil on panel","st":"Flemish Baroque","mu":"Museo del Prado, Madrid","fa":"Rubens's celebration of feminine beauty; the three women are thought to include his young second wife Isabella Brant"},
    {"n":"The Laughing Cavalier","ar":"Frans Hals","yr":"1624","me":"Oil on canvas","st":"Dutch Golden Age","mu":"The Wallace Collection, London","fa":"Despite the title, the man is not laughing — his slight smile and arrogant posture make him one of portraiture's most vivid personalities"},
    # ── XVIIIe SIÈCLE ET NÉOCLASSICISME ──────────────────────────────────
    {"n":"The Garden of Earthly Delights","ar":"Hieronymus Bosch","yr":"1490-1510","me":"Oil on oak panels","st":"Northern Renaissance","mu":"Museo del Prado, Madrid","fa":"The most mysterious triptych in art history; its surreal visions of paradise and hell continue to baffle and fascinate art historians"},
    {"n":"The Tower of Babel","ar":"Pieter Bruegel the Elder","yr":"1563","me":"Oil on panel","st":"Northern Renaissance","mu":"Kunsthistorisches Museum, Vienna","fa":"A masterpiece of architectural fantasy showing thousands of workers; Bruegel modeled the tower on the Colosseum in Rome"},
    {"n":"The Hunters in the Snow","ar":"Pieter Bruegel the Elder","yr":"1565","me":"Oil on panel","st":"Northern Renaissance","mu":"Kunsthistorisches Museum, Vienna","fa":"One of the most iconic winter landscapes ever painted; Bruegel captured the peasant experience of winter with extraordinary realism"},
    {"n":"Napoleon Crossing the Alps","ar":"Jacques-Louis David","yr":"1801","me":"Oil on canvas","st":"Neoclassicism","mu":"Château de Malmaison, Rueil-Malmaison","fa":"A heroic propaganda image — Napoleon insisted on being shown 'calm on a fiery steed'; in reality he crossed on a mule"},
    # ── ROMANTISME ────────────────────────────────────────────────────────
    {"n":"The Raft of the Medusa","ar":"Théodore Géricault","yr":"1818-1819","me":"Oil on canvas","st":"Romanticism","mu":"Louvre Museum, Paris","fa":"Based on a real scandal — shipwreck survivors were abandoned; the monumental painting caused a political storm at the Paris Salon"},
    {"n":"Liberty Leading the People","ar":"Eugène Delacroix","yr":"1830","me":"Oil on canvas","st":"Romanticism","mu":"Louvre Museum, Paris","fa":"The allegorical figure of Liberty leads revolutionaries over the barricades; inspired the Statue of Liberty and countless political images"},
    {"n":"The Third of May 1808","ar":"Francisco Goya","yr":"1814","me":"Oil on canvas","st":"Romanticism","mu":"Museo del Prado, Madrid","fa":"One of the first anti-war paintings; the anonymous white-shirted man facing the firing squad became a symbol of all innocent victims of war"},
    {"n":"Saturn Devouring His Son","ar":"Francisco Goya","yr":"1819-1823","me":"Oil on plaster","st":"Dark Romanticism","mu":"Museo del Prado, Madrid","fa":"Painted secretly on his dining room wall during his darkest years of deafness and isolation — one of art's most disturbing masterpieces"},
    {"n":"Washington Crossing the Delaware","ar":"Emanuel Leutze","yr":"1851","me":"Oil on canvas","st":"Romanticism","mu":"Metropolitan Museum of Art, New York","fa":"America's most famous historical painting; the dramatic night crossing that changed the Revolutionary War's outcome"},
    # ── RÉALISME ET IMPRESSIONNISME ───────────────────────────────────────
    {"n":"Olympia","ar":"Édouard Manet","yr":"1863","me":"Oil on canvas","st":"Realism","mu":"Musée d'Orsay, Paris","fa":"The nude woman's direct, unapologetic gaze at the viewer caused a scandal at the 1865 Salon — it challenged the idealized nude tradition"},
    {"n":"Le Déjeuner sur l'herbe","ar":"Édouard Manet","yr":"1863","me":"Oil on canvas","st":"Realism","mu":"Musée d'Orsay, Paris","fa":"The naked woman picnicking with fully dressed men caused moral outrage — Napoleon III himself declared it an offense to modesty"},
    {"n":"A Bar at the Folies-Bergère","ar":"Édouard Manet","yr":"1882","me":"Oil on canvas","st":"Impressionism","mu":"Courtauld Gallery, London","fa":"Manet's last major painting; the impossible reflections in the mirror have puzzled art historians for over a century"},
    {"n":"Impression, Sunrise","ar":"Claude Monet","yr":"1872","me":"Oil on canvas","st":"Impressionism","mu":"Musée Marmottan Monet, Paris","fa":"The painting that gave Impressionism its name — a critic used it mockingly, but the movement embraced it proudly"},
    {"n":"Bal du moulin de la Galette","ar":"Pierre-Auguste Renoir","yr":"1876","me":"Oil on canvas","st":"Impressionism","mu":"Musée d'Orsay, Paris","fa":"A joyful celebration of Parisian working-class leisure; the dappled light filtering through trees became Renoir's signature effect"},
    {"n":"A Sunday on La Grande Jatte","ar":"Georges Seurat","yr":"1886","me":"Oil on canvas","st":"Post-Impressionism / Pointillism","mu":"Art Institute of Chicago","fa":"Created entirely from millions of tiny dots of color — Seurat invented Pointillism to apply scientific color theory to painting"},
    {"n":"The Potato Eaters","ar":"Vincent van Gogh","yr":"1885","me":"Oil on canvas","st":"Post-Impressionism","mu":"Van Gogh Museum, Amsterdam","fa":"Van Gogh's first major work; deliberately dark and crude to show peasant life honestly — 'the color of a good, dusty potato'"},
    {"n":"Sunflowers","ar":"Vincent van Gogh","yr":"1888","me":"Oil on canvas","st":"Post-Impressionism","mu":"National Gallery, London","fa":"One of the world's most recognized paintings; Van Gogh used 'chrome yellow' to capture the radiance and vitality of living flowers"},
    {"n":"The Starry Night","ar":"Vincent van Gogh","yr":"1889","me":"Oil on canvas","st":"Post-Impressionism","mu":"MoMA, New York","fa":"Painted from memory in an asylum, it combines emotional intensity with swirling cosmic energy — the ultimate expression of Van Gogh's inner vision"},
    {"n":"Wheat Field with Crows","ar":"Vincent van Gogh","yr":"1890","me":"Oil on canvas","st":"Post-Impressionism","mu":"Van Gogh Museum, Amsterdam","fa":"Often cited as his final painting before his death; the stormy sky and fleeing crows create an overwhelming sense of menace and despair"},
    {"n":"Starry Night over the Rhône","ar":"Vincent van Gogh","yr":"1888","me":"Oil on canvas","st":"Post-Impressionism","mu":"Musée d'Orsay, Paris","fa":"Van Gogh painted it at night under lamplight; the reflections of gas lights on water anticipate his later, more turbulent night skies"},
    {"n":"The Bedroom","ar":"Vincent van Gogh","yr":"1889","me":"Oil on canvas","st":"Post-Impressionism","mu":"Art Institute of Chicago","fa":"Van Gogh painted three versions of his simple bedroom in Arles; the tilted perspective and bold colors convey both comfort and anxiety"},
    {"n":"Mont Sainte-Victoire","ar":"Paul Cézanne","yr":"1887","me":"Oil on canvas","st":"Post-Impressionism","mu":"Courtauld Gallery, London","fa":"Cézanne painted this mountain over 60 times; his geometric simplification of nature directly inspired Cubism and modern art"},
    {"n":"The Large Bathers","ar":"Paul Cézanne","yr":"1906","me":"Oil on canvas","st":"Post-Impressionism","mu":"Philadelphia Museum of Art","fa":"Cézanne's final masterpiece, worked on for 7 years; the monumental composition of female bathers in nature inspired Picasso and Matisse"},
    # ── XXe SIÈCLE ───────────────────────────────────────────────────────
    {"n":"The Scream","ar":"Edvard Munch","yr":"1893","me":"Oil, tempera, pastel on cardboard","st":"Symbolism / Expressionism","mu":"National Museum, Oslo","fa":"The ultimate image of modern existential anxiety; Munch wrote of feeling 'an infinite scream passing through nature' while walking"},
    {"n":"The Kiss","ar":"Gustav Klimt","yr":"1907-1908","me":"Oil and gold leaf on canvas","st":"Symbolism / Art Nouveau","mu":"Österreichische Galerie Belvedere, Vienna","fa":"Austria's most treasured artwork; the couple's embrace under a golden mosaic blanket merges human passion with divine transcendence"},
    {"n":"The Sleeping Gypsy","ar":"Henri Rousseau","yr":"1897","me":"Oil on canvas","st":"Naive Art / Post-Impressionism","mu":"MoMA, New York","fa":"Rousseau's dreamlike masterpiece — a lion inexplicably sniffs a sleeping woman under a full moon in a desert without attacking her"},
    {"n":"The Dream","ar":"Henri Rousseau","yr":"1910","me":"Oil on canvas","st":"Naive Art","mu":"MoMA, New York","fa":"Rousseau's final work; a naked woman on a velvet sofa floats in a jungle — its magical unreality prefigures Surrealism"},
    {"n":"The Dance","ar":"Henri Matisse","yr":"1910","me":"Oil on canvas","st":"Fauvism","mu":"Hermitage Museum, Saint Petersburg","fa":"Five dancing figures in a ring against a blue-green background — one of the most important paintings of the 20th century"},
    {"n":"Les Demoiselles d'Avignon","ar":"Pablo Picasso","yr":"1907","me":"Oil on canvas","st":"Proto-Cubism","mu":"MoMA, New York","fa":"The painting that changed everything; its fragmented faces influenced by African masks launched Cubism and the entire modern art movement"},
    {"n":"Guernica","ar":"Pablo Picasso","yr":"1937","me":"Oil on canvas","st":"Cubism / Expressionism","mu":"Museo Reina Sofía, Madrid","fa":"The most powerful anti-war painting ever made; created in response to the Nazi bombing of the Basque town during the Spanish Civil War"},
    {"n":"Girl Before a Mirror","ar":"Pablo Picasso","yr":"1932","me":"Oil on canvas","st":"Cubism","mu":"MoMA, New York","fa":"A Cubist meditation on female identity; the woman sees a darker, more knowing reflection of herself — youth confronting mortality"},
    {"n":"The Persistence of Memory","ar":"Salvador Dalí","yr":"1931","me":"Oil on canvas","st":"Surrealism","mu":"MoMA, New York","fa":"The melting watches in a dreamlike Catalan landscape have become the defining image of Surrealism and of the relativity of time"},
    {"n":"American Gothic","ar":"Grant Wood","yr":"1930","me":"Oil on beaverboard","st":"American Regionalism","mu":"Art Institute of Chicago","fa":"The stern farmer with a pitchfork and his daughter became the definitive image of rural American values — the most parodied painting in history"},
    {"n":"Nighthawks","ar":"Edward Hopper","yr":"1942","me":"Oil on canvas","st":"American Realism","mu":"Art Institute of Chicago","fa":"Three strangers in a late-night diner with no door out — the most evocative image of urban loneliness in American art"},
    {"n":"Christina's World","ar":"Andrew Wyeth","yr":"1948","me":"Tempera on hardboard","st":"Regionalism / Magic Realism","mu":"MoMA, New York","fa":"A young woman crawls toward a distant farmhouse; only later do we learn she had polio — her struggle gives the painting hidden depth"},
    {"n":"Campbell's Soup Cans","ar":"Andy Warhol","yr":"1962","me":"Synthetic polymer paint on canvas","st":"Pop Art","mu":"MoMA, New York","fa":"32 canvases of everyday soup cans that asked: what IS art? Warhol's answer — anything can be elevated by simply looking at it"},
    {"n":"Marilyn Diptych","ar":"Andy Warhol","yr":"1962","me":"Silkscreen ink on canvas","st":"Pop Art","mu":"Tate Modern, London","fa":"Made weeks after Monroe's death; the repeated fading image on the right side transforms celebrity worship into a meditation on mortality"},
    {"n":"Whaam!","ar":"Roy Lichtenstein","yr":"1963","me":"Acrylic and oil on canvas","st":"Pop Art","mu":"Tate Modern, London","fa":"Adapted from a DC comic book, Lichtenstein's explosion canvas questioned the boundary between high art and popular culture"},
    # ── ART ORIENTAL ET NON-OCCIDENTAL ───────────────────────────────────
    {"n":"The Great Wave off Kanagawa","ar":"Katsushika Hokusai","yr":"1831","me":"Woodblock print","st":"Ukiyo-e","mu":"Metropolitan Museum of Art, New York","fa":"The most recognized work of Japanese art; the towering wave dwarfing Mount Fuji combines beauty and terror in a single image"},
    {"n":"The Wanderer above the Sea of Fog","ar":"Caspar David Friedrich","yr":"1818","me":"Oil on canvas","st":"Romanticism","mu":"Kunsthalle Hamburg","fa":"A man contemplates a misty landscape from a mountain — the defining image of the Romantic sublime and of human smallness before nature"},
    {"n":"The Arnolfini Portrait","ar":"Jan van Eyck","yr":"1434","me":"Oil on oak panel","st":"Northern Renaissance","mu":"National Gallery, London","fa":"One of the earliest oil paintings; the convex mirror in the background reflects the entire scene including possibly the artist himself"},
    {"n":"Las Meninas — Las Hilanderas","ar":"Diego Velázquez","yr":"1657","me":"Oil on canvas","st":"Spanish Baroque","mu":"Museo del Prado, Madrid","fa":"Velázquez's meditation on the nature of art and labor; Picasso was so obsessed with this work he painted 58 variations of it"},
    {"n":"The Gleaners","ar":"Jean-François Millet","yr":"1857","me":"Oil on canvas","st":"Realism","mu":"Musée d'Orsay, Paris","fa":"Three women gleaning leftover grain after harvest; when first shown, it shocked wealthy viewers as a political statement about poverty"},
    {"n":"The Milkmaid (Vermeer)","ar":"Johannes Vermeer","yr":"1657-1658","me":"Oil on canvas","st":"Dutch Golden Age","mu":"Rijksmuseum, Amsterdam","fa":"Vermeer's mastery of light makes the pouring milk almost hypnotic; the humble domestic scene is elevated to quiet, timeless perfection"},
    {"n":"The Birth of Venus (Cabanel)","ar":"Alexandre Cabanel","yr":"1863","me":"Oil on canvas","st":"Academic Art","mu":"Musée d'Orsay, Paris","fa":"Napoleon III bought it immediately at the 1863 Salon — the establishment's ideal nude vs. Manet's scandalous Olympia shown the same year"},
    {"n":"The Luncheon of the Boating Party","ar":"Pierre-Auguste Renoir","yr":"1881","me":"Oil on canvas","st":"Impressionism","mu":"The Phillips Collection, Washington D.C.","fa":"A summer afternoon on the Seine packed with Renoir's friends; his future wife Aline holds a small dog in the lower left corner"},
    {"n":"Sunday Afternoon on the Island of La Grande Jatte","ar":"Georges Seurat","yr":"1886","me":"Oil on canvas","st":"Pointillism","mu":"Art Institute of Chicago","fa":"Seurat spent 2 years applying millions of tiny dots; the stiff, frozen figures in the park give it an eerie, dreamlike quality"},
    {"n":"The Card Players","ar":"Paul Cézanne","yr":"1892-1895","me":"Oil on canvas","st":"Post-Impressionism","mu":"Musée d'Orsay, Paris","fa":"Cézanne painted 5 versions of peasants playing cards; the Qatar royal family paid $250 million for one version in 2011 — then a record"},
    {"n":"Water Lilies","ar":"Claude Monet","yr":"1906","me":"Oil on canvas","st":"Impressionism","mu":"Art Institute of Chicago","fa":"One of 250 paintings in Monet's Water Lilies series; his garden at Giverny became an obsession that produced one of history's greatest cycles"},
    {"n":"Self-Portrait with Bandaged Ear","ar":"Vincent van Gogh","yr":"1889","me":"Oil on canvas","st":"Post-Impressionism","mu":"Courtauld Gallery, London","fa":"Van Gogh painted this two weeks after cutting off part of his ear during a breakdown; his calm expression is deeply unsettling in context"},
    {"n":"The Night Café","ar":"Vincent van Gogh","yr":"1888","me":"Oil on canvas","st":"Post-Impressionism","mu":"Yale University Art Gallery","fa":"Van Gogh wrote that he used red and green to express 'the terrible passions of humanity'; he called it one of his ugliest paintings"},
    {"n":"Café Terrace at Night","ar":"Vincent van Gogh","yr":"1888","me":"Oil on canvas","st":"Post-Impressionism","mu":"Kröller-Müller Museum, Otterlo","fa":"The first painting Van Gogh made at night, outdoors — he set up candles on his hat to paint the warm glow of the café against the starry sky"},
]

def fetch_wikipedia_image(name, artist):
    wiki_title = WIKI_OVERRIDES.get(name, name)
    try:
        r = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={"action":"query","titles":wiki_title,"prop":"pageimages",
                    "format":"json","pithumbsize":600,"redirects":1},
            headers=HEADERS, timeout=8
        )
        if r.status_code != 200:
            return None
        for page in r.json().get("query",{}).get("pages",{}).values():
            src = page.get("thumbnail",{}).get("source")
            if src:
                return src
        # Fallback: search with artist name
        r2 = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={"action":"query","titles":f"{name} {artist}","prop":"pageimages",
                    "format":"json","pithumbsize":600,"redirects":1},
            headers=HEADERS, timeout=8
        )
        if r2.status_code == 200:
            for page in r2.json().get("query",{}).get("pages",{}).values():
                src = page.get("thumbnail",{}).get("source")
                if src:
                    return src
        return None
    except Exception:
        return None

print(f"Fetching images for {len(paintings_raw)} paintings...")
result = []
for i, p in enumerate(paintings_raw):
    img = fetch_wikipedia_image(p["n"], p["ar"])
    p["im"] = img
    result.append(p)
    status = "ok" if img else "x"
    print(f"  [{i+1}/{len(paintings_raw)}] {status} {p['n']} — {p['ar']}")
    time.sleep(0.3)

os.makedirs("assets/art", exist_ok=True)
with open("assets/art/paintings.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, separators=(',',':'))

found = sum(1 for p in result if p["im"])
print(f"\n{len(result)} tableaux generes. Images: {found}/{len(result)}.")
