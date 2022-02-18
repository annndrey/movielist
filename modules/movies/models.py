# Movie model
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, backref
from .. import db

genre_association_table = Table('genre_movie', db.Base.metadata,
                          Column('genre_id', ForeignKey('genre.id'), primary_key=True),
                          Column('movie_id', ForeignKey('movie.id'), primary_key=True)
)


class Movie(db.Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String(1))
    year = Column(Integer)
    genres = relationship("Genre", secondary=genre_association_table, backref="movies", lazy='joined')
