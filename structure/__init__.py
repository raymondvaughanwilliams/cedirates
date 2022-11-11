from flask import Flask, render_template, request
import tweepy
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_migrate import Migrate
import requests
import logging
import os
from flask_msearch import Search
import sys
import whoosh.index
from whoosh.fields import Schema
from tweepy import Stream
# from tweepy.streaming import StreamListener
from flask import Flask, render_template, request,redirect,url_for,flash,jsonify
from os import environ
from dotenv import load_dotenv

load_dotenv()



app = Flask(__name__)







basedir = os.path.abspath(os.path.dirname(__file__))


# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://rpkdyhnqthcxnl:443aba18f66736602f2919c0f6cbfb3adcf28523fd96e384c7b022d961ec75c9@ec2-176-34-211-0.eu-west-1.compute.amazonaws.com/d2ofmk5as6mscp"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')

app.config['SECRET_KEY']='hfouewhfoiwefoquw'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SESSION_TYPE'] = 'sqlalchemy'
# app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'



app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
app.config['UPLOADED_PHOTOS_ALLOW'] = set(['png', 'jpg', 'jpeg','mp4'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)





# db = SQLAlchemy(app)
# migrate = Migrate(app, db,render_as_batch=True)


logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)



# print(os.environ)
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = environ.get('consumer_secret')
access_token = environ.get('access_token')
access_token_secret = environ.get('access_token_secret')




auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)

