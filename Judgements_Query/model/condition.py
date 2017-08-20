from Util import util
import datetime
#储存查询条件的类
class Conditon:
#这是在download程序里用到的属性 在查询程序里不用
    '''
    _id = None  #案件唯一ID
    ajlx = None  # 案件类型
    ay = None  # 案由
    gjc = None  # 关键词
    fycj = None  # 法院层级
    fydy = None  # 法院地域
    wslx = None  # 文书类型
    pjjg = None  # 判决结果
    sprqS = None  # 裁判日期 开始
    sprqE = None  # 裁判日期 结束
    '''
#下面是为了网页上查询而添加的 只会在网页里被赋值
    ajmc = None#案件名称
    ah = None#案号
    gjc = None#全文关键词
    fycj = None#法院层级
    fydy = None#法院地域
    spcx = None#审判程序
    sprqS = None#审判日期开始
    sprqE = None#审判日期结束
    fbrqS = None#发布日期开始
    fbrqE = None#发布日期结束
    def __init__(self, ajmc=None,ah=None,gjc=None,fycj=None,fydy=None,spcx=None,sprqS=None,sprqE=None,fbrqS=None,fbrqE=None):
        self.ajmc = ajmc
        self.ah = ah
        self.gjc = gjc
        self.fycj = fycj
        self.fydy = fydy
        self.spcx = spcx
        self.sprqS = datetime.datetime.strptime(sprqS,"%Y-%m-%d") if sprqS!=None and sprqS!="" else None
        self.sprqE = datetime.datetime.strptime(sprqE,"%Y-%m-%d") if sprqE!=None and sprqE!="" else None
        self.fbrqS = datetime.datetime.strptime(fbrqS,"%Y-%m-%d") if fbrqS!=None and fbrqS!="" else None
        self.fbrqE = datetime.datetime.strptime(fbrqE,"%Y-%m-%d") if fbrqE!=None and fbrqE!="" else None


    def toDict(self):
        json = {}
        json['ajmc'] = self.ajmc
        json['ah'] = self.ah
        json['gjc'] = self.gjc
        json['fycj'] = self.fycj
        json['fydy'] = self.fydy
        json['spcx'] = self.spcx
        json['sprqS'] = self.sprqS.strftime("%Y-%m-%d") if self.sprqS!=None and self.sprqS!="" else None
        json['sprqE'] = self.sprqE.strftime("%Y-%m-%d") if self.sprqE!=None and self.sprqE!="" else None
        json['fbrqS'] = self.fbrqS.strftime("%Y-%m-%d") if self.fbrqS!=None and self.fbrqS!="" else None
        json['fbrqE'] = self.fbrqE.strftime("%Y-%m-%d") if self.fbrqE!=None and self.fbrqE!="" else None
        return json

    #给压缩文件命名
    def toString(self):
        dict=self.toDict()
        result=""
        for i in ["ajmc","ah","gjc","fydy","fycj","spcx","sprqS","sprqE","fbrqS","fbrqE"]:
            if dict[i]==None or dict[i]=="":
                continue
            else:
                result += dict[i] + " "
        return result