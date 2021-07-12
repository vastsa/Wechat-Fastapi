from sqlalchemy import Column, String

from .database import Base, engine


# 创建数据库模型
class Users(Base):
    __tablename__ = 'Users'
    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    nickname = Column(String(255))
    createTime = Column(String(255))
    updateTime = Column(String(255))
    province = Column(String(255))
    county = Column(String(255))
    city = Column(String(255))
    avatar = Column(String(255))
    loginIp = Column(String(255))


Base.metadata.create_all(engine)
