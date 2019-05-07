from src.connectors import mongo
from src.connectors import pymysql
import numpy as np
import pandas as pd
from datetime import datetime
from flask_caching import Cache
from app import app

TIMEOUT = 60*60*8  # refresh data each 8 hours
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

@cache.memoize(timeout=TIMEOUT)
def df_emotion(class_ids=None,col_name='emotion_data'):
    """
    Args:
    class_ids(list): a list of class id to retrieve data, If None get all of it
    """
    db = mongo.mongo_connect()
    if class_ids:
        df = mongo.mongo_query(db[col_name],{'id_class':{'$in':class_ids}})
    else:
        df = mongo.mongo_get_col(db,col_name)
    # Divide the time video to each 30s cuts
    df['time_video_cut'] = pd.cut(df.time_video,bins=np.arange(0,df.time_video.max(),30))

    # the increasing ladder score of emotion
    emotion_score = {
        'fear':0,
        'disgust':1,
        'angry':2,
        'sad':3,
        'neutral':4,
        'happy':5,
        'surprise':6,
        None:4 # if don't spot face=> neutral
    }
    df['emotion_score'] = df.emotion.map(emotion_score)
    return df


@cache.memoize(timeout=TIMEOUT)
def df_classinfo():
    # not keep all of theme
    keep_cols = ['day_learned','is_completed','studentid','lessonid','lessonname','roomid','star','starttime','teacherid','kidname']

    db = mongo.mongo_connect()
    df = mongo.mongo_get_col(db,'class_info')
    df = df[keep_cols]
    df.starttime = df.starttime.apply(lambda x : datetime.fromtimestamp(int(x)) if isinstance(x,str) else df.starttime)
    # remove duplicates by room id
    df.drop_duplicates(subset='roomid',inplace=True)
    return df


@cache.memoize(timeout=TIMEOUT)
def emotion_w_classinfo():
    df_e = df_emotion()
    df_cl = df_classinfo()
    df = df_e.merge(df_cl,left_on='id_class',right_on='roomid')
    assert df.shape[0]==df_e.shape[0] , "Shape of Dataframe changed"
    return df

@cache.memoize(timeout=TIMEOUT)
def now(): return datetime.now()
    


@cache.memoize(timeout=TIMEOUT)
def df_user():
    keep_cols = ['username','kid_name','id','firstname','lastname','kid_sex',
            'lastaccess','kid_birthday','pictures']
#     keep_cols = ['*']
    db = pymysql.sql_connect()
    #df = pymysql.sql_table('mdl_user',db)
    df = pymysql.sql_query(f"SELECT {','.join(keep_cols)} FROM mdl_user;",con=db);
    df.lastaccess= df.lastaccess.apply(lambda x : datetime.fromtimestamp(int(x)) )
    df['fullname'] = df['firstname'] 
    return df


@cache.memoize(timeout=TIMEOUT)
def df_slots():
    keep_cols = ['id','schedulerid','starttime','teacherid','notice']
    db = pymysql.sql_connect()
    #df = pymysql.sql_table('mdl_scheduler_slots',db)
    df = pymysql.sql_query(f"SELECT {','.join(keep_cols)} FROM mdl_scheduler_slots;",con=db);
    df.starttime = df.starttime.apply(lambda x : datetime.fromtimestamp(int(x)))
    return df


@cache.memoize(timeout=TIMEOUT)
def df_appts():
    keep_cols = ['id','slotid','studentid','status_completed']
    db = pymysql.sql_connect()
    #df = pymysql.sql_table('mdl_scheduler_appointment',db)
    df = pymysql.sql_query(f"SELECT {','.join(keep_cols)} FROM mdl_scheduler_appointment;",con=db);
    return df







