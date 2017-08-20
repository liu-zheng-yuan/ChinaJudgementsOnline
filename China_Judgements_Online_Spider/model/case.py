import datetime
class Case:
    caseId = None  # 文书ID
    ah = None  # 案号
    ajmc = None  # 案件名称
    spcx = None  # 审判程序
    fymc = None  # 法院名称
    wsbt = None  # 文书标题
    wsnr = None  # 文书内容
    cprq = None  # 裁判日期
    fbrq = None  # 发布日期


    def __init__(self,caseId = None,ah = None,ajmc = None,spcx = None,fymc = None,wsbt = None,wsnr=None,cprq = None,fbrq = None):
        self.caseId=caseId
        self.ah=ah
        self.ajmc=ajmc
        self.spcx=spcx
        self.fymc=fymc
        self.wsbt=wsbt
        self.wsnr=wsnr
        self.cprq=datetime.datetime.strptime(cprq,"%Y-%m-%d") if cprq!=None or cprq!="" else None
        self.fbrq=datetime.datetime.strptime(fbrq,"%Y-%m-%d") if fbrq !=None or cprq!="" else None

    def toDict(self):
        json = {}
        json['caseId'] = self.caseId
        json['ah'] = self.ah
        json['ajmc'] = self.ajmc
        json['spcx'] = self.spcx
        json['fymc'] = self.fymc
        json['wsbt'] = self.wsbt
        json['wsnr'] = self.wsnr
        json['cprq'] = self.cprq
        json['fbrq'] = self.fbrq
        return json