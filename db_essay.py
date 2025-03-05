import pymysql
import random

def get_con():
    return  pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            database='db_ysks',
            charset='utf8',
            port= 3306
    )

def get_zuowen_timu(id):
    num = random.randint(1,5)
    save_zuowenjilu(id, num)
    con = get_con()
    cur = con.cursor()
    sql = "select question from zuowen_timu where zuowen_id = '%s'"%(num)
    sql2 = "select example from zuowen_timu where zuowen_id='%s'"%(num)
    cur.execute(sql)
    question=cur.fetchone()[0]
    cur.execute(sql2)
    example = cur.fetchone()[0]
    print(question)
    return question,example

def save_zuowenjilu(id,zuowen_id):
    con = get_con()
    cur = con.cursor()
    sql = "INSERT INTO zuowen_jilu(zuowen_id,id) VALUES ('%s','%s')" % (zuowen_id,id)
    cur.execute(sql)
    con.commit()  # 将更改提交到数据库，对数据库内容有改变，需要commit()
    con.close()