import pymysql
import random

# 数据库连接配置
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'database': 'db_ysks',
    'charset': 'utf8',
    'port': 3306
}


def get_random_question_id():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT question_id FROM listen_question")
            question_ids = cursor.fetchall()
            if question_ids:
                random_question_ids = random.choice(question_ids)[0]
                return random_question_ids
            else:
                return None
    finally:
        connection.close()

def get_images_for_question_ids(question_ids):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 根据question_id获取所有相关的图片路径
            cursor.execute("SELECT question FROM listen_question WHERE question_id = %s", (question_ids,))
            images = cursor.fetchall()
            return images
    finally:
        connection.close()

def get_listen_material_for_question_id(question_id):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 根据question_id获取所有相关的listen_material
            cursor.execute("SELECT listen_material FROM listen_material WHERE question_id = %s", (question_id,))
            listen_materials = cursor.fetchall()
            print(listen_materials)
            return listen_materials

    finally:
        connection.close()

def get_listen_material_count_for_question_id(question_id):
    connection = pymysql.connect(**db_config,cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # 根据question_id获取listen_material的条数
            cursor.execute("SELECT COUNT(*) FROM listen_material WHERE question_id = %s", (question_id,))
            result = cursor.fetchone()
            count = result['COUNT(*)'] if result else 0
            return count
    finally:
        connection.close()

def compare_Lanswers_and_calculate_accuracy(question_id, submitted_answers):
    # 连接到数据库
    connection = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # 获取数据库中的答案
            sql = "SELECT `question_answer` FROM `listen_answer` WHERE `question_id` = %s"
            cursor.execute(sql, (question_id,))
            result = cursor.fetchone()

            # 检查result是否为None
            if result is None:
                raise ValueError(f"No record found for question_id: {question_id}")

            correct_answers = result['question_answer'].split(',') if 'question_answer' in result else []  # 现在result是一个字典

            # 比对答案并计算正确率
            correct_count = sum(a == b for a, b in zip(submitted_answers, correct_answers))
            accuracy = correct_count / len(submitted_answers)
            accuracy= round(accuracy, 3)
            print(accuracy)
            return {
                'submitted_answers': submitted_answers,
                'correct_answers': correct_answers,
                'accuracy': accuracy
            }
    finally:
        connection.close()

def get_answers_from_database(question_id):
    connection = pymysql.connect(**db_config)
    try:
        # 创建游标对象
        with connection.cursor() as cursor:
            # 执行SQL查询
            sql = "SELECT `question_image` FROM `listen_answer_pic` WHERE `question_id` = %s"
            cursor.execute(sql, (question_id,))

            # 获取查询结果
            result = cursor.fetchall()

            # 提取答案列表
            answers = [row[0] for row in result]

            return answers
    finally:
        # 关闭数据库连接
        connection.close()


def update_user_right_Lrate(user_id, question_id, accuracy):
    # 连接到数据库
    print("数据库链接成功")
    print(accuracy)
    connection = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # 检查数据库中是否已存在该用户的该题目的正确率记录
            cursor.execute(
                'SELECT * FROM listen_right_rate WHERE id = %s AND question_id = %s',
                (user_id, question_id)
            )
            result = cursor.fetchone()
            if result:
                # 如果已存在记录，则更新原数据
                cursor.execute(
                    'UPDATE listen_right_rate SET right_rate = %s WHERE id = %s AND question_id = %s',
                    (accuracy, user_id, question_id)
                )
            else:
                # 如果不存在记录，则插入新数据
                cursor.execute(
                    'INSERT INTO listen_right_rate (id, question_id, right_rate) VALUES (%s, %s, %s)',
                    (user_id, question_id, accuracy)
                )
        # 提交数据库事务
        connection.commit()
    finally:
        # 关闭数据库连接
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
            sql = "UPDATE listen_submit SET submit_answer = %s WHERE question_id = %s"
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
            sql = "SELECT submit_answer FROM listen_submit WHERE question_id = %s"
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


def get_right_answer_from_db(question_id):
    # 建立数据库连接
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 执行SQL查询
            sql = "SELECT question_answer FROM listen_answer WHERE question_id = %s"
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
