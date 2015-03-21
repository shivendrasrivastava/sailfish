__author__ = 'Shiven'
import plotly.plotly as py
import plotly.graph_objs as graph
import colorutils as color


def scatter(xaxis, yaxis, year, green):
    trace = graph.Scatter(x=xaxis, y=yaxis, mode='markers', name=year,
                          marker=graph.Marker(color=color.color_as_hex(green),
                                              size=12, line=graph.Line(color='white', width=0.5)))
    return trace


def plot_data(data_list):
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