# db_functions.py
import pymysql
import random
from pymysql.cursors import DictCursor
# 数据库配置信息
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'database': 'db_ysks',
    'charset': 'utf8',
    'port': 3306
}

def get_random_timu_id():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 获取所有不同的timu_id
            cursor.execute("SELECT DISTINCT timu_id FROM zhenti")
            timu_ids = cursor.fetchall()
            if timu_ids:
                # 随机选择一个timu_id
                random_timu_id = random.choice(timu_ids)[0]
                return random_timu_id
            else:
                return None
    finally:
        connection.close()

def get_images_for_timu_id(timu_id):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 根据timu_id获取所有相关的图片路径
            cursor.execute("SELECT timu FROM zhenti WHERE timu_id = %s", (timu_id,))
            images = cursor.fetchall()
            return images
    finally:
        connection.close()
def get_answers_from_database(timu_id):
    connection = pymysql.connect(**db_config)
    try:
        # 创建游标对象
        with connection.cursor() as cursor:
            # 执行SQL查询
            sql = "SELECT `answer` FROM `answer` WHERE `timu_id` = %s"
            cursor.execute(sql, (timu_id,))

            # 获取查询结果
            result = cursor.fetchall()

            # 提取答案列表
            answers = [row[0] for row in result]

            return answers
    finally:
        # 关闭数据库连接
        connection.close()

def get_num_for_timu_id(timu_id):
    # 连接到数据库
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 执行SQL查询
            sql = "SELECT num FROM zhenti_count WHERE timu_id = %s"
            cursor.execute(sql, (timu_id,))
            result = cursor.fetchone()[0]
            print(result)
            return result if result else 0
    except TypeError:
        # 处理查询结果为None的情况
        return 0
    finally:
        # 关闭数据库连接
        connection.close()


def compare_answers_and_calculate_accuracy(timu_id, submitted_answers):
    # 连接到数据库
    connection = pymysql.connect(**db_config, cursorclass=DictCursor)
    try:
        with connection.cursor() as cursor:
            # 获取数据库中的答案
            sql = "SELECT `answer` FROM `answer_min` WHERE `timu_id` = %s"
            cursor.execute(sql, (timu_id,))
            result = cursor.fetchone()

            # 检查result是否为None
            if result is None:
                raise ValueError(f"No record found for timu_id: {timu_id}")

            correct_answers = result['answer'].split(',') if 'answer' in result else []  # 现在result是一个字典

            # 比对答案并计算正确率
            correct_count = sum(a == b for a, b in zip(submitted_answers, correct_answers))
            accuracy = correct_count / len(submitted_answers)
            accuracy= round(accuracy, 3)
            return {
                'submitted_answers': submitted_answers,
                'correct_answers': correct_answers,
                'accuracy': accuracy
            }
    finally:
        connection.close()

def update_user_right_rate(user_id, timu_id, accuracy):
    # 连接到数据库
    print("数据库链接成功")
    print(accuracy)
    connection = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # 检查数据库中是否已存在该用户的该题目的正确率记录
            cursor.execute(
                'SELECT * FROM user_right_rate WHERE id = %s AND timu_id = %s',
                (user_id, timu_id)
            )
            result = cursor.fetchone()
            if result:
                # 如果已存在记录，则更新原数据
                cursor.execute(
                    'UPDATE user_right_rate SET right_rate = %s WHERE id = %s AND timu_id = %s',
                    (accuracy, user_id, timu_id)
                )
            else:
                # 如果不存在记录，则插入新数据
                cursor.execute(
                    'INSERT INTO user_right_rate (id, timu_id, right_rate) VALUES (%s, %s, %s)',
                    (user_id, timu_id, accuracy)
                )
        # 提交数据库事务
        connection.commit()
    finally:
        # 关闭数据库连接
        connection.close()

import pymysql
import random

def get_random_timu_id_by_right_rate():
    connection = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # 查询zhenti表中的所有timu_id
            cursor.execute("SELECT timu_id FROM zhenti")
            zhenti_timu_ids = set(row['timu_id'] for row in cursor.fetchall())

            # 查询user_right_rate表中的所有timu_id
            cursor.execute("SELECT timu_id FROM user_right_rate")
            urr_timu_ids = set(row['timu_id'] for row in cursor.fetchall())

            # 找到zhenti存在但user_right_rate不存在的timu_id
            priority_timu_ids = zhenti_timu_ids - urr_timu_ids

            # 如果有符合条件的timu_id，随机返回一个
            if priority_timu_ids:
                return random.choice(list(priority_timu_ids))

            # 如果没有符合条件的timu_id，使用原来的权重算法
            cursor.execute("SELECT timu_id, right_rate FROM user_right_rate")
            results = cursor.fetchall()

            # 计算每个题目的权重
            weights = [(1 - row['right_rate']) for row in results]

            # 如果所有题目的right_rate都为1，则随机选择一个题目
            if sum(weights) == 0:
                return random.choice([row['timu_id'] for row in results])

            # 根据权重随机选择题目
            total_weight = sum(weights)
            chosen_index = random.random() * total_weight
            current_weight = 0
            for i, weight in enumerate(weights):
                current_weight += weight
                if current_weight >= chosen_index:
                    return results[i]['timu_id']

            # 如果没有选中任何题目，返回None
            return None
    finally:
        connection.close()
def save_submitted_answers_to_db(id, submitted_answers):
    # 建立数据库连接
    connection = pymysql.connect(**db_config)
    print(submitted_answers)
    try:
        with connection.cursor() as cursor:
            # 将所有答案放入一个字符串中，并用逗号分隔
            answers_str = ','.join(submitted_answers)
            # 尝试更新现有记录
            sql = "UPDATE zhenti_submit SET submit_answer = %s WHERE timu_id = %s"
            cursor.execute(sql, (answers_str, id))

            # 提交事务
            connection.commit()
    finally:
        # 关闭数据库连接
        connection.close()

def get_answer_from_db(question_id):
    # 建立数据库连接
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 执行SQL查询
            sql = "SELECT submit_answer FROM zhenti_submit WHERE timu_id = %s"
            cursor.execute(sql, (question_id,))
            # 获取结果
            result = cursor.fetchone()
            # 如果结果存在，分割答案并返回，否则返回空列表
            if result:
                return result[0].split(',')
            else:
                return []
    finally:
        # 关闭数据库连接
        connection.close()


def get_right_answer_from_db(timu_id):
    # 建立数据库连接
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 执行SQL查询
            sql = "SELECT answer FROM answer_min WHERE timu_id = %s"
            cursor.execute(sql, (timu_id,))
            # 获取结果
            result = cursor.fetchone()
            # 如果结果存在，分割答案并返回，否则返回空列表
            if result:
                return result[0].split(',')
            else:
                return []
    finally:
        # 关闭数据库连接
        connection.close()

