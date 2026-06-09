import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=name, na=nationality, bo=born, di=died, st=style, fw=famous_work, fa=famous_for, im=imageUrl

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_EN = {
    "Nadar": "Nadar (photographer)",
    "Julia Margaret Cameron": "Julia Margaret Cameron",
    "Eadweard Muybridge": "Eadweard Muybridge",
    "Alfred Stieglitz": "Alfred Stieglitz",
    "Edward Steichen": "Edward Steichen",
    "Eugene Atget": "Eugene Atget",
    "August Sander": "August Sander",
    "Lewis Hine": "Lewis Hine",
    "Man Ray": "Man Ray",
    "Laszlo Moholy-Nagy": "Laszlo Moholy-Nagy",
    "Brassai": "Brassai",
    "Andre Kertesz": "Andre Kertesz",
    "Robert Doisneau": "Robert Doisneau",
    "Henri Cartier-Bresson": "Henri Cartier-Bresson",
    "Robert Capa": "Robert Capa",
    "Dorothea Lange": "Dorothea Lange",
    "Walker Evans": "Walker Evans",
    "Ansel Adams": "Ansel Adams",
    "Weegee": "Weegee",
    "W. Eugene Smith": "W. Eugene Smith",
    "Yousuf Karsh": "Yousuf Karsh",
    "Margaret Bourke-White": "Margaret Bourke-White",
    "Berenice Abbott": "Berenice Abbott",
    "Lisette Model": "Lisette Model",
    "Irving Penn": "Irving Penn",
    "Richard Avedon": "Richard Avedon",
    "Helmut Newton": "Helmut Newton",
    "Guy Bourdin": "Guy Bourdin",
    "David Bailey": "David Bailey (photographer)",
    "Philippe Halsman": "Philippe Halsman",
    "Arnold Newman": "Arnold Newman",
    "Diane Arbus": "Diane Arbus",
    "Garry Winogrand": "Garry Winogrand",
    "Lee Friedlander": "Lee Friedlander",
    "Elliot Erwitt": "Elliott Erwitt",
    "Joel Meyerowitz": "Joel Meyerowitz",
    "William Eggleston": "William Eggleston",
    "Stephen Shore": "Stephen Shore",
    "Cindy Sherman": "Cindy Sherman",
    "Nan Goldin": "Nan Goldin",
    "Sally Mann": "Sally Mann",
    "Robert Mapplethorpe": "Robert Mapplethorpe",
    "Annie Leibovitz": "Annie Leibovitz",
    "Sebastiao Salgado": "Sebastiao Salgado",
    "Steve McCurry": "Steve McCurry",
    "James Nachtwey": "James Nachtwey",
    "Don McCullin": "Don McCullin",
    "Nick Ut": "Nick Ut",
    "Eddie Adams": "Eddie Adams (photographer)",
    "Joe Rosenthal": "Joe Rosenthal",
    "Alfred Eisenstaedt": "Alfred Eisenstaedt",
    "Mary Ellen Mark": "Mary Ellen Mark",
    "Imogen Cunningham": "Imogen Cunningham",
    "Edward Weston": "Edward Weston",
    "Paul Strand": "Paul Strand",
    "Andreas Gursky": "Andreas Gursky",
    "Thomas Struth": "Thomas Struth",
    "Wolfgang Tillmans": "Wolfgang Tillmans",
    "Martin Parr": "Martin Parr",
    "Hiroshi Sugimoto": "Hiroshi Sugimoto",
    "Nobuyoshi Araki": "Nobuyoshi Araki",
    "Daido Moriyama": "Daido Moriyama",
    "Gregory Crewdson": "Gregory Crewdson",
    "Vivian Maier": "Vivian Maier",
    "Saul Leiter": "Saul Leiter",
    "Francesca Woodman": "Francesca Woodman",
    "Jacques-Henri Lartigue": "Jacques Henri Lartigue",
    "Ilse Bing": "Ilse Bing",
    "Eve Arnold": "Eve Arnold",
    "Gordon Parks": "Gordon Parks",
    "Ernst Haas": "Ernst Haas",
    "Andres Serrano": "Andres Serrano",
    "Joel Sternfeld": "Joel Sternfeld",
    "Gordon Parks": "Gordon Parks",
}

