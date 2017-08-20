import requests
import re
import validationService
def parser(html):
    content = html[html.index('= "') + 3:html.index('"}";') + 2]
    content = content.replace("\n","")
    content = content.replace("</a>", "</a>\r\n")
    content = content.replace("</div>", "</div>\r\n")
    content = content.replace("</style>", "</style>\r\n")
    divs = re.findall("<div.+>.+</div>", content)
    result = ""
    for div in divs:
        text = div[div.index('>') + 1:div.index('</div>')]
        if "style" in text: continue
        if '<' in text and '>' in text: continue
        result += text.strip() + "\n"
    return result

#根据Id 返回文书内容和发布日期
def getCaseContent(caseId):
    try:
        urlParam={"DocID":caseId}
        url="http://192.0.101.71/CreateContentJS/CreateContentJS.aspx"
        r=requests.get(url,urlParam)
        if "Remind" in r.text or "remind" in r.text:#如果有验证码了 就识别之后再下载当前页一次
            validationService.valid()
            r=requests.get(url,urlParam)
        fbrq=re.search("[\d]{4}-[\d]{2}-[\d]{2}",r.text).group()
        result=parser(r.text)
        return dict(content=result,fbrq=fbrq)
    except Exception:
        print("Id为{}的案件未下载成功，可能条件不合法或者该案件有问题".format(caseId))
        return dict(content="",fbrq="")



