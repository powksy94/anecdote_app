import json, requests, time, pathlib, sys

# Légende des champs (format compact)
# n  = name (nom de l'état)
# ca = capital (capitale)
# ni = nickname (surnom officiel)
# re = region (Northeast / South / Midwest / Southwest / West)
# po = population
# ar = area km² (superficie)
# sy = statehood year (année d'admission)
# fa = famous for (anecdote principale, en anglais)
# im = image_url (Wikipedia thumbnail, null si introuvable)

HEADERS = {"User-Agent": "DailyFactsApp/1.0 (matthieuuzan@gmail.com)"}

# Titres Wikipedia alternatifs quand le nom de l'article diffère du nom de l'état
WIKI_OVERRIDES = {
    "Alaska":           "Alaska",
    "Hawaii":           "Hawaii",
    "New York":         "New York (state)",
    "Washington":       "Washington (state)",
    "Georgia":          "Georgia (U.S. state)",
    "Indiana":          "Indiana",
    "New Mexico":       "New Mexico",
    "New Hampshire":    "New Hampshire",
    "New Jersey":       "New Jersey",
    "West Virginia":    "West Virginia",
    "North Carolina":   "North Carolina",
    "South Carolina":   "South Carolina",
    "North Dakota":     "North Dakota",
    "South Dakota":     "South Dakota",
    "Rhode Island":     "Rhode Island",
}

def fetch_wiki_image(state_name: str) -> str | None:
    wiki_title = WIKI_OVERRIDES.get(state_name, state_name)
    url = (
        "https://en.wikipedia.org/w/api.php"
        "?action=query&prop=pageimages&format=json"
        f"&titles={requests.utils.quote(wiki_title)}&pithumbsize=500"
    )
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            src = page.get("thumbnail", {}).get("source")
            if src:
                return src
    except Exception as e:
        print(f"  ⚠ {state_name}: {e}")
    return None

