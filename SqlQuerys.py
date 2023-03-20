from pymongo import MongoClient
# from bson.objectid import ObjectId

client = MongoClient(
    'mongodb+srv://Theamzingu:Socr%40tis123@teamproject14.nnzfaib.mongodb.net/test')
db = client.Menu


def FetchMenu():
    """
    Retrieve the names and prices of all items in the 'Menu' collection of the connected MongoDB database.

    Returns:
    names: list of strings representing the names of each item in the 'Menu' collection.
    prices: list of floats representing the prices of each item in the 'Menu' collection.
    """
    names = []
    prices = []
    for item in db.Menu.find({}):
        names.append(item["name"])
        prices.append(item["price"])
    return names, prices


def FetchAllergies():
    """
    Retrieve all items in the 'Allergies' collection of the connected MongoDB database.

    Returns:
    menuItem: list of dictionaries representing each item in the 'Allergies' collection.
    """
    menuItem = []
    for item in db.Allergies.find({}):
        menuItem.append(item)
    return menuItem

def FetchGluten():
    """
    Retrieve a list of all items in the 'Allergies' collection that contain gluten.

    Returns:
    Item: list of strings representing the names of all items in the 'Allergies' collection that contain gluten.
    """
    Item = []
    for item in FetchAllergies():
        if (item["gluten"] == True):
            Item.append(item["name"])
    return Item

def FetchPeanuts():
    """
    Retrieve a list of all items in the 'Allergies' collection that contain peanuts.

    Returns:
    Item: list of strings representing the names of all items in the 'Allergies' collection that contain peanuts.
    """
    Item = []
    for item in FetchAllergies():
        if (item["peanuts"] == True):
            Item.append(item["name"])
    return Item

def FetchTreenuts():
    """
    Retrieve a list of all items in the 'Allergies' collection that contain tree nuts.

    Returns:
    Item: list of strings representing the names of all items in the 'Allergies' collection that contain tree nuts.
    """
    Item = []
    for item in FetchAllergies():
        if (item["treenuts"] == True):
            Item.append(item["name"])
    return Item

def FetchCelery():
    """
    Retrieve a list of all items in the 'Allergies' collection that contain celery.

    Returns:
    Item: list of strings representing the names of all items in the 'Allergies' collection that contain celery.
    """
    Item = []
    for item in FetchAllergies():
        if (item["celery"] == True):
            Item.append(item["name"])
    return Item

def FetchMustard():
    """
    Retrieve a list of all items in the 'Allergies' collection that contain mustard.

    Returns:
    Item: list of strings representing the names of all items in the 'Allergies' collection that contain mustard.
    """
    Item = []
    for item in FetchAllergies():
        if (item["mustard"] == True):
            Item.append(item["name"])
    return Item

def FetchEggs():
    """
    Retrieve a list of all items in the 'Allergies' collection that contain eggs.

    Returns:
    Item: list of strings representing the names of all items in the 'Allergies' collection that contain eggs.
    """
    Item = []
    for item in FetchAllergies():
        if (item["eggs"] == True):
            Item.append(item["name"])
    return Item

def FetchDairy():
    """
    Retrieve a list of all items in the 'Allergies' collection that contain milk.

    Returns:
    Item: list of strings representing the names of all items in the 'Allergies' collection that contain milk.
    """
    Item = []
    for item in FetchAllergies():
        if (item["milk"] == True):
            Item.append(item["name"])
    return Item

def FetchSesame():
    """
    Retrieve a list of all items in the 'Allergies' collection that contain sesame.

    Returns:
    Item: list of strings representing the names of all items in the 'Allergies' collection that contain sesame.
    """
    Item = []
    for item in FetchAllergies():
        if (item["sesame"] == True):
            Item.append(item["name"])
    return Item

def FetchFish():
    """
    Retrieve a list of all items in the 'Allergies' collection that contain fish.

    Returns:
    Item: list of strings representing the names of all items in the 'Allergies' collection that contain fish.
    """
    Item = []
    for item in FetchAllergies():
        if (item["fish"] == True):
            Item.append(item["name"])
    return Item

def FetchCrustaceans():
    """
    Retrieve a list of all items in the 'Allergies' collection that contain crustaceans.

    Returns:
    Item: list of strings representing the names of all items in the 'Allergies' collection that contain crustaceans.
    """
    Item = []
    for item in FetchAllergies():
        if (item["crustaceans"] == True):
            Item.append(item["name"])
    return Item

def FetchMolluscs():
    """
    Retrieve a list of all items in the 'Allergies' collection that contain molluscs.

    Returns:
    Item: list of strings representing the names of all items in the 'Allergies' collection that contain molluscs.
    """
    Item = []
    for item in FetchAllergies():
        if (item["molluscs"] == True):
            Item.append(item["name"])
    return Item

def FetchSulphites():
    """
    Retrieve a list of all items in the 'Allergies' collection that contain sulphites.

    Returns:
    Item: list of strings representing the names of all items in the 'Allergies' collection that contain sulphites.
    """
    Item = []
    for item in FetchAllergies():
        if (item["sulphites"] == True):
            Item.append(item["name"])
    return Item

def FetchLupin():
    """
    Retrieve a list of all items in the 'Allergies' collection that contain lupin.

    Returns:
    Item: list of strings representing the names of all items in the 'Allergies' collection that contain lupin.
    """
    Item = []
    for item in FetchAllergies():
        if (item["lupin"] == True):
            Item.append(item["name"])
    return Item