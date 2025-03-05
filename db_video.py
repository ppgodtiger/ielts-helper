import pymysql
from pymysql.cursors import DictCursor

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'database': 'db_ysks',
    'charset': 'utf8',
    'port': 3306

}


def get_video_list():
    # 连接数据库
    connection = pymysql.connect(**db_config,cursorclass=DictCursor)
    try:
        # 创建游标对象
        with connection.cursor() as cursor:
            # 执行SQL查询
            cursor.execute("SELECT video_path FROM video")
            # 获取所有记录
            result = cursor.fetchall()
            # 提取视频路径列表
            video_list = [row['video_path'] for row in result]
            return video_list
    finally:
        # 关闭数据库连接
        connection.close()