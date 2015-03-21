__author__ = 'Shiven'
import pymongo


def connect_mongo():
    client = pymongo.MongoClient('localhost', 27017)
    db = client.f1db
    posts = db.test
    return posts