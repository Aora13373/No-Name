from pymongo import MongoClient
from flask import current_app, g



def get_db():
    '''Docstring'''
    # First we verify that 'db' is not empty
    if 'db' is None:
        raise ValueError('There is currently nothing inside db')
        
    # Setting the required information in order to establish the connection between db and g
    elif 'db' not in g:
        client = MongoClient("mongodb+srv://hakon:123@studio.r7myl.mongodb.net/testing?retryWrites=true&w=majority") 
        g.db = client.FactBook    
        return g.db
    
    # We are certain that db is not empty and that it has been connected with g. so we simply return that connection.
    else:
        return g.db