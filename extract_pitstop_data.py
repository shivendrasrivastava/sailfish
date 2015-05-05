__author__ = 'Shiven'
import requests
import json
import argparse
import mongoutils as db
from ergast_api_error import ErgastConnectionException


def get_url_data(url):
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        return r
    else:
        raise ErgastConnectionException("Could not connect with Ergast API..")


def read_data(url):
    r = get_url_data(url)
    data = json.loads(r.text)
    return data


def get_pitstop_collection():
    f1db = db.connect_mongo()
    posts = f1db.pitstop
    return posts


def insert_into_mongo(race):
    posts = get_pitstop_collection()
    posts.insert(race)


def remove_key(data, key):
    data.pop(key, None)
    return data


def build_url(year, round, driverId):
    url_prefix = "http://ergast.com/api/f1"
    url = '{url_prefix}/{year}/{round}/drivers/{driverId}/pitstops.json'.format(url_prefix=url_prefix, year=year,
                                                                                driverId=driverId, round=round)
    return url


def get_data_after_year(starting_year, ending_year, data_type="constructorStandings"):
    print "We will fetch the data for {type}".format(type=data_type)
    for year in range(starting_year, ending_year):
        for race_data in get_next_season_race_data(year, "alonso"):
            # print race_data
            for race in race_data:
                remove_key(race, "url")
                remove_key(race, "Circuit")
                print json.dumps(race)
                insert_into_mongo(race)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", choices=["pitstop"], help="Fetch type data")
    parser.add_argument("-s", "--start", help="Enter the start year", type=int)
    parser.add_argument("-e", "--end", help="Enter the end year", type=int)
    args = parser.parse_args()
    if args.type and args.start and args.end:
        get_data_after_year(args.start, args.end, args.type)
    else:
        parser.print_help()


def get_next_season_race_data(year, driver_id):
    race_round = 1

    while race_round < 20:
        url = build_url(year, race_round, driver_id)
        data = read_data(url)
        race_data = data["MRData"]["RaceTable"]["Races"]
        if race_data:
            yield race_data
        race_round += 1


if __name__ == '__main__':
    main()