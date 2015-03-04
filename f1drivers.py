__author__ = 'Shiven'
import requests
import json
import pymongo


def read_data():
    url = 'http://ergast.com/api/f1/2010/driverStandings.json'
    r = requests.get(url)
    print r.headers.get('content-type')
    data = json.loads(r.text)
    print type(data)
    # print data["MRData"]["StandingsTable"]["StandingsLists"]
    posts = connect_mongo()
    print "Details are as follows :-"
    for standings_list in data["MRData"]["StandingsTable"]["StandingsLists"]:
        # print json.dumps(standings_list["DriverStandings"], indent=4)
        for drivers_standings in standings_list["DriverStandings"]:
            document = {}
            print json.dumps(drivers_standings, indent=4)
            constructor = drivers_standings["Constructors"][0]
            document["const"] = constructor
            document["driver"] = drivers_standings["Driver"]
            json_doc = json.dumps(document)
            print json_doc
            posts.insert(document)

    # formatted_data = json.dumps(data, sort_keys=True, indent=4)

    # print formatted_data


def connect_mongo():
    client = pymongo.MongoClient('localhost', 27017)
    db = client.f1db
    print "Database names are "
    print client.database_names()
    print "Collections in f1db are "
    print db.collection_names()
    posts = db.test
    print "Record in f1db.test are "
    print posts.find_one()
    return posts


read_data()
connect_mongo()
