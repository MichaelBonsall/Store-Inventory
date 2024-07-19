from pymongo import MongoClient

def getDatabase():
    """
    Gets the database from mongoclient

    Returns:
        client['Items'] the client from mongoDB
    """
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)

    return client['Items']

if __name__ == "__main__":
    dbname = getDatabase()
