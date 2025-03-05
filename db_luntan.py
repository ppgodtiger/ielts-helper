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


def get_all():#获取全部论坛数据
    con = get_con()
    cur = con.cursor()
    sql = "select * from luntan"
    cur.execute(sql)
    all = cur.fetchall()
    data =  [{'id': x, 'title': y, 'body': z, 'username': w, 'title_id': a} for x, y, z, w, a in all]
    cur.close()
    return data

def get_new_title(id, title, body):#创建信的论坛主题
    con = get_con()
    cur = con.cursor()
    sql1 = "select username from user_msg where id = '%s'" % id
    cur.execute(sql1)
    username1 = cur.fetchone()
    username = username1[0]
    sql2 = "insert into luntan(id, title, body, username) values('%s','%s','%s','%s')"%(id, title, body, username)
    cur.execute(sql2)
    con.commit()  # 将更改提交到数据库，对数据库内容有改变，需要commit()
    con.close()

def get_title_num():#获取总论坛的数量，作用于ORM分页
    con = get_con()
    cur = con.cursor()
    sql = "SELECT COUNT(*) FROM luntan"
    cur.execute(sql)
    total = cur.fetchall()[0]
    print(total)
    con.close()
    return total

def show_comment(t_id):
    arr2 = []
    con = get_con()
    cur = con.cursor()
    sql = "select id,username,body from comment where title_id = '%s' " %(t_id)
    cur.execute(sql)
    result = cur.fetchall()  # 返回查询到的数据
    for i in result:
        arr = list(i)
        arr2.append(arr)
    con.close()
    return arr2

def add_comment(t_id,username,id,body):
    con = get_con()
    cur = con.cursor()
    sql = "INSERT INTO comment(id,title_id,body,username) VALUES ('%s','%s','%s')" % (id,t_id, body, username)
    cur.execute(sql)  # 执行sql
    con.commit()  # 将更改提交到数据库，对数据库内容有改变，需要commit()
    con.close()