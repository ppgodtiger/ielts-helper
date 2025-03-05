import random
import pymysql
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




def compare_answers_and_calculate_score(timu_id, submitted_answers):
    # 连接到数据库
    connection = pymysql.connect(**db_config, cursorclass=DictCursor)
    try:
        with connection.cursor() as cursor:
            # 获取数据库中的答案
            sql = "SELECT `question_answer` FROM `listen_answer` WHERE `question_id` = %s"
            cursor.execute(sql, (timu_id,))
            result = cursor.fetchone()

            # 检查result是否为None
            if result is None:
                raise ValueError(f"No record found for timu_id: {timu_id}")

            correct_answers = result['question_answer'].split(',') if 'question_answer' in result else [] # 现在result是一个字典

            # 比对答案并计算正确率
            correct_count = sum(a == b for a, b in zip(submitted_answers, correct_answers))

            print(correct_count)
            # 根据雅思听力评分标准计算分数
            if correct_count == 0:
                score = 0
            elif correct_count == 1:
                score = 2
            elif correct_count == 2:
                score = 2.5
            elif 3 <= correct_count <= 5:
                score = 3
            elif 6 <= correct_count <= 9:
                score = 3.5
            elif 10 <= correct_count <= 12:
                score = 4.0
            elif 13 <= correct_count <= 15:
                score = 4.5
            elif 16 <= correct_count <= 19:
                score = 5.0
            elif 20 <= correct_count <= 22:
                score = 5.5
            elif 23 <= correct_count <= 26:
                score = 6.0
            elif 27 <= correct_count <= 29:
                score = 6.5
            elif 30 <= correct_count <= 32:
                score = 7.0
            elif 33 <= correct_count <= 34:
                score = 7.5
            elif 35 <= correct_count <= 36:
                score = 8.0
            elif 37 <= correct_count <= 38:
                score = 8.5
            elif 39 <= correct_count <= 40:
                score = 9.0
            else:
                score = 0

            return {
                'submitted_listen_answers': submitted_answers,
                'correct_listen_answers': correct_answers,
                'listen_score': score
            }
    finally:
        connection.close()

def get_images_for_question_ids(question_ids):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 根据question_id获取所有相关的图片路径
            cursor.execute("SELECT read_pic FROM test_read_question WHERE question_id = %s", (question_ids,))
            images = cursor.fetchall()
            return images
    finally:
        connection.close()

def compare_answers_and_calculate_score_read(timu_id, submitted_answers):
    # 连接到数据库
    connection = pymysql.connect(**db_config, cursorclass=DictCursor)
    try:
        with connection.cursor() as cursor:
            # 获取数据库中的答案
            sql = "SELECT `read_answer` FROM `test_read_answer` WHERE `question_id` = %s"
            cursor.execute(sql, (timu_id,))
            result = cursor.fetchone()

            # 检查result是否为None
            if result is None:
                raise ValueError(f"No record found for timu_id: {timu_id}")

            correct_answers = result['read_answer'].split(',') if 'read_answer' in result else [] # 现在result是一个字典

            # 比对答案并计算正确率
            correct_count = sum(a == b for a, b in zip(submitted_answers, correct_answers))

            print(correct_count)
            # 根据雅思听力评分标准计算分数
            if correct_count == 0:
                score = 0
            elif correct_count == 1:
                score = 2
            elif correct_count == 2:
                score = 2.5
            elif 3 <= correct_count <= 5:
                score = 3
            elif 6 <= correct_count <= 9:
                score = 3.5
            elif 10 <= correct_count <= 12:
                score = 4.0
            elif 13 <= correct_count <= 15:
                score = 4.5
            elif 16 <= correct_count <= 19:
                score = 5.0
            elif 20 <= correct_count <= 22:
                score = 5.5
            elif 23 <= correct_count <= 26:
                score = 6.0
            elif 27 <= correct_count <= 29:
                score = 6.5
            elif 30 <= correct_count <= 32:
                score = 7.0
            elif 33 <= correct_count <= 34:
                score = 7.5
            elif 35 <= correct_count <= 36:
                score = 8.0
            elif 37 <= correct_count <= 38:
                score = 8.5
            elif 39 <= correct_count <= 40:
                score = 9.0
            else:
                score = 0

            return {
                'submitted_read_answers': submitted_answers,
                'correct_read_answers': correct_answers,
                'read_score': score
            }
    finally:
        connection.close()

def get_images_for_question_ids_Lwrite(question_ids):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 根据question_id获取所有相关的图片路径
            cursor.execute("SELECT question_pic FROM write_test_little WHERE question_id = %s", (question_ids,))
            images = cursor.fetchall()
            return images
    finally:
        connection.close()

