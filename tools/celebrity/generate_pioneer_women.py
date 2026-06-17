import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=name, co=country, yr=years, fi=field, ctx=socio-feminist context of era,
# fa=impact, im=imageUrl

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_EN = {
    "Marie Curie":              "Marie Curie",
    "Simone de Beauvoir":       "Simone de Beauvoir",
    "Rosa Parks":               "Rosa Parks",
    "Florence Nightingale":     "Florence Nightingale",
    "Amelia Earhart":           "Amelia Earhart",
    "Harriet Tubman":           "Harriet Tubman",
    "Wangari Maathai":          "Wangari Maathai",
    "Emmeline Pankhurst":       "Emmeline Pankhurst",
    "Hypatia":                  "Hypatia",
    "Ada Lovelace":             "Ada Lovelace",
    "Sojourner Truth":          "Sojourner Truth",
    "Valentina Tereshkova":     "Valentina Tereshkova",
    "Nellie Bly":               "Nellie Bly",
    "Rigoberta Menchu":         "Rigoberta Menchu",
    "Sally Ride":               "Sally Ride",
    "Olympe de Gouges":         "Olympe de Gouges",
    "Susan B. Anthony":         "Susan B. Anthony",
    "Clara Barton":             "Clara Barton",
    "Razia Sultana":            "Razia Sultana",
    "Marie Curie":              "Marie Curie",
    "Mary Wollstonecraft":      "Mary Wollstonecraft",
    "Elizabeth Blackwell":      "Elizabeth Blackwell",
    "Rosalind Franklin":        "Rosalind Franklin",
    "Malala Yousafzai":         "Malala Yousafzai",
    "Simone Veil":              "Simone Veil",
    "Nelly Bly":                "Nellie Bly",
    # new entries
    "Eleanor Roosevelt":        "Eleanor Roosevelt",
    "Katherine Johnson":        "Katherine Johnson (mathematician)",
    "Sor Juana Ines de la Cruz":"Sor Juana Inés de la Cruz",
    "Elizabeth I":              "Elizabeth I of England",
    "Ruth Bader Ginsburg":      "Ruth Bader Ginsburg",
    "Jane Addams":              "Jane Addams",
    "Rachel Carson":            "Rachel Carson",
    "Virginia Woolf":           "Virginia Woolf",
    "Gerty Cori":               "Gerty Cori",
    "Chien-Shiung Wu":          "Chien-Shiung Wu",
    "Frances Perkins":          "Frances Perkins",
    "Junko Tabei":              "Junko Tabei",
    "Sophie Germain":           "Sophie Germain",
    "Leymah Gbowee":            "Leymah Gbowee",
    "Nettie Stevens":           "Nettie Stevens",
    "Harriet Beecher Stowe":    "Harriet Beecher Stowe",
}

