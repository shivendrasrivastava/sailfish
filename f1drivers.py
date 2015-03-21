__author__ = 'Shiven'
import requests
import json
import argparse
import mongoutils as db


def read_data(url, year):
    r = requests.get(url)
    data = json.loads(r.text)
    posts = db.connect_mongo()
    # print "Details are as follows :-"
    for standings_list in data["MRData"]["StandingsTable"]["StandingsLists"]:
        for drivers_standings in standings_list["DriverStandings"]:
            document = {}
            # print json.dumps(drivers_standings, indent=4)
            constructor = drivers_standings["Constructors"][0]
            document["constructor"] = remove_key(constructor, 'url')
            document["driver"] = remove_key(drivers_standings["Driver"], 'url')
            document["wins"] = int(drivers_standings["wins"])
            document["points"] = float(drivers_standings["points"])
            document["position"] = int(drivers_standings["position"])
            document["year"] = year
            json_doc = json.dumps(document)
            print json_doc
            posts.insert(document)


def remove_key(data, key):
    data.pop(key, None)
    return data


def build_url(year, data_type):
    url_prefix = "http://ergast.com/api/f1"
    url = '{url_prefix}/{year}/{data_type}.json'.format(url_prefix=url_prefix, year=year, data_type=data_type)
    return url


def get_data_after_year(starting_year, ending_year, data_type="driverStandings"):
    print "We will fetch the data for {type}".format(type=data_type)
    for year in range(starting_year, ending_year):
        url = build_url(str(year), data_type)
        print url
        read_data(url, year)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", choices=["driverStandings", "drivers"], help="Fetch type data")
    parser.add_argument("-s", "--start", help="Enter the start year", type=int)
    parser.add_argument("-e", "--end", help="Enter the end year", type=int)
    args = parser.parse_args()
    if args.type and args.start and args.end:
        get_data_after_year(args.start, args.end, args.type)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
