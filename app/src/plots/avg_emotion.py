import plotly.graph_objs as go
from src.connectors import mongo
import numpy as np
import pandas as pd


def get_sclass(df,class_id): return df[df.id_class == class_id] # get single class

def avg_emotion(df,class_id):
    df_sclass = get_sclass(df,class_id)
    if len(df_sclass) < 1:
        return None
    time_range = np.arange(0,df_sclass.time_video.max(),60)/60 # in minutes
    emotion_mean_by_range = df_sclass.groupby('time_video_code').emotion_score.mean()
    trace = go.Scatter(
        x = time_range,
        y = emotion_mean_by_range,
        mode='lines',
        name = str(class_id)
    )
    return trace



def data(db):
    print('Preparing data')
    df = mongo.mongo_get_col(db,'emotion_data')
    # the increasing ladder score of emotion
    emotion_score = {
        'fear':0,
        'disgust':1,
        'angry':2,
        'sad':3,
        'neutral':4,
        'happy':5,
        'surprise':6,
        None:-1
    }
    df['emotion_score'] = df.emotion.map(emotion_score)
    # Devide the time
    df['time_video_code'] = pd.cut(df.time_video,bins=np.arange(0,3000,60))
    data = []
    for class_id in df.id_class.unique():
        df_temp = avg_emotion(df,class_id)
        if df_temp:
            data.append(df_temp)
    layout = go.Layout(
        hovermode='closest',
        xaxis={'range':[0,60]},
        yaxis={'range':[0,6]}
        
    )
    return data,layout

        
    


