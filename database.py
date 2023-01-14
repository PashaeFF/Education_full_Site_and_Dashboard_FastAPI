from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/eduway'


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo = True)

Base = declarative_base()

SessionLocal = scoped_session(sessionmaker(bind = engine))


def get_db():
    db = SessionLocal()
    return db