import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=name, yr=year, ca=category, co=country, fa=famous_for, im=imageUrl

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_EN = {
    "Wilhelm Rontgen": "Wilhelm Rontgen",
    "Marie Curie": "Marie Curie",
    "Albert Einstein": "Albert Einstein",
    "Niels Bohr": "Niels Bohr",
    "Werner Heisenberg": "Werner Heisenberg",
    "Erwin Schrodinger": "Erwin Schrodinger",
    "Paul Dirac": "Paul Dirac",
    "Enrico Fermi": "Enrico Fermi",
    "Max Planck": "Max Planck",
    "Richard Feynman": "Richard Feynman",
    "John Bardeen": "John Bardeen",
    "Ernest Rutherford": "Ernest Rutherford",
    "William Bragg": "William Lawrence Bragg",
    "Peter Higgs": "Peter Higgs",
    "Andre Geim": "Andre Geim",
    "Donna Strickland": "Donna Strickland",
    "Pierre and Marie Curie": "Pierre Curie",
    "Antoine Henri Becquerel": "Henri Becquerel",
    "Guglielmo Marconi": "Guglielmo Marconi",
    "Robert Koch": "Robert Koch",
    "Alexander Fleming": "Alexander Fleming",
    "James Watson": "James Watson",
    "Francis Crick": "Francis Crick",
    "Barbara McClintock": "Barbara McClintock",
    "Christiaan Barnard": "Christiaan Barnard",
    "Jonas Salk": "Jonas Salk",
    "Linus Pauling": "Linus Pauling",
    "Fritz Haber": "Fritz Haber",
    "Antoine Lavoisier": "Antoine Lavoisier",
    "Frederick Sanger": "Frederick Sanger",
    "Ahmed Zewail": "Ahmed Zewail",
    "William Faulkner": "William Faulkner",
    "Ernest Hemingway": "Ernest Hemingway",
    "Albert Camus": "Albert Camus",
    "Jean-Paul Sartre": "Jean-Paul Sartre",
    "Pablo Neruda": "Pablo Neruda",
    "Gabriel Garcia Marquez": "Gabriel Garcia Marquez",
    "Toni Morrison": "Toni Morrison",
    "Samuel Beckett": "Samuel Beckett",
    "Doris Lessing": "Doris Lessing",
    "Rabindranath Tagore": "Rabindranath Tagore",
    "Boris Pasternak": "Boris Pasternak",
    "Alexander Solzhenitsyn": "Alexander Solzhenitsyn",
    "Wole Soyinka": "Wole Soyinka",
    "Orhan Pamuk": "Orhan Pamuk",
    "Alice Munro": "Alice Munro",
    "Bob Dylan": "Bob Dylan",
    "Peter Handke": "Peter Handke",
    "Mo Yan": "Mo Yan",
    "Elfriede Jelinek": "Elfriede Jelinek",
    "Nelson Mandela": "Nelson Mandela",
    "Mother Teresa": "Mother Teresa",
    "Martin Luther King Jr": "Martin Luther King Jr.",
    "Andrei Sakharov": "Andrei Sakharov",
    "Desmond Tutu": "Desmond Tutu",
    "Aung San Suu Kyi": "Aung San Suu Kyi",
    "Malala Yousafzai": "Malala Yousafzai",
    "Barack Obama": "Barack Obama",
    "Henri Dunant": "Henry Dunant",
    "ICRC": "International Committee of the Red Cross",
    "Fridtjof Nansen": "Fridtjof Nansen",
    "Elie Wiesel": "Elie Wiesel",
    "Mikhail Gorbachev": "Mikhail Gorbachev",
    "Yasser Arafat": "Yasser Arafat",
    "Wangari Maathai": "Wangari Maathai",
    "Liu Xiaobo": "Liu Xiaobo",
    "Milton Friedman": "Milton Friedman",
    "John Nash": "John Forbes Nash Jr.",
    "Paul Krugman": "Paul Krugman",
    "Amartya Sen": "Amartya Sen",
    "Muhammad Yunus": "Muhammad Yunus",
    "Daniel Kahneman": "Daniel Kahneman",
    "Friedrich Hayek": "Friedrich Hayek",
    "Simon Kuznets": "Simon Kuznets",
    "Paul Samuelson": "Paul Samuelson",
    "Gary Becker": "Gary Becker",
    "Angus Deaton": "Angus Deaton",
    "Richard Thaler": "Richard Thaler",
    "Esther Duflo": "Esther Duflo",
    "William Nordhaus": "William Nordhaus",
}

