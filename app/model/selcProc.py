import warnings

import numpy as np

warnings.filterwarnings("ignore")
import pandas as pd
import os
import joblib
from app.dataInfo import  DataInfo

class SelcProc:
    def chageModel(mdlNo):
        db = DataInfo().dataInfo()
        cursor = db.cursor()
        sql = "UPDATE MDL_MASTER SET APLY_YN = 'N' "
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE MDL_MASTER SET APLY_YN = 'Y' WHERE STUD_NUM ="+str(mdlNo)
        cursor.execute(sql)
        db.commit()
        db.close()
        return mdlNo

    def selcProcess(self):
        db = DataInfo().dataInfo()
        cursor = db.cursor()
        sql = "SELECT STUD_NUM FROM MDL_MASTER WHERE APLY_YN = 'Y'"
        cursor.execute(sql)
        mdlNo = cursor.fetchone()
        selcMdlNum = str(mdlNo[0])
        mdPath = "/ccfdml/models/" + str(mdlNo[0])
        # 경로 이동
        os.chdir(mdPath)
        selcPredMdl = joblib.load('toyProjRfMd.h5')
        # 실시간 처리 건 수집
        selcListSql = "SELECT * FROM SELC_DATA WHERE DEL_YN = 'N' AND SELC_YN = 'N'"
        selcList = pd.read_sql(selcListSql, db)
        # 처리건별 선별 진행및 임계치 저장
        for selcdata, row in selcList.iterrows():
            dataV = row[2:30]
            dataV = np.array(dataV)
            dataV = dataV.reshape(1, -1)
            selcPredProba = selcPredMdl.predict_proba(dataV)
            selcKey = row[0]
            thresholdRto = selcPredProba[0][1]
            updateSql = "UPDATE SELC_DATA SET THRESHOLD_RTO = %s ,SELC_MDL_NUM = %s , SELC_YN = 'Y' ,SELC_DTTM = SYSDATE()" \
                        "WHERE ID = %s"
            cursor.execute(updateSql, (thresholdRto, selcMdlNum, selcKey))
            db.commit()
        db.close()
        return "sucsess"


    def selcDataUpdate(self):
        db = DataInfo().dataInfo()
        cursor = db.cursor()
        sql = "UPDATE SELC_DATA SET DEL_YN = 'N' WHERE SELC_YN = 'N' LIMIT 10"
        cursor.execute(sql)
        db.commit()
        db.close()


    def modelListSelect(self):
        db = DataInfo().dataInfo()
        cursor = db.cursor()
        cursor.execute("SELECT *  FROM MDL_MASTER")
        result = [dict((cursor.description[i][0], value) for i, value in enumerate(row))
                  for row in cursor.fetchall()]
        db.close()
        return result

    def selcResult(self):
        db = DataInfo().dataInfo()
        cursor = db.cursor()
        cursor.execute("SELECT ID, THRESHOLD_RTO  FROM SELC_DATA WHERE SELC_YN = 'Y' ORDER BY SELC_DTTM DESC LIMIT 10")
        result = [dict((cursor.description[i][0], value) for i, value in enumerate(row))
                  for row in cursor.fetchall()]
        db.close()
        return result


