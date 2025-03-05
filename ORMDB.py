
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Index

# 创建连接
engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/db_ysks?charset=utf8")
conn = engine.connect()
cur = conn.execute('select * from user_msg')
result = cur.fetchall()
print(result)

#生成ORM基类
Base=declarative_base()

class  luntan(Base):
    __tablename__ = 'luntan'  # 表名
    id = Column(Integer,primary_key=True )
    title = Column(String(255))
    body = Column(String(255))
    username = Column(String(255))
    title_id = (Integer)

Base.metadata.create_all(engine)

