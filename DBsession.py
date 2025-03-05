from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ORMDB import luntan

# 通常我们把数据库表模型统一放到一个模块里，所以这里需要导入

# 准备工作
engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/db_ysks?charset=utf8mb4")

Session = sessionmaker(engine)
DBsession= Session()#创建一个引擎工作

# 查询 query(表结构的类名)
res = DBsession.query(luntan)
print(res)  # 直接翻译输出对应的SQL查询语句

res = DBsession.query(luntan).all()  # 返回表中所有数据对象
print(res)