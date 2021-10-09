from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Float
from sqlalchemy.sql.sqltypes import DATE, STRINGTYPE, TEXT, DateTime
from sqlalchemy import Column, String, Integer

db = SQLAlchemy()

class users(db.Model):
	__tablename__ = 'users'
	id = db.Column(Integer, primary_key=True)
	username = db.Column(TEXT, unique=True)# emailカラム→usernameカラム
	hash = db.Column(TEXT, unique=False)
	nickname = db.Column(TEXT, unique=False)# nameカラム→nicknameカラム

	def __init__(self, username=None, hash=None, nickname=None):
		self.username = username
		self.hash = hash
		self.nickname = nickname

class song_locations(db.Model):
  __tablename__ = 'song_locations'
  id = db.Column(Integer, primary_key=True)
  user_id = db.Column(Integer, unique=False)
  track_id = db.Column(TEXT, unique=False)
  longitude = db.Column(Float, unique=False)
  latitude = db.Column(Float, unique=False)
  date = db.Column(DATE, unique=False)
  emotion = db.Column(TEXT, unique=False)
  comment = db.Column(TEXT, unique=False)

  def __init__(self, user_id=None, track_id=None, longitude=None, latitude=None, date=None, emotion = None, comment = None):
    self.user_id = user_id
    self.track_id = track_id
    self.longitude = longitude
    self.latitude = latitude
    self.date = date
    self.emotion = emotion
    self.comment = comment

class songs(db.Model):
  __tablename__ = 'songs'
  id = db.Column(Integer, primary_key=True)
  track_id = db.Column(TEXT, unique=True)
  track_name = db.Column(TEXT, unique=False)
  artist_name = db.Column(TEXT, unique=False)
  track_image = db.Column(TEXT, unique=False)
  spotify_url = db.Column(TEXT, unique=True)

  def __init__(self, track_id=None, track_name=None, artist_name=None, track_image=None, spotify_url=None):
    self.track_id = track_id
    self.track_name = track_name
    self.artist_name = artist_name
    self.track_image = track_image
    self.spotify_url = spotify_url

class follow(db.Model):
  __tablename__ = 'follow'
  id = db.Column(Integer, primary_key=True)
  follow_user_id = db.Column(Integer)
  followed_user_id = db.Column(Integer)

  def __init__(self, follow_user_id=None, followed_user_id = None):
    self.follow_user_id = follow_user_id
    self.followed_user_id = followed_user_id