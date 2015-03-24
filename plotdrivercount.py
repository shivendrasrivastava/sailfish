__author__ = 'Shiven'
import pymongo
import plotly.plotly as py
import plotly.graph_objs as graph


def extract_data():
    print "Connecting Mongo"
    client = pymongo.MongoClient('localhost', 27017)
    db = client.f1db
    result = run_query(db)
    if result["ok"] == 1.0:
        result = result["result"]
        print result
        data_list = []
        for dat in result:
            count = dat["count"]
            nat = dat['_id']["nat"]
            year = dat["_id"]["yr"]

            trace = graph.Bar(x=year, y=count, name=nat)
            data_list.append(trace)

    data = graph.Data(data_list)
    layout = graph.Layout(barmode='group')
    fig = graph.Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='grouped-bar')
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