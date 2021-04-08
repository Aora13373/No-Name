from pymongo import MongoClient
from flask import current_app, g

def get_db():
    '''Setting up connection to the databse / verifying the connection'''

    if 'db' not in g:
        client = MongoClient("mongodb+srv://hakon:123@studio.r7myl.mongodb.net/testing?retryWrites=true&w=majority") 
        g.db = client.FactBook    
        return g.db
    else:
        return g.db