states_raw = [
    {"n":"Alabama","ca":"Montgomery","ni":"Yellowhammer State","re":"South","po":5074296,"ar":135767,"sy":1819,"fa":"Birthplace of the Civil Rights Movement; Rosa Parks refused to give up her bus seat in Montgomery in 1955; home to NASA's Marshall Space Flight Center in Huntsville"},
    {"n":"Alaska","ca":"Juneau","ni":"The Last Frontier","re":"West","po":733583,"ar":1723337,"sy":1959,"fa":"Largest US state, twice the size of Texas; Mt. Denali is North America's highest peak at 6,190m; more coastline than all other states combined; the Northern Lights are visible from Fairbanks"},
    {"n":"Arizona","ca":"Phoenix","ni":"The Grand Canyon State","re":"Southwest","po":7151502,"ar":295234,"sy":1912,"fa":"The Grand Canyon — one of the seven natural wonders of the world; Monument Valley; Saguaro cactus forests; the Navajo Nation stretches across its northeast"},
    {"n":"Arkansas","ca":"Little Rock","ni":"The Natural State","re":"South","po":3011524,"ar":137732,"sy":1836,"fa":"Birthplace of Bill Clinton (Hope, 1946); Walmart founded in Bentonville in 1962; the only US state that mines diamonds open to the public at Crater of Diamonds State Park"},
    {"n":"California","ca":"Sacramento","ni":"The Golden State","re":"West","po":39538223,"ar":423967,"sy":1850,"fa":"Hollywood and Silicon Valley; Yosemite, Big Sur and Death Valley; if it were a country it would be the world's 5th largest economy; more Nobel Prize winners than most nations"},
    {"n":"Colorado","ca":"Denver","ni":"The Centennial State","re":"West","po":5773714,"ar":269601,"sy":1876,"fa":"Rocky Mountain National Park; 58 peaks above 4,267m; skiing capital of North America; Denver sits exactly one mile above sea level — the Mile High City"},
    {"n":"Connecticut","ca":"Hartford","ni":"The Constitution State","re":"Northeast","po":3605944,"ar":14357,"sy":1788,"fa":"Home of the first written constitution in the Western world (Fundamental Orders, 1639); Yale University; the first hamburger was patented here in 1895 by Charlie Nagreen"},
    {"n":"Delaware","ca":"Dover","ni":"The First State","re":"Northeast","po":989948,"ar":6446,"sy":1787,"fa":"First state to ratify the US Constitution; corporate capital of America — 67% of Fortune 500 companies are incorporated here due to Delaware's favorable corporate law"},
    {"n":"Florida","ca":"Tallahassee","ni":"The Sunshine State","re":"South","po":21538187,"ar":170312,"sy":1845,"fa":"Kennedy Space Center at Cape Canaveral; Walt Disney World; the Everglades — the largest subtropical wilderness in the US; most visited US state by international tourists"},
    {"n":"Georgia","ca":"Atlanta","ni":"The Peach State","re":"South","po":10711908,"ar":153910,"sy":1788,"fa":"Birthplace of Martin Luther King Jr. and Jimmy Carter; home to Coca-Cola and CNN headquarters; Sherman's March to the Sea (1864) devastated the state during the Civil War"},
    {"n":"Hawaii","ca":"Honolulu","ni":"The Aloha State","re":"West","po":1455271,"ar":28313,"sy":1959,"fa":"Only US state made entirely of islands; Pearl Harbor attack launched the US into WWII; active Kilauea volcano; the most geographically isolated populated place on Earth"},
    {"n":"Idaho","ca":"Boise","ni":"The Gem State","re":"West","po":1839106,"ar":216443,"sy":1890,"fa":"World's largest producer of potatoes; Hells Canyon is the deepest river gorge in North America at 2,400m; Sun Valley was America's first destination ski resort (1936)"},
    {"n":"Illinois","ca":"Springfield","ni":"Land of Lincoln","re":"Midwest","po":12812508,"ar":149995,"sy":1818,"fa":"Abraham Lincoln's home state; Chicago invented the skyscraper and deep-dish pizza; the world's first nuclear reactor (Chicago Pile-1) was built under Stagg Field stadium in 1942"},
    {"n":"Indiana","ca":"Indianapolis","ni":"The Hoosier State","re":"Midwest","po":6785528,"ar":94326,"sy":1816,"fa":"Indianapolis 500 — world's largest single-day sporting event (250,000 spectators); birthplace of James Dean, Michael Jackson; the popcorn machine was invented in Chicago but popularised here"},
    {"n":"Iowa","ca":"Des Moines","ni":"The Hawkeye State","re":"Midwest","po":3190369,"ar":145746,"sy":1846,"fa":"Leads the US in corn, pork and eggs production; the Iowa caucuses traditionally open every presidential election season; Grant Wood's American Gothic was painted in Eldon, Iowa"},
    {"n":"Kansas","ca":"Topeka","ni":"The Sunflower State","re":"Midwest","po":2937880,"ar":213100,"sy":1861,"fa":"The geographic center of the contiguous US; The Wizard of Oz is set here; largest wheat-producing state; birthplace of Amelia Earhart (Atchison, 1897)"},
    {"n":"Kentucky","ca":"Frankfort","ni":"The Bluegrass State","re":"South","po":4505836,"ar":104656,"sy":1792,"fa":"Birthplace of bourbon whiskey — 95% of the world's supply is made here; the Kentucky Derby (1875) is the oldest continuously held major American sporting event"},
    {"n":"Louisiana","ca":"Baton Rouge","ni":"The Pelican State","re":"South","po":4657757,"ar":134382,"sy":1812,"fa":"New Orleans jazz, Mardi Gras and Creole cuisine; the only US state with a legal system based on Napoleonic Code; the Mississippi Delta blues music was born here"},
    {"n":"Maine","ca":"Augusta","ni":"The Pine Tree State","re":"Northeast","po":1362359,"ar":91633,"sy":1820,"fa":"Easternmost US state; lobster capital producing 80M lbs annually; Acadia National Park; birthplace of Stephen King; L.L.Bean was founded in Freeport in 1912"},
    {"n":"Maryland","ca":"Annapolis","ni":"The Old Line State","re":"Northeast","po":6177224,"ar":32131,"sy":1788,"fa":"Francis Scott Key wrote the Star-Spangled Banner after the Battle of Baltimore (1814); birthplace of Babe Ruth; Chesapeake Bay blue crab capital of the United States"},
    {"n":"Massachusetts","ca":"Boston","ni":"The Bay State","re":"Northeast","po":7029917,"ar":27336,"sy":1788,"fa":"Birthplace of the American Revolution; Harvard (1636) and MIT; home of the first public school (Boston Latin, 1635) and first free public library in the US"},
    {"n":"Michigan","ca":"Lansing","ni":"The Great Lakes State","re":"Midwest","po":10077331,"ar":250487,"sy":1837,"fa":"Detroit — the Motor City; Ford, GM and Chrysler born here; Motown Records launched; surrounded by four Great Lakes with more freshwater coastline than any other state"},
    {"n":"Minnesota","ca":"Saint Paul","ni":"Land of 10,000 Lakes","re":"Midwest","po":5706494,"ar":225163,"sy":1858,"fa":"Actually has 11,842 lakes; world-class Mayo Clinic in Rochester; birthplace of Bob Dylan and Prince; the Mississippi River begins here at Lake Itasca"},
    {"n":"Mississippi","ca":"Jackson","ni":"The Magnolia State","re":"South","po":2961279,"ar":125438,"sy":1817,"fa":"Birthplace of the blues and Elvis Presley (Tupelo, 1935); the Mississippi River forms its entire western border; last US state to ratify the 13th Amendment abolishing slavery (1995)"},
    {"n":"Missouri","ca":"Jefferson City","ni":"The Show Me State","re":"Midwest","po":6154913,"ar":180540,"sy":1821,"fa":"The Gateway Arch in St. Louis (192m) marks where westward expansion began; birthplace of Mark Twain; Kansas City jazz and BBQ traditions; the Pony Express started in St. Joseph"},
    {"n":"Montana","ca":"Helena","ni":"Big Sky Country","re":"West","po":1084225,"ar":380831,"sy":1889,"fa":"Third largest US state; Glacier National Park is the Crown of the Continent; more cattle than people; Battle of Little Bighorn — Custer's Last Stand (1876) took place near Hardin"},
    {"n":"Nebraska","ca":"Lincoln","ni":"The Cornhusker State","re":"Midwest","po":1961504,"ar":200330,"sy":1867,"fa":"Chimney Rock guided Oregon Trail settlers westward; birthplace of Warren Buffett; Kool-Aid was invented in Hastings in 1927; Arbor Day was first celebrated here in 1872"},
    {"n":"Nevada","ca":"Carson City","ni":"The Silver State","re":"West","po":3104614,"ar":286352,"sy":1864,"fa":"Las Vegas — entertainment capital of the world; the most arid US state; Area 51 has spawned decades of UFO legends; legal gambling was established here in 1931 during the Great Depression"},
    {"n":"New Hampshire","ca":"Concord","ni":"The Granite State","re":"Northeast","po":1377529,"ar":24214,"sy":1788,"fa":"Live Free or Die — no income tax AND no sales tax; first in the nation presidential primary since 1920; Robert Frost spent summers here; the Old Man of the Mountain was its symbol"},
    {"n":"New Jersey","ca":"Trenton","ni":"The Garden State","re":"Northeast","po":9288994,"ar":22591,"sy":1787,"fa":"Most densely populated US state; birthplace of Thomas Edison who invented the lightbulb in Menlo Park; Atlantic City boardwalk since 1870; more diners than any other state"},
    {"n":"New Mexico","ca":"Santa Fe","ni":"Land of Enchantment","re":"Southwest","po":2117522,"ar":314917,"sy":1912,"fa":"Santa Fe is the oldest US capital city (1610); Los Alamos was the birthplace of the atomic bomb; Roswell UFO incident (1947); ancient Pueblo cliff dwellings at Chaco Canyon"},
    {"n":"New York","ca":"Albany","ni":"The Empire State","re":"Northeast","po":20201249,"ar":141297,"sy":1788,"fa":"New York City — global capital of finance, arts and culture; the Statue of Liberty was France's gift; Niagara Falls; the first US capital city (NYC, 1789); Ellis Island welcomed 12M immigrants"},
    {"n":"North Carolina","ca":"Raleigh","ni":"The Tar Heel State","re":"South","po":10439388,"ar":139391,"sy":1789,"fa":"The Wright Brothers made the world's first powered flight at Kitty Hawk (December 17, 1903); birthplace of three US presidents; Great Smoky Mountains National Park"},
    {"n":"North Dakota","ca":"Bismarck","ni":"The Peace Garden State","re":"Midwest","po":779094,"ar":183108,"sy":1889,"fa":"Least visited US state; Theodore Roosevelt National Park's dramatic Badlands; an early-2000s oil boom transformed it into the fastest-growing US state for several years"},
    {"n":"Ohio","ca":"Columbus","ni":"The Buckeye State","re":"Midwest","po":11799448,"ar":116098,"sy":1803,"fa":"Birthplace of 7 US presidents; 24 of 29 Americans to fly in space were born here; Wright Brothers were from Dayton; Rock and Roll Hall of Fame in Cleveland"},
    {"n":"Oklahoma","ca":"Oklahoma City","ni":"The Sooner State","re":"South","po":3959353,"ar":181037,"sy":1907,"fa":"The 1889 Land Run — settlers raced to claim free land at the starting gun; Route 66 begins here; the Dust Bowl of the 1930s inspired Steinbeck's The Grapes of Wrath"},
    {"n":"Oregon","ca":"Salem","ni":"The Beaver State","re":"West","po":4237256,"ar":254799,"sy":1859,"fa":"Crater Lake — deepest US lake at 594m; Nike and Intel founded in the Portland area; Voodoo Doughnut; the Oregon Trail ended at Oregon City; Crater Lake is the bluest water on Earth"},
    {"n":"Pennsylvania","ca":"Harrisburg","ni":"The Keystone State","re":"Northeast","po":13002700,"ar":119280,"sy":1787,"fa":"Declaration of Independence signed at Independence Hall in Philadelphia (1776); Gettysburg battlefield; the first electronic computer (ENIAC) was built at UPenn in 1945"},
    {"n":"Rhode Island","ca":"Providence","ni":"The Ocean State","re":"Northeast","po":1097379,"ar":4001,"sy":1790,"fa":"Smallest US state (4,001 km²); first colony to declare independence from Britain (May 1776); Brown University; Newport's Gilded Age mansions hosted the wealthiest American families"},
    {"n":"South Carolina","ca":"Columbia","ni":"The Palmetto State","re":"South","po":5118425,"ar":82933,"sy":1788,"fa":"The Civil War began at Fort Sumter in Charleston Harbor (April 12, 1861); Francis Marion 'The Swamp Fox' pioneered guerrilla warfare here during the American Revolution"},
    {"n":"South Dakota","ca":"Pierre","ni":"The Mount Rushmore State","re":"Midwest","po":886667,"ar":199729,"sy":1889,"fa":"Mount Rushmore — four presidents carved into granite (60m tall faces); the Crazy Horse Memorial nearby will be the world's largest sculpture when complete; Sacred Black Hills of the Lakota Sioux"},
    {"n":"Tennessee","ca":"Nashville","ni":"The Volunteer State","re":"South","po":6910840,"ar":109153,"sy":1796,"fa":"Nashville — country music capital and Music City USA; Graceland (Elvis's home in Memphis); Jack Daniel's distillery in Lynchburg; Great Smoky Mountains National Park (most visited in the US)"},
    {"n":"Texas","ca":"Austin","ni":"The Lone Star State","re":"South","po":29145505,"ar":695662,"sy":1845,"fa":"Largest contiguous US state; an independent republic for 9 years (1836-1845); the NASA Johnson Space Center; the Alamo in San Antonio; the state's economy would rank 9th in the world"},
    {"n":"Utah","ca":"Salt Lake City","ni":"The Beehive State","re":"West","po":3271616,"ar":219882,"sy":1896,"fa":"Five national parks in one state: Arches, Zion, Bryce Canyon, Canyonlands, Capitol Reef; the Great Salt Lake is saltier than the ocean; Mormon pioneer heritage shaped its entire identity"},
    {"n":"Vermont","ca":"Montpelier","ni":"The Green Mountain State","re":"Northeast","po":643077,"ar":24906,"sy":1791,"fa":"Montpelier is the only US state capital without a McDonald's; produces 40% of US maple syrup; Ben & Jerry's ice cream was founded in Burlington in 1978; billboards are banned by state law"},
    {"n":"Virginia","ca":"Richmond","ni":"The Old Dominion","re":"South","po":8631393,"ar":110787,"sy":1788,"fa":"Birthplace of 8 US presidents — more than any other state; Jamestown (1607) was the first permanent English settlement in America; the Pentagon; Arlington National Cemetery"},
    {"n":"Washington","ca":"Olympia","ni":"The Evergreen State","re":"West","po":7705281,"ar":184661,"sy":1889,"fa":"Seattle — birthplace of Starbucks, Amazon, Boeing and grunge music; Mount Rainier (4,392m) is the most glaciated peak in the contiguous US; the Space Needle was built for the 1962 World's Fair"},
    {"n":"West Virginia","ca":"Charleston","ni":"The Mountain State","re":"South","po":1793716,"ar":62756,"sy":1863,"fa":"Split from Virginia during the Civil War in 1863 refusing to secede; New River Gorge — one of North America's oldest rivers; coal mining and Appalachian culture shaped its entire identity"},
    {"n":"Wisconsin","ca":"Madison","ni":"The Badger State","re":"Midwest","po":5893718,"ar":169635,"sy":1848,"fa":"America's dairy capital — produces 25% of US cheese; the Republican Party was founded in Ripon (1854); Milwaukee's brewing heritage gave America Pabst, Schlitz and Miller"},
    {"n":"Wyoming","ca":"Cheyenne","ni":"The Equality State","re":"West","po":576851,"ar":253335,"sy":1890,"fa":"First US territory to grant women the right to vote (1869); Yellowstone — the world's first national park (1872); Old Faithful geyser; least populated US state with 576,000 residents"},
]

def main():
    results = []
    for i, s in enumerate(states_raw):
        name = s["n"]
        print(f"  [{i+1}/{len(states_raw)}] {name}...", end=" ", flush=True)
        img = fetch_wiki_image(name)
        entry = dict(s)
        entry["im"] = img
        results.append(entry)
        print("ok" if img else "no image")
        time.sleep(0.3)

    with_img = sum(1 for r in results if r["im"])
    out = pathlib.Path("assets/world/american_states.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    sys.stdout.buffer.write(f"\n{len(results)} etats generees. Images: {with_img}/{len(results)} -> {out}\n".encode('utf-8'))

if __name__ == "__main__":
    main()
