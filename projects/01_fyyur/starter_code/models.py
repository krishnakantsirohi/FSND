import os
from datetime import datetime

from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    db.app = app
    db.init_app(app)
    db.create_all()
    return db


class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    genres = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String)
    website = db.Column(db.String)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    createddatetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    shows = db.relationship('Show', cascade="save-update, merge, delete")

    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.city} {self.state} {self.address} {self.phone} {self.image_link} {self.facebook_link}>'


class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    availability = db.Column(db.String)
    website = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    createddatetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    shows = db.relationship('Show', cascade="save-update, merge, delete")

    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.city} {self.state} {self.phone} {self.genres} {self.image_link} {self.facebook_link}>'


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    starttime = db.Column(db.DateTime, nullable=False)
    endtime = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    createddatetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f'<Show {self.id} {self.name} {self.starttime} {self.endtime} {self.description} {self.venue_id} {self.artist_id}>'
