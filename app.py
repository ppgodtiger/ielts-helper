from flask import *
import json
from flask import render_template,request
import itertools
import pymysql
import db
import db_word
import db_luntan
import re
import config
from english_dict import english_dict
from translate import dft_blueprint
import time
from flask import Flask,session
import os
import DBsession
from  flask_paginate import Pagination,get_page_parameter
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ORMDB import luntan
import db_admin
import score
import db_essay
import db_zhenti
import db_listen
import db_rank
import db_test
import score_LW
import score_BW
import db_video
engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/db_ysks?charset=utf8mb4")
Session = sessionmaker(engine)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.register_blueprint(dft_blueprint)
english_dict.load_data("./mydict/stardict.csv")


@app.route("/",methods = ['GET','POST'])
def main():
    return render_template('main.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    for key in list(session.keys()):
        session.pop(key)
        # 重定向到登录页面
    return redirect(url_for('main'))


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
            db_word.add(userid, 1)
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
    email = db.find_user_email(id)
    image_path = '/static/mrtx.jpg'#后期时间充足可以再写一个接口
    return render_template('userINFO.html',id = id,username = username,image_path=image_path,email = email )

#修改用户信息
@app.route("/euserinfo",methods=['GET', 'POST'])
def euserinfo():
    id = session.get('id')
    if request.method == 'POST':
        userid1 = request.form['userid']
        userpsw1 = request.form['userpsw']
        username1 = request.form['username']
        useremail1 = request.form['useremail']
        db.edit_self(userid1,userpsw1,username1,useremail1,id)
        flash('您的个人信息已更新！')
        return redirect(url_for('userinfo'))
    user = db.show_user(id)
    userid = user[0]
    userpsw = user[1]
    username = user[2]
    useremail = user[3]
    return render_template('edit_yourself.html',user = user, userpsw = userpsw,userid = userid,username = username,
                           useremail = useremail)


@app.route("/learn",methods=['GET','POST'])
def learn():
    id = session.get('id')

    return render_template('learn.html',id = id)


@app.route("/word_learn",methods=['GET','POST'])
def word_learn():
    id = session.get('id')


    return render_template('word_learn.html', id=id)
##################################################################################
#单词学习模块
@app.route("/word_new",methods=['GET','POST'])
def word_new():
    id = session.get('id')
    re = db_word.find_user_record(id)
    w,w1,w2,w3,w4 = db_word.show2(re)
    right = w[0]['translation']
    if right == w1:  # 判断哪个选项正确，并定义一个全局变量将正确答案存储，最后用来判断是否正确或者错误
        session['right'] = {'id': 1}
        JUD = 1
    elif right == w2:
        session['right'] = {'id': 2}
        JUD = 2
    elif right == w3:
        session['right'] = {'id': 3}
        JUD = 3
    elif right == w4:
        session['right'] = {'id': 4}
        JUD = 4
        print(JUD)
    jud = request.form.get('JUD', type=int)#此处的jug和JUD的意义不同
    result = '你好' + str(jud)
    print(result)
    if jud == 2:
        db_word.save_jud(id, re, jud)
    return render_template('word_new.html', w = w,w1 = w1,w2 = w2,w3 = w3,w4 = w4,JUD = JUD)

@app.route("/word_detail",methods=['GET','POST'])
def word_detail():
    re = 1
    id = session.get('id')
    re = db_word.find_user_record(id)
    code = request.args.get('code')
    option = request.args.get('option')
    # 将选项数据转换为整数类型
    option_id = int(option)

    right = session.get('right')
    if right:
        # 从 Session 对象中提取正确答案选项 ID
        right_id = session.get('right', {}).get('id')
        # 将其转换为整型（int）
        right_id_int = int(right_id)

        # 进行比较
    if option_id == right_id_int:
        JUD = 1
    else:
        JUD = 2  # 否则表示选择错误
    print(JUD)
    w,w1,w2,w3,w4 = db_word.show2(re)
    db_word.update_re(re, id)
    return render_template('word_detail.html', w = w)

@app.route("/word_wrong",methods=['GET','POST'])
def word_wrong():
    id = session.get('id')
    re = db_word.find_user_wrong(id)
    num =db_word.get_wrong_num(id)
    w,w1,w2,w3,w4 = db_word.show2(re)
    right = w[0]['translation']

    if right == w1:  # 判断哪个选项正确，并定义一个全局变量将正确答案存储，最后用来判断是否正确或者错误
        session['right'] = {'id': 1}
        JUD = 1
    elif right == w2:
        session['right'] = {'id': 2}
        JUD = 2
    elif right == w3:
        session['right'] = {'id': 3}
        JUD = 3
    elif right == w4:
        session['right'] = {'id': 4}
        JUD = 4
        print(JUD)
    jud = request.form.get('JUD', type=int)
    result = '你好' + str(jud)
    print(result)

    if jud == 1:
        db_word.update_wrong(re,id)
    return render_template('word_wrong.html', w = w,w1 = w1,w2 = w2,w3 = w3,w4 = w4,JUD = JUD, num = num)


@app.route("/word_detail_wrong",methods=['GET','POST'])
def word_detail_wrong():
    re = 1
    id = session.get('id')
    re = db_word.find_user_wrong(id)
    code = request.args.get('code')
    option = request.args.get('option')
    # 将选项数据转换为整数类型
    option_id = int(option)

    right = session.get('right')
    if right:
        # 从 Session 对象中提取正确答案选项 ID
        right_id = session.get('right', {}).get('id')
        # 将其转换为整型（int）
        right_id_int = int(right_id)

        # 进行比较
    if option_id == right_id_int:
        JUD = 1
    else:
        JUD = 2  # 否则表示选择错误
    print(JUD)

    w,w1,w2,w3,w4 = db_word.show2(re)

    if JUD == 1:
        db_word.update_wrong(re, id)

    return render_template('word_detail_wrong.html', w = w)



@app.route('/get-time')#用轮询实时更新数据库
def get_time():
    return jsonify({'time': time.time()})




@app.route("/luntan1", methods=['GET', 'POST'])
def luntan1():
    DBsession = Session()  # 创建一个引擎工作
    id = session.get('id')
    # 分页查询所有的数据  组装数据
    pageSize = 3  # 每页显示的记录条数
    # 获取页码 默认为1 int类型
    page = request.args.get(get_page_parameter(), type=int, default=1)

    start = (page - 1) * pageSize  # limit后第一个参数 每一页开始位置
    end = start + pageSize  # limit后第二个参数 每一页结束位置
    print(start)
    print(end)
    total = DBsession.query(luntan).count()  # 总记录数
    pagination = Pagination(by_version=3, page=page, total=total)  # bootstrap版本 默认为3
    luntan_info = DBsession.query(luntan).limit(3).offset(start).all()
    print(type(luntan_info))  # 检查luntan_info的类型
    print(luntan_info[0].title)
    #print(luntan_info[1].title)
    luntant_id= luntan_info[0].title_id
    # 总页码数量 用来控制分页按钮
    totalPage = total / pageSize if total % pageSize == 0 else (total / pageSize) + 1
    totalPage = int(totalPage)
    # 封装的分页参数,和页面显示的参数
    pageInfo = {"nowPage": page, "pageSize": pageSize, "total": total, "totalPage": totalPage}

    return render_template("luntan_index.html",id = id,luntan_info= luntan_info, pageInfo=pageInfo, pagination=pagination,luntant_id =luntant_id)



@app.route("/post", methods=['GET','POST'])
def post():
    id = session.get('id')
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if len(title) < 1 or len(body) < 1:
            message = "标题和内容不能为空"
            return render_template("post.html", message=message)

        try:
            db_luntan.get_new_title(id, title, body)
            message = "发帖成功"
            return render_template("post.html",id = id , message=message)
        except Exception as e:
            message = f"数据库操作出错: {e}"
            return render_template("post.html", message=message)

    return render_template("post.html", id = id )

@app.route("/cpost/<int:postid>", methods=['GET','POST'])
def cpost(postid):
    id = session.get('id')
    if request.method =='POST':
        cbody = request.form['body']
        if len(cbody)< 1:
            message = "评论不为空！"
        else:
            username = db.get_username(id)
            db_luntan.add_comment(id,postid,cbody,username)
        cbody = db_luntan.show_comment(postid)
        pinlun = [{'id':x,'username':y,'body':z} for x,y,z in cbody]
        return render_template('comment.html',message = message, pinlun = pinlun)


########################################################################################
#以下为管理员接口

@app.route("/admin_login",methods = ['GET', 'POST'])
def admin_login():
    global ID
    if request.method == 'POST':
        id = request.form['id']
        psw = request.form['psw']
        if db_admin.is_existed(id, psw):
            session['id'] = id  # 将用户名存储在session中
            print (session['id'])
            return render_template("/admin_index.html",id = session['id'])
        else:
            login_message = "账号或密码错误！请输入正确的账号密码！"
            return render_template("/admin_login.html", message=login_message)

    else:
        return render_template('/admin_login.html')


##样式测试页面
@app.route("/edit",methods = ['GET', 'POST'])
def edit():
    return render_template('/edit.html')



#######学生信息管理页面
@app.route("/stu_info",methods = ['GET', 'POST'])
def stu_info():

    return render_template('admin_stu_info.html')


#######学生背词数据页面
@app.route("/student_m",methods = ['GET', 'POST'])
def student_m():


    return render_template('admin_studentm.html')


#######作文信息管理页面
@app.route("/zuowen_info",methods = ['GET', 'POST'])
def zuowen_info():

    return render_template('admin_zuoweninfo.html')
#作文记录管理页面
@app.route("/zuowen_jilu",methods = ['GET', 'POST'])
def zuowen_jilu():

    return render_template('admin_zuowenjilu.html')



#######论坛信息管理页面
@app.route("/luntan_info",methods = ['GET', 'POST'])
def luntan_info():

    return render_template('admin_luntan.html')

#######真题信息管理页面
@app.route("/yuedu_info",methods = ['GET', 'POST'])
def yuedu_info():

    return render_template('admin_yuedu.html')
####视频管理
@app.route("/video_info",methods = ['GET', 'POST'])
def video_info():

    return render_template('admin_video.html')
####真题数据
@app.route("/get_video_list",methods = ['GET', 'POST'])
def get_video_list():
    yuedu_info = db_admin.find_video_all()

    data = {"code":0,
            "msg":"",
            "count":1000,
            "data":yuedu_info}
    return jsonify(data)
#后端向前端传输阅读真题的数据
@app.route("/get_yuedu_zhenti_list",methods = ['GET', 'POST'])
def get_yuedu_zhenti_list():
    yuedu_info = db_admin.find_yuedu_zhenti_all()

    data = {"code":0,
            "msg":"",
            "count":1000,
            "data":yuedu_info}
    return jsonify(data)
#后端数据库添加传输阅读真题的数据
@app.route('/add_yuedu_zhenti', methods=['POST'])
def add_yuedu_zhenti():
    data = request.form
    timu_id = data['timu_id']
    timu = data['timu']

    # 调用数据库函数添加数据
    result = db_admin.add_to_database(timu_id, timu)

    if result:
        return jsonify({'status': 'success', 'message': '阅读真题添加成功'})
    else:
        return jsonify({'status': 'error', 'message': '阅读真题添加失败'})

#######听力真题信息管理页面
@app.route("/listen_info",methods = ['GET', 'POST'])
def listen_info():

    return render_template('admin_listen.html')
#管理员rank页
@app.route("/rank",methods = ['GET', 'POST'])
def rank():

    return render_template('admin_rank.html')
#后端向前端传输阅读真题的数据
@app.route("/get_listen_zhenti_list",methods = ['GET', 'POST'])
def get_listen_zhenti_list():
    listen_info = db_admin.find_listen_zhenti_all()

    data = {"code":0,
            "msg":"",
            "count":1000,
            "data":listen_info}
    return jsonify(data)

#后端数据库添加传输阅读真题的数据
@app.route('/add_listen_zhenti', methods=['POST'])
def add_listen_zhenti():
    data = request.form
    question_id = data['timu_id']
    question_image = data['timu']

    # 调用数据库函数添加数据
    result = db_admin.add_to_database(question_id, question_image)

    if result:
        return jsonify({'status': 'success', 'message': '真题添加成功'})
    else:
        return jsonify({'status': 'error', 'message': '真题添加失败'})

#后端向前端传输rank数据
@app.route("/get_rank_list",methods = ['GET', 'POST'])
def get_rank_list():
    rank_info = db_admin.find_rank_all()

    data = {"code":0,
            "msg":"",
            "count":1000,
            "data":rank_info}

    return jsonify(data)
#后端向前端传输作文批改数据
#后端向前端传输作文数据
@app.route("/get_zuowen_list",methods = ['GET', 'POST'])
def get_zuowen_list():
    zuowen_info = db_admin.find_zuowen_all()

    data = {"code":0,
            "msg":"",
            "count":1000,
            "data":zuowen_info}

    return jsonify(data)
##查找作文信息
@app.route('/search_zuowen', methods=['GET'])
def search_zuowen_api():
    zuowen_id = request.args.get('zuowen_id')
    result = db_admin.search_zuowen(zuowen_id)
    if result:
        return jsonify({'code': 0, 'data': [result]})
    else:
        return jsonify({'code': 1, 'msg': '没有找到相关作文'})
#后端向前端传输作文批改数据
@app.route("/get_zuowenjilu_list",methods = ['GET', 'POST'])
def get_zuowenjilu_list():
    zuowen_info = db_admin.find_zuowenjilu_all()

    data = {"code":0,
            "msg":"",
            "count":1000,
            "data":zuowen_info}

    return jsonify(data)
#后端向前端传输学生数据
@app.route("/get_stu_list",methods = ['GET', 'POST'])
def get_stu_list():
    stu_info = db_admin.find_user_all()

    data = {"code":0,
            "msg":"",
            "count":1000,
            "data":stu_info}

    return jsonify(data)
#后端向前端传输论坛数据
@app.route("/get_luntan_list",methods = ['GET', 'POST'])
def get_luntan_list():
    zuowen_info = db_admin.find_luntan_all()
    data = {"code":0,
            "msg":"",
            "count":1000,
            "data":zuowen_info}
    return jsonify(data)

#前端的删除接口1
@app.route("/delete_stu_info/<int:id>", methods=['DELETE'])
def delete_stu_info(id):
    # 使用 DELETE 方法
    db_admin.del_stu_info(id)
    return jsonify({"message": "删除成功"}), 200

#前端的编辑接口1
@app.route("/edit_stu_info/<int:id>", methods=['GET', 'POST', 'PUT'])
def edit_stu_info(id):
    if request.method == 'PUT':
        data = request.get_json()
        print(data)
        db_admin.update_stu_info(data, id)
        # 返回一个成功的响应
        return jsonify({"message": "修改成功"}), 200
    else:
        # 如果不是PUT请求，返回一个错误
        return jsonify({'error': 'Method not allowed.'}), 405




@app.route('/admin_index',methods=['GET','POST'])
def admin_index():
    return render_template("admin_index.html")



@app.route('/admin_logout',methods=['GET','POST'])
def admin_logout():
    for key in list(session.keys()):
        session.pop(key)
        # 重定向到登录页面
    return redirect(url_for('admin_login'))


#学生做题数据
@app.route("/get_stu_jilu",methods = ['GET', 'POST'])
def get_stu_jilu():
    stu_info = db_admin.get_user_jilu()

    data = {"code":0,
            "msg":"",
            "count":1000,
            "data":stu_info}

    return jsonify(data)
#######考试信息管理
@app.route('/test_info',methods=['GET','POST'])
def test_info():
    return render_template("admin_test_info.html")

@app.route("/get_test_read_list",methods = ['GET', 'POST'])
def get_test_read_list():
    yuedu_info = db_admin.find_test_read_all()

    data = {"code":0,
            "msg":"",
            "count":1000,
            "data":yuedu_info}
    return jsonify(data)
#后端数据库添加传输阅读真题的数据
@app.route('/add_test_read', methods=['POST'])
def add_test_read():
    data = request.form
    timu_id = data['question_id']
    timu = data['read_pic']

    # 调用数据库函数添加数据
    result = db_admin.add_to_database(timu_id, timu)

    if result:
        return jsonify({'status': 'success', 'message': '阅读真题添加成功'})
    else:
        return jsonify({'status': 'error', 'message': '阅读真题添加失败'})

######学生考试数据
@app.route('/stu_test_info',methods=['GET','POST'])
def stu_test_info():
    return render_template("admin_stu_test.html")

@app.route("/get_testinfo_list",methods = ['GET', 'POST'])
def get_testinfo_list():
    yuedu_info = db_admin.find_test_info_all()

    data = {"code":0,
            "msg":"",
            "count":1000,
            "data":yuedu_info}
    return jsonify(data)


#############################################作文评分模块
@app.route('/rate_essay', methods=['GET','POST'])
def rate_essay():
    id = session.get('id')
    question,example = db_essay.get_zuowen_timu(id)
    if request.method == 'POST':
       essay_content = request.form.get('essay_content')
       if not essay_content:
           return "作文内容不能为空。", 400
       result = score.rate_essay(essay_content)
       return render_template('get_score.html', result=result,example = example)
    return render_template('write.html',question = question)


################真题练习模块

@app.route('/show_random_images')
def show_random_images():
    id = session.get('id')
    timu_id = db_zhenti.get_random_timu_id_by_right_rate()
    if timu_id:
        images = db_zhenti.get_images_for_timu_id(timu_id)
        num = db_zhenti.get_num_for_timu_id(timu_id)  # 获取循环次数
        return render_template('zhenti.html', images=images, timu_id=timu_id, id=id, num=num)
    else:
        return "No images found in the database."


#####处理前端提交的数据
@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    # 获取前端发送的答案数据
    data = request.json
    timu_id = data['timu_id']
    answers = data['answers']

    # 比对答案并计算正确率
    result = db_zhenti.compare_answers_and_calculate_accuracy(timu_id,answers)
    print(result)
    # 将结果存储在会话中
    session['result'] = result

    # 重定向到答案页面
    return redirect('/show_answer/' + str(timu_id))


#####阅读答案页面
@app.route('/show_answer/<int:timu_id>')
def show_answer(timu_id):
    # 从会话中获取结果
    result = session.get('result', {})
    id = session.get('id')
    answers = db_zhenti.get_answers_from_database(timu_id)  # 假设这是一个从数据库获取答案的函数

    # 获取submitted_answers, correct_answers和accuracy
    submitted_answers = result.get('submitted_answers', [])
    correct_answers = result.get('correct_answers', [])
    accuracy = result.get('accuracy', 0)
    print(accuracy)
    db_zhenti.update_user_right_rate(id, timu_id, accuracy)
    db_zhenti.save_submitted_answers_to_db(timu_id,submitted_answers)
    if db_rank.update_rank_based_on_accuracy(id, submitted_answers, correct_answers):
    # 渲染模板并传递结果
        return render_template('answer.html', timu_id=timu_id, submitted_answers=submitted_answers,
                           correct_answers=correct_answers, accuracy=accuracy, id=id, answers= answers)
###阅读删除
@app.route('/delete_yuedu_zhenti', methods=['POST'])
def delete_yuedu_zhenti():
    data = request.form
    timu_id = data['timu_id']

    # 调用数据库函数删除数据
    result = db_admin.delete_from_database(timu_id)

    if result:
        return jsonify({'status': 'success', 'message': '阅读真题删除成功'})
    else:
        return jsonify({'status': 'error', 'message': '阅读真题删除失败'})

#####跳转到真题主页
@app.route("/zhenti_index",methods=['GET','POST'])
def zhenti_index():
    id = session.get('id')

    return render_template("zhenti_index.html",id =id )

#######听力模块
@app.route('/show_random_listen_images')
def show_random_listen_images():
    id = session.get('id')
    question_id = db_listen.get_random_question_id()
    if question_id:
        images = db_listen.get_images_for_question_ids(question_id)
        print(images)
        listen_materials = db_listen.get_listen_material_for_question_id(question_id)
        num = 40
        listen_material_count = db_listen.get_listen_material_count_for_question_id(question_id)
        print(listen_material_count)
        return render_template('zhenti_listen.html', images=images, question_id=question_id, id=id, num=num, listen_materials=listen_materials,listen_material_count=listen_material_count)
    else:
        return "No images found in the database."

###处理接口
@app.route('/submit_listen_answers', methods=['POST','GET'])
def submit_listen_answers():
    # 获取前端发送的答案数据
    data = request.json
    question_id = data['question_id']
    answers = data['answers']
    result = db_listen.compare_Lanswers_and_calculate_accuracy(question_id, answers)
    print(result)
    session['result'] = result
    # 重定向到答案页面
    return redirect('/show_listen_answer/' + str(question_id))

###听力答案接口
@app.route('/show_listen_answer/<int:question_id>', methods=['POST','GET'])
def show_listen_answer(question_id):
    # 从会话中获取结果
    result = session.get('result', {})
    id = session.get('id')
    answers = db_listen.get_answers_from_database(question_id)  # 假设这是一个从数据库获取答案的函数

    # 获取submitted_answers, correct_answers和accuracy
    submitted_answers = result.get('submitted_answers', [])
    correct_answers = result.get('correct_answers', [])
    accuracy = result.get('accuracy', 0)
    print(accuracy)
    db_listen.update_user_right_Lrate(id, question_id, accuracy)
    db_listen.save_submitted_answers_to_db(question_id,submitted_answers)
    # 渲染模板并传递结果
    return render_template('answer.html', question_id=question_id, submitted_answers=submitted_answers,
                           correct_answers=correct_answers, accuracy=accuracy, id=id, answers= answers)

#####ranking页面
@app.route('/ranking', methods=['POST','GET'])
def ranking():
    id = session.get('id')
    rank = db_rank.get_rank_by_id(id)
    user_rates = db_rank.get_user_right_rates_by_id(id)
    user_listen_rates = db_rank.get_user_listen_right_rates_by_id(id)
    print(user_listen_rates)
    if user_rates:
        return render_template('ranking.html', user_rates=user_rates,rank=rank,id =id,user_listen_rates = user_listen_rates)
    else:
        return "没有找到对应的记录"

######阅读重新练习逻辑
@app.route('/practice/<int:timu_id>')
def practice(timu_id):
    id = session.get('id')
    if timu_id:
        images = db_zhenti.get_images_for_timu_id(timu_id)
        num = db_zhenti.get_num_for_timu_id(timu_id)  # 获取循环次数
        return render_template('zhenti.html', images=images, timu_id=timu_id, id=id, num=num)
    else:
        return "No images found in the database."
    return render_template('practice.html', timu_id=timu_id)

####查看阅读做题记录
@app.route('/show_practice_record/<int:timu_id>', methods=['POST','GET'])
def show_practice_record(timu_id):

    id = session.get('id')
    answers = db_zhenti.get_answers_from_database(timu_id)  # 假设这是一个从数据库获取答案的函数
    # 获取submitted_answers, correct_answers和accuracy
    submitted_answers = db_zhenti.get_answer_from_db(timu_id)
    correct_answers = db_zhenti.get_right_answer_from_db(timu_id)
    return render_template('answer.html', timu_id=timu_id, submitted_answers=submitted_answers,
                               correct_answers=correct_answers, id=id, answers=answers)


######听力重新练习逻辑
@app.route('/listen_practice/<int:question_id>')
def listen_practice(question_id):
    id = session.get('id')
    if question_id:
        images = db_listen.get_images_for_question_ids(question_id)
        print(images)
        listen_materials = db_listen.get_listen_material_for_question_id(question_id)
        num = 40
        listen_material_count = db_listen.get_listen_material_count_for_question_id(question_id)
        print(listen_material_count)
        return render_template('zhenti_listen.html', images=images, question_id=question_id, id=id, num=num, listen_materials=listen_materials,listen_material_count=listen_material_count)
    else:
        return "No images found in the database."

##查看听力做题记录
@app.route('/show_listen_record/<int:question_id>', methods=['POST','GET'])
def show_listen_record(question_id):
    id = session.get('id')
    answers = db_listen.get_answers_from_database(question_id)

    # 获取submitted_answers, correct_answers和accuracy
    submitted_answers = db_listen.get_answer_from_db(question_id)
    correct_answers = db_listen.get_right_answer_from_db(question_id)
    # 渲染模板并传递结果
    return render_template('Lanswer_record.html', question_id=question_id, submitted_answers=submitted_answers,
                           correct_answers=correct_answers, id=id, answers= answers)

#######考试中心
@app.route('/test_index', methods=['GET','POST'])
def test_index():
    id = session.get('id')

    return render_template('test_indexa.html',id = id)
#######听力考试
@app.route('/test_practice_listen', methods=['GET','POST'])
def test_practice_listen():
    id = session.get('id')
    question_id = db_listen.get_random_question_id()
    if question_id:
        images = db_listen.get_images_for_question_ids(question_id)
        print(images)
        listen_materials = db_listen.get_listen_material_for_question_id(question_id)
        num = 40
        listen_material_count = db_listen.get_listen_material_count_for_question_id(question_id)
        print(listen_material_count)
        return render_template('test_practice_listen.html', images=images, question_id=question_id, id=id, num=num,
                               listen_materials=listen_materials, listen_material_count=listen_material_count)
    else:
        return "No images found in the database."

#####处理前端提交的数据
@app.route('/submit_listen_answers_t',  methods=['GET','POST'])
def submit_listen_answers_t():
    # 获取前端发送的答案数据
    data = request.json
    question_id = data['question_id']
    answers = data['answers']
    # 比对答案并计算正确率
    result = db_test.compare_answers_and_calculate_score(question_id, answers)
    # 根据雅思听力评分标准计算分数
    session['correct_listen_answers'] = result['correct_listen_answers']
    session['submitted_listen_answers']=result['submitted_listen_answers']
    session['listen_score'] = result['listen_score']
    print(session['listen_score'])
    # 现在去阅读页面
    return redirect('/test_practice_read/'+str(question_id))
######阅读考试
@app.route('/test_practice_read/<int:question_id>')
def test_practice_read(question_id):
    id = session.get('id')
    print("已进入阅读模块")
    print(id)
    if question_id:
        images = db_test.get_images_for_question_ids(question_id)
        print(images)
        num = 40
        print(num)
        return render_template('test_practice_read.html', images=images, question_id=question_id, id=id, num=num,)
    else:
        return "No images found in the database."

#####处理前端提交的数据
@app.route('/submit_practice_read_answers_t/', methods=['POST'])
def submit_practice_read_answers_t():
    print("已进入阅读答案模块")
    data = request.json
    print(data)  # 应该打印出前端发送的 JSON 数据
    question_id = data['question_id']
    answers = data['answers']
    # 比对答案并计算正确率
    result = db_test.compare_answers_and_calculate_score_read(question_id, answers)
    # 根据雅思听力评分标准计算分数
    session['submitted_read_answers'] = result['submitted_read_answers']
    session['correct_read_answers'] = result['correct_read_answers']
    session['read_score'] = result['read_score']
    print(session['read_score'])
    # 现在去写作页面
    return redirect('/test_practice_Lwrite/' + str(question_id))

######小作文考试
@app.route('/test_practice_Lwrite/<int:question_id>',methods=['POST','GET'])
def test_practice_Lwrite(question_id):
    id = session.get('id')
    print("已进入小写作模块")
    print(id)
    if question_id:
        images = db_test.get_images_for_question_ids_Lwrite(question_id)
        print(images)
        return render_template('test_practice_write.html', images=images, question_id=question_id, id=id)
    else:
        return "No images found in the database."


@app.route('/submit_test_Lessay', methods=['POST','GET'])
def submit_test_Lessay():
    id = session.get('id')
    if request.method == 'POST':
        question_id = 1
        essay_content = request.form.get('essay_content')
        print(essay_content)
        db_test.save_answer_to_db(id, question_id,essay_content)
        if not essay_content:
            return "作文内容不能为空。", 400
        result = score_LW.rate_essay(essay_content)
        print(result)
        session['Lwrite_score'] = result
    return redirect('/test_practice_Bwrite/' + str(question_id))

######大作文考试
@app.route('/test_practice_Bwrite/<int:question_id>',methods=['POST','GET'])
def test_practice_Bwrite(question_id):
    id = session.get('id')
    print("已进入大写作模块")
    print(id)
    if question_id:
        images = db_test.get_images_for_question_ids_Bwrite(question_id)
        print(images)
        return render_template('test_practice_Bwrite.html', images=images, question_id=question_id, id=id)
    else:
        return "No images found in the database."

@app.route('/submit_test_Bessay', methods=['POST','GET'])
def submit_test_Bessay():
    id = session.get('id')
    if request.method == 'POST':
        question_id = 1
        essay_content = request.form.get('essay_content')
        print(essay_content)
        db_test.save_answer_to_dbB(id, question_id,essay_content)
        if not essay_content:
            return "作文内容不能为空。", 400
        result = score_BW.rate_essay(essay_content)
        print(result)
        session['Bwrite_score'] = result
        print(session['Bwrite_score'])
    return redirect('/show_test_score/' + str(question_id))

@app.route('/show_test_score/<int:question_id>', methods=['POST', 'GET'])
def show_test_score(question_id):
    id = session.get('id')
    submitted_listen_answers = session['submitted_listen_answers']
    submitted_read_answers = session['submitted_read_answers']
    correct_read_answers = session['correct_read_answers']
    correct_listen_answers = session['correct_listen_answers']
    listen_score = session['listen_score']
    read_score = session['read_score']
    Lwrite_score = session['Lwrite_score']
    Bwrite_score = session['Bwrite_score']
    Lwrite=db_test.get_user_lr(question_id,id)
    Bwrite=db_test.get_user_br(question_id,id)
    answer_Broute = db_test.get_Rbanswer_route(question_id)
    answer_Lroute = db_test.get_RLanswer_route(question_id)
    # 确保所有数据都是列表格式
    if not isinstance(submitted_listen_answers, list):
        submitted_listen_answers = [submitted_listen_answers]
    if not isinstance(submitted_read_answers, list):
        submitted_read_answers = [submitted_read_answers]
    if not isinstance(correct_listen_answers, list):
        correct_listen_answers = [correct_listen_answers]
    if not isinstance(correct_read_answers, list):
        correct_read_answers = [correct_read_answers]
    db_test.save_answers_to_db_LS(id, question_id, submitted_listen_answers, submitted_read_answers)
    db_test.update_or_insert_score(id, question_id, listen_score, read_score, Lwrite_score, Bwrite_score)
    return render_template('test_practice_score.html', submitted_listen_answers=submitted_listen_answers,
        submitted_read_answers=submitted_read_answers,correct_listen_answers=correct_listen_answers,
        correct_read_answers=correct_read_answers,listen_score=listen_score,
    read_score=read_score, Lwrite_score=Lwrite_score, Bwrite_score=Bwrite_score,Lwrite=Lwrite,  # 将小作文内容传递给模板
                           Bwrite=Bwrite,question_id = question_id,id = id,answer_Broute = answer_Broute,
                           answer_Lroute =answer_Lroute
                           )
####考试记录

@app.route('/video_index')
def video_index():
    # 从数据库获取视频列表
    id = session.get('id')
    videos = db_video.get_video_list()
    # 将视频列表传递给前端模板
    return render_template('video.html', videos=videos,id = id)

@app.route('/video/<filename>')
def video(filename):
    # 替换为你的视频文件存储路径
    video_path = f"videos/{filename}"
    print(video_path)
    return send_file(video_path, mimetype="video/mp4")

