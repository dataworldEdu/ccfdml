# db 정보
import pymysql
from app import dbConfig

login = dbConfig.database_info
class DataInfo():

    def dataInfo(self) :
        db = pymysql.connect(host=login['host'],
                         port=login['port'],
                         user=login['user'],
                         password=login['password'],
                         db=login['db'],
                         charset=login['charset']
                         )
        return db