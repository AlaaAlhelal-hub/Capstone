import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from datetime import datetime


database_path = None

if os.environ.get('ENV') == 'test':
    database_path = os.environ.get('DATABASE_URL_TEST')
else:
    database_path = os.environ.get('DATABASE_URL')

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    # migrate = Migrate(app, db)


# Movies with attributes title and release date
class Movie(db.Model):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(db.Date)

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

    @property
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release date': self.release_date.strftime("%d-%m-%Y")
        }


# Actors with attributes name, age and gender
class Actor(db.Model):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

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

    @property
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
