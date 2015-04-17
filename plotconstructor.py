__author__ = 'Shiven'
import mongoutils as mongo
import plot
import plotly.plotly as py
import plotly.graph_objs as graph


def extract_data():
    db = mongo.connect_mongo()
    driver_id_list = ["michael_schumacher", "barrichello", "hakkinen"]
    trace_list = []
    for driver in driver_id_list:
        result = mongo.aggregate_constructor_driver(db, driver)
        print result
        if result["ok"] == 1.0:
            result = result["result"]
            print result

            years = []
            constructors = []
            positions = []
            for dat in result:
                years.append(dat["_id"]["year"])
                constructors.append(dat["_id"]["constructor"])
                positions.append(dat["_id"]["position"])

            trace = graph.Scatter(x=years, y=positions, name=driver, text=constructors, mode="lines")
            trace_list.append(trace)

    data = graph.Data(trace_list)
    plot_url = py.plot(data, filename="F1 Constructor Vs Driver")
    print plot_url


if __name__ == "__main__":
    extract_data()
