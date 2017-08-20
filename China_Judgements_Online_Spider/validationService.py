from PIL import Image

from Util import htmlUtil
from Util import util
#图像识别来破验证码

class ImageService:
    image = None
    width = None
    height = None
    vals = None
    maxVal = None
    minVal = None
    rowsDiscrete = None
    colsDiscrete = None
    rowsep = None  # 列阈值
    colsep = None  # 行阈值

    def __init__(self, imagePath):
        self.image = Image.open(imagePath)
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.__initValues()
        self.__initDiscreteVals()
        self.__initSeperator()

    def __initValues(self):
        list = []
        for i in range(256):
            list.append(0)
        for x in range(self.width):
            for y in range(self.height):
                val = self.getPixelVal(x, y)
                list[val] += 1
        max = 0
        min = 255
        for val in list:
            if val > max: max = val
            if val < min: min = val
        self.vals = list
        self.maxVal = max
        self.minVal = min

    def __initDiscreteVals(self):
        rowsDiscrete = []
        colsDiscrete = []
        for y in range(self.height):
            rowVals = []
            for x in range(self.width): rowVals.append(self.getPixelVal(x, y))
            rowsDiscrete.append(self.calVariance(rowVals))
        for x in range(self.width):
            rowVals = []
            for y in range(self.height): rowVals.append(self.getPixelVal(x, y))
            colsDiscrete.append(self.calVariance(rowVals))
        self.rowsDiscrete = rowsDiscrete
        self.colsDiscrete = colsDiscrete

    def __initSeperator(self):
        PERCENT = 10
        rowsd = self.rowsDiscrete
        colsd = self.colsDiscrete
        rowMax = 0
        colMax = 0
        for d in rowsd:
            if d > rowMax: rowMax = d
        for d in colsd:
            if d > colMax: colMax = d
        self.rowsep = PERCENT * rowMax / 100
        self.colsep = PERCENT * colMax / 100

    def autoCrop(self, border=1):
        rowsd = self.rowsDiscrete
        colsd = self.colsDiscrete

        index = 0
        colScopes = []
        while (index < len(colsd)):
            while index < len(colsd) and colsd[index] < self.colsep: index += 1
            left = index
            while index < len(colsd) and colsd[index] >= self.colsep: index += 1
            right = index
            if left < right: colScopes.append([left, right])
        index = 0
        rowScopes = []
        while (index < len(rowsd)):
            while index < len(rowsd) and rowsd[index] < self.rowsep: index += 1
            left = index
            while index < len(rowsd) and rowsd[index] >= self.rowsep: index += 1
            right = index
            if left < right: rowScopes.append([left, right])

        images = []
        for row in rowScopes:
            for col in colScopes:
                im = self.image.crop((col[0] - border, row[0] - border, col[1] + border, row[1] + border))
                images.append(im)
        return images

    def getPixelVal(self, x, y):
        val = self.image.getpixel((x, y))
        if not isinstance(val, int):
            val = (val[0] + val[1] + val[2]) / 3
        return int(val)

    def calVariance(self, list, rl=2):
        if len(list) == 0: return 0
        sum = 0
        for val in list: sum += val
        avg = sum / len(list)
        squareSum = 0
        for val in list: squareSum += (val - avg) * (val - avg)
        result = squareSum / len(list)
        return round(result, rl)


class OcrService:
    trainImages = None

    def __init__(self):
        self.initTrainImages()

    def initTrainImages(self):
        service = ImageService("code/sample/one.jpg")
        images = service.autoCrop()
        self.trainImages = images

    def getPixelVal(self, image, x, y, scope=0):
        width = image.size[0]
        height = image.size[1]
        size = 0
        sum = 0
        for i in range(x - scope, x + scope + 1):
            if i < 0 or i >= width: continue
            for j in range(y - scope, y + scope + 1):
                if j < 0 or j >= height: continue
                val = image.getpixel((i, j))
                if not isinstance(val, int):
                    val = (val[0] + val[1] + val[2]) / 3
                size += 1
                sum += val
        return int(sum / size)

    def getSimilarity(self, this, that):
        width = max(this.size[0], that.size[0])
        height = max(this.size[1], that.size[1])
        this = this.resize((width, height))
        that = that.resize((width, height))
        pointNum = width * height
        sum = 0
        for x in range(min(width, width)):
            for y in range(min(height, height)):
                val = self.getPixelVal(this, x, y, 0)
                tval = self.getPixelVal(that, x, y, 0)
                span = abs(val - tval)
                sum += span / 255
        return round(100 - 100 * sum / pointNum, 2)

    def getNum(self, that):
        index = -1
        max = 0
        list = []
        for i in range(9):
            val = self.getSimilarity(self.trainImages[i], that)
            list.append((i, val))
            if val > max:
                index = i
                max = val
        # print(list)
        return index

    def ocr(self, path):
        list = []
        service = ImageService(path)
        numImages = service.autoCrop()
        for numImage in numImages:
            num = self.getNum(numImage)
            list.append(num)
        return list


class ValidationService:
    IMAGE_PATH = "code/validation.jpg"
    ocrService = None
    brower = None

    def __init__(self):
        self.ocrService = OcrService()
        self.brower = htmlUtil.Browser()
        self.IMAGE_PATH = "code/{}.jpg".format(util.getTimeId())

    def getCodeImage(self):
        url = "http://192.0.101.71/User/ValidateCode"
        htmlUtil.getAndSaveImg(url, self.IMAGE_PATH)

    def ocr(self):
        list = self.ocrService.ocr(self.IMAGE_PATH)
        result = ''
        for item in list:
            result += str(item)
        return result

    def check(self, code):
        url = "http://192.0.101.71/Content/CheckVisitCode"
        para = {'ValidateCode': code}
        html = htmlUtil.postUrl(url, para)
        return html

    def valid(self):
        self.getCodeImage()
        code = service.ocr()
        result = self.check(code)
        return result


service = ValidationService()


def valid():
    service.valid()
