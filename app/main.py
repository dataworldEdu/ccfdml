from fastapi import FastAPI

from app.model.baseModel import RandomForest
from app.model.selcProc import SelcProc

app = FastAPI()


@app.get("/learnModel")
async def learnModel():
    mdlNo = RandomForest().learnningModel()
    return mdlNo


@app.post("/chooseModel/{mdlNo}")
async def chooseModel(mdlNo):
    result = SelcProc.chageModel(mdlNo)
    return result

@app.put("/selcModel")
async def selcModel():
    SelcProc().selcDataUpdate()
    result = SelcProc().selcProcess()
    return result


@app.get("/modelList")
async def modelList():
    modelList = SelcProc().modelListSelect()
    return modelList


@app.get("/selcResult")
async def selcResult():
    result = SelcProc().selcResult()
    return result



