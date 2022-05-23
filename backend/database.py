# -----------------------------------------------------------
# File database definition - Mongo DB
# see file json (path) config/config.json
#
# (C) 2022 Marco Vannoli, Rome, Italy
# email marcovannoli@hotmial.it
# -----------------------------------------------------------

from config import get_config
from pymongo import MongoClient

data = get_config()

# get database mongo initialization
def get_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = data["connection_string"]

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[data["database"]]


# save inside database
def save_to_database(collection, data):
	collection.insert_one(data)

# perform query into mongo db
def find_query(collection,query,sort='',desc=-1,limit=0):
    if limit != 0 and sort == '':
       return collection.find(query).limit(limit)
    elif limit == 0 and sort != '':
       return collection.find(query).sort(sort, desc)
    elif limit != 0 and sort != '':
       return collection.find(query).sort(sort, desc).limit(limit)
    else:
       return collection.find(query)
    

def aggregation_collection(collection,aggregation):
    return collection.aggregate(aggregation)


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    
    # Get the database
    dbname = get_database()