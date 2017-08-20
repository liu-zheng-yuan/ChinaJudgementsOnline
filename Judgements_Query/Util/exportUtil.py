#把文书内容输出成txt文件，filename是文书标题
from model import condition
from Util import mongoUtil
import zipfile


def dealDuplicateName(filename,hashtable,length):
    hashnumber=hash(filename) % length
    hashtable[hashnumber]+=1
    if hashtable[hashnumber]==1:
        return filename
    else:
        return filename+str(hashtable[hashnumber])

#从数据库里输出成zip 记得传完了要删除所有
#这里面所有的相对路径都是相对于调用该函数的文件的相对路径

def exportAndToRar(con):
    caseList=list(mongoUtil.getCaseList(con))
    zipname=con.toString()
    hashtable=[0]*(len(caseList)+100)
    zf=zipfile.ZipFile("temp/%s.zip"%zipname.strip(),"w",zipfile.ZIP_DEFLATED)
    #创建所有txt并挨个加入zip
    for i,case in enumerate(caseList):
        filename=case["ah"]
        filename=dealDuplicateName(filename,hashtable,len(caseList))
        with open("temp/%s.txt"%filename,"w",encoding="UTF-8") as f:
            f.writelines(case["wsnr"])
        zf.write("temp/%s.txt" % filename,"编号%d-%s.txt" % (i+1,filename))
    zf.close()

if(__name__=="__main__"):
    con=condition.Conditon("毒品")
    exportAndToRar(con)