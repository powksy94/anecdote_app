import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=name, na=nationality, bo=born, di=died, mo=movement, fa=famous_for, im=imageUrl

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_EN = {
    "Leonardo da Vinci":    "Leonardo da Vinci",
    "Michelangelo":         "Michelangelo",
    "Raphael":              "Raphael (painter)",
    "Sandro Botticelli":    "Sandro Botticelli",
    "Titian":               "Titian",
    "Tintoretto":           "Tintoretto",
    "Caravaggio":           "Caravaggio",
    "Peter Paul Rubens":    "Peter Paul Rubens",
    "Rembrandt":            "Rembrandt",
    "Johannes Vermeer":     "Johannes Vermeer",
    "Diego Velazquez":      "Diego Velazquez",
    "El Greco":             "El Greco",
    "Francisco Goya":       "Francisco Goya",
    "William Turner":       "J. M. W. Turner",
    "Eugene Delacroix":     "Eugene Delacroix",
    "Gustave Courbet":      "Gustave Courbet",
    "Jean-Auguste-Dominique Ingres": "Jean-Auguste-Dominique Ingres",
    "Edouard Manet":        "Edouard Manet",
    "Claude Monet":         "Claude Monet",
    "Edgar Degas":          "Edgar Degas",
    "Pierre-Auguste Renoir": "Pierre-Auguste Renoir",
    "Paul Cezanne":         "Paul Cezanne",
    "Vincent van Gogh":     "Vincent van Gogh",
    "Paul Gauguin":         "Paul Gauguin",
    "Georges Seurat":       "Georges Seurat",
    "Henri de Toulouse-Lautrec": "Henri de Toulouse-Lautrec",
    "Camille Pissarro":     "Camille Pissarro",
    "Gustav Klimt":         "Gustav Klimt",
    "Egon Schiele":         "Egon Schiele",
    "Edvard Munch":         "Edvard Munch",
    "Alphonse Mucha":       "Alphonse Mucha",
    "Henri Matisse":        "Henri Matisse",
    "Pablo Picasso":        "Pablo Picasso",
    "Georges Braque":       "Georges Braque",
    "Marcel Duchamp":       "Marcel Duchamp",
    "Wassily Kandinsky":    "Wassily Kandinsky",
    "Paul Klee":            "Paul Klee",
    "Piet Mondrian":        "Piet Mondrian",
    "Kazimir Malevich":     "Kazimir Malevich",
    "Max Ernst":            "Max Ernst",
    "Salvador Dali":        "Salvador Dali",
    "Rene Magritte":        "Rene Magritte",
    "Joan Miro":            "Joan Miro",
    "Marc Chagall":         "Marc Chagall",
    "Amedeo Modigliani":    "Amedeo Modigliani",
    "Giorgio de Chirico":   "Giorgio de Chirico",
    "Frida Kahlo":          "Frida Kahlo",
    "Diego Rivera":         "Diego Rivera",
    "Katsushika Hokusai":   "Katsushika Hokusai",
    "Utagawa Hiroshige":    "Utagawa Hiroshige",
    "Jackson Pollock":      "Jackson Pollock",
    "Mark Rothko":          "Mark Rothko",
    "Willem de Kooning":    "Willem de Kooning",
    "Francis Bacon":        "Francis Bacon (artist)",
    "Lucian Freud":         "Lucian Freud",
    "Andy Warhol":          "Andy Warhol",
    "Roy Lichtenstein":     "Roy Lichtenstein",
    "David Hockney":        "David Hockney",
    "Jean-Michel Basquiat": "Jean-Michel Basquiat",
    "Gerhard Richter":      "Gerhard Richter",
    "Yayoi Kusama":         "Yayoi Kusama",
    "Ai Weiwei":            "Ai Weiwei",
    "Banksy":               "Banksy",
    "Fernando Botero":      "Fernando Botero",
    "Georgia O'Keeffe":     "Georgia O'Keeffe",
    "Edward Hopper":        "Edward Hopper",
    "Grant Wood":           "Grant Wood",
    "Andrew Wyeth":         "Andrew Wyeth",
    "Jasper Johns":         "Jasper Johns",
    "Robert Rauschenberg":  "Robert Rauschenberg",
    "Cy Twombly":           "Cy Twombly",
    "James Whistler":       "James McNeill Whistler",
    "John Singer Sargent":  "John Singer Sargent",
    "Winslow Homer":        "Winslow Homer",
    "Paul Signac":          "Paul Signac",
    "Alfred Sisley":        "Alfred Sisley",
    "Berthe Morisot":       "Berthe Morisot",
    "Mary Cassatt":         "Mary Cassatt",
}

