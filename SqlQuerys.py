from pymongo import MongoClient
# from bson.objectid import ObjectId

client = MongoClient(
    'mongodb+srv://Theamzingu:Socr%40tis123@teamproject14.nnzfaib.mongodb.net/test')
db = client.Menu


def FetchMenu():
    menuItem = []
    for item in db.Menu.find({}):
        menuItem.append(item)
    return menuItem


for item in FetchMenu():
    print(item["name"])
    print(item["price"])
    print(item["description"])
