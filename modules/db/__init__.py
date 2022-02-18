from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

some_engine = create_engine('sqlite:///modules/db/database.db')
Session = sessionmaker(bind=some_engine)
session = Session()

Base = declarative_base()
