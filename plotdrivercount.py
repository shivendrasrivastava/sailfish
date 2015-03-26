__author__ = 'Shiven'
import pymongo
import plotly.plotly as py
import plotly.graph_objs as graph
import collections


def extract_data():
    print "Connecting Mongo"
    client = pymongo.MongoClient('localhost', 27017)
    db = client.f1db
    result = run_query(db)
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

            print country_years
            print driver_count

            trace = graph.Bar(x=country_years, y=driver_count, name=nationality)
            trace_list.append(trace)

        trace_list[:] = trace_list[:5]
        data = graph.Data(trace_list)
        plot_url = py.plot(data, filename='F1 Country Data')
        print plot_url


def construct_query():
    pipeline = [{'$group': {'_id': {'driver': "$driver.driverId", 'nation': "$driver.nationality", 'year': "$year"}}},
                {'$group': {'_id': {'yr': "$_id.year", 'nat': "$_id.nation"}, 'count': {'$sum': 1}}},
                {'$sort': {'_id': 1}}]
    # pipeline = [{'$group': {'_id': {'driver' : "$driver.driverId", 'nation': "$driver.nationality"}}},
    # {'$group': {'_id': "$_id.nation", 'count': {'$sum': 1}}}]
    return pipeline


def run_query(db):
    pipeline = construct_query()
    return db.command('aggregate', 'test', pipeline=pipeline)


if __name__ == "__main__":
    extract_data()