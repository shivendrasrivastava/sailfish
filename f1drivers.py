__author__ = 'Shiven'
import requests
import json
import pymongo
import sys

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


def start(starting_year, data_type="driverStandings"):
    url_prefix = "http://ergast.com/api/f1"

    for x in range(0, 4):
        year = str(starting_year+x)
        url = '{url_prefix}/{year}/{data_type}.json'.format(url_prefix=url_prefix, year=year, data_type=data_type)
        print url
        # read_data(url, year)


def help_message():
    print "Please enter atleast one argument (1st argument= Year, 2nd argument= data type)"

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        try:
            year = int(sys.argv[1])
        except ValueError:
            help_message()
            exit(1)
        if len(sys.argv) == 3:
            data_type = sys.argv[2]
            start(year, data_type)
        else:
            start(year)
    else:
        help_message()
