from sqlalchemy import create_engine, Table, Column
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#"mysql+pymysql://dooo:1234@127.0.0.1:3307/corpusdb?charset=utf8"

# Declare connection
mysql_url = "mysql+pymysql://dooo:1234@127.0.0.1/corpusdb?charset=utf8"
engine = create_engine(mysql_url, echo=True, convert_unicode=True)

# Declare & create Session
db_session = scoped_session( sessionmaker(autocommit=False, autoflush=False, bind=engine) )

# Create SqlAlchemy Base Instance
Base = declarative_base()
Base.query = db_session.query_property()

def init_database():
    Base.metadata.create_all(bind=engine)


    