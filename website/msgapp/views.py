#coding=utf-8   
from django.shortcuts import render
from datetime import datetime
import re
# Create your views here.
def msgproc(request):
    time = datetime.now()
    datalist = []
    if request.method == "POST":
        name = request.POST.get("name", None)
        phone = request.POST.get("phone", None)
        major = request.POST.get("major", None)
        if re.match(u"[\u4e00-\u9fa5]+", name) is None:
            with open('^msgdata.txt$', 'a+') as f:
                f.write("{}--{}--{}--{}\n".format(name, phone, major, time.strftime("%Y-%m-%d %H:%M:%S")))
                f.write("名字输入错误")
                f.write("\n")
            return render(request,'failed.html')
        if re.match("^\d{11}$", phone) is None:
            with open('msgdata.txt', 'a+') as f:
                f.write("{}--{}--{}--{}\n".format(name, phone, major, time.strftime("%Y-%m-%d %H:%M:%S")))
                f.write("电话输入错误")
                f.write("\n")
            return render(request,'failed.html')
        if re.match(u"^[\u4e00-\u9fa5]+$", major) is None:
            with open('msgdata.txt', 'a+') as f:
                f.write("{}--{}--{}--{}\n".format(name, phone, major, time.strftime("%Y-%m-%d %H:%M:%S")))
                f.write("专业输入错误")
                f.write("\n")
            return render(request,'failed.html')

        with open('msgdata.txt', 'a+') as f:
            f.write("{}--{}--{}--{}--\n".format(name, phone,\
                            major, time.strftime("%Y-%m-%d %H:%M:%S")))
        return render(request, 'succeed.html')
    if request.method == "GET":
        return render(request, "MsgSingleWeb.html", {"data":datalist})
