# coding=utf-8
from django.shortcuts import render
from datetime import datetime
import re
import sqlite3


# Create your views here.
def msgproc(request):
    time = datetime.now()
    datalist = []
    if request.method == "POST":
        name = request.POST.get("name", None)
        phone = request.POST.get("phone", None)
        major = request.POST.get("major", None)
        if re.match(u"[\u4e00-\u9fa5]+", name) is None:
            return render(request, 'failed.html')
        if re.match("^\d{11}$", phone) is None:
            return render(request, 'failed.html')
        if re.match(u"^[\u4e00-\u9fa5]+$", major) is None:
            return render(request, 'failed.html')

        with open('msgdata.txt', 'a+') as f:
            f.write("{}--{}--{}--{}--\n".format(name, phone, \
                                                major, time.strftime("%Y-%m-%d %H:%M:%S")))
        return render(request, 'succeed.html')
    if request.method == "GET":
        return render(request, "MsgSingleWeb.html", {"data": datalist})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        user_id = request.POST.get('id')
        if re.match(r'^\w{6,10}$', user_id) is None:
            return render(request, 'register_error.html')
        password = request.POST.get('password')
        if re.match(r'^[a-zA-Z]\w{6,10}$', password) is None:
            return render(request, 'register_error.html')
        conn = sqlite3.connect('test.db')
        conn.execute("create table if not exists user_msg (ID  TEXT PRIMARY KEY NOT NULL, PWD TEXT NOT NULL)")
        add = 'insert into user_msg(ID, PWD) VALUES((?), (?))'
        cursor = conn.cursor()
        try:
            cursor.execute(add, (user_id, password))
            conn.commit()
            cursor.close()
            conn.close()
            return render(request, 'register_success.html')
        except sqlite3.IntegrityError:
            return render(request, 'register_error.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        user_id = request.POST.get('id')
        if re.match(r'^\w{6,10}$', user_id) is None:
            return render(request, 'login_error.html')
        password = request.POST.get('password')
        if re.match(r'^[a-zA-Z]\w{6,10}$', password) is None:
            return render(request, 'login_error.html')
        conn = sqlite3.connect('test.db')
        cursor =conn.cursor()
        sign = 'select * from user_msg where ID="%s"' % user_id
        data = cursor.execute(sign).fetchone()
        if data is None:
            return render(request, 'login_error.html')
        if data[1] == password:
            return render(request, 'login_success.html')
        if data[1] != password:
            return render(request, 'login_error.html')


