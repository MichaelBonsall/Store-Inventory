from database import getDatabase

dbname = getDatabase()
collection_name = dbname["ItemList"]

print(dbname.list_collection_names())