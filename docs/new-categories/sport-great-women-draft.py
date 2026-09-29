# FINAL: Great Sportswomen (replaces "Pioneers & Firsts" on the Athletes side of Sport hub)
# 66 entries, locked 2026-09-29. Content written in ENGLISH (see lesson in TECH_PLAN.md:
# runtime translation pipeline requires English source, French caused Google Translate garbling).
# Structure: n=name, sp=sport, cc=ISO2 country code, yr=LIFESPAN (birth-death, not achievement year;
# matches existing pioneerWoman convention), ctx=era/social context, fa=achievement/impact (no em-dash).
# Each entry verified via web search on 2026-09-29, not just model memory. No overlap with the
# existing legendaryAthlete (59) or sportRecord (91) entries. 26 countries represented, US ~48%.
# Next step: tools/sport/generate_sport_great_women.py + Dart data/service/ContentType wiring,
# following the exact pattern used for sportRecord.

records = [
    # Batch 1 (verified 2026-09-29)
    {"n": "Kathrine Switzer", "sp": "Running (marathon)", "cc": "US", "yr": "1947-",
     "ctx": "In the 1960s, women were widely believed to be physically incapable of running long distances, and the Boston Marathon formally barred female entrants.",
     "fa": "She registered under the gender-neutral name \"K.V. Switzer\" and ran with an official bib number in 1967. A race official spotted her mid-race and tried to physically tear her number off, but her boyfriend blocked him and she finished. Women weren't officially allowed to enter Boston until five years later."},

    {"n": "Junko Tabei", "sp": "Mountaineering", "cc": "JP", "yr": "1939-2016",
     "ctx": "In 1970s Japan, mountaineering was seen as a male domain; sponsors reportedly told her she should be raising children instead of climbing mountains.",
     "fa": "She reached the summit of Everest on May 16, 1975, days after an avalanche buried her team's camp and injured her. She later became the first woman to complete the Seven Summits, the highest peak on every continent."},

    {"n": "Toni Stone", "sp": "Baseball", "cc": "US", "yr": "1921-1996",
     "ctx": "In the segregated, all-male world of 1950s Negro League baseball, a woman taking an infield position was almost unthinkable, and she faced open hostility from teammates.",
     "fa": "In 1953 she became the first woman to play as a regular for a men's professional baseball team, the Indianapolis Clowns, taking the second base job vacated by Hank Aaron. She once got a hit off Hall of Famer Satchel Paige."},

    {"n": "Manon Rhéaume", "sp": "Ice hockey", "cc": "CA", "yr": "1972-",
     "ctx": "No woman had ever appeared on an NHL roster, and her signing was widely dismissed by observers as a publicity stunt rather than a genuine hockey move.",
     "fa": "On September 23, 1992, she started in goal for the Tampa Bay Lightning in a preseason exhibition game, becoming the first woman to play in an NHL game. She stopped 7 of 9 shots before being pulled after one period."},

    {"n": "Nawal El Moutawakel", "sp": "Athletics (400m hurdles)", "cc": "MA", "yr": "1962-",
     "ctx": "She was the only woman on Morocco's Olympic team that year, competing in an event making its very first Olympic appearance for women.",
     "fa": "Her win at the 1984 Los Angeles Games made her the first woman from an Arab or Muslim-majority country to win Olympic gold. The King of Morocco declared her birthday a national holiday for all girls born that day."},

    {"n": "Ibtihaj Muhammad", "sp": "Fencing", "cc": "US", "yr": "1985-",
     "ctx": "She competed amid rising public debate over Muslim identity in the United States, having modified her own uniforms as a teenager since no hijab-friendly sportswear existed.",
     "fa": "At the 2016 Rio Olympics she became the first American Olympian to compete wearing a hijab, winning bronze in the team sabre event as the first Muslim American woman to win an Olympic medal."},

    {"n": "Suzanne Lenglen", "sp": "Tennis", "cc": "FR", "yr": "1899-1938",
     "ctx": "Edwardian-era women's tennis was played in corsets and full-length skirts that severely restricted movement; showing an ankle on court was considered improper.",
     "fa": "At Wimbledon in 1919 she played in a calf-length pleated skirt with no corset, an outfit the press called \"indecent.\" Her aggressive style and six Wimbledon singles titles permanently changed how women's tennis was played and worn."},

    {"n": "Alice Coachman", "sp": "Athletics (high jump)", "cc": "US", "yr": "1923-2014",
     "ctx": "Growing up in the segregated American South, she was barred from formal athletics facilities and reportedly trained jumping barefoot over ropes and sticks in open fields.",
     "fa": "At the 1948 London Olympics she became the first Black woman ever to win an Olympic gold medal, clearing the bar on her very first attempt. She was also the only American woman to win gold at those Games."},

    {"n": "Gertrude Ederle", "sp": "Swimming", "cc": "US", "yr": "1905-2003",
     "ctx": "Many doctors of the era considered the English Channel crossing to be beyond women's physical capability, following several failed attempts by female swimmers.",
     "fa": "On August 6, 1926 she swam from France to England in 14 hours 34 minutes, becoming the first woman to cross the Channel and beating the existing men's record by nearly two hours."},

    {"n": "Annie Londonderry", "sp": "Cycling", "cc": "US", "yr": "1870-1947",
     "ctx": "In 1890s America, women cycling alone in public, let alone wearing practical clothing instead of long skirts, was considered scandalous and a threat to feminine respectability.",
     "fa": "A 24-year-old mother of three, she left Boston in June 1894 to cycle around the world, funding the 15-month journey through sponsorships and paid appearances, and returned having crossed Europe, the Middle East, and Asia."},

    # Batch 2 (verified 2026-09-29)
    {"n": "Bobbi Gibb", "sp": "Running (marathon)", "cc": "US", "yr": "1942-",
     "ctx": "A year before Kathrine Switzer's officially-numbered run, the Boston Marathon's race director had publicly declared women \"not physiologically able\" to run the distance and barred them outright.",
     "fa": "She hid in the bushes near the start line on April 19, 1966, wearing her brother's shorts and a hooded sweatshirt to conceal her identity, then slipped into the field. She finished in 3:21:40, ahead of two-thirds of the men who started, becoming the first woman to complete the Boston Marathon."},

    {"n": "Charlotte Cooper", "sp": "Tennis", "cc": "GB", "yr": "1870-1966",
     "ctx": "The 1900 Paris Games were the first Olympics ever to allow women to compete, in a small handful of sports considered genteel enough for ladies, such as tennis and golf.",
     "fa": "She won the women's singles tennis title on July 11, 1900, becoming the first individual female Olympic champion in history. She went on to win five Wimbledon singles titles, the last at age 37, still the oldest Wimbledon women's singles champion ever."},

    {"n": "Shirley Muldowney", "sp": "Drag racing", "cc": "US", "yr": "1940-",
     "ctx": "Drag racing in the 1960s and 70s was considered exclusively a man's sport, and she was repeatedly told a 300+ mph Top Fuel dragster was no place for a woman.",
     "fa": "She became the first woman licensed by the NHRA to drive a Top Fuel dragster. In 1977 she won her first NHRA Top Fuel championship, and went on to become the first person, male or female, to win the title three times."},

    {"n": "Janet Guthrie", "sp": "Motorsport (IndyCar/NASCAR)", "cc": "US", "yr": "1938-",
     "ctx": "American motorsport's biggest races had never had a female driver on the grid, and Guthrie, a trained aerospace engineer, had to fight for sponsorship that male drivers with similar credentials received easily.",
     "fa": "In 1977 she became the first woman to qualify for and compete in both the Indianapolis 500 and the Daytona 500 in the same year, opening the door for every woman who has raced at Indy since."},

    {"n": "Wyomia Tyus", "sp": "Athletics (sprint)", "cc": "US", "yr": "1945-",
     "ctx": "She achieved her feat during the height of the US civil rights movement, and later became one of the first female athletes to have a professional sponsorship contract in her own name, at a time when almost no money existed for women's sports.",
     "fa": "At the 1968 Mexico City Olympics she defended her 100m title from 1964, becoming the first person, man or woman, to win consecutive Olympic gold medals in the event, setting a world record of 11.08 seconds."},

    {"n": "Keiko Fukuda", "sp": "Judo", "cc": "JP", "yr": "1913-2013",
     "ctx": "For decades the Kodokan, judo's governing institute in Japan, capped women's ranks at 5th dan regardless of skill or seniority, reflecting the sport's male-only competitive structure.",
     "fa": "In 1972 she became one of the first two women ever promoted to 6th dan by the Kodokan. In 2006, at age 98, she reached 9th dan, and in 2011 she was awarded 10th dan by American judo federations, the highest rank any woman had ever held in the sport."},

    {"n": "Hassiba Boulmerka", "sp": "Athletics (middle distance)", "cc": "DZ", "yr": "1968-",
     "ctx": "Competing during a surge of Islamist militancy in Algeria, she was spat on and had stones thrown at her while training on public roads, and was denounced at her local mosque for running in shorts.",
     "fa": "She won the 1500m at the 1991 World Championships in Tokyo, becoming the first African woman to win a world title in any sport, and went on to win Olympic gold in Barcelona the following year."},

    {"n": "Annika Sörenstam", "sp": "Golf", "cc": "SE", "yr": "1970-",
     "ctx": "No woman had played in a PGA Tour event in 58 years, since Babe Zaharias made the cut at the 1945 Los Angeles Open, and several male players publicly questioned whether she belonged in the field.",
     "fa": "In May 2003 she teed off at the Bank of America Colonial in Texas, becoming the first woman in 58 years to compete on the PGA Tour. She missed the cut by four strokes but earned praise even from skeptical rivals for her composure under intense media scrutiny."},

    # Batch 3 (verified 2026-09-29)
    {"n": "Sonja Henie", "sp": "Figure skating", "cc": "NO", "yr": "1912-1969",
     "ctx": "Figure skating in the 1920s was skated in long, heavy skirts with rigid, formal choreography; jumps and freer movement were considered unladylike and impractical for women.",
     "fa": "She won three consecutive Olympic gold medals (1928, 1932, 1936) and ten consecutive world titles, shortening her skirts above the knee to allow for jumps and spins, a move that shocked audiences but became the new standard for women's figure skating within a few years."},

    {"n": "Ronda Rousey", "sp": "Mixed martial arts", "cc": "US", "yr": "1987-",
     "ctx": "The UFC's president had publicly stated for years that women would \"never\" fight in the organization, believing there wasn't a deep enough pool of credible female fighters to build weight divisions around.",
     "fa": "In November 2012 she became the first woman signed to a UFC contract and was named the promotion's first women's bantamweight champion, a move that led directly to the creation of the UFC's first women's divisions."},

    {"n": "Se Ri Pak", "sp": "Golf", "cc": "KR", "yr": "1977-",
     "ctx": "In 1998 she was the only South Korean player on the LPGA Tour, competing during the Asian financial crisis, a period of severe economic hardship back home that left the country hungry for a source of national pride.",
     "fa": "At age 20, in only her rookie season, she won the U.S. Women's Open after an 18-hole playoff, becoming the tournament's youngest-ever champion. Her win inspired a generation of young Korean girls, nicknamed \"Se Ri's Kids,\" who went on to dominate the LPGA Tour."},

    {"n": "Lusia Harris", "sp": "Basketball", "cc": "US", "yr": "1955-2022",
     "ctx": "Women's professional basketball leagues barely existed in the US at the time, and being drafted by an NBA team was purely symbolic since no woman had ever been given a real chance to make an NBA roster.",
     "fa": "On June 10, 1977 she was selected 137th overall by the New Orleans Jazz, becoming the only woman ever officially drafted by an NBA team. She never attended training camp, having just given birth, but remains the sole woman in NBA draft history."},

    # Batch 4 (verified 2026-09-29)
    {"n": "Diana Nyad", "sp": "Swimming", "cc": "US", "yr": "1949-",
     "ctx": "She first attempted the 110-mile crossing in 1978 at age 28; by the time she finally succeeded decades later, popular opinion held that endurance swimming through shark-infested open water was a young person's pursuit.",
     "fa": "On September 2, 2013, at age 64, she completed the swim from Havana to Key West in 52 hours 54 minutes without a shark cage, becoming the first person, of any gender, to make the crossing unprotected, after four failed attempts spanning 35 years."},

    {"n": "Amanda Nunes", "sp": "Mixed martial arts", "cc": "BR", "yr": "1988-",
     "ctx": "Before her, only two fighters in UFC history, both men, had ever held titles in two weight divisions at the same time, and many doubted a woman could physically campaign across categories at the top level.",
     "fa": "With a 51-second knockout of Cris Cyborg at UFC 232 in December 2018, she became the first woman to hold UFC titles in two divisions simultaneously, and the only fighter in UFC history, male or female, to actively defend both belts at once."},

    {"n": "P. T. Usha", "sp": "Athletics (hurdles)", "cc": "IN", "yr": "1964-",
     "ctx": "Indian women's athletics had almost no international profile before her, and she trained on unpaved tracks in rural Kerala with minimal funding or facilities.",
     "fa": "At the 1984 Los Angeles Olympics she finished fourth in the 400m hurdles, missing bronze by just one hundredth of a second, still the closest any Indian athlete has come to an individual Olympic medal in track and field. Her performance helped turn athletics into a mainstream sport for girls across India."},

    {"n": "Fu Mingxia", "sp": "Diving", "cc": "CN", "yr": "1978-",
     "ctx": "She began intensive diving training at age 6, spending hours a day drilling dives in a state sports academy system built to identify and develop Olympic talent as early as possible.",
     "fa": "At the 1992 Barcelona Olympics she won platform diving gold at just 13 years old, the youngest Olympic diving champion in history. FINA subsequently raised the minimum competing age to 14, making her record permanent."},

    # Batch 5 (verified 2026-09-29)
    {"n": "Maria Bueno", "sp": "Tennis", "cc": "BR", "yr": "1939-2018",
     "ctx": "Brazilian tennis in the 1950s had produced no significant international champions, and she grew up practicing on public courts in São Paulo with no conventional pathway to the professional game.",
     "fa": "In 1959 she won both Wimbledon and the US National Championships, becoming the first South American, male or female, to win a Grand Slam singles title. She went on to win 19 Grand Slam titles in total and became a national symbol of Brazil's modernization."},

    {"n": "Sarah Thomas", "sp": "American football (officiating)", "cc": "US", "yr": "1979-",
     "ctx": "No woman had ever officiated an NFL game in the league's 95-year history when she was hired, and she had spent nearly two decades working her way up through youth, college, and Conference USA games to prove herself.",
     "fa": "She was hired as the NFL's first full-time female official in 2015, debuting that September. In 2021 she became the first woman to officiate a Super Bowl, capping a career that began with peewee football games in 1996."},

    {"n": "Wojdan Shaherkani", "sp": "Judo", "cc": "SA", "yr": "1994-",
     "ctx": "Saudi Arabia had never sent a female athlete to the Olympics and enforced a strict ban on women's sport; her participation only happened after intense IOC pressure and required special permission to wear a modified hijab in competition.",
     "fa": "At the 2012 London Olympics, aged 16, she became the first woman ever to compete for Saudi Arabia at the Olympic Games, in a judo match that lasted just 82 seconds. Her appearance meant that for the first time in Olympic history, every single competing nation had sent at least one female athlete."},

    {"n": "Zhang Shan", "sp": "Shooting", "cc": "CN", "yr": "1968-",
     "ctx": "Olympic skeet shooting in 1992 was still an open, mixed-gender event, one of the last in any sport where women competed directly against men rather than in a separate category.",
     "fa": "At the Barcelona Games she hit 223 targets to win gold, beating every male competitor in the field. The event was subsequently split into separate men's and women's competitions, meaning she remains the only woman in history to win an Olympic shooting title against men."},

    # Batch 6 (verified 2026-09-29)
    {"n": "Simone Manuel", "sp": "Swimming", "cc": "US", "yr": "1996-",
     "ctx": "Competitive swimming in the US has historically had very low participation among Black athletes, partly due to a long history of segregated public pools and unequal access to swimming lessons.",
     "fa": "At the Rio 2016 Olympics she tied for gold in the 100m freestyle, becoming the first Black woman to win an individual Olympic swimming gold medal. She finished the Games with four medals total and said she hoped her win would help diversify the sport."},

    {"n": "Alice Milliat", "sp": "Athletics (administration)", "cc": "FR", "yr": "1884-1957",
     "ctx": "In the early 1920s the IOC and the international athletics federation refused outright to let women compete in Olympic track and field events, considering the sport unsuitable and unfeminine.",
     "fa": "When her request was denied, she organized a rival competition, the Women's World Games, first held in Paris in 1922 and drawing 20,000 spectators. The pressure it created forced the IOC to finally add women's track and field events to the 1928 Olympics."},

    {"n": "Yusra Mardini", "sp": "Swimming", "cc": "SY", "yr": "1998-",
     "ctx": "She fled the Syrian civil war in 2015 at age 17, attempting the sea crossing from Turkey to Greece that thousands of refugees were making at the height of the European migrant crisis.",
     "fa": "When the motor on her overcrowded boat failed mid-crossing, she and her sister jumped into the open water and swam alongside it for three hours, helping guide it to shore and saving the roughly 20 people aboard. The following year she competed for the first-ever Refugee Olympic Team at Rio 2016."},

    {"n": "Kim Ng", "sp": "Baseball (administration)", "cc": "US", "yr": "1968-",
     "ctx": "She interviewed for at least five MLB general manager openings over 15 years without being hired, watching less experienced male candidates repeatedly land the jobs she was passed over for.",
     "fa": "In November 2020 the Miami Marlins named her general manager, making her the first woman ever to lead the front office of a major North American men's professional sports team."},

    # Batch 7 (verified 2026-09-29)
    {"n": "Betty Robinson", "sp": "Athletics (sprint)", "cc": "US", "yr": "1911-1999",
     "ctx": "1928 marked the very first time women were allowed to compete in Olympic track and field, after years of resistance from officials who considered the events too strenuous for women; she had been running competitively for only four months.",
     "fa": "At the Amsterdam Games she won the inaugural women's 100m Olympic title in a world record 12.2 seconds, in what was just her fourth-ever track meet. She remains the youngest woman to win Olympic 100m gold."},

    {"n": "Danica Patrick", "sp": "Motorsport (IndyCar)", "cc": "US", "yr": "1982-",
     "ctx": "In more than a decade of major open-wheel racing history before her, no woman had ever won a top-tier IndyCar race, in a series where cars, teams, and sponsorship money were built almost entirely around male drivers.",
     "fa": "On April 20, 2008 she won the Indy Japan 300 at Twin Ring Motegi, becoming the first woman to win a major American open-wheel race. It remains the only IndyCar Series win by a woman."},

    {"n": "Becky Hammon", "sp": "Basketball (coaching)", "cc": "US", "yr": "1977-",
     "ctx": "In the NBA's 74-year history, no woman had ever directed a team during a live game; she had spent six years as an assistant coach proving herself to skeptical players and staff before the moment came.",
     "fa": "On December 30, 2020, when San Antonio Spurs head coach Gregg Popovich was ejected, assistant Becky Hammon took over on the sideline, becoming the first woman to act as head coach of an NBA team during a regular-season game."},

    {"n": "Patty Berg", "sp": "Golf", "cc": "US", "yr": "1918-2006",
     "ctx": "In 1950 there was no organized professional tour for women golfers, and the men-only structure of professional golf offered women essentially no path to compete for prize money or public recognition.",
     "fa": "She was one of 13 founders of the LPGA in 1950 and served as its first president. She went on to win a record 15 major championships over her career, a record that still stands today."},

    # Batch 8 (verified 2026-09-29)
    {"n": "Grete Waitz", "sp": "Running (marathon)", "cc": "NO", "yr": "1953-2011",
     "ctx": "Before her, long-distance running was considered a fringe pursuit for women, and many doctors and Olympic officials still believed the marathon distance was too grueling, even medically dangerous, for female athletes.",
     "fa": "She won the New York City Marathon nine times between 1978 and 1988, and her dominance helped prove that prejudice wrong, contributing directly to the women's marathon finally being added to the Olympic program in 1984, where she won silver."},

    {"n": "Kittie Knox", "sp": "Cycling", "cc": "US", "yr": "1874-1900",
     "ctx": "In 1894 the League of American Wheelmen, the era's dominant cycling organization, amended its constitution to formally bar Black members, a year after she had already joined.",
     "fa": "At the League's 1895 national meet in segregated Asbury Park, New Jersey, she showed up and insisted on claiming the membership privileges she was entitled to, forcing organizers into a public standoff over her right to belong. She was ultimately allowed to keep her membership since she had joined before the color bar was passed."},

    {"n": "Chloe Kim", "sp": "Snowboarding", "cc": "US", "yr": "2000-",
     "ctx": "Women's snowboarding halfpipe was still a relatively young Olympic discipline, and few teenagers had ever been able to handle the pressure of the Games while also performing at the sport's highest level.",
     "fa": "At the 2018 PyeongChang Olympics she won gold at age 17 with a score of 98.25, ten points clear of her nearest rival, becoming the youngest woman to win Olympic snowboarding gold. She defended the title in 2022, becoming the first woman to win back-to-back Olympic halfpipe golds."},

    # Batch 9 (verified 2026-09-29)
    {"n": "Debi Thomas", "sp": "Figure skating", "cc": "US", "yr": "1967-",
     "ctx": "No Black athlete, man or woman, had ever won a medal at the Winter Olympics before her, in a sport whose competitors and traditions had been almost exclusively white.",
     "fa": "At the 1988 Calgary Games she won bronze in figure skating, becoming the first Black athlete to medal at a Winter Olympics. She later became an orthopedic surgeon after retiring from competition."},

    {"n": "Vonetta Flowers", "sp": "Bobsled", "cc": "US", "yr": "1973-",
     "ctx": "After repeated failed attempts to qualify for the Summer Olympics as a sprinter and long jumper, she switched to bobsled, a sport that had never had a Black gold medalist from any country in its Winter Olympic history.",
     "fa": "At the 2002 Salt Lake City Games she won gold as a brakewoman alongside Jill Bakken, becoming the first Black athlete from any nation to win a Winter Olympic gold medal."},

    {"n": "Natalie du Toit", "sp": "Swimming", "cc": "ZA", "yr": "1984-",
     "ctx": "In 2001, at age 17, a car accident led to the amputation of her left leg below the knee; able-bodied Olympic swimming had never included an amputee athlete.",
     "fa": "At the 2008 Beijing Olympics she became the first leg amputee to compete in Olympic swimming, finishing the open water 10km race just 1 minute 22 seconds behind the winner, against competitors with no disability. She also won five golds at the Beijing Paralympics that same year."},

    {"n": "Homare Sawa", "sp": "Football", "cc": "JP", "yr": "1978-",
     "ctx": "She captained Japan just months after the devastating March 2011 earthquake and tsunami that killed nearly 20,000 people and displaced over 200,000, and spoke of wanting to give the country something to celebrate.",
     "fa": "She scored the tying goal in the 117th minute of the World Cup final against the United States, leading Japan to its first-ever World Cup title on penalties. She won both the tournament's Golden Ball and Golden Boot, becoming the first Asian player of any gender to be named FIFA World Player of the Year."},

    # Batch 10 (verified 2026-09-29)
    {"n": "Helen Maroulis", "sp": "Wrestling", "cc": "US", "yr": "1991-",
     "ctx": "American women's freestyle wrestling had never produced an Olympic champion; her opponent in the final, Japan's Saori Yoshida, was a three-time defending Olympic champion and thirteen-time world champion considered the greatest female wrestler of all time.",
     "fa": "At the 2016 Rio Olympics she upset Yoshida to win gold at 53kg, becoming the first American woman to win an Olympic wrestling title."},

    {"n": "Kayla Harrison", "sp": "Judo", "cc": "US", "yr": "1990-",
     "ctx": "She had been sexually abused for years by a former coach as a teenager, and American judo had produced only one Olympic medal by a woman before her, a bronze four years earlier.",
     "fa": "At the 2012 London Olympics she won the 78kg judo title, becoming the first American, male or female, to win an Olympic gold medal in judo."},

    {"n": "Toni Harris", "sp": "American football", "cc": "US", "yr": "1996-",
     "ctx": "Women had occasionally kicked for college football teams before, but no woman had ever been offered an athletic scholarship to play a non-kicking position.",
     "fa": "In February 2019 she signed with Central Methodist University as a defensive back, becoming the first woman to receive a college football scholarship at a skill position rather than as a kicker."},

    {"n": "Surya Bonaly", "sp": "Figure skating", "cc": "FR", "yr": "1973-",
     "ctx": "The backflip had been effectively banned from competitive figure skating since the 1970s over safety concerns, and she was already out of medal contention, frustrated with what she felt was biased judging.",
     "fa": "At the 1998 Nagano Olympics she closed her free skate with an illegal backflip, landing it on a single blade rather than two feet, a far harder version than the one that had gotten the move banned decades earlier, knowing it would hurt her score."},

    # Batch 11 (verified 2026-09-29)
    {"n": "Susan Butcher", "sp": "Sled dog racing", "cc": "US", "yr": "1954-2006",
     "ctx": "The Iditarod, a grueling 1,000-mile sled dog race across Alaska, was widely regarded as a man's endurance test; the year before her first win, several of her dogs had been killed in a moose attack mid-race.",
     "fa": "She won the Iditarod in 1986, 1987, 1988, and 1990, becoming the first woman to win it four times, including three consecutive victories. Her 1990 win came in near-record time despite brutal weather along the trail."},

    {"n": "Judit Polgár", "sp": "Chess", "cc": "HU", "yr": "1976-",
     "ctx": "She and her sisters were raised under an unconventional home-schooling experiment by their father, who believed geniuses could be deliberately trained, in a chess world where women were almost entirely absent from elite competition.",
     "fa": "In 1991 she became a grandmaster at 15 years and 4 months, the youngest person ever to do so at the time, breaking Bobby Fischer's record. She went on to defeat 11 current or former world champions and is the only woman ever to rank in the world's top 10."},

    {"n": "Uta Pippig", "sp": "Running (marathon)", "cc": "DE", "yr": "1965-",
     "ctx": "She grew up in communist East Germany, where the Berlin Wall made the Boston Marathon, the world's most storied road race, seem like an unreachable dream.",
     "fa": "In 1990 she won the \"Reunification Marathon,\" the first Berlin Marathon to run through the Brandenburg Gate from West to East, three days before official German reunification. She later became the first woman to win the Boston Marathon three years in a row, from 1994 to 1996."},

    {"n": "Cecilia Colledge", "sp": "Figure skating", "cc": "GB", "yr": "1920-2008",
     "ctx": "Figure skating had no minimum competition age at the time, and her mother pulled her out of school to train abroad in pursuit of Olympic qualification for a child not yet a teenager.",
     "fa": "At the 1932 Lake Placid Games, aged just 11 years and 73 days, she became the youngest competitor in Winter Olympics history and remains Britain's youngest-ever Olympian, a record that still stands today."},

    # Batch 12 (verified 2026-09-29)
    {"n": "Amy Van Dyken", "sp": "Swimming", "cc": "US", "yr": "1973-",
     "ctx": "She was diagnosed with severe asthma at 18 months old and couldn't swim a full pool length until age 12, taking up the sport on doctors' advice as a way to strengthen her lungs.",
     "fa": "At the 1996 Atlanta Olympics she won four gold medals, becoming the first American woman to win four golds at a single Olympics. She finished her career with six Olympic golds in total."},

    {"n": "Marion Ladewig", "sp": "Bowling", "cc": "US", "yr": "1914-2010",
     "ctx": "Competitive bowling in the mid-20th century was dominated by men's leagues, and mixed-gender competitions against top male bowlers were almost unheard of.",
     "fa": "In 1951 she won her city, state, and national all-events titles in the same year, a feat no other woman has matched, defeating all 63 women AND all 160 men entered in the competition. She was named Bowler of the Year nine times between 1950 and 1963."},

    {"n": "Eleonora Sears", "sp": "Multi-sport (tennis/squash/polo)", "cc": "US", "yr": "1881-1968",
     "ctx": "In Edwardian-era Boston high society, women's sport was expected to be genteel and modest; riding onto a polo field in trousers in 1909 was scandalous enough that local ministers preached sermons against her.",
     "fa": "She became the first woman to play polo on a men's team, broke the Harvard Club's men-only squash ban by 1918, and championed women's access to the sport as founding president of the U.S. Women's Squash Racquets Association, earning her the nickname \"Mother of Squash.\""},

    {"n": "Ana Fidelia Quirot", "sp": "Athletics (middle distance)", "cc": "CU", "yr": "1963-",
     "ctx": "In early 1993 a domestic gas accident left 38% of her body covered in severe burns; she underwent a dozen rounds of reconstructive surgery over the following two years and missed an entire competitive season.",
     "fa": "In 1995, less than two and a half years after the accident, she won the 800m world title in Gothenburg, later calling it the most beautiful victory of her life. She won a second world title in 1997 and two Olympic silver medals."},

    {"n": "Althea Gibson", "sp": "Tennis", "cc": "US", "yr": "1927-2003",
     "ctx": "Tennis in the 1950s was played in exclusive, segregated country clubs, and she had already broken through as the first Black player to compete at both the US Championships (1950) and Wimbledon (1951) before winning a single major title.",
     "fa": "On July 6, 1957 she won the Wimbledon singles title, becoming the first Black player, man or woman, to win a Grand Slam tournament. She won 11 Grand Slam titles between 1956 and 1958 and was honored with a ticker-tape parade in New York."},

    {"n": "Milena Duchková", "sp": "Diving", "cc": "CZ", "yr": "1952-",
     "ctx": "At just 16, she competed for Czechoslovakia only weeks after Soviet-led forces invaded the country to crush the Prague Spring reform movement, an event that shadowed the entire Czechoslovak team's presence at the Games.",
     "fa": "At the 1968 Mexico City Olympics she won gold in platform diving, becoming the first diver of any nationality to score over 100 points at the Olympics, and delivering Czechoslovakia's first-ever Olympic medal in any water sport."},

    {"n": "Nicola Adams", "sp": "Boxing", "cc": "GB", "yr": "1982-",
     "ctx": "London 2012 marked the very first time women's boxing was included in the Olympic program, after decades of the sport being considered exclusively male at the Games.",
     "fa": "She beat three-time world champion Ren Cancan of China in the flyweight final to win gold in front of her home crowd, becoming the first female Olympic boxing champion in history."},

    # Batch 13 (verified 2026-09-29, added to rebalance geography beyond the US)
    {"n": "Derartu Tulu", "sp": "Athletics (long distance)", "cc": "ET", "yr": "1972-",
     "ctx": "No Black African woman had ever won an Olympic gold medal before her, and South Africa had only just been readmitted to the Games after years of exclusion over apartheid.",
     "fa": "She won the 10,000m at the 1992 Barcelona Olympics ahead of South Africa's Elana Meyer, and the two took a joint victory lap holding hands, an image that became one of the era's most iconic symbols of post-apartheid reconciliation. She won the event again in 2000, becoming the only woman to win Olympic 10,000m gold twice."},

    {"n": "Tegla Loroupe", "sp": "Running (marathon)", "cc": "KE", "yr": "1973-",
     "ctx": "Before her, no African woman had ever won one of the world's major city marathons, in a sport where East African men were already dominant but women's distance running had barely developed as a pathway out of poverty.",
     "fa": "In 1994, at age 21, she won the New York City Marathon on her very first attempt at the distance, becoming the first African woman to win a major marathon. She later held the marathon world record and became a prominent peace advocate, organizing races across conflict zones in East Africa."},

    {"n": "Wanda Rutkiewicz", "sp": "Mountaineering", "cc": "PL", "yr": "1943-1992",
     "ctx": "High-altitude mountaineering in communist-era Poland offered almost no institutional support for women, and international expeditions above 8,000 meters were still considered the domain of male climbers.",
     "fa": "In 1978 she became the first European woman to summit Everest. In 1986 she became the first woman ever to summit K2, widely considered the most dangerous mountain in the world, without supplemental oxygen. She disappeared attempting Kangchenjunga in 1992."},

    {"n": "Merlene Ottey", "sp": "Athletics (sprint)", "cc": "JM", "yr": "1960-",
     "ctx": "She competed across seven Olympic Games from 1980 to 2004, an unmatched span for any track and field athlete, repeatedly finishing agonizingly close to gold in the era of the fastest sprinters in history.",
     "fa": "She holds the record for the most World Championship medals won by any athlete in an individual event, 10, and earned the nickname \"the Bronze Queen\" after finishing third an extraordinary 13 times at the Olympics and World Championships combined."},

    {"n": "Susi Susanti", "sp": "Badminton", "cc": "ID", "yr": "1971-",
     "ctx": "No athlete from Southeast Asia, a region of over 600 million people, had ever won an Olympic gold medal before her, and badminton was making its debut as a full medal sport at these Games.",
     "fa": "At the 1992 Barcelona Olympics she won the women's singles badminton title, becoming the first Olympic gold medalist in Southeast Asian history. She returned home to a hero's welcome and remains one of Indonesia's most celebrated athletes."},

    {"n": "Betty Cuthbert", "sp": "Athletics (sprint)", "cc": "AU", "yr": "1938-2017",
     "ctx": "At the 1956 Melbourne Games, the host nation's female sprinters dominated a program that still offered women only four track events in total, a fraction of the men's schedule.",
     "fa": "At just 18 she won three gold medals at her home Olympics in the 100m, 200m, and 4x100m relay. She later added a fourth gold in the 400m at the 1964 Tokyo Games, making her the only athlete in history, male or female, to win Olympic gold in the 100m, 200m, and 400m."},
]
