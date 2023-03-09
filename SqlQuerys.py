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


# for item in FetchMenu():
#     print(item["name"])
#     print(item["price"])
#     print(item["description"])


def FetchAllergies():
    menuItem = []
    for item in db.Allergies.find({}):
        menuItem.append(item)
    return menuItem


# print(FetchAllergies())

def FetchGluten():
    Item = []
    for item in FetchAllergies():
        if (item["gluten"] == True):
            print(item["name"])
            Item.append(item["name"])
    return Item

# print(FetchGluten())


def FetchPeanuts():
    Item = []
    for item in FetchAllergies():
        if (item["peanuts"] == True):
            print(item["name"])
            Item.append(item["name"])
    return Item

# print(FetchPeanuts())


def FetchTreenuts():
    Item = []
    for item in FetchAllergies():
        if (item["treenuts"] == True):
            print(item["name"])
            Item.append(item["name"])
    return Item

# print(FetchTreenuts())


def FetchCelery():
    Item = []
    for item in FetchAllergies():
        if (item["celery"] == True):
            print(item["name"])
            Item.append(item["name"])
    return Item
# print(FetchCelery())


def FetchMustard():
    Item = []
    for item in FetchAllergies():
        if (item["mustard"] == True):
            print(item["name"])
            Item.append(item["name"])
    return Item

# print(FetchMustard())


def FetchEggs():
    Item = []
    for item in FetchAllergies():
        if (item["eggs"] == True):
            print(item["name"])
            Item.append(item["name"])
    return Item

# print(FetchEggs())


def FetchDairy():
    Item = []
    for item in FetchAllergies():
        if (item["milk"] == True):
            # print(item["name"])
            Item.append(item["name"])
    return Item

# print(FetchDairy())


def FetchSesame():
    Item = []
    for item in FetchAllergies():
        if (item["sesame"] == True):
            print(item["name"])
            Item.append(item["name"])
    return Item

# print(FetchSesame())


def FetchFish():
    Item = []
    for item in FetchAllergies():
        if (item["fish"] == True):
            print(item["name"])
            Item.append(item["name"])
    return Item

# print(FetchFish())


def FetchCrustaceans():
    Item = []
    for item in FetchAllergies():
        if (item["crustaceans"] == True):
            print(item["name"])
            Item.append(item["name"])
    return Item
# print(FetchCrustaceans())


def FetchMolluscs():
    Item = []
    for item in FetchAllergies():
        if (item["molluscs"] == True):
            print(item["name"])
            Item.append(item["name"])
    return Item

# print(FetchMolluscs())


def FetchSulphites():
    Item = []
    for item in FetchAllergies():
        if (item["sulphites"] == True):
            print(item["name"])
            Item.append(item["name"])
    return Item

# print(FetchSulphites())


def FetchLupin():
    Item = []
    for item in FetchAllergies():
        if (item["lupin"] == True):
            print(item["name"])
            Item.append(item["name"])
    return Item


# print(FetchLupin())
