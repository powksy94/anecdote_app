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
    "Walt Whitman":              "Walt Whitman",
    "Arthur Rimbaud":            "Arthur Rimbaud",
    "Tennessee Williams":        "Tennessee Williams",
    "Truman Capote":             "Truman Capote",
    "Gertrude Stein":            "Gertrude Stein",
    "Radclyffe Hall":            "Radclyffe Hall",
    "Patricia Highsmith":        "Patricia Highsmith",
    "E.M. Forster":              "E. M. Forster",
    "Jean Genet":                "Jean Genet",
    "Noel Coward":               "Noel Coward",
    "Langston Hughes":           "Langston Hughes",
    "Cole Porter":               "Cole Porter",
    "Dusty Springfield":         "Dusty Springfield",
    "George Michael":            "George Michael",
    "Rock Hudson":               "Rock Hudson",
    "Montgomery Clift":          "Montgomery Clift",
    "Derek Jarman":              "Derek Jarman",
    "Pedro Almodovar":           "Pedro Almodovar",
    "Magnus Hirschfeld":         "Magnus Hirschfeld",
    "Sylvia Rivera":             "Sylvia Rivera",
    "Lorraine Hansberry":        "Lorraine Hansberry",
    "Hadrian":                   "Hadrian",
    "Alexander the Great":       "Alexander the Great",
    "Queen Christina of Sweden": "Christina, Queen of Sweden",
    "Yukio Mishima":             "Yukio Mishima",
    "Liberace":                  "Liberace",
    "Janis Joplin":              "Janis Joplin",
    "Ian McKellen":              "Ian McKellen",
    "Pier Paolo Pasolini":       "Pier Paolo Pasolini",
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

    # ── Literature (additional) ───────────────────────────────────────────────
    {"n": "Walt Whitman", "co": "United States", "yr": "1819-1892",
     "or": "gay", "fi": "Poetry",
     "fa": "Author of Leaves of Grass (1855), one of the most influential collections in American literature. His Calamus poems openly celebrated same-sex love — revolutionary in 19th-century America. Often called the 'father of free verse', he shaped modern poetry worldwide."},

    {"n": "Arthur Rimbaud", "co": "France", "yr": "1854-1891",
     "or": "gay", "fi": "Poetry",
     "fa": "Wrote some of the most experimental poetry of the 19th century — including A Season in Hell and Illuminations — before the age of 21, then abandoned literature entirely. His intense relationship with poet Paul Verlaine (who shot him) scandalised Paris and shaped Symbolism and Surrealism."},

    {"n": "Tennessee Williams", "co": "United States", "yr": "1911-1983",
     "or": "gay", "fi": "Theatre",
     "fa": "Two-time Pulitzer Prize-winning playwright (A Streetcar Named Desire, Cat on a Hot Tin Roof). His plays explored repressed desire, identity, and the American South. A closeted gay man whose works subtly but powerfully encoded queer experience in mid-century American drama."},

    {"n": "Truman Capote", "co": "United States", "yr": "1924-1984",
     "or": "gay", "fi": "Literature",
     "fa": "Author of In Cold Blood (1966), which invented the 'non-fiction novel' genre, and Breakfast at Tiffany's. Openly gay at a time when it was deeply stigmatised in American society. His flamboyant public persona challenged the idea of what a serious American writer could look like."},

    {"n": "Gertrude Stein", "co": "United States / France", "yr": "1874-1946",
     "or": "lesbian", "fi": "Literature & Art",
     "fa": "Avant-garde writer and art collector whose Paris salon was the hub of Modernism — she was the patron and friend of Picasso, Hemingway, Matisse, and Fitzgerald. Lived openly with her partner Alice B. Toklas for nearly 40 years. Her experimental prose directly influenced American literature."},

    {"n": "Radclyffe Hall", "co": "United Kingdom", "yr": "1880-1943",
     "or": "lesbian", "fi": "Literature",
     "fa": "Author of The Well of Loneliness (1928), the first serious English-language novel to portray lesbian relationships with dignity. The British government banned it as obscene, but it became an underground classic that gave millions of readers the first language for their own identity."},

    {"n": "Patricia Highsmith", "co": "United States", "yr": "1921-1995",
     "or": "lesbian", "fi": "Literature",
     "fa": "Crime novelist whose characters — including Tom Ripley — redefined the psychological thriller. Her lesbian novel The Price of Salt (1952), published pseudonymously, was the first novel featuring a same-sex romance with a happy ending; republished as Carol in 1984 under her own name."},

    {"n": "E.M. Forster", "co": "United Kingdom", "yr": "1879-1970",
     "or": "gay", "fi": "Literature",
     "fa": "Author of A Room with a View and A Passage to India. His novel Maurice — a gay love story — was written in 1913 but only published posthumously in 1971, the year after his death. He feared it would destroy his reputation. It is now a landmark in LGBTQ+ literature."},

    {"n": "Jean Genet", "co": "France", "yr": "1910-1986",
     "or": "gay", "fi": "Literature & Theatre",
     "fa": "Raised in a reformatory, he turned petty crime and prison life into literature. Our Lady of the Flowers, The Maids, and The Balcony explored homosexuality, transgression, and power. Sartre championed him; his work became foundational for queer theory and postcolonial studies."},

    {"n": "Noel Coward", "co": "United Kingdom", "yr": "1899-1973",
     "or": "gay", "fi": "Theatre, Music & Film",
     "fa": "Playwright, composer, actor, and director who defined British wit and sophistication for 50 years. Openly gay in his private life but guarded publicly due to the era's laws. Works like Private Lives and Brief Encounter remain staples of the British theatrical canon."},

    {"n": "Langston Hughes", "co": "United States", "yr": "1902-1967",
     "or": "gay", "fi": "Poetry & Literature",
     "fa": "Central figure of the Harlem Renaissance whose poems celebrated Black American life with jazz rhythms and vernacular speech. His sexual orientation — extensively documented by biographers — was kept private during his lifetime due to the racism and homophobia he faced simultaneously."},

    # ── Music (additional) ────────────────────────────────────────────────────
    {"n": "Cole Porter", "co": "United States", "yr": "1891-1964",
     "or": "gay", "fi": "Music & Theatre",
     "fa": "Songwriter of over 800 songs and 21 Broadway musicals including Anything Goes and Kiss Me, Kate. His lyrics were famous for their double entendres encoding queer desire into mainstream entertainment. Lived openly with his male partner while maintaining a marriage of convenience with Linda Lee Thomas."},

    {"n": "Dusty Springfield", "co": "United Kingdom", "yr": "1939-1999",
     "or": "bisexual", "fi": "Music",
     "fa": "One of the greatest British vocalists of the 1960s-70s, known for Son of a Preacher Man and her album Dusty in Memphis. A pioneer of blue-eyed soul. Openly bisexual in interviews as early as 1970, she was one of the first major British pop stars to come out publicly."},

    {"n": "George Michael", "co": "United Kingdom", "yr": "1963-2016",
     "or": "gay", "fi": "Music",
     "fa": "One of the best-selling music artists of all time (over 100 million records). Came out publicly in 1998 and became an outspoken advocate for HIV/AIDS charities and LGBTQ+ rights. His album Faith (1987) remains one of the best-selling albums in history."},

    # ── Film & Arts (additional) ──────────────────────────────────────────────
    {"n": "Rock Hudson", "co": "United States", "yr": "1925-1985",
     "or": "gay", "fi": "Film",
     "fa": "Major Hollywood star of the 1950s-60s, known for Magnificent Obsession and Giant. His public disclosure of his AIDS diagnosis in 1985 was the first by a major celebrity and transformed global awareness of the epidemic, helping galvanise political action that had been ignored for years."},

    {"n": "Montgomery Clift", "co": "United States", "yr": "1920-1966",
     "or": "bisexual", "fi": "Film",
     "fa": "One of the most acclaimed actors of the 1950s, known for A Place in the Sun and From Here to Eternity. His bisexuality, kept hidden due to Hollywood's strict moral codes, and a car accident in 1956 that disfigured his face contributed to his personal and professional decline."},

    {"n": "Derek Jarman", "co": "United Kingdom", "yr": "1942-1994",
     "or": "gay", "fi": "Film & Visual Arts",
     "fa": "Avant-garde filmmaker and activist whose films (Sebastiane, Caravaggio, Edward II) radically reimagined queer history and aesthetics. His memoir Modern Nature, written while living with AIDS, is a masterpiece of landscape writing and queer grief. A defining voice of British gay culture."},

    {"n": "Pedro Almodovar", "co": "Spain", "yr": "1949-",
     "or": "gay", "fi": "Film",
     "fa": "Spain's most celebrated filmmaker, whose work (Women on the Verge of a Nervous Breakdown, All About My Mother, Pain and Glory) centres on women, queer characters, and the absurdity of desire. Emerged from Madrid's post-Franco La Movida counterculture and brought Spanish cinema to global recognition."},

    # ── Activism & History (additional) ──────────────────────────────────────
    {"n": "Magnus Hirschfeld", "co": "Germany", "yr": "1868-1935",
     "or": "gay", "fi": "Medicine & Activism",
     "fa": "Founded the Institut fur Sexualwissenschaft in Berlin (1919) — the world's first institute for the scientific study of human sexuality. Coined the word 'transvestism'. His institute was destroyed by the Nazis in 1933 in one of the first book-burnings of the regime. Called the 'Einstein of sex.'"},

    {"n": "Sylvia Rivera", "co": "United States", "yr": "1951-2002",
     "or": "transgender woman", "fi": "LGBTQ+ Activism",
     "fa": "Latina transgender activist who fought at the Stonewall Inn in 1969 alongside Marsha P. Johnson. Co-founded STAR (Street Transvestite Action Revolutionaries). Spent decades fighting for transgender people of colour who were systematically excluded from mainstream gay rights organisations."},

    {"n": "Lorraine Hansberry", "co": "United States", "yr": "1930-1965",
     "or": "lesbian", "fi": "Theatre & Activism",
     "fa": "Author of A Raisin in the Sun (1959), the first play by a Black woman produced on Broadway. The youngest American and first Black playwright to win the New York Drama Critics' Circle Award. Wrote anonymously to lesbian publications; died at 34 of pancreatic cancer, her full identity only widely known posthumously."},

    {"n": "Hadrian", "co": "Roman Empire", "yr": "76-138 CE",
     "or": "bisexual", "fi": "Politics & Architecture",
     "fa": "Roman Emperor who built Hadrian's Wall in Britain and the Pantheon in Rome. His grief over the death of his male lover Antinous — whom he deified — led to the creation of one of antiquity's most extensive religious cults. Considered one of Rome's 'Five Good Emperors'."},

    {"n": "Alexander the Great", "co": "Ancient Macedonia", "yr": "356-323 BCE",
     "or": "bisexual", "fi": "Military & Politics",
     "fa": "Created one of the largest empires in ancient history by age 30, spanning from Greece to northwestern India. His deep emotional relationship with his companion Hephaestion was widely recognised in antiquity; he mourned his death by crucifying the court physician who failed to save him."},

    {"n": "Queen Christina of Sweden", "co": "Sweden", "yr": "1626-1689",
     "or": None, "fi": "Politics & Philosophy",
     "fa": "Queen of Sweden who abdicated at 27, scandalising Europe. She dressed in men's clothes, refused to marry, and surrounded herself with female favourites; historians widely discuss her identity in terms of gender non-conformity and same-sex attraction. Converted to Catholicism and spent her life in Rome as an intellectual patron."},

    {"n": "Yukio Mishima", "co": "Japan", "yr": "1925-1970",
     "or": "gay", "fi": "Literature",
     "fa": "Japan's most controversial modern writer (Confessions of a Mask, The Temple of the Golden Pavilion), nominated multiple times for the Nobel Prize. Openly wrote about homosexual desire. Founded a private paramilitary group and died by ritual suicide (seppuku) after a failed attempt to incite a nationalist uprising."},

    {"n": "Liberace", "co": "United States", "yr": "1919-1987",
     "or": "gay", "fi": "Entertainment",
     "fa": "The highest-paid entertainer in the world during the 1950s-70s, known for his flamboyant costumes, candelabra, and pianism. Successfully sued a British newspaper for suggesting he was gay in 1959 — while privately gay throughout his career. Died of AIDS-related illness in 1987."},

    {"n": "Janis Joplin", "co": "United States", "yr": "1943-1970",
     "or": "bisexual", "fi": "Music",
     "fa": "One of the most powerful rock and blues vocalists in history, known for Piece of My Heart and Me and Bobby McGee. Openly bisexual, she had relationships with both men and women throughout her short life. Died at 27 of a heroin overdose; her vocal intensity has never been matched."},

    {"n": "Ian McKellen", "co": "United Kingdom", "yr": "1939-",
     "or": "gay", "fi": "Theatre & Film",
     "fa": "Widely regarded as one of the greatest living Shakespearean actors and known globally for Gandalf (Lord of the Rings) and Magneto (X-Men). Came out in 1988 on BBC radio while opposing Clause 28, a law banning 'promotion of homosexuality'. Co-founded Stonewall UK, the leading LGBTQ+ rights organisation."},

    {"n": "Pier Paolo Pasolini", "co": "Italy", "yr": "1922-1975",
     "or": "gay", "fi": "Film, Poetry & Literature",
     "fa": "Italian filmmaker, poet, and intellectual whose films (Accattone, Teorema, Salo) provoked fierce controversy for their treatment of religion, sexuality, and politics. Openly gay in a Catholic society, he was repeatedly prosecuted for obscenity. Murdered in 1975 under circumstances never fully explained."},
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
