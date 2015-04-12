__author__ = 'Shiven'

import plot
import colorutils as color
import mongoutils as db


def extract_data():
    print "Connecting Mongo"
    database = db.connect_mongo()
    posts = database.test
    construct_lists(posts)


def construct_lists(posts):
    print "Constructing Lists"
    data_list = []
    years = posts.distinct("year")
    for index, year in enumerate(years):
        print year

        result = get_data(posts, year)

        points = result["points"]
        position = result["position"]

        trace = plot.scatter(points, position, year, color.get_green(len(years), index))

        data_list.append(trace)

    plot.plot_drivers_position(data_list)


def get_data(posts, year):
    cursor = posts.find({"year": year})
    points = []
    position = []
    for doc in cursor:
        points.append(doc["driver"]["driverId"])
        position.append(doc["position"])

    return {"points": points, "position": position}


if __name__ == "__main__":
    extract_data()