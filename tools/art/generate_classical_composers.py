import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=name, na=nationality, bo=born, di=died, pe=period, fw=famous_works, fa=famous_for, im=imageUrl

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_EN = {
    "Hildegard von Bingen": "Hildegard of Bingen",
    "Guillaume de Machaut": "Guillaume de Machaut",
    "Josquin des Prez": "Josquin des Prez",
    "Giovanni Pierluigi da Palestrina": "Giovanni Pierluigi da Palestrina",
    "Claudio Monteverdi": "Claudio Monteverdi",
    "Henry Purcell": "Henry Purcell",
    "Arcangelo Corelli": "Arcangelo Corelli",
    "Antonio Vivaldi": "Antonio Vivaldi",
    "Georg Friedrich Handel": "George Frideric Handel",
    "Johann Sebastian Bach": "Johann Sebastian Bach",
    "Georg Philipp Telemann": "Georg Philipp Telemann",
    "Jean-Philippe Rameau": "Jean-Philippe Rameau",
    "Domenico Scarlatti": "Domenico Scarlatti",
    "Christoph Willibald Gluck": "Christoph Willibald Gluck",
    "Joseph Haydn": "Joseph Haydn",
    "Wolfgang Amadeus Mozart": "Wolfgang Amadeus Mozart",
    "Ludwig van Beethoven": "Ludwig van Beethoven",
    "Franz Schubert": "Franz Schubert",
    "Carl Maria von Weber": "Carl Maria von Weber",
    "Felix Mendelssohn": "Felix Mendelssohn",
    "Robert Schumann": "Robert Schumann",
    "Clara Schumann": "Clara Schumann",
    "Frederic Chopin": "Frederic Chopin",
    "Franz Liszt": "Franz Liszt",
    "Hector Berlioz": "Hector Berlioz",
    "Giacomo Meyerbeer": "Giacomo Meyerbeer",
    "Gaetano Donizetti": "Gaetano Donizetti",
    "Vincenzo Bellini": "Vincenzo Bellini",
    "Giuseppe Verdi": "Giuseppe Verdi",
    "Richard Wagner": "Richard Wagner",
    "Johannes Brahms": "Johannes Brahms",
    "Anton Bruckner": "Anton Bruckner",
    "Camille Saint-Saens": "Camille Saint-Saens",
    "Gabriel Faure": "Gabriel Faure",
    "Georges Bizet": "Georges Bizet",
    "Jacques Offenbach": "Jacques Offenbach",
    "Johann Strauss II": "Johann Strauss II",
    "Bedrich Smetana": "Bedrich Smetana",
    "Antonin Dvorak": "Antonin Dvorak",
    "Edvard Grieg": "Edvard Grieg",
    "Pyotr Ilyich Tchaikovsky": "Pyotr Ilyich Tchaikovsky",
    "Modest Mussorgsky": "Modest Mussorgsky",
    "Nikolai Rimsky-Korsakov": "Nikolai Rimsky-Korsakov",
    "Alexander Borodin": "Alexander Borodin",
    "Gustav Mahler": "Gustav Mahler",
    "Giacomo Puccini": "Giacomo Puccini",
    "Richard Strauss": "Richard Strauss",
    "Edward Elgar": "Edward Elgar",
    "Jean Sibelius": "Jean Sibelius",
    "Leos Janacek": "Leos Janacek",
    "Claude Debussy": "Claude Debussy",
    "Maurice Ravel": "Maurice Ravel",
    "Erik Satie": "Erik Satie",
    "Bela Bartok": "Bela Bartok",
    "Igor Stravinsky": "Igor Stravinsky",
    "Arnold Schoenberg": "Arnold Schoenberg",
    "Alban Berg": "Alban Berg",
    "Anton Webern": "Anton Webern",
    "Sergei Prokofiev": "Sergei Prokofiev",
    "Dmitri Shostakovich": "Dmitri Shostakovich",
    "Paul Hindemith": "Paul Hindemith",
    "Benjamin Britten": "Benjamin Britten",
    "Olivier Messiaen": "Olivier Messiaen",
    "Samuel Barber": "Samuel Barber",
    "Aaron Copland": "Aaron Copland",
    "George Gershwin": "George Gershwin",
    "Benny Goodman": "Benny Goodman",
    "Dmitri Kabalevsky": "Dmitri Kabalevsky",
    "Aram Khachaturian": "Aram Khachaturian",
    "Astor Piazzolla": "Astor Piazzolla",
    "Gyorgy Ligeti": "Gyorgy Ligeti",
    "Karlheinz Stockhausen": "Karlheinz Stockhausen",
    "Pierre Boulez": "Pierre Boulez",
    "Arvo Part": "Arvo Part",
    "Henryk Gorecki": "Henryk Gorecki",
    "Philip Glass": "Philip Glass",
    "John Adams": "John Adams (composer)",
    "Steve Reich": "Steve Reich",
    "Sofia Gubaidulina": "Sofia Gubaidulina",
    "Morten Lauridsen": "Morten Lauridsen",
}

