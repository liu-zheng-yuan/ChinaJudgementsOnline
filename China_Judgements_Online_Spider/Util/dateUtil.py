from datetime import timedelta

from Util import mongoUtil


#用来计算时间的

#用来判断两个日期是不是只间隔了一天
def isNextDay(dateS,dateE):#不知道为什么 datetime类型的dateS传进来变成了String
    return dateS+timedelta(days=1)==dateE

#找两个日期中间的一天（用于download里的二分法）
def findMiddleDate(dateS,dateE):
    '''
    middleTimeStamp=dateS.timestamp()+(dateE.timestamp()-dateS.timestamp())/2
    middleDate=datetime.fromtimestamp(middleTimeStamp)
    return middleDate
    '''
    if(dateS==dateE):
        return dateS
    tempdate=dateS
    number=0
    while(tempdate!=dateE):
        tempdate=tempdate+timedelta(days=1)
        number+=1
    for i in range(0,number//2):
        dateS=dateS+timedelta(days=1)

    return dateS
#给一个日期加一天
def addOneDay(date):
    return date+timedelta(days=1)

def toString(date):
    return date.strftime("%Y-%m-%d")

#找两个日期之间的天数
def getIntervalDays(dateS,dateE):
    if(dateE < dateS): #最小间隔就是0 不能是负数
        return 0
    tempdate=dateS
    number=0
    while(tempdate!=dateE):
        tempdate=tempdate+timedelta(days=1)
        number+=1
    return number

#从数据库里找出S到E时间段内 数据库没有储存的时间段
def getSpacePeriod(con):
    conId=mongoUtil.getConId(con)
    queryList=mongoUtil.getSameConPeriod(con,conId) #已存在的period记录 迭代器
    intervalDays=getIntervalDays(con.sprqS,con.sprqE) #间隔天数
    table=[None]*(intervalDays+1) #标记为1表明已存在 0为不存在

    for query in queryList:
        sprqS=query["sprqS"]
        sprqE=query["sprqE"]
        start=getIntervalDays(con.sprqS,sprqS) #标记数组里标1的起始点
        end=getIntervalDays(con.sprqS,sprqE) #数组里标1的终点 不能大于hashtable总长度
        if(end>len(table)-1):
            end=len(table)-1

        for i in range(start,end+1):
            table[i]=1

    spacePeriodList=[]
    i=0
    while i < len(table):
        if(table[i]==1):
            i+=1
            continue
        else:
            s=i
            e=None
            j=s
            while j < len(table):
                if(table[j]==1):
                    j+=1
                    break
                else:
                    e=j
                    j+=1
            i=j+1
            dateS=con.sprqS+timedelta(days=s)
            dateE=con.sprqS+timedelta(days=e)
            spacePeriodList.append(dict(dateS=dateS,dateE=dateE))

    return spacePeriodList


