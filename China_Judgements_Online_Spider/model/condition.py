from Util import util
import datetime
#储存查询条件的类
class Conditon:
#    _id = None  #案件唯一ID
    ajlx = None  # 案件类型
    ay = None  # 案由
    gjc = None  # 关键词
    fycj = None  # 法院层级
    fydy = None  # 法院地域
    wslx = None  # 文书类型
    pjjg = None  # 判决结果
    sprqS = None  # 裁判日期 开始
    sprqE = None  # 裁判日期 结束

    def __init__(self, ajlx=None, ay=None, gjc=None, fycj=None, fydy=None, wslx=None, pjjg=None,sprqS=None,sprqE=None):
        self.ajlx = ajlx
        self.ay = ay
        self.gjc = gjc
        self.fycj = fycj
        self.fydy = fydy
        self.wslx = wslx
        self.pjjg = pjjg
        self.sprqS = datetime.datetime.strptime(sprqS,"%Y-%m-%d")
        self.sprqE = datetime.datetime.strptime(sprqE,"%Y-%m-%d")

    #把审判日期起止时间变成String
    def __toTime(self):
        return self.sprqS.strftime("%Y-%m-%d")+"  TO  "+self.sprqE.strftime("%Y-%m-%d")
    #转变成可以填进url的字符串
    def toParam(self):
        paras = [];
        if util.isValid(self.ajlx):
            paras.append("案件类型:" + self.ajlx)
        if util.isValid(self.ay):
            paras.append("案由:" + self.ay)
        if util.isValid(self.fycj):
            paras.append("法院层级:" + self.fycj)
        if util.isValid(self.gjc):
            paras.append("全文检索:" + self.gjc)
        if util.isValid(self.fydy):
            paras.append("法院地域:" + self.fydy)
        if util.isValid(self.wslx):
            paras.append("文书类型:" + self.wslx)
        if util.isValid(self.pjjg):
            paras.append("判决结果:" + self.pjjg)
        if util.isValid(self.sprqE) and util.isValid(self.sprqS):
            paras.append("裁判日期:" + self.__toTime())
        return ",".join(paras);

    #用于mongoDB的save，转变为字典格式 插入数据库
    def toDict(self):
        json = {}
#        json['_id'] = self._id
        json['ajlx'] = self.ajlx
        json['ay'] = self.ay
        json['gjc'] = self.gjc
        json['fycj'] = self.fycj
        json['fydy'] = self.fydy
        json['wslx'] = self.wslx
        json['pjjg'] = self.pjjg
        return json
