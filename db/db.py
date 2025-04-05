from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



DB_URL = "sqlite:///app.db"
engine = create_engine(DB_URL, connect_args={'check_same_thread': False})
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from model.user import User
from model.note import Note

Base.metadata.create_all(engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