artists = [
    # ── Renaissance italienne ───────────────────────────────────────────────
    {"n":"Leonardo da Vinci","na":"Italian","bo":"1452","di":"1519","mo":"High Renaissance","fa":"The ultimate 'Renaissance man': painter, sculptor, architect, engineer, anatomist, and musician — he left only about 15 completed paintings yet changed art forever"},
    {"n":"Michelangelo","na":"Italian","bo":"1475","di":"1564","mo":"High Renaissance","fa":"Spent 4 years painting the Sistine Chapel ceiling lying on scaffolding; he also created David, the Pieta, and designed St. Peter's dome — at age 71"},
    {"n":"Raphael","na":"Italian","bo":"1483","di":"1520","mo":"High Renaissance","fa":"Died at 37 leaving 300 works; his The School of Athens placed all of history's great thinkers together in one room — the ultimate image of intellectual ambition"},
    {"n":"Sandro Botticelli","na":"Italian","bo":"1445","di":"1510","mo":"Early Renaissance","fa":"Birth of Venus was considered scandalous when unveiled; he burned many of his own works under Savonarola's influence, then was forgotten for 400 years before rediscovery"},
    {"n":"Titian","na":"Italian","bo":"~1488","di":"1576","mo":"Venetian Renaissance","fa":"His late style of loose, textured brushwork — applied with fingers and palette knife — anticipated Impressionism by 300 years; he painted until age 88"},
    {"n":"Tintoretto","na":"Italian","bo":"1518","di":"1594","mo":"Venetian Mannerism","fa":"He painted his way into the Scuola di San Rocco by working overnight on a ceiling — submitting a finished painting when others submitted sketches; it earned him a lifetime contract"},
    # ── Baroque & XVIIe siècle ──────────────────────────────────────────────
    {"n":"Caravaggio","na":"Italian","bo":"1571","di":"1610","mo":"Baroque","fa":"Used real beggars and prostitutes as models for saints and virgins; wanted for murder in 1606, he painted some of his greatest works while a fugitive"},
    {"n":"Peter Paul Rubens","na":"Flemish","bo":"1577","di":"1640","mo":"Baroque","fa":"His studio mass-produced paintings with 200 assistants; he simultaneously served as diplomat to three royal courts — art-world productivity redefined"},
    {"n":"Rembrandt","na":"Dutch","bo":"1606","di":"1669","mo":"Dutch Golden Age","fa":"His over 90 self-portraits form an unbroken visual autobiography from youth to bankruptcy to old age — the most intimate self-examination in art history"},
    {"n":"Johannes Vermeer","na":"Dutch","bo":"1632","di":"1675","mo":"Dutch Golden Age","fa":"Left only 34 to 36 paintings; his use of the camera obscura and perfect light have baffled experts for centuries — Girl with a Pearl Earring is his Mona Lisa"},
    {"n":"Diego Velazquez","na":"Spanish","bo":"1599","di":"1660","mo":"Baroque","fa":"Las Meninas contains two mirrors, the king, the queen, the artist, and a philosophical puzzle about who is the true subject — Picasso painted 58 variations of it"},
    {"n":"El Greco","na":"Greek / Spanish","bo":"1541","di":"1614","mo":"Mannerism","fa":"His elongated figures and hallucinogenic colours were dismissed in his time; rediscovered by Cezanne and Picasso who called him 'the first modern painter'"},
    # ── XVIIIe–XIXe siècles ────────────────────────────────────────────────
    {"n":"Francisco Goya","na":"Spanish","bo":"1746","di":"1828","mo":"Romanticism","fa":"Court painter to the Spanish royal family, he secretly depicted them as ugly and ridiculous; his Black Paintings — painted on his house walls — are the first modern nightmares"},
    {"n":"Jean-Auguste-Dominique Ingres","na":"French","bo":"1780","di":"1867","mo":"Neoclassicism","fa":"His nudes have anatomically impossible spines (La Grande Odalisque has three extra vertebrae); when critics pointed this out, he refused to change them"},
    {"n":"William Turner","na":"British","bo":"1775","di":"1851","mo":"Romanticism","fa":"Had himself tied to a ship's mast in a storm to observe it firsthand for a painting; his final words reportedly were 'The sun is God'"},
    {"n":"Eugene Delacroix","na":"French","bo":"1798","di":"1863","mo":"Romanticism","fa":"Liberty Leading the People was so incendiary the government refused to display it after purchase; it became the inspiration for the Statue of Liberty's face"},
    {"n":"Gustave Courbet","na":"French","bo":"1819","di":"1877","mo":"Realism","fa":"His The Origin of the World (an explicit female nude) was hidden for 130 years by successive owners including Jacques Lacan; now hangs publicly at the Musee d'Orsay"},
    {"n":"James Whistler","na":"American / British","bo":"1834","di":"1903","mo":"Aestheticism","fa":"Won a landmark libel case against John Ruskin who called his Nocturne paintings 'flinging a pot of paint in the public's face'; he was awarded one farthing in damages"},
    {"n":"Mary Cassatt","na":"American","bo":"1844","di":"1926","mo":"Impressionism","fa":"The only American in the core Impressionist group; she influenced major American collectors to buy French Impressionist art — shaping the collections of institutions like the Art Institute of Chicago"},
    {"n":"Berthe Morisot","na":"French","bo":"1841","di":"1895","mo":"Impressionism","fa":"The first woman admitted to the Impressionist inner circle; she exhibited in 7 of the 8 Impressionist exhibitions — more than any male member except Pissarro"},
    # ── Impressionnisme ─────────────────────────────────────────────────────
    {"n":"Edouard Manet","na":"French","bo":"1832","di":"1883","mo":"Realism / Impressionism","fa":"Le Dejeuner sur l'herbe (nude woman picnicking with clothed men) caused such outrage Napoleon III created a 'Salon des Refuses' just to house the rejected scandalous art"},
    {"n":"Claude Monet","na":"French","bo":"1840","di":"1926","mo":"Impressionism","fa":"Painted his Waterlilies series in the last 30 years of his life nearly blind from cataracts; the 8 panels in the Orangerie form an immersive 360-degree room"},
    {"n":"Edgar Degas","na":"French","bo":"1834","di":"1917","mo":"Impressionism","fa":"Despite being grouped with Impressionists, he hated painting outdoors; his obsession with dancers was less about beauty than about capturing the exhaustion of professional labor"},
    {"n":"Pierre-Auguste Renoir","na":"French","bo":"1841","di":"1919","mo":"Impressionism","fa":"Continued painting until his death despite severe arthritis that deformed his hands; his brushes were tied to his wrists — his final works are among his most joyful"},
    {"n":"Camille Pissarro","na":"French","bo":"1830","di":"1903","mo":"Impressionism","fa":"The only artist to exhibit in all eight Impressionist exhibitions; called 'the father of Impressionism' by Cezanne — he mentored Cezanne, Gauguin, and van Gogh"},
    {"n":"Alfred Sisley","na":"British / French","bo":"1839","di":"1899","mo":"Impressionism","fa":"The most consistent and pure Impressionist; despite this, he died in poverty — the day after his death his prices doubled; he never knew fame in his lifetime"},
    {"n":"Paul Cezanne","na":"French","bo":"1839","di":"1906","mo":"Post-Impressionism","fa":"Called 'the father of modern art'; his way of depicting geometric forms in nature directly inspired Cubism — Picasso and Braque both cited him as their primary influence"},
    {"n":"Paul Gauguin","na":"French","bo":"1848","di":"1903","mo":"Post-Impressionism","fa":"Abandoned his Paris stockbroker career at 35, left his wife and five children, and sailed to Tahiti to paint — his life story as scandalous as his art"},
    {"n":"Vincent van Gogh","na":"Dutch","bo":"1853","di":"1890","mo":"Post-Impressionism","fa":"Sold only one painting in his lifetime; wrote over 800 letters to his brother Theo that form one of the most profound art documents ever written. Shot himself at 37"},
    {"n":"Georges Seurat","na":"French","bo":"1859","di":"1891","mo":"Pointillism","fa":"Developed Pointillism scientifically: pure colour dots that the eye blends at a distance; A Sunday on La Grande Jatte took 2 years and contains over 3 million dots"},
    {"n":"Henri de Toulouse-Lautrec","na":"French","bo":"1864","di":"1901","mo":"Post-Impressionism","fa":"A fall at 13 stunted his leg growth; he documented Paris nightlife from his lowered vantage point — his Moulin Rouge posters invented modern advertising"},
    # ── Art Nouveau & Symbolisme ────────────────────────────────────────────
    {"n":"Gustav Klimt","na":"Austrian","bo":"1862","di":"1918","mo":"Art Nouveau / Symbolism","fa":"The Kiss contains gold leaf from real gold; Klimt never gave interviews and almost never left Vienna — yet his influence on European decorative art is incalculable"},
    {"n":"Egon Schiele","na":"Austrian","bo":"1890","di":"1918","mo":"Expressionism","fa":"Died in the 1918 flu pandemic at 28, three days after his pregnant wife; his raw, contorted figures were seized by police as obscene — today sell for tens of millions","wl":"red","wi":"Convicted in 1912 and sentenced to 24 days in prison. The initial charge was abducting a 13-year-old girl; the judge also burned several of his drawings in court for indecency."},
    {"n":"Edvard Munch","na":"Norwegian","bo":"1863","di":"1944","mo":"Expressionism","fa":"The Scream exists in 4 versions; he wrote in his diary about the inspiration: 'I felt a great, unending scream passing through nature' — anxiety given visual form"},
    {"n":"Alphonse Mucha","na":"Czech","bo":"1860","di":"1939","mo":"Art Nouveau","fa":"His poster of Sarah Bernhardt (designed overnight in January 1895) created Art Nouveau style; he spent his final 20 years on The Slav Epic — 20 enormous canvases for his nation"},
    # ── Fauvisme, Cubisme, Dada, Surréalisme ───────────────────────────────
    {"n":"Henri Matisse","na":"French","bo":"1869","di":"1954","mo":"Fauvism","fa":"Called a 'wild beast' (fauve) for his shocking colours in 1905; spent his final years cutting coloured paper with scissors when too ill to paint — producing his greatest works"},
    {"n":"Pablo Picasso","na":"Spanish","bo":"1881","di":"1973","mo":"Cubism","fa":"Created Guernica in 6 weeks after the Nazi bombing of a Basque town; made 20,000 works across his 75-year career — the most prolific major artist in history","wl":"red","wi":"Multiple long-term partners documented physical and psychological abuse. Two of his companions, Marie-Therese Walter and Jacqueline Roque, died by suicide. No criminal charges were filed."},
    {"n":"Georges Braque","na":"French","bo":"1882","di":"1963","mo":"Cubism","fa":"Developed Cubism alongside Picasso in such close collaboration they called themselves 'roped together like mountaineers'; their 1908-1914 paintings are barely distinguishable"},
    {"n":"Marcel Duchamp","na":"French","bo":"1887","di":"1968","mo":"Dada","fa":"Submitted a urinal titled 'Fountain' to a 1917 exhibition — arguably the most influential single artwork of the 20th century; he spent his last 20 years playing chess"},
    {"n":"Wassily Kandinsky","na":"Russian","bo":"1866","di":"1944","mo":"Abstract Expressionism","fa":"Painted the first purely abstract artwork in 1910; he described seeing colours as sounds and hearing sounds as colours — his synaesthesia shaped his entire theory of art"},
    {"n":"Paul Klee","na":"Swiss / German","bo":"1879","di":"1940","mo":"Expressionism","fa":"Was a gifted violinist who chose painting; his 9,000 works span many styles — his journal entry 'Drawing is taking a line for a walk' defines spontaneous art making"},
    {"n":"Piet Mondrian","na":"Dutch","bo":"1872","di":"1944","mo":"De Stijl","fa":"His grids of primary colours influenced everything from Yves Saint Laurent fashion to IKEA design; he refused to hang his paintings near red flowers — too much visual noise"},
    {"n":"Kazimir Malevich","na":"Russian","bo":"1879","di":"1935","mo":"Suprematism","fa":"Black Square (a black square on white) was hung in the 'beautiful corner' — the traditional place for icons in Russian homes; art replacing religion, deliberately"},
    {"n":"Salvador Dali","na":"Spanish","bo":"1904","di":"1989","mo":"Surrealism","fa":"The Persistence of Memory was inspired by a melting Camembert; he called himself a genius daily, staged publicity stunts obsessively, and arrived at events in a Rolls-Royce with a pet ocelot"},
    {"n":"Rene Magritte","na":"Belgian","bo":"1898","di":"1967","mo":"Surrealism","fa":"The Treachery of Images (Ceci n'est pas une pipe) teaches a philosophy lesson: the image of a pipe is not a pipe. He wore a bowler hat daily as a defence against art-world theatrics"},
    {"n":"Max Ernst","na":"German","bo":"1891","di":"1976","mo":"Dada / Surrealism","fa":"Invented frottage (rubbing surfaces through paper) and grattage (scraping paint layers) — techniques to bypass rational thought and access the unconscious directly"},
    {"n":"Joan Miro","na":"Spanish","bo":"1893","di":"1983","mo":"Surrealism","fa":"His playful symbols — stars, moon, woman, bird — form a private language repeated across thousands of works; he called himself 'an assassin of painting' trying to kill convention"},
    {"n":"Marc Chagall","na":"Belarusian / French","bo":"1887","di":"1985","mo":"Expressionism / Surrealism","fa":"His floating lovers, fiddlers, and village memories from Vitebsk became universal symbols of love and nostalgia; he designed stained glass for Reims Cathedral at age 73"},
    {"n":"Amedeo Modigliani","na":"Italian","bo":"1884","di":"1920","mo":"Expressionism","fa":"His elongated nudes were removed from his first gallery show by police for indecency; he died at 35 of tubercular meningitis worsened by alcohol — his partner threw herself from a window","wl":"orange","wi":"Physical abuse of his partner Jeanne Hebuterne during episodes of alcohol and drug abuse is documented in multiple biographies."},
    {"n":"Giorgio de Chirico","na":"Italian","bo":"1888","di":"1978","mo":"Metaphysical Art","fa":"His empty piazzas with long shadows and statues — the world after humans have gone — directly inspired Surrealism; Dali and Magritte both cited him as the origin of everything"},
    # ── Expressionnisme abstrait ────────────────────────────────────────────
    {"n":"Jackson Pollock","na":"American","bo":"1912","di":"1956","mo":"Abstract Expressionism","fa":"Invented drip painting by dancing around canvases on the floor; his death in a drunk-driving crash at 44 cemented his myth — Number 31 sold for $200M in 2015"},
    {"n":"Mark Rothko","na":"American (Latvian-born)","bo":"1903","di":"1970","mo":"Abstract Expressionism","fa":"His floating colour rectangles are designed to be viewed from 45 cm — at that distance, viewers report feeling surrounded by emotion. He wept when he saw them installed"},
    {"n":"Willem de Kooning","na":"Dutch / American","bo":"1904","di":"1997","mo":"Abstract Expressionism","fa":"His Women series provoked outrage for depicting women as grotesque; he continued working productively well into Alzheimer's disease, producing a late style critics call his finest"},
    {"n":"Francis Bacon","na":"British (Irish-born)","bo":"1909","di":"1992","mo":"Figurative Expressionism","fa":"Destroyed most of his early work by cutting canvases; his screaming, smeared figures in caged interiors are the defining image of post-war existential horror"},
    {"n":"Lucian Freud","na":"British (German-born)","bo":"1922","di":"2011","mo":"Figurative Realism","fa":"Grandson of Sigmund Freud; his unflinching nude portraits show flesh as vulnerable, naked fact; Benefits Supervisor Sleeping (1995) sold for $33.6M in 2008"},
    # ── Pop Art & contemporain ─────────────────────────────────────────────
    {"n":"Georgia O'Keeffe","na":"American","bo":"1887","di":"1986","mo":"Modernism","fa":"Moved to the New Mexico desert at 46 and stayed for 40 years; her giant close-up flowers were accused of being sexual imagery — she spent her career denying it"},
    {"n":"Edward Hopper","na":"American","bo":"1882","di":"1967","mo":"Realism","fa":"Nighthawks (diner scene at night) is the most reproduced American painting; his images of urban loneliness have been endlessly referenced in film, advertising, and pop culture"},
    {"n":"Andy Warhol","na":"American","bo":"1928","di":"1987","mo":"Pop Art","fa":"Turned Campbell's soup cans and Marilyn Monroe into high art; he ran 'The Factory' like an actual factory — his assistants produced most of his silkscreens"},
    {"n":"Roy Lichtenstein","na":"American","bo":"1923","di":"1997","mo":"Pop Art","fa":"His Ben-Day dot enlargements of comic panels were dismissed as fake-art by critics; 'Whaam!' (a fighter jet in battle) sold for $43M in 2015 — one comic panel, museum-size"},
    {"n":"David Hockney","na":"British","bo":"1937","di":"-","mo":"Pop Art / Realism","fa":"A Bigger Splash (1967) was bought for a fraction of its current price; he returned to Yorkshire at 60 to paint landscapes and, at 82, produced his biggest iPad painting"},
    {"n":"Jean-Michel Basquiat","na":"American","bo":"1960","di":"1988","mo":"Neo-Expressionism","fa":"Went from SAMO graffiti on Lower Manhattan walls to Sotheby's in 4 years; Untitled (skull) sold for $110.5M in 2017; he died of a heroin overdose at 27"},
    {"n":"Gerhard Richter","na":"German","bo":"1932","di":"-","mo":"Photorealism / Abstract","fa":"The only living artist to work in both photorealistic and abstract styles simultaneously; his Atlas is a collection of 5,000 photo-newspaper references — memory as art"},
    {"n":"Yayoi Kusama","na":"Japanese","bo":"1929","di":"-","mo":"Pop Art / Avant-garde","fa":"Diagnosed herself with obsessive-compulsive disorder and checked herself into a psychiatric institution in 1977 — where she has voluntarily lived ever since, painting prolifically"},
    {"n":"Frida Kahlo","na":"Mexican","bo":"1907","di":"1954","mo":"Surrealism / Magical Realism","fa":"Survived polio and a devastating bus crash; painted 55 self-portraits from her hospital bed using a mirror rigged above it — her pain became her universal language"},
    {"n":"Diego Rivera","na":"Mexican","bo":"1886","di":"1957","mo":"Muralism","fa":"His Detroit Industry Murals hired real Ford factory workers as models; Nelson Rockefeller had his Rockefeller Center mural destroyed for including Lenin — Rivera re-created it from memory"},
    # ── Art asiatique ───────────────────────────────────────────────────────
    {"n":"Katsushika Hokusai","na":"Japanese","bo":"1760","di":"1849","mo":"Ukiyo-e","fa":"The Great Wave is the most reproduced artwork in history; Hokusai moved house 93 times in his life and changed his name 30 times — restlessness was his creative philosophy"},
    {"n":"Utagawa Hiroshige","na":"Japanese","bo":"1797","di":"1858","mo":"Ukiyo-e","fa":"His One Hundred Famous Views of Edo directly inspired Monet's Japanese bridge and Van Gogh who copied two of his prints in oil — the influence of Japanese art on Western modernism runs through Hiroshige"},
    # ── Autres contemporains ────────────────────────────────────────────────
    {"n":"Ai Weiwei","na":"Chinese","bo":"1957","di":"-","mo":"Contemporary","fa":"Detained by Chinese authorities for 81 days in 2011 without charge; documented every moment on social media beforehand — activism and art inseparably fused"},
    {"n":"Banksy","na":"British","bo":"~1974","di":"-","mo":"Street Art","fa":"Girl with Balloon shredded itself moments after selling for $1.4M at Sotheby's — a prank pre-installed in the frame. Sotheby's renamed it Love is in the Bin and it sold for $25.4M in 2021"},
    {"n":"Fernando Botero","na":"Colombian","bo":"1932","di":"2023","mo":"Figurative","fa":"Every figure he painted was deliberately inflated — he called it 'the sensuality of form'; the Abu Ghraib series (2005) used his round style to depict torture, creating disturbing dissonance"},
    {"n":"Jasper Johns","na":"American","bo":"1930","di":"-","mo":"Neo-Dada","fa":"Flag (1954-55) — a plain painting of the American flag — bridged Abstract Expressionism and Pop Art; sold to MoMA for what seemed an absurd price, then became one of America's most studied works"},
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
    total = len(artists)
    found = 0
    for i, s in enumerate(artists):
        title = WIKI_EN.get(s["n"], s["n"])
        img = wiki_img(title)
        s["im"] = img
        if img: found += 1
        status = "ok" if img else "xx"
        sys.stdout.buffer.write(f"  [{i+1:2}/{total}] {status} {s['n']}\n".encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)
    out = Path("assets/art/famous_artists.json")
    out.write_text(json.dumps(artists, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    sys.stdout.buffer.write(f"\nDone: {found}/{total} images -- {total} artists total.\n".encode("utf-8"))

if __name__ == "__main__":
    main()
