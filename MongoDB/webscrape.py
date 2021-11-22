from bs4 import BeautifulSoup
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pymongo
import certifi

players = []
assists = []
# playerName = []
# countries = []
# goals = []
# goalRank = []
# club = []
def scrapeData(url):
    players = []

    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)

    driver.get(url)

    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "js-accept-all-close").click()
    time.sleep(1)

    for i in range(1,125):
        time.sleep(0.25)
        driver.find_element(By.CLASS_NAME, "paginationNextContainer").click()
        time.sleep(0.25)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("tbody", class_="statsTableContainer")
        for row in table.findAll("tr"): 
            # goalRank.append(row.find("strong").text)
            player = {}
            player["name"] = row.find("a", class_="playerName").find("strong").text.strip()
            player["country"] = row.find(class_="playerCountry").text
            #For goals
            # player["goals"] = row.find(class_="mainStat").text
            #For assists
            player["assists"] = row.find(class_="mainStat").text
            tmp = row.find("span", class_="badge-image-container")
            if tmp:
                player["club"] = tmp.nextSibling.text.strip()
            else: 
                player["club"] = '-'
            
            players.append(player)
        if player["name"] == " Richard Walker":
            break
        
    return players


url = "https://www.premierleague.com/stats/top/players/goals?co=1&se=-1&co=1&cl=-1&iso=-1&po=-1?se=-1"
# players = scrapeData(url)

client = pymongo.MongoClient("mongodb+srv://m001-student:m001-mongodb-basics@sandbox.dstos.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client.premier_league
try:
    db.goals.insert_many(players)
    print(f'Inserted {len(players)} articles')
except:
    print('An error occurred - Players were not stored to db')


url2 = "https://www.premierleague.com/stats/top/players/goal_assist?se=-1"
assists = scrapeData(url2)

to_ignore = ['key1', 'key2', 'key3', ...]
filtered_dict = {key: value for (key, value) in original_dict.items() if key.rsplit('_', 1)[-1] not in to_ignore}

# try: 
for item in assists: 
    db.goals.update_one({"name": {"$eq": item.get("name")}}, item)

print(f"Updated {len(assists)} documents")
# except: 
    # print('An erorr occured - Players were not updated')

# for i in range(len(players)):
    # print("{name}\t\t\t{country}\t\t\t{club}\t\t\t{goals}".format(**players[i]))





# for i in range(1,1000):
#     url = f"https://www.premierleague.com/players/{i}"

#     # driver.set_page_load_timeout(5)
#     # time.sleep(1)
#     driver.get(url)
#     time.sleep(0.5)

#     html = driver.page_source
#     soup = BeautifulSoup(html, "html.parser")

#     name = soup.find("div", class_="name")
#     if name == None: 
#         continue
#     playerName.append(name.text)
#     # print(name.text)

#     country = soup.find("span", class_="playerCountry")
#     countries.append(country.text)
#     # print(country.text)

#     pos = soup.find("div", class_="info")
#     position.append(pos.text)
#     # print(pos.text)

#     for row in soup.find("tbody").find_all('tr'):
#         # print(row.th.text)
#         if row.th.text == "Appearances":
#             appearances.append(row.td.text)
#         elif row.th.text == "Goals":
#             goals.append(row.td.text)
#         elif row.th.text == "Assists":
#             assists.append(row.td.text)


# for i in range(0,1000):
#     print(f"{playerName[i]}\t\t{countries[i]}\t\t{position[i]}\t\t{appearances[i]}\t\t{goals[i]}\t\t{assists[i]}")
