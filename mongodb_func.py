
import pymongo
from pymongo import MongoClient

def get_max_id(mongo_uri, db_name, collection_name):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    total_documents = collection.count_documents({}) 

    client.close()

    return total_documents

def check_value_exists(mongo_uri, db_name, collection_name, field, value):

    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    query = {field: value}

    
    document = collection.find_one(query)

    client.close()

    return document is not None
def insert_if_cookie_unique(mongo_uri, db_name, collection_name, cookie_value):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    query = {"cookie": cookie_value}
    existing_document = collection.find_one(query)

    if existing_document:

        
        client.close()
        return False  

    cookie = {}
    cookie["cookie"] = cookie_value  
    collection.insert_one(cookie)


    client.close()

    
    return True  