from helloflask.init_db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, ForeignKey, PrimaryKeyConstraint, func

class Talk(Base):
    __tablename__ = 'Talk'

    talk_id = Column(Integer, primary_key = True)
    title = Column(String)
    event = Column(String)
    talk_year = Column(Integer)
    tags = Column(String)
    isKorean = Column(Integer)
    diff = Column(Integer)

    def __init__(self, talk_id, title, event, talk_year, tags, isKorean, diff):
        self.talk_id = talk_id
        self.title = title
        self.event = event
        self.talk_year = talk_year
        self.tags = tags
        self.isKorean = isKorean
        self.diff = diff
    
    def __repr__(self):
        return '%s, %s, %s, %s, %s, %s, %s' %(self.talk_id, self.title, self.event, self.talk_year, self.tags, self.isKorean, self.diff)
    
    def json (self) :
        j = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return j


class User(Base):
    # Table created at Mysql5(workbench)
    __tablename__='User'

    id = Column(Integer, primary_key = True)
    passwd = Column(String)
    email = Column(String)
    username = Column(String)
    
    #None = null;
    def __init__(self, passwd, email, username, makesha=False):
        
        if makesha:
            self.passwd = passwd
        else:
            self.passwd = func.sha2(passwd, 256)

        self.email = email
        self.username = username

    #tostring
    def __repr__(self):
        return '%s, %s, %s' %(self.passwd,self.email, self.username)




