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
