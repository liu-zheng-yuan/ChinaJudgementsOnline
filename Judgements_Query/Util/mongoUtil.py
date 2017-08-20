from datetime import datetime

from pymongo import MongoClient

from Util import util
from model import condition

URL = 'localhost'
PORT = 27017
DB = 'wspc'
client = MongoClient(URL, PORT)

#三个表 Case Period Con

#返回所有案件的迭代器
def getCaseList(con):
    coll=client[DB]['Case']
    queryDict={}

    if getattr(con,"gjc")!='' and getattr(con,"gjc")!=None:
        queryDict.update(wsnr={"$regex":con.gjc})
    if getattr(con,"fycj")!='' and getattr(con,"fycj")!=None:
        queryDict.update(fymc={"$regex":con.fycj})
    if getattr(con,"fydy")!='' and getattr(con,"fydy")!=None:
        if "fymc" in queryDict.keys():
            queryDict["fymc"]["$regex"]=con.fydy+".*"+queryDict["fymc"]["$regex"]
        else:
            queryDict.update(fymc={"$regex":con.fydy})
    if getattr(con,"spcx")!='' and getattr(con,"spcx")!=None:
        queryDict.update(spcx={"$regex":con.spcx})
    if getattr(con,"ajmc")!='' and getattr(con,"ajmc")!=None:
        queryDict.update(ajmc={"$regex":con.ajmc})
    if getattr(con,"ah")!='' and getattr(con,"ah")!=None:
        queryDict.update(ah={"$regex":con.ah})
    if getattr(con,"sprqS")!='' and getattr(con,"sprqS")!=None and getattr(con,"sprqE")!='' and getattr(con,"sprqE")!=None:
        queryDict.update(cprq={"$gte":con.sprqS,"$lte":con.sprqE})
    if getattr(con,"fbrqS")!='' and getattr(con,"fbrqS")!=None and getattr(con,"fbrqE")!='' and getattr(con,"fbrqE")!=None:
        queryDict.update(fbrq={"$gte":con.fbrqS,"$lte":con.fbrqE})

    queryList=coll.find(queryDict)

    return queryList

# 获取符合条件的案件的总数
def getCaseNumber(con):

    return  getCaseList(con).count()

def getOnePageCase(con,currentPage):
    perPage=20

    queryList=getCaseList(con).skip((currentPage-1)*perPage).limit(perPage)

    return list(queryList)

if __name__=="__main__":
    #con= condition.Conditon("毒品","2016","其","高级","吉林","审查",sprqS="2017-01-01",sprqE="2017-01-10",fbrqS="2017-01-01",fbrqE="2017-10-02")
    con= condition.Conditon("毒品",fycj="高级",fydy="吉林")
    caseList=getOnePageCase(con,1)
    print(len(caseList))