prizes = [
    # Physique
    {"n": "Wilhelm Rontgen", "yr": "1901", "ca": "Physics", "co": "Germany", "fa": "Received the very first Nobel Prize in Physics for discovering X-rays in 1895; he refused to take out patents on his discovery so it would remain freely available to science and medicine"},
    {"n": "Pierre and Marie Curie", "yr": "1903", "ca": "Physics", "co": "France/Poland", "fa": "The only couple to share a Nobel Prize; Marie Curie was the first woman to win a Nobel and the only person to win two in different sciences; her notebooks are still too radioactive to handle without lead gloves"},
    {"n": "Antoine Henri Becquerel", "yr": "1903", "ca": "Physics", "co": "France", "fa": "Shared the prize with the Curies for discovering radioactivity; he accidentally discovered it by leaving uranium salts on a photographic plate in a drawer - the radiation exposed the plate in the dark"},
    {"n": "Guglielmo Marconi", "yr": "1909", "ca": "Physics", "co": "Italy", "fa": "Invented wireless radio communication; the first transatlantic radio message in 1901 was the Morse code letter S; the Titanic survivors owed their rescue to Marconi's technology"},
    {"n": "Max Planck", "yr": "1918", "ca": "Physics", "co": "Germany", "fa": "Founded quantum theory by proposing that energy comes in discrete packets called quanta; he called it a desperate act that saved his thermodynamic equations - not realizing he had just changed physics forever"},
    {"n": "Albert Einstein", "yr": "1921", "ca": "Physics", "co": "Germany/USA", "fa": "Won not for relativity (considered too speculative) but for explaining the photoelectric effect; he gave his Nobel Prize money to his ex-wife as promised in their divorce settlement"},
    {"n": "Niels Bohr", "yr": "1922", "ca": "Physics", "co": "Denmark", "fa": "His model of the atom - electrons orbiting a nucleus in fixed shells - transformed chemistry; he escaped occupied Denmark by fishing boat in 1943, then helped the Manhattan Project in secret"},
    {"n": "Werner Heisenberg", "yr": "1932", "ca": "Physics", "co": "Germany", "fa": "Formulated the uncertainty principle: the more precisely you know a particle's position, the less precisely you can know its momentum; he led Germany's nuclear program in WWII but it never succeeded"},
    {"n": "Erwin Schrodinger", "yr": "1933", "ca": "Physics", "co": "Austria", "fa": "His cat thought experiment illustrates the absurdity of quantum superposition at the macro level; he fled Nazi Germany with both his wife and his mistress and settled in Dublin"},
    {"n": "Paul Dirac", "yr": "1933", "ca": "Physics", "co": "UK", "fa": "Predicted antimatter exists before it was discovered; so famously taciturn that colleagues invented the Dirac unit: one word per hour; he wrote one of the most elegant equations in physics"},
    {"n": "Enrico Fermi", "yr": "1938", "ca": "Physics", "co": "Italy/USA", "fa": "On the way from Stockholm to the US, he never returned to Fascist Italy; led the team that built the first nuclear reactor under a Chicago stadium in 1942 - changing history with a secret controlled reaction"},
    {"n": "Ernest Rutherford", "yr": "1908", "ca": "Chemistry", "co": "New Zealand/UK", "fa": "Won Chemistry while considering himself a physicist; his gold foil experiment discovered the atomic nucleus in 1909 - he said it was like firing artillery shells at tissue paper and having them bounce back"},
    {"n": "John Bardeen", "yr": "1956 and 1972", "ca": "Physics", "co": "USA", "fa": "The only person to win the Nobel Prize in Physics twice: once for the transistor (which made all modern electronics possible) and once for superconductivity theory"},
    {"n": "Richard Feynman", "yr": "1965", "ca": "Physics", "co": "USA", "fa": "Developed quantum electrodynamics using diagrams now named after him; demonstrated the Challenger shuttle O-ring failure by dropping one in ice water at a congressional hearing - taking 30 seconds to solve what NASA had missed"},
    {"n": "Peter Higgs", "yr": "2013", "ca": "Physics", "co": "UK", "fa": "Predicted the existence of the Higgs boson in 1964; it was finally confirmed by the Large Hadron Collider in 2012 - 48 years later; the particle that gives matter its mass is now called the God Particle"},
    {"n": "Andre Geim", "yr": "2010", "ca": "Physics", "co": "Netherlands/UK", "fa": "Won for graphene, the wonder material; he is the only Nobel laureate also to have won the Ig Nobel Prize (for levitating a frog with magnets) - the playful prize for improbable research"},
    {"n": "Donna Strickland", "yr": "2018", "ca": "Physics", "co": "Canada", "fa": "Only the third woman to win the Physics Nobel in 117 years; won for chirped pulse amplification, used in laser eye surgery; Wikipedia had refused to create a page for her before the prize because she was not famous enough"},
    {"n": "William Bragg", "yr": "1915", "ca": "Physics", "co": "Australia/UK", "fa": "Won jointly with his father, the only parent-child pair to share a Nobel Prize; at 25 he remains the youngest Physics laureate ever; their work founded X-ray crystallography"},
    # Chimie
    {"n": "Marie Curie", "yr": "1911", "ca": "Chemistry", "co": "Poland/France", "fa": "Her second Nobel - in Chemistry - was for discovering radium and polonium; she named polonium after her occupied homeland Poland; the French Academy of Sciences refused to admit her because she was a woman"},
    {"n": "Linus Pauling", "yr": "1954 and 1962", "ca": "Chemistry/Peace", "co": "USA", "fa": "The only person to win two unshared Nobel Prizes in different categories; his Peace Prize was for nuclear disarmament activism; he was denied a US passport for two years for his political views"},
    {"n": "Fritz Haber", "yr": "1918", "ca": "Chemistry", "co": "Germany", "fa": "His nitrogen fixation process feeds half the world's population today - a genuine miracle; he also developed chemical weapons in WWI and supervised their first use at Ypres; his wife shot herself in protest"},
    {"n": "Frederick Sanger", "yr": "1958 and 1980", "ca": "Chemistry", "co": "UK", "fa": "The only person to win the Chemistry Nobel twice; developed the method to sequence DNA, making the entire Human Genome Project possible; retired modestly to do gardening at age 65"},
    {"n": "Ahmed Zewail", "yr": "1999", "ca": "Chemistry", "co": "Egypt/USA", "fa": "Took the first photographs of atoms in the act of forming and breaking chemical bonds using laser flashes lasting femtoseconds (a millionth of a billionth of a second) - founding femtochemistry"},
    # Medecine et physiologie
    {"n": "Robert Koch", "yr": "1905", "ca": "Medicine", "co": "Germany", "fa": "Identified the bacteria causing tuberculosis, cholera and anthrax; his four postulates for proving a microbe causes a disease are still used today; he named his techniques with the same rigor he applied to microbes"},
    {"n": "Alexander Fleming", "yr": "1945", "ca": "Medicine", "co": "UK", "fa": "Discovered penicillin by noticing mold killing bacteria on a forgotten petri dish; he said luck favors the prepared mind; the antibiotic has saved an estimated 200 million lives since its introduction"},
    {"n": "James Watson", "yr": "1962", "ca": "Medicine", "co": "USA", "fa": "Co-discovered the double helix structure of DNA; their model was built using X-ray diffraction data from Rosalind Franklin without her knowledge - a scientific injustice Franklin died before addressing"},
    {"n": "Francis Crick", "yr": "1962", "ca": "Medicine", "co": "UK", "fa": "Celebrated the double helix discovery by walking into a Cambridge pub and announcing he had found the secret of life; he and Watson were notoriously difficult collaborators who nonetheless changed biology"},
    {"n": "Barbara McClintock", "yr": "1983", "ca": "Medicine", "co": "USA", "fa": "Won at 81 after being dismissed for 30 years; her discovery of jumping genes in corn was called mysticism by her colleagues; the Nobel Committee said she deserved the prize 30 years earlier"},
    {"n": "Christiaan Barnard", "yr": "Not awarded (non-laureate)", "ca": "Medicine", "co": "South Africa", "fa": "Performed the first human heart transplant in 1967; the patient lived 18 days; the Nobel Committee never awarded the prize for it, a decision still debated; Barnard became the most famous surgeon in the world overnight"},
    # Literature
    {"n": "Rabindranath Tagore", "yr": "1913", "ca": "Literature", "co": "India", "fa": "The first Asian to win the Nobel Prize in Literature; his Gitanjali poetry translated into English won the prize; he later wrote the national anthems of both India and Bangladesh - the only person whose words became two national anthems"},
    {"n": "William Faulkner", "yr": "1949", "ca": "Literature", "co": "USA", "fa": "His Nobel speech - just 536 words - is considered the greatest acceptance speech in Nobel history; he declared that the only subject worth writing about is the human heart in conflict with itself"},
    {"n": "Ernest Hemingway", "yr": "1954", "ca": "Literature", "co": "USA", "fa": "Survived two plane crashes in two days in Africa in 1954 and read his own obituaries while in hospital; his doctor told him he was too weak to travel to Stockholm, so he sent a written speech instead"},
    {"n": "Albert Camus", "yr": "1957", "ca": "Literature", "co": "France/Algeria", "fa": "At 44, the second-youngest Literature laureate; he called his fellow finalist Andre Malraux far more deserving; died in a car crash three years later - his Nobel medal was found in the wreckage"},
    {"n": "Jean-Paul Sartre", "yr": "1964", "ca": "Literature", "co": "France", "fa": "Refused the Nobel Prize - the only laureate to decline voluntarily; he said accepting would compromise his integrity as a writer; he also refused the Legion of Honor saying one cannot accept official distinctions"},
    {"n": "Samuel Beckett", "yr": "1969", "ca": "Literature", "co": "Ireland/France", "fa": "Hiding from reporters after the announcement, he only learned he had won from his wife; he called the prize a catastrophe and sent his publisher to Stockholm instead"},
    {"n": "Pablo Neruda", "yr": "1971", "ca": "Literature", "co": "Chile", "fa": "His love poems Veinte poemas de amor are the best-selling Spanish-language poetry book ever written; he died 12 days after the Pinochet coup; friends said he died of cancer, others said of grief"},
    {"n": "Boris Pasternak", "yr": "1958", "ca": "Literature", "co": "USSR", "fa": "Forced by the Soviet government to refuse the prize; a letter was read at the ceremony in Stockholm pleading for help; Doctor Zhivago had been smuggled out of the USSR to be published in Italy"},
    {"n": "Alexander Solzhenitsyn", "yr": "1970", "ca": "Literature", "co": "USSR/USA", "fa": "Could not collect his prize for fear of not being readmitted to the USSR; expelled in 1974 and collected his Nobel in Stockholm after 4 years of exile; The Gulag Archipelago shocked the Western left"},
    {"n": "Gabriel Garcia Marquez", "yr": "1982", "ca": "Literature", "co": "Colombia", "fa": "He had the idea for One Hundred Years of Solitude on the road to Acapulco; turned the car around, drove home, and wrote for 18 months - his wife sold the car and their furniture to feed the family during those months"},
    {"n": "Wole Soyinka", "yr": "1986", "ca": "Literature", "co": "Nigeria", "fa": "The first African writer to receive the Nobel Prize; spent two years in solitary confinement in a Nigerian prison for his political views; wrote a secret book in the margins of a book using homemade ink"},
    {"n": "Toni Morrison", "yr": "1993", "ca": "Literature", "co": "USA", "fa": "Beloved was rejected by 18 publishers; Morrison wrote it while working as an editor at Random House during the day; it won the Pulitzer Prize in 1988 and made her the only Black American woman to win the Nobel in Literature"},
    {"n": "Doris Lessing", "yr": "2007", "ca": "Literature", "co": "UK", "fa": "At 87, the oldest Literature laureate; she learned of the prize from reporters waiting outside her house; she sat on the steps of her London home and said 'Oh, Christ' - the most quotable Nobel response ever"},
    {"n": "Orhan Pamuk", "yr": "2006", "ca": "Literature", "co": "Turkey", "fa": "Faced criminal prosecution in Turkey for publicly acknowledging the Armenian genocide; the charges were dropped after European pressure and one month before his Nobel Prize was announced"},
    {"n": "Alice Munro", "yr": "2013", "ca": "Literature", "co": "Canada", "fa": "The first Canadian and first short story writer to win the prize; she said she wrote stories because she was a mother with not enough time for novels; later revelations about her personal life complicated her legacy"},
    {"n": "Bob Dylan", "yr": "2016", "ca": "Literature", "co": "USA", "fa": "Did not respond to the Nobel Committee for weeks after the announcement; eventually delivered a stunning acceptance lecture comparing himself to Herman Melville; the first musician to receive the Literature prize", "wl": "orange", "wi": "A 2021 civil lawsuit alleged sexual abuse of a 12-year-old girl in 1965. Dylan denied all allegations. The plaintiff voluntarily dismissed the case in 2023. The allegations were not proven in court."},
    {"n": "Mo Yan", "yr": "2012", "ca": "Literature", "co": "China", "fa": "His pen name means do not speak in Chinese; won for his hallucinator realism that merges folk tales and history; the Chinese government celebrated the prize but continued censoring books by his fellow writers"},
    # Paix
    {"n": "Henri Dunant", "yr": "1901", "ca": "Peace", "co": "Switzerland", "fa": "Founded the Red Cross after witnessing the Battle of Solferino in 1859; went bankrupt after the battle, forgotten by the world; a journalist found him in 1895 living in poverty in a hospice - the 1901 prize restored his dignity"},
    {"n": "Fridtjof Nansen", "yr": "1922", "ca": "Peace", "co": "Norway", "fa": "The greatest explorer of his era (first to cross Greenland on skis); later became a diplomat who saved 400,000 Greek and Turkish refugees after WWI using the Nansen passport for stateless people"},
    {"n": "Martin Luther King Jr", "yr": "1964", "ca": "Peace", "co": "USA", "fa": "At 35, the youngest Peace laureate at the time; donated the entire prize money to the civil rights movement; was assassinated four years later while supporting striking sanitation workers"},
    {"n": "Mother Teresa", "yr": "1979", "ca": "Peace", "co": "Albania/India", "fa": "Asked the Nobel Committee to cancel the traditional banquet and donate the money to the poor instead - a saving of 192,000 Norwegian kroner; she used it to feed 15,000 people in Calcutta for a year"},
    {"n": "Andrei Sakharov", "yr": "1975", "ca": "Peace", "co": "USSR", "fa": "The father of the Soviet hydrogen bomb who became its most famous opponent; refused a visa to travel to Oslo; his wife Elena Bonner read his Nobel lecture in his place - KGB agents surrounded the hall"},
    {"n": "Desmond Tutu", "yr": "1984", "ca": "Peace", "co": "South Africa", "fa": "His prize galvanized international sanctions against apartheid South Africa; Nelson Mandela said no single individual did more to focus the world's attention on the injustice of apartheid than Tutu"},
    {"n": "Mikhail Gorbachev", "yr": "1990", "ca": "Peace", "co": "USSR", "fa": "Won for ending the Cold War; celebrated in the West, reviled at home for presiding over the Soviet Union's collapse; he said the prize was the greatest honor and the biggest burden of his life"},
    {"n": "Nelson Mandela", "yr": "1993", "ca": "Peace", "co": "South Africa", "fa": "Shared with F.W. de Klerk for ending apartheid; had spent 27 years in prison on Robben Island; his release and election as South Africa's first Black president was watched by a billion people on television"},
    {"n": "Yasser Arafat", "yr": "1994", "ca": "Peace", "co": "Palestine", "fa": "One of the most controversial Peace Prizes; two committee members resigned in protest; shared with Rabin and Peres for the Oslo Accords; Arafat continued wearing his keffiyeh and pistol holster to the ceremony"},
    {"n": "Aung San Suu Kyi", "yr": "1991", "ca": "Peace", "co": "Myanmar", "fa": "Was under house arrest when she won; her sons accepted in her place; her Nobel was stripped of its moral authority after 2017 when she failed to condemn the military's genocide against the Rohingya people"},
    {"n": "Elie Wiesel", "yr": "1986", "ca": "Peace", "co": "Romania/USA", "fa": "Holocaust survivor whose memoir Night, rejected by 18 publishers and initially only 1,000 copies, eventually sold 10 million copies; he said he wrote because silence in the face of horror is a form of complicity"},
    {"n": "Wangari Maathai", "yr": "2004", "ca": "Peace", "co": "Kenya", "fa": "The first African woman and first environmentalist to receive the Peace Prize; founded the Green Belt Movement which planted 47 million trees in Kenya; imprisoned twice for her activism under Daniel arap Moi"},
    {"n": "Liu Xiaobo", "yr": "2010", "ca": "Peace", "co": "China", "fa": "The empty chair at the Oslo ceremony - China had imprisoned him for subversion; the Chinese government pressured 19 countries to boycott the ceremony; he died in custody in 2017 as the only laureate to die under state detention"},
    {"n": "Malala Yousafzai", "yr": "2014", "ca": "Peace", "co": "Pakistan/UK", "fa": "At 17, the youngest Nobel laureate ever; shot in the head by the Taliban in 2012 for advocating for girls' education; she said one child, one teacher, one pen and one book can change the world"},
    {"n": "Barack Obama", "yr": "2009", "ca": "Peace", "co": "USA", "fa": "Won after just 9 months in office for giving the world hope for international diplomacy; even he admitted it was premature; donated the 1.4 million dollar prize to 10 charities"},
    # Economie
    {"n": "Paul Samuelson", "yr": "1970", "ca": "Economics", "co": "USA", "fa": "His textbook Economics has sold 4 million copies in 41 languages and taught economics to generations of students worldwide; he unified classical and Keynesian economics in a single mathematical framework"},
    {"n": "Friedrich Hayek", "yr": "1974", "ca": "Economics", "co": "Austria/UK", "fa": "Shared his prize with a socialist - the committee forced them to sit together at the banquet; his Road to Serfdom argued that central planning inevitably leads to tyranny, influencing Thatcher and Reagan"},
    {"n": "Milton Friedman", "yr": "1976", "ca": "Economics", "co": "USA", "fa": "His monetarist revolution blamed the Great Depression on the Federal Reserve's failure to expand the money supply; his ideas of free markets and small government became the dominant economic ideology of the 1980s"},
    {"n": "Simon Kuznets", "yr": "1971", "ca": "Economics", "co": "USA", "fa": "Invented Gross Domestic Product as a measurement tool for the US Department of Commerce in 1934; he immediately warned Congress that the welfare of a nation cannot be inferred from the measurement of national income"},
    {"n": "John Nash", "yr": "1994", "ca": "Economics", "co": "USA", "fa": "His Nash equilibrium in game theory is used everywhere from economics to evolutionary biology; he spent decades battling paranoid schizophrenia, documented in the film A Beautiful Mind; died in a taxi crash in 2015"},
    {"n": "Amartya Sen", "yr": "1998", "ca": "Economics", "co": "India", "fa": "His capability approach measures poverty not by income but by what people can actually do and be; he proved that famines never happen in democracies because free press and elections force governments to act"},
    {"n": "Muhammad Yunus", "yr": "2006", "ca": "Peace", "co": "Bangladesh", "fa": "Won the Peace Prize for inventing microcredit through Grameen Bank - making small loans to the rural poor (mostly women) without collateral; lifted millions from poverty using 50 dollars as his first loan"},
    {"n": "Daniel Kahneman", "yr": "2002", "ca": "Economics", "co": "Israel/USA", "fa": "A psychologist who won the Economics Nobel for proving humans are systematically irrational; his Thinking Fast and Slow shows that intuition reliably fails in predictable ways that can be studied and corrected"},
    {"n": "Paul Krugman", "yr": "2008", "ca": "Economics", "co": "USA", "fa": "Won for his theory of economic geography explaining why manufacturing clusters in specific places; announced on the same Monday the global financial crisis peaked; his New York Times column has influenced economic policy for 25 years"},
    {"n": "Esther Duflo", "yr": "2019", "ca": "Economics", "co": "France/USA", "fa": "At 46, the youngest Economics laureate; won with her husband Abhijit Banerjee for applying randomized control trials to poverty reduction - testing anti-poverty programs scientifically instead of ideologically"},
    {"n": "Richard Thaler", "yr": "2017", "ca": "Economics", "co": "USA", "fa": "Won for nudge theory: small changes in how choices are presented dramatically affect decisions; he said he would spend his prize money as irrationally as possible, consistent with his life's work"},
    {"n": "William Nordhaus", "yr": "2018", "ca": "Economics", "co": "USA", "fa": "Won for integrating climate change into long-run macroeconomic analysis; first showed in the 1970s that carbon taxes were the most efficient way to fight global warming - a finding still resisted by political systems"},
    {"n": "Gary Becker", "yr": "1992", "ca": "Economics", "co": "USA", "fa": "Applied economic analysis to human behavior beyond markets: education as investment, crime as rational choice, discrimination as costly irrationality; was derided for reducing human life to equations, then proved right"},
    {"n": "Angus Deaton", "yr": "2015", "ca": "Economics", "co": "UK/USA", "fa": "His research on consumption, poverty and welfare led to the Great Escape - his book showing how modern economic growth has dramatically reduced human misery globally; later documented the deaths of despair in rural America"},
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
    total = len(prizes)
    found = 0
    for i, s in enumerate(prizes):
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
    out = Path("assets/art/nobel_prize.json")
    out.write_text(json.dumps(prizes, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    summary = "\nDone: {}/{} images -- {} laureates total.\n".format(found, total, total)
    sys.stdout.buffer.write(summary.encode("utf-8"))

if __name__ == "__main__":
    main()
