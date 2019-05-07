# have to run this first
import DATA 
DATA.init()

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from plotly import graph_objs as go

from app import app
from src.layouts import layout_test
from src.layouts import emotion_during_class,overall,student,compare_gg
from src.layouts import navbar
import datetime


app.layout = html.Div([
    #html.H3(f"Time : {DATA.now} ,actual : {datetime.datetime.now()}"),
    dbc.Container([
        navbar.layout,
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
    ]),
    html.Div(id='hidden-div', style={'display':'none'})
])


# update graphs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    # original path name start with a /
    pathname = pathname if pathname is None  else "/".join(pathname.split('/')[2:])
    if pathname == emotion_during_class.__name__.split('.')[-1]:
        layout = emotion_during_class.layout
    elif pathname == overall.__name__.split('.')[-1]:
        layout = overall.layout 
    elif pathname == student.__name__.split('.')[-1]:
        layout = student.layout 
    elif pathname == compare_gg.__name__.split('.')[-1]:
        layout = compare_gg.layout 
    elif pathname =='':
        layout = emotion_during_class.layout
    else:
        layout = '404'
    return layout




if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0',port=8050)










