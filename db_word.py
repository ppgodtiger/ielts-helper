import random
import pymysql

def get_con():
    return  pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            database='db_ysks',
            charset='utf8',
            port=3306
    )

def add(id, num):#添加错题记录
    con = get_con()
    cur = con.cursor()
    # sql commands
    sql = "INSERT INTO jilu(id, e_id) VALUES ('%s','%s')" % (id, num)
    # execute(sql)
    cur.execute(sql)
    # commit
    con.commit()  # 对数据库内容有改变，需要commit()
    con.close()


def show2(e_id):  # 背单词页面的数据库代码
    num1 = random.randint(1, 399)
    num2 = random.randint(399, 699)
    num3 = random.randint(699, 999)
    con = get_con()
    cur = con.cursor()
    sql = "SELECT * FROM k_e_word WHERE id ='%s'" % e_id
    sql1 = "SELECT translation FROM k_e_word WHERE id ='%s'" % e_id
    sql2 = "SELECT translation FROM k_e_word WHERE id ='%s'" % (e_id + num1)
    sql3 = "SELECT translation FROM k_e_word WHERE id ='%s'" % (e_id + num2)
    sql4 = "SELECT translation FROM k_e_word WHERE id ='%s'" % (e_id + num3)

    cur.execute(sql)
    u = cur.fetchall()
    # date = np.array([row[0] for row in u.fetchall()])
    date = [{'id': x, 'word': y, 'phonetic': z, 'definition': w, 'translation': a, 'exchange': b} for x, y, z, w, a, b
            in u]

    cur.execute(sql1)  # 将数据预处理
    u1 = cur.fetchall()
    a1 = u1[0][0]
    cur.execute(sql2)
    u2 = cur.fetchall()
    a2 = u2[0][0]
    cur.execute(sql3)
    u3 = cur.fetchall()
    a3 = u3[0][0]
    cur.execute(sql4)
    u4 = cur.fetchall()
    a4 = u4[0][0]

    data = [a1, a2, a3, a4]
    random.shuffle(data)
    b1 = data[0]
    b2 = data[1]
    b3 = data[2]
    b4 = data[3]

    cur.close()
    con.close()
    return date, b1, b2, b3, b4


def find_user_record(id):#查找用户的背词记录
    con = get_con()
    cur = con.cursor()
    print(id)
    sql ="select e_id from jilu where id = '%s'" % id
    cur.execute(sql)
    re = cur.fetchone()
    print(re)
    con.close()
    return re[0]

def update_re(e_id,id):#跟新背单词记录
    con = get_con()
    cur = con.cursor()
    print(e_id)
    e_id_new = e_id + 1
    print(e_id_new)
    sql = "UPDATE jilu SET e_id = '%s' WHERE id = '%s'" % (e_id_new, id)
    cur.execute(sql)
    con.commit()  # 对数据库内容有改变，需要commit()
    con.close

def save_jud(id, e_id, flag):#保存错题信息
    con = get_con()
    cur = con.cursor()
    sql = "INSERT INTO jilu_cuoti(id,e_id,flag) VALUES ('{}','{}','{}')".format(id, e_id, flag)
    cur.execute(sql)
    con.close

def find_user_wrong(id):#查找用户错词
    con = get_con()
    cur = con.cursor()
    sql = "select e_id from jilu_cuoti where id = '%s' and flag = 2"% id
    cur.execute(sql)
    wrong = cur.fetchone()
    print(wrong[0])
    return wrong[0]
    con.close()

def update_wrong(re, id):#更新错题记录
    con = get_con()
    cur = con.cursor()
    sql = "update jilu_cuoti set flag = 1 where e_id = '%s' AND id = '%s'" %(re ,id)
    cur.execute(sql)
    con.commit()  # 对数据库内容有改变，需要commit()
    con.close()

def get_wrong_num(id):#获取错题数目
    con = get_con()
    cur = con.cursor()
    sql = "select * from jilu_cuoti where id = '%s' and flag = 2" %id
    cur.execute(sql)
    num = cur.fetchall()
    num1 = len(num)
    print("错词长度为" + str(num1))
    return num1
    con.close()