photographers = [
    # Pionniers
    {"n": "Nadar", "na": "French", "bo": "1820", "di": "1910", "st": "Portrait", "fw": "Portrait of Sarah Bernhardt", "fa": "The first photographer to use electric light in a studio; he also made the first aerial photographs from a hot air balloon in 1858, pioneering aerial photography"},
    {"n": "Julia Margaret Cameron", "na": "British", "bo": "1815", "di": "1879", "st": "Pictorialism", "fw": "Whisper of the Muse", "fa": "Received her first camera at 48 as a gift; her soft-focus portraits of Tennyson, Darwin and Victorian celebrities deliberately blurred the line between photography and painting"},
    {"n": "Eadweard Muybridge", "na": "British/American", "bo": "1830", "di": "1904", "st": "Motion Study", "fw": "The Horse in Motion", "fa": "Settled a bet by proving that horses have all four hooves off the ground simultaneously; his 1878 sequence images became the foundation of cinema"},
    {"n": "Lewis Hine", "na": "American", "bo": "1874", "di": "1940", "st": "Documentary", "fw": "Child laborers in cotton mill", "fa": "His photographs of child laborers in factories and mines directly led to US child labor laws in 1938; he also documented workers building the Empire State Building"},
    {"n": "Jacques-Henri Lartigue", "na": "French", "bo": "1894", "di": "1986", "st": "Snapshot", "fw": "Zissou Racing Car", "fa": "Started photographing at age 6 with his father's camera; his spontaneous images of Edwardian bourgeois life were shown at MoMA in 1963 - 50 years after being taken"},
    # Modernisme et avant-garde
    {"n": "Alfred Stieglitz", "na": "American", "bo": "1864", "di": "1946", "st": "Pictorialism/Straight Photography", "fw": "The Steerage", "fa": "Spent years as editor of Camera Work to establish photography as fine art; discovered and promoted Georgia O'Keeffe, whom he later married"},
    {"n": "Edward Steichen", "na": "American", "bo": "1879", "di": "1973", "st": "Pictorialism/Fashion", "fw": "The Pond Moonlight", "fa": "Organized The Family of Man at MoMA in 1955 - still the most visited photography exhibition ever, seen by 9 million people across 38 countries"},
    {"n": "Eugene Atget", "na": "French", "bo": "1857", "di": "1927", "st": "Documentary", "fw": "Versailles series", "fa": "Spent 30 years documenting disappearing Paris; ignored in his lifetime, rescued by Berenice Abbott who preserved his glass negatives and introduced him to the Surrealists"},
    {"n": "August Sander", "na": "German", "bo": "1876", "di": "1964", "st": "Typological Portrait", "fw": "Man of the 20th Century", "fa": "Planned to photograph every social type in Germany in one encyclopedic work; the Nazis destroyed his book for showing faces they considered racially unacceptable"},
    {"n": "Man Ray", "na": "American", "bo": "1890", "di": "1976", "st": "Dada/Surrealism", "fw": "Tears", "fa": "Invented rayographs by placing objects directly on photographic paper and exposing them to light; his work dissolved the boundary between photography and fine art"},
    {"n": "Laszlo Moholy-Nagy", "na": "Hungarian", "bo": "1895", "di": "1946", "st": "Constructivism", "fw": "From the Radio Tower Berlin", "fa": "His extreme angles and abstract compositions from the Bauhaus pioneered a new visual language; he wrote that photography was the creation of light - inspiring a generation"},
    {"n": "Brassai", "na": "Hungarian/French", "bo": "1899", "di": "1984", "st": "Documentary/Surrealism", "fw": "Paris de nuit", "fa": "His Paris de nuit was the first major photobook of a city at night; Picasso called him the eye of Paris - he photographed the city exclusively after midnight for years"},
    {"n": "Andre Kertesz", "na": "Hungarian/American", "bo": "1894", "di": "1985", "st": "Humanist Documentary", "fw": "Distortions", "fa": "His photo of a man reading on a Paris rooftop hung in a New York apartment for years before he knew it - when he found it, he said it was him before he knew himself"},
    {"n": "Ilse Bing", "na": "German", "bo": "1899", "di": "1998", "st": "Modernism", "fw": "Self-Portrait with Leica", "fa": "Called the Queen of the Leica for pioneering handheld 35mm street photography in Frankfurt and Paris in the 1930s; fled the Nazis and stopped photographing at age 57"},
    {"n": "Paul Strand", "na": "American", "bo": "1890", "di": "1976", "st": "Straight Photography", "fw": "Wall Street New York", "fa": "His Wall Street photo showing tiny workers dwarfed by enormous bank arches is considered the first political photograph in art history; Stieglitz said Strand had invented a new kind of photography"},
    {"n": "Edward Weston", "na": "American", "bo": "1886", "di": "1958", "st": "Fine Art", "fw": "Pepper No. 30", "fa": "His extreme close-ups of peppers, shells and nudes treated the natural world as abstract sculpture; diagnosed with Parkinson's at 55, he made his last photograph two years later"},
    {"n": "Imogen Cunningham", "na": "American", "bo": "1883", "di": "1976", "st": "Botanical/Portrait", "fw": "Magnolia Blossom", "fa": "Was photographing in her 90s when she died; her close-up botanical prints from the 1920s matched the formal rigor of her Bauhaus contemporaries without knowing them"},
    {"n": "Ernst Haas", "na": "Austrian/American", "bo": "1921", "di": "1986", "st": "Color Abstraction", "fw": "New York in Color series", "fa": "First photographer given a solo show at MoMA in 1962; his abstract color work treating motion, light and reflection as the subject influenced the entire field of color photography"},
    # Humanisme et reportage
    {"n": "Henri Cartier-Bresson", "na": "French", "bo": "1908", "di": "2004", "st": "Humanist Documentary", "fw": "Behind the Gare Saint-Lazare", "fa": "Coined the decisive moment - capturing the instant when form and feeling align perfectly; he taped his Leica with black tape to remain invisible in the street"},
    {"n": "Robert Capa", "na": "Hungarian/American", "bo": "1913", "di": "1954", "st": "War Photography", "fw": "The Falling Soldier", "fa": "Survived D-Day landing with Allied troops; died stepping on a landmine in Vietnam - his last words as he fell were reportedly about getting a good shot"},
    {"n": "Robert Doisneau", "na": "French", "bo": "1912", "di": "1994", "st": "Humanist Photography", "fw": "Le Baiser de l Hotel de Ville", "fa": "The famous kiss photo was actually staged with two student actors - a fact Doisneau hid for 40 years; the woman sued him after seeing it in a gallery window"},
    {"n": "W. Eugene Smith", "na": "American", "bo": "1918", "di": "1978", "st": "Photo Essay", "fw": "Country Doctor", "fa": "His 28-page Life magazine essay on a country doctor defined the photo essay format; he was beaten severely for his Minamata mercury poisoning coverage in Japan"},
    {"n": "Margaret Bourke-White", "na": "American", "bo": "1904", "di": "1971", "st": "Photojournalism", "fw": "Fort Peck Dam", "fa": "The first American female war correspondent; photographed Gandhi the day before his assassination and the liberation of Buchenwald concentration camp in 1945"},
    {"n": "Gordon Parks", "na": "American", "bo": "1912", "di": "2006", "st": "Documentary/Fashion", "fw": "American Gothic", "fa": "The first African-American photographer at Life magazine; his American Gothic showing a Black cleaning woman before an American flag became an icon of racial inequality"},
    {"n": "Eve Arnold", "na": "American", "bo": "1912", "di": "2012", "st": "Photojournalism", "fw": "Marilyn Monroe on the set of The Misfits", "fa": "One of the first women to join Magnum Photos; her decade-long access to Marilyn Monroe produced intimate images that contradicted the star's public persona"},
    {"n": "Yousuf Karsh", "na": "Armenian-Canadian", "bo": "1908", "di": "2002", "st": "Portrait", "fw": "Churchill portrait 1941", "fa": "His Churchill portrait was taken when Karsh snatched the Prime Minister's cigar to get a fierce expression; Churchill's face went from jovial to thunderous in an instant"},
    {"n": "Weegee", "na": "American", "bo": "1899", "di": "1968", "st": "Press Photography", "fw": "Their First Murder", "fa": "Had a police scanner in his car and slept outside New York Police HQ; he photographed murders, fires and arrests so fast that police sometimes arrived after him"},
    {"n": "Elliot Erwitt", "na": "American", "bo": "1928", "di": "2023", "st": "Humanist/Humor", "fw": "New York City mother and child", "fa": "His images of dogs and their owners elevated pets to subjects of philosophical contemplation; his humor was so light-footed that viewers laughed before they understood why"},
    # Mode et portrait
    {"n": "Irving Penn", "na": "American", "bo": "1917", "di": "2009", "st": "Fashion/Still Life", "fw": "Cigarettes 1972", "fa": "His fashion minimalism - shooting in natural north light against a grey backdrop - stripped away studio artifice; his cigarette butts series elevated trash to art"},
    {"n": "Richard Avedon", "na": "American", "bo": "1923", "di": "2004", "st": "Fashion/Portrait", "fw": "Dovima with Elephants", "fa": "His white background stripped subjects of all context; he photographed his dying father over 8 years - the resulting series redefines portrait photography"},
    {"n": "Helmut Newton", "na": "German/Australian", "bo": "1920", "di": "2004", "st": "Fashion/Erotica", "fw": "Big Nudes", "fa": "His powerful confrontational female nudes reversed the power dynamic in fashion photography; he died when his car accelerated into a wall leaving the Chateau Marmont hotel"},
    {"n": "Guy Bourdin", "na": "French", "bo": "1928", "di": "1991", "st": "Fashion/Surrealism", "fw": "Charles Jourdan shoes campaign", "fa": "His shoe ads were regularly refused by magazines for being too disturbing; crime scenes, mannequin limbs and surrealist staging made shoe ads into art objects worth collecting"},
    {"n": "David Bailey", "na": "British", "bo": "1938", "di": "-", "st": "Fashion/Portrait", "fw": "Jean Shrimpton portraits", "fa": "Turned fashion photography from aristocratic formality to rock-and-roll energy; he was the model for the photographer in Antonioni's Blow-Up - the defining film about photographer obsession"},
    {"n": "Philippe Halsman", "na": "American", "bo": "1906", "di": "1979", "st": "Portrait/Surrealism", "fw": "Dali Atomicus", "fa": "Co-created Dali Atomicus with Dali himself; assistants threw three cats and a bucket of water 26 times before getting the shot with Dali leaping in front of his painting"},
    {"n": "Arnold Newman", "na": "American", "bo": "1918", "di": "2006", "st": "Environmental Portrait", "fw": "Igor Stravinsky at the piano", "fa": "Invented environmental portraiture: placing subjects in their natural workspace; his portrait of Stravinsky bent over a Steinway piano is the defining image of the composer"},
    # Photographie sociale
    {"n": "Dorothea Lange", "na": "American", "bo": "1895", "di": "1965", "st": "Documentary", "fw": "Migrant Mother 1936", "fa": "Migrant Mother is the most reproduced photograph in history; the subject Florence Owens Thompson spent her life asking for royalties - Lange had sold the image to the government"},
    {"n": "Walker Evans", "na": "American", "bo": "1903", "di": "1975", "st": "Documentary", "fw": "Allie Mae Burroughs 1936", "fa": "His Let Us Now Praise Famous Men documented Alabama sharecroppers; his direct unsentimental photography became the DNA of American documentary tradition"},
    {"n": "Ansel Adams", "na": "American", "bo": "1902", "di": "1984", "st": "Landscape", "fw": "Moonrise Hernandez 1941", "fa": "Developed the Zone System to perfectly control exposure and development; Moonrise Hernandez was taken in 30 seconds before the light disappeared - one of the most printed photographs ever"},
    {"n": "Berenice Abbott", "na": "American", "bo": "1898", "di": "1991", "st": "Documentary", "fw": "Changing New York", "fa": "Rescued Eugene Atget's 8,000 negatives and printed them for decades; her Changing New York documented Manhattan's transformation - now an invaluable historical record"},
    {"n": "Lisette Model", "na": "Austrian/American", "bo": "1901", "di": "1983", "st": "Street Photography", "fw": "Coney Island Bather", "fa": "Her confrontational images were taken with a camera at hip level; she taught Diane Arbus, who called her the most important influence on her work"},
    {"n": "Diane Arbus", "na": "American", "bo": "1923", "di": "1971", "st": "Documentary Portrait", "fw": "Identical Twins Roselle 1967", "fa": "Her photographs of people on the margins - giants, nudists, twins, drag queens - replaced pity with dignity; Kubrick used her twins photo as direct inspiration for The Shining"},
    {"n": "Garry Winogrand", "na": "American", "bo": "1928", "di": "1984", "st": "Street Photography", "fw": "World's Fair New York 1964", "fa": "Left 2,500 undeveloped rolls of film when he died - so prolific he could not review his own work; the posthumous prints revealed an extraordinary hidden archive"},
    {"n": "Lee Friedlander", "na": "American", "bo": "1934", "di": "-", "st": "Street Photography", "fw": "Self-Portrait series", "fa": "Pioneered using his own shadow and reflection as compositional elements, creating a new kind of self-portrait where the photographer haunts rather than poses in the image"},
    # Couleur et contemporain
    {"n": "William Eggleston", "na": "American", "bo": "1939", "di": "-", "st": "Colour Photography", "fw": "The Red Ceiling 1973", "fa": "His 1976 MoMA show of color photographs was called perfectly banal by critics; it is now considered the show that legitimized color photography as fine art"},
    {"n": "Stephen Shore", "na": "American", "bo": "1947", "di": "-", "st": "Colour Photography", "fw": "US 97 Pringle Oregon 1973", "fa": "Drove across America photographing diners, motel rooms and gas stations; his large format color images of ordinary America became the grammar of an entire photographic movement"},
    {"n": "Joel Meyerowitz", "na": "American", "bo": "1938", "di": "-", "st": "Street/Color Photography", "fw": "Cape Light series", "fa": "Was the only photographer given unrestricted access to Ground Zero after 9/11; his archive of 8,000 images is the definitive documentary record of the site"},
    {"n": "Saul Leiter", "na": "American", "bo": "1923", "di": "2013", "st": "Color Photography", "fw": "Red Umbrella 1958", "fa": "Gave up a career in fashion photography to pursue personal work; his richly atmospheric color images of New York were ignored for 50 years before being acclaimed as the start of modern color photography"},
    {"n": "Joel Sternfeld", "na": "American", "bo": "1944", "di": "-", "st": "Colour Photography", "fw": "American Prospects", "fa": "His American Prospects series photographed the American landscape in large format color for five years; his image of a man watching a house burn while a pumpkin stand operates nearby became iconic"},
    {"n": "Cindy Sherman", "na": "American", "bo": "1954", "di": "-", "st": "Conceptual", "fw": "Untitled Film Stills", "fa": "Has never photographed anyone but herself - in 50 years every image is a self-portrait in costume; Untitled Film Still no. 21 sold for 3.9 million dollars in 2011"},
    {"n": "Nan Goldin", "na": "American", "bo": "1953", "di": "-", "st": "Documentary/Confessional", "fw": "The Ballad of Sexual Dependency", "fa": "Her decade-long intimate slideshow of her friends in New York gave human faces to a generation lost to AIDS; she became a key activist against OxyContin manufacturers"},
    {"n": "Sally Mann", "na": "American", "bo": "1951", "di": "-", "st": "Fine Art", "fw": "Immediate Family", "fa": "Her photographs of her own children sparked a censorship controversy in 1992; she went on to photograph decomposing bodies in a forensic study of mortality and beauty"},
    {"n": "Robert Mapplethorpe", "na": "American", "bo": "1946", "di": "1989", "st": "Fine Art/Portrait", "fw": "Self-Portrait with Gun 1988", "fa": "His retrospective at Cincinnati in 1990 led to the director being charged with obscenity - and acquitted; the case defined American art censorship law for a generation"},
    {"n": "Annie Leibovitz", "na": "American", "bo": "1949", "di": "-", "st": "Portrait", "fw": "John Lennon and Yoko Ono 1980", "fa": "The Lennon photo was taken hours before his murder - when Yoko saw the proof she said this was the picture that tells the truth; Leibovitz became Rolling Stone's first staff photographer at 21"},
    # Photojournalisme de guerre
    {"n": "Sebastiao Salgado", "na": "Brazilian", "bo": "1944", "di": "-", "st": "Documentary", "fw": "Workers series", "fa": "Spent 6 years photographing gold miners in Brazil; the resulting images of 50,000 men looked like a Dore illustration of hell; he then replanted 2.7 million trees on his family's land"},
    {"n": "Steve McCurry", "na": "American", "bo": "1950", "di": "-", "st": "Photojournalism", "fw": "Afghan Girl 1984", "fa": "Afghan Girl with green eyes ran on the June 1985 National Geographic cover; the girl was not identified for 17 years; McCurry found her again in 2002"},
    {"n": "James Nachtwey", "na": "American", "bo": "1948", "di": "-", "st": "War Photography", "fw": "Rwanda genocide 1994", "fa": "Has covered every major war and humanitarian crisis since 1981; his work on drug-resistant tuberculosis was credited with opening 100 million dollars in emergency funding from the Gates Foundation"},
    {"n": "Don McCullin", "na": "British", "bo": "1935", "di": "-", "st": "War Photography", "fw": "Shell-Shocked Soldier Hue 1968", "fa": "His Vietnam images were so disturbing the British government refused him a press pass to the Falklands War; he spent decades photographing rural Somerset to recover from what he had seen"},
    {"n": "Nick Ut", "na": "Vietnamese-American", "bo": "1951", "di": "-", "st": "War Photography", "fw": "The Terror of War 1972", "fa": "His photo of a 9-year-old girl running from a napalm attack won the 1973 Pulitzer Prize; he immediately took the girl to hospital after taking the shot and saved her life"},
    {"n": "Eddie Adams", "na": "American", "bo": "1933", "di": "2004", "st": "War Photography", "fw": "Saigon Execution 1968", "fa": "His Pulitzer-winning photo of a prisoner being shot at point-blank range changed American opinion on Vietnam; Adams said it destroyed two lives - the executed and the executioner"},
    {"n": "Joe Rosenthal", "na": "American", "bo": "1911", "di": "2006", "st": "War Photography", "fw": "Raising the Flag on Iwo Jima 1945", "fa": "His flag-raising photo took 1/400th of a second; it became the most reproduced photograph in history and the model for the US Marine Corps War Memorial in Arlington"},
    {"n": "Alfred Eisenstaedt", "na": "American", "bo": "1898", "di": "1995", "st": "Photojournalism", "fw": "V-J Day in Times Square 1945", "fa": "The V-J Day kissing sailor photo appeared in Life magazine; the identities of the sailor and nurse were disputed by at least 11 different people claiming to be the subjects"},
    {"n": "Mary Ellen Mark", "na": "American", "bo": "1940", "di": "2015", "st": "Documentary", "fw": "Falkland Road 1981", "fa": "Spent 6 weeks living in Mumbai's red-light district to photograph its inhabitants; her empathetic approach to marginalised communities influenced a generation of photographers"},
    # Art photographique contemporain
    {"n": "Andreas Gursky", "na": "German", "bo": "1955", "di": "-", "st": "Large Scale Art Photography", "fw": "Rhine II 1999", "fa": "Rhine II sold for 4.3 million dollars in 2011, then a record for a photograph; his panoramic images of stock exchanges and concerts reduce humanity to a repeating pattern"},
    {"n": "Hiroshi Sugimoto", "na": "Japanese", "bo": "1948", "di": "-", "st": "Conceptual", "fw": "Movie Theater series", "fa": "Left his camera open for an entire film screening - the moving images averaged into a blank white rectangle of light; the films disappeared, leaving only time visible"},
    {"n": "Martin Parr", "na": "British", "bo": "1952", "di": "-", "st": "Social Documentary", "fw": "The Last Resort", "fa": "His The Last Resort documented British seaside holidays with garish colour and biting observation; condemned as exploitative by critics and beloved by the public"},
    {"n": "Wolfgang Tillmans", "na": "German", "bo": "1968", "di": "-", "st": "Contemporary", "fw": "Concorde over the Pacific", "fa": "The first photographer to win the Turner Prize in 2000; his installations print photographs in many sizes and pin them at different heights - treating the exhibition space as a photograph"},
    {"n": "Gregory Crewdson", "na": "American", "bo": "1962", "di": "-", "st": "Cinematic", "fw": "Twilight series", "fa": "Each photograph requires a Hollywood-scale production: a crew of 50, a week of preparation, and a single suburban American moment of unease shot with a large format view camera"},
    {"n": "Vivian Maier", "na": "American", "bo": "1926", "di": "2009", "st": "Street Photography", "fw": "Self-Portrait New York 1953", "fa": "Worked as a nanny for 40 years; her 150,000 negatives were discovered and auctioned in a storage locker after her death - she had never shown her work to a single person"},
    {"n": "Francesca Woodman", "na": "American", "bo": "1958", "di": "1981", "st": "Conceptual Self-Portrait", "fw": "Space2 Providence Rhode Island 1975", "fa": "Created nearly 800 photographs between age 13 and her death at 22; her ghostly self-portraits blurring into walls were largely unknown until a retrospective 20 years after her death"},
    # Photographes japonais
    {"n": "Nobuyoshi Araki", "na": "Japanese", "bo": "1940", "di": "-", "st": "Intimate Diary Photography", "fw": "Sentimental Journey", "fa": "Photographed his wife Yoko over their entire marriage including her death and its aftermath; the resulting work is one of the most intimate documentary projects in photography", "wl": "red", "wi": "Multiple models publicly accused him of non-consensual photography and sexual coercion. Czech photographer Kaori made a formal public statement in 2019. His main publisher ended their partnership following the accusations."},
    {"n": "Daido Moriyama", "na": "Japanese", "bo": "1938", "di": "-", "st": "Street Photography", "fw": "Stray Dog 1971", "fa": "His blurred high-contrast black-and-white images of Tokyo at night created a visual language of urban alienation; he shoots hundreds of rolls a week and selects in the editing"},
    {"n": "Thomas Struth", "na": "German", "bo": "1954", "di": "-", "st": "Conceptual", "fw": "Museum Photographs series", "fa": "His large photographs of museum visitors staring at famous paintings reflect on how we look at art; photographing the act of seeing became his subject"},
    {"n": "Andres Serrano", "na": "American", "bo": "1950", "di": "-", "st": "Conceptual/Provocative", "fw": "Piss Christ 1987", "fa": "Piss Christ provoked riots, death threats and government debates over arts funding; Serrano argued it was a meditation on the commercialization of Christian imagery, not blasphemy"},
    # Autres contemporains
    {"n": "Rineke Dijkstra", "na": "Dutch", "bo": "1959", "di": "-", "st": "Portrait", "fw": "Beach Portraits series", "fa": "Her series of teenagers on beaches across the world captures adolescent vulnerability with such precision that viewers recognize their own past self in the subjects"},
    {"n": "Nan Goldin", "na": "American", "bo": "1953", "di": "-", "st": "Intimate Documentary", "fw": "Nan One Month After Being Battered 1984", "fa": "Her self-portrait after domestic violence became one of the most powerful images in photography; it transformed how abuse victims were seen by turning private trauma into public art"},
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
    seen = set()
    deduped = []
    for s in photographers:
        if s["n"] not in seen:
            seen.add(s["n"])
            deduped.append(s)

    total = len(deduped)
    found = 0
    for i, s in enumerate(deduped):
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

    out = Path("assets/art/photographers.json")
    out.write_text(json.dumps(deduped, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    summary = "\nDone: {}/{} images -- {} photographers total.\n".format(found, total, total)
    sys.stdout.buffer.write(summary.encode("utf-8"))

if __name__ == "__main__":
    main()
