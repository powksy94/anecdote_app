import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=invention name, inv=inventor(s) credited (None if anonymous), cc=ISO2 country code(s) of the
# inventor(s) ("/"-joined when several, None if no meaningful country), yr=year (or approximate
# date), fa=fact, wk=Wikipedia article title of the INVENTION, used as the image source and not
# written to the JSON, im=imageUrl (picture of the invention, not a portrait of its inventor)
#
# Content is written in ENGLISH (source language for the app's translation pipeline, see
# content_loader.dart), with no em/en dash as a separator in the fact text.
# Excluded on purpose: accidental discoveries (penicillin, Viagra, X-rays, pacemaker, gunpowder...)
# go to the "Accidental inventions" category; video games belong to the Gaming hub.

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

records = [
    # Antiquity & Middle Ages
    {"n": "Writing", "inv": None, "cc": "IQ", "yr": "c. 3300 BC",
     "wk": "Cuneiform",
     "fa": "The world's first writing wasn't created for poetry or prayer, but for bookkeeping. The oldest tablets from Uruk, in Mesopotamia, are mostly lists tallying grain, livestock and beer. Literature only came along centuries later, once scribes realized the system could record more than inventory."},

    {"n": "The wheel", "inv": None, "cc": None, "yr": "c. 3500 BC",
     "wk": "Wheel",
     "fa": "Humans were farming, brewing and making music long before anyone built a wheel. It may even have spun clay for potters before it ever carried a load. In Mesoamerica, wheels appeared on small animal figurines, yet they were never adopted for transport."},

    {"n": "Paper", "inv": "Cai Lun", "cc": "CN", "yr": "105",
     "wk": "Paper",
     "fa": "Cai Lun, a eunuch at the Han imperial court, presented his papermaking process to the emperor in 105 AD, using tree bark, hemp, old rags and worn-out fishing nets. Archaeologists have since found paper fragments about 250 years older than that, so he likely perfected the process rather than invented it. The first recorded paper mill in Europe only opened in Spain around 1150."},

    {"n": "The magnetic compass", "inv": None, "cc": "CN", "yr": "11th century",
     "wk": "Compass",
     "fa": "The Chinese scholar Shen Kuo gave the first known description of a magnetic needle compass around 1088, and also noticed that the needle doesn't point exactly to true north. Long before guiding ships, Chinese magnetic devices were used for geomancy and divination, and they were traditionally described as pointing south rather than north."},

    {"n": "The number zero", "inv": "Brahmagupta", "cc": "IN", "yr": "628",
     "wk": "Bakhshali manuscript",
     "fa": "In 628, the Indian mathematician Brahmagupta wrote down the first known rules for treating zero as a number in its own right. The idea traveled through the Arab world and reached Europe with Fibonacci in 1202, where it met real resistance: in 1299, Florence's bankers' guild banned Arabic numerals from account books, partly over fears of fraud."},

    {"n": "Porcelain", "inv": None, "cc": "CN", "yr": "c. 7th century",
     "wk": "Porcelain",
     "fa": "China kept the secret of true porcelain for around a thousand years, and Europeans paid fortunes for it. Europe finally cracked the recipe around 1708 in Saxony, with the help of Johann Friedrich Böttger, an alchemist who had been held by King Augustus the Strong after promising to make gold."},

    {"n": "The astronomical clock tower", "inv": "Su Song", "cc": "CN", "yr": "c. 1094",
     "wk": "Su Song",
     "fa": "By 1094, the Chinese polymath Su Song had completed a water-driven clock tower about 12 meters tall in Kaifeng, with an armillary sphere on the roof and mechanical figures announcing the hours. When Jurchen invaders took the city in 1127, the tower was dismantled, and despite later attempts to reassemble it, it was never restored."},

    {"n": "The elephant clock", "inv": "Ismail al-Jazari", "cc": "TR", "yr": "1206",
     "wk": "Elephant clock",
     "fa": "In his 1206 book of mechanical devices, the engineer al-Jazari described a water clock in the shape of an elephant, topped with moving figures, snakes and a dragon. Modern writers often read it as a tribute to the wider world, with an Indian elephant, Chinese dragons, an Egyptian phoenix and Arab figures in one machine."},

    {"n": "Eyeglasses", "inv": None, "cc": "IT", "yr": "c. 1286",
     "wk": "Glasses",
     "fa": "Nobody knows who invented eyeglasses, which appeared in northern Italy around 1286. The best clue comes from a sermon given in Florence in 1306 by the friar Giordano da Pisa, who said it had been less than twenty years since the art of making them was discovered, and that he had met the man who did it. He didn't give the name."},

    {"n": "The windmill", "inv": None, "cc": "IR", "yr": "9th century",
     "wk": "Panemone windmill",
     "fa": "The first clearly documented windmills turned in Sistan, in Persia, by the 9th century, and they looked nothing like the Dutch kind: their sails spun around a vertical axis, like a revolving door. In the Iranian village of Nashtifan, mud-walled mills estimated at up to 1,000 years old stand today, and a handful of them still grind grain."},

    {"n": "The printing press", "inv": "Johannes Gutenberg", "cc": "DE", "yr": "c. 1450",
     "wk": "Printing press",
     "fa": "Gutenberg wasn't the first to print with movable metal type: the Korean Buddhist text Jikji was printed that way in 1377, almost 80 years before his famous Bible. His real breakthrough was a whole system (an oil-based ink, a hand mould to cast letters fast, an adapted press) that made printing cheap. In 1455, his own financier, Johann Fust, sued him for repayment, then went on to run a rival print shop."},

    {"n": "Hangul, the Korean alphabet", "inv": "King Sejong the Great", "cc": "KR", "yr": "1443",
     "wk": "Hangul",
     "fa": "Most writing systems evolved slowly over centuries, but Hangul was designed on purpose. King Sejong created it in 1443 so that ordinary Koreans could read, instead of relying on Chinese characters mastered mostly by the elite. Some court scholars objected, while its 1446 presentation boasted that a wise man could learn it in a morning."},

    # Industry & materials
    {"n": "The steam engine", "inv": "Thomas Newcomen", "cc": "GB", "yr": "1712",
     "wk": "Newcomen atmospheric engine",
     "fa": "James Watt didn't invent the steam engine. Thomas Newcomen, a Devon ironmonger, built the first practical one in 1712 to pump water out of mines, and Watt made it far more efficient decades later. Watt's lasting marketing move was the term \"horsepower\", which told customers exactly how many animals his machine could replace."},

    {"n": "Canned food", "inv": "Nicolas Appert", "cc": "FR", "yr": "1810",
     "wk": "Canning",
     "fa": "The French confectioner Nicolas Appert won a 12,000 franc government prize around 1810 for preserving food by sealing it in glass bottles and boiling them, decades before anyone understood why it worked. Tin cans followed quickly, but the first dedicated can opener didn't arrive until 1858. Until then, soldiers often used bayonets or chisels."},

    {"n": "The Jacquard loom", "inv": "Joseph Marie Jacquard", "cc": "FR", "yr": "1804",
     "wk": "Jacquard machine",
     "fa": "In 1804, the weaver Joseph Marie Jacquard built a loom controlled by chains of punched cards, so that complex patterns could be repeated automatically. It's a direct ancestor of programming: Charles Babbage borrowed the punched card idea for his Analytical Engine, and he owned a silk portrait of Jacquard woven using around 24,000 cards."},

    {"n": "The safety elevator", "inv": "Elisha Otis", "cc": "US", "yr": "1854",
     "wk": "Elevator",
     "fa": "Elevators already existed, but nobody trusted them. At the 1854 New York Crystal Palace exhibition, Elisha Otis stood on a raised platform and ordered the rope cut in front of the crowd. His safety brake caught the platform almost instantly, and the skyscraper became possible."},

    {"n": "Mass-produced steel", "inv": "Henry Bessemer", "cc": "GB", "yr": "1856",
     "wk": "Bessemer process",
     "fa": "Henry Bessemer's converter, which blasted air through molten iron, made steel cheap enough to build railways and bridges. His next idea went far worse: the SS Bessemer, a steamship with a swinging cabin meant to prevent seasickness. It handled so badly that it crashed into the pier at Calais in 1875, and the project was abandoned."},

    {"n": "Reinforced concrete", "inv": "Joseph Monier", "cc": "FR", "yr": "1867",
     "wk": "Reinforced concrete",
     "fa": "The material behind most modern buildings owes its breakthrough to a French gardener who wanted sturdier flowerpots. Others had already tried putting iron in concrete, but Joseph Monier embedded an iron mesh in his planters to stop them from cracking, patented the idea in 1867, then extended it to pipes, tanks and bridges."},

    {"n": "Synthetic ammonia", "inv": "Fritz Haber & Carl Bosch", "cc": "DE", "yr": "1909",
     "wk": "Haber process",
     "fa": "The Haber-Bosch process pulls nitrogen out of the air to make fertilizer, and more than half of the world's population is estimated to depend on the food it makes possible. Fritz Haber won the Nobel Prize for it, yet he also led Germany's chemical weapons program in World War I. His wife Clara Immerwahr, also a chemist, took her own life in 1915."},

    {"n": "Bakelite", "inv": "Leo Baekeland", "cc": "BE/US", "yr": "1907",
     "wk": "Bakelite",
     "fa": "Belgian-born chemist Leo Baekeland had already sold his photographic paper to George Eastman, making him rich enough to work in a home lab. He set out to replace shellac, which came from lac beetle secretions, and instead created the first fully synthetic plastic in 1907. It soon appeared in telephones, radios and electrical parts."},

    {"n": "Air conditioning", "inv": "Willis Carrier", "cc": "US", "yr": "1902",
     "wk": "Air conditioning",
     "fa": "Modern air conditioning was built for paper, not people. In 1902, the young engineer Willis Carrier designed a system for a Brooklyn printing plant where humidity was warping the paper and ruining color alignment. For years it remained an industrial tool, and comfort only came later, when cinemas adopted it."},

    # Energy
    {"n": "The electric battery", "inv": "Alessandro Volta", "cc": "IT", "yr": "1800",
     "wk": "Voltaic pile",
     "fa": "Volta's battery came out of an argument. Luigi Galvani believed frog legs twitched because of a special \"animal electricity\", and Volta set out to prove him wrong. His stack of alternating metal discs produced a steady current with no frog involved, and Napoleon later made him a count."},

    {"n": "The electric motor", "inv": "Michael Faraday", "cc": "GB", "yr": "1821",
     "wk": "Homopolar motor",
     "fa": "The son of a blacksmith, Michael Faraday left school early and became a bookbinder's apprentice, educating himself by reading the books he bound. In 1821, he made a wire rotate continuously around a magnet in a bath of mercury, the first demonstration of electrical energy turned into motion."},

    {"n": "Alternating current", "inv": "Nikola Tesla", "cc": "RS/US", "yr": "1888",
     "wk": "War of the currents",
     "fa": "During the \"war of the currents\", Edison's camp tried to convince the public that Tesla and Westinghouse's alternating current was deadly. The campaign included public electrocutions of animals, and New York's first electric chair, used in 1890, ran on AC. It didn't work: AC powered the Niagara Falls plant in 1895 and still runs the grid today."},

    {"n": "The light bulb", "inv": "Joseph Swan & Thomas Edison", "cc": "GB/US", "yr": "1879",
     "wk": "Incandescent light bulb",
     "fa": "Joseph Swan demonstrated a working incandescent bulb in Newcastle months before Edison's famous October 1879 test. In Britain, Edison ended up having to share the market: their two firms merged in 1883 and sold bulbs under the name \"Ediswan\". London's Savoy Theatre became the first public building lit entirely by electricity in 1881, with Swan's lamps."},

    {"n": "The nuclear reactor", "inv": "Enrico Fermi", "cc": "IT/US", "yr": "1942",
     "wk": "Chicago Pile-1",
     "fa": "The first nuclear chain reaction was achieved on December 2, 1942, in a rackets court under the stands of an unused football stadium at the University of Chicago, right in the middle of the city. The news was passed on in code: \"The Italian navigator has landed in the New World\", a nod to Enrico Fermi."},

    {"n": "The lithium-ion battery", "inv": "John Goodenough, Stanley Whittingham & Akira Yoshino", "cc": "US/GB/JP", "yr": "1985",
     "wk": "Lithium-ion battery",
     "fa": "The battery in your phone took three scientists on three continents' worth of work: Stanley Whittingham at Exxon, John Goodenough at Oxford and Akira Yoshino in Japan. They shared the 2019 Nobel Prize in Chemistry, and Goodenough, then 97, became the oldest Nobel laureate ever."},

    {"n": "The blue LED", "inv": "Isamu Akasaki, Hiroshi Amano & Shuji Nakamura", "cc": "JP", "yr": "1993",
     "wk": "Blue LED",
     "fa": "Red and green LEDs existed for decades, but white LED lighting needed a blue one, and big companies had largely given up. Shuji Nakamura cracked it at a small Japanese chemical firm, which reportedly rewarded him with a 20,000 yen bonus. He sued, and after a court awarded him 20 billion yen, the case settled for about 840 million. He shared the 2014 Nobel Prize in Physics."},

    # Communication
    {"n": "The electric telegraph and Morse code", "inv": "Samuel Morse", "cc": "US", "yr": "1844",
     "wk": "Electrical telegraph",
     "fa": "Before inventing anything, Samuel Morse was a celebrated portrait painter. In 1825, while he was in Washington painting the Marquis de Lafayette, his wife died back home in Connecticut; by the time he got back, she had already been buried. His first official telegraph message, sent from Washington to Baltimore in 1844, read: \"What hath God wrought\"."},

    {"n": "The transatlantic cable", "inv": "Cyrus Field", "cc": "US", "yr": "1858",
     "wk": "Transatlantic telegraph cable",
     "fa": "The first transatlantic telegraph cable opened in 1858 to huge celebrations, but Queen Victoria's 98-word greeting to President Buchanan took about 16 hours to get through. Within weeks, the cable was dead, damaged in part by the excessive voltage used to push signals through it. A lasting connection only came in 1866."},

    {"n": "The telephone", "inv": "Alexander Graham Bell", "cc": "GB/US", "yr": "1876",
     "wk": "Telephone",
     "fa": "On February 14, 1876, Bell's patent application and a filing by rival inventor Elisha Gray for a very similar device reached the U.S. Patent Office on the same day. Bell got the patent. In 2002, the U.S. House of Representatives passed a resolution honoring Antonio Meucci, an Italian immigrant who had worked on a talking telegraph years earlier but couldn't afford to keep renewing his patent notice."},

    {"n": "Radio", "inv": "Guglielmo Marconi", "cc": "IT", "yr": "1901",
     "wk": "Invention of radio",
     "fa": "In December 1901, Guglielmo Marconi reported receiving the Morse letter S across the Atlantic, and he went on to share the 1909 Nobel Prize in Physics. In 1912, wireless distress calls brought rescuers to the Titanic's survivors. Yet in 1943, the U.S. Supreme Court invalidated key parts of his patent, citing earlier work by other inventors."},

    {"n": "Electronic television", "inv": "Philo Farnsworth", "cc": "US", "yr": "1927",
     "wk": "Video camera tube",
     "fa": "By his own account, Philo Farnsworth got the idea at 14 while working a field in Idaho: the parallel rows suggested a way to scan an image line by line. At 21, he transmitted the first fully electronic television image in San Francisco, in 1927. He then spent years fighting the giant RCA over patents, and won."},

    {"n": "Color television", "inv": "Guillermo González Camarena", "cc": "MX", "yr": "1940",
     "wk": "Guillermo González Camarena",
     "fa": "In 1940, at just 23, the Mexican engineer Guillermo González Camarena applied for a patent on a color television system that used a spinning filter of red, green and blue. The U.S. granted it in 1942. His method never became the American standard, but it shows that color TV wasn't only a story of big U.S. labs."},

    {"n": "ARPANET, the Internet's ancestor", "inv": "Leonard Kleinrock", "cc": "US", "yr": "1969",
     "wk": "ARPANET",
     "fa": "The first message ever sent over the network that became the Internet was supposed to be \"LOGIN\". On October 29, 1969, a UCLA student started typing to a computer at Stanford, and the system crashed after two letters. So the Internet's first word was, by accident, \"LO\"."},

    {"n": "Fiber optics", "inv": "Charles Kao", "cc": "CN/GB/US", "yr": "1966",
     "wk": "Optical fiber",
     "fa": "In 1966, Charles Kao argued that light could carry data across long distances through glass fibers, provided the glass was made far purer than anyone had managed. Many engineers doubted him. Corning made the low-loss fiber in 1970, and Kao received the Nobel Prize in Physics in 2009."},

    {"n": "The mobile phone", "inv": "Martin Cooper", "cc": "US", "yr": "1973",
     "wk": "Motorola DynaTAC",
     "fa": "On April 3, 1973, Motorola engineer Martin Cooper stood on a New York street and made the first public handheld cellular call. He rang Joel Engel, his rival at Bell Labs, to tell him he was calling from a portable phone. The prototype weighed about 1.1 kg, and its battery lasted only about 20 minutes."},

    {"n": "The World Wide Web", "inv": "Tim Berners-Lee", "cc": "GB", "yr": "1989",
     "wk": "World Wide Web",
     "fa": "When Tim Berners-Lee handed his proposal for an information management system to his boss at CERN in March 1989, Mike Sendall scribbled three words on the cover: \"Vague but exciting\". On April 30, 1993, CERN put the Web's software in the public domain, letting anyone build on it without paying a single royalty."},

    {"n": "Mobile money", "inv": "Safaricom & Vodafone (M-Pesa)", "cc": "KE", "yr": "2007",
     "wk": "M-Pesa",
     "fa": "M-Pesa started out as a way for Kenyans to repay microloans by phone. After the pilot, it was broadened into a general money transfer service and launched in March 2007. Kenya, not Silicon Valley, ended up showing the world that a basic mobile phone could work as a bank account."},

    # Transport
    {"n": "The hot air balloon", "inv": "Joseph-Michel & Jacques-Étienne Montgolfier", "cc": "FR", "yr": "1783",
     "wk": "Hot air balloon",
     "fa": "The first passengers in human history to fly in a man-made craft weren't people. In September 1783, at Versailles, in front of Louis XVI, the Montgolfier brothers, paper manufacturers by trade, sent up a sheep, a duck and a rooster. All three landed safely, and two months later humans made the trip."},

    {"n": "The railway locomotive", "inv": "Richard Trevithick", "cc": "GB", "yr": "1804",
     "wk": "Steam locomotive",
     "fa": "The first steam locomotive to run on rails got started because of a bet. In 1804, ironmaster Samuel Homfray wagered 500 guineas that Richard Trevithick's engine could haul ten tons of iron along the Penydarren tramway, and it did. Trevithick died penniless in 1833, and colleagues paid for his funeral."},

    {"n": "The bicycle", "inv": "Karl von Drais", "cc": "DE", "yr": "1817",
     "wk": "Dandy horse",
     "fa": "The ancestor of the bicycle had no pedals. On June 12, 1817, in Mannheim, the German baron Karl von Drais showed off his wooden \"running machine\", a two-wheeler that riders pushed along with their feet. The press soon named it the \"draisine\" after him, and pedals only arrived decades later."},

    {"n": "The automobile", "inv": "Carl Benz", "cc": "DE", "yr": "1886",
     "wk": "Benz Patent-Motorwagen",
     "fa": "Carl Benz patented the first true automobile in 1886, but his wife Bertha is the one who proved it worked. In 1888, she took it without telling him and drove with their two sons roughly 100 km to Pforzheim, the first long-distance car trip. She bought fuel at a pharmacy in Wiesloch, often described as the world's first filling station."},

    {"n": "The submarine", "inv": "Cornelis Drebbel", "cc": "NL/GB", "yr": "1620",
     "wk": "Cornelis Drebbel",
     "fa": "The first navigable submarine traveled along the River Thames around 1620, built by Dutch inventor Cornelis Drebbel, with King James I of England among the spectators. It was essentially a greased leather-covered rowing boat, powered by oarsmen. Reports of the demonstration still leave historians wondering how the crew managed to breathe."},

    {"n": "The diesel engine", "inv": "Rudolf Diesel", "cc": "DE", "yr": "1897",
     "wk": "Diesel engine",
     "fa": "Rudolf Diesel boarded the steamer Dresden at Antwerp on September 29, 1913, bound for England, and was never seen alive again. About ten days later, a Dutch crew found a badly decomposed body at sea, kept the personal items and returned the body to the water. Suicide, accident and murder have all been suggested, and the mystery remains unsolved."},

    {"n": "The helicopter", "inv": "Paul Cornu & Igor Sikorsky", "cc": "FR/US", "yr": "1907",
     "wk": "Helicopter",
     "fa": "In 1907, the French bicycle maker Paul Cornu lifted off in a rotor craft for about 20 seconds, barely off the ground. Three decades later, Igor Sikorsky's VS-300 established the design used today, with one main rotor and a small tail rotor."},

    {"n": "The airplane", "inv": "Orville & Wilbur Wright", "cc": "US", "yr": "1903",
     "wk": "Wright Flyer",
     "fa": "The first powered airplane flight, on December 17, 1903, lasted 12 seconds and covered about 36 meters, less than the wingspan of a Boeing 747. The Wright brothers, bicycle makers, tossed a coin to see who would fly first: Wilbur won, but his attempt failed, so the honor went to Orville three days later. In 1969, Neil Armstrong carried a piece of their Flyer's fabric to the Moon."},

    {"n": "The jet engine", "inv": "Frank Whittle & Hans von Ohain", "cc": "GB/DE", "yr": "1939",
     "wk": "Jet engine",
     "fa": "Two men invented the jet engine independently, on opposite sides of a coming war. Frank Whittle, an RAF officer, patented it in 1930 but let the patent lapse in 1935 because he couldn't afford the £5 renewal fee. Germany's Hans von Ohain flew first, in August 1939, while Britain's first jet only took off in 1941."},

    {"n": "The shipping container", "inv": "Malcom McLean", "cc": "US", "yr": "1956",
     "wk": "Intermodal container",
     "fa": "A trucking boss tired of waiting at the docks may have done more for globalization than any treaty. In 1956, Malcom McLean loaded 58 metal boxes onto the Ideal X in Newark. Loading loose cargo then cost about $5.83 a ton, and his method cut it to around 16 cents."},

    {"n": "The bullet train", "inv": "Hideo Shima", "cc": "JP", "yr": "1964",
     "wk": "Shinkansen",
     "fa": "Japan's Shinkansen opened in October 1964, just days before the Tokyo Olympics, and has never had a passenger death from a derailment or collision. A later model solved its tunnel noise problem thanks to a birdwatching engineer: Eiji Nakatsu reshaped the train's nose after the beak of the kingfisher."},

    {"n": "GPS", "inv": "Bradford Parkinson, Ivan Getting & Roger Easton", "cc": "US", "yr": "1978",
     "wk": "Global Positioning System",
     "fa": "GPS was built as a U.S. military system. It was opened to civilians after Korean Air Lines Flight 007 strayed into Soviet airspace and was shot down in 1983, killing all 269 people aboard. Until May 2000, the signal available to civilians was deliberately degraded, an option President Clinton then switched off."},

    # Medicine
    {"n": "The vaccine", "inv": "Edward Jenner", "cc": "GB", "yr": "1796",
     "wk": "Smallpox vaccine",
     "fa": "In 1796, Edward Jenner inoculated 8-year-old James Phipps with cowpox taken from a milkmaid's hand, then exposed him to smallpox, and the boy never fell ill. The word \"vaccine\" comes from the Latin \"vacca\", meaning cow. The hide of Blossom, the cow behind that first sample, still hangs in the library of St George's medical school in London."},

    {"n": "General anesthesia", "inv": "Hanaoka Seishū & William Morton", "cc": "JP/US", "yr": "1804",
     "wk": "Anesthesia",
     "fa": "The West celebrates October 16, 1846, when William Morton demonstrated ether in Boston, as the birth of anesthesia. But in 1804, Japanese surgeon Hanaoka Seishū had already removed a breast tumor from a patient under general anesthesia, using a herbal mix. Japan's isolation kept the achievement almost unknown abroad."},

    {"n": "The stethoscope", "inv": "René Laennec", "cc": "FR", "yr": "1816",
     "wk": "Stethoscope",
     "fa": "The stethoscope was born of embarrassment. In 1816, the French doctor René Laennec needed to listen to a young woman's heart but felt it improper to press his ear to her chest. He rolled a sheet of paper into a tube and found that it made her heartbeat clearer than ever."},

    {"n": "Handwashing in medicine", "inv": "Ignaz Semmelweis", "cc": "HU", "yr": "1847",
     "wk": "Hand washing",
     "fa": "In 1847, Hungarian doctor Ignaz Semmelweis saw that women in his Vienna maternity ward were dying far more often when treated by doctors coming straight from autopsies. Handwashing cut the death rate dramatically, yet many colleagues took the idea as an insult. He died in an asylum in 1865, before germ theory proved him right."},

    {"n": "The newborn incubator", "inv": "Stéphane Tarnier", "cc": "FR", "yr": "1880",
     "wk": "Neonatal intensive care unit",
     "fa": "The French obstetrician Stéphane Tarnier got the idea for a baby incubator from chicken incubators at the Paris zoo. Hospitals were slow to adopt it, so for decades Martin Couney kept premature babies alive in sideshow exhibits, notably at Coney Island, financing their care with visitors' tickets."},

    {"n": "The electrocardiograph", "inv": "Willem Einthoven", "cc": "NL", "yr": "1903",
     "wk": "String galvanometer",
     "fa": "The first practical electrocardiograph, built by Dutch physiologist Willem Einthoven in 1903, weighed about 270 kg, needed five people to operate, and had patients sit with their limbs in buckets of salt water. Everyday cardiology owes its terms P, Q, R, S and T to him, and it earned him the 1924 Nobel Prize."},

    {"n": "The dialysis machine", "inv": "Willem Kolff", "cc": "NL", "yr": "1943",
     "wk": "Hemodialysis",
     "fa": "Willem Kolff built the first artificial kidney in the Nazi-occupied Netherlands, using sausage casing, orange juice cans and parts from a washing machine. His early patients all died. His first success, in 1945, was a 67-year-old woman jailed for collaborating with the Nazis, who came out of a coma and survived."},

    {"n": "The MRI scanner", "inv": "Paul Lauterbur & Peter Mansfield", "cc": "US/GB", "yr": "1973",
     "wk": "Magnetic resonance imaging",
     "fa": "Paul Lauterbur reportedly came up with the key idea of MRI in 1971 while eating at a Big Boy restaurant, scribbling it on a napkin. He and Peter Mansfield won the 2003 Nobel Prize, prompting rival Raymond Damadian to take out full-page newspaper ads protesting his exclusion."},

    # Image & sound
    {"n": "Photography", "inv": "Nicéphore Niépce", "cc": "FR", "yr": "c. 1826",
     "wk": "View from the Window at Le Gras",
     "fa": "The oldest surviving camera photograph, taken by Nicéphore Niépce from a window of his house in Burgundy, needed an exposure of at least eight hours, possibly several days. His partner Louis Daguerre got most of the fame after Niépce's death. In 1839, the French state bought the process and declared it free to the world, except in Britain, where Daguerre's agent had quietly filed a patent days earlier."},

    {"n": "Sound recording", "inv": "Édouard-Léon Scott de Martinville", "cc": "FR", "yr": "1860",
     "wk": "Phonautograph",
     "fa": "Edison is credited with the first device to play sound back, in 1877. But seventeen years earlier, the Parisian printer Scott de Martinville recorded a voice singing \"Au clair de la lune\" as a line on soot-blackened paper. He never meant it to be heard: it was only played back in 2008, by American researchers using computers."},

    {"n": "Magnetic recording", "inv": "Valdemar Poulsen", "cc": "DK", "yr": "1898",
     "wk": "Telegraphone",
     "fa": "Danish engineer Valdemar Poulsen patented the first magnetic recorder in 1898, storing sound on steel wire. His telegraphone won a Grand Prix at the 1900 Paris Exposition, where it is said to have recorded the voice of Emperor Franz Joseph. Every tape deck and hard drive descends from that wire."},

    {"n": "Cinema", "inv": "Auguste & Louis Lumière", "cc": "FR", "yr": "1895",
     "wk": "Cinématographe",
     "fa": "The Lumière brothers held their first paid public screening on December 28, 1895, in the basement of a Paris café. Only a few dozen spectators reportedly attended. The famous story of terrified viewers fleeing from a film of an arriving train is most likely a legend."},

    {"n": "The digital camera", "inv": "Steven Sasson", "cc": "US", "yr": "1975",
     "wk": "Digital camera",
     "fa": "The first digital camera was built in 1975 at Kodak, by a young engineer named Steven Sasson. It weighed about 3.6 kg, captured 0.01 megapixels in black and white, and took 23 seconds to record an image. Kodak's management didn't rush to promote it, and the company filed for bankruptcy in 2012."},

    # Computing
    {"n": "The Analytical Engine", "inv": "Charles Babbage", "cc": "GB", "yr": "1837",
     "wk": "Analytical engine",
     "fa": "Charles Babbage designed a programmable mechanical computer in the 1830s, with a memory and a processing unit, but never built it. In 1991, London's Science Museum finished his earlier Difference Engine No. 2 from his original plans, using only tolerances achievable in his time. It worked, calculating to 31 digits."},

    {"n": "ENIAC, the electronic computer", "inv": "John Mauchly & J. Presper Eckert", "cc": "US", "yr": "1945",
     "wk": "ENIAC",
     "fa": "ENIAC weighed about 30 tons and filled a large room. It was programmed by six women, including Kay McNulty and Betty Snyder, who taught themselves from its diagrams, with no manual. They wrote the program shown at the 1946 public unveiling, yet they were never introduced, and only the men were named in the photo captions."},

    {"n": "The transistor", "inv": "John Bardeen, Walter Brattain & William Shockley", "cc": "US", "yr": "1947",
     "wk": "Transistor",
     "fa": "Bardeen and Brattain built the first working transistor at Bell Labs in December 1947, and their boss, William Shockley, was left off the patent, so he worked on his own to design a better one. All three shared the 1956 Nobel Prize. Shockley's abrasive management later drove eight of his engineers to leave and help create Silicon Valley."},

    {"n": "The perceptron, ancestor of AI", "inv": "Frank Rosenblatt", "cc": "US", "yr": "1958",
     "wk": "Mark I Perceptron",
     "fa": "In 1958, psychologist Frank Rosenblatt presented a machine that could learn to recognize patterns, and the press reported that the U.S. Navy expected such machines to walk, talk and see. Enthusiasm crashed after a critical 1969 book, and Rosenblatt died in a boating accident in 1971, on his 43rd birthday. The neural networks behind today's AI descend from his idea."},

    {"n": "The integrated circuit", "inv": "Jack Kilby & Robert Noyce", "cc": "US", "yr": "1958",
     "wk": "Integrated circuit",
     "fa": "In the summer of 1958, Jack Kilby had just joined Texas Instruments and had no vacation time, so he spent the company's holiday shutdown alone in the lab, working out the first integrated circuit. Robert Noyce independently reached a better design months later. Kilby received the 2000 Nobel Prize; Noyce had died in 1990 and could not share it."},

    {"n": "The microprocessor", "inv": "Federico Faggin, Ted Hoff, Stanley Mazor & Masatoshi Shima", "cc": "IT/US/JP", "yr": "1971",
     "wk": "Intel 4004",
     "fa": "The world's first commercial microprocessor, the Intel 4004, was ordered by a Japanese company, Busicom, for a calculator. Designer Federico Faggin signed his initials, F.F., on the silicon. Busicom held the exclusive rights, until Intel won them back in 1971 by returning its $60,000 investment, one of the best deals in tech history."},
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
    total = len(records)
    found = 0
    for i, s in enumerate(records):
        title = s.pop("wk")
        img = wiki_img(title)
        s["im"] = img
        if img:
            found += 1
        status = "ok" if img else "xx"
        sys.stdout.buffer.write((f"  [{i+1:2}/{total}] {status} {title}" + chr(10)).encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)

    out = Path("assets/tech/great_inventions.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(records, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    sys.stdout.buffer.write((chr(10) + f"Done: {found}/{total} images found." + chr(10)).encode("utf-8"))


if __name__ == "__main__":
    main()
