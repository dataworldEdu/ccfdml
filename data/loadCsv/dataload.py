import pymysql
import pandas as pd
from sqlalchemy import create_engine
# db 정보
db = pymysql.connect(host='180.64.50.38',
                     port=8890,
                     user='ccfd',
                     password='dataworld7789',
                     db='ccfddb',
                     charset='utf8',
                     local_infile=1
                     )

cursor = db.cursor()
#파일 위치 변경
df = pd.read_csv('../data/creditcard.csv')
# 테이블저장 컬럼 나열
df.columns = ['TIME','V1','V2','V3','V4','V5'
    ,'V6','V7','V8','V9','V10','V11'
    ,'V12','V13','V14','V15','V16'
    ,'V17','V18','V19','V20','V21'
    ,'V22','V23','V24','V25','V26'
    ,'V27','V28','AMOUNT','CLASS']


print("전체 행 : ", len(df.index))

row_count, column_count = df.shape
print("총 행(row) 수 : ", row_count)
print("총 칼럼(열) 수 : ", column_count)


engine = create_engine("mysql+pymysql://ccfd:"+"dataworld7789"+"@180.64.50.38:8890/ccfddb?charset=utf8", encoding = "utf-8")

conn = engine.connect()

df.to_sql(name="CREDIT_MASTER", con= engine, if_exists='append', index=False)
conn.close()


sql = "SELECT * FROM CREDIT_MASTER "
pd.read_sql(sql,db)