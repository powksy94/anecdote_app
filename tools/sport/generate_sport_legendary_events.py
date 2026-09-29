import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=event title, sp=sport, pr=protagonist (person; null if team-collective moment with no
# single figure), cc=ISO2 country code, yr=year, fa=fact/highlight, im=imageUrl (only
# fetched for individual named protagonists)
#
# Content is written in ENGLISH (source language for the app's translation pipeline, see
# content_loader.dart).

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Overrides where the protagonist name doesn't map cleanly to its Wikipedia article title.
WIKI_EN = {
    "Jean Van de Velde": "Jean van de Velde (golfer)",
    "Eddie Edwards": "Eddie the Eagle",
}

records = [
    {"n": 'The Miracle on Ice', "sp": 'Ice hockey', "pr": None, "cc": 'US', "yr": '1980',
     "fa": 'A team of American college players, the youngest in Olympic hockey history, beat the four-time defending champion Soviet Union 4-3 in the semifinal, a team that had not lost an Olympic hockey game since 1968; the Americans won gold two days later against Finland.'},

    {"n": 'Hand of God and Goal of the Century', "sp": 'Football', "pr": 'Diego Maradona', "cc": 'AR', "yr": '1986',
     "fa": 'In the same World Cup quarterfinal against England, Maradona punched the ball into the net for a goal the referees failed to catch, then minutes later dribbled the length of the pitch past five defenders and the goalkeeper for what was later voted the greatest goal in World Cup history; Argentina won 2-1 and went on to lift the trophy.'},

    {"n": 'The Miracle of Istanbul', "sp": 'Football', "pr": None, "cc": 'GB', "yr": '2005',
     "fa": "Down 3-0 to AC Milan at halftime in the Champions League final, Liverpool scored three goals in six second-half minutes to level the match, then won the trophy on penalties, the greatest comeback in the competition's final history."},

    {"n": 'North Korea stuns Italy', "sp": 'Football', "pr": 'Pak Doo-ik', "cc": 'KP', "yr": '1966',
     "fa": "Playing in their first ever World Cup, North Korea beat two-time champions Italy 1-0 on a goal from Pak Doo-ik, still considered one of the greatest upsets in the tournament's history; the Italian team returned home to be pelted with rotten tomatoes by furious fans."},

    {"n": "Roger Milla's Indomitable Lions", "sp": 'Football', "pr": 'Roger Milla', "cc": 'CM', "yr": '1990',
     "fa": "At 38 years old and playing only as a substitute, Milla scored four goals to send Cameroon into the quarterfinals, the first African team ever to reach that stage of the World Cup; his corner-flag dance celebrations became one of the tournament's most iconic images."},

    {"n": "Zidane's headbutt", "sp": 'Football', "pr": 'Zinedine Zidane', "cc": 'FR', "yr": '2006',
     "fa": 'In the 109th minute of what was set to be his final match as a professional, France captain Zinedine Zidane headbutted Italian defender Marco Materazzi in the chest after a verbal exchange and was sent off; France lost the World Cup final on penalties minutes later.'},

    {"n": "Brandi Chastain's winning penalty", "sp": 'Football', "pr": 'Brandi Chastain', "cc": 'US', "yr": '1999',
     "fa": "Chastain scored the decisive penalty to win the Women's World Cup final for the United States in front of 90,000 fans, then tore off her shirt in celebration; the image became one of the defining moments in the growth of women's sport in America."},

    {"n": "Bob Beamon's leap of the century", "sp": 'Athletics (long jump)', "pr": 'Bob Beamon', "cc": 'US', "yr": '1968',
     "fa": 'Beamon jumped 8.90 meters at the high-altitude Mexico City Games, beating the existing world record by 55 centimeters, one of the largest single improvements ever recorded in an athletics world record; the mark stood for 23 years and remains the Olympic record today.'},

    {"n": 'Derek Redmond finishes with his father', "sp": 'Athletics (400m)', "pr": 'Derek Redmond', "cc": 'GB', "yr": '1992',
     "fa": 'Redmond tore his hamstring 150 meters into his Olympic semifinal and collapsed in pain, but got up and kept hobbling toward the finish line; his father broke through security to help him across, and the two finished the race together to a standing ovation from 65,000 spectators.'},

    {"n": 'Kip Keino outruns the world record holder', "sp": 'Athletics (1500m)', "pr": 'Kip Keino', "cc": 'KE', "yr": '1968',
     "fa": "Competing in pain from untreated gallstones and arriving late after getting stuck in Mexico City traffic, Keino still beat the heavily favored American world record holder Jim Ryun by 20 meters, the largest winning margin in the event's Olympic history."},

    {"n": "Jesse Owens' four golds in Berlin", "sp": 'Athletics', "pr": 'Jesse Owens', "cc": 'US', "yr": '1936',
     "fa": "Owens won four gold medals, in the 100m, 200m, long jump, and 4x100m relay, at the Olympics Adolf Hitler had intended as a showcase for Nazi racial ideology; his victories were a direct blow to that narrative in front of the German dictator's own crowd."},

    {"n": 'The first four-minute mile', "sp": 'Athletics (mile)', "pr": 'Roger Bannister', "cc": 'GB', "yr": '1954',
     "fa": "Bannister ran a mile in 3:59.4 at Oxford's Iffley Road track, becoming the first person ever recorded to break the four-minute barrier once thought physically impossible; within three years, fifteen other runners had also done it."},

    {"n": 'Cathy Freeman lights the flame and wins gold', "sp": 'Athletics (400m)', "pr": 'Cathy Freeman', "cc": 'AU', "yr": '2000',
     "fa": 'Freeman, the first Aboriginal Australian to light an Olympic flame, won the 400m final on home soil ten days later in front of a packed stadium, becoming the first Indigenous Australian to win an individual Olympic gold medal and carrying both the Australian and Aboriginal flags on her victory lap.'},

    {"n": "Don Larsen's perfect game", "sp": 'Baseball', "pr": 'Don Larsen', "cc": 'US', "yr": '1956',
     "fa": 'Larsen retired all 27 batters he faced against the Brooklyn Dodgers in Game 5 of the World Series, the only perfect game in World Series history; three days earlier in the same series, he had been pulled from a game after conceding runs in the second inning.'},

    {"n": "Kirk Gibson's impossible home run", "sp": 'Baseball', "pr": 'Kirk Gibson', "cc": 'US', "yr": '1988',
     "fa": 'Gibson, injured in both legs and not even in the starting lineup, was called on to pinch hit in the ninth inning of Game 1 of the World Series and hit a game-winning home run in his only plate appearance of the entire series.'},

    {"n": 'The bloody sock game', "sp": 'Baseball', "pr": 'Curt Schilling', "cc": 'US', "yr": '2004',
     "fa": 'Pitching on a dislocated ankle tendon stitched into place the day before, Schilling threw seven innings of one-run baseball with blood visibly soaking through his sock, keeping Boston alive as they came back from three games down to beat the Yankees in the ALCS.'},

    {"n": "Jackie Robinson breaks baseball's color line", "sp": 'Baseball', "pr": 'Jackie Robinson', "cc": 'US', "yr": '1947',
     "fa": 'Robinson started at first base for the Brooklyn Dodgers, becoming the first Black player in the major leagues in the modern era, ending 50 years of segregation in professional baseball; he went on to win the first ever Rookie of the Year award that season despite facing constant hostility.'},

    {"n": 'Buster Douglas shocks Mike Tyson', "sp": 'Boxing', "pr": 'Buster Douglas', "cc": 'US', "yr": '1990',
     "fa": 'A 42-to-1 underdog who had never beaten a world-class opponent, Douglas knocked out the previously unbeaten and widely feared heavyweight champion Mike Tyson in the tenth round in Tokyo, in what remains one of the biggest upsets in the history of sport.'},

    {"n": 'The Rumble in the Jungle', "sp": 'Boxing', "pr": 'Muhammad Ali', "cc": 'US', "yr": '1974',
     "fa": 'Ali leaned against the ropes and absorbed punches for round after round, a tactic later named the rope-a-dope, letting the younger and harder-hitting champion George Foreman tire himself out before knocking him out in the eighth round to reclaim the heavyweight title in Kinshasa, Zaire.'},

    {"n": 'The Long Count fight', "sp": 'Boxing', "pr": 'Gene Tunney', "cc": 'US', "yr": '1927',
     "fa": 'Knocked down in the seventh round, Tunney got an extra several seconds to recover because challenger Jack Dempsey failed to retreat to a neutral corner as the new rules required, delaying the start of the count; Tunney got back up and went on to win by decision, retaining his heavyweight title.'},

    {"n": "Nadia Comaneci's first perfect 10", "sp": 'Gymnastics', "pr": 'Nadia Comaneci', "cc": 'RO', "yr": '1976',
     "fa": 'Comaneci, 14 years old, scored a flawless routine on the uneven bars, a result so unprecedented that the scoreboard, not designed to display three digits, showed 1.00 instead of 10.00; she went on to score seven perfect 10s that Olympics and became the youngest all-around gymnastics gold medalist in history.'},

    {"n": "Kerri Strug's vault on one leg", "sp": 'Gymnastics', "pr": 'Kerri Strug', "cc": 'US', "yr": '1996',
     "fa": "Strug badly injured her ankle on her first vault attempt, then, unsure if her team still needed the score, landed a second vault on the same leg before collapsing in pain; the United States had already secured the team gold without that final vault, but her performance became one of the Games' most iconic images."},

    {"n": 'Simone Biles and the twisties', "sp": 'Gymnastics', "pr": 'Simone Biles', "cc": 'US', "yr": '2020',
     "fa": 'Biles withdrew from most individual finals after losing her sense of orientation mid-air, a dangerous phenomenon gymnasts call the twisties, prioritizing her safety over competing; she returned days later to win bronze on the balance beam, and her decision sparked a global conversation about athlete mental health.'},

    {"n": 'The Immaculate Reception', "sp": 'American football', "pr": 'Franco Harris', "cc": 'US', "yr": '1972',
     "fa": 'With 22 seconds left in a playoff game against the Raiders and his team facing fourth down, a deflected pass bounced off a collision between two players and was scooped inches off the ground by rookie running back Franco Harris, who ran it in for the winning touchdown; it was later voted the greatest play in NFL history.'},

    {"n": "Joe Namath's guarantee", "sp": 'American football', "pr": 'Joe Namath', "cc": 'US', "yr": '1969',
     "fa": "Three days before Super Bowl III, Namath publicly guaranteed a win for his New York Jets, 18-point underdogs against the Baltimore Colts; the Jets won 16-7, and Namath was named the game's MVP, a result still considered one of the biggest upsets in American sports history."},

    {"n": 'The Catch', "sp": 'American football', "pr": 'Dwight Clark', "cc": 'US', "yr": '1982',
     "fa": "With 58 seconds left in the NFC Championship game, Clark leaped to grab a high pass from Joe Montana in the back of the end zone for the winning touchdown, sending the 49ers to their first Super Bowl and marking the start of the team's 1980s dynasty."},

    {"n": "Jean Van de Velde's collapse", "sp": 'Golf', "pr": 'Jean Van de Velde', "cc": 'FR', "yr": '1999',
     "fa": 'Needing only a double-bogey on the final hole to win the Open Championship, Van de Velde hit his approach into a grandstand, then a creek, then a bunker, eventually carding a triple-bogey and losing the ensuing playoff; it remains one of the most infamous collapses in golf history.'},

    {"n": 'The Miracle at Brookline', "sp": 'Golf', "pr": 'Justin Leonard', "cc": 'US', "yr": '1999',
     "fa": "Trailing Europe by four points heading into the final day of the Ryder Cup, the largest deficit ever overcome, the United States won seven of the first eight singles matches; Justin Leonard sank a 40-foot putt on the 17th hole that sealed the largest comeback in the competition's history."},

    {"n": "The Dream Team's Olympic debut", "sp": 'Basketball', "pr": None, "cc": 'US', "yr": '1992',
     "fa": 'The first US Olympic team to include active NBA players, featuring Michael Jordan, Magic Johnson, and Larry Bird among others, won all eight of its games by an average of 44 points; eleven of its twelve players are now in the Basketball Hall of Fame.'},

    {"n": "India's first Cricket World Cup", "sp": 'Cricket', "pr": 'Kapil Dev', "cc": 'IN', "yr": '1983',
     "fa": "Captained by Kapil Dev, India, appearing in their first ever World Cup final, beat the two-time defending champion West Indies at Lord's, a result so unexpected it transformed cricket's popularity in India for generations."},

    {"n": "Eddie the Eagle's Olympic debut", "sp": 'Ski jumping', "pr": 'Eddie Edwards', "cc": 'GB', "yr": '1988',
     "fa": 'Edwards became the first competitor to represent Great Britain in Olympic ski jumping, finishing dead last in both his events while jumping with glasses that fogged up mid-air; his cheerful refusal to give up made him one of the most beloved figures of the Games despite never coming close to a medal.'},

    {"n": 'Greg Louganis dives through injury', "sp": 'Diving', "pr": 'Greg Louganis', "cc": 'US', "yr": '1988',
     "fa": 'Louganis hit his head on the springboard during a preliminary dive, opening a gash that required stitches, then returned to the same board the next day to win gold; he later revealed he had been diagnosed HIV-positive just months before the Games.'},

    {"n": 'Billie Jean King wins the Battle of the Sexes', "sp": 'Tennis', "pr": 'Billie Jean King', "cc": 'US', "yr": '1973',
     "fa": "King beat 55-year-old self-proclaimed male chauvinist Bobby Riggs in straight sets in front of 90 million television viewers worldwide, a result widely credited with boosting the legitimacy of women's professional sport."},

    {"n": 'Mandela hands the trophy to Pienaar', "sp": 'Rugby union', "pr": 'Nelson Mandela', "cc": 'ZA', "yr": '1995',
     "fa": "Wearing the Springbok captain's own number 6 jersey, a team long associated with apartheid-era white South Africa, President Nelson Mandela presented the Rugby World Cup to captain Francois Pienaar after South Africa's home victory, a moment widely seen as a landmark in the country's post-apartheid reconciliation."},
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
        protagonist = s.get("pr")
        if protagonist is None:
            s["im"] = None
            skipped += 1
            sys.stdout.buffer.write((f"  [{i+1:2}/{total}] -- (no single protagonist) {s['n'][:50]}" + chr(10)).encode("utf-8"))
            continue
        title = WIKI_EN.get(protagonist, protagonist)
        img = wiki_img(title)
        s["im"] = img
        if img:
            found += 1
        status = "ok" if img else "xx"
        sys.stdout.buffer.write((f"  [{i+1:2}/{total}] {status} {protagonist}" + chr(10)).encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)

    out = Path("assets/sport/sport_legendary_events.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(records, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    sys.stdout.buffer.write(
        (chr(10) + f"Done: {found}/{total - skipped} images found, {skipped} skipped (no single protagonist) -- {total} events total." + chr(10)).encode("utf-8")
    )


if __name__ == "__main__":
    main()
