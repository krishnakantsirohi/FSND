from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os

SECRET_KEY = os.urandom(32)
database_path = 'postgres://irtvazxzctigea:9e2ba1473974c795047613cc31c9ef2f16f09f31b3704359b44e167bdc3ea93c@ec2-18-210-214-86.compute-1.amazonaws.com:5432/d81lojlrjp5o00'#os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movies(db.Model):
    __tablename__ = 'Movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    image_link = db.Column(db.String)
    createddatetime = db.Column(db.Date, nullable=False, default=datetime.utcnow())

    def __init__(self, title, release_date, image_link=None):
        self.title = title
        self.release_date = release_date
        self.image_link = image_link

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
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'image_link': self.image_link
        }

    def __repr__(self):
        return f'<Venue {self.id} {self.title} {self.release_date} {self.image_link} {self.createddatetime}>'


class Actors(db.Model):
    __tablename__ = 'Actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    image_link = db.Column(db.String)
    createddatetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, name, age, gender, image_link=None):
        self.name = name
        self.age = age
        self.gender = gender
        self.image_link = image_link

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
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'image_link': self.image_link
        }

    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.age} {self.gender} {self.image_link} {self.createddatetime}>'
