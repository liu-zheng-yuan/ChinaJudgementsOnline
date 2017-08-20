import copy
import configparser
from Util import dateUtil
from Util import mongoUtil
from caseListProcess import *
from contentProcess import *
from model import condition, period, case

#储存时要增量储存，不能有重复的时间段（按法院层级分的时候要保证四个层级的合并起来存一条period）
'''
给一个条件 能够下载con对应的case，存入数据库
因为返回的idlist最多只有2000个，所以下载要分三（四）个阶段：
1传入con 找该条件下，数据库里没有的空白时间段（如果数据库里没有这个条件 空白时间段就是整个时间段）只储存空白的时间段
2传入con和时间段 把每个时间段分成要么是1天 要么段内案件数小于2000个 的很多个子时间段
3传入con和时间段 按照法院地域，分成若干个con 分别下载 使得每次下载数小于2000个
4传入所有的con 直接下载并存入 因为上面三层保证了条件有效并且小于2000
'''
#第一层
def downByCon(con):
    #数据库中没存这个条件的案件 重新下载
    if(mongoUtil.getConId(con)==None):
        mongoUtil.saveCon(con)
        peri= period.Period(con, conId=mongoUtil.getConId(con))
        downByPeriod(con,peri)
        #以上都应该写在第一层
    else:#数据库中有相同的条件
        conId=mongoUtil.getConId(con)
        spacePeriodList=dateUtil.getSpacePeriod(con)
        for dic in spacePeriodList:
            con.sprqS=dic["dateS"]
            con.sprqE=dic["dateE"]
            peri= period.Period(con, conId=conId)
            downByPeriod(con,peri)

#第二层 peri是时间段period
def downByPeriod(con,peri):

    caseTotalNumber=getCaseTotalNumber(con)
    if caseTotalNumber<2000 or con.sprqS==con.sprqE:
        downByFydy(con,peri)
    else:
        middleDate=dateUtil.findMiddleDate(con.sprqS,con.sprqE)
        #将前一半递归处理判断小不小于2000
        con1=copy.copy(con)
        con1.sprqE=middleDate
        peri1=copy.copy(peri)
        peri1.sprqE=middleDate
        downByPeriod(con1,peri1)
        #将后一半递归处理判断小不小于2000
        con2=copy.copy(con)
        con2.sprqS=dateUtil.addOneDay(middleDate) #要加一天 避免重复读入数据库
        peri2=copy.copy(peri)
        peri2.sprqS=dateUtil.addOneDay(middleDate)
        downByPeriod(con2,peri2)


#第三层
def downByFydy(con,peri):
    #按法院地域划分可能会少 本身就会少
    if(getCaseTotalNumber(con)<2000):
        download(con,peri)
    elif(con.fydy=="全部" or con.fydy=="" or con.fydy==None):
        dyList = ['最高法院', '北京市', '天津市', '河北省', '山西省', '内蒙古自治区', '辽宁省', '吉林省',
                  '黑龙江省', '上海市', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省', '湖北省',
                  '湖南省', '广东省', '广西壮族自治区', '海南省', '重庆市', '四川省', '贵州省', '云南省', '西藏自治区',
                  '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区', '新疆维吾尔自治区高级人民法院生产建设兵团分院']
        idList=[] #总的list 可能会超2000
        for i,dy in enumerate(dyList):
            con.fydy=dy
            caseTotalNumber=getCaseTotalNumber(con)

            if caseTotalNumber==0: #此条件下没有案件
                continue
            elif caseTotalNumber>2000: #超过了限制，只能下载2000个
                print("当前条件划分下，法院地域为{}的案件数是{}，超过了限制".format(dy,caseTotalNumber))
            caseIds=__download(con)
            orilen=len(idList)
            idList.extend(caseIds)
            nowlen=len(idList)
            if(nowlen-orilen!=caseTotalNumber):
                print("此条件下，在发源地域为{}，出现了案件数{}的偏差".format(fydy,nowlen-orilen))
        #构造period 存入表里
        peri.caseIds=idList
        peri.count=len(peri.caseIds)
        mongoUtil.savePeriod(peri)

    else:
        #con里已经设置过了法院地域 直接下载
        download(con,peri)

#第四层 直接下载
def download(con,peri):
    dict=getCaseContentList(con)
    caseIds=dict["caseIds"]
    cprqList=dict["caseDates"]
    ajmcList=dict["ajmcList"]
    fymcList=dict["fymcList"]
    ahList=dict["ahList"]
    spcxList=dict["spcxList"]
    peri.caseIds=caseIds
    peri.count=len(peri.caseIds)
    mongoUtil.savePeriod(peri)
    #下载所有id的文书，存入数据库
    for i,Id in enumerate(caseIds):
    #做一个简化 文书所有内容都存入wsnr中，再存一个裁判日期其他各种属性为空
        try:
            contentdict=getCaseContent(Id)
            content=contentdict["content"]
            cprq=cprqList[i]
            ajmc=ajmcList[i]
            fymc=fymcList[i]
            ah=ahList[i]
            spcx=spcxList[i]
            fbrq=contentdict["fbrq"]
            a_case= case.Case(caseId=Id,ah=ah,ajmc=ajmc,spcx=spcx,fymc=fymc,wsnr=content, cprq=cprq,fbrq=fbrq)
            mongoUtil.saveCase(a_case)
        except Exception:
            print("ID为{}的案件有问题，请手动存入".format(Id))
            continue



#只在Byfycj里用，为了让按四个法院层级分完下载后 只存一条period(增量储存原则)
#按分完法院层级的条件，下载case存进去之后，返回该条件下的caseIdList
def __download(con):
    dict=getCaseContentList(con)
    caseIds=dict["caseIds"]
    cprqList=dict["caseDates"]
    ajmcList=dict["ajmcList"]
    fymcList=dict["fymcList"]
    ahList=dict["ahList"]
    spcxList=dict["spcxList"]
    #下载所有id的文书，存入数据库
    for i,Id in enumerate(caseIds):
        try:
            contentdict=getCaseContent(Id)
            content=contentdict["content"]
            cprq=cprqList[i]
            ajmc=ajmcList[i]
            fymc=fymcList[i]
            ah=ahList[i]
            spcx=spcxList[i]
            fbrq=contentdict["fbrq"]
            a_case= case.Case(caseId=Id,ah=ah,ajmc=ajmc,spcx=spcx,fymc=fymc,wsnr=content, cprq=cprq,fbrq=fbrq)
            mongoUtil.saveCase(a_case)
        except Exception:
            print("ID为{}的案件有问题，请手动存入".format(Id))
            continue

    return caseIds

#下载下来的总数会比读取的少 因为在按法院层级分类时本身就会少
if __name__=="__main__":

    config=configparser.ConfigParser()
    config.read("downloadConfig.ini","UTF-8")
    ajlx =config.get("Condition","ajlx")   # 案件类型
    ay = config.get("Condition","ay")    # 案号
    gjc = config.get("Condition","gjc")   # 案件名称
    fycj = config.get("Condition","fycj")  # 法院层级
    fydy = config.get("Condition","fydy")  # 法院地域
    wslx = config.get("Condition","wslx")  # 文书类型
    pjjg = config.get("Condition","pjjg")  # 判决结果
    sprqS = config.get("Condition","sprqS")  # 裁判日期 开始
    sprqE = config.get("Condition","sprqE")  # 裁判日期 结束
    con=condition.Conditon(ajlx,ay,gjc,fycj,fydy,wslx,pjjg,sprqS,sprqE)
    downByCon(con)


