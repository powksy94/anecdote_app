import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=name, co=country, sp=sport, yr=active years,
# tr=trophies (None if not applicable), md=medals (None if not applicable),
# fa=impact, im=imageUrl

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

WIKI_EN = {
    "Muhammad Ali":       "Muhammad Ali",
    "Usain Bolt":         "Usain Bolt",
    "Michael Jordan":     "Michael Jordan",
    "Serena Williams":    "Serena Williams",
    "Pele":               "Pele (Brazilian footballer)",
    "Michael Phelps":     "Michael Phelps",
    "Roger Federer":      "Roger Federer",
    "Simone Biles":       "Simone Biles",
    "Lionel Messi":       "Lionel Messi",
    "Ayrton Senna":       "Ayrton Senna",
    "Michael Schumacher": "Michael Schumacher",
    "Jesse Owens":        "Jesse Owens",
    "Jackie Robinson":    "Jackie Robinson",
    "Nadia Comaneci":     "Nadia Comaneci",
    "Diego Maradona":     "Diego Maradona",
    "Carl Lewis":         "Carl Lewis",
    "Tiger Woods":        "Tiger Woods",
    "Wayne Gretzky":      "Wayne Gretzky",
    "Billie Jean King":   "Billie Jean King",
    "Zinedine Zidane":    "Zinedine Zidane",
    "Eliud Kipchoge":     "Eliud Kipchoge",
    "Steffi Graf":        "Steffi Graf",
    "Ronaldo":            "Ronaldo (Brazilian footballer)",
    # additional entries
    "Martina Navratilova":    "Martina Navratilova",
    "Rafael Nadal":           "Rafael Nadal",
    "Novak Djokovic":         "Novak Djokovic",
    "LeBron James":           "LeBron James",
    "Magic Johnson":          "Magic Johnson",
    "Kareem Abdul-Jabbar":    "Kareem Abdul-Jabbar",
    "Wilt Chamberlain":       "Wilt Chamberlain",
    "Sachin Tendulkar":       "Sachin Tendulkar",
    "Mia Hamm":               "Mia Hamm",
    "Marta":                  "Marta (footballer)",
    "Cristiano Ronaldo":      "Cristiano Ronaldo",
    "Gerd Muller":            "Gerd Müller",
    "Florence Griffith-Joyner": "Florence Griffith-Joyner",
    "Wilma Rudolph":          "Wilma Rudolph",
    "Paavo Nurmi":            "Paavo Nurmi",
    "Emil Zatopek":           "Emil Zátopek",
    "Bob Beamon":             "Bob Beamon",
    "Fanny Blankers-Koen":    "Fanny Blankers-Koen",
    "Haile Gebrselassie":     "Haile Gebrselassie",
    "Cathy Freeman":          "Cathy Freeman",
    "Roger Bannister":        "Roger Bannister",
    "Mark Spitz":             "Mark Spitz",
    "Dawn Fraser":            "Dawn Fraser (swimmer)",
    "Eddy Merckx":            "Eddy Merckx",
    "Valentino Rossi":        "Valentino Rossi (motorcyclist)",
    "Jonah Lomu":             "Jonah Lomu",
    "Richie McCaw":           "Richie McCaw",
    "Jack Nicklaus":          "Jack Nicklaus",
    "Babe Ruth":              "Babe Ruth",
    "Jim Thorpe":             "Jim Thorpe",
    "Babe Didrikson Zaharias":"Babe Didrikson Zaharias",
    "Eric Heiden":            "Eric Heiden",
    "Katarina Witt":          "Katarina Witt",
    "Greg Louganis":          "Greg Louganis",
    "Yelena Isinbayeva":      "Yelena Isinbayeva",
    "Bo Jackson":             "Bo Jackson",
    "Jim Brown":              "Jim Brown (American football)",
}

