import pymongo
import certifi

client = pymongo.MongoClient("mongodb+srv://m001-student:m001-mongodb-basics@sandbox.dstos.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client.premier_league.goals

####    Query #1
print("\n----------------------------------\t\tQuery #1\t\t----------------------------------\n")
print("How many players have scored over 100 goals?\n")
result1 = db.count_documents({
    "goals": {"$gt": 100}
})
print(result1)


###     Query #2
print("\n----------------------------------\t\tQuery #2\t\t----------------------------------\n")
print("List the players and their nations, who have had +200 goals contributions (goals+assists)? \n")
result2 = db.find({
    "$expr":{ 
        "$gt":[{
            "$sum" :["$goals","$assists"]
        }, 
        200] 
    }
});
for item in result2: 
    name = item.get("name")
    nation = item.get("country")
    row = [name, nation]
    print("{: >20} {: >20}".format(*row))

###     Query #3
print("\n----------------------------------\t\tQuery #3\t\t----------------------------------\n")
print("List all the player's names and clubs who have scored over 50 goals and 50 assists\n")
result3 = db.find({
    "goals": {"$gt": 50}, 
    "assists": {"$gt": 50}
})

for item in result3: 
    name = item.get("name")
    nation = item.get("country")
    club = item.get("club")
    row = [name, nation, club]
    print("{: >25} {: >25} {: >25}".format(*row))



###     Query #4
print("\n----------------------------------\t\tQuery #4\t\t----------------------------------\n")
print("Top 3 players who had the most goals+assists? (List name and total contributions)\n")

result4 = db.aggregate([
    {
        "$project" : {
            'name': '$name',
            'goals' : '$goals',
            'assists' : '$assists',
            'totalSum' : { '$add' : [ '$assists', '$goals' ] },
        }
    },
    { "$limit": 3 }
])

for item in result4: 
    name = item.get("name")
    goals = item.get("goals")
    assists = item.get("assists")
    totalSum = item.get("totalSum")
    club = item.get("club")
    row = [name, goals, assists, totalSum, club]
    print("{: >25} {: >25} {: >25} {: >25}".format(*row))


###     Query #5
print("\n----------------------------------\t\tQuery #5\t\t----------------------------------\n")
print("List the top 7 player names,clubs and nations, who had the best goals/game ratio?\n")

result5 = db.aggregate([
    {
        "$project" : {
            'name': '$name',
            'goals' : '$goals',
            'club': '$club',
            'country': '$country',
            'appearances' : '$appearances',
            'ratio' : { '$divide' : [ '$goals', '$appearances' ] },
        }
    },
    {"$sort": {"ratio": pymongo.DESCENDING}},
    { "$limit": 7 }

])
for item in result5: 
    name = item.get("name")
    goals = item.get("goals")
    club = item.get("club")
    nation = item.get("country")
    apps = item.get("appearances")
    ratio = round(item.get("ratio"),3)
    row = [name, goals, apps, club, nation, ratio]
    print("{: >25} {: >10} {: >10} {: >25} {: >25} {: >10}".format(*row))

###     Query #6
print("\n------------\t\t------------\t\tQuery #6\t\t------------\t\t------------\n")
print("How many goals in the Premier League did English players score? French Players?\n")
result6 = db.aggregate([
    {
        "$group" : {"_id" : "$country", "goals": {"$sum" : "$goals"}}
    },
    {"$sort": {"goals": pymongo.DESCENDING}},
    {
        "$match": {
               "$or": [{"_id": {"$eq": "France"}}, {"_id": {"$eq": "England"}}]
        }
    }
])

for item in result6: 
    nation = item.get("_id")
    goals = item.get("goals")
    row = [nation, goals]
    print("{: >10} {: >10} goals".format(*row))

###     Query #7
print("\n------------\t\t------------\t\tQuery #7\t\t------------\t\t------------\n")
print("How many different nationalities have played in the Premier League?\n")
result7 = db.aggregate([
    {
        "$group" : {"_id" : "$country", "Country": {"$addToSet" : "$country"}}
    },
    {"$count": "Nations"}
])
for item in result7:
    print(item)

###     Query #8
print("\n------------\t\t------------\t\tQuery #8\t\t------------\t\t------------\n")
print("How many Belgian, Croatian, or Brazilian players appeared in at least 100 matches in the Premier League?\n")
result8 = db.aggregate([
    {
        "$group" : {"_id" : "$country", "appearances": {"$addToSet": "$appearances"}}
    },
    # {"$sort": {"appearances": pymongo.DESCENDING}},
    {
        "$match": {
               "$or": [{"_id": "Belgium"}, {"_id": "Croatia"}, {"_id": "Brazil"}], 
        }
    },
    {"$project":{
        "apps": { "$filter": { "input": "$appearances", "as": "item", "cond": {"$gte": ["$$item", 100]}}},
        }
    },
    {"$project": { "label": { "$size":"$apps" }}}
])

for item in result8:
    count = item.get("_id")
    total = item.get("label")
    row = [count, total]
    print("{: >5}: {: >5} Players".format(*row))


###     Query #9
print("\n------------\t\t------------\t\tQuery #9\t\t------------\t\t------------\n")
print("List the players who assisted 70+ goals and appeared in 300+ matches\n")
result9 = db.find({
    "assists": {"$gte": 70}, 
    "appearances": {"$gte": 300}
})

for item in result9:
    name = item.get("name")
    assists = item.get("assists")
    apps = item.get("appearances")
    row = [name, assists, apps]
    print("{: >18} {: >10}  {: >10} ".format(*row))