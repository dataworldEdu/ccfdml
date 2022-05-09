
import warnings
warnings.filterwarnings("ignore")
import pymysql
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from app import dbConfig

from app.model.saveModel import SavedModel

from sklearn.ensemble import RandomForestClassifier

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
class RandomForest:
    def __init__(self):
        pass

    def start(self):
        pd.set_option('display.max_rows', 100)
        pd.set_option('display.max_columns', 200)

        cursor.execute("SELECT IFNULL(MAX(STUD_NUM)+1,1)  FROM MDL_MASTER")

        mdlMtNo = cursor.fetchone()
        sql = "SELECT * FROM CREDIT_LEARN_DATA"
        logger.info("data select")
        creditDatas = pd.read_sql(sql,db)
         # 조회한 테이블 컬럼 정보 확인
        #creditDatas.info()

        #print(creditDatas['CLASS'].value_counts())

        #fig, axe = plt.subplots(ncols=1)
        #fig.set_size_inches(6, 3)
        #sns.countplot(creditDatas['CLASS'])

        # 불필요 컬럼 제거
        vCols = []
        for i in range(28):
            col = 'V'+str(i+1)
            vCols.append(col)

        vCols.append('CLASS')

        dataV = creditDatas[vCols]

        #print(dataV.head(5))
        # min max 값 확인
        #cols = dataV.dtypes.index.tolist()

        #print(cols)

        # feature , label 분리
        raw_data = dataV.values
        # The last element contains the labels
        labels = raw_data[:, -1]

        # The other data points are the electrocadriogram data
        col_data = raw_data[:, 0:-1]

        #학습, 테스트 데이터 분리
        train_data, test_data, train_labels, test_labels = train_test_split(
            col_data, labels, test_size=0.2, random_state=21
        )

        logger.info("data learnning")
        # 학습
        randomforest = RandomForestClassifier(n_jobs = -1, n_estimators= 100, max_depth = 10, min_samples_leaf = 2, max_features = 'sqrt', verbose = 1 )
        randomforest.fit(train_data, train_labels)

        # 테스트 데이터 예측 수행
        y_pred = randomforest.predict(test_data)


        np.set_printoptions(precision=6, suppress=True)



        # 모델파일저장
        SavedModel.saveModelFile(mdlMtNo[0],randomforest,y_pred,test_labels)
        return mdlMtNo[0]

