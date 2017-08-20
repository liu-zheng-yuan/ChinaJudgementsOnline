import datetime

class Period:
    sprqS=None #审判日期开始点
    sprqE=None #审判日期结束点
    caseIds=[] #存这个时段里符合条件的案件Id 可能很多
    conId=None #所属查询条件 可在conditon表中查条件
    count=None #对应案件数

    def __init__(self,con,caseIds=None,conId=None,count=None):
        self.sprqS=con.sprqS
        self.sprqE=con.sprqE
        self.caseIds=caseIds
        self.conId=conId
        self.count=count

    def toDict(self):
        json = {}
        json['sprqS'] = self.sprqS
        json['sprqE'] = self.sprqE
        json['conId'] = self.conId
        json['count'] = self.count
        json['caseIds'] = self.caseIds
        return json


