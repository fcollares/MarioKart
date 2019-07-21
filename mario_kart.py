import requests
import bs4 as bs

def get_content_from_url(url):
    r = requests.get(url)
    soup = bs.BeautifulSoup(r.content,'lxml')
    return soup

def get_character_bonuses(soup):
    tables = soup.find_all("table",class_="wikitable")
    for table in tables:
        header = table.find("tr")
        if header.get_text().strip() == "Character Bonuses":
            break
    rows = table.find_all("tr")
    rows.pop(0)
    headings_temp = rows.pop(0).find_all("th")
    data = []
    headings = []
    for h in headings_temp:
        headings.append(h.get_text().strip())
    data.append(headings)

    sizes = get_character_sizes(soup)
    small = []
    medium = []
    large = []
    for row in rows:
        name = row.find("th").get_text().strip()
        stats = [x.get_text().strip() for x in row.find_all("td")]
        for i in range(len(stats)):
            if stats[i] == '-':
                stats[i] = '0'
        stats = list(map(int,stats))
        if name in sizes["S"]:
            small.append([name] + stats)
        elif name in sizes["M"]:
            medium.append([name] + stats)
        elif name in sizes["L"]:
            large.append([name] + stats)
    data.append(small)
    data.append(medium)
    data.append(large)
    return data

def get_character_sizes(soup):
    gal_text = soup.find_all("div", class_="gallerytext")
    sizes = {"S":[],"M":[],"L":[]}
    for t in gal_text:
        name = t.find("a").get_text()
        if "Small" in t.get_text():
            sizes["S"].append(name)
        elif "Medium" in t.get_text():
            sizes["M"].append(name)
        elif "Large" in t.get_text():
            sizes["L"].append(name)
    return sizes


def get_vehicle_stats(soup):
    tables = soup.find_all("table",class_="wikitable")
    for table in tables:
        header = table.find("tr")
        if header.get_text().strip() == "Vehicle Stats":
            break
    
    rows = table.find_all("tr")
    rows.pop(0)
    headings_temp = rows.pop(0).find_all("th")
    headings = []
    data = []
    for h in headings_temp:
        headings.append(h.get_text().strip())
    data.append(headings[:8])
    small = []
    medium = []
    large = []
    current_heading = headings[0]
    for row in rows:
        row_data = row.find_all("td")
        if row_data != []:
            row_data[0] = row_data[0].get_text().strip()
            for i in range(1,8):
                datum = row_data[i].get_text()
                if datum == "-":
                    row_data[i] = 0
                else:
                    row_data[i] = int(datum)
            if "Small" in current_heading:
                small.append(row_data[:8])
            elif "Medium" in current_heading:
                medium.append(row_data[:8])
            elif "Large" in current_heading:
                large.append(row_data[:8])
        else:
            current_heading = (row.find("th").get_text())
    data.append(small)
    data.append(medium)
    data.append(large)
    return data

def all_char_vec_combos(c,v):
    cross_join = []
    for j in range(3):
        characters = c[j]
        vehicles = v[j]
        for char in characters:
            for vehic in vehicles:
                cross = []
                cross.append(char[0] + " in " + vehic[0])
                for i in range(1,len(char)):
                    cross.append(char[i] + vehic[i])
                cross_join.append(cross)
    return cross_join

def get_data():
    mario_kart_wiki_url = "https://www.mariowiki.com/Mario_Kart_Wii"
    soup = get_content_from_url(mario_kart_wiki_url)
    char_bonuses = get_character_bonuses(soup)
    headings = (char_bonuses[0])
    headings[0] += ",Vehicle"
    v_stats = get_vehicle_stats(soup)

    c = all_char_vec_combos(char_bonuses[1:], v_stats[1:])

    #drift_sorted = sorted(c,key=lambda x: (x[headings.index("Drift")], x[headings.index("Mini-Turbo")], x[headings.index("Speed")]),reverse=True)
    return headings, c

    
