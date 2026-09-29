import json
from pathlib import Path

# n=rivalry title ("X vs Y"), sp=sport, cc=ISO2 country code(s) ("/"-joined for dual
# nationality, single code if both from the same country), yr=years the rivalry was
# active, ctx=context, fa=fact/highlight
#
# Content is written in ENGLISH (source language for the app's translation pipeline, see
# content_loader.dart). Text-only category, no images: ImageContentCard only supports a
# single portrait, which doesn't fit a two-person duel, so this data has no "im" field and
# the app falls back to the standard icon-based ContentCard automatically.

records = [
    {"n": 'Federer vs Nadal', "sp": 'Tennis', "cc": 'CH/ES', "yr": '2004-2019',
     "ctx": "Federer's elegant all-court game and Nadal's relentless heavy topspin from the baseline made them stylistic opposites, and for over a decade their meetings, especially in Grand Slam finals, defined the debate over who was tennis's greatest player.",
     "fa": 'Nadal led their head-to-head 24-16 across 40 matches, but their most celebrated encounter was the 2008 Wimbledon final, a nearly five-hour, rain-interrupted match widely regarded as the greatest ever played.'},

    {"n": 'Ali vs Frazier', "sp": 'Boxing', "cc": 'US', "yr": '1971-1975',
     "ctx": 'Ali, stripped of his title and banned for three years after refusing the Vietnam War draft, returned to face Frazier, the reigning champion who had kept the title warm in his absence, and their fights carried heavy political and racial weight far beyond boxing.',
     "fa": "The trilogy split 2-1 in Ali's favor, ending with the Thrilla in Manila in 1975, a fight so brutal that both men later said it felt closer to death than any other bout of their careers."},

    {"n": 'Messi vs Ronaldo', "sp": 'Football', "cc": 'AR/PT', "yr": '2009-2018',
     "ctx": 'For nearly a decade, individual awards in football and its biggest club rivalry, El Clasico between Barcelona and Real Madrid, revolved almost entirely around these two players, splitting fans worldwide into two camps.',
     "fa": "They faced off 36 times, with Messi winning 16 matches to Ronaldo's 11 and 9 draws; Messi scored 22 goals in these meetings to Ronaldo's 21, one of the closest individual scoring rivalries in football history."},

    {"n": 'Bird vs Magic', "sp": 'Basketball', "cc": 'US', "yr": '1979-1992',
     "ctx": "Introduced to each other in the 1979 NCAA final, Bird and Johnson arrived in the NBA the same year and were cast as opposites: the workmanlike small-town forward against the flashy Los Angeles point guard, reviving the entire league's popularity through their teams' rivalry.",
     "fa": 'Their NCAA final drew 40 million television viewers, still a record for a college basketball game; in the NBA they met 37 times, with Bird winning 3 championships and Magic 5.'},

    {"n": 'Senna vs Prost', "sp": 'Formula 1', "cc": 'BR/FR', "yr": '1988-1993',
     "ctx": "Teammates turned bitter rivals at McLaren, Senna's raw aggression and Prost's calculated precision clashed both on track and in the team's internal politics, turning what should have been a title-winning partnership into one of sport's most personal feuds.",
     "fa": 'Their world championships were decided by collisions between the two of them in consecutive years, at the same corner of the same circuit: Suzuka in 1989, which handed the title to Prost, and Suzuka again in 1990, which handed it to Senna.'},

    {"n": 'Lin Dan vs Lee Chong Wei', "sp": 'Badminton', "cc": 'CN/MY', "yr": '2004-2018',
     "ctx": 'For over a decade the two men met at nearly every major final, and Lee became widely regarded as one of the greatest players never to win an Olympic gold, largely because Lin Dan kept standing in his way.',
     "fa": 'They played 40 times, with Lin Dan winning 28, including both of their Olympic finals, in 2008 and 2012, and both their World Championship finals, in 2011 and 2013.'},

    {"n": 'Kasparov vs Karpov', "sp": 'Chess', "cc": 'RU', "yr": '1984-1990',
     "ctx": 'Their first World Championship match in 1984 was halted without a winner after 48 games and nearly six months of play, a decision so controversial it remains debated in chess circles to this day.',
     "fa": 'Between 1984 and 1990 they played five consecutive World Championship matches, a record that still stands, with Kasparov eventually winning the rivalry and becoming, at 22, the youngest world champion in chess history.'},

    {"n": 'Coe vs Ovett', "sp": 'Athletics (middle distance)', "cc": 'GB', "yr": '1978-1980',
     "ctx": 'British rivals who traded world records at 800m and 1500m throughout the late 1970s without ever racing each other directly, they finally met head-to-head at a major championship for the first time at the 1980 Moscow Olympics.',
     "fa": "At Moscow 1980, each won gold in what was considered the other's stronger event: Ovett won the 800m, Coe's specialty, and Coe won the 1500m, Ovett's specialty, a symmetry considered one of athletics' strangest outcomes."},

    {"n": 'Gebrselassie vs Tergat', "sp": 'Athletics (long distance)', "cc": 'ET/KE', "yr": '1996-2000',
     "ctx": "Their duels became a proxy for the wider distance-running rivalry between Ethiopia and Kenya, with Tergat cast as the stronger front-runner who could never quite get past Gebrselassie's finishing kick.",
     "fa": 'Gebrselassie beat Tergat in the Olympic 10,000m final twice, at Atlanta 1996 and Sydney 2000, winning the second by just 0.09 seconds, one of the closest finishes in Olympic distance-running history.'},

    {"n": 'Rossi vs Marquez', "sp": 'Motorcycle racing (MotoGP)', "cc": 'IT/ES', "yr": '2013-2018',
     "ctx": 'The rivalry between the established Italian veteran and the younger Spanish rider defined a generational shift in MotoGP, and turned openly hostile after a title-deciding collision.',
     "fa": 'At the 2015 Malaysian Grand Prix, Rossi and Marquez collided while fighting for track position; race stewards ruled Rossi had caused the crash and demoted him to the back of the grid for the final race, costing him what would have been a tenth world title.'},

    {"n": 'Fischer vs Spassky', "sp": 'Chess', "cc": 'US/RU', "yr": '1972',
     "ctx": 'Billed as the Match of the Century, their World Championship in Reykjavik became a Cold War proxy battle between an eccentric American challenger and the reigning Soviet champion, ending 24 years of uninterrupted Soviet dominance of the title.',
     "fa": 'Fischer won 12.5 to 8.5 over 21 games, becoming the first American-born world chess champion, despite forfeiting the second game entirely after a dispute over cameras in the playing hall.'},

    {"n": 'Chamberlain vs Russell', "sp": 'Basketball', "cc": 'US', "yr": '1959-1969',
     "ctx": "The era's two dominant centers, the overwhelming individual scorer against the relentless team defender and winner, met so often in the regular season and playoffs that their personal duel became a running storyline of an entire decade of the NBA.",
     "fa": "They faced off 143 times combined in the regular season and playoffs, with Russell's teams winning the majority of those games, including an 8-4 record in their head-to-head playoff series, despite Chamberlain consistently outscoring and out-rebounding him individually."},

    {"n": 'Borg vs McEnroe', "sp": 'Tennis', "cc": 'SE/US', "yr": '1978-1981',
     "ctx": "The ice-cool Swedish baseliner against the volatile, serve-and-volley New Yorker became tennis's defining contrast in temperament, and their five-set 1980 Wimbledon final is still cited as one of the sport's greatest matches.",
     "fa": 'In that 1980 final, McEnroe saved five championship points to win a fourth-set tiebreak 18-16, widely considered the greatest tiebreak ever played, before Borg recovered to win the deciding fifth set 8-6.'},

    {"n": 'Evert vs Navratilova', "sp": 'Tennis', "cc": 'US/CZ', "yr": '1973-1988',
     "ctx": "The contrast between Evert's disciplined baseline consistency and Navratilova's athletic serve-and-volley game, sharpened by Navratilova's defection from Czechoslovakia to the United States in 1975, produced what is still considered the greatest rivalry in women's tennis.",
     "fa": 'They played 80 matches over 15 years, 60 of them finals, with Navratilova leading the overall head-to-head 43-37; Evert led every year from 1973 to 1978, then Navratilova took over for the rest of the rivalry.'},

    {"n": 'Hunt vs Lauda', "sp": 'Formula 1', "cc": 'GB/AT', "yr": '1976',
     "ctx": "Hunt's carefree playboy image against Lauda's clinical precision defined a single dramatic season, made more intense after Lauda nearly died in a fiery crash at the Nurburgring and returned to racing just six weeks later, still bleeding from his injuries.",
     "fa": 'At the rain-soaked season-ending Japanese Grand Prix, Lauda withdrew after two laps, saying his life mattered more than the title, handing Hunt the championship by a single point.'},

    {"n": 'Nicklaus vs Palmer', "sp": 'Golf', "cc": 'US', "yr": '1962-1970s',
     "ctx": "The young, powerfully built Nicklaus arrived as the challenger to Palmer, golf's most popular star and leader of a fan army nicknamed Arnie's Army, and their generational handover played out across two decades of major championships.",
     "fa": "Their rivalry began at the 1962 US Open at Oakmont, Palmer's home region, where the 22 year old Nicklaus beat the local favorite in an 18-hole playoff for his first professional win."},

    {"n": 'Nicklaus vs Watson', "sp": 'Golf', "cc": 'US', "yr": '1977',
     "ctx": "By 1977, Watson had already beaten the established Nicklaus at the Masters that same year, and their final-round duel at the Open Championship in Turnberry became known as the Duel in the Sun for the pair's near-identical scores under blazing weather.",
     "fa": "Tied entering the final round, both players shot 65 the day before and traded birdies until Watson's closing birdie beat Nicklaus's own brilliant recovery shot by a single stroke; the two walked off the final green arm in arm."},

    {"n": 'Lewis vs Johnson', "sp": 'Athletics (sprint)', "cc": 'US/CA', "yr": '1987-1988',
     "ctx": 'Their rivalry culminated in the 100m final at the 1988 Seoul Olympics, one of the most anticipated races in athletics history, where Johnson had beaten the reigning champion Lewis with a new world record.',
     "fa": 'Johnson was stripped of his gold medal and world record three days later after testing positive for a banned steroid; Lewis was elevated to the title, becoming the first man to successfully defend an Olympic 100m crown.'},

    {"n": 'Bolt vs Gatlin', "sp": 'Athletics (sprint)', "cc": 'JM/US', "yr": '2004-2017',
     "ctx": "Gatlin, a former Olympic champion who served a four-year doping ban, became the sport's most persistent villain to Bolt's clean-cut global superstar, and their careers kept intersecting at major finals for over a decade.",
     "fa": "At the 2017 World Championships, in what was billed as Bolt's final individual race, Gatlin upset him for gold, the only time in ten meetings between them that Bolt lost a major 100m final; Gatlin then knelt in front of Bolt in a gesture of respect."},

    {"n": 'Bradman vs Larwood', "sp": 'Cricket', "cc": 'AU/GB', "yr": '1932-1933',
     "ctx": "England, desperate to blunt Bradman's overwhelming batting dominance, had fast bowler Larwood target the body with short-pitched deliveries backed by a packed leg-side field, a tactic that came to be known as Bodyline and nearly caused a diplomatic incident between the two countries.",
     "fa": "The tactic worked: Bradman's series average dropped to 56.57, still remarkable by any normal standard but far below his career average of 99.94; cricket's laws were rewritten afterward to ban the tactic, and Larwood was never picked for England again."},

    {"n": 'Villeneuve vs Pironi', "sp": 'Formula 1', "cc": 'CA/FR', "yr": '1982',
     "ctx": 'Ferrari teammates who had raced as a united front, their partnership collapsed at the 1982 San Marino Grand Prix when Pironi passed Villeneuve for the win in the closing laps, defying what Villeneuve believed was a team order to hold position.',
     "fa": "Villeneuve refused to speak to Pironi again and was killed two weeks later while trying to beat Pironi's qualifying time at the next race in Belgium; Pironi's own career ended later that season in a career-ending crash."},

    {"n": 'Anquetil vs Poulidor', "sp": 'Cycling', "cc": 'FR', "yr": '1962-1966',
     "ctx": "France split into two camps, the cool and calculating Anquetil against the earnest, unlucky Poulidor, who despite being one of the strongest climbers of his generation never once wore the Tour de France's yellow leader's jersey.",
     "fa": 'On the Puy de Dome climb during the 1964 Tour, the two rode elbow to elbow up the mountain in front of half a million spectators; Poulidor gained time but not enough, finishing the Tour 55 seconds behind Anquetil, who won his record fifth title.'},

    {"n": 'LeMond vs Hinault', "sp": 'Cycling', "cc": 'US/FR', "yr": '1985-1986',
     "ctx": "Hinault had publicly promised to ride in support of his young American teammate LeMond at the 1986 Tour de France after LeMond helped him win the year before, but Hinault's repeated attacks during the race cast doubt on that promise and split their own team.",
     "fa": 'LeMond held on to beat his teammate by 3 minutes 10 seconds, becoming the first non-European winner of the Tour de France in its history.'},

    {"n": 'DiMaggio vs Williams', "sp": 'Baseball', "cc": 'US', "yr": '1941',
     "ctx": "The stoic, all-around Yankees center fielder and the outspoken Red Sox slugger, sworn rivals through their teams' historic rivalry, both had career-defining seasons in 1941 that are still used as the benchmark for greatness nearly a century later.",
     "fa": 'DiMaggio hit safely in 56 consecutive games while Williams batted .406, the last time any player has hit over .400 in a season; DiMaggio won the MVP award that year largely because his Yankees won the pennant.'},

    {"n": 'Phelps vs Lochte', "sp": 'Swimming', "cc": 'US', "yr": '2004-2016',
     "ctx": 'American teammates and training rivals for over a decade, their friendly but intense rivalry in the individual medley events pushed both to become the two most decorated Olympic swimmers in history.',
     "fa": 'Phelps won four of their five head-to-head Olympic meetings; the only exception came in the 2012 London 400m individual medley, where Lochte took gold and a stunned Phelps finished fourth.'},

    {"n": 'Slater vs Irons', "sp": 'Surfing', "cc": 'US', "yr": '2002-2006',
     "ctx": "Irons broke through to win his first world title in 2002 while a six-time champion Slater was temporarily away from the tour, and Slater's competitive return the following year turned their rivalry into the most intense world title race professional surfing had seen.",
     "fa": 'Irons won three straight world titles from 2002 to 2004, but Slater reclaimed the crown in 2005 and 2006, even after losing the decisive Pipe Masters final to Irons in 2006 by enough of a margin elsewhere on tour to still take the overall title.'},

    {"n": 'Davis vs Taylor', "sp": 'Snooker', "cc": 'GB/IE', "yr": '1985',
     "ctx": "Defending champion Davis appeared to be cruising after leading 8-0 early in their 1985 World Championship final, only for the underdog Taylor to claw back frame after frame in one of the most dramatic comebacks in the sport's history.",
     "fa": "The match went to a deciding frame that came down to the final black ball, which Taylor potted after Davis missed his own attempt; watched live by 18.5 million people, it remains snooker's most-watched broadcast ever."},

    {"n": 'Taylor vs Bristow', "sp": 'Darts', "cc": 'GB', "yr": '1990',
     "ctx": 'Five-time world champion Bristow discovered the unknown Taylor playing county darts, personally mentored him, and even sponsored his early career, only to face his own student in the 1990 World Championship final.',
     "fa": 'Taylor beat his mentor 6-1 to win the first of his sixteen world titles; Bristow, true to the tough-love relationship between them, reportedly refused to praise Taylor unless he had actually won a tournament.'},

    {"n": 'Gretzky vs Lemieux', "sp": 'Ice hockey', "cc": 'CA', "yr": '1984-1997',
     "ctx": "Gretzky, already established as the league's most prolific scorer, found his only true statistical rival in Lemieux, whose scoring pace per game eventually surpassed Gretzky's own, despite a career cut short by injuries and cancer treatment.",
     "fa": "Gretzky led the NHL in scoring for 10 seasons to Lemieux's 6, but Lemieux's 1.883 points per game remains the highest in league history, edging out Gretzky's 1.921 career rate only when adjusted for games actually played."},

    {"n": 'Crosby vs Ovechkin', "sp": 'Ice hockey', "cc": 'CA/RU', "yr": '2005-',
     "ctx": "Selected first overall in back-to-back drafts and debuting the same season, the disciplined two-way center and the explosive power forward became the defining rivalry of the NHL's modern era, renewed dozens of times a season for two decades.",
     "fa": "They have faced off 65 times in the regular season since their 2005 debuts; Ovechkin passed Wayne Gretzky's all-time goals record in April 2025, a mark Crosby himself called incredible."},

    {"n": 'Biles vs Andrade', "sp": 'Gymnastics', "cc": 'US/BR', "yr": '2016-2024',
     "ctx": 'Andrade emerged as the only gymnast able to consistently challenge the otherwise dominant Biles, and the two developed an unusually warm friendship even as their rivalry intensified at the very top of the sport.',
     "fa": 'At the 2024 Paris Olympics, Andrade beat Biles for floor exercise gold by just 0.033 points, the first time Biles had lost a major floor final since 2015; Biles and bronze medalist Jordan Chiles bowed to Andrade on the podium in a widely shared moment of sportsmanship.'},

    {"n": 'Witt vs Thomas', "sp": 'Figure skating', "cc": 'DE/US', "yr": '1988',
     "ctx": 'Both women skated to the same Bizet opera, Carmen, in their long programs at the 1988 Calgary Olympics, and the coincidence turned their competition into a media-fed showdown nicknamed the Battle of the Carmens.',
     "fa": 'Witt won gold to defend her 1984 title despite an underwhelming free skate, while Thomas fell short of her own high expectations to take bronze, becoming the first Black athlete to medal at a Winter Olympics.'},

    {"n": 'Harding vs Kerrigan', "sp": 'Figure skating', "cc": 'US', "yr": '1994',
     "ctx": 'Weeks before the 1994 Winter Olympics, reigning US champion Kerrigan was attacked and struck on the leg by a man hired by associates of her rival Harding, in one of the most notorious scandals in sports history.',
     "fa": 'Kerrigan recovered in time to compete and won Olympic silver, while Harding finished off the podium; she was later banned for life from US Figure Skating after admitting she learned of the plot after the fact and failed to report it.'},

    {"n": 'Khabib vs McGregor', "sp": 'Mixed martial arts', "cc": 'RU/IE', "yr": '2018',
     "ctx": "Months of personal insults from McGregor, including remarks about Khabib's religion, nationality, and family, built one of MMA's most hostile rivalries ahead of their lightweight title fight at UFC 229.",
     "fa": "Khabib submitted McGregor in the fourth round, then immediately jumped the cage to attack McGregor's team, setting off a mass brawl that spilled both inside and outside the octagon."},

    {"n": 'Asashoryu vs Hakuho', "sp": 'Sumo', "cc": 'MN', "yr": '2005-2010',
     "ctx": "Two Mongolian-born wrestlers rose to sumo's highest rank of yokozuna and dominated the traditionally Japanese-led sport together for years, their rivalry marking a historic shift in a discipline steeped in centuries of Japanese tradition.",
     "fa": 'Asashoryu won 25 top-division championships before an abrupt retirement in 2010 following a personal scandal, leaving Hakuho to go on alone and eventually break the all-time record for tournament titles.'},

    {"n": 'Warne vs Tendulkar', "sp": 'Cricket', "cc": 'AU/IN', "yr": '1998',
     "ctx": "Warne was widely considered the finest leg-spin bowler of his generation, and Tendulkar's ability to consistently dismantle his bowling became the sport's ultimate test of a batsman's class.",
     "fa": "During a tri-series in Sharjah in 1998, Tendulkar scored back-to-back centuries against Warne's Australia, hitting Warne for 39 runs in nine overs in one match and 61 runs in ten overs in the next; Warne later joked he had nightmares of Tendulkar dancing down the pitch to hit him for six."},

    {"n": 'Kohli vs Smith', "sp": 'Cricket', "cc": 'IN/AU', "yr": '2014-',
     "ctx": "As the two most dominant batsmen and rival national captains of their generation, Kohli's aggressive intensity and Smith's unconventional technique defined a modern era of Test cricket between India and Australia.",
     "fa": 'A heated moment during a 2017 Test series, when Kohli publicly accused Smith of seeking outside help to decide on a video review, became a defining flashpoint of their rivalry, before the two later described their relationship as one of mutual respect.'},

    {"n": 'Schumacher vs Hill', "sp": 'Formula 1', "cc": 'DE/GB', "yr": '1994',
     "ctx": 'A rookie-turned-champion German driver against a steady British veteran, their tight title battle came down to the final race of the 1994 season, separated by a single point.',
     "fa": "After Schumacher clipped a wall and rejoined the track ahead of Hill, the two collided when Hill attempted to pass; both cars retired, handing Schumacher his first world title in one of Formula 1's most controversial championship deciders."},

    {"n": 'Leonard vs Duran', "sp": 'Boxing', "cc": 'US/PA', "yr": '1980',
     "ctx": 'After Duran had beaten him in a brutal, close decision five months earlier, Leonard rebuilt his tactics entirely for the rematch, taunting and out-boxing Duran instead of trading punches with him.',
     "fa": 'In the eighth round of the rematch, Duran abruptly turned away and quit, reportedly saying No mas, no more, one of the most shocking surrenders in boxing history.'},

    {"n": 'Tyson vs Holyfield', "sp": 'Boxing', "cc": 'US', "yr": '1996-1997',
     "ctx": 'After Holyfield shocked the boxing world by beating the heavily favored Tyson to take his title in 1996, their rematch seven months later carried enormous anticipation and an even bigger payday.',
     "fa": "Enraged mid-fight, Tyson bit off part of Holyfield's ear in the third round; he was disqualified and had his boxing license temporarily revoked over the incident."},
]


def main():
    out = Path("assets/sport/sport_rivalries.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(records, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    print(f"Done: {len(records)} rivalries written.")


if __name__ == "__main__":
    main()
