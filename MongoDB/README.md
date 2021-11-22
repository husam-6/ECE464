## Husam Almanakly - Databases Assignment #2

This program has two files attached: <webscraper.py> and <mongoQueries.py>. The file 
labelled webscraper.py scrapes data off of the official Premier League website (all time statistics)

https://www.premierleague.com/stats/top/players/goals?co=1&se=-1&co=1&cl=-1&iso=-1&po=-1?se=-1

The program creates a Selenium Chrome Driver that steps through each page of players, while 
the BeautifulSoup library was utilized to take the HTML from each page and parse the text. 
The following stats were collected: Player Name, Nationality, current club ('-' if 
inactive/retired), # of career goals, assists, and appearances made in the Premier League. 
The data collected from each page was then stored in a MongoDB Database (on an Atlas 
cluster). To collect the data, run the command with the BeautifulSoup and Selenium 
libraries installed: 

# python3 webscraper.py

The second program included, titled mongoQueries.py, tests this database with various 
test queries. Examples include listing all the players with +50 goals and +50 assists, 
listing the players who have had +200 goal contributions (assists+goals), and listing the 
players with the best Goal/Game ratio. After connecting successfully to the MongoDB database
using PyMongo, run the script with 

# python3 mongoQueries.py
