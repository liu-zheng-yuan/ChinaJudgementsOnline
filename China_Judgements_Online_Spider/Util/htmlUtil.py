
import urllib
from Util import util
from http import cookiejar


class Browser:
    cookieFile = None
    opener = None

    def __init__(self, cookieFilePath='defaultCookieJar.txt'):
        self.cookieFile = cookieFilePath

    def postHtml(self, url, values=None):
        return self.openHtml(url, values, 'post')

    def getHtml(self, url, values=None):
        return self.openHtml(url, values, 'get')

    def openHtml(self, url, values, method):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
            'Connection': 'keep-alive', 'Referer': '******'}
        if util.isEmpty(values):
            postData = urllib.parse.urlencode({})
        else:
            postData = urllib.parse.urlencode(values)
        cookie = cookiejar.MozillaCookieJar(self.cookieFile)
        handler = urllib.request.HTTPCookieProcessor(cookie)
        if self.opener == None:
            self.opener = urllib.request.build_opener(handler)
        request = None
        if (method.lower() == "post"):
            if util.isEmpty(postData):
                request = urllib.request.Request(url, '', header)
            else:
                request = urllib.request.Request(url, postData.encode('utf-8'), header)
        else:
            if util.isEmpty(postData):
                request = urllib.request.Request(url)
            else:
                request = urllib.request.Request(url + "?%s" % postData)
        response = self.opener.open(request)
        html = response.read().decode()
        return html


def getUrl(url, values):
    html = None
    if values == None or values == '':
        html = urllib.request.urlopen(url).read()
    else:
        data = urllib.parse.urlencode(values)
        html = urllib.request.urlopen(url + "?%s" % data).read()
    return html


def postUrl(url, values):
    data = urllib.parse.urlencode(values).encode('utf-8')
    req = urllib.request.Request(url)
    page = urllib.request.urlopen(req, data)
    html = page.read().decode('utf-8')
    return html


def getAndSaveImg(imgUrl, localPath):
    urllib.request.urlretrieve(imgUrl, localPath)

