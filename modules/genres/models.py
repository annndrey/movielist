# Genre model

from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship, backref
from .. import db



class Genre(db.Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(1))
    
    
