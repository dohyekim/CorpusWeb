from helloflask.init_db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, ForeignKey, PrimaryKeyConstraint, func
from sqlalchemy.orm import relationship, backref

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
    
    def json (self) :
        j = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return j


# create table Memo(
# 	id int unsigned auto_increment primary key,
#     user_id int unsigned not null,
#     title varchar(256) not null unique key,
#     memo text not null
# );
class Memo(Base):
    __tablename__='Memo'

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('User.id'))
    name = Column(String)
    content = Column(String)
    user = relationship('User')

    def __init__(self, user_id, name, content):
        self.user_id = user_id
        self.name = name
        self.content = content

    #tostring
    def __repr__(self):
        return '%s, %s, %s, %s' %(self.user_id, self.content, self.user, self.name)
    
    def json (self) :
        j = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return j

class Checklist(Base):
    # Table created at Mysql5(workbench)
    __tablename__='Checklist'

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('User.id'))
    name = Column(String)
    content = Column(String)
    user = relationship('User')

    def __init__(self, user_id, name, content):
        self.user_id = user_id
        self.name = name
        self.content = content

    #tostring
    def __repr__(self):
        return '%s, %s, %s, %s' %(self.user,self.user_id, self.name, self.content)
    
    def json (self) :
        j = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return j

class Post(Base):

    __tablename__='Post'

    postid = Column(Integer, primary_key = True)
    title = Column(String(256))
    date_posted = Column(TIMESTAMP)
    content = Column(String(1024))
    user_id = Column(Integer, ForeignKey('User.id'))
    user = relationship('User')

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return 'Post %r, %r, %r, %r' %(self.postid, self.title, self.content, self.user_id)
    
    def json (self) :
        j = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return j