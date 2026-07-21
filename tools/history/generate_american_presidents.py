import json, sys
sys.stdout.reconfigure(encoding="utf-8")

# n=name, nu=number, mn=mandate_number(None=single term), ts=term_start, te=term_end,
# pa=party, st=state, vp=vice_president, fa=famous_for
presidents = [
    # ── PRÉSIDENTS À MANDAT UNIQUE ─────────────────────────────────────────
    {"n":"John Adams","nu":2,"mn":None,"ts":1797,"te":1801,"pa":"Federalist","st":"Massachusetts","vp":"Thomas Jefferson","fa":"First vice president to become president, avoided war with France"},
    {"n":"John Quincy Adams","nu":6,"mn":None,"ts":1825,"te":1829,"pa":"Democratic-Republican","st":"Massachusetts","vp":"John C. Calhoun","fa":"Son of a president, won a contested election decided by the House, championed infrastructure and science"},
    {"n":"Martin Van Buren","nu":8,"mn":None,"ts":1837,"te":1841,"pa":"Democratic","st":"New York","vp":"Richard Mentor Johnson","fa":"Presidency defined by the Panic of 1837, opposed the annexation of Texas to avoid war with Mexico"},
    {"n":"William Henry Harrison","nu":9,"mn":None,"ts":1841,"te":1841,"pa":"Whig","st":"Ohio","vp":"John Tyler","fa":"Shortest presidency in US history — died 31 days after the longest inaugural address ever given"},
    {"n":"John Tyler","nu":10,"mn":None,"ts":1841,"te":1845,"pa":"Whig (expelled) / Independent","st":"Virginia","vp":"None","fa":"First VP to become president after a death in office, set the succession precedent, annexed Texas"},
    {"n":"James K. Polk","nu":11,"mn":None,"ts":1845,"te":1849,"pa":"Democratic","st":"Tennessee","vp":"George M. Dallas","fa":"Expanded US to Pacific, acquired California and Southwest from Mexico"},
    {"n":"Zachary Taylor","nu":12,"mn":None,"ts":1849,"te":1850,"pa":"Whig","st":"Louisiana","vp":"Millard Fillmore","fa":"War hero of Mexican-American War, died 16 months into term"},
    {"n":"Millard Fillmore","nu":13,"mn":None,"ts":1850,"te":1853,"pa":"Whig","st":"New York","vp":"None","fa":"Signed Compromise of 1850, sent Perry to open Japan"},
    {"n":"Franklin Pierce","nu":14,"mn":None,"ts":1853,"te":1857,"pa":"Democratic","st":"New Hampshire","vp":"William Rufus DeVane King","fa":"Kansas-Nebraska Act inflamed slavery debate"},
    {"n":"James Buchanan","nu":15,"mn":None,"ts":1857,"te":1861,"pa":"Democratic","st":"Pennsylvania","vp":"John C. Breckinridge","fa":"Only bachelor president, failed to prevent Civil War"},
    {"n":"Andrew Johnson","nu":17,"mn":None,"ts":1865,"te":1869,"pa":"Democratic / National Union","st":"Tennessee","vp":"None","fa":"First impeached president, controversial Reconstruction policies"},
    {"n":"Rutherford B. Hayes","nu":19,"mn":None,"ts":1877,"te":1881,"pa":"Republican","st":"Ohio","vp":"William A. Wheeler","fa":"Ended Reconstruction, disputed election decided by Congress"},
    {"n":"James A. Garfield","nu":20,"mn":None,"ts":1881,"te":1881,"pa":"Republican","st":"Ohio","vp":"Chester A. Arthur","fa":"Assassinated after only 200 days in office"},
    {"n":"Chester A. Arthur","nu":21,"mn":None,"ts":1881,"te":1885,"pa":"Republican","st":"New York","vp":"None","fa":"Pendleton Civil Service Reform Act, modernized US Navy"},
    {"n":"Grover Cleveland","nu":22,"mn":None,"ts":1885,"te":1889,"pa":"Democratic","st":"New York","vp":"Thomas A. Hendricks","fa":"First Democrat since the Civil War, vetoed hundreds of spending bills"},
    {"n":"Benjamin Harrison","nu":23,"mn":None,"ts":1889,"te":1893,"pa":"Republican","st":"Indiana","vp":"Levi P. Morton","fa":"Six states admitted to Union, first billion-dollar Congress"},
    {"n":"Grover Cleveland","nu":24,"mn":None,"ts":1893,"te":1897,"pa":"Democratic","st":"New York","vp":"Adlai Stevenson I","fa":"Only president to serve two non-consecutive terms, faced Panic of 1893"},
    {"n":"William McKinley","nu":25,"mn":None,"ts":1897,"te":1901,"pa":"Republican","st":"Ohio","vp":"Garret Hobart / Theodore Roosevelt","fa":"Spanish-American War made US a world power, assassinated in 1901"},
    {"n":"Theodore Roosevelt","nu":26,"mn":None,"ts":1901,"te":1909,"pa":"Republican","st":"New York","vp":"Charles W. Fairbanks","fa":"Trust-busting, conservation of national parks, Nobel Peace Prize, Panama Canal"},
    {"n":"William Howard Taft","nu":27,"mn":None,"ts":1909,"te":1913,"pa":"Republican","st":"Ohio","vp":"James S. Sherman","fa":"Only person to serve as both President and Chief Justice of Supreme Court"},
    {"n":"Warren G. Harding","nu":29,"mn":None,"ts":1921,"te":1923,"pa":"Republican","st":"Ohio","vp":"Calvin Coolidge","fa":"Teapot Dome Scandal, died in office"},
    {"n":"Calvin Coolidge","nu":30,"mn":None,"ts":1923,"te":1929,"pa":"Republican","st":"Massachusetts","vp":"Charles G. Dawes","fa":"Roaring Twenties prosperity, known for minimal government intervention"},
    {"n":"Herbert Hoover","nu":31,"mn":None,"ts":1929,"te":1933,"pa":"Republican","st":"California","vp":"Charles Curtis","fa":"Great Depression began under his watch, opposed direct federal relief"},
    {"n":"Harry S. Truman","nu":33,"mn":None,"ts":1945,"te":1953,"pa":"Democratic","st":"Missouri","vp":"Alben W. Barkley","fa":"Ended WWII with atomic bombs, Marshall Plan, Korean War, NATO"},
    {"n":"John F. Kennedy","nu":35,"mn":None,"ts":1961,"te":1963,"pa":"Democratic","st":"Massachusetts","vp":"Lyndon B. Johnson","fa":"Cuban Missile Crisis, Space Race, assassinated in Dallas (1963)"},
    {"n":"Lyndon B. Johnson","nu":36,"mn":None,"ts":1963,"te":1969,"pa":"Democratic","st":"Texas","vp":"Hubert Humphrey","fa":"Great Society, Civil Rights Act, Voting Rights Act, Vietnam escalation"},
    {"n":"Richard Nixon","nu":37,"mn":None,"ts":1969,"te":1974,"pa":"Republican","st":"California","vp":"Spiro Agnew / Gerald Ford","fa":"Opened China relations, ended Vietnam War, resigned due to Watergate"},
    {"n":"Gerald Ford","nu":38,"mn":None,"ts":1974,"te":1977,"pa":"Republican","st":"Michigan","vp":"Nelson Rockefeller","fa":"Only president never elected VP or President, pardoned Nixon"},
    {"n":"Jimmy Carter","nu":39,"mn":None,"ts":1977,"te":1981,"pa":"Democratic","st":"Georgia","vp":"Walter Mondale","fa":"Camp David Accords, Iran hostage crisis, Nobel Peace Prize (2002)"},
    {"n":"George H.W. Bush","nu":41,"mn":None,"ts":1989,"te":1993,"pa":"Republican","st":"Texas","vp":"Dan Quayle","fa":"Gulf War, German reunification, fall of Soviet Union"},
    {"n":"Donald Trump","nu":45,"mn":None,"ts":2017,"te":2021,"pa":"Republican","st":"New York / Florida","vp":"Mike Pence","fa":"America First policy, impeached twice, COVID-19 pandemic"},
    {"n":"Joe Biden","nu":46,"mn":None,"ts":2021,"te":2025,"pa":"Democratic","st":"Delaware","vp":"Kamala Harris","fa":"Oldest elected president, withdrew from Afghanistan, Ukraine support"},
    {"n":"Donald Trump","nu":47,"mn":None,"ts":2025,"te":None,"pa":"Republican","st":"Florida","vp":"JD Vance","fa":"Only president to serve two non-consecutive terms (45th and 47th)"},
    # ── PRÉSIDENTS À MANDATS MULTIPLES CONSÉCUTIFS ────────────────────────
    {"n":"George Washington","nu":1,"mn":1,"ts":1789,"te":1793,"pa":"Independent","st":"Virginia","vp":"John Adams","fa":"First President, established the Cabinet and two-party system precedents"},
    {"n":"George Washington","nu":1,"mn":2,"ts":1793,"te":1797,"pa":"Independent","st":"Virginia","vp":"John Adams","fa":"Neutrality Proclamation, Whiskey Rebellion, Jay Treaty with Britain"},
    {"n":"Thomas Jefferson","nu":3,"mn":1,"ts":1801,"te":1805,"pa":"Democratic-Republican","st":"Virginia","vp":"Aaron Burr","fa":"Louisiana Purchase doubled US territory, Lewis and Clark expedition launched"},
    {"n":"Thomas Jefferson","nu":3,"mn":2,"ts":1805,"te":1809,"pa":"Democratic-Republican","st":"Virginia","vp":"George Clinton","fa":"Embargo Act against Britain and France, abolished slave trade in US"},
    {"n":"James Madison","nu":4,"mn":1,"ts":1809,"te":1813,"pa":"Democratic-Republican","st":"Virginia","vp":"George Clinton","fa":"Father of the Constitution, rising tensions with Britain, War of 1812 declared"},
    {"n":"James Madison","nu":4,"mn":2,"ts":1813,"te":1817,"pa":"Democratic-Republican","st":"Virginia","vp":"Elbridge Gerry","fa":"War of 1812 ends with Treaty of Ghent, White House burned by British"},
    {"n":"James Monroe","nu":5,"mn":1,"ts":1817,"te":1821,"pa":"Democratic-Republican","st":"Virginia","vp":"Daniel D. Tompkins","fa":"Era of Good Feelings, Transcontinental Treaty with Spain, Missouri crisis"},
    {"n":"James Monroe","nu":5,"mn":2,"ts":1821,"te":1825,"pa":"Democratic-Republican","st":"Virginia","vp":"Daniel D. Tompkins","fa":"Monroe Doctrine warned Europe against further colonialism in the Americas"},
    {"n":"Andrew Jackson","nu":7,"mn":1,"ts":1829,"te":1833,"pa":"Democratic","st":"Tennessee","vp":"John C. Calhoun","fa":"First Democrat, Indian Removal Act, spoils system expanded in federal government"},
    {"n":"Andrew Jackson","nu":7,"mn":2,"ts":1833,"te":1837,"pa":"Democratic","st":"Tennessee","vp":"Martin Van Buren","fa":"Bank War — dismantled the Second Bank of the US, nullification crisis resolved"},
    {"n":"Abraham Lincoln","nu":16,"mn":1,"ts":1861,"te":1865,"pa":"Republican","st":"Illinois","vp":"Hannibal Hamlin","fa":"Led US through Civil War, Emancipation Proclamation, Gettysburg Address"},
    {"n":"Abraham Lincoln","nu":16,"mn":2,"ts":1865,"te":1865,"pa":"Republican","st":"Illinois","vp":"Andrew Johnson","fa":"'With malice toward none' inaugural address, assassinated April 14, 1865"},
    {"n":"Ulysses S. Grant","nu":18,"mn":1,"ts":1869,"te":1873,"pa":"Republican","st":"Ohio","vp":"Schuyler Colfax","fa":"Union general who won Civil War, 15th Amendment ratified, fought the KKK"},
    {"n":"Ulysses S. Grant","nu":18,"mn":2,"ts":1873,"te":1877,"pa":"Republican","st":"Ohio","vp":"Henry Wilson","fa":"Credit Mobilier scandal, Panic of 1873, Reconstruction increasingly undermined"},
    {"n":"Woodrow Wilson","nu":28,"mn":1,"ts":1913,"te":1917,"pa":"Democratic","st":"New Jersey","vp":"Thomas R. Marshall","fa":"Federal Reserve Act, income tax, Clayton Antitrust Act, lower tariffs"},
    {"n":"Woodrow Wilson","nu":28,"mn":2,"ts":1917,"te":1921,"pa":"Democratic","st":"New Jersey","vp":"Thomas R. Marshall","fa":"Led US in WWI, 14 Points for peace, League of Nations proposed, suffered stroke"},
    {"n":"Franklin D. Roosevelt","nu":32,"mn":1,"ts":1933,"te":1937,"pa":"Democratic","st":"New York","vp":"John Nance Garner","fa":"New Deal launched, Banking Act, Social Security Act, end of Prohibition"},
    {"n":"Franklin D. Roosevelt","nu":32,"mn":2,"ts":1937,"te":1941,"pa":"Democratic","st":"New York","vp":"John Nance Garner","fa":"Court-packing attempt, Second New Deal, Roosevelt Recession of 1937"},
    {"n":"Franklin D. Roosevelt","nu":32,"mn":3,"ts":1941,"te":1945,"pa":"Democratic","st":"New York","vp":"Henry A. Wallace","fa":"Pearl Harbor, led US into WWII, D-Day, Atlantic Charter with Churchill"},
    {"n":"Franklin D. Roosevelt","nu":32,"mn":4,"ts":1945,"te":1945,"pa":"Democratic","st":"New York","vp":"Harry S. Truman","fa":"Yalta Conference, died in office April 12, 1945 — never saw the end of WWII"},
    {"n":"Dwight D. Eisenhower","nu":34,"mn":1,"ts":1953,"te":1957,"pa":"Republican","st":"Kansas","vp":"Richard Nixon","fa":"Korean War armistice, McCarthy era, Interstate Highway System launched"},
    {"n":"Dwight D. Eisenhower","nu":34,"mn":2,"ts":1957,"te":1961,"pa":"Republican","st":"Kansas","vp":"Richard Nixon","fa":"Little Rock Crisis, NASA created, warned of military-industrial complex"},
    {"n":"Ronald Reagan","nu":40,"mn":1,"ts":1981,"te":1985,"pa":"Republican","st":"California","vp":"George H.W. Bush","fa":"Reaganomics, assassination attempt survived, Lebanon bombing, SDI launched"},
    {"n":"Ronald Reagan","nu":40,"mn":2,"ts":1985,"te":1989,"pa":"Republican","st":"California","vp":"George H.W. Bush","fa":"Iran-Contra affair, Reykjavik Summit, 'Tear down this wall', Cold War ends"},
    {"n":"Bill Clinton","nu":42,"mn":1,"ts":1993,"te":1997,"pa":"Democratic","st":"Arkansas","vp":"Al Gore","fa":"NAFTA, Brady Bill, Family and Medical Leave Act, Oslo Accords"},
    {"n":"Bill Clinton","nu":42,"mn":2,"ts":1997,"te":2001,"pa":"Democratic","st":"Arkansas","vp":"Al Gore","fa":"Budget surplus, Kosovo War, impeached over Lewinsky scandal but acquitted"},
    {"n":"George W. Bush","nu":43,"mn":1,"ts":2001,"te":2005,"pa":"Republican","st":"Texas","vp":"Dick Cheney","fa":"9/11 response, War on Terror, Afghanistan War, Iraq War, Patriot Act"},
    {"n":"George W. Bush","nu":43,"mn":2,"ts":2005,"te":2009,"pa":"Republican","st":"Texas","vp":"Dick Cheney","fa":"Hurricane Katrina failures, Iraq surge strategy, 2008 financial crisis bailout"},
    {"n":"Barack Obama","nu":44,"mn":1,"ts":2009,"te":2013,"pa":"Democratic","st":"Illinois","vp":"Joe Biden","fa":"First African-American president, Affordable Care Act, economic stimulus, killed Bin Laden"},
    {"n":"Barack Obama","nu":44,"mn":2,"ts":2013,"te":2017,"pa":"Democratic","st":"Illinois","vp":"Joe Biden","fa":"Obergefell same-sex marriage ruling, Iran nuclear deal, Paris Agreement, Cuba normalization"},
]

with open("assets/history/american_presidents.json", "w", encoding="utf-8") as f:
    json.dump(presidents, f, ensure_ascii=False, separators=(',', ':'))

single = sum(1 for p in presidents if p["mn"] is None)
multi  = sum(1 for p in presidents if p["mn"] is not None)
print(f"{len(presidents)} entrees : {single} mandats uniques + {multi} mandats multiples.")
