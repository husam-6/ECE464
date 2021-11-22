from bs4 import BeautifulSoup
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pymongo
import certifi

#This file scrapes data off of the official Premier League website (all time statistics)
#The scraped data is stored on a MongoDB cluster with the intention of applying various queries
#to demonstrate understanding


#lists to store documents to be entered into MongoDB database
players = []
assists = []
apps = []

#Function to scrape the data off of the Official Premier League Statistics page
def scrapeData(url, option):
    count=0
    players = []

    #Set up selenium driver to walk through each page
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)

    driver.get(url)

    #Accept cookies alert
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "js-accept-all-close").click()
    time.sleep(1)

    #Loop through all pages of premier league players
    while count<2497:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("tbody", class_="statsTableContainer")
        for row in table.findAll("tr"):
            #Gather data
            count+=1 
            # goalRank.append(row.find("strong").text)
            player = {}
            player["name"] = row.find("a", class_="playerName").find("strong").text.strip()
            #For goals
            player["country"] = row.find(class_="playerCountry").text
            tmp = row.find("span", class_="badge-image-container")
            if tmp:
                player["club"] = tmp.nextSibling.text.strip()
            else: 
                player["club"] = '-'
            
            #For goals
            if option == 1:
                player["goals"] = row.find(class_="mainStat").text
            #For assists
            elif option == 2:
                player["assists"] = row.find(class_="mainStat").text
            #For appearances
            elif option == 3:
                player["appearances"] = row.find(class_="mainStat").text
            players.append(player)
        
        #Click next arrow button
        time.sleep(0.25)
        driver.find_element(By.CLASS_NAME, "paginationNextContainer").click()
        # time.sleep(0.25)
    return players

#Function to insert assists and appearances into the MongodB cluster
def updateDocs(attribute, newStat):
    try: 
        for item in newStat: 
            db.goals.update_one({"name": item.get("name")}, {"$set": {attribute: item.get(attribute)}})
        print(f"Updated {len(newStat)} documents")
    except: 
        print('An erorr occured - Players were not updated')


#For goals, country, club, 
url = "https://www.premierleague.com/stats/top/players/goals?co=1&se=-1&co=1&cl=-1&iso=-1&po=-1?se=-1"
# players = scrapeData(url,1)

client = pymongo.MongoClient("mongodb+srv://m001-student:m001-mongodb-basics@sandbox.dstos.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client.premier_league
try:
    db.goals.insert_many(players)
    print(f'Inserted {len(players)} articles')
except:
    print('An error occurred - Players were not stored to db')

#For assists stat
url2 = "https://www.premierleague.com/stats/top/players/goal_assist?se=-1"
# assists = scrapeData(url2,2)
# updateDocs("assists", assists)

#For appearances stat
url3 = "https://www.premierleague.com/stats/top/players/appearances?se=-1"
apps = scrapeData(url3,3)
updateDocs("appearances", apps)


# for i in range(len(players)):
#     print("{name}\t\t\t{country}\t\t\t{club}\t\t\t{goals}".format(**players[i]))