def get_images_for_question_ids_Bwrite(question_ids):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 根据question_id获取所有相关的图片路径
            cursor.execute("SELECT question_pic FROM write_test_big WHERE question_id = %s", (question_ids,))
            images = cursor.fetchall()
            return images
    finally:
        connection.close()

def save_answer_to_db(id, question_id, essay_content):
    # 使用db_config连接到数据库
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 更新作文内容
            sql = "UPDATE user_write_le SET answer = %s WHERE id = %s AND question_id = %s"
            cursor.execute(sql, (essay_content, id, question_id))

            # 如果受影响的行数为0，则插入新记录
            if cursor.rowcount == 0:
                sql = "INSERT INTO user_write_le (id, question_id, answer) VALUES (%s, %s, %s)"
                cursor.execute(sql, (id, question_id, essay_content))

            # 提交事务
            connection.commit()
    except Exception as e:
        print("Error:", e)
        connection.rollback()
    finally:
        # 关闭连接
        connection.close()


def save_answer_to_dbB(id, question_id, essay_content):
    # 使用db_config连接到数据库
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 更新作文内容
            sql = "UPDATE user_write_be SET answer = %s WHERE id = %s AND question_id = %s"
            cursor.execute(sql, (essay_content, id, question_id))

            # 如果受影响的行数为0，则插入新记录
            if cursor.rowcount == 0:
                sql = "INSERT INTO user_write_be (id, question_id, answer) VALUES (%s, %s, %s)"
                cursor.execute(sql, (id, question_id, essay_content))

            # 提交事务
            connection.commit()
    except Exception as e:
        print("Error:", e)
        connection.rollback()
    finally:
        # 关闭连接
        connection.close()

def save_answers_to_db_LS(id, question_id, submitted_listen_answers, submitted_read_answers):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 将答案列表转换为由逗号分隔的字符串
            listen_submit = ','.join(submitted_listen_answers)
            read_submit = ','.join(submitted_read_answers)
            # 执行SQL插入语句
            cursor.execute("INSERT INTO test_record (id, question_id, listen_submit, read_submit) VALUES (%s, %s, %s, %s)",
                           (id, question_id, listen_submit, read_submit))
        # 提交事务
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        # 如果发生错误，回滚事务
        connection.rollback()
    finally:
        # 关闭数据库连接
        connection.close()


def get_user_lr(id, question_id):
    # 创建数据库连接
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # 查询answer
    sql = "SELECT answer FROM user_write_le WHERE id = %s AND question_id = %s"
    cursor.execute(sql, (id, question_id))

    # 获取查询结果
    result = cursor.fetchone()
    answer = result['answer'] if result else None

    # 关闭数据库连接
    cursor.close()
    conn.close()

    return answer


def get_user_br(id, question_id):
    # 创建数据库连接
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # 查询answer
    sql = "SELECT answer FROM user_write_be WHERE id = %s AND question_id = %s"
    cursor.execute(sql, (id, question_id))

    # 获取查询结果
    result = cursor.fetchone()
    answer = result['answer'] if result else None

    # 关闭数据库连接
    cursor.close()
    conn.close()

    return answer

def get_RLanswer_route(question_id):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 根据question_id获取所有相关的图片路径
            cursor.execute("SELECT answer_route FROM lwrite_route WHERE question_id = %s", (question_id,))
            images = cursor.fetchall()
            return images[0]
    finally:
        connection.close()


def get_Rbanswer_route(question_id):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 根据question_id获取所有相关的图片路径
            cursor.execute("SELECT answer_route FROM bwrite_route WHERE question_id = %s", (question_id,))
            images = cursor.fetchall()
            return images[0]
    finally:
        connection.close()

def update_or_insert_score(id, question_id, listen_score, read_score, Lwrite_score, Bwrite_score):
    # 建立数据库连接
    connection = pymysql.connect(**db_config,cursorclass=DictCursor)
    try:
        with connection.cursor() as cursor:
            # 尝试更新现有记录
            sql = "UPDATE test_score SET listen_score = %s, read_score = %s, Lwrite_score = %s, Bwrite_score = %s WHERE id = %s AND question_id = %s"
            cursor.execute(sql, (listen_score, read_score, Lwrite_score, Bwrite_score, id, question_id))

            # 如果受影响的行数为0，则插入新记录
            if cursor.rowcount == 0:
                sql = "INSERT INTO test_score (id, question_id, listen_score, read_score, Lwrite_score, Bwrite_score) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (id, question_id, listen_score, read_score, Lwrite_score, Bwrite_score))

            # 提交事务
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        # 关闭数据库连接
        connection.close()
