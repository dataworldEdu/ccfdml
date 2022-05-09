import warnings

import numpy as np

warnings.filterwarnings("ignore")
import pandas as pd
import os
import joblib
import pymysql

from app import dbConfig

login = dbConfig.database_info

db = pymysql.connect(host=login['host'],
                     port=login['port'],
                     user=login['user'],
                     password=login['password'],
                     db=login['db'],
                     charset=login['charset']
                     )
cursor = db.cursor()

class SelcProc:
    def __init__(self):
        pass


    def chageModel(stud_num):
        sql = "UPDATE MDL_MASTER SET APLY_YN = 'Y' WHERE STUD_NUM = %s"
        cursor.execute(sql, stud_num)
        db.commit()




    def selcProcess(self):
        sql = "SELECT STUD_NUM FROM MDL_MASTER WHERE APLY_YN = 'Y'"
        cursor.execute(sql)

        mdlNo = cursor.fetchone()
        selcMdlNum = str(mdlNo[0])
        mdPath = "./models/"+str(mdlNo[0])
        #mdPath = "../../models/"+selcMdlNum
        # 경로 이동
        os.chdir(mdPath)
        selcPredMdl = joblib.load('toyProjRfMd.h5')
        # 실시간 처리 건 수집
        selcListSql = "SELECT * FROM SELC_DATA WHERE DEL_YN = 'N' AND SELC_YN = 'N'"
        selcList = pd.read_sql(selcListSql,db)
        # 처리건별 선별 진행및 임계치 저장
        for selcdata, row in selcList.iterrows() :
            dataV = row[2:30]
            dataV = np.array(dataV)
            dataV = dataV.reshape(1, -1)
            selcPredProba = selcPredMdl.predict_proba(dataV)
            selcKey = row[0]
            thresholdRto = selcPredProba[0][1]
            updateSql = "UPDATE SELC_DATA SET THRESHOLD_RTO = %s ,SELC_MDL_NUM = %s , SELC_YN = 'Y'" \
                        "WHERE ID = %s"
            cursor.execute(updateSql,(thresholdRto,selcMdlNum,selcKey))
            db.commit()
        return "sucsess"


    def selcDataUpdate(self):
        sql = "UPDATE SELC_DATA SET DEL_YN = 'N' WHERE SELC_YN = 'N' LIMIT 10"
        cursor.execute(sql)
        db.commit()
        
    def modelListSelect(self):
        try :
            cursor.execute("SELECT *  FROM MDL_MASTER")
        except :
            { 'resultCode':500, 'resultMsg': 'query execution fail : member info' }
        result = [dict((cursor.description[i][0],value) for i , value in enumerate(row))
                  for row in cursor.fetchall()]
        return result
