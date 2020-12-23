import os
from sqlalchemy import Column, String, Integer, create_engine, Table
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
'''
database_name = "castingagencymodels"
database_path =  "postgres://{}:{}@{}/{}".format('postgres', '1234','localhost:5432', database_name)
'''
database_path = os.environ['DATABASE_URL_TEST'] if os.environ['ENV'] == 'test' else os.environ['DATABASE_URL']

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


# association tabe bidirectional Many-to-Many relationship
association_table = Table('movie_actor', db.metadata,
    Column('movies', Integer, db.ForeignKey('movies.id')),
    Column('actors', Integer, db.ForeignKey('actors.id')))

# Movies with attributes title and release date
class Movie(db.Model):
    __tablename__="movies"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(db.Date)

    actors = db.relationship("Actor",
    secondary=association_table,
    back_populates="movies")


    def __init__(self, title, release_date):
      self.title = title
      self.release_date = release_date

    def insert(self):
      db.session.add(self)
      db.session.commit()

    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def format(self):
        return {
        'title':self.title,
        'release date': self.release_date.strftime("%d-%m-%Y")
        }


# Actors with attributes name, age and gender
class Actor(db.Model):
    __tablename__="actors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    movies = db.relationship(
        "Movie",
        secondary=association_table,
        back_populates="actors")


    def __init__(self, name, age, gender):
      self.name = name
      self.age = age
      self.gender = gender

    def insert(self):
      db.session.add(self)
      db.session.commit()

    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def format(self):
        return {
        'name':self.name,
        'age': self.age,
        'gender': self.gender
        }
