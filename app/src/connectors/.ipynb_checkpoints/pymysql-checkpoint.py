import mysql.connector as sql
import pandas as pd

def sql_connect(host='42.113.207.169',
                database='uat_lms',
                user='topkid',
                password='yKRnqa96Sw7gEleCjuwrDIfpdqcxBLHjjfJccXsfrabc'):
    db_connection = sql.connect(host=host, database=database, user=user, password=password)
    return db_connection

def sql_query(query,con):
    df = pd.read_sql(query,con=con)
    return df

def sql_table(table,con):
    df = pd.read_sql(f"SELECT * FROM {table}",con=con)
    return df