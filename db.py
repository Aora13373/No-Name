import pymongo
from flask import current_app, g



def get_db():
    if 'db' not in g:
        # Update this with the connection string to the Atlas cluster.
        client = pymongo.MongoClient()
        g.db = client.maps
    return g.db

        