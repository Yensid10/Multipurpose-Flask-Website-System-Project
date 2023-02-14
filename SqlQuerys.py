from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient(
    'mongodb+srv://Theamzingu:Socr%40tis123@teamproject14.nnzfaib.mongodb.net/test')
db = client.Menu


def FetchDescription():
    menuItem = db.Menu.find_one({"name": "Guacamole and chips"})
    print(menuItem["name"])
    print(menuItem["description"])


def FetchMenu():
    for menuItem in db.Menu.find({}):
        print(menuItem)


def FetchAllergies():
    for menuItem in db.Menu.find({}):
        oid = ObjectId(menuItem["_id"])
        allergies = db.Allergies.find_one({"_id": oid})
        print(allergies)


FetchDescription()
FetchMenu()
FetchAllergies()