composers = [
    # Medieval et Renaissance
    {"n": "Hildegard von Bingen", "na": "German", "bo": "1098", "di": "1179", "pe": "Medieval", "fw": "Ordo Virtutum, Symphonia", "fa": "The first named composer in history whose biography is known; the abbess wrote music, poetry, theology and medicine - her chants have been continuously performed for 900 years"},
    {"n": "Guillaume de Machaut", "na": "French", "bo": "~1300", "di": "1377", "pe": "Medieval", "fw": "Messe de Nostre Dame", "fa": "The first composer known to have overseen the collection and arrangement of his own complete works; his Messe de Nostre Dame is the earliest known complete setting of the Mass by a single composer"},
    {"n": "Josquin des Prez", "na": "Flemish", "bo": "~1450", "di": "1521", "pe": "Renaissance", "fw": "Missa Pange Lingua, Ave Maria", "fa": "Called the master of the notes by Luther and the first composer to achieve international fame in his lifetime; he was so revered that compositions were falsely attributed to him after his death"},
    {"n": "Giovanni Pierluigi da Palestrina", "na": "Italian", "bo": "~1525", "di": "1594", "pe": "Renaissance", "fw": "Missa Papae Marcelli", "fa": "Legend says his Missa Papae Marcelli saved polyphonic music from being banned by the Council of Trent; his smooth, controlled style became the model for sacred choral music for 400 years"},
    {"n": "Claudio Monteverdi", "na": "Italian", "bo": "1567", "di": "1643", "pe": "Late Renaissance/Early Baroque", "fw": "L'Orfeo, Vespers of 1610", "fa": "Invented opera - L'Orfeo (1607) is the first opera still performed regularly; he bridged Renaissance and Baroque by introducing dissonance and expressive harmony to represent human emotion"},
    {"n": "Henry Purcell", "na": "English", "bo": "1659", "di": "1695", "pe": "Baroque", "fw": "Dido and Aeneas", "fa": "Dido's Lament from Dido and Aeneas remains one of the most heartbreaking pieces in Western music; Purcell died at 36 leaving a body of work that would not be equaled in England for 200 years"},
    # Baroque
    {"n": "Arcangelo Corelli", "na": "Italian", "bo": "1653", "di": "1713", "pe": "Baroque", "fw": "12 Concerti Grossi Op. 6", "fa": "Essentially invented the modern violin technique and established the concerto grosso form; every Baroque composer who came after him - Vivaldi, Handel, Bach - learned from his innovations"},
    {"n": "Antonio Vivaldi", "na": "Italian", "bo": "1678", "di": "1741", "pe": "Baroque", "fw": "The Four Seasons", "fa": "A priest who was excused from saying mass because of his asthma; he wrote over 500 concertos - Bach copied and arranged many of them, calling Vivaldi his greatest teacher"},
    {"n": "Georg Friedrich Handel", "na": "German/British", "bo": "1685", "di": "1759", "pe": "Baroque", "fw": "Messiah, Water Music", "fa": "When the king stood up during the Hallelujah Chorus, everyone followed - creating a tradition that continues today; Handel went blind at 74 and continued composing by dictation"},
    {"n": "Johann Sebastian Bach", "na": "German", "bo": "1685", "di": "1750", "pe": "Baroque", "fw": "Mass in B Minor, The Well-Tempered Clavier", "fa": "Had 20 children, wrote over 1,000 works, and died largely forgotten; rediscovered by Mendelssohn in 1829, he is now considered the greatest composer who ever lived"},
    {"n": "Georg Philipp Telemann", "na": "German", "bo": "1681", "di": "1767", "pe": "Baroque", "fw": "Tafelmusik", "fa": "The most prolific composer in history with over 3,000 works; was more famous than Bach during his lifetime - Bach actually came second to Telemann when applying for a prestigious post"},
    {"n": "Jean-Philippe Rameau", "na": "French", "bo": "1683", "di": "1764", "pe": "Baroque", "fw": "Castor et Pollux, Hippolyte et Aricie", "fa": "Wrote the first systematic treatise on harmony, establishing the rules of tonal music that all Western composers have followed since; wrote his first opera at age 50"},
    {"n": "Domenico Scarlatti", "na": "Italian", "bo": "1685", "di": "1757", "pe": "Baroque", "fw": "555 Keyboard Sonatas", "fa": "Wrote 555 keyboard sonatas, many exploring impossible technical challenges that anticipated Romantic piano writing by 100 years; he and Handel met as young men and their keyboard duel is legendary"},
    # Classicisme
    {"n": "Christoph Willibald Gluck", "na": "German/Bohemian", "bo": "1714", "di": "1787", "pe": "Classical", "fw": "Orfeo ed Euridice, Alceste", "fa": "Revolutionized opera by eliminating unnecessary vocal display and making drama primary; his reform divided Paris into two warring factions - Gluckists versus Piccinnists - for years"},
    {"n": "Joseph Haydn", "na": "Austrian", "bo": "1732", "di": "1809", "pe": "Classical", "fw": "The Creation, Surprise Symphony", "fa": "Invented the string quartet and the modern symphony - earning the title Father of the Symphony; he lived in relative isolation as court composer at Esterhaza for 30 years, developing his style undisturbed"},
    {"n": "Wolfgang Amadeus Mozart", "na": "Austrian", "bo": "1756", "di": "1791", "pe": "Classical", "fw": "Don Giovanni, Requiem, Symphony No. 40", "fa": "Composed his first symphony at age 8; wrote his Requiem on his deathbed at 35 - it remains unfinished; over 600 works in 35 years that cover every genre of Western music"},
    {"n": "Ludwig van Beethoven", "na": "German", "bo": "1770", "di": "1827", "pe": "Classical/Romantic", "fw": "9th Symphony, Moonlight Sonata, Fur Elise", "fa": "Composed his greatest works - including the 9th Symphony - while completely deaf; the premiere of the 9th moved him to tears he could not hear; he bridged the Classical and Romantic eras"},
    # Romantisme premier
    {"n": "Franz Schubert", "na": "Austrian", "bo": "1797", "di": "1828", "pe": "Romantic", "fw": "Ave Maria, Winterreise, Unfinished Symphony", "fa": "Died at 31 leaving 1,500 works including 600 songs; his Unfinished Symphony has only two movements - no one knows why he stopped; he died without knowing how great he was"},
    {"n": "Carl Maria von Weber", "na": "German", "bo": "1786", "di": "1826", "pe": "Early Romantic", "fw": "Der Freischutz, Invitation to the Dance", "fa": "Invented German Romantic opera and influenced every composer who followed; Wagner idolized him and personally conducted the transfer of his remains from London to Dresden as a tribute"},
    {"n": "Felix Mendelssohn", "na": "German", "bo": "1809", "di": "1847", "pe": "Romantic", "fw": "Violin Concerto, A Midsummer Night's Dream", "fa": "Rediscovered Bach's St. Matthew Passion in 1829, 100 years after its first performance, and launched the Bach revival; he wrote the Wedding March used at every Western marriage today"},
    {"n": "Robert Schumann", "na": "German", "bo": "1810", "di": "1856", "pe": "Romantic", "fw": "Piano Concerto, Kinderszenen", "fa": "Destroyed his right hand trying to strengthen it with a mechanical device; spent his final years in a mental asylum; his wife Clara continued performing and promoting his music after his death"},
    {"n": "Clara Schumann", "na": "German", "bo": "1819", "di": "1896", "pe": "Romantic", "fw": "Piano Concerto, Piano Trio", "fa": "One of the greatest pianists of the 19th century; raised 8 children, cared for her mentally ill husband, and maintained a 60-year performance career - largely unrecognized as a composer until recently"},
    {"n": "Frederic Chopin", "na": "Polish/French", "bo": "1810", "di": "1849", "pe": "Romantic", "fw": "Nocturnes, Ballades, Etudes", "fa": "Wrote almost exclusively for piano; performed rarely in public, preferring salons; his heart is buried in Warsaw under a church pillar - he made his sister promise to take it home from Paris when he died"},
    {"n": "Franz Liszt", "na": "Hungarian", "bo": "1811", "di": "1886", "pe": "Romantic", "fw": "Hungarian Rhapsodies, Liebestraum", "fa": "The first pop star: women tore his gloves and fought over his old piano strings; he invented the solo piano recital and the symphonic poem, and gave away most of his fortune to charity"},
    {"n": "Hector Berlioz", "na": "French", "bo": "1803", "di": "1869", "pe": "Romantic", "fw": "Symphonie Fantastique, The Damnation of Faust", "fa": "His Symphonie Fantastique depicted a drug-fueled nightmare love obsession - the first piece of program music to tell a specific narrative; he required orchestras of 400 and once used 1,000 performers"},
    # Opera romantique
    {"n": "Gaetano Donizetti", "na": "Italian", "bo": "1797", "di": "1848", "pe": "Romantic", "fw": "Lucia di Lammermoor, L'Elisir d'Amore", "fa": "Wrote 65 operas in 30 years; the mad scene from Lucia di Lammermoor is considered the ultimate test of a dramatic soprano - it includes a glass harmonica part to suggest supernatural madness"},
    {"n": "Vincenzo Bellini", "na": "Italian", "bo": "1801", "di": "1835", "pe": "Romantic", "fw": "Norma, La Sonnambula", "fa": "Died at 33 leaving only 10 operas; his long cantabile melodies inspired Chopin and Wagner alike; Norma is considered the Mount Everest of soprano roles - few can climb it"},
    {"n": "Giuseppe Verdi", "na": "Italian", "bo": "1813", "di": "1901", "pe": "Romantic", "fw": "Rigoletto, La Traviata, Aida, Otello", "fa": "Became a symbol of Italian unification - his name was used as a political slogan meaning Vittorio Emanuele Re D'Italia; crowds outside his hotel sang arias all night after Rigoletto's premiere"},
    {"n": "Richard Wagner", "na": "German", "bo": "1813", "di": "1883", "pe": "Romantic", "fw": "Ring Cycle, Tristan und Isolde, Parsifal", "fa": "Built his own opera house at Bayreuth specifically for his works; he revolutionized harmony with Tristan und Isolde, which begins with a chord that went unresolved for four hours"},
    {"n": "Jacques Offenbach", "na": "French (German-born)", "bo": "1819", "di": "1880", "pe": "Romantic", "fw": "Orpheus in the Underworld, The Tales of Hoffmann", "fa": "Invented operetta - light satirical musical theatre; the can-can music everyone knows is from his Orpheus in the Underworld, written to mock Gluck's serious treatment of the same myth"},
    {"n": "Johann Strauss II", "na": "Austrian", "bo": "1825", "di": "1899", "pe": "Romantic", "fw": "The Blue Danube, Die Fledermaus", "fa": "Called the Waltz King; wrote 500 waltzes; Brahms wrote on one of Strauss's fan letters: Unfortunately not by Brahms; the Vienna New Year's Concert plays his waltzes every year to a billion TV viewers"},
    # Nationalisme
    {"n": "Bedrich Smetana", "na": "Czech", "bo": "1824", "di": "1884", "pe": "Romantic/Nationalist", "fw": "Ma vlast, The Bartered Bride", "fa": "Composed his greatest works - including the Vltava - completely deaf; the cycle Ma vlast (My Homeland) became the anthem of Czech national identity and is performed at every Prague Spring festival"},
    {"n": "Antonin Dvorak", "na": "Czech", "bo": "1841", "di": "1904", "pe": "Romantic", "fw": "New World Symphony, Cello Concerto", "fa": "His New World Symphony - written in New York after hearing Native American music and spirituals - includes the melody that became the song Going Home; he returned to Bohemia homesick after 3 years"},
    {"n": "Edvard Grieg", "na": "Norwegian", "bo": "1843", "di": "1907", "pe": "Romantic/Nationalist", "fw": "Piano Concerto, Peer Gynt", "fa": "His piano concerto was rejected by the conservatory professor who told him never to write for orchestra; In the Hall of the Mountain King from Peer Gynt is the most recognizable opening in classical music"},
    {"n": "Pyotr Ilyich Tchaikovsky", "na": "Russian", "bo": "1840", "di": "1893", "pe": "Romantic", "fw": "Swan Lake, 1812 Overture, Nutcracker", "fa": "The 1812 Overture requires actual cannon fire and church bells; his ballets transformed ballet from background entertainment into an art form; he died 9 days after conducting his Pathetique Symphony"},
    {"n": "Modest Mussorgsky", "na": "Russian", "bo": "1839", "di": "1881", "pe": "Romantic/Nationalist", "fw": "Pictures at an Exhibition, Boris Godunov", "fa": "An officer who drank himself to death at 42; his raw unpolished style was considered amateurish but influenced Debussy, Ravel and Stravinsky; Ravel orchestrated Pictures at an Exhibition after Mussorgsky's death"},
    {"n": "Nikolai Rimsky-Korsakov", "na": "Russian", "bo": "1844", "di": "1908", "pe": "Romantic/Nationalist", "fw": "Scheherazade, Flight of the Bumblebee", "fa": "A navy officer who taught himself composition and became the greatest orchestral colorist of the 19th century; he taught Prokofiev and Stravinsky, and revised Mussorgsky's incomplete works after his death"},
    {"n": "Alexander Borodin", "na": "Russian", "bo": "1833", "di": "1887", "pe": "Romantic/Nationalist", "fw": "Prince Igor, In the Steppes of Central Asia", "fa": "A professional chemist who wrote music as a hobby; Prince Igor was unfinished at his death and completed from memory by Glazunov; the Polovtsian Dances from it became the hit musical Kismet"},
    {"n": "Jean Sibelius", "na": "Finnish", "bo": "1865", "di": "1957", "pe": "Late Romantic", "fw": "Finlandia, Violin Concerto, Symphony No. 2", "fa": "Finlandia was banned by the Russian authorities for inflaming Finnish nationalist sentiment; he stopped composing at 60, lived for 30 more years, and never explained why - one of music's great mysteries"},
    {"n": "Leos Janacek", "na": "Czech", "bo": "1854", "di": "1928", "pe": "Late Romantic/Modern", "fw": "Jenufa, Sinfonietta", "fa": "Most of his greatest works were written after 60; obsessively notated the speech rhythms of everyday language to create his unique musical language; fell in love with a married woman at 62 and wrote masterpieces for her"},
    # Fin du romantisme et impressionnisme
    {"n": "Johannes Brahms", "na": "German", "bo": "1833", "di": "1897", "pe": "Romantic", "fw": "German Requiem, 4 Symphonies, Violin Concerto", "fa": "Waited 20 years to publish his first symphony for fear of comparison with Beethoven; destroyed all his early manuscripts; called his mature works too academic by critics who preferred Wagner's revolution"},
    {"n": "Anton Bruckner", "na": "Austrian", "bo": "1824", "di": "1896", "pe": "Late Romantic", "fw": "9 Symphonies, Te Deum", "fa": "A devoutly religious peasant who wrote massive cathedral symphonies; he revised his works obsessively at critics' suggestions, leaving multiple versions of each symphony; died before finishing his 9th"},
    {"n": "Camille Saint-Saens", "na": "French", "bo": "1835", "di": "1921", "pe": "Romantic", "fw": "Carnival of the Animals, Symphony No. 3, Samson et Dalila", "fa": "A child prodigy who could read at age 3 and memorized Beethoven at 7; he refused to allow Carnival of the Animals to be published during his lifetime - he considered it too frivolous for his reputation"},
    {"n": "Gabriel Faure", "na": "French", "bo": "1845", "di": "1924", "pe": "Late Romantic", "fw": "Requiem, Pavane, Pelleas et Melisande", "fa": "His Requiem was premiered at a funeral and became his most loved work; he composed his finest chamber music while nearly completely deaf - like Beethoven, he heard his last works only in his imagination"},
    {"n": "Georges Bizet", "na": "French", "bo": "1838", "di": "1875", "pe": "Romantic", "fw": "Carmen, L'Arlesienne", "fa": "Carmen was booed at its premiere and considered a failure; Bizet died 3 months later never knowing it would become the most performed opera in history; the premiere audience expected a light comedy"},
    {"n": "Gustav Mahler", "na": "Austrian", "bo": "1860", "di": "1911", "pe": "Late Romantic", "fw": "9 Symphonies, Das Lied von der Erde", "fa": "His symphonies require orchestras of 100 and last 90 minutes; he said a symphony must contain the whole world; he died before completing his 10th - the same curse as Beethoven, Schubert and Bruckner"},
    {"n": "Giacomo Puccini", "na": "Italian", "bo": "1858", "di": "1924", "pe": "Late Romantic", "fw": "La Boheme, Tosca, Madama Butterfly, Turandot", "fa": "His operas are now the most performed in the world; Turandot was unfinished when he died of cancer; at its premiere, conductor Toscanini stopped the orchestra at the point where Puccini had stopped composing"},
    {"n": "Richard Strauss", "na": "German", "bo": "1864", "di": "1949", "pe": "Late Romantic", "fw": "Also Sprach Zarathustra, Der Rosenkavalier", "fa": "Also Sprach Zarathustra became universally known as the 2001 A Space Odyssey theme; he continued living comfortably in Germany under the Nazis, a decision that damaged his legacy but saved his Jewish daughter-in-law"},
    {"n": "Edward Elgar", "na": "British", "bo": "1857", "di": "1934", "pe": "Late Romantic", "fw": "Enigma Variations, Cello Concerto", "fa": "The Pomp and Circumstance march is played at every US graduation ceremony; the Enigma Variations conceals a hidden theme that appears nowhere in the music - no one has definitively identified it in 125 years"},
    # Fin du XIXe - debut XXe
    {"n": "Claude Debussy", "na": "French", "bo": "1862", "di": "1918", "pe": "Impressionism", "fw": "Clair de lune, Pelleas et Melisande, La Mer", "fa": "Rejected the German tradition entirely and created Impressionism in music; Clair de lune is the most beloved piano piece in the world; he died during the German bombardment of Paris in 1918"},
    {"n": "Maurice Ravel", "na": "French", "bo": "1875", "di": "1937", "pe": "Impressionism", "fw": "Bolero, Piano Concerto in G, Daphnis et Chloe", "fa": "Bolero is the best-selling classical recording of all time; he rejected the Nobel Prize but accepted the Legion of Honor; diagnosed with a brain disease at 57, he stopped composing but continued attending concerts until death"},
    {"n": "Erik Satie", "na": "French", "bo": "1866", "di": "1925", "pe": "Avant-garde", "fw": "Gymnopedies, Gnossiennes, Parade", "fa": "His Gymnopedies are the most frequently heard pieces in cafes worldwide; he invented ambient music and composed in genres he invented himself: furniture music, gymnopedies and humoristic pieces"},
    # XXe siecle
    {"n": "Bela Bartok", "na": "Hungarian", "bo": "1881", "di": "1945", "pe": "Modern", "fw": "Music for Strings Percussion and Celesta, Concerto for Orchestra", "fa": "Traveled thousands of miles recording folk music on wax cylinders before radio existed; his research preserved 10,000 folk melodies and transformed his harmonic language - making him the bridge between folk and modern music"},
    {"n": "Igor Stravinsky", "na": "Russian/French/American", "bo": "1882", "di": "1971", "pe": "Modern", "fw": "The Rite of Spring, The Firebird, Petrushka", "fa": "The premiere of The Rite of Spring in 1913 caused a riot in the theatre - audience members fought in the aisles over whether it was genius or garbage; it is now considered the most influential work in 20th century music"},
    {"n": "Arnold Schoenberg", "na": "Austrian/American", "bo": "1874", "di": "1951", "pe": "Expressionism/12-Tone", "fw": "Pierrot Lunaire, A Survivor from Warsaw", "fa": "Invented twelve-tone technique - a method of composition using all 12 notes equally - which his pupil Webern and Alban Berg developed; suffered from triskaidekaphobia and feared the number 13 his whole life"},
    {"n": "Alban Berg", "na": "Austrian", "bo": "1885", "di": "1935", "pe": "Expressionism", "fw": "Wozzeck, Violin Concerto, Lulu", "fa": "His opera Wozzeck - about a soldier's descent into madness and murder - is so emotionally shattering that audiences leave in silence; he died before finishing Lulu, which was completed posthumously"},
    {"n": "Anton Webern", "na": "Austrian", "bo": "1883", "di": "1945", "pe": "Expressionism/Serialism", "fw": "Symphony Op. 21, Variations for Orchestra", "fa": "His entire output lasts barely 4 hours; each piece distills music to its essence - a single melody lasting 23 seconds, orchestral movements measured in seconds; he was shot by accident by an American soldier in 1945"},
    {"n": "Sergei Prokofiev", "na": "Russian", "bo": "1891", "di": "1953", "pe": "Modern", "fw": "Romeo and Juliet, Peter and the Wolf, Piano Concerto No. 3", "fa": "Peter and the Wolf has introduced millions of children to the orchestra since 1936; he died the same day as Stalin - his death was barely reported because all available flowers went to Stalin's state funeral"},
    {"n": "Dmitri Shostakovich", "na": "Russian", "bo": "1906", "di": "1975", "pe": "Modern", "fw": "Symphony No. 5, Symphony No. 7, String Quartets", "fa": "The premiere of his 7th Symphony was broadcast from besieged Leningrad in 1942 - a defiant act of cultural survival; Stalin twice nearly had him arrested; he encoded secret messages in his music using his musical monogram DSCH"},
    {"n": "Benjamin Britten", "na": "British", "bo": "1913", "di": "1976", "pe": "Modern", "fw": "Peter Grimes, War Requiem, Young Person's Guide to the Orchestra", "fa": "His War Requiem interleaves the Latin Mass with WWI poetry by Wilfred Owen - a peace manifesto first performed in the rebuilt Coventry Cathedral, destroyed in the Blitz, in 1962"},
    {"n": "Olivier Messiaen", "na": "French", "bo": "1908", "di": "1992", "pe": "Modern", "fw": "Quartet for the End of Time, Turangalila Symphony", "fa": "Wrote his Quartet for the End of Time in a Nazi prisoner-of-war camp using whatever instruments were available: clarinet, violin, cello and piano; premiered before 400 prisoners in January 1941 in freezing cold"},
    {"n": "Aaron Copland", "na": "American", "bo": "1900", "di": "1990", "pe": "Modern/Americanism", "fw": "Appalachian Spring, Fanfare for the Common Man, Billy the Kid", "fa": "His Fanfare for the Common Man is played at every American sporting event, political rally, and presidential inauguration - the sound of democratic optimism in 30 seconds of brass"},
    {"n": "George Gershwin", "na": "American", "bo": "1898", "di": "1937", "pe": "Jazz/Classical", "fw": "Rhapsody in Blue, Porgy and Bess, An American in Paris", "fa": "Died at 38 from an undiagnosed brain tumor; Rhapsody in Blue fused jazz and classical music for the first time; Porgy and Bess was the first American opera accepted into the international repertoire"},
    {"n": "Samuel Barber", "na": "American", "bo": "1910", "di": "1981", "pe": "Modern/Romantic", "fw": "Adagio for Strings, Violin Concerto", "fa": "His Adagio for Strings is the piece played at state funerals, memorial services and moments of national mourning worldwide; it was broadcast on radio when Roosevelt and Einstein died"},
    {"n": "Aram Khachaturian", "na": "Armenian/Soviet", "bo": "1903", "di": "1978", "pe": "Modern", "fw": "Spartacus, Sabre Dance, Piano Concerto", "fa": "The Sabre Dance is played at every circus and comedy skit requiring frenetic urgency; he was reprimanded by the Soviet Union for formalism but continued writing in his colorful Armenian-influenced style"},
    {"n": "Astor Piazzolla", "na": "Argentine", "bo": "1921", "di": "1992", "pe": "Modern/Tango", "fw": "Libertango, Oblivion, The Four Seasons of Buenos Aires", "fa": "Transformed tango from dance music into concert music; classical musicians told him tango was beneath them, tango dancers said his music was unplayable - he played both worlds against each other and won"},
    # Avant-garde et minimalisme
    {"n": "Gyorgy Ligeti", "na": "Hungarian/Austrian", "bo": "1923", "di": "2006", "pe": "Avant-garde", "fw": "Atmospheres, Etudes, Lux Aeterna", "fa": "Stanley Kubrick used his music in 2001 A Space Odyssey without permission; Ligeti sued and won; his cluster-chord technique - hundreds of notes played simultaneously - creates a sound like luminous fog"},
    {"n": "Karlheinz Stockhausen", "na": "German", "bo": "1928", "di": "2007", "pe": "Avant-garde", "fw": "Gesang der Junglinge, Helicopter String Quartet", "fa": "His Helicopter String Quartet requires four musicians to perform in four hovering helicopters over an audience below; he was listed by the Beatles on the Sgt. Pepper album cover as one of their greatest influences"},
    {"n": "Pierre Boulez", "na": "French", "bo": "1925", "di": "2016", "pe": "Avant-garde/Serialism", "fw": "Le Marteau sans maitre, Pli selon pli", "fa": "Equally famous as composer and conductor; built IRCAM in Paris - a research institute for musical acoustics; called all operas except those of Boulez and Debussy garbage that needed to be burnt down"},
    {"n": "Philip Glass", "na": "American", "bo": "1937", "di": "-", "pe": "Minimalism", "fw": "Einstein on the Beach, Koyaanisqatsi, Glassworks", "fa": "Worked as a plumber and taxi driver while composing; Einstein on the Beach ran for 4.5 hours without intermission - audiences wandered in and out freely; he has scored over 50 films and won 3 Oscars"},
    {"n": "Steve Reich", "na": "American", "bo": "1936", "di": "-", "pe": "Minimalism", "fw": "Music for 18 Musicians, Different Trains", "fa": "Invented phase music by using two tape recorders at slightly different speeds; his Different Trains uses recordings of Holocaust survivors alongside strings - a meditation on history through sound"},
    {"n": "Arvo Part", "na": "Estonian", "bo": "1935", "di": "-", "pe": "Minimalism/Sacred", "fw": "Spiegel im Spiegel, Tintinnabuli, Cantus in Memory of Britten", "fa": "Invented tintinnabuli - a style of extreme simplicity derived from medieval chant; his music of silence and space is the most performed by living composers worldwide - often requested for funerals"},
    {"n": "Henryk Gorecki", "na": "Polish", "bo": "1933", "di": "2010", "pe": "Minimalism", "fw": "Symphony No. 3 Symphony of Sorrowful Songs", "fa": "His Symphony of Sorrowful Songs was recorded in 1992 and became the first classical album to reach the pop charts - selling over a million copies; the second movement is a prayer written by a Jewish girl on a Gestapo cell wall"},
    {"n": "Sofia Gubaidulina", "na": "Russian/German", "bo": "1931", "di": "-", "pe": "Modern", "fw": "Offertorium, Stimmen... Verstummen...", "fa": "Her devout spirituality led Soviet authorities to describe her music as hostile; Shostakovich told her to keep going in her own direction - the most important encouragement she ever received"},
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
    total = len(composers)
    found = 0
    for i, s in enumerate(composers):
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
    out = Path("assets/art/classical_composers.json")
    out.write_text(json.dumps(composers, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    summary = "\nDone: {}/{} images -- {} composers total.\n".format(found, total, total)
    sys.stdout.buffer.write(summary.encode("utf-8"))

if __name__ == "__main__":
    main()
