import requests
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pymongo
import certifi


client = pymongo.MongoClient("mongodb+srv://m001-student:m001-mongodb-basics@sandbox.dstos.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client.premier_league

# print(client)
player = {
    "name": "testing",
    "goals": 100
}

db.goals.insert_one(player)

# playerName = []
# points = []
# assists = []
# rebounds = []
# games = []

# url = "https://www.nba.com/stats/alltime-leaders/"


# s = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=s)
# driver.get(url)

# for i in range(1,27):



#     time.sleep(0.5)
#     driver.find_element(By.CLASS_NAME, "stats-table-pagination__next").click()
#     time.sleep(0.5)
