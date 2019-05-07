from src.connectors import mongo
from src.connectors import queries
from time import time
import pandas as pd
from flask_caching import Cache

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def init():
    global df_e,df_e_gg,df_e_mi,df_cl,df_u,df_e_cl,df_e_cl_gg,df_cl_e,df_appts,df_slots,now
    print('Initializing data')
    start = time()
    now = queries.now()
    #df_e = queries.df_emotion([8513,7238,8453,8183,8486])
    #df_e = queries.df_emotion(col_name = 'emotion_data_gg')
    #df_e.to_csv('src/data/emotion_gg_12042019.csv',index=False)
    df_e = pd.read_csv('src/data/emotion_10042019.csv')
    df_cl = queries.df_classinfo()
    df_u = queries.df_user()

    df_slots = queries.df_slots()
    df_appts = queries.df_appts()


    # Emotion through time with added class info
    df_e_cl = df_e.merge(df_cl,left_on='id_class',right_on='roomid')
    assert df_e_cl.shape[0]==df_e.shape[0] , "Shape of Dataframe changed"

    # Emotion through time with added class info
    df_e_gg = pd.read_csv('src/data/emotion_gg_12042019.csv')
    df_e_cl_gg = df_e_gg.merge(df_cl,left_on='id_class',right_on='roomid')
    assert df_e_cl_gg.shape[0]==df_e_gg.shape[0] , "Shape of Dataframe changed"

    df_e_mi = pd.read_csv('src/data/emotion_mi_24042019.csv')
    df_e_cl_mi = df_e_mi.merge(df_cl,left_on='id_class',right_on='roomid')
    assert df_e_cl_mi.shape[0]==df_e_mi.shape[0] , "Shape of Dataframe changed"


    
    df_cl_e = df_cl.copy()
    df_cl_e['emotion_score_teacher'] = df_cl_e.roomid.map(df_e[df_e.user_role=='teacher'].groupby('id_class').emotion_score.mean().to_dict())
    df_cl_e['emotion_score_kid'] = df_cl_e.roomid.map(df_e[df_e.user_role=='student'].groupby('id_class').emotion_score.mean().to_dict())
    df_cl_e['emotion_score'] = df_cl_e.roomid.map(df_e.groupby('id_class').emotion_score.mean().to_dict())
    assert df_cl_e.shape[0]==df_cl.shape[0], "Shape of Dataframe changed"
    


    print(f'Finished initialize data in {time()-start}')

    # return with .copy() to avoid modifying the global variable
    #return  dotdict({
    #        'df_e':df_e.copy(),
    #        'df_cl':df_cl.copy(),
    #        'df_u':df_u.copy(),
    #        'df_e_cl':df_e_cl.copy(),
    #        'df_cl_e':df_cl_e.copy(),
    #        })

