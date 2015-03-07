__author__ = 'Shiven'
import requests
import json
import pymongo


def read_data(url, year):
    r = requests.get(url)
    data = json.loads(r.text)
    posts = connect_mongo()
    print "Details are as follows :-"
    for standings_list in data["MRData"]["StandingsTable"]["StandingsLists"]:
        for drivers_standings in standings_list["DriverStandings"]:
            document = {}
            print json.dumps(drivers_standings, indent=4)
            constructor = drivers_standings["Constructors"][0]
            document["constructor"] = remove_data(constructor)
            document["driver"] = remove_data(drivers_standings["Driver"])
            document["wins"] = drivers_standings["wins"]
            document["points"] = drivers_standings["points"]
            document["position"] = drivers_standings["position"]
            document["year"] = year
            json_doc = json.dumps(document)
            print json_doc
            posts.insert(document)


def connect_mongo():
    client = pymongo.MongoClient('localhost', 27017)
    db = client.f1db
    posts = db.test
    return posts


def remove_data(data):
    data.pop('url', None)
    return data


def start():
    url_part_1 = "http://ergast.com/api/f1/"
    url_part_2 = 2010
    url_part_3 = "/driverStandings.json"

    for x in range(0, 4):
        year = str(url_part_2+x)
        url = url_part_1 + year + url_part_3
        print url
        read_data(url, year)

start()
