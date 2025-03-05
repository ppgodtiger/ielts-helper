from flask import *
import json
from flask import render_template,request
import itertools
import pymysql
import db
import re
import config
from english_dict import english_dict
from translate import dft_blueprint
from flask import Flask,session
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.register_blueprint(dft_blueprint)
english_dict.load_data("./mydict/stardict.csv")

@app.route("/",methods = ['GET','POST'])
def main():
    return render_template('main.html')


@app.route("/login",methods = ['GET', 'POST'])
def login():
    global ID
    if request.method == 'POST':
        id = request.form['id']
        psw = request.form['psw']
        if db.is_existed(id, psw):
            session['id'] = id  # 将用户名存储在session中
            print (session['id'])
            return render_template("Index.html",id = session['id'])
        else:
            login_message = "账号或密码错误！请输入正确的账号密码！"
            return render_template("login.html", message=login_message)

    else:
        return render_template('login.html')


@app.route("/register",methods = ['GET', 'POST'])
def register():

    if request.method == 'POST':
        userid = request.form['userid']
        passwd = request.form['passwd']
        username = request.form['username']
        if db.exist_user(userid):
            rigister_message = "该用户已存在，请输入id与密码"
            return render_template("login.html",message =  rigister_message)
        else:
            if not re.match('^\\S{7,15}$', userid):     #re.match匹配失败返回none，本行验证用户名是否合法
                register_message = "请输入7-15位字符的id!"
                return render_template('register.html', message=register_message)
            if not re.match('^\\d{6,20}$', passwd):    #验证密码是否合法
                register_message = "请输入6-20位整数的密码!"
                return render_template('register.html', message=register_message)
            elif int(request.form['passwd']) != int(request.form['passwd2']):  # 两次密码输入是否相同
                register_message = "两次密码输入不同，请重新输入！"
                return render_template('register.html', message=register_message)
            db.add_user(userid, passwd, username)
            login_massage = "注册成功"
            return render_template('main.html', message=login_massage)
    else:
        return render_template('register.html')

@app.route("/index",methods=['GET', 'POST'])
def index():
    id = session.get('id')
    print(1)
    print(f"ID in index function: {id}")  # 添加这行代码来检查id是否在函数中正确获取
    return render_template('Index.html', id=id)


@app.route("/userinfo",methods=['GET', 'POST'])
def userinfo():
    id = session.get('id')
    username = db.find_user_name(id)
    image_path = '/static/mrtx.jpg'#后期时间充足可以再写一个接口
    return render_template('userINFO.html',id = id,username = username,image_path=image_path )

@app.route("/learn",methods=['GET','POST'])
def learn():
    id = session.get('id')

    return render_template('learn.html',id = id)




if __name__ == '__main__':
        app.run()