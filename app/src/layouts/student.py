import pandas as pd
import numpy as np
import calendar
import datetime
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
l1 = go.Layout(
    hovermode='closest',
    title='Emotion of each class',
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

l2 = go.Layout(
    hovermode='closest',
    title='Overall class',
    showlegend=True,
    xaxis={
        'type':'date',
        'range':[DATA.df_cl_e.starttime.dt.date.min(),DATA.df_cl_e.starttime.dt.date.max()],
        'title':'Time',
        },
    yaxis={
        'range':[0,6],
        'title':'Feelings',
        },
    bargap = .99,

)

graphs = html.Div(
   dbc.Row([
        dbc.Col([
            dcc.Graph(id='student_emotion_class',figure={'data':[],'layout':l1}),
        ],md=6),
        dbc.Col([
            dcc.Graph(id='student_emotion_overall',figure={'data':[],'layout':l1}),
        ],md=6),
    ])
)


##### INFO 
info = html.Div(
    id = 'user_info'
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
            html.H4('Student ID'),
            dcc.Dropdown(
                id='studentid',
                options=[{'value':studentid,'label':DATA.df_cl[DATA.df_cl.studentid==studentid].kidname.iloc[0]} for studentid in sorted(DATA.df_cl.studentid.unique())],
                value = sorted(DATA.df_cl.studentid.unique())[0],
            )
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
    html.H3(),
    info,
    graphs
])


@app.callback(
    Output('user_info','children'),
    [Input('studentid','value')])
def update_figure(studentid):   
    df_u = DATA.df_u[DATA.df_u.id==studentid]
    div = html.Div([
            html.H3(F"My name is {df_u.kid_name.values[0]}"),
            dbc.Row([
                dbc.Col([
                    html.P(f"My mom is {df_u['firstname'].values[0]}"),
                    html.P(f"Total booked classes : {int(len(DATA.df_appts[DATA.df_appts.studentid==studentid])/2)}"),
                    html.P(f"Last accecss : {df_u.lastaccess.dt.time.values[0]} {df_u.lastaccess.dt.date.values[0]}"),
                ],md=6),
                dbc.Col([
                    html.P(f"I'm learning at : Level 2 Unit 1 Lesson 1"),
                    html.P(f"My 🎁: {df_u.kid_birthday.values[0]}"),
                    html.P(f"Joined time : "),
                ],md=6),
                ]),
            ])
    return div
    

@app.callback(
        Output('student_emotion_overall','figure'),
        [Input('studentid','value'),
        Input('smoothness', 'value'),
        Input('user_role', 'value'),
            ])
def update_figure1(studentid,smoothness,user_role):
    if user_role == 'teacher':
        emotion_col_name = 'emotion_score_teacher'
    elif user_role == 'student':
        emotion_col_name = 'emotion_score_kid'
    else:
        emotion_col_name = 'emotion_score'

    df = DATA.df_cl_e[DATA.df_cl_e.studentid == studentid].copy()
    d = []
    for c in sorted(df.roomid.unique()):
        df_sclass = df[df.roomid== c].copy()
        trace = go.Bar(
                x = df_sclass.starttime.dt.date,
                y = df_sclass[emotion_col_name],
                name = str(c),
                width=6*60*60*1000, # 6 hours
                )
        d.append(trace)

    return {'data':d,'layout':l2}




@app.callback(
    Output('student_emotion_class', 'figure'),
    [
        Input('studentid', 'value'),
        Input('user_role', 'value'),
        #Input('smoothness', 'value'),
    ])
def update_figure2(studentid,user_role):
    """
    Args:
        teacherid (int) : the id of teacher to get all class from
        user_role (list) : whose emotion to display 
        months (list) : Filter class by months
    """
    user_role = [user_role] if user_role!='all' else ['teacher','student']
    # Get all class taught by this teacher id
    df = DATA.df_e_cl[DATA.df_e_cl.studentid==studentid]

    # filter by month
    #df = df[df.starttime.dt.month.isin(list(range(months[0],months[1]+1)))]

    # filter emotion with role
    df = df[df.user_role.isin(user_role)]
    d = []
    for c in sorted(df.id_class.unique()):
        df_sclass = df[df.id_class==c].copy()
        time_range = np.arange(0,df_sclass.time_video.max(),30)/60 # in minutes
        # Divide the time class to each blocks of 30s second
        df_sclass.loc[:,'time_video_cut'] = pd.cut(df_sclass.time_video,bins=np.arange(0,df_sclass.time_video.max(),30))

        emotion_mean_by_range = df_sclass.groupby('time_video_cut').emotion_score.mean()
        emotion_mean_by_range_smooth = utils.smooth(emotion_mean_by_range,.5)

        trace = go.Scatter(
            x = time_range,
            y = emotion_mean_by_range_smooth,
            mode='lines',
            name = str(c),
        )
        d.append(trace)

    return {'data':d,'layout':l1} # layout defined on top



