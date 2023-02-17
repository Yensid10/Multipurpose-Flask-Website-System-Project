from pymongo import MongoClient
# from bson.objectid import ObjectId

client = MongoClient(
    'mongodb+srv://Theamzingu:Socr%40tis123@teamproject14.nnzfaib.mongodb.net/test')
db = client.Menu


def FetchMenu():
    names = []
    prices = []
    for item in db.Menu.find({}):
        names.append(item["name"])
        prices.append(item["price"])
    return names, prices


names, prices = FetchMenu()
