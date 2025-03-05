import pymysql

def get_con():
    return  pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            database='db_ysks',
            charset='utf8',
            port= 3306
    )


def is_existed(id, psw):#用于login页面用户登录 如果数据库有用户存在则登录
    con = get_con()
    cur = con.cursor()
    sql = "SELECT * FROM user_msg WHERE id ='%s' and psw ='%s'" % (id, psw)
    cur.execute(sql)
    result = cur.fetchall()
    print(result)
    if (len(result) == 0):
        return False
    else:
        return True

def exist_user(id):  # 用于register查询注册验证用户是否已经存在
    con = get_con()
    cur = con.cursor()
    sql = "SELECT * FROM user_msg WHERE id ='%s' " % (id)
    cur.execute(sql)
    result = cur.fetchall()
    con.close()
    if len(result) == 1:
        return True
    else:
        return False

def add_user(id, password,username):#用于register页面添加用户
    con = get_con()
    cur = con.cursor()
    # sql commands
    sql = "INSERT INTO user_msg(id, psw,username) VALUES ('%s','%s','%s')" % (id, password,username)
    # execute(sql)
    cur.execute(sql)
    # commit
    con.commit()  # 对数据库内容有改变，需要commit()
    con.close()

def find_user_name(id): #查找用户名
    con = get_con()
    cur = con.cursor()
    sql = "select username from user_msg where id = '%s'"%(id)
    cur.execute(sql)
    username = cur.fetchone()
    if len(username) == 1:
        return username[0]
    else:
        return False

    con.close()

def find_user_email(id):
    con = get_con()
    cur = con.cursor()
    sql = "select email from user_msg where id ='%s'"%(id)
    cur.execute(sql)
    email = cur.fetchone()
    if len(email) == 1:
        return email[0]
    else:
        return False

def show_user(id):
    con = get_con()
    cur = con.cursor()
    sql = "select * from user_msg where id ='%s'"%(id)
    cur.execute(sql)
    user = cur.fetchone()
    print(user)
    return user

def edit_self(userid,psw,name,email,id):
    con = get_con()
    cur = con.cursor()
    sql = "UPDATE user_msg SET psw ='%s' ,username = '%s',email = '%s' where id = '%s'"
    sql = sql % (psw,name, email, id)#使用字符串格式化方法 % 将 name、email 和 id 作为参数传递给 sql 字符串。这样做可以避免 SyntaxWarning。
    cur.execute(sql)

def get_username(id):
    con = get_con()
    cur = con.cursor()
    sql = "select username from user_msg where id = %'s'"%(id)
    cur.execute(sql)
    username = cur.fetchone()[0]
    print(username)
    return username
