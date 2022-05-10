import os, pickle, joblib

from sklearn.metrics import accuracy_score, precision_score, recall_score
from app.dataInfo import  DataInfo
import logging

logger = logging.getLogger(__name__)

class SavedModel:
    def __init__(self):
        pass

    # 모델파일저장
    def saveModelFile(mdlMtNo, randomforest, predictions, labels):
        db = DataInfo().dataInfo()
        cursor = db.cursor()
        logger.info("model file save")
        # 파일 저장
        # crr_path = os.getcwd()
        mdPath = "/ccfdml/models/" + str(mdlMtNo)
        os.makedirs(mdPath, exist_ok=True)
        saved_model = pickle.dumps(randomforest)
        os.chdir(mdPath)
        joblib.dump(randomforest, 'toyProjRfMd.h5')
        accRto = format(accuracy_score(labels, predictions))
        preRto = format(precision_score(labels, predictions))
        recRto = format(recall_score(labels, predictions))
        logger.info("model info save")
        sql = "INSERT INTO MDL_MASTER VALUES (%s,%s,%s,%s,'N',sysdate())"
        print("insert")
        cursor.execute(sql, (mdlMtNo, accRto, preRto, recRto))
        db.commit()
        db.close()
