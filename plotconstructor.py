__author__ = 'Shiven'
import mongoutils as mongo
import plot
import plotly.plotly as py
import plotly.graph_objs as graph


def extract_data():
    db = mongo.connect_mongo()
    driver_id_list = ["michael_schumacher", "barrichello"]
    trace_list = []
    for driver in driver_id_list:
        result = mongo.aggregate_constructor_driver(db, driver)
        print result
        if result["ok"] == 1.0:
            result = result["result"]
            print result

            years_driver = []
            constructors = []
            positions_driver = []
            for dat in result:
                years_driver.append(dat["_id"]["year"])
                constructors.append(dat["_id"]["constructor"])
                positions_driver.append(dat["_id"]["position"])

            trace_driver = graph.Scatter(x=years_driver, y=positions_driver, name=driver, text=constructors, mode="lines+markers")

            trace_list.append(trace_driver)

    constructor_list = ["ferrari"]
    for constructor in constructor_list:
        result_constructor = mongo.aggregate_constructor_by_year(db, constructor)
        if result_constructor["ok"] == 1.0:
            result_constructor = result_constructor["result"]
            print result_constructor
            years_constructor = []
            positions_constructor = []
            for data in result_constructor:
                years_constructor.append(data["_id"]["year"])
                positions_constructor.append(data["_id"]["position"])

            trace_constructor = graph.Scatter(x=years_constructor, y=positions_constructor, name=constructor, mode="lines+markers")
            trace_list.append(trace_constructor)

    data_graph = graph.Data(trace_list)
    plot_url = py.plot(data_graph, filename="F1 Constructor Vs Driver")
    print plot_url


if __name__ == "__main__":
    extract_data()
