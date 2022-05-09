import json

from fastapi import FastAPI
import  logging.config, logging.handlers

from app.model.baseModel import RandomForest
from app.model.selcProc import SelcProc



config = json.load(open('./app/logging.json'))

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

app = FastAPI()
@app.get("/learnModel")
async def learn_model():
    logger.info("model learnnig")
    mdlNo = RandomForest().start()
    return mdlNo



@app.get("/chooseModel/{stud_num}")
async def learn_model(stud_num: str):
    logger.info("model learnnig")
    mdlNo = SelcProc().chageModel(stud_num)


@app.get("/selcModel")
async def selcModel():
    SelcProc().selcDataUpdate()
    print("selcDataList")
    result = SelcProc().selcProcess()
    return result

@app.get("/modelList")
async def modelList():
    modelList = SelcProc().modelListSelect()
    return modelList

