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

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'database': 'db_ysks',
    'charset': 'utf8',
    'port': 3306
}


def is_existed(id, psw):#用于login页面用户登录 如果数据库有用户存在则登录
    con = get_con()
    cur = con.cursor()
    sql = "SELECT * FROM admin_msg WHERE id ='%s' and psw ='%s'" % (id, psw)
    cur.execute(sql)
    result = cur.fetchall()
    print(result)
    if (len(result) == 0):
        return False
    else:
        return True

def find_user_all():#查找全部用户信息返回给前端表格
    con = get_con()
    cur = con.cursor()
    sql = "select * from user_msg"
    cur.execute(sql)
    result = cur.fetchall()
    date = [{'id': x, 'psw': y, 'username': z, 'email': w,} for x, y, z, w, in result]
    return date

def del_stu_info(id):
    con = get_con()
    cur = con.cursor()
    sql = "DELETE FROM user_msg WHERE id = '%s'"% id
    cur.execute(sql)
    con.commit()  # 对数据库内容有改变，需要commit()
    con.close()

def update_stu_info(data,id):
    con = get_con()
    cur = con.cursor()
    info = data
    sql = "UPDATE user_msg SET psw = %s, username = %s, email = %s WHERE id = %s"
    cur.execute(sql, (info['psw'], info['username'], info['email'], id))
    con.commit()  # 对数据库内容有改变，需要commit()
    con.close()

def get_user_jilu():#查找做题记录
    con = get_con()
    cur = con.cursor()
    sql = "select * from jilu"
    cur.execute(sql)
    result = cur.fetchall()
    date = [{'id': x, 'e_id':y, } for x,y in result]
    return date

def find_zuowen_all():#查找全部用户信息返回给前端表格
    con = get_con()
    cur = con.cursor()
    sql = "select * from zuowen_timu"
    cur.execute(sql)
    result = cur.fetchall()
    date = [{'zuowen_id': x, 'example': y, 'question': z, } for x, y, z, in result]
    return date

def find_zuowenjilu_all():#查找全部用户信息返回给前端表格
    con = get_con()
    cur = con.cursor()
    sql = "select * from zuowen_jilu"
    cur.execute(sql)
    result = cur.fetchall()
    date = [{'zuowen_id': x, 'id': y, } for x, y, in result]
    return date

def find_luntan_all():#查找全部用户信息返回给前端表格
    con = get_con()
    cur = con.cursor()
    sql = "select * from luntan"
    cur.execute(sql)
    result = cur.fetchall()
    date = [{'id': x, 'title': y, 'body': z,'username':m,'title_id':n } for x, y, z,m,n in result]
    return date

def find_yuedu_zhenti_all():#查找全部用户信息返回给前端表格
    con = get_con()
    cur = con.cursor()
    sql = "select * from zhenti"
    cur.execute(sql)
    result = cur.fetchall()
    date = [{'timu_id': x, 'timu': y, } for x, y in result]
    return date

def add_to_database(timu_id, timu):
    # 创建数据库连接
    connection = pymysql.connect(**db_config,cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # 执行SQL插入语句
            sql = "INSERT INTO `zhenti` (`timu_id`, `timu`) VALUES (%s, %s)"
            cursor.execute(sql, (timu_id, timu))
        # 提交事务
        connection.commit()
        return True
    except Exception as e:
        print(e)
        # 回滚事务
        connection.rollback()
        return False
    finally:
        # 关闭数据库连接
        connection.close()

import pymysql  # 假设使用pymysql库

def delete_from_database(timu_id):
    # 创建数据库连接
    connection = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # 执行SQL删除语句
            sql = "DELETE FROM `zhenti` WHERE `timu_id` = %s"
            cursor.execute(sql, (timu_id,))
        # 提交事务
        connection.commit()
        return True
    except Exception as e:
        print(e)
        # 回滚事务
        connection.rollback()
        return False
    finally:
        # 关闭数据库连接
        connection.close()

def find_listen_zhenti_all():#查找全部用户信息返回给前端表格
    con = get_con()
    cur = con.cursor()
    sql = "select * from listen_answer_pic"
    cur.execute(sql)
    result = cur.fetchall()
    date = [{'question_id': x, 'question_image': y, } for x, y in result]
    return date

def find_rank_all():
    con = get_con()
    cur = con.cursor()
    sql = "select * from rank"
    cur.execute(sql)
    result = cur.fetchall()
    date = [{'id': x, 'rank': y, } for x, y in result]
    return date

def search_zuowen(zuowen_id):
    # 连接数据库
    conn = get_con()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # 执行SQL查询
        cursor.execute("SELECT * FROM zuowen_timu WHERE zuowen_id = %s", (zuowen_id,))
        result = cursor.fetchone()
        return result
    except Exception as e:
        print("查询出错", e)
        return None
    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()

def find_test_read_all():#查找全部用户信息返回给前端表格
    con = get_con()
    cur = con.cursor()
    sql = "select * from test_read_question"
    cur.execute(sql)
    result = cur.fetchall()
    date = [{'question_id': x, 'read_pic': y, } for x, y in result]
    return date

def add_to_database_test(timu_id, timu):
    # 创建数据库连接
    connection = pymysql.connect(**db_config,cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # 执行SQL插入语句
            sql = "INSERT INTO `test_read_question` (`question_id`, `read_pic`) VALUES (%s, %s)"
            cursor.execute(sql, (timu_id, timu))
        # 提交事务
        connection.commit()
        return True
    except Exception as e:
        print(e)
        # 回滚事务
        connection.rollback()
        return False
    finally:
        # 关闭数据库连接
        connection.close()

def find_test_info_all():#查找全部用户信息返回给前端表格
    con = get_con()
    cur = con.cursor()
    sql = "select * from test_record"

    cur.execute(sql)
    result = cur.fetchall()
    date = [{'id': x, 'question_id': y, 'listen_submit':z,'read_submit':m } for x, y,z,m in result]
    return date
def find_video_all():
    con = get_con()
    cur = con.cursor()
    sql = "select * from video"

    cur.execute(sql)
    result = cur.fetchall()
    date = [{'video_id': x, 'video_path': y, } for x, y, in result]
    return date