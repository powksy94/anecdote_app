import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=record name, sp=sport, hd=holder (person/duo/team, None if no single holder),
# cc=ISO2 country code(s) ("/"-joined for dual nationality, None if team/no single nationality),
# yr=year, fa=fact/context, im=imageUrl (only fetched for individual named holders)
#
# Content is written in ENGLISH (source language for the app's translation pipeline — see
# content_loader.dart, which always caches fetched content as locale='en' and translates it
# on the fly for other locales). Writing this in French caused it to be re-translated FR->FR
# by Google Translate and garbled (e.g. "cricket test" became "Test cricket..."). Do not
# write record content in French again.

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Holders that are teams, duos, institutions, countries or have no single named holder —
# no meaningful single portrait to fetch from Wikipedia.
NO_IMAGE_HOLDERS = {
    "John Isner & Nicolas Mahut",
    "Los Angeles Lakers",
    "Huaso (ridden by Alberto Larraguibel)",
    "Birgit Fischer & Lisa Carrington",
    "AC Milan",
    "New York Yacht Club",
    "Jamaica (Bolt, Blake, Carter, Frater)",
    "India",
    "Ivan Nikolić & Goran Arsović",
    "Real Madrid",
    "South Korea (women's team)",
    "Indonesia",
    "Italy & Argentina",
}

# Overrides where the holder name doesn't map cleanly to its Wikipedia article title.
WIKI_EN = {
    "Armand \"Mondo\" Duplantis": "Armand Duplantis",
    "Hakuho Sho": "Hakuho",
}

