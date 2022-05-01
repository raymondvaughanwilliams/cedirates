from flask import Flask, render_template, request
import tweepy
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_migrate import Migrate
import requests
import logging
import os



app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')

app.config['SECRET_KEY']='hfouewhfoiwefoquw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SESSION_TYPE'] = 'sqlalchemy'
# app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'



app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)






db = SQLAlchemy(app)
migrate = Migrate(app, db,render_as_batch=True)

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)

consumer_key = "TLhUlcuYQ9UzwvFyfEzcwoRGY"
consumer_secret= "zSRMSeeAWvmF3A9iYfJNuel7iovnqBhAT20a9BZQeTTF8FbJHJ"
# bearer_token =AAAAAAAAAAAAAAAAAAAAAJWMbgEAAAAAgyY0aynqDdjHll1ps1UaZHQPLaI%3D3acLywE5rmQggaiCGzXvNvAE8WMty56ZgRq6jhvr4EuM4kGx1U
access_token = "944709207038754816-4pxm3AJYW5pSinuHDtarzoflLxm6hp1"
access_token_secret ="l1JdNagmeif7fDKKyVJNbmmwTqF2fRVY4QZIz28hZh4Mq"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

