#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#



import json
from stringprep import in_table_a1
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from pytz import timezone, utc
from datetime import datetime, tzinfo
from sqlalchemy import JSON, DateTime, false, or_
from sqlalchemy.sql import func
from forms import *
from flask_migrate import Migrate
from collections import OrderedDict
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database

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
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(255))
    seeking_talent =db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'
    print
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean,default=False)
    seeking_description = db.Column(db.String(500))

class Shows(db.Model):
  __tablename__='Shows'

  id = db.Column(db.Integer,primary_key=True)
  artist_id =  db.Column(db.Integer,db.ForeignKey('Artist.id'), nullable=True)
  venue_id =  db.Column(db.Integer,db.ForeignKey('Venue.id'), nullable=True)
  start_time = db.Column(db.DateTime(True),default=datetime.now())


class Venue_search(db.Model):
  __tablename__ = 'Venue_search'

  id  = db.Column(db.Integer, primary_key=True)
  word = db.Column(db.String(255),nullable=False)
  count = db.Column(db.Integer,nullable=False)
  venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'), nullable=False)

class Artist_search(db.Model):
  __tablename__ = 'Artist_search'

  id  = db.Column(db.Integer, primary_key=True)
  word = db.Column(db.String(255),nullable=False)
  count = db.Column(db.Integer,nullable=False)
  artist_id = db.Column(db.Integer,db.ForeignKey('Artist.id'), nullable=False)

