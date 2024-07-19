import DBUtility
import pandas as pd
from PIL import Image
import shortestPath


def makeBatch():
    """
    Used to make a batch to run. Asks user in stdin for IDs for the desired items to be
    put in the batch

    Returns:
        a Datafraame containing the items in the batch

    """
    batch = pd.DataFrame()
    while True:
        input1 = input("Enter an item ID or q to finish.")
        if input1.lower() == "q": break
        item = DBUtility.searchByID(input1)
        if type(item) == str: #not a valid ID
            print("The given ID did not match any items. Please try again")
            continue
        if item.iloc[0]['count'] == 0:
            print("The selected item has none left. Please try another item")
            continue
        print("Item added:\n", item)
        batch = pd.concat([batch, item], ignore_index=True)
    
    batch.sort_values('shelf_location') #sorts first by shelf location as whole, then by shelf. it works.
    sortedBatch = sortBatch(batch)

    return sortedBatch


"""
TODO: pickedItems and dnf dataframes need fixin
"""
def runBatch(batch):
    """
    Runs the batch in arg. Asks for ID when the item is found and moves through the batch,
    opening pictures so the user can reference them when looking for the item

    Args:
        the desired batch to be run

    Returns:
        PickedItems: A dataframe containing the items found and collected by the user
        dnf: A dataframe containing the items that the user could not find
    """
     
    dnf = pd.DataFrame()
    pickedItems = pd.DataFrame()

    for i in range(batch.shape[0]):
        print("Item ID:", batch.at[i,"_id"], "  Item Name:", batch.at[i, "item_name"], \
              "  Shelf Location:", batch.at[i, "shelf_location"], "  Count:", batch.at[i, "count"], \
              "  Price:", batch.at[i, "price"])
        imgFile = batch.at[i, "image_path"]
        if pd.isna(imgFile):
            img = Image.open("images/no-image-available.jpg")
        else: img = Image.open(imgFile)
        img.show()
       
        while True:
            input1 = input("Please enter the Item ID to proceed to the next item. Or enter DNF if there was no item on shelf.")
            if input1 == batch.at[i, "_id"]:
                pickedItems = pd.concat([pickedItems, batch.loc[[i]]], ignore_index=True)
                #subtract 1 from count
                DBUtility.storeDB["ItemList"].update_one({"_id": batch.at[i,"_id"]}, {"$set":{"count": str(int(batch.at[i, "count"]) - 1)}})
                break
            elif input1.lower() == "dnf": #couldnt find item, add to dnf dataframe
                dnf = pd.concat([dnf, batch.loc[[i]]], ignore_index=True)
                print("Item was marked as DNF.")
                break
            else: print("Incorrect ID number. ")
    return pickedItems, dnf


def sortBatch(batch):
    """
    Sorts the batch into the most efficient path for running it

    Args:
        Batch: a batch to  be sorted

    Returns:
        A sorted batch
    """
    shelfsNeeded = []
    for index, row in batch.iterrows():
        shelf = row['shelf_location'][:2]
        if shelf not in shelfsNeeded:
            shelfsNeeded.append(shelf)
    if len(shelfsNeeded) < 3:
        batch.sort_values('shelf_location', ignore_index=True)
        sortedBatch = batch
    else:
        #then further order by more precise location
        #put batch in path order
        sortedBatch = pd.DataFrame()
        path = shortestPath.findOptimalPath(shelfsNeeded)
        for shelf in path:
            currentShelf = pd.DataFrame()
            for index, row in batch.iterrows():
                if int(row['shelf_location'][:2]) - 1 == shelf: 
                    row = row.to_frame().transpose()
                    currentShelf = pd.concat([currentShelf, row], ignore_index=True) 
            currentShelf.sort_values('shelf_location', ignore_index=True)
            sortedBatch = pd.concat([sortedBatch, currentShelf], ignore_index=True) 
    return sortedBatch


def main():
    batch = makeBatch()
    pickedItems, dnf = runBatch(batch)
    print(pickedItems)
    print(dnf)

if __name__ == "__main__":
    main()