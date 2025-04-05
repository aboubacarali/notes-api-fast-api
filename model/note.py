from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from db.db import Base


class Note(Base):
    __tablename__ = 'notes'



    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, index=True)
    content = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    visibility = Column(Enum('private', 'public', 'shared', name='visibility_enum'))
    user_id = Column(Integer, ForeignKey('users.id'))

    # owner = relationship("User", backref="notes")