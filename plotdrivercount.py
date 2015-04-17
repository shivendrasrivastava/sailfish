__author__ = 'Shiven'
import collections
import mongoutils as mongo
import plot


def extract_data():
    print "Connecting Mongo"
    db = mongo.connect_mongo()
    result = mongo.aggregate_driver_country(db)
    if result["ok"] == 1.0:
        result = result["result"]
        print result
        # data_list = []
        country_dict = collections.defaultdict(dict)
        for dat in result:
            year = dat["_id"]["yr"]
            nationality = dat["_id"]["nat"]
            country_dict[nationality][year] = dat["count"]

        trace_list = []
        for nationality in country_dict.keys():
            country_years = [year for year in country_dict[nationality]]
            driver_count = [country_dict[nationality][year] for year in country_years]

            trace = plot.trace_bar(country_years, driver_count, nationality)
            print trace['name']
            country_list = ["Polish", "Indian", "Brazilian", "British", "Italian", "German"]
            if trace["name"] in country_list:
                trace_list.append(trace)

        plot.plot_bar(trace_list, 'stack', 'F1 Country Data')


if __name__ == "__main__":
    extract_data()