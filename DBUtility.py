from database import getDatabase
from pandas import DataFrame
import random

storeDB = getDatabase()


def searchByID(ID):
    """
    Searches and returns the matching item for the given ID

    Args:
        ID: a string containing the ID of the desired item

    Returns:
        A dataframe containing the item
    """ 
    result = storeDB["ItemList"].find({"_id": ID})
    result_df = DataFrame(result)
    if (len(result_df.columns) == 0):
        return "No item matched the given ID number."
    return result_df
    

def searchByName(str):
    """
    Searches and returns the matching item for the given name

    Args:
        str: a string containing the name of the desired item

    Returns:
        A dataframe containing the first instance of a matching name
    """
    result = storeDB["ItemList"].find({"item_name": {"$regex": str, "$options": "i"}}) #this is *probably* slow but idc
    result_df = DataFrame(result)
    if (len(result_df.columns) == 0):
        return "No items matched your search." 
    return result_df

"""
FOR TESTING ONLY. DO NOT USE IN PROD
this would be a serious security issue in a real environment lol
"""
def clearDB():
    storeDB["ItemList"].drop()


def printDB():
    """
    Prints the entire database to terminal
    """
    return DataFrame(storeDB["ItemList"].find({}))

#specifications is arr. should be : seperated. ie weight:20. No whitespace

def insertItem(name, shelf_location, count, price, category,  image_path=None, specifications = None):
    """
    Inserts a new item into the database. Generates an ID, and asks the user if they're sure if an item with a matching
    name is entered

    Args:
        name: the desired name of the item
        shelf_location: the item's loation on a shelf in the format 00-00-00-00, aisle-block-shelf-location
        count: the number of items on shelf
        price: the price of the item
        category: the category of the item
        image_Path: the path of the image in images folder, format is images/file_name
        specifications: a list containing extra specifications as desired. Format colon seperated. ie weight:20. No whitespace
    """

    duplicateCheck = searchByName(name)
    if isinstance(duplicateCheck, DataFrame): #searchByName() returns a string if it doesnt find anything. this is checking for that
        while True:
            input1 = input("The item(s) above has the same name as provided. Insert anyway?? (Y/N)")
            if input1.lower() == "n":
                print("Insert aborted.")
                return
            elif input1.lower() == "y": break
            else: print("Input not recognized")

    while True:
        id = str(random.randint(0, 99999999))
        if (len(id) < 8): id = id.zfill(8)
        if searchByID(id) == "No item matched the given ID number.": break

    item = {
        "_id": id,
        "item_name": name,
        "shelf_location": shelf_location,
        "count": count,
        "price": price,
        "category": category,
        "image_path": image_path
    } 
    if specifications is not None:
        for spec in specifications:
            s = spec.split(":")
            item[s[0]] = s[1]
    storeDB["ItemList"].insert_one(item)

def deleteByID(ID):
    """
    Deletes an item in the database matching the provided ID

    Args:
        ID: the string ID of the item you want to delete
    """
    storeDB["ItemList"].find_one_and_delete({"_id": ID})


def updateCount(ID, count):
    """
    Updates the count of an item in the database

    Args:
        ID: The ID of the item you want to update
        count: The new count of the item 
    """
    if type(searchByID(ID)) is not DataFrame:
        print("There is no item by that ID in the database. Please try again")
    else: storeDB["ItemList"].update_one({"_id": ID},{ "$set":{ "count": count}})

#a = ["weight:25", "height:20 in", "length:20 in"]
#insertItem(name="Garfield Suit", shelf_location="01-50-04-06", count="59", price="999.99", category="Clothing", image_path=None)
#print(searchByName("Garfield Kart"))
updateCount("3134426", "99")
#clearDB()
print(printDB())

