"""
Inspect the emotion within class length
Display the emotion of all classes for a particular teacher
"""
import pandas as pd
import numpy as np
import calendar
from src.connectors import mongo
from src.connectors import mongo,queries
from src.plots import utils

from dash.dependencies import Input,Output,State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from plotly import graph_objs as go


from app import app
import DATA

"""
Choices:
    - teacher id
    - kid/teacher emotion to show
"""

# plot layout
l = go.Layout(
    hovermode='closest',
    title='Emotion during class taught by each teacher',
    showlegend=True,
    xaxis={
        'range':[0,60],
        'title':'Time',
        },
    yaxis={
        'range':[0,6],
        'title':'Feelings',
        }
)
options = dbc.Row([
        dbc.Col([
            html.H4('Emotion of'),
            dcc.RadioItems(
                id='user_role',
                options = [
                    {'label':'teacher','value':'teacher'},
                    {'label':'student','value':'student'},
                    {'label':'all','value':'all'},
                    ],
                value = 'student',
            ),
        ],md=4),
        dbc.Col([
            html.H4('Teacher'),
            dcc.Dropdown(
                id='teacherid',
                options=[{'value':teacherid,'label':DATA.df_u[DATA.df_u.id==teacherid].firstname} for teacherid in sorted(DATA.df_cl.teacherid.unique())],
                value = sorted(DATA.df_cl.teacherid.unique())[0],
            ),

        ],md=4),
        dbc.Col([
            html.H4('Smoothness'),
            dcc.Slider(
                id='smoothness',
                min=0,
                max=1,
                step=0.1,
                value=.3,
            ),
        ],md=4),

    ])


layout = html.Div([
    options,
    html.H4('Month'),
    dcc.Graph(id='graph_emotion',figure={'data':[],'layout':l}),
     dcc.RangeSlider(
        id='months',
        count=1,
        min=1,
        max=12,
        step=1,
        value=[1,12],
        marks = {i:calendar.month_name[i] for i in range(1,13)},
    ),

])



@app.callback(
    Output('graph_emotion', 'figure'),
    [
        Input('teacherid', 'value'),
        Input('user_role', 'value'),
        Input('months','value'),
        Input('smoothness', 'value'),
    ])
def update_figure(teacherid,user_role,months,smoothness):
    """
    Args:
        teacherid (int) : the id of teacher to get all class from
        user_role (list) : whose emotion to display 
        months (list) : Filter class by months
    """
    user_role = [user_role] if user_role!='all' else ['teacher','student']
    # Get all class taught by this teacher id
    df = DATA.df_e_cl[DATA.df_e_cl.teacherid==teacherid]

    # filter by month
    df = df[df.starttime.dt.month.isin(list(range(months[0],months[1]+1)))]

    # filter emotion with role
    df = df[df.user_role.isin(user_role)]
    d = []
    for c in sorted(df.id_class.unique()):

        df_sclass = df[df.id_class==c].copy()
        time_range = np.arange(0,df_sclass.time_video.max(),30)/60 # in minutes
        # Divide the time class to each blocks of 30s second
        # df_sclass['time_video_cut'] = pd.cut(df_sclass.time_video,bins=np.arange(0,df_sclass.time_video.max(),30))
        df_sclass.loc[:,'time_video_cut'] = pd.cut(df_sclass.time_video,bins=np.arange(0,df_sclass.time_video.max(),30))
        emotion_mean_by_range = df_sclass.groupby('time_video_cut').emotion_score.mean()
        emotion_mean_by_range_smooth = utils.smooth(emotion_mean_by_range,smoothness)


        trace = go.Scatter(
            x = time_range,
            y = emotion_mean_by_range_smooth,
            mode='lines',
            name = str(c),
        )
        d.append(trace)

    return {'data':d,'layout':l} # layout defined on top





