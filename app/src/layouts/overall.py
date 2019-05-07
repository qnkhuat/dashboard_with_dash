"""
Inspect the emotion within class length
Display the emotion of all classes for a particular teacher
"""
import pandas as pd
import numpy as np
from src.connectors import mongo
from src.connectors import mongo,queries

from dash.dependencies import Input,Output,State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from plotly import graph_objs as go


from app import app
import DATA


### Emotion graph by time
d1 = []
for role in ['student','teacher','all']:
    role = [role] if role!='all' else ['student','teacher']
    #df = DATA.df_cl_e[DATA.df_cl_e.user_role.isin(role)]
    df = DATA.df_cl_e
    d1.append(go.Bar(
        x=df.starttime.dt.hour,
        y=df.emotion_score)
        )
l1 = go.Layout(
    hovermode='closest',
    title="Average of all class by start time in day",
    xaxis={'range':[0,24],'title':'Time','dtick':1},
    yaxis={'range':[0,6],'title':'Feelings'},
)
g1 = dcc.Graph(id='emotion_by_start_time',
        figure={'data':d1,'layout':l1})


graphs = html.Div(
        dbc.Row([
            dbc.Col([
                g1,
                ],md=6)
            ]),
        )


layout = html.Div([
    graphs
    ])

