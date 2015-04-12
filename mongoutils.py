__author__ = 'Shiven'
import pymongo


def connect_mongo():
    client = pymongo.MongoClient('localhost', 27017)
    db = client.f1db
    return db


def aggregate_driver_country(db):
    pipeline = [{'$group': {'_id': {'driver': "$driver.driverId", 'nation': "$driver.nationality", 'year': "$year"}}},
                {'$group': {'_id': {'yr': "$_id.year", 'nat': "$_id.nation"}, 'count': {'$sum': 1}}},
                {'$sort': {'_id': 1}}]
    # pipeline = [{'$group': {'_id': {'driver' : "$driver.driverId", 'nation': "$driver.nationality"}}},
    # {'$group': {'_id': "$_id.nation", 'count': {'$sum': 1}}}]
    return db.command('aggregate', 'test', pipeline=pipeline)
