import json, requests, time, sys
from pathlib import Path
from urllib.parse import quote

# n=name, co=country, yr=years, or=orientation (None if uncertain/debated by historians),
# fi=field, fa=impact, im=imageUrl

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# name → Wikipedia page title for image lookup
WIKI_EN = {
    "Alan Turing":               "Alan Turing",
    "Oscar Wilde":               "Oscar Wilde",
    "Pyotr Ilyich Tchaikovsky":  "Pyotr Ilyich Tchaikovsky",
    "Frida Kahlo":               "Frida Kahlo",
    "James Baldwin":             "James Baldwin",
    "Marlene Dietrich":          "Marlene Dietrich",
    "Harvey Milk":               "Harvey Milk",
    "Bayard Rustin":             "Bayard Rustin",
    "Virginia Woolf":            "Virginia Woolf",
    "Andy Warhol":               "Andy Warhol",
    "Marsha P. Johnson":         "Marsha P. Johnson",
    "Leonard Bernstein":         "Leonard Bernstein",
    "Christine Jorgensen":       "Christine Jorgensen",
    "Josephine Baker":           "Josephine Baker",
    "Michel Foucault":           "Michel Foucault",
    "Karl Heinrich Ulrichs":     "Karl Heinrich Ulrichs",
    "Sergei Diaghilev":          "Sergei Diaghilev",
    "Alvin Ailey":               "Alvin Ailey",
    "Sappho":                    "Sappho",
    "Elton John":                "Elton John",
    "Lili Elbe":                 "Lili Elbe",
    "Freddie Mercury":           "Freddie Mercury",
    "Willa Cather":              "Willa Cather",
    "Audre Lorde":               "Audre Lorde",
    "David Bowie":               "David Bowie",
}

