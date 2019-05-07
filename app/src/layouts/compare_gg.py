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
    title='Emotion detection by Google vision vs Resnet18',
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
            html.H4('Room ID'),
            dcc.Dropdown(
                id='roomid',
                options=[{'value':roomid,'label':roomid} for roomid in DATA.df_e_gg.id_class.unique()],
                value = sorted(DATA.df_e_gg.id_class.unique())[0],
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
    dcc.Graph(id='graph_emotion_2',figure={'data':[],'layout':l}),
    
])



@app.callback(
    Output('graph_emotion_2', 'figure'),
    [
        Input('roomid', 'value'),
        Input('user_role', 'value'),
        Input('smoothness', 'value'),
    ])
def update_figure(roomid,user_role,smoothness):
    """
    Args:
        (int) : the id of teacher to get all class from
        user_role (list) : whose emotion to display 
    """
    user_role = [user_role] if user_role!='all' else ['teacher','student']
    # Get the single chosen class
    df_e = DATA.df_e[DATA.df_e.id_class==roomid].copy()
    df_e_gg = DATA.df_e_gg[DATA.df_e_gg.id_class==roomid].copy()
    df_e_mi = DATA.df_e_mi[DATA.df_e_mi.id_class==roomid].copy()


    # filter emotion with role
    df_e = df_e[df_e.user_role.isin(user_role)]
    df_e_gg = df_e_gg[df_e_gg.user_role.isin(user_role)]
    df_e_mi = df_e_mi[df_e_mi.user_role.isin(user_role)]
    d = []
    for df,model in zip([df_e,df_e_gg,df_e_mi],['Resnet18','Google Vision','Microsoft']):

        time_range = np.arange(0,df.time_video.max(),30)/60 # in minutes
        # Divide the time class to each blocks of 30s second
        df.loc[:,'time_video_cut'] = pd.cut(df.time_video,bins=np.arange(0,df.time_video.max(),30))
        emotion_mean_by_range = df.groupby('time_video_cut').emotion_score.mean()
        emotion_mean_by_range_smooth = utils.smooth(emotion_mean_by_range,smoothness)


        trace = go.Scatter(
            x = time_range,
            y = emotion_mean_by_range_smooth,
            mode='lines',
            name = model,
        )
        d.append(trace)

    return {'data':d,'layout':l} # layout defined on top

























