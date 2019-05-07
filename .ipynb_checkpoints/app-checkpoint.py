import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from src.plots import avg_emotion
from src.connectors import mongo


db = mongo.mongo_connect()



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


data,layout = avg_emotion.data(db)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider',figure={'data':data,'layout':layout}),
    #dcc.Interval(
    #    id='interval-component',
    #    interval=1*1000,
    #    n_intervals=0
    #    )
])
if __name__ == '__main__':
    app.run_server(debug=True)
