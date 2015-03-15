__author__ = 'Shiven'

import f1drivers as f1
import plotly.plotly as py
import plotly.graph_objs as graph
import random


def extract_data():
    print "Connecting Mongo"
    posts = f1.connect_mongo()
    construct_lists(posts)


def construct_lists(posts):
    print "Constructing Lists"
    data_list = []
    years = posts.distinct("year")
    for year in years:
        print year
        result = get_data(posts, year)

        points = result["points"]
        position = result["position"]

        trace = graph.Scatter(x=points, y=position, mode='markers',
                              name=year, marker=graph.Marker(color=get_color(),
                                                               size=12, line=graph.Line(color='white', width=0.5)))
        print trace
        data_list.append(trace)

    data = graph.Data(data_list)
    layout = graph.Layout(
        title='Drivers Vs Position Summary',
        xaxis=graph.XAxis(
            title='Position',
            showgrid=False,
            zeroline=False
        ),
        yaxis=graph.YAxis(
            title='Drivers',
            showline=False
        )
    )
    fig = graph.Figure(data=data, layout=layout)
    url = py.plot(fig, filename="f1test1")
    print url


def get_data(posts, year):
    cursor = posts.find({"year": year})
    points = []
    position = []
    for doc in cursor:
        points.append(doc["driver"]["driverId"])
        position.append(doc["position"])

    return {"points": points, "position": position}


def get_color():
    r = lambda: random.randint(0,255)
    color = ('#%02X%02X%02X' % (r(), r(), r()))
    return color

if __name__ == "__main__":
    extract_data()