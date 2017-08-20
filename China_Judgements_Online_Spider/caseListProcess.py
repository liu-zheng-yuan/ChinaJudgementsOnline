import re

import requests

import validationService


#获取此条件下共有多少案件
#deep是重新爬取的次数，如果出remind就识别验证码 2次不成功就放弃
def getCaseTotalNumber(con,deep=2):
    index=1 #目前是查询结果第几页
    direction="asc"#不明白含义
    order="法院层级"#查询结构排序的根据
    page=20#查询结构每页显示多少条
    param=con.toParam()
    para={"Param":param,"Index":index,"Page":page,"Order":order,"Direction":direction}
    url="http://192.0.101.71/List/ListContent"
    txt=requests.post(url,para).text

    if "remind" in txt and deep >= 0:
        validationService.valid()
        return getCaseTotalNumber(con, deep - 1)
    if "remind" in txt:
        print("验证码识别失败")
        return None
    #匹配第一个数字就是案件总数
    caseTotalNumber=re.search(r'\d+',txt).group()
    return int(caseTotalNumber)

#同时返回案件ID和其他 提升效率
def getCaseContentList(con,deep=2):
    direction="asc"#不明白含义
    order="法院层级"#查询结构排序的根据
    page=20#查询结构每页显示多少条
    param=con.toParam()
    url="http://192.0.101.71/List/ListContent"
    idList=[]
    cprqList=[]
    ajmcList=[]
    fymcList=[]
    ahList=[]
    spcxList=[]
    totalnunber=getCaseTotalNumber(con)
    totalPages=totalnunber//page +1 #总数整除每页20个 得出共有多少页
    #如果总页数都读不到 说明验证码识别失败

    for i in range(1,totalPages+1):
        index=i#目前是查询结果第几页
        para={"Param":param,"Index":index,"Page":page,"Order":order,"Direction":direction}
        txt=requests.post(url,para).text
        if "remind" in txt :#如果有验证码了 就识别之后再下载当前页一次
            validationService.valid()
            txt=requests.post(url,para).text
            js=eval(eval(txt))
            for i in range(1,len(js)):
                ajmcList.append(js[i]["案件名称"])
                fymcList.append(js[i]["法院名称"])
                ahList.append(js[i]["案号"])
                spcxList.append(js[i]["审判程序"])
                idList.append(js[i]["文书ID"])
                cprqList.append(js[i]["裁判日期"])
            continue

        js=eval(eval(txt))
        for i in range(1,len(js)):
            ajmcList.append(js[i]["案件名称"])
            fymcList.append(js[i]["法院名称"])
            ahList.append(js[i]["案号"])
            spcxList.append(js[i]["审判程序"])
            idList.append(js[i]["文书ID"])
            cprqList.append(js[i]["裁判日期"])
    if deep>0 and totalnunber>len(idList):
        return getCaseContentList(con,deep-1)
    elif(totalnunber > len(idList)):
        print("在此条件{}下，已爬取的案件ID数是{},实际案件ID数是{},发生缺少".format(con.toParam(),len(idList),totalnunber))

    return dict(caseIds=idList,caseDates=cprqList,ajmcList=ajmcList,fymcList=fymcList,ahList=ahList,spcxList=spcxList)


