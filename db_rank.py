import pymysql


db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'database': 'db_ysks',
    'charset': 'utf8',
    'port': 3306
}

def get_rank_by_id(id):
    # 创建数据库连接
    conn = pymysql.connect(**db_config)
    # 创建游标
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        # 执行SQL查询
        cursor.execute("SELECT rank FROM rank WHERE id = %s", (id,))
        # 获取查询结果
        result = cursor.fetchone()
        return result.get('rank') if result else None
    except Exception as e:
        print("数据库操作出错：", e)
        return None
    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()


def get_user_right_rates_by_id(user_id):
    # 创建数据库连接
    conn = pymysql.connect(**db_config)
    # 创建游标
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        # 执行SQL查询
        cursor.execute("SELECT id, timu_id, right_rate FROM user_right_rate WHERE id = %s", (user_id,))
        # 获取所有查询结果
        results = cursor.fetchall()
        return results if results else None
    except Exception as e:
        print("数据库操作出错：", e)
        return None
    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()


def get_user_listen_right_rates_by_id(user_id):
    # 创建数据库连接
    conn = pymysql.connect(**db_config)
    # 创建游标
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        # 执行SQL查询
        cursor.execute("SELECT id, question_id, right_rate FROM listen_right_rate WHERE id = %s", (user_id,))
        # 获取所有查询结果
        results = cursor.fetchall()
        return results if results else None
    except Exception as e:
        print("数据库操作出错：", e)
        return None
    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()


def update_rank_based_on_accuracy(user_id, submitted_answers, correct_answers):
    # 创建数据库连接
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # 创建游标

    try:
        # 计算相同答案的数量
        common_answers = sum(1 for a, b in zip(submitted_answers, correct_answers) if a == b)

        # 更新用户的rank分
        cursor.execute("UPDATE rank SET rank = rank + %s WHERE id = %s", (common_answers, user_id))
        # 提交事务
        conn.commit()
        return True
    except Exception as e:
        print("数据库操作出错：", e)
        # 回滚事务
        conn.rollback()
        return False
    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()