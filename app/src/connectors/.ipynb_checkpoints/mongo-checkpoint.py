from pymongo import MongoClient
import pandas as pd

def mongo_connect(host='35.187.248.148',port=27017,database='restfulapi',collection='emotion'):
    client = MongoClient(host,port)
    db = client[database]
    return db

def mongo_query(col,query):
    """
    col(collection of mongodb)
    queyry 
    """
    cursor  = col.find(query)
    df = pd.DataFrame(list(cursor))
    return df

def mongo_get_col(db,col):
    """ 
    Get collection as dataframe
    """
    cursor  = db[col].find()
    df = pd.DataFrame(list(cursor))
    return df
