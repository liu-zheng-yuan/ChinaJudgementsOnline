from Util import mongoUtil
def toButtonHtml(con,currentPage,baseUrl):
    totalNumber=mongoUtil.getCaseNumber(con)
    allPages=totalNumber//20 + 1 if totalNumber//20 *20 !=totalNumber else totalNumber//20

    str=""
    #加一个最前页
    str+=r'<a style="padding: 10px" href="/result?page=1">最前页</a>'
    #默认可以看到的页码是11个
    start = currentPage - 5 if currentPage-5>=1 else 1
    end = currentPage + 6 if currentPage+6<= allPages else allPages

    for i in range(start,end+1):
        #判断是否为当前页
        if i==currentPage:
            temp = r'<a style="color:red;font-size:26px;padding: 5px" href="%s?page=%d">%d</a>' \
                   % (baseUrl,i,i)
        else:
            temp = '<a style="padding: 5px" href="%s?page=%d">%d</a>' % (baseUrl,i,i)
        str+=temp

    #加一个最后页
    str+=r'<a style="padding: 10px" href="/result?page=%d">最后页</a>' % allPages
    return str