women = [
    # ── Science & Medicine ────────────────────────────────────────────────────
    {"n": "Marie Curie", "co": "Poland / France", "yr": "1867-1934",
     "fi": "Physics & Chemistry",
     "ctx": "Women were barred from higher education in Russian-occupied Poland and excluded from the French Academy of Sciences throughout her life. A woman pursuing a doctorate in physics was virtually unheard of.",
     "fa": "First woman to win a Nobel Prize (1903, Physics) and the only person to win Nobel Prizes in two different sciences (also 1911, Chemistry). Discovered polonium and radium. Her research on radioactivity laid the foundation for nuclear physics and cancer radiotherapy."},

    {"n": "Rosalind Franklin", "co": "United Kingdom", "yr": "1920-1958",
     "fi": "Biophysics & Molecular Biology",
     "ctx": "Women scientists were routinely denied full academic positions and credit for their discoveries. At King's College London, female staff were not allowed in the common room where scientific discussion often happened.",
     "fa": "Her X-ray crystallography work — particularly Photo 51 — was essential to Watson and Crick's discovery of DNA's double helix structure (1953). Her contribution was not acknowledged in their Nobel Prize. She died at 37 of ovarian cancer; her role was only fully recognised posthumously."},

    {"n": "Elizabeth Blackwell", "co": "United States / United Kingdom", "yr": "1821-1910",
     "fi": "Medicine",
     "ctx": "Every American medical school refused her application. She was admitted to Geneva Medical College in New York after the all-male student body voted 'yes' as a joke — not expecting she would actually enroll.",
     "fa": "First woman to receive a medical degree in the United States (1849). Founded the New York Infirmary for Indigent Women and Children. Her persistence shattered the barrier for women entering the medical profession."},

    {"n": "Ada Lovelace", "co": "United Kingdom", "yr": "1815-1852",
     "fi": "Mathematics & Computing",
     "ctx": "In Victorian England, women of the aristocracy were educated in 'ornamental' subjects; mathematics was considered unsuitable for the female mind. Her mother insisted on rigorous mathematical education specifically to counter any 'poetic' tendencies inherited from her father, Lord Byron.",
     "fa": "Wrote the first algorithm intended to be processed by a machine — Charles Babbage's Analytical Engine. Recognised as the world's first computer programmer, a century before the first modern computer was built. The Ada programming language is named in her honour."},

    {"n": "Hypatia", "co": "Egypt (Roman Alexandria)", "yr": "c. 360-415 CE",
     "fi": "Mathematics & Astronomy",
     "ctx": "Late Roman Alexandria was a place of intellectual ferment but also violent religious and political conflict. As a woman holding a public teaching position and intellectual authority, she occupied an almost unique position in the ancient world.",
     "fa": "Head of the Neoplatonist school in Alexandria and the first female mathematician recorded in history. Wrote commentaries on major mathematical and astronomical works. Murdered by a Christian mob in 415 CE; her death is often seen as a symbol of the decline of Greco-Roman science."},

    # ── Activism & Civil Rights ────────────────────────────────────────────────
    {"n": "Harriet Tubman", "co": "United States", "yr": "~1822-1913",
     "fi": "Abolitionism & Civil Rights",
     "ctx": "Born into slavery in Maryland at a time when enslaved people were legally property. The Fugitive Slave Act of 1850 meant even escaped slaves in the North could be captured and returned.",
     "fa": "Escaped slavery in 1849 and returned south approximately 13 times to guide about 70 enslaved people to freedom via the Underground Railroad. During the Civil War, she became the first woman to lead an armed assault — the Combahee River Raid, freeing 700 enslaved people."},

    {"n": "Sojourner Truth", "co": "United States", "yr": "~1797-1883",
     "fi": "Abolitionism & Women's Rights",
     "ctx": "Born into slavery in New York when slavery was still legal there. Even after emancipation, Black women were systematically excluded from the women's suffrage movement by white leaders who feared alienating Southern states.",
     "fa": "Escaped slavery in 1826. Delivered her landmark 'Ain't I a Woman?' speech (1851) challenging the exclusion of Black women from the feminist movement. First Black woman to win a legal case against a white man when she successfully sued for the return of her son in 1828."},

    {"n": "Rosa Parks", "co": "United States", "yr": "1913-2005",
     "fi": "Civil Rights Activism",
     "ctx": "In Alabama in 1955, racial segregation on buses was enforced by law. Black passengers had to give up their seats to white passengers. This was not mere custom — refusal was a criminal act.",
     "fa": "Her arrest in December 1955 for refusing to give up her seat on a Montgomery bus sparked the 381-day Montgomery Bus Boycott, a turning point in the American Civil Rights Movement. Called 'the mother of the civil rights movement' by the US Congress."},

    {"n": "Emmeline Pankhurst", "co": "United Kingdom", "yr": "1858-1928",
     "fi": "Women's Suffrage",
     "ctx": "In Victorian and Edwardian Britain, women of all classes were denied the right to vote. Political arguments that women were too emotional for political decisions were mainstream. Peaceful suffrage campaigns had achieved nothing in 40 years.",
     "fa": "Founded the Women's Social and Political Union (WSPU) in 1903, adopting 'Deeds, not Words' as its motto. Led increasingly militant suffragette campaigns including window-smashing, arson, and hunger strikes in prison. Died weeks before British women finally gained equal voting rights in 1928."},

    {"n": "Olympe de Gouges", "co": "France", "yr": "1748-1793",
     "fi": "Political Writing & Feminism",
     "ctx": "The French Revolution proclaimed 'Liberty, Equality, Fraternity' — but entirely for men. The Declaration of the Rights of Man (1789) explicitly excluded women from political and civil rights.",
     "fa": "Author of the Declaration of the Rights of Woman and of the Female Citizen (1791), which asserted that women are equal to men and deserved the same political rights. Condemned that 'a woman has the right to mount the scaffold; she must equally have the right to mount the rostrum.' Guillotined in 1793."},

    {"n": "Susan B. Anthony", "co": "United States", "yr": "1820-1906",
     "fi": "Women's Suffrage",
     "ctx": "In 19th-century America, married women could not own property, sign contracts, or keep their wages. Women were legally considered the property of their husbands. The suffrage movement was widely ridiculed as absurd and dangerous.",
     "fa": "A central leader of the women's suffrage movement for over 50 years. Arrested and tried for voting in 1872. The 19th Amendment granting women the right to vote (1920) is often called the 'Susan B. Anthony Amendment.' She died 14 years before seeing her life's work become law."},

    {"n": "Mary Wollstonecraft", "co": "United Kingdom", "yr": "1759-1797",
     "fi": "Philosophy & Feminist Writing",
     "ctx": "In 18th-century Britain, women were educated only for marriage and considered intellectually inferior by nature. Rousseau, the era's leading philosopher on education, explicitly argued women should be raised to please men.",
     "fa": "Author of A Vindication of the Rights of Woman (1792), the founding document of modern feminism. Argued that women appeared inferior only because they were denied education. She was the mother of Mary Shelley. Her work was ridiculed in her lifetime; she died at 38 of childbed fever."},

    {"n": "Rigoberta Menchu", "co": "Guatemala", "yr": "1959-",
     "fi": "Indigenous Rights Activism",
     "ctx": "Guatemala's civil war (1960-1996) saw mass atrocities against the indigenous Mayan population. Indigenous women faced triple marginalisation: as women, as indigenous people, and as poor campesinas. Advocating for indigenous rights meant risking death.",
     "fa": "K'iche' Mayan activist who documented human rights abuses during the Guatemalan Civil War. Her autobiography I, Rigoberta Menchú (1983) brought international attention to indigenous oppression. Nobel Peace Prize laureate in 1992 — the first indigenous person so honoured."},

    {"n": "Wangari Maathai", "co": "Kenya", "yr": "1940-2011",
     "fi": "Environmental Activism",
     "ctx": "Post-independence Kenya was governed by authoritarian regimes that criminalised dissent. Women had virtually no voice in political or environmental policy. Deforestation was driving rural poverty, particularly affecting women who collected firewood.",
     "fa": "Founded the Green Belt Movement in 1977, mobilising rural women to plant over 51 million trees across Kenya. First African woman to win the Nobel Peace Prize (2004). First woman to earn a Ph.D. in East and Central Africa. Imprisoned multiple times for her activism."},

    {"n": "Malala Yousafzai", "co": "Pakistan", "yr": "2000-- (b. 1997)",
     "fi": "Education Activism",
     "ctx": "Under Taliban occupation of Pakistan's Swat Valley (2007-2009), girls' schools were bombed and girls forbidden to attend school. The Taliban issued death threats against those who promoted girls' education.",
     "fa": "Survived a Taliban assassination attempt in 2012 at age 15 for publicly advocating for girls' education. Became the youngest Nobel Peace Prize laureate in 2014 (age 17). Founded the Malala Fund, which has helped millions of girls access education worldwide."},

    # ── Aviation & Exploration ─────────────────────────────────────────────────
    {"n": "Amelia Earhart", "co": "United States", "yr": "1897-1937",
     "fi": "Aviation",
     "ctx": "In the 1920s-30s, aviation was an exclusively male domain. Women were considered physically and mentally unfit to pilot aircraft. Female aviators were dismissed as novelty acts rather than serious pilots.",
     "fa": "First woman to fly solo across the Atlantic Ocean (1932). Set multiple world aviation records. Disappeared over the Pacific Ocean in 1937 during an attempted circumnavigation of the globe. Her courage and skill permanently changed attitudes about what women could accomplish."},

    {"n": "Valentina Tereshkova", "co": "Soviet Union (Russia)", "yr": "1937-",
     "fi": "Aerospace",
     "ctx": "The Space Race between the USSR and USA had used only male military pilots as cosmonauts. The selection of a woman was partly a Cold War propaganda move, but Tereshkova proved herself through rigorous training alongside men.",
     "fa": "First woman in space (June 1963), orbiting Earth 48 times over three days aboard Vostok 6. She remains the only woman to have completed a solo space mission. Her flight preceded the second woman in space by 19 years."},

    # ── Journalism & Media ─────────────────────────────────────────────────────
    {"n": "Nellie Bly", "co": "United States", "yr": "1864-1922",
     "fi": "Investigative Journalism",
     "ctx": "In the Gilded Age, newspaper work for women was restricted to 'women's pages' covering fashion and society. Investigative journalism was a men's domain. Mental asylums were largely unregulated and virtually invisible to public scrutiny.",
     "fa": "Pioneered investigative journalism by faking insanity to expose the brutal conditions of New York's Blackwell's Island asylum (1887). Circumnavigated the globe in 72 days, beating Phileas Fogg's fictional record. Her reporting drove direct legal reforms."},

    # ── Nursing & Humanitarianism ─────────────────────────────────────────────
    {"n": "Florence Nightingale", "co": "United Kingdom", "yr": "1820-1910",
     "fi": "Nursing & Public Health",
     "ctx": "Nursing was considered disreputable work for 'fallen women.' Upper-class women were expected to be idle ornaments. The British Army during the Crimean War had no organised medical care and a mortality rate from disease 10× that from battle wounds.",
     "fa": "Transformed nursing into a respected profession. During the Crimean War (1853-1856) she cut hospital mortality rates from 42% to 2% through hygiene reforms. Pioneered the use of statistical graphics in medicine. Founded the first secular nursing school (1860), now part of King's College London."},

    {"n": "Clara Barton", "co": "United States", "yr": "1821-1912",
     "fi": "Nursing & Humanitarian Aid",
     "ctx": "During the American Civil War, women were barred from official military nursing. The social norm was that 'proper' women should not witness or treat battlefield wounds. Organising aid for soldiers was done entirely outside official channels.",
     "fa": "Provided battlefield nursing and supplies during the Civil War despite official obstacles. Founded the American Red Cross in 1881 and served as its first president for 23 years. Lobbied successfully for the U.S. ratification of the Geneva Convention."},

    # ── Philosophy & Social Thought ────────────────────────────────────────────
    {"n": "Simone de Beauvoir", "co": "France", "yr": "1908-1986",
     "fi": "Philosophy & Feminism",
     "ctx": "Post-war France was a deeply patriarchal society where women had only just gained the vote in 1944. The concept of gender as a social construct rather than a biological destiny was radical and widely rejected.",
     "fa": "Author of The Second Sex (1949), the foundational text of second-wave feminism. Her phrase 'One is not born, but rather becomes, a woman' articulated the distinction between biological sex and socially constructed gender. Her work directly inspired the women's liberation movements of the 1960s-70s."},

    {"n": "Simone Veil", "co": "France", "yr": "1927-2017",
     "fi": "Politics & Law",
     "ctx": "In France in 1975, abortion was a criminal act. The debate in the National Assembly was savage; several deputies compared the bill to the Holocaust (which Veil, an Auschwitz survivor, found deeply offensive). Death threats were common.",
     "fa": "Holocaust survivor and French politician who as Health Minister successfully passed the Veil Law (1975) legalising abortion in France, in the face of extraordinary hostility. Elected to the Académie Française. Her legacy spans human rights, European construction, and women's emancipation."},

    # ── Royalty & Power ────────────────────────────────────────────────────────
    {"n": "Razia Sultana", "co": "Delhi Sultanate (India)", "yr": "~1205-1240",
     "fi": "Governance",
     "ctx": "The Delhi Sultanate was a conservative Islamic monarchy in which female rule was considered religiously and politically illegitimate. Her own brothers and nobles repeatedly challenged her authority solely on the grounds of her sex.",
     "fa": "First female Sultan of Delhi (reigned 1236-1240). Rode elephants into battle, appeared unveiled in court, and refused to use a litter. She told her critics: 'If I am worthy to be sultan, my sex is irrelevant.' Ruled competently until overthrown by nobles who could not accept a female sovereign."},

    {"n": "Sally Ride", "co": "United States", "yr": "1951-2012",
     "fi": "Aerospace & Physics",
     "ctx": "NASA had no female astronauts until 1978. The media coverage of Sally Ride's selection was notably patronising — reporters asked if spaceflight would affect her reproductive system and whether she would wear makeup.",
     "fa": "First American woman in space (1983), aboard the Space Shuttle Challenger. Became a physics professor at UC San Diego and founded Sally Ride Science to inspire girls in STEM. Came out as a lesbian in her obituary, making her the first known LGBT astronaut."},

    # ── Politics & Governance ─────────────────────────────────────────────────
    {"n": "Eleanor Roosevelt", "co": "United States", "yr": "1884-1962",
     "fi": "Diplomacy & Human Rights",
     "ctx": "As First Lady, women's roles in government were purely ceremonial. After Franklin D. Roosevelt's death, women were rarely taken seriously in foreign policy. The UN Commission on Human Rights was considered a minor posting when she was appointed.",
     "fa": "Chaired the UN Commission that drafted the Universal Declaration of Human Rights (1948) — arguably the most important human rights document ever written. As First Lady she championed civil rights at a time when her husband hesitated. The most admired woman in the world for many consecutive years."},

    {"n": "Shirley Chisholm", "co": "United States", "yr": "1924-2005",
     "fi": "Politics",
     "ctx": "In 1968 America, being Black and a woman were both considered disqualifying for high political office. The Civil Rights Act was only 4 years old. She faced virulent opposition from both racial and gender discrimination simultaneously.",
     "fa": "First Black woman elected to the US Congress (1968) and first Black candidate to seek a major party presidential nomination (1972). Her campaign slogan was 'Unbought and Unbossed.' She served seven terms in Congress, consistently championing education, social services, and minority rights."},

    {"n": "Indira Gandhi", "co": "India", "yr": "1917-1984",
     "fi": "Politics",
     "ctx": "India in the 1960s was a male-dominated democracy where female political leadership at the national level was virtually unprecedented. As a woman leading the world's largest democracy, she faced deep scepticism from both political opponents and world leaders.",
     "fa": "First and only female Prime Minister of India (served 1966-1977 and 1980-1984). Led India to victory in the 1971 war with Pakistan, overseeing the creation of Bangladesh. Nationalised major industries. Assassinated by her own bodyguards in 1984. The most powerful woman of the 20th century."},

    {"n": "Golda Meir", "co": "Ukraine / Israel", "yr": "1898-1978",
     "fi": "Politics",
     "ctx": "Israel in the 1960s, like most nations, had never had a female head of government. As Prime Minister of a nation literally fighting for survival, she was required to make life-or-death decisions that most women were categorically excluded from in that era.",
     "fa": "Fourth Prime Minister of Israel (1969-1974) and the third female head of government in modern history. Led Israel through the Yom Kippur War (1973). Born in Ukraine, raised in Milwaukee, she was a founding architect of the State of Israel. Called 'the Iron Lady of Israeli politics.'"},

    {"n": "Benazir Bhutto", "co": "Pakistan", "yr": "1953-2007",
     "fi": "Politics",
     "ctx": "Pakistan was a conservative Islamic republic where women's political leadership was considered illegitimate by powerful religious and military factions. Her father had been executed by a military regime. She returned to Pakistan despite credible death threats.",
     "fa": "First female Prime Minister of Pakistan (1988-1990 and 1993-1996) and the first female head of government of a Muslim-majority country. Educated at Harvard and Oxford, she represented a vision of democratic, modern Islam. Assassinated at a political rally in 2007."},

    {"n": "Madeleine Albright", "co": "Czech Republic / United States", "yr": "1937-2022",
     "fi": "Diplomacy",
     "ctx": "The US Secretary of State position had never been held by a woman. Foreign policy had been a male preserve throughout American history. As a refugee from communist Czechoslovakia, she was also a naturalised citizen taking one of the most powerful posts in the world.",
     "fa": "First female US Secretary of State (1997-2001). Oversaw NATO's expansion into Eastern Europe and US policy during the Kosovo War. Known for her signature brooch diplomacy — choosing pins to send diplomatic messages. A powerful voice for democracy and human rights until her death."},

    # ── Science & Mathematics (additional) ────────────────────────────────────
    {"n": "Lise Meitner", "co": "Austria / Sweden", "yr": "1878-1968",
     "fi": "Nuclear Physics",
     "ctx": "Women were barred from attending university in Vienna when Meitner began her studies. In Nazi Germany, her Jewish heritage forced her to flee in 1938, leaving behind 30 years of collaborative work — and the discovery she had just made.",
     "fa": "Co-discovered nuclear fission in 1938 with Otto Hahn, providing the theoretical explanation. Hahn alone received the 1944 Nobel Prize in Chemistry; Meitner was overlooked in what is widely called the greatest injustice in Nobel Prize history. Element 109, meitnerium, is named after her."},

    {"n": "Emmy Noether", "co": "Germany", "yr": "1882-1935",
     "fi": "Mathematics",
     "ctx": "Women were not permitted to enroll in German universities when Noether began studying. She had to audit classes unofficially. Even after earning her doctorate, she taught without salary for years because the University of Gottingen refused to employ women.",
     "fa": "Called 'the most significant creative mathematical genius thus far produced' by Albert Einstein. Noether's Theorem (1915) is one of the most important results in theoretical physics, connecting symmetry and conservation laws. She revolutionised abstract algebra and ring theory."},

    {"n": "Hedy Lamarr", "co": "Austria / United States", "yr": "1914-2000",
     "fi": "Film & Invention",
     "ctx": "In 1940s Hollywood, actresses were considered decorative. The idea that a film star could be a serious inventor was so inconceivable that her co-invention of frequency-hopping spread spectrum was patented but never rewarded financially or professionally during her lifetime.",
     "fa": "MGM star and co-inventor (with composer George Antheil) of frequency-hopping spread spectrum communication (1942), the technology underlying modern Wi-Fi, GPS, and Bluetooth. Inducted into the National Inventors Hall of Fame in 2014. Her patent expired before its commercial potential was realised."},

    {"n": "Katherine Johnson", "co": "United States", "yr": "1918-2020",
     "fi": "Mathematics & Aerospace",
     "ctx": "NASA's computing division employed Black women as 'human computers' in racially segregated facilities. Johnson had to fight to attend mission briefings that were technically restricted to men.",
     "fa": "NASA mathematician whose orbital mechanics calculations were critical to the success of the first US crewed spaceflights, including John Glenn's 1962 orbit. Glenn refused to launch until Johnson personally verified the computer's calculations. Presidential Medal of Freedom (2015); her story was told in Hidden Figures."},

    {"n": "Barbara McClintock", "co": "United States", "yr": "1902-1992",
     "fi": "Genetics",
     "ctx": "When McClintock proposed that genes could move between chromosomes in the 1950s, the scientific establishment was so sceptical she largely stopped publishing. It took 30 years for her peers to understand and accept her discovery.",
     "fa": "Nobel Prize in Physiology or Medicine (1983) for her discovery of genetic transposition — 'jumping genes' — in maize. She won the Nobel alone, at age 81, three decades after the discovery. The first woman to win an unshared Nobel Prize in that category."},

    {"n": "Dorothy Hodgkin", "co": "United Kingdom", "yr": "1910-1994",
     "fi": "Chemistry",
     "ctx": "At Oxford in the 1930s, women were not allowed to be full members of the university. Hodgkin did groundbreaking research under institutional rules that treated female scientists as second-class members of academia.",
     "fa": "Won the Nobel Prize in Chemistry (1964) for using X-ray crystallography to determine the structure of penicillin, vitamin B12, and later insulin — work that enabled the mass production of antibiotics. The third woman to win the Nobel Prize in Chemistry, after Marie Curie and Irene Joliot-Curie."},

    # ── Literature & Culture ──────────────────────────────────────────────────
    {"n": "Toni Morrison", "co": "United States", "yr": "1931-2019",
     "fi": "Literature",
     "ctx": "When Morrison published her first novel in 1970, Black American women writers were almost entirely absent from the mainstream literary canon. Publishing was dominated by white editors and critics who consistently undervalued Black narratives.",
     "fa": "Nobel Prize in Literature (1993) — the first Black woman to receive it. Her novels Beloved, Song of Solomon, and The Bluest Eye are considered among the greatest American novels ever written. Her work centred Black American experience with a power and beauty that permanently expanded American literature."},

    {"n": "Mary Shelley", "co": "United Kingdom", "yr": "1797-1851",
     "fi": "Literature",
     "ctx": "In Regency England, serious literary fiction was almost exclusively a male domain. Women who wrote were expected to produce domestic or religious works. A teenage girl proposing a novel about the ethics of creating artificial life was unprecedented.",
     "fa": "Wrote Frankenstein; or, The Modern Prometheus at age 18, widely considered the first science fiction novel. The book's profound questions about scientific responsibility, creation, and what it means to be human remain central to modern ethical debates. Her mother was feminist philosopher Mary Wollstonecraft."},

    {"n": "George Sand", "co": "France", "yr": "1804-1876",
     "fi": "Literature",
     "ctx": "In 19th-century France, women could not publish under their own names without their husband's permission, own property independently, or appear in public spaces alone. George Sand defied all of these conventions simultaneously.",
     "fa": "One of the most popular French writers of the 19th century, with 60 novels and a vast body of journalism. Adopted a male pseudonym and wore men's clothing to move freely in Parisian society. Had famous relationships with Frederic Chopin and Alfred de Musset. A central figure in Romanticism."},

    # ── Ancient & Medieval ────────────────────────────────────────────────────
    {"n": "Hatshepsut", "co": "Ancient Egypt", "yr": "~1507-~1458 BCE",
     "fi": "Governance",
     "ctx": "In ancient Egypt, the pharaoh was by definition male — the role was fundamentally linked to male gods. Female regents were expected to step aside when a male heir came of age. Hatshepsut did the opposite.",
     "fa": "Female pharaoh of ancient Egypt who reigned for approximately 22 years as the most powerful person in the world at the time. Commissioned some of Egypt's greatest monuments and expanded trade networks. After her death, her successor systematically erased her image and name from official records — a deliberate attempt to erase a woman from history."},

    {"n": "Wu Zetian", "co": "Tang Dynasty China", "yr": "624-705 CE",
     "fi": "Governance",
     "ctx": "In Confucian Chinese society, women were explicitly subordinate in all spheres. The idea of a woman ruling China in her own name — not as regent for a male heir — violated the fundamental social and political order. She was the only person in 4,000 years of Chinese imperial history to do it.",
     "fa": "The only woman in Chinese history to rule as Empress Regnant (690-705 CE). Expanded the empire, reformed the civil service examination to be more meritocratic, and patronised Buddhism. Reigned for 15 years and died at 81, having held effective power for decades before assuming the throne."},

    {"n": "Joan of Arc", "co": "France", "yr": "1412-1431",
     "fi": "Military & Religion",
     "ctx": "Medieval France was engaged in the Hundred Years' War and deeply divided. Military leadership was the exclusive province of noble men. A teenage peasant girl claiming divine guidance to lead an army violated every social, religious, and military norm of the era.",
     "fa": "Led the French army to several important victories at age 17-18 during the Hundred Years' War, reversing the course of the conflict. Captured, tried for heresy by an English-aligned court, and burned at the stake at 19. Declared a martyr and eventually a saint by the Catholic Church (1920). The enduring symbol of French national identity."},

    {"n": "Nzinga of Ndongo", "co": "Angola (Kingdom of Ndongo)", "yr": "~1583-1663",
     "fi": "Governance & Resistance",
     "ctx": "17th-century West-Central Africa was under sustained Portuguese colonisation. The transatlantic slave trade was devastating the region. A woman ruling a kingdom was considered illegitimate by both African traditional norms and European colonial powers.",
     "fa": "Queen of the Mbundu kingdoms of Ndongo and Matamba (modern Angola) who led a 30-year military resistance against Portuguese colonisation. Conducted sophisticated diplomacy — including personally negotiating with the Portuguese governor. Considered the founding mother of Angolan national identity."},

    # ── Exploration ────────────────────────────────────────────────────────────
    {"n": "Sacagawea", "co": "United States (Shoshone Nation)", "yr": "~1788-1812",
     "fi": "Exploration & Diplomacy",
     "ctx": "In 1804 America, Native American women were invisible to white society. Sacagawea joined the Lewis and Clark Expedition as a teenager with a newborn baby, in a role that was unprecedented and entirely outside the social imagination of the era.",
     "fa": "Shoshone interpreter and guide who helped the Lewis and Clark Expedition (1804-1806) navigate from the Missouri River to the Pacific Ocean. Her presence with a baby was essential: it signalled to Native tribes that the expedition was peaceful. Her cultural knowledge was indispensable to the mission's survival."},

    {"n": "Ida B. Wells", "co": "United States", "yr": "1862-1931",
     "fi": "Journalism & Civil Rights",
     "ctx": "Born into slavery in Mississippi, Wells worked as a journalist in a country where both her race and gender made her a target for violence. Her investigation of lynching was so threatening that a mob destroyed her newspaper office.",
     "fa": "Pioneering journalist and civil rights activist who conducted the first systematic investigation of lynching in the American South (1892). Her research destroyed the myth that lynching was a response to sexual assault, revealing it as a tool of racial terror. Co-founded the NAACP and was a leading voice for anti-lynching legislation."},

    {"n": "Sor Juana Ines de la Cruz", "co": "Mexico (New Spain)", "yr": "1648-1695",
     "fi": "Poetry, Philosophy & Science",
     "ctx": "In 17th-century colonial Mexico, intellectual life was the exclusive province of the Catholic Church, which was the exclusive province of men. Women were expected to be silent and obedient to religious authority.",
     "fa": "The first published feminist of the Americas, called 'The Tenth Muse'. A self-taught genius who learned Latin, music, and science — impossible for a woman in her era without entering a convent. Her essay Reply to Sister Filotea (1691) is the first published defence of women's right to education in the Western Hemisphere."},

    # ── Politics & Law (additional) ───────────────────────────────────────────
    {"n": "Elizabeth I", "co": "England", "yr": "1533-1603",
     "fi": "Governance",
     "ctx": "Tudor England had never accepted female rule without controversy. The Salic Law barring women from thrones was widely respected across Europe. Elizabeth's own Parliament repeatedly pressured her to marry and produce a male heir — treating her independent rule as an aberration.",
     "fa": "Queen of England for 44 years (1558-1603), presiding over the Elizabethan era — a golden age of English literature, theatre, and exploration. Defeated the Spanish Armada (1588). Remained unmarried to preserve political independence, declaring 'I know I have the body of a weak and feeble woman, but I have the heart and stomach of a king.' Her reign is one of the most celebrated in European history."},

    {"n": "Ruth Bader Ginsburg", "co": "United States", "yr": "1933-2020",
     "fi": "Law & Civil Rights",
     "ctx": "When Ginsburg attended Harvard Law School in 1956, the dean asked female students to justify taking spots from men. Law firms routinely refused to hire women regardless of qualifications. Discrimination on the basis of sex was not constitutionally prohibited.",
     "fa": "Spent the 1970s systematically dismantling legal sex discrimination as an ACLU attorney, winning landmark cases before the Supreme Court. Appointed to the Supreme Court in 1993, becoming only the second woman ever to serve as a Justice. Her dissents became rallying cries for gender equality. Became a cultural icon — 'the Notorious RBG' — late in life."},

    {"n": "Frances Perkins", "co": "United States", "yr": "1880-1965",
     "fi": "Politics & Labour Rights",
     "ctx": "In 1933, women had never served in a presidential Cabinet. The idea of a woman overseeing the nation's workforce and economy was met with hostility from both Congress and business leaders who refused to take her seriously.",
     "fa": "First female member of a US presidential Cabinet, serving as Secretary of Labor under FDR for 12 years (1933-1945). Designed and implemented most of the New Deal's key labour protections: the Social Security Act, the 40-hour work week, the minimum wage, and the abolition of child labour. Changed the lives of every American worker."},

    # ── Science (additional) ──────────────────────────────────────────────────
    {"n": "Gerty Cori", "co": "Czech Republic / United States", "yr": "1896-1957",
     "fi": "Biochemistry",
     "ctx": "At the time of Gerty Cori's research, women in academia routinely faced institutional bars on advancement. Washington University offered her a research position one-tenth the salary of her husband Carl's, explicitly because she was a woman. She was told her scientific collaboration with her husband was 'unAmerican.'",
     "fa": "First American woman to win a Nobel Prize in science — Nobel Prize in Physiology or Medicine (1947), shared with her husband Carl. Discovered the Cori cycle: how the body converts glycogen to glucose and back, foundational knowledge for treating diabetes and glycogen storage diseases."},

    {"n": "Chien-Shiung Wu", "co": "China / United States", "yr": "1912-1997",
     "fi": "Nuclear Physics",
     "ctx": "In 1950s physics, women were almost entirely absent from experimental research roles. The experiment Wu designed and executed was the definitive proof of one of the most important discoveries in particle physics — yet the Nobel Prize went to the two male theorists whose prediction it verified.",
     "fa": "Conducted the 1956 Wu experiment that disproved the law of conservation of parity — one of the most important experiments in particle physics history. Lee and Yang won the Nobel Prize for their theoretical prediction; Wu, who provided the experimental proof, did not. Called 'the First Lady of Physics.'"},

    {"n": "Rachel Carson", "co": "United States", "yr": "1907-1964",
     "fi": "Marine Biology & Environmental Writing",
     "ctx": "In the early 1960s, the chemical industry was the most powerful lobby in Washington. A woman publishing scientific criticism of pesticide policy was dismissed as an 'emotional hysterical woman.' The industry mounted a $250,000 campaign to destroy her credibility.",
     "fa": "Author of Silent Spring (1962), the book that launched the modern environmental movement. Documented the devastating effect of synthetic pesticides — especially DDT — on wildlife and human health. Led directly to the US ban on DDT and the creation of the Environmental Protection Agency. Died of cancer 18 months after publication."},

    {"n": "Nettie Stevens", "co": "United States", "yr": "1861-1912",
     "fi": "Genetics",
     "ctx": "At the turn of the 20th century, women faced near-total exclusion from research science. The Carnegie Institution, which funded her work, routinely paid female researchers less and promoted male colleagues over them regardless of achievement.",
     "fa": "Discovered sex chromosomes in 1905, demonstrating that biological sex is determined by a specific chromosome pair (XX for female, XY for male) — one of the most fundamental discoveries in genetics. Her male supervisor Edmund Wilson made a similar discovery simultaneously; history initially attributed the finding largely to him."},

    {"n": "Sophie Germain", "co": "France", "yr": "1776-1831",
     "fi": "Mathematics & Physics",
     "ctx": "In Revolutionary-era France, women were completely excluded from the Ecole Polytechnique. Germain could only access mathematical correspondence by using a male pseudonym — 'Monsieur LeBlanc' — to communicate with leading mathematicians including Gauss, who was astonished to discover she was a woman.",
     "fa": "Made fundamental contributions to number theory and elasticity theory. Her work on Fermat's Last Theorem (Sophie Germain's Theorem) was not surpassed for 200 years. Won the Grand Prix of the French Academy of Sciences three times for her work on the vibration of elastic surfaces. Named in the Institut de France for the first time in 1822."},

    # ── Literature & Journalism (additional) ──────────────────────────────────
    {"n": "Virginia Woolf", "co": "United Kingdom", "yr": "1882-1941",
     "fi": "Literature & Feminist Theory",
     "ctx": "Edwardian England offered women no university education (Oxford and Cambridge did not grant women full degrees until after her death), no right to vote until 1918, and a publishing world that treated female authors as a lesser category.",
     "fa": "Author of Mrs Dalloway, To the Lighthouse, and Orlando — foundational texts of literary modernism. Her essay A Room of One's Own (1929) remains the defining statement on women and creative freedom: 'A woman must have money and a room of her own if she is to write fiction.' Pioneered the stream of consciousness technique."},

    {"n": "Harriet Beecher Stowe", "co": "United States", "yr": "1811-1896",
     "fi": "Literature & Abolitionism",
     "ctx": "In 1852, a woman publishing a political novel that directly attacked the institution of slavery was taking a radical social risk. The Fugitive Slave Act had just been passed. Southern states banned the book and offered a reward for Stowe's arrest.",
     "fa": "Author of Uncle Tom's Cabin (1852), the best-selling novel of the 19th century and the best-selling book of the century after the Bible. Brought the reality of slavery to millions of Northern readers who had never witnessed it, galvanising anti-slavery sentiment. When Lincoln met her in 1862, he reportedly said, 'So you're the little woman who wrote the book that started this great war.'"},

    # ── Humanitarianism & Peace ───────────────────────────────────────────────
    {"n": "Jane Addams", "co": "United States", "yr": "1860-1935",
     "fi": "Social Work & Peace Activism",
     "ctx": "In the Gilded Age, middle-class women were expected to stay home. The idea of a woman establishing a community centre for immigrants and the urban poor, and then becoming a national political voice on social reform, labour rights, and peace, was without precedent.",
     "fa": "Co-founded Hull House (1889) in Chicago, one of the most influential social settlement houses in American history, providing services to immigrants and the poor. Co-founded the ACLU. First American woman to win the Nobel Peace Prize (1931) for her advocacy for international peace and social justice."},

    {"n": "Leymah Gbowee", "co": "Liberia", "yr": "1972-",
     "fi": "Peace Activism",
     "ctx": "Liberia in the early 2000s was torn apart by two civil wars and the brutal regime of Charles Taylor. Women had no formal political voice and faced systematic violence. Organising cross-religious and cross-ethnic resistance under such conditions required extraordinary personal courage.",
     "fa": "Led the Women of Liberia Mass Action for Peace movement (2003), bringing together Christian and Muslim women to demand an end to the Second Liberian Civil War. Her movement's non-violent protests — including a 'sex strike' — helped force peace negotiations that ended the war. Nobel Peace Prize (2011)."},

    # ── Exploration ───────────────────────────────────────────────────────────
    {"n": "Junko Tabei", "co": "Japan", "yr": "1939-2016",
     "fi": "Mountaineering",
     "ctx": "In 1970s Japan, the mountaineering establishment considered high-altitude climbing too dangerous for women. Tabei had to form her own women's climbing club because established clubs refused to admit women. Sponsors for her Everest expedition were nearly impossible to find for a women's team.",
     "fa": "First woman to reach the summit of Mount Everest (May 1975). First woman to climb the Seven Summits (the highest peak on each continent). A licensed English teacher, she organised the climb herself despite institutional resistance at every step. Later became an advocate for environmental conservation of mountain ecosystems."},
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
                    if src:
                        return src
            else:
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title)}"
                r = requests.get(url, headers=HEADERS, timeout=10)
                if r.status_code == 200:
                    src = r.json().get("thumbnail", {}).get("source")
                    if src:
                        return src
        except Exception:
            pass
    return None


def main():
    total = len(women)
    found = 0
    for i, s in enumerate(women):
        title = WIKI_EN.get(s["n"], s["n"])
        img = wiki_img(title)
        s["im"] = img
        if img:
            found += 1
        status = "ok" if img else "xx"
        sys.stdout.buffer.write(f"  [{i+1:2}/{total}] {status} {s['n']}\n".encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)
    out = Path("assets/celebrity/pioneer_women.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(women, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    sys.stdout.buffer.write(f"\nDone: {found}/{total} images — {total} women total.\n".encode("utf-8"))


if __name__ == "__main__":
    main()