personalities = [
    # ── Literature & Arts ─────────────────────────────────────────────────────
    {"n": "Oscar Wilde", "co": "Ireland / United Kingdom", "yr": "1854-1900",
     "or": "gay", "fi": "Literature & Theatre",
     "fa": "One of the greatest playwrights and wits of the Victorian era. Sentenced to two years' hard labour for 'gross indecency' in 1895. His works including The Importance of Being Earnest and The Picture of Dorian Gray endure as classics of English literature."},

    {"n": "Virginia Woolf", "co": "United Kingdom", "yr": "1882-1941",
     "or": "bisexual", "fi": "Literature",
     "fa": "Pioneering modernist novelist and essayist, author of Mrs Dalloway and Orlando — the latter a gender-fluid love letter to her partner Vita Sackville-West. Her essay A Room of One's Own is a cornerstone of feminist literary criticism."},

    {"n": "Willa Cather", "co": "United States", "yr": "1873-1947",
     "or": "lesbian", "fi": "Literature",
     "fa": "Pulitzer Prize-winning novelist celebrated for her portrayals of frontier life in O Pioneers! and My Ántonia. Lived for nearly 40 years with her partner Edith Lewis. Scholars broadly recognise her same-sex relationships as central to her identity."},

    {"n": "James Baldwin", "co": "United States", "yr": "1924-1987",
     "or": "gay", "fi": "Literature & Civil Rights",
     "fa": "Groundbreaking novelist and essayist who explored racial and sexual identity in America. His works Giovanni's Room and Notes of a Native Son confronted race, class, and homosexuality when both were taboo. A pivotal voice in the American civil rights movement."},

    {"n": "Audre Lorde", "co": "United States", "yr": "1934-1992",
     "or": "lesbian", "fi": "Poetry & Activism",
     "fa": "Black lesbian feminist poet whose works explored race, sex, and class intersectionality. Her collection The Cancer Journals documented her experience with breast cancer as a political act. She coined the phrase 'The master's tools will never dismantle the master's house.'"},

    {"n": "Sappho", "co": "Ancient Greece (Lesbos)", "yr": "c. 630-c. 570 BCE",
     "or": "lesbian", "fi": "Poetry",
     "fa": "Ancient Greek lyric poet from the island of Lesbos, widely regarded as one of the greatest poets of antiquity. Her poems express love and longing for women; the words 'lesbian' and 'sapphic' derive from her name and birthplace. Only fragments of her nine volumes survive."},

    # ── Music ─────────────────────────────────────────────────────────────────
    {"n": "Pyotr Ilyich Tchaikovsky", "co": "Russia", "yr": "1840-1893",
     "or": "gay", "fi": "Classical Music",
     "fa": "One of the most celebrated composers in history, creator of Swan Lake, The Nutcracker, and the 1812 Overture. His homosexuality was a source of great personal anguish in Tsarist Russia, where it was illegal. Historians widely agree on his orientation from personal letters."},

    {"n": "Leonard Bernstein", "co": "United States", "yr": "1918-1990",
     "or": "bisexual", "fi": "Classical Music & Theatre",
     "fa": "One of the greatest American conductors and composers, creator of West Side Story. Openly bisexual in private, he navigated identity in an era of intense social pressure. His candid later interviews helped destigmatise bisexuality in public life."},

    {"n": "Freddie Mercury", "co": "United Kingdom (born Zanzibar)", "yr": "1946-1991",
     "or": "bisexual", "fi": "Music",
     "fa": "Lead vocalist of Queen and one of rock music's greatest performers, known for his extraordinary vocal range and showmanship. His death from AIDS-related illness in 1991 put a human face on the epidemic and contributed to global AIDS awareness."},

    {"n": "Elton John", "co": "United Kingdom", "yr": "1947-",
     "or": "gay", "fi": "Music",
     "fa": "One of the best-selling music artists of all time with over 300 million records sold. Came out publicly in 1988 and married his partner David Furnish in 2014. His Elton John AIDS Foundation has raised over $600 million for HIV/AIDS relief worldwide."},

    {"n": "David Bowie", "co": "United Kingdom", "yr": "1947-2016",
     "or": "bisexual", "fi": "Music",
     "fa": "Rock pioneer whose alter egos Ziggy Stardust and Aladdin Sane challenged gender norms worldwide. Identified as bisexual in 1972 in one of rock's first major coming-out interviews, though he later described himself as 'a closet heterosexual'. A cultural icon of gender fluidity."},

    # ── Science & Technology ──────────────────────────────────────────────────
    {"n": "Alan Turing", "co": "United Kingdom", "yr": "1912-1954",
     "or": "gay", "fi": "Mathematics & Computing",
     "fa": "Father of computer science and artificial intelligence. His Turing machine concept laid the foundation for modern computing. Convicted under anti-homosexuality laws in 1952 and chemically castrated by the British government; received a posthumous royal pardon in 2013."},

    # ── Visual Arts ───────────────────────────────────────────────────────────
    {"n": "Frida Kahlo", "co": "Mexico", "yr": "1907-1954",
     "or": "bisexual", "fi": "Painting",
     "fa": "Iconic Mexican painter known for deeply personal self-portraits exploring pain, identity, and Mexican culture. Openly bisexual, she had affairs with women including Georgia O'Keeffe. Her life and work became a symbol of resilience, feminism, and LGBTQ+ pride."},

    {"n": "Andy Warhol", "co": "United States", "yr": "1928-1987",
     "or": "gay", "fi": "Visual Arts & Pop Culture",
     "fa": "Father of Pop Art and one of the most influential artists of the 20th century. His Factory studio became a creative sanctuary for LGBTQ+ communities. Through his work and persona, he openly challenged heteronormative culture at a time when being openly gay was deeply taboo."},

    {"n": "Marlene Dietrich", "co": "Germany / United States", "yr": "1901-1992",
     "or": "bisexual", "fi": "Film & Music",
     "fa": "Legendary actress and singer who defied gender norms by wearing men's suits on stage and screen. Openly bisexual, she had relationships with both men and women in Hollywood. Her anti-Nazi stance during WWII and support for Allied troops made her a symbol of moral courage."},

    # ── Dance & Theatre ───────────────────────────────────────────────────────
    {"n": "Alvin Ailey", "co": "United States", "yr": "1931-1989",
     "or": "gay", "fi": "Dance & Choreography",
     "fa": "Founder of the Alvin Ailey American Dance Theater (1958), which brought African-American cultural expression to the centre of modern dance. His masterwork Revelations is among the most-seen dance pieces in history. A pioneering Black gay artist who broke multiple barriers."},

    {"n": "Sergei Diaghilev", "co": "Russia", "yr": "1872-1929",
     "or": "gay", "fi": "Ballet & Visual Arts",
     "fa": "Founder of the Ballets Russes, the most influential ballet company of the 20th century, which revolutionised dance, music, and visual art. Collaborated with Stravinsky, Picasso, and Matisse. His relationships with male dancers including Nijinsky were an open secret in European artistic circles."},

    # ── Philosophy ────────────────────────────────────────────────────────────
    {"n": "Michel Foucault", "co": "France", "yr": "1926-1984",
     "or": "gay", "fi": "Philosophy",
     "fa": "Influential philosopher whose work on power, sexuality, and social norms transformed the humanities. His book The History of Sexuality examined how societies construct and control sexual identities. A prominent voice in French gay liberation politics."},

    # ── Activism & Politics ───────────────────────────────────────────────────
    {"n": "Harvey Milk", "co": "United States", "yr": "1930-1978",
     "or": "gay", "fi": "Politics & Activism",
     "fa": "First openly gay elected official in California history, serving on the San Francisco Board of Supervisors. His election in 1977 was a milestone for LGBTQ+ political representation. Assassinated in 1978, he became a martyr for gay rights and is celebrated every May 22."},

    {"n": "Bayard Rustin", "co": "United States", "yr": "1912-1987",
     "or": "gay", "fi": "Civil Rights Activism",
     "fa": "Chief organiser of the 1963 March on Washington where Martin Luther King Jr. delivered his 'I Have a Dream' speech. An openly gay Black man, he was often pushed to the background of the civil rights movement due to homophobia. Posthumously awarded the Presidential Medal of Freedom in 2013."},

    {"n": "Karl Heinrich Ulrichs", "co": "Germany", "yr": "1825-1895",
     "or": "gay", "fi": "Legal Advocacy",
     "fa": "First person in recorded history to publicly argue for gay rights. In 1867 he openly addressed the Congress of German Jurists to call for repeal of anti-sodomy laws — the first public gay rights speech. His writings coined terms foundational to early sexology."},

    {"n": "Marsha P. Johnson", "co": "United States", "yr": "1945-1992",
     "or": "gay", "fi": "LGBTQ+ Activism",
     "fa": "Black transgender activist who was among the first to resist police raids at the Stonewall Inn in 1969 — a pivotal moment in LGBTQ+ liberation. Co-founded the Street Transvestite Action Revolutionaries (STAR) to support homeless LGBTQ+ youth."},

    {"n": "Josephine Baker", "co": "United States / France", "yr": "1906-1975",
     "or": "bisexual", "fi": "Entertainment & Civil Rights",
     "fa": "Legendary dancer, singer, and civil rights activist who became the most celebrated Black entertainer in Europe. Openly bisexual. She refused to perform for segregated audiences and was the only official female speaker at the 1963 March on Washington."},

    # ── Transgender pioneers ──────────────────────────────────────────────────
    {"n": "Christine Jorgensen", "co": "United States", "yr": "1926-1989",
     "or": "transgender woman", "fi": "Advocacy & Entertainment",
     "fa": "First American to become widely known for having gender reassignment surgery (1952). Her story sparked international conversation about gender identity at a time when the concept was almost entirely unknown to the public. A pioneer for transgender visibility."},

    {"n": "Lili Elbe", "co": "Denmark", "yr": "1882-1931",
     "or": "transgender woman", "fi": "Painting & Advocacy",
     "fa": "Danish painter and one of the first known recipients of gender reassignment surgery (1930). Born Einar Wegener, her life and courage inspired the novel and film The Danish Girl. A landmark figure in the history of transgender identity and rights."},
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
    total = len(personalities)
    found = 0
    for i, s in enumerate(personalities):
        title = WIKI_EN.get(s["n"], s["n"])
        img = wiki_img(title)
        s["im"] = img
        if img:
            found += 1
        status = "ok" if img else "xx"
        sys.stdout.buffer.write(f"  [{i+1:2}/{total}] {status} {s['n']}\n".encode("utf-8"))
        sys.stdout.buffer.flush()
        time.sleep(0.3)
    out = Path("assets/celebrity/lgbtqia.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(personalities, ensure_ascii=False, separators=(',', ':')), encoding="utf-8")
    sys.stdout.buffer.write(f"\nDone: {found}/{total} images — {total} personalities total.\n".encode("utf-8"))


if __name__ == "__main__":
    main()
