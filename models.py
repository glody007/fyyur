from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import ARRAY
from datetime import datetime

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    genres = db.Column(MutableList.as_mutable(ARRAY(db.String(60))), default=[])
    phone = db.Column(db.String(120), unique=True)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120), unique=True)
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', cascade="all,delete", backref='venue', lazy=True)  

    def past_shows(self):
      past_shows = Show.query.with_entities(
        Show.artist_id, 
        Show.start_time,
        Artist.name.label('artist_name'),
        Artist.image_link.label('artist_image_link')
      ).join(
        Show.venue
      ).join(
        Show.artist
      ).filter(
        Show.start_time < datetime.now(),
        Show.venue_id == self.id
      ).all()
      return [
        {
          "artist_id": show.artist_id,
          "artist_name": show.artist_name,
          "artist_image_link": show.artist_image_link,
          "start_time": show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        } for show in past_shows
      ]

    def upcoming_shows(self):
      upcoming_shows = Show.query.with_entities(
        Show.artist_id, 
        Show.start_time,
        Artist.name.label('artist_name'),
        Artist.image_link.label('artist_image_link')
      ).join(
        Show.venue
      ).join(
        Show.artist
      ).filter(
        Show.start_time > datetime.now(),
        Show.venue_id == self.id
      ).all()
      return [
        {
          "artist_id": show.artist_id,
          "artist_name": show.artist_name,
          "artist_image_link": show.artist_image_link,
          "start_time": show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        } for show in upcoming_shows
      ]
    
    def past_shows_count(self):
      return db.session.query(
        db.func.count(Show.id)
      ).filter(
        Show.start_time < datetime.now(),
        Show.venue_id == self.id
      ).scalar()

    def upcoming_shows_count(self):
      return db.session.query(
        db.func.count(Show.id)
      ).filter(
        Show.start_time > datetime.now(),
        Show.venue_id == self.id
      ).scalar()

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120), unique=True)
    genres = db.Column(MutableList.as_mutable(ARRAY(db.String(60))), default=[])
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120), unique=True)
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist', lazy=True) 

    def past_shows(self):
      past_shows = Show.query.with_entities(
        Show.venue_id, 
        Show.start_time,
        Venue.name.label('venue_name'),
        Venue.image_link.label('venue_image_link')
      ).join(
        Show.venue
      ).join(
        Show.artist
      ).filter(
        Show.start_time < datetime.now(),
        Show.artist_id == self.id
      ).all()
      return [
        {
          "venue_id": show.venue_id,
          "venue_name": show.venue_name,
          "venue_image_link": show.venue_image_link,
          "start_time": show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        } for show in past_shows
      ]

    def upcoming_shows(self):
      upcoming_shows = Show.query.with_entities(
        Show.venue_id, 
        Show.start_time,
        Venue.name.label('venue_name'),
        Venue.image_link.label('venue_image_link')
      ).join(
        Show.venue
      ).join(
        Show.artist
      ).filter(
        Show.start_time > datetime.now(),
        Show.artist_id == self.id
      ).all()
      return [
        {
          "venue_id": show.venue_id,
          "venue_name": show.venue_name,
          "venue_image_link": show.venue_image_link,
          "start_time": show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        } for show in upcoming_shows
      ]

    def past_shows_count(self):
      return db.session.query(
        db.func.count(Show.id)
      ).filter(
        Show.start_time < datetime.now(),
        Show.artist_id == self.id
      ).scalar()

    def upcoming_shows_count(self):
      return db.session.query(
        db.func.count(Show.id)
      ).filter(
        Show.start_time > datetime.now(),
        Show.artist_id == self.id
      ).scalar()

class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  start_time = db.Column(db.DateTime(), nullable=False)