athletes = [
    # ── Combat Sports ─────────────────────────────────────────────────────────
    {"n": "Muhammad Ali", "co": "United States", "sp": "Boxing", "yr": "1960-1981",
     "tr": "3x World Heavyweight Champion (1964, 1974, 1978)",
     "md": None,
     "fa": "Widely considered the greatest boxer of all time. Olympic gold medallist in 1960. Stripped of his title and banned for three years after refusing military service in 1967. The 'Rumble in the Jungle' and 'Thrilla in Manila' are the most celebrated fights in history. Symbol of Black pride, anti-war resistance, and sporting greatness."},

    # ── Athletics ─────────────────────────────────────────────────────────────
    {"n": "Usain Bolt", "co": "Jamaica", "sp": "Athletics (Sprinting)", "yr": "2004-2017",
     "tr": "8 World Championship gold medals",
     "md": "8 Olympic gold medals (100m, 200m, 4x100m relay — 2008, 2012, 2016)",
     "fa": "The fastest human being ever recorded. Holder of the 100m (9.58s) and 200m (19.19s) world records since 2009. The only man to win both events at three consecutive Olympics. His dominance of sprinting is without parallel in the sport's history."},

    {"n": "Jesse Owens", "co": "United States", "sp": "Athletics (Sprinting & Long Jump)", "yr": "1935-1936",
     "tr": "4 world records set in 45 minutes (1935)",
     "md": "4 Olympic gold medals (Berlin 1936: 100m, 200m, long jump, 4x100m relay)",
     "fa": "His four gold medals at the Berlin 1936 Olympics — in front of Adolf Hitler — directly contradicted Nazi claims of Aryan racial superiority. Set three world records and tied a fourth in a single afternoon on 25 May 1935. Returned home a global hero but was still denied basic civil rights in the United States."},

    {"n": "Carl Lewis", "co": "United States", "sp": "Athletics (Sprinting & Long Jump)", "yr": "1979-1997",
     "tr": "10 World Championship gold medals",
     "md": "9 Olympic gold medals across four Olympics (1984-1996)",
     "fa": "Won the long jump gold medal at four consecutive Olympics — an almost unique achievement in athletics. Emulated Jesse Owens by winning 4 gold medals at a single Olympics (Los Angeles 1984). Voted 'Sportsman of the Century' by the International Olympic Committee."},

    {"n": "Eliud Kipchoge", "co": "Kenya", "sp": "Marathon", "yr": "2003-",
     "tr": "2 Olympic gold medals (2016, 2021). 14 of 15 marathons won.",
     "md": None,
     "fa": "The greatest marathon runner in history. In October 2019 became the first human to run a marathon in under two hours (1:59:40) in a controlled time trial. His philosophical approach — 'No human is limited' — has made him a global cultural figure beyond sport."},

    # ── Swimming ──────────────────────────────────────────────────────────────
    {"n": "Michael Phelps", "co": "United States", "sp": "Swimming", "yr": "2000-2016",
     "tr": None,
     "md": "28 Olympic medals (23 gold, 3 silver, 2 bronze) — the most decorated Olympian of all time",
     "fa": "Competed in five Olympics and won a medal in each. At Beijing 2008 won 8 gold medals in a single Games — the most by any athlete at a single Olympics. His dominance of swimming from 2000 to 2016 is without precedent. Openly discussed his battle with mental health after retirement."},

    # ── Tennis ────────────────────────────────────────────────────────────────
    {"n": "Serena Williams", "co": "United States", "sp": "Tennis", "yr": "1995-2022",
     "tr": "23 Grand Slam singles titles (Open Era record)",
     "md": "4 Olympic gold medals (3 doubles, 1 singles - 2012 London)",
     "fa": "The greatest female tennis player of the Open Era. Won 23 Grand Slam singles titles. Held all four Grand Slam titles simultaneously twice ('Serena Slam'). Her power and athleticism transformed women's tennis. A fierce advocate for gender and racial equality in sport."},

    {"n": "Roger Federer", "co": "Switzerland", "sp": "Tennis", "yr": "1998-2022",
     "tr": "20 Grand Slam singles titles (men's record at retirement)",
     "md": "Olympic gold: doubles 2008, singles silver 2012",
     "fa": "Held the World No. 1 ranking for a record 310 weeks. Won 20 Grand Slam titles across a 24-year career. Known for his graceful, near-perfect game, he is considered the embodiment of sporting elegance. His rivalry with Nadal and Djokovic elevated men's tennis to its most-watched era."},

    {"n": "Billie Jean King", "co": "United States", "sp": "Tennis", "yr": "1961-1990",
     "tr": "39 Grand Slam titles (singles, doubles, mixed) — 12 singles",
     "md": None,
     "fa": "Won the famous 'Battle of the Sexes' match against Bobby Riggs in 1973, watched by 90 million people worldwide. Campaigned for equal prize money in tennis — the US Open became the first Grand Slam to offer equal pay in 1973. A foundational figure in women's sports equality."},

    {"n": "Steffi Graf", "co": "Germany", "sp": "Tennis", "yr": "1982-1999",
     "tr": "22 Grand Slam singles titles",
     "md": "Olympic gold medal (Seoul 1988) — completing the 'Golden Grand Slam'",
     "fa": "The only tennis player in history — male or female — to win the Golden Grand Slam: all four Grand Slams and the Olympic gold medal in the same calendar year (1988). Held the World No. 1 ranking for a record 377 weeks."},

    # ── Football / Soccer ──────────────────────────────────────────────────────
    {"n": "Pele", "co": "Brazil", "sp": "Football (Soccer)", "yr": "1956-1977",
     "tr": "3x FIFA World Cup winner (1958, 1962, 1970)",
     "md": None,
     "fa": "Only player in history to win three FIFA World Cups. Scored an official 757 goals in his career, widely considered a world record. Won his first World Cup at age 17 — still the youngest World Cup winner ever. Declared a national treasure by Brazil, preventing his transfer abroad."},

    {"n": "Diego Maradona", "co": "Argentina", "sp": "Football (Soccer)", "yr": "1976-1997",
     "tr": "FIFA World Cup 1986 (tournament's outstanding player)",
     "md": None,
     "fa": "His performance in the 1986 World Cup — scoring both the 'Hand of God' goal and the 'Goal of the Century' in the same match against England — is the greatest individual World Cup display ever. Led Napoli from relegation candidates to two Serie A titles."},

    {"n": "Lionel Messi", "co": "Argentina", "sp": "Football (Soccer)", "yr": "2004-",
     "tr": "FIFA World Cup 2022. 8x Ballon d'Or (record). 10x La Liga. 4x UEFA Champions League.",
     "md": "Olympic gold medal (Beijing 2008)",
     "fa": "Widely considered the greatest footballer of all time. Won the 2022 World Cup — completing a career that needed only that trophy. Set La Liga records for goals (50 in a single season) and assists. Spent 21 years at FC Barcelona before moving to PSG and Inter Miami."},

    {"n": "Zinedine Zidane", "co": "France", "sp": "Football (Soccer)", "yr": "1988-2006",
     "tr": "FIFA World Cup 1998. UEFA Champions League 2001-02. 3x FIFA World Player of the Year.",
     "md": None,
     "fa": "Arguably the greatest individual performance in a World Cup final: two headers against Brazil in 1998. Renowned for his elegance, vision, and 'roulette' turn. His headbutt of Materazzi in the 2006 World Cup final — ending his career — remains one of sport's most unforgettable moments."},

    {"n": "Ronaldo", "co": "Brazil", "sp": "Football (Soccer)", "yr": "1993-2011",
     "tr": "FIFA World Cup 1994 (squad), 2002. 3x FIFA World Player of the Year.",
     "md": None,
     "fa": "'The Phenomenon' — Ronaldo Luiz Nazario de Lima. Greatest centre-forward of his generation. Scored 15 World Cup goals (a record at the time). Overcame career-threatening injuries to win the 2002 World Cup. His performances in that tournament are among the greatest in football history."},

    # ── Basketball ────────────────────────────────────────────────────────────
    {"n": "Michael Jordan", "co": "United States", "sp": "Basketball", "yr": "1984-2003",
     "tr": "6x NBA Champion. 6x NBA Finals MVP. 5x NBA Most Valuable Player.",
     "md": "2 Olympic gold medals (1984, 1992 Dream Team)",
     "fa": "Widely considered the greatest basketball player of all time. Led the Chicago Bulls to six NBA championships with six Finals MVP awards — a perfect record. Elevated the NBA to a global phenomenon. His Air Jordan brand remains the most successful athlete endorsement in history."},

    # ── Gymnastics ─────────────────────────────────────────────────────────────
    {"n": "Simone Biles", "co": "United States", "sp": "Gymnastics", "yr": "2013-",
     "tr": "7 Olympic medals (4 gold, 1 silver, 2 bronze — 2016 & 2024). 30 World Championship medals (including 23 gold).",
     "md": None,
     "fa": "The most decorated gymnast in World Championship history. Four gymnastics moves are named after her. Withdrew from the 2020 Tokyo Games to prioritise mental health — a decision that sparked global conversation about athlete wellbeing and redefined what athletic courage means."},

    {"n": "Nadia Comaneci", "co": "Romania", "sp": "Gymnastics", "yr": "1975-1989",
     "tr": "3 Olympic gold medals (Montreal 1976), 2 (Moscow 1980). 9 Olympic medals total.",
     "md": None,
     "fa": "First gymnast in history to receive a perfect score of 10.0 at the Olympics (Montreal 1976) — the scoreboard could not display 10, so it showed 1.00. She received seven perfect 10s at that single Games. Performed at age 14 what has never been equalled."},

    # ── Formula 1 ─────────────────────────────────────────────────────────────
    {"n": "Ayrton Senna", "co": "Brazil", "sp": "Formula 1", "yr": "1984-1994",
     "tr": "3x Formula 1 World Champion (1988, 1990, 1991)",
     "md": None,
     "fa": "65 pole positions (a record when he died), 41 race wins. Killed in the 1994 San Marino Grand Prix — his death prompted the biggest overhaul of F1 safety in the sport's history. Considered by many drivers the greatest of all time."},

    {"n": "Michael Schumacher", "co": "Germany", "sp": "Formula 1", "yr": "1991-2012",
     "tr": "7x Formula 1 World Champion (1994, 1995, 2000, 2001, 2002, 2003, 2004) — all-time record",
     "md": None,
     "fa": "Holds records for most World Championship titles (7) and most wins (91) at the time of his retirement. Won five consecutive titles with Ferrari (2000-2004). Suffered a severe brain injury in a skiing accident in 2013."},

    # ── Golf ──────────────────────────────────────────────────────────────────
    {"n": "Tiger Woods", "co": "United States", "sp": "Golf", "yr": "1996-",
     "tr": "15 Major championships",
     "md": None,
     "fa": "Transformed golf from a largely white, elite sport into a global phenomenon. Won the Masters at 21 by 12 strokes (1997) — the largest margin in Masters history. His 2019 Masters win, after multiple back surgeries and a personal scandal, is considered one of sport's greatest comebacks."},

    # ── Ice Hockey ─────────────────────────────────────────────────────────────
    {"n": "Wayne Gretzky", "co": "Canada", "sp": "Ice Hockey", "yr": "1978-1999",
     "tr": "4x Stanley Cup Champion. 9x Hart Trophy (MVP). 10x Art Ross Trophy (top scorer).",
     "md": None,
     "fa": "Known as 'The Great One' — the only player whose NHL records are considered virtually unbreakable. Scored more goals (894) than any other player, AND has more assists (1,963) than any player has total points. The NHL retired jersey number 99 league-wide in his honour."},

    # ── Baseball ──────────────────────────────────────────────────────────────
    {"n": "Jackie Robinson", "co": "United States", "sp": "Baseball", "yr": "1945-1956",
     "tr": "World Series winner 1955. National League MVP 1949.",
     "md": None,
     "fa": "First African-American to play in Major League Baseball (1947), breaking the sport's colour barrier. Endured death threats, racial abuse, and physical attacks throughout his career. His courage paved the way for the desegregation of all American professional sports. Received the Presidential Medal of Freedom and the Congressional Gold Medal."},

    {"n": "Babe Ruth", "co": "United States", "sp": "Baseball", "yr": "1914-1935",
     "tr": "7x World Series Champion. 714 home runs (stood as MLB record until 1974).",
     "md": None,
     "fa": "The most iconic figure in American sports history. Transformed baseball from a low-scoring game into a power-hitting spectacle that captivated a nation. Hit 60 home runs in 1927 — a single-season record that stood for 34 years. Called 'the Sultan of Swat'; his fame popularised professional baseball globally."},

    # ── Tennis (additional) ───────────────────────────────────────────────────
    {"n": "Martina Navratilova", "co": "Czech Republic / United States", "sp": "Tennis", "yr": "1978-2006",
     "tr": "18 Grand Slam singles titles. 59 Grand Slam titles overall (singles, doubles, mixed).",
     "md": None,
     "fa": "Dominated women's tennis for two decades. Won Wimbledon nine times — a record. Held the World No. 1 ranking for a total of 332 weeks. Defected from communist Czechoslovakia at 18. Came out as a lesbian in 1981 — at enormous personal and commercial cost. One of the greatest athletes in any sport."},

    {"n": "Rafael Nadal", "co": "Spain", "sp": "Tennis", "yr": "2001-2024",
     "tr": "22 Grand Slam singles titles. 14x French Open champion — the most titles at a single major in history.",
     "md": "Olympic gold medal: singles (Beijing 2008) and doubles (2016)",
     "fa": "The greatest clay court player in history. His 14 French Open titles at Roland Garros is one of the most dominant records in all of sport. Overcame serious knee injuries multiple times to return to the top. His rivalry with Federer is considered the greatest in tennis history."},

    {"n": "Novak Djokovic", "co": "Serbia", "sp": "Tennis", "yr": "2003-",
     "tr": "24 Grand Slam singles titles — the all-time men's record.",
     "md": "Olympic gold medal: singles (Paris 2024)",
     "fa": "Holds the all-time record for most Grand Slam titles in men's tennis (24) and most weeks at World No. 1 (428 weeks). Won the Career Golden Slam in 2024. Overcame sanctions for not being vaccinated — including deportation from Australia — to continue competing at the highest level into his late 30s."},

    # ── Basketball (additional) ───────────────────────────────────────────────
    {"n": "LeBron James", "co": "United States", "sp": "Basketball", "yr": "2003-",
     "tr": "4x NBA Champion (2012, 2013, 2016, 2020). 4x NBA Finals MVP. 4x NBA Most Valuable Player.",
     "md": "2 Olympic gold medals (2004, 2012)",
     "fa": "The only player to win NBA championships with three different franchises. The all-time NBA scoring leader. Drafted first overall aged 18 directly from high school, he has sustained elite performance for over 20 years. A global figure off the court through his LeBron James Family Foundation and social justice advocacy."},

    {"n": "Magic Johnson", "co": "United States", "sp": "Basketball", "yr": "1979-1996",
     "tr": "5x NBA Champion (1980, 1982, 1985, 1987, 1988). 3x NBA Finals MVP. 3x NBA Most Valuable Player.",
     "md": "Olympic gold medal (1992 Dream Team)",
     "fa": "Revolutionised the point guard position at 6'9\". His 'Showtime' Lakers dominated the 1980s. Retired suddenly in 1991 after testing HIV-positive — a moment that transformed public understanding of HIV/AIDS. His openness about his condition saved countless lives and removed a massive stigma from the disease."},

    {"n": "Kareem Abdul-Jabbar", "co": "United States", "sp": "Basketball", "yr": "1969-1989",
     "tr": "6x NBA Champion. 6x NBA Most Valuable Player (record). All-time NBA scoring leader (38,387 points) until 2023.",
     "md": None,
     "fa": "The all-time NBA scoring leader for 38 years. His 'skyhook' shot — virtually unblockable — is the most devastating weapon in basketball history. Converted to Islam at 24 and changed his name from Lew Alcindor. A civil rights activist who refused to play for the 1968 US Olympic team in protest."},

    {"n": "Wilt Chamberlain", "co": "United States", "sp": "Basketball", "yr": "1959-1973",
     "tr": "2x NBA Champion (1967, 1972). 4x NBA Most Valuable Player.",
     "md": None,
     "fa": "Scored 100 points in a single NBA game on 2 March 1962 — a record that will almost certainly never be broken. In that same season, averaged 50.4 points and 25.7 rebounds per game — statistics so extraordinary they seem impossible. The most dominant physical force in NBA history."},

    # ── Cricket ───────────────────────────────────────────────────────────────
    {"n": "Sachin Tendulkar", "co": "India", "sp": "Cricket", "yr": "1989-2013",
     "tr": "ICC Cricket World Cup 2011. 100 international centuries — the only player in history.",
     "md": None,
     "fa": "Called 'the God of Cricket' in India. The first and only cricketer to score 100 international centuries. Played 200 Test matches and 463 One Day Internationals over 24 years. In a country of over a billion people, his retirement was a national moment of mourning. Awarded India's highest civilian honour, the Bharat Ratna."},

    # ── Football / Soccer (additional) ────────────────────────────────────────
    {"n": "Cristiano Ronaldo", "co": "Portugal", "sp": "Football (Soccer)", "yr": "2002-",
     "tr": "5x UEFA Champions League. 5x Ballon d'Or. All-time international top scorer (130 goals).",
     "md": None,
     "fa": "The all-time top scorer in international football with 130 goals. Won the Champions League with three different clubs (Manchester United, Real Madrid x4, Juventus). His relentless self-discipline and physical conditioning redefined what a footballer's body could achieve into their late 30s."},

    {"n": "Mia Hamm", "co": "United States", "sp": "Football (Soccer)", "yr": "1987-2004",
     "tr": "2x FIFA Women's World Cup (1991, 1999).",
     "md": "2 Olympic gold medals (1996, 2004)",
     "fa": "The most famous female footballer in history — the face that made women's football a mass sport. Her penalty in the 1999 World Cup final shootout, watched by 90,000 fans in the Rose Bowl and 40 million on television, is one of sport's iconic moments. Held the international goals record for both men and women for years."},

    {"n": "Marta", "co": "Brazil", "sp": "Football (Soccer)", "yr": "2002-",
     "tr": "6x FIFA World Player of the Year — the record for any player, male or female.",
     "md": None,
     "fa": "The greatest female footballer in history. Won FIFA World Player of the Year a record six times. Became the all-time leading scorer in Women's World Cup history. Born in poverty in rural Brazil, she overcame every obstacle — including a football culture that actively discouraged girls — to become the defining figure of the women's game."},

    {"n": "Gerd Muller", "co": "Germany", "sp": "Football (Soccer)", "yr": "1964-1981",
     "tr": "FIFA World Cup 1974. UEFA Euro 1972. 4x Bundesliga. 4x European Cup.",
     "md": None,
     "fa": "'Der Bomber' — the greatest pure goalscorer in football history. Scored 68 goals in 62 international appearances. His 365 goals in Bundesliga football — at a rate of 0.85 per game — was a record for 49 years. Scored the winning goal in the 1974 World Cup final. Struck with an economy and precision that no defender could read."},

    # ── Athletics (additional) ────────────────────────────────────────────────
    {"n": "Florence Griffith-Joyner", "co": "United States", "sp": "Athletics (Sprinting)", "yr": "1980-1989",
     "tr": None,
     "md": "3 Olympic gold medals, 1 silver (Seoul 1988: 100m, 200m, 4x100m relay)",
     "fa": "Set world records in the 100m (10.49s) and 200m (21.34s) at the 1988 Olympics that still stand today — 36 years later. 'FloJo' combined unprecedented physical power with extraordinary style, transforming how female athletes presented themselves. Died of an epileptic seizure at 38 — one of sport's greatest losses."},

    {"n": "Wilma Rudolph", "co": "United States", "sp": "Athletics (Sprinting)", "yr": "1958-1962",
     "tr": None,
     "md": "3 Olympic gold medals (Rome 1960: 100m, 200m, 4x100m relay)",
     "fa": "First American woman to win three gold medals at a single Olympics. Born premature and survived polio and scarlet fever as a child, wearing a leg brace until age 12. Her 1960 Rome victories — as a Black woman in the Jim Crow era — made her a global symbol of overcoming adversity. She refused to attend her own homecoming parade unless it was desegregated — it was."},

    {"n": "Paavo Nurmi", "co": "Finland", "sp": "Athletics (Long Distance)", "yr": "1919-1934",
     "tr": "12 World records",
     "md": "9 Olympic gold medals, 3 silver — the most of any track and field athlete",
     "fa": "Called 'the Flying Finn' — the dominant distance runner of the 1920s. Won 9 Olympic gold medals at three Games (1920, 1924, 1928). At the 1924 Paris Olympics, he won the 1500m and 5000m within an hour of each other — a feat considered physiologically impossible. Ran with a stopwatch in hand, the first athlete to use scientific pacing."},

    {"n": "Emil Zatopek", "co": "Czech Republic (Czechoslovakia)", "sp": "Athletics (Long Distance)", "yr": "1948-1958",
     "tr": "18 World records",
     "md": "4 Olympic gold medals, 1 silver (1948, 1952). At Helsinki 1952: 5000m, 10000m, and marathon — the only man to win all three at a single Olympics.",
     "fa": "The greatest long-distance runner of all time. His Helsinki triple — including a marathon he had never run before — is sport's greatest single Games performance. Invented interval training, the method that still underpins distance running. Spoke out against the 1968 Prague Spring suppression; was punished by the Czech regime and forced to work in a uranium mine."},

    {"n": "Bob Beamon", "co": "United States", "sp": "Athletics (Long Jump)", "yr": "1964-1973",
     "tr": None,
     "md": "Olympic gold medal (Mexico City 1968)",
     "fa": "His long jump of 8.90m at the 1968 Mexico City Olympics shattered the world record by 55cm — the largest margin improvement in the history of the event. The record stood for 23 years. Sports commentators called it 'the perfect jump.' Beamon himself collapsed and was helped off the runway, overcome by the realisation of what he had done."},

    {"n": "Fanny Blankers-Koen", "co": "Netherlands", "sp": "Athletics (Sprinting & Jumping)", "yr": "1936-1955",
     "tr": None,
     "md": "4 Olympic gold medals (London 1948: 100m, 200m, 80m hurdles, 4x100m relay)",
     "fa": "Won four gold medals at the 1948 London Olympics at age 30 — a mother of two. Before the Games, the press wrote that she was 'too old to compete.' She held world records in six events but was only allowed to enter four. Called 'the Flying Housewife' in a phrase that revealed every prejudice of the era. The greatest female athlete of the immediate post-war generation."},

    {"n": "Haile Gebrselassie", "co": "Ethiopia", "sp": "Long Distance Running", "yr": "1992-2010",
     "tr": "2x Olympic gold medals. 2x World Athletics Championships 10000m. Multiple world records.",
     "md": "2 Olympic gold medals (10000m: Atlanta 1996, Sydney 2000)",
     "fa": "One of the greatest distance runners in history. Set 27 world records across distances from 2000m to the marathon. Set the marathon world record (2:03:59) in 2008 — the first man under 2:04. Ran barefoot as a child to school; became the face of Ethiopian athletics and a global ambassador for the sport."},

    {"n": "Cathy Freeman", "co": "Australia", "sp": "Athletics (400m)", "yr": "1990-2003",
     "tr": "2x World Athletics Championships 400m gold (1997, 1999).",
     "md": "Olympic gold medal (Sydney 2000)",
     "fa": "Won Olympic gold in the 400m at the Sydney 2000 home Games — the most watched moment in Australian sports history. An Aboriginal Australian, she carried both the Australian and Aboriginal flags after winning the 1994 Commonwealth Games, sparking national debate about reconciliation. Her Sydney gold, lit by the entirety of Australia watching, became a moment of profound national meaning."},

    {"n": "Roger Bannister", "co": "United Kingdom", "sp": "Athletics (Middle Distance)", "yr": "1951-1954",
     "tr": None,
     "md": None,
     "fa": "On 6 May 1954, became the first human to run a mile in under four minutes (3:59.4) — a barrier many physiologists had declared biologically impossible. The four-minute mile had been the sporting world's great obsession for decades. Within 46 days, his record was broken — proving that the barrier was psychological, not physical."},

    # ── Swimming (additional) ─────────────────────────────────────────────────
    {"n": "Mark Spitz", "co": "United States", "sp": "Swimming", "yr": "1965-1972",
     "tr": None,
     "md": "9 Olympic gold medals. Won 7 gold medals at Munich 1972 — each in world record time.",
     "fa": "At the 1972 Munich Olympics, won 7 gold medals in 7 events — all in world record time — a record that stood until Michael Phelps's 8 golds in 2008. His image in a swimsuit with seven gold medals became one of the most reproduced sports photographs of the 20th century. Competed in the shadow of the Munich massacre."},

    {"n": "Dawn Fraser", "co": "Australia", "sp": "Swimming", "yr": "1956-1964",
     "tr": "3x World record in 100m freestyle.",
     "md": "4 Olympic gold medals: 100m freestyle at three consecutive Olympics (1956, 1960, 1964) — the first swimmer to win the same event at three consecutive Games.",
     "fa": "The first swimmer to win the same individual event at three consecutive Olympics. Held the world record in the 100m freestyle for 15 years. Banned for 10 years after the 1964 Tokyo Olympics for stealing a flag as a prank — a punishment that ended her competitive career. The most beloved Australian athlete of her generation."},

    # ── Cycling ───────────────────────────────────────────────────────────────
    {"n": "Eddy Merckx", "co": "Belgium", "sp": "Cycling", "yr": "1965-1978",
     "tr": "5x Tour de France. 5x Giro d'Italia. 3x World Road Championship. 11 Grand Tours total.",
     "md": None,
     "fa": "Called 'The Cannibal' because he devoured every race. Won 11 Grand Tours and holds the record for most Tour de France stage wins (34). In 1972 set the Hour Record (the most prestigious individual record in cycling) that stood for 12 years. Considered by many the greatest athlete in any sport."},

    # ── Motorcycle Racing ─────────────────────────────────────────────────────
    {"n": "Valentino Rossi", "co": "Italy", "sp": "Motorcycle Racing (MotoGP)", "yr": "1996-2021",
     "tr": "9x World Motorcycle Champion (1997, 1999, 2001-2005, 2008, 2009)",
     "md": None,
     "fa": "The most celebrated motorcycle racer in history. Won world titles in four different classes. His nine world championships include seven in the top class (MotoGP). His showmanship, yellow and sun-logo helmet, and team 'VR46' created a global fan base unequalled in motorsport outside F1. His duels with Sete Gibernau and Jorge Lorenzo defined an era."},

    # ── Rugby ─────────────────────────────────────────────────────────────────
    {"n": "Jonah Lomu", "co": "New Zealand", "sp": "Rugby Union", "yr": "1994-2002",
     "tr": "2x Rugby World Cup winner (1995 finalist, 2003 squad). 63 tries in 63 Tests.",
     "md": None,
     "fa": "Changed rugby union forever at the 1995 World Cup, where his performance against England — running through and over defenders — was broadcast globally to audiences who had never watched rugby. At 6'5\" and 119kg, he had sprint speed that smaller backs could not match. Died at 40 from kidney disease, mourned worldwide."},

    {"n": "Richie McCaw", "co": "New Zealand", "sp": "Rugby Union", "yr": "2001-2015",
     "tr": "2x Rugby World Cup winner (2011, 2015). Most capped All Black (148 Tests). Most wins as Test captain (110).",
     "md": None,
     "fa": "The greatest rugby player of all time by most measures. Led the All Blacks to consecutive Rugby World Cup victories (2011, 2015) — the first team to win back-to-back World Cups. Named World Rugby Player of the Year three times. Redefined the openside flanker position through reading of the game and relentless physicality."},

    # ── Golf (additional) ─────────────────────────────────────────────────────
    {"n": "Jack Nicklaus", "co": "United States", "sp": "Golf", "yr": "1961-2005",
     "tr": "18 Major championships — the all-time record.",
     "md": None,
     "fa": "The 'Golden Bear' — holds the all-time record of 18 Major victories, including 6 Masters titles. His rivalry with Arnold Palmer defined golf in the 1960s-70s. His 1986 Masters win at age 46, coming from behind in the final round, is considered the greatest final round in golf history. Tiger Woods built his entire career in pursuit of this record."},

    # ── Multi-sport ────────────────────────────────────────────────────────────
    {"n": "Jim Thorpe", "co": "United States", "sp": "Athletics, American Football & Baseball", "yr": "1908-1928",
     "tr": "Olympic gold medals: pentathlon and decathlon (Stockholm 1912). NFL champion 1920.",
     "md": "2 Olympic gold medals (Stockholm 1912)",
     "fa": "Considered by many the greatest all-round athlete in American history. Won Olympic gold in both the pentathlon and decathlon in 1912 — medals that were controversially stripped because he had played semi-professional baseball. Also played professional baseball and football. A member of the Sac and Fox Nation, his story is one of extraordinary achievement against systemic discrimination."},

    {"n": "Babe Didrikson Zaharias", "co": "United States", "sp": "Athletics, Golf & Basketball", "yr": "1930-1956",
     "tr": "3 LPGA majors. 82 competitive golf titles.",
     "md": "2 Olympic gold medals, 1 silver (Los Angeles 1932: javelin, 80m hurdles)",
     "fa": "Possibly the greatest female athlete of the 20th century. Won Olympic gold medals in athletics in 1932, then became one of the greatest golfers of all time, winning 82 competitive titles. Also excelled at basketball, baseball, and tennis. Overcame colon cancer in 1953 to win the 1954 US Women's Open by 12 strokes."},

    # ── Speed Skating ─────────────────────────────────────────────────────────
    {"n": "Eric Heiden", "co": "United States", "sp": "Speed Skating", "yr": "1977-1980",
     "tr": "5 World Championship titles (1977-1979).",
     "md": "5 Olympic gold medals (Lake Placid 1980: all five speed skating distances — 500m to 10000m)",
     "fa": "At the 1980 Lake Placid Olympics, won all five individual speed skating events — from sprint to endurance — a feat never equalled. Set world records in four of the five. Then retired from skating at 22 and became a professional cyclist, finishing in the top 10 at the Tour de France. His Lake Placid performance is one of sport's greatest single Olympic achievements."},

    # ── Figure Skating ────────────────────────────────────────────────────────
    {"n": "Katarina Witt", "co": "Germany (East Germany)", "sp": "Figure Skating", "yr": "1983-1994",
     "tr": "6x European Champion. 4x World Champion.",
     "md": "2 Olympic gold medals (Sarajevo 1984, Calgary 1988)",
     "fa": "The most dominant figure skater of the 1980s, winning two Olympic gold medals and four world titles. As an East German athlete, she was a product of the state sporting machine — and used that position to become a global celebrity at a time when East-West Cold War tensions were at their peak. Her 1988 Olympic performance to Carmen is considered the greatest in figure skating history."},

    # ── Diving ────────────────────────────────────────────────────────────────
    {"n": "Greg Louganis", "co": "United States", "sp": "Diving", "yr": "1976-1988",
     "tr": "5 World Championship titles.",
     "md": "4 Olympic gold medals (Los Angeles 1984: platform, springboard; Seoul 1988: platform, springboard)",
     "fa": "The greatest diver in history. Won both platform and springboard gold at two consecutive Olympics. At the 1988 Seoul Games, hit his head on the springboard during preliminaries — sustaining a concussion — but returned to win gold. He was HIV-positive at the time, a fact he revealed years later. Came out as gay in 1994, becoming a prominent advocate for HIV awareness."},

    # ── Athletics (Pole Vault) ────────────────────────────────────────────────
    {"n": "Yelena Isinbayeva", "co": "Russia", "sp": "Athletics (Pole Vault)", "yr": "2000-2016",
     "tr": "2x World Athletics Championship. 28 world records — the most in any single athletics discipline.",
     "md": "2 Olympic gold medals (Athens 2004, Beijing 2008), 1 bronze (London 2012)",
     "fa": "The most decorated female pole vaulter in history. Set 28 world records across her career — an unprecedented number for any individual event. Was the first woman to vault over 5 metres. Her dominance of the event for over a decade redefined what was thought physically possible for female athletes."},

    # ── American Football ─────────────────────────────────────────────────────
    {"n": "Jim Brown", "co": "United States", "sp": "American Football", "yr": "1957-1965",
     "tr": "NFL Champion 1964. 3x NFL Most Valuable Player.",
     "md": None,
     "fa": "Considered the greatest running back in NFL history. Rushed for 12,312 yards at an average of 5.2 yards per carry over 9 seasons — averages never surpassed. Retired at the peak of his powers at 29 to become an actor and civil rights activist. Marched alongside Martin Luther King Jr. His combination of power, speed, and agility set the template for the position."},
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
    total = len(athletes)
    found = 0
    for i, s in enumerate(athletes):
        title = WIKI_EN.get(s["n"], s["n"])
        img = wiki_img(title)
        s["im"] = img
        if img:
            found += 1
        status = "ok" if img else "xx"
        sys.stdout.buffer.write(f"  [{i+1:2}/{total}] {status} {s['n']}\n".encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)
    out = Path("assets/celebrity/legendary_athletes.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(athletes, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    sys.stdout.buffer.write(f"\nDone: {found}/{total} images — {total} athletes total.\n".encode("utf-8"))


if __name__ == "__main__":
    main()
