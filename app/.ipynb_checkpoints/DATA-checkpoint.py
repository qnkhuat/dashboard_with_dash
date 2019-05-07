from src.connectors import mongo
from src.connectors import queries
from time import time
import pandas as pd

def init():
    global df_e,df_cl,df_u,df_e_cl,df_cl_e
    print('Initializing data')
    start = time()
    #df_e = queries.df_emotion([8513,7238,8453,8183,8486])
    df_e = queries.df_emotion()
    #df_e.to_csv('src/data/emotion_05042019.csv',index=False)
    #df_e = pd.read_csv('src/data/emotion_05042019.csv')
    df_cl = queries.df_classinfo()
    df_u = queries.df_user()


    # Emotion through time with added class info
    df_e_cl = df_e.merge(df_cl,left_on='id_class',right_on='roomid')
    assert df_e_cl.shape[0]==df_e.shape[0] , "Shape of Dataframe changed"


    # class info with emotion score
    #df_cl['emotion_score_mean'] =         df_e.groupby('id_class').emotion_score.mean()
    #df_cl['emotion_score_teacher_mean'] = df_e[df_e.user_role=='teacher'].groupby('id_class').emotion_score.mean()
    #df_cl['emotion_score_student_mean'] = df_e[df_e.user_role=='student'].groupby('id_class').emotion_score.mean()
    #df_cl_e = df_e.reset_index().merge(df_cl,left_on='id_class',right_on='roomid',how='right')
    # class info with emotion score
    df_cl_e = df_e.groupby('id_class').emotion_score.mean().to_frame().reset_index().merge(df_cl,left_on='id_class',right_on='roomid',how='right')
    assert df_cl_e.shape[0]==df_cl.shape[0], "Shape of Dataframe changed"










    print(f'Finished initialize data in {time()-start}')


