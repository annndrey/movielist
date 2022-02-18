# Actor model
from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship, backref
from .. import db


actor_association_table = Table('actor_movie', db.Base.metadata,
                          Column('actor_id', ForeignKey('actor.id'), primary_key=True),
                          Column('movie_id', ForeignKey('movie.id'), primary_key=True)
)


class Actor(db.Base):
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True)
    name = Column(String(1))
    movies = relationship("Movie", secondary=actor_association_table, backref="cast", lazy='joined')
