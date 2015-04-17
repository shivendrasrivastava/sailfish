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


def aggregate_constructor_driver_ferrari(db):
    pipeline = [{'$match': {"constructor.name": "Ferrari"}},
                {'$group': {'_id': {"year": "$year", "constructor_name": "$constructor.name",
                                    "driver": "$driver.driverId", "position": "$position"}}},
                {'$sort': {'_id': 1}}]
    return db.command('aggregate', 'test', pipeline=pipeline)


def aggregate_constructor_driver_mclaren(db):
    pipeline = [{'$match': {"constructor.name": "McLaren"}},
                {'$group': {'_id': {"year": "$year", "constructor_name": "$constructor.name",
                                    "driver": "$driver.driverId", "position": "$position"}}},
                {'$sort': {'_id': 1}}]
    return db.command('aggregate', 'test', pipeline=pipeline)


def aggregate_constructor_driver(db, driver_id):
    pipeline = [{'$match': {"driver.driverId": driver_id}},
                {'$group': {'_id': {"year": "$year", "constructor": "$constructor.name",
                                    "driver": "$driver.driverId", "position": "$position"}}}, {'$sort': {'_id.year': 1}}]
    return db.command('aggregate', 'test', pipeline=pipeline)