from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.db import Base

class User(Base):
    __tablename__ = 'users'


    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True)
    password = Column(String)

    # notes = relationship("Note", backref="owner")
