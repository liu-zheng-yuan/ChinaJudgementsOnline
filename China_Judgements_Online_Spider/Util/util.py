def getDict(data, name):
    if data == None or name == None: return None
    if name in data:
        return data[name]
    return None


def copyList(list):
    newList = []
    if list == None: return newList
    for item in list:
        newList.append(list)
    return newList


def getDateId():
    import datetime
    timeStr = datetime.datetime.now().strftime('%Y%m%d')
    return timeStr


def getTimeId(format='%Y%m%d%H%M%S'):
    import datetime
    timeStr = datetime.datetime.now().strftime(format)
    return timeStr


def getTimeStr():
    import datetime
    timeStr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return timeStr


def getUuid():
    import uuid
    return str(uuid.uuid1())


# 判断两个简单值是否相等
def equalsValue(a, b):
    validA = isValid(a)
    validB = isValid(b)
    if (validA == False and validB == False):
        return True
    return a == b


def hasText(text):
    if text == None: return False
    if len(text.strip()) == 0: return False
    return True


def isEmpty(val):
    return not isNotEmpty(val)


def isNotEmpty(val):
    if val == None:
        return False
    if isinstance(val, str) and len(val) == 0:
        return False
    if isinstance(val, list) and len(val) == 0:
        return False
    return True


# 判断值是否有效
def isValid(para):
    if para == None:
        return False
    if isinstance(para, str) and len(para) == 0:
        return False
    if isinstance(para, list) and len(para) == 0:
        return False
    return True
