
import os, pickle, joblib


from sklearn.metrics import accuracy_score, precision_score, recall_score

from app import dbConfig
import pymysql
import logging


logger = logging.getLogger(__name__)

login = dbConfig.database_info
# db 정보
db = pymysql.connect(host=login['host'],
                     port=login['port'],
                     user=login['user'],
                     password=login['password'],
                     db=login['db'],
                     charset=login['charset']
                     )
cursor = db.cursor()

class SavedModel:

# 모델파일저장
    def saveModelFile(mdlMtNo,randomforest,predictions, labels ):
        logger.info("model file save")
        # 파일 저장

        mdPath = "./models/"+str(mdlMtNo)
        os.makedirs(mdPath, exist_ok=False)
        saved_model = pickle.dumps(randomforest)
        os.chdir(mdPath)
        joblib.dump(randomforest, 'toyProjRfMd.h5')
        accRto = format(accuracy_score(labels, predictions))
        preRto = format(precision_score(labels, predictions))
        recRto = format(recall_score(labels, predictions))
        logger.info("model info save")
        sql = "INSERT INTO MDL_MASTER VALUES (%s,%s,%s,%s,'N',sysdate())"
        print("insert")
        cursor.execute(sql,(mdlMtNo,accRto,preRto,recRto))
        db.commit()