records = [
    {"n": "The first official marathon under two hours", "sp": "Athletics (marathon)", "hd": "Sabastian Sawe", "cc": "KE", "yr": "2026",
     "fa": "1:59:30 at the London Marathon, becoming the first runner to break the two-hour barrier in an official record-eligible race. He improved on Kelvin Kiptum's previous record by more than a minute."},

    {"n": "The fastest marathon ever run by a woman", "sp": "Athletics (marathon)", "hd": "Ruth Chepngetich", "cc": "KE", "yr": "2024",
     "fa": "2:09:56 in Chicago, in a mixed-gender race, still the fastest performance ever recorded by a woman in any category."},

    {"n": "The 100m world record", "sp": "Athletics (sprint)", "hd": "Usain Bolt", "cc": "JM", "yr": "2009",
     "fa": "9.58 seconds at the Berlin World Championships, a time nobody has come within two tenths of a second of in over fifteen years."},

    {"n": "The fastest serve ever recorded in tennis", "sp": "Tennis", "hd": "Sam Groth", "cc": "AU", "yr": "2012",
     "fa": "263.4 km/h at a Challenger tournament in Busan. It remains the fastest ever timed, even though the ATP doesn't recognize it as the official tour record, since Challenger-level radars aren't held to the same calibration standards."},

    {"n": "The longest tennis match in history", "sp": "Tennis", "hd": "John Isner & Nicolas Mahut", "cc": None, "yr": "2010",
     "fa": "11 hours and 5 minutes of play at Wimbledon, spread across three days, ending 70-68 in the 5th set. This record can no longer be matched: Wimbledon has since introduced a tiebreak at 12-12 in deciding sets."},

    {"n": "The longest ski jump ever recorded", "sp": "Ski jumping", "hd": "Domen Prevc", "cc": "SI", "yr": "2025",
     "fa": "254.5 meters at Planica, improving by one meter on Austrian Stefan Kraft's eight-year-old record."},

    {"n": "The youngest Formula 1 world champion", "sp": "Formula 1", "hd": "Sebastian Vettel", "cc": "DE", "yr": "2010",
     "fa": "23 years old when he won his first title, clinched on the very last race of the season after finishing ahead of three other drivers still in contention for the championship that day."},

    {"n": "The only perfect professional heavyweight boxing career", "sp": "Boxing", "hd": "Rocky Marciano", "cc": "US", "yr": "1956",
     "fa": "49 wins in 49 fights at retirement, the only heavyweight world champion to never suffer a defeat."},

    {"n": "The heaviest total ever lifted in Olympic weightlifting", "sp": "Weightlifting", "hd": "Lasha Talakhadze", "cc": "GE", "yr": "2021",
     "fa": "488 kg combined across the snatch and clean and jerk at the Tokyo Games, improving his own world record in the middle of competition."},

    {"n": "The most home runs in a single baseball season", "sp": "Baseball", "hd": "Barry Bonds", "cc": "US", "yr": "2001",
     "fa": "73 home runs with the San Francisco Giants, a record that remains controversial due to doping suspicions that were never fully resolved."},

    {"n": "The men's 100m freestyle world record", "sp": "Swimming", "hd": "Pan Zhanle", "cc": "CN", "yr": "2024",
     "fa": "46.40 seconds set at the Paris Games, shattering a record that had seemed untouchable since full-body swimsuits were banned in 2010."},

    {"n": "The longest winning streak in NBA history", "sp": "Basketball", "hd": "Los Angeles Lakers", "cc": "US", "yr": "1972",
     "fa": "33 consecutive wins during the 1971-72 season, a streak that lasted more than two months without a single loss and has never been approached since."},

    {"n": "The track cycling Hour Record", "sp": "Cycling", "hd": "Filippo Ganna", "cc": "IT", "yr": "2022",
     "fa": "56.792 km covered in one hour at the Grenchen velodrome, the longest distance ever covered in this legendary event."},

    {"n": "The pole vault world record", "sp": "Athletics (pole vault)", "hd": "Armand \"Mondo\" Duplantis", "cc": "SE", "yr": "2026",
     "fa": "6.31 meters cleared in Sweden, the 15th time he has broken his own record since 2020, usually improving it by a single centimeter each time."},

    {"n": "The high jump world record", "sp": "Athletics (high jump)", "hd": "Javier Sotomayor", "cc": "CU", "yr": "1993",
     "fa": "2.45 meters cleared in Salamanca, the oldest standing record in men's athletics, unbeaten for over 30 years."},

    {"n": "The highest individual score in Test cricket history", "sp": "Cricket", "hd": "Brian Lara", "cc": "TT", "yr": "2004",
     "fa": "400 runs scored without being dismissed against England, batting for nearly three days. He remains the only player ever to pass the symbolic 400 mark in Test cricket history."},

    {"n": "The most goals scored in a calendar year in football", "sp": "Football", "hd": "Lionel Messi", "cc": "AR", "yr": "2012",
     "fa": "91 goals scored for FC Barcelona and the Argentina national team, a total officially recognized by the International Federation of Football History and Statistics as the modern-era record."},

    {"n": "The most decorated Olympian in history", "sp": "Swimming", "hd": "Michael Phelps", "cc": "US", "yr": "2016",
     "fa": "28 Olympic medals in total across five Games, including 23 gold. No other athlete, in any sport, has ever come close to this total."},

    {"n": "The most points scored in a single NBA game", "sp": "Basketball", "hd": "Wilt Chamberlain", "cc": "US", "yr": "1962",
     "fa": "100 points scored in a single game against the New York Knicks, an individual feat never matched in over 60 years."},

    {"n": "The lowest 72-hole score in a men's major golf championship", "sp": "Golf", "hd": "Xander Schauffele", "cc": "US", "yr": "2024",
     "fa": "263 strokes (21 under par) at the PGA Championship at Valhalla, the best total ever recorded across the four men's major championships."},

    {"n": "The most rushing yards in a single NFL season", "sp": "American football", "hd": "Eric Dickerson", "cc": "US", "yr": "1984",
     "fa": "2,105 rushing yards in a single regular season, a record that has stood for over 40 years despite the game's evolution toward increasingly pass-heavy offenses."},

    {"n": "The 500m speed skating world record", "sp": "Speed skating", "hd": "Pavel Kulizhnikov", "cc": "RU", "yr": "2019",
     "fa": "33.61 seconds set in Salt Lake City, a high-altitude track where thinner air means less resistance, making it the go-to venue for speed skating records."},

    {"n": "The fastest human being on skis", "sp": "Speed skiing", "hd": "Simon Billy", "cc": "FR", "yr": "2023",
     "fa": "255.5 km/h reached in a straight line, a discipline distinct from classic alpine skiing where skiers aim purely for maximum speed on a dedicated slope, with no gates to navigate."},

    {"n": "The youngest world chess champion in history", "sp": "Chess", "hd": "Gukesh Dommaraju", "cc": "IN", "yr": "2024",
     "fa": "18 years old when he was crowned against Ding Liren, breaking the record for youngest champion held by Garry Kasparov since 1985, when he was crowned at 22."},

    {"n": "The highest break ever made in competitive snooker", "sp": "Snooker", "hd": "Ronnie O'Sullivan", "cc": "GB", "yr": "2026",
     "fa": "153 points scored in a single visit to the table at the World Open, more than the theoretical maximum of 147 usually considered the absolute limit, made possible by a rare free-ball situation."},

    {"n": "The most career passing yards in NFL history", "sp": "American football", "hd": "Tom Brady", "cc": "US", "yr": "2022",
     "fa": "89,214 passing yards across a 23-season career, on top of the record for career touchdown passes (738); no other quarterback has come close to this longevity at the highest level."},

    {"n": "The fastest smash ever measured in badminton", "sp": "Badminton", "hd": "Satwiksairaj Rankireddy", "cc": "IN", "yr": "2023",
     "fa": "565 km/h measured under laboratory conditions at manufacturer Yonex's factory in Japan, far above the speed of any tennis serve or volleyball spike."},

    {"n": "The most goals scored in a single NHL season", "sp": "Ice hockey", "hd": "Wayne Gretzky", "cc": "CA", "yr": "1982",
     "fa": "92 goals scored during the 1981-82 season, a total that has remained out of reach for over 40 years despite the efforts of the best scorers of every generation."},

    {"n": "The most career goals in NHL history", "sp": "Ice hockey", "hd": "Alexander Ovechkin", "cc": "RU", "yr": "2025",
     "fa": "895th career goal scored on April 6, 2025, surpassing a record Wayne Gretzky had held for 31 years. Both players reached that total in exactly the same number of games: 1,487."},

    {"n": "The first nine-dart finish at a World Championship", "sp": "Darts", "hd": "Paul Lim", "cc": "US", "yr": "1990",
     "fa": "Nine darts thrown to clear 501 points, the perfect game in darts, achieved for the first time at a World Championship against Ireland's Jack McKenna."},

    {"n": "The most Tour de France overall wins", "sp": "Cycling", "hd": "Tadej Pogačar", "cc": "SI", "yr": "2026",
     "fa": "5th overall victory in 2026, joining an exclusive club that already includes Jacques Anquetil, Eddy Merckx, Bernard Hinault, and Miguel Indurain, now all tied at five titles each."},

    {"n": "The 400m world record", "sp": "Athletics (sprint)", "hd": "Wayde van Niekerk", "cc": "ZA", "yr": "2016",
     "fa": "43.03 seconds run at the Rio Games, from lane 8, where he couldn't see any of his rivals for the entire race."},

    {"n": "The most Olympic gold medals won by a gymnast", "sp": "Gymnastics", "hd": "Larisa Latynina", "cc": "UA", "yr": "1964",
     "fa": "9 Olympic gold medals collected between 1956 and 1964, a record that has withstood every generation of gymnasts since, including Simone Biles."},

    {"n": "The most premier-class wins in motorcycle Grand Prix racing", "sp": "Motorcycle racing (MotoGP)", "hd": "Valentino Rossi", "cc": "IT", "yr": "2026",
     "fa": "89 wins in the premier class (500cc, then MotoGP) over a career spanning more than 20 years, a total that even Marc Marquez, second on the all-time list, has still not managed to reach."},

    {"n": "The fastest perfect game in bowling history", "sp": "Bowling", "hd": "Ben Ketola", "cc": "US", "yr": "2017",
     "fa": "A perfect 300 score rolled in under 90 seconds, each ball thrown the moment the previous one finished, a pace considered nearly impossible to sustain without a single aiming mistake."},

    {"n": "The hammer throw world record", "sp": "Athletics (throwing)", "hd": "Yuriy Sedykh", "cc": "RU", "yr": "1986",
     "fa": "86.74 meters thrown in Stuttgart, the oldest men's world record still standing in athletics, set nearly forty years ago back in the Soviet era."},

    {"n": "The 800m world record", "sp": "Athletics (middle distance)", "hd": "David Rudisha", "cc": "KE", "yr": "2012",
     "fa": "1:40.91 run with perfect pacing at the London Games, where he ran the first and second laps at almost exactly the same speed, a tactical feat considered unachievable over this distance."},

    {"n": "The most British Open squash titles", "sp": "Squash", "hd": "Jahangir Khan", "cc": "PK", "yr": "1991",
     "fa": "10 consecutive titles won between 1982 and 1991, during a period when he went unbeaten in official competition for more than five years, one of the longest individual unbeaten streaks in any sport."},

    {"n": "The biggest wave ever surfed", "sp": "Surfing", "hd": "Sebastian Steudtner", "cc": "DE", "yr": "2020",
     "fa": "26.21 meters high at Nazaré, Portugal, a spot known for an underwater canyon that amplifies Atlantic swells into record-breaking walls of water every winter."},

    {"n": "The most goals scored in Olympic water polo", "sp": "Water polo", "hd": "Manuel Estiarte", "cc": "ES", "yr": "1996",
     "fa": "127 goals scored across six Olympic appearances between 1980 and 1996, exceptional longevity for such a physically demanding sport played in near-constant immersion."},

    {"n": "The first 1080 landed on a vert ramp in skateboarding", "sp": "Skateboarding", "hd": "Gui Khury", "cc": "BR", "yr": "2020",
     "fa": "Three full airborne rotations at just 11 years old, breaking Tony Hawk's record, who needed twelve attempts to land 900 degrees, one rotation less, back in 1999."},

    {"n": "The most decorated Olympic fencer in history", "sp": "Fencing", "hd": "Edoardo Mangiarotti", "cc": "IT", "yr": "1960",
     "fa": "13 Olympic medals in total (6 gold, 5 silver, 2 bronze) collected between 1936 and 1960, a career spanning more than two decades despite the Games being interrupted by World War II."},

    {"n": "The most individual world titles won in judo", "sp": "Judo", "hd": "Teddy Riner", "cc": "FR", "yr": "2023",
     "fa": "12 world titles collected between 2009 and 2023, nine in his weight category and two in the open category, a record no other judoka in history has ever come close to."},

    {"n": "The highest air ever landed in BMX", "sp": "BMX", "hd": "Mat Hoffman", "cc": "US", "yr": "2001",
     "fa": "8.07 meters high off a 7.31-meter ramp, with speed built up by being towed by a motorcycle to reach velocity impossible to generate by pedaling alone."},

    {"n": "The highest speed ever recorded in luge", "sp": "Luge", "hd": "Felix Loch", "cc": "DE", "yr": "2009",
     "fa": "153.98 km/h reached on the Whistler track in Canada, lying on a sled mere centimeters above the ice, with no braking system at all before the finish line."},

    {"n": "The highest jump ever cleared by a horse in official competition", "sp": "Equestrian (show jumping)", "hd": "Huaso (ridden by Alberto Larraguibel)", "cc": "CL", "yr": "1949",
     "fa": "2.47 meters cleared in Chile, a record that has stood unbeaten for over 75 years and is officially recognized by the International Equestrian Federation as the highest ever ratified."},

    {"n": "The most Olympic gold medals in canoe/kayak", "sp": "Canoe/kayak", "hd": "Birgit Fischer & Lisa Carrington", "cc": None, "yr": "2024",
     "fa": "8 Olympic titles each, a record shared since 2024 between Germany's Birgit Fischer, retired for 20 years, and New Zealand's Lisa Carrington, who matched her in Paris."},

    {"n": "The highest cliff jump ever performed", "sp": "Cliff diving", "hd": "Laso Schaller", "cc": "CH", "yr": "2015",
     "fa": "58.5 meters off a waterfall in Switzerland. Technically a jump, not a dive: unlike a classic dive, the feet enter the water first, with no 180-degree rotation."},

    {"n": "The longest unbeaten streak in Italian Serie A", "sp": "Football", "hd": "AC Milan", "cc": "IT", "yr": "1993",
     "fa": "58 matches unbeaten between May 1991 and March 1993 under manager Fabio Capello, a dominant run that earned the team the nickname \"The Invincibles.\""},

    {"n": "The most championship titles in sumo history", "sp": "Sumo", "hd": "Hakuho Sho", "cc": "MN", "yr": "2021",
     "fa": "45 top-division championship titles between 2006 and 2021, including 16 tournaments won without a single loss, a total that surpasses the previous record held by legend Taiho by 13."},

    {"n": "The longest field goal in NFL history", "sp": "American football", "hd": "Cam Little", "cc": "US", "yr": "2025",
     "fa": "68 yards, over 62 meters, kicked in a regular-season game against the Raiders. He also holds the second-longest, with a 67-yard kick the same season."},

    {"n": "The most career three-pointers made in NBA history", "sp": "Basketball", "hd": "Stephen Curry", "cc": "US", "yr": "2021",
     "fa": "Record broken on December 14, 2021, passing Ray Allen, who was in attendance and came onto the court to congratulate him as play stopped. Curry has kept extending his own total every season since."},

    {"n": "The 3000m steeplechase world record", "sp": "Athletics (steeplechase)", "hd": "Lamecha Girma", "cc": "ET", "yr": "2023",
     "fa": "7:52.11 clearing 28 hurdles and 7 water jumps, the most technical event in athletics, where endurance must contend with an obstacle on every lap."},

    {"n": "The longest unbeaten streak in sports history", "sp": "Sailing", "hd": "New York Yacht Club", "cc": "US", "yr": "1983",
     "fa": "25 consecutive successful defenses of the America's Cup between 1851 and 1983, 132 years without ever losing the trophy, one of the longest dominant streaks ever recorded in any sport."},

    {"n": "The highest speed ever reached in drag racing", "sp": "Drag racing", "hd": "Brittany Force", "cc": "US", "yr": "2025",
     "fa": "552.85 km/h (343.51 mph) covered over 305 meters of track in under 4 seconds, in a Top Fuel dragster powered by an engine that burns more fuel in one race than a regular car does in several years."},

    {"n": "The women's 100m butterfly world record", "sp": "Swimming", "hd": "Gretchen Walsh", "cc": "US", "yr": "2026",
     "fa": "54.33 seconds set in Florida, the fourth time she has broken her own record since June 2024. She alone holds the 13 fastest times ever recorded over this distance."},

    {"n": "The most decorated Olympic biathlete in history", "sp": "Biathlon", "hd": "Ole Einar Bjørndalen", "cc": "NO", "yr": "2014",
     "fa": "13 Olympic medals in total, including 8 gold, collected over an 18-year career. At the 2002 Salt Lake City Games, he won all three individual events plus the relay, a quadruple no one has repeated since."},

    {"n": "The highest individual score in ODI cricket history", "sp": "Cricket", "hd": "Rohit Sharma", "cc": "IN", "yr": "2014",
     "fa": "264 runs scored in a single innings against Sri Lanka, off just 173 balls, the only player ever to pass 260 runs in a One Day International."},

    {"n": "The 4x100m relay world record", "sp": "Athletics (relay)", "hd": "Jamaica (Bolt, Blake, Carter, Frater)", "cc": "JM", "yr": "2012",
     "fa": "36.84 seconds run at the London Games with Usain Bolt anchoring, a record even today's best teams haven't come close to in over ten years."},

    {"n": "The most international goals scored in football history", "sp": "Football", "hd": "Cristiano Ronaldo", "cc": "PT", "yr": "2026",
     "fa": "146 goals scored for Portugal, the highest total ever recorded by any national team player in the history of international football."},

    {"n": "The most successful nation in Olympic field hockey", "sp": "Field hockey", "hd": "India", "cc": "IN", "yr": "1980",
     "fa": "8 gold medals won between 1928 and 1980, six of them consecutive between 1928 and 1956, a dominance with no equivalent in the history of Olympic team sports."},

    {"n": "The longest chess game ever played", "sp": "Chess", "hd": "Ivan Nikolić & Goran Arsović", "cc": None, "yr": "1989",
     "fa": "269 moves played in Belgrade over nearly 20 hours, before ending in a draw under the 50-move rule with no capture or pawn move."},

    {"n": "Curling's rarest perfect score", "sp": "Curling", "hd": None, "cc": None, "yr": "2026",
     "fa": "Scoring an \"eight-ender\" (all eight of a team's stones counting in a single end) has an estimated probability of 1 in 120,000 in amateur curling, rarer than a hole-in-one in golf or a perfect game in bowling."},

    {"n": "The most Wimbledon men's singles titles", "sp": "Tennis", "hd": "Roger Federer", "cc": "CH", "yr": "2017",
     "fa": "8 titles won between 2003 and 2017. He is also the only player in any era to have reached the tournament final twelve times."},

    {"n": "The most career pole positions in Formula 1", "sp": "Formula 1", "hd": "Lewis Hamilton", "cc": "GB", "yr": "2021",
     "fa": "105 career pole positions, becoming the first driver to pass the symbolic 100 mark at the 2021 Spanish Grand Prix, having already surpassed Michael Schumacher's record four years earlier."},

    {"n": "The most career triple-doubles in NBA history", "sp": "Basketball", "hd": "Russell Westbrook", "cc": "US", "yr": "2026",
     "fa": "209 triple-doubles at the time of his retirement in August 2026, a record he took from Oscar Robertson in 2021 and one that could well be next to fall, to Nikola Jokić."},

    {"n": "The most Super Bowl titles won by a player", "sp": "American football", "hd": "Tom Brady", "cc": "US", "yr": "2021",
     "fa": "7 championship rings won, six with the New England Patriots and a seventh at age 43 with the Tampa Bay Buccaneers. No other player in history has won more than five."},

    {"n": "The most wickets taken in Test cricket history", "sp": "Cricket", "hd": "Muttiah Muralitharan", "cc": "LK", "yr": "2010",
     "fa": "Exactly 800 wickets, a total reached on the very last ball of his very last career match, against India, a scenario so perfect it feels scripted."},

    {"n": "The most successful club in the Champions League", "sp": "Football", "hd": "Real Madrid", "cc": "ES", "yr": "2024",
     "fa": "15 titles in total, five of them consecutive between 1956 and 1960 during the competition's very first decade, an early dominance no other club has ever matched since."},

    {"n": "The most career home runs in baseball history", "sp": "Baseball", "hd": "Barry Bonds", "cc": "US", "yr": "2007",
     "fa": "762 home runs in total, a record reached on August 7, 2007 by passing Hank Aaron, in a career defined as much by doping suspicions as by the statistics themselves."},

    {"n": "The longest winning streak in tennis (Open Era)", "sp": "Tennis", "hd": "Guillermo Vilas", "cc": "AR", "yr": "1977",
     "fa": "46 consecutive match wins in 1977, the record officially recognized by the ATP. Björn Borg claims even longer streaks during the same period, but they include walkover wins not counted by the ATP."},

    {"n": "The most NBA championships won by a player", "sp": "Basketball", "hd": "Bill Russell", "cc": "US", "yr": "1969",
     "fa": "11 titles won in 13 seasons with the Boston Celtics between 1957 and 1969, eight of them consecutive, a team-sport record that remains completely out of reach in any sport today."},

    {"n": "The most Tour de France stage wins", "sp": "Cycling", "hd": "Mark Cavendish", "cc": "GB", "yr": "2024",
     "fa": "35 stage wins on the tally after the 2024 Tour, surpassing Eddy Merckx's decades-old record of 34."},

    {"n": "The most international goals scored in women's football history", "sp": "Football", "hd": "Christine Sinclair", "cc": "CA", "yr": "2020",
     "fa": "190 goals scored for Canada, a total that even surpasses the men's record across all nations. She broke Abby Wambach's previous record during an Olympic qualifying match won 11-0."},

    {"n": "The most goals scored by a player at a single World Cup", "sp": "Football", "hd": "Just Fontaine", "cc": "FR", "yr": "1958",
     "fa": "13 goals scored in Sweden, more than double the tournament's second-highest scorer. He played the entire competition in boots borrowed from a teammate, since his own didn't fit."},

    {"n": "The longest scoreless streak by a football goalkeeper", "sp": "Football", "hd": "Abel Resino", "cc": "ES", "yr": "1991",
     "fa": "14 matches and 15 minutes without conceding a single goal with Atlético Madrid, the all-time record across all competitions for a goalkeeper."},

    {"n": "The only boxer to be world champion in eight different weight divisions", "sp": "Boxing", "hd": "Manny Pacquiao", "cc": "PH", "yr": "2010",
     "fa": "12 world titles collected between 48 and 70 kg, from flyweight to super welterweight. No other boxer in history has ever been world champion in more than four different divisions."},

    {"n": "The longest unbeaten streak in Olympic team archery", "sp": "Archery", "hd": "South Korea (women's team)", "cc": "KR", "yr": "2024",
     "fa": "Unbeaten since the team event was introduced in 1988, chasing a 10th consecutive title. South Korea alone has amassed 43 Olympic archery medals, 13 more than second-place United States."},

    {"n": "The most career hits in professional baseball", "sp": "Baseball", "hd": "Ichiro Suzuki", "cc": "JP", "yr": "2016",
     "fa": "4,257 hits combined between Japan's NPB and MLB, surpassing Pete Rose's record. He also holds the MLB single-season hits record with 262 in 2004."},

    {"n": "The most successful nation at the Thomas Cup in badminton", "sp": "Badminton", "hd": "Indonesia", "cc": "ID", "yr": "2020",
     "fa": "14 titles won since the men's team competition began in 1948, including two runs of four and five consecutive titles, ahead of China's 12."},

    {"n": "The all-time top scorer in World Cup history", "sp": "Football", "hd": "Kylian Mbappé", "cc": "FR", "yr": "2026",
     "fa": "22 World Cup goals following the 2026 edition, overtaking Lionel Messi (21) in the third-place match. The two players traded the all-time scoring lead several times during the same tournament."},

    {"n": "The 100m breaststroke world record", "sp": "Swimming", "hd": "Adam Peaty", "cc": "GB", "yr": "2019",
     "fa": "56.88 seconds set at the Gwangju World Championships, the only swimmer in history to break the symbolic 57-second barrier over this distance."},

    {"n": "The 100m backstroke world record", "sp": "Swimming", "hd": "Thomas Ceccon", "cc": "IT", "yr": "2022",
     "fa": "51.60 seconds set at the Budapest World Championships, improving on the previous record by more than three tenths of a second in one go, a huge margin at this level of competition."},

    {"n": "The most Grand Slam titles across all categories combined", "sp": "Tennis", "hd": "Margaret Court", "cc": "AU", "yr": "1975",
     "fa": "64 titles won between 1960 and 1975, split between 24 singles titles, 19 women's doubles, and 21 mixed doubles, a total no player has ever come close to since."},

    {"n": "The speed climbing world record", "sp": "Sport climbing", "hd": "Zhao Yicheng", "cc": "CN", "yr": "2026",
     "fa": "4.54 seconds to climb a 15-meter wall, set at just 16 years old at a competition in China, only weeks after already breaking his own previous record."},

    {"n": "The most Winter Olympic gold medals won by a cross-country skier", "sp": "Cross-country skiing", "hd": "Johannes Høsflot Klæbo", "cc": "NO", "yr": "2026",
     "fa": "11 Olympic gold medals in total after the Milan-Cortina Games, where he won gold in all six events he entered. Only swimmer Michael Phelps, the only athlete in any sport to do better, stands ahead of him."},

    {"n": "The single sculls rowing world record (2000m)", "sp": "Rowing", "hd": "Simon van Dorp", "cc": "NL", "yr": "2026",
     "fa": "5 minutes and 33.4 seconds, becoming the first rower to break the 5:34 barrier, just weeks after the record had already been broken by Olympic champion Oliver Zeidler."},

    {"n": "The fastest smash ever measured in table tennis", "sp": "Table tennis", "hd": "Łukasz Budner", "cc": "PL", "yr": "2016",
     "fa": "116 km/h recorded at a championship in Poland, a speed almost impossible to follow with the naked eye on a table less than three meters long."},

    {"n": "The highest score on a 1440 round in compound archery", "sp": "Archery", "hd": "Mike Schloesser", "cc": "NL", "yr": "2026",
     "fa": "1,421 points out of a possible 1,440, scored in the Netherlands over a 144-arrow competition shot at distances ranging from 30 to 90 meters."},

    {"n": "The most Olympic gold medals won by a wrestler", "sp": "Wrestling", "hd": "Mijaín López", "cc": "CU", "yr": "2024",
     "fa": "5 consecutive gold medals won between 2008 and 2024, across two different weight classes, a 16-year individual Olympic reign no other wrestler has ever matched."},

    {"n": "The longest set in Olympic volleyball history", "sp": "Volleyball", "hd": "Italy & Argentina", "cc": None, "yr": "2000",
     "fa": "Italy won 40-38 against Argentina in Sydney, a set so long it remains the all-time benchmark nearly 25 years later, with advantage-set rules since tightened in several competitions."},
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
    skipped = 0
    for i, s in enumerate(records):
        holder = s.get("hd")
        if holder is None or holder in NO_IMAGE_HOLDERS:
            s["im"] = None
            skipped += 1
            sys.stdout.buffer.write(f"  [{i+1:2}/{total}] -- (no image target) {s['n'][:50]}\n".encode("utf-8"))
            continue
        title = WIKI_EN.get(holder, holder)
        img = wiki_img(title)
        s["im"] = img
        if img:
            found += 1
        status = "ok" if img else "xx"
        sys.stdout.buffer.write(f"  [{i+1:2}/{total}] {status} {holder}\n".encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)

    out = Path("assets/sport/sport_records.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(records, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    sys.stdout.buffer.write(
        f"\nDone: {found}/{total - skipped} images found, {skipped} skipped (no single holder) -- {total} records total.\n".encode("utf-8")
    )


if __name__ == "__main__":
    main()
