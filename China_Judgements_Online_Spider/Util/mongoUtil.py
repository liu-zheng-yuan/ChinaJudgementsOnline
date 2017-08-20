from datetime import datetime

from pymongo import MongoClient

from Util import util
from model import condition

URL = 'localhost'
PORT = 27017
DB = 'wspc'
client = MongoClient(URL, PORT)

#三个表 Case Period Con

# 保存
#把case、condtion存到数据库里对应的表里
def save(collection, model):
    if util.isValid(collection) and util.isValid(model):
        coll = client[DB][collection]
        coll.insert(model.toDict())
    else:
        print("参数无效：col={},model={}".format(collection, model))

#存到“查询条件”表中
def saveCon(con):
    save("Con", con)

#存到“审判时段”表中
#开始和结束时间存在condition类中
def savePeriod(period):
    save("Period", period)

#存到“案件”表中
def saveCase(case):
    save("Case", case)




# 获取
#查询con数据库里有没有存符合条件的con
#如果有说明此条件已经搜索过 直接去period里找所有的案件id
#如果没有 说明此条件未查过 要去爬
def getConId(con):
    coll=client[DB]['Con']
    #去con表里找符合要求的 因为返回的是迭代器 所以要用next 只可能返回一个结果
    queryNumber=coll.find(con.toDict()).count()
    if(queryNumber==0):
        return None
    else:
        #返回的是此条件唯一ID 是bson.objectid.ObjectId类型的
        query=coll.find(con.toDict()).next()
        return query["_id"]

#获取相同条件下 数据库中满足（sprqS小于E，sprqE大于S）条件的period文档
def getSameConPeriod(con,conId):
    coll=client[DB]['Period']
    pattern={
        "sprqS":{"$lte":con.sprqE},
        "sprqE":{"$gte":con.sprqS},
        "conId":conId
    }
    queryList=coll.find(pattern)
    return queryList #这是一个迭代器

def isIdExistAndSuitalbe(Id,con):
    coll=client[DB]['Case']
    queryList=coll.find({"caseId":Id})
    if(queryList.count()!=0): #可能有重复的案件 只需要判断重复的其中之一就行
        #并且Id的案件要在con.S和con.E之间
        query=queryList.next()
        cprq=datetime.strptime(query["cprq"],"%Y-%m-%d")
        if(cprq >= con.sprqS and cprq <= con.sprqE):
            return True
        else:
            return False
    else:
        return False


