from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import make_response
from flask import send_file
from flask import flash
from model.condition import Conditon
from Util import mongoUtil
from Util import exportUtil
from Util import util
import shutil
import os
import time
from urllib.parse import quote

app=Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return render_template("main.html")

@app.route("/result",methods=["POST","GET"])
def search():
    if request.method=="POST":
        ajmc = request.form["ajmc"]
        ah = request.form["ah"]
        gjc = request.form["gjc"]
        fycj = request.form["fycj"]
        fydy = request.form["fydy"]
        spcx = request.form["spcx"]
        sprqS = request.form["sprqS"]
        sprqE = request.form["sprqE"]
        fbrqS = request.form["fbrqS"]
        fbrqE = request.form["fbrqE"]
        con=Conditon(ajmc,ah,gjc,fycj,fydy,spcx,sprqS,sprqE,fbrqS,fbrqE)
        session["Condition"]=con.toDict()
        session["TotalNumber"]=mongoUtil.getCaseNumber(con)
        return redirect("/result?page=1") #重定向到加了个参数的url

    else:
        ajmc=session["Condition"]["ajmc"]
        ah=session["Condition"]["ah"]
        gjc=session["Condition"]["gjc"]
        fycj=session["Condition"]["fycj"]
        fydy=session["Condition"]["fydy"]
        spcx=session["Condition"]["spcx"]
        sprqS=session["Condition"]["sprqS"]
        sprqE=session["Condition"]["sprqE"]
        fbrqS=session["Condition"]["fbrqS"]
        fbrqE=session["Condition"]["fbrqE"]
        con=Conditon(ajmc,ah,gjc,fycj,fydy,spcx,sprqS,sprqE,fbrqS,fbrqE)

        currentPage=int(request.args.get("page",1))
        currentCaseList=mongoUtil.getOnePageCase(con,currentPage)
        totalnumber=mongoUtil.getCaseNumber(con)
        buttonHtmlStr=util.toButtonHtml(con,currentPage,"/result")

        return render_template("response.html",caseList=currentCaseList,
                               count=len(currentCaseList),
                               currentPage=currentPage,
                               buttonHtmlStr=buttonHtmlStr,
                               totalnumber=totalnumber) #模板支持把list传入
@app.route("/download")
def download():
    ajmc=session["Condition"]["ajmc"]
    ah=session["Condition"]["ah"]
    gjc=session["Condition"]["gjc"]
    fycj=session["Condition"]["fycj"]
    fydy=session["Condition"]["fydy"]
    spcx=session["Condition"]["spcx"]
    sprqS=session["Condition"]["sprqS"]
    sprqE=session["Condition"]["sprqE"]
    fbrqS=session["Condition"]["fbrqS"]
    fbrqE=session["Condition"]["fbrqE"]
    con=Conditon(ajmc,ah,gjc,fycj,fydy,spcx,sprqS,sprqE,fbrqS,fbrqE)
    #把上一次的搜索结果删除
    try:#没删除成功说明temp文件夹不存在
        shutil.rmtree("temp")
    except Exception:
        pass
    try:#不要打开temp文件夹 不然删不掉
        os.mkdir("temp")
    except Exception:
        flash("请关闭temp文件夹")
        time.sleep(1)
        os.mkdir("temp")
    #把搜出来的文档存成txt再打包。rar
    exportUtil.exportAndToRar(con)
    response = make_response(send_file("temp/%s.zip" % con.toString().strip(),as_attachment=True))
    #因为中文文件名在header中不支持 所以必须用以下写法来编码
    filenameUtf=quote(con.toString().strip()+".zip")
    response.headers["Content-Disposition"] = "attachment; filename=%s;" % filenameUtf +" filename*=utf-8''%s" % filenameUtf

    return response

if(__name__=="__main__"):
    app.secret_key='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()


