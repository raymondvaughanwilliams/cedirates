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
from whoosh.qparser import OrGroup
from whoosh.qparser import AndGroup
from whoosh.qparser import MultifieldParser
from whoosh.analysis import StemmingAnalyzer
import whoosh.index
from whoosh.fields import Schema
from tweepy import Stream
# from tweepy.streaming import StreamListener
from flask import Flask, render_template, request,redirect,url_for,flash,jsonify

app = Flask(__name__)







basedir = os.path.abspath(os.path.dirname(__file__))


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://rpkdyhnqthcxnl:443aba18f66736602f2919c0f6cbfb3adcf28523fd96e384c7b022d961ec75c9@ec2-176-34-211-0.eu-west-1.compute.amazonaws.com/d2ofmk5as6mscp"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')

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




consumer_key = os.environ.get('twitter_consumer_key')
consumer_secret = os.environ.get('twitter_consumer_secret')
access_token = os.environ.get('twitter_access_token')
access_token_secret = os.environ.get('twitter_access_token_secret')






auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)

# stream = tweepy.Stream(
#    consumer_key, consumer_secret,
#   access_token, access_token_secret
# )

# class IDPrinter(tweepy.Stream):

#     def on_status(self, status):
#         # mentions =stream.filter(track=['python'])
#         print(status.text)
#         text = status.text
#         new_id = status.id
#         screen_name = status.user.screen_name
#         ntxt=[]
#         txt = []
#         for x in text.split():
#             if x.startswith("@"):
#                 ntxt.append(x)
#             elif x.startswith("qqq"):
#                 ntxt.append(x)
#             else:
#                 txt.append(x)
#         for tex in txt:
#             tags= ''.join(tex)
#         themention = Mention(mention_id=new_id,full_text=text,tags=tags)
#         db.session.add(themention)
#         db.session.commit()
#         domain = "localhost:5000/home/" + tags 
#         url = domain + text
#         api.update_status('@' + status.user.screen_name + " Here's your Search results. Click the link below: " + domain)



#         # for s in status.text:
#         #     if "rv__williams" in status.text:
#         #         # print(status.user)

#         #         # print(status.text)
#         #         # print(len(status))
#         #     # print(status)
#         #         print("next")
#         #         print(status.text)


# printer = IDPrinter(
#   consumer_key, consumer_secret,
#   access_token, access_token_secret
# )
# printer.filter(track=['@rv__williams'])
# mention = printer.filter(track=['@rv__williams'])
# print("mention:")
# print(mention)
# printer.sample(threaded=True)
# mentionstream = Stream(auth, IDPrinter())
# the = mentionstream.filter(track=['a'])
# print(the)
# stream = tweepy.Stream(auth, IDPrinter())
# mentions = tweepy.stream.filter(track=['@rv__williams'])
# print(mentions)
# class Listener(tweepy.Stream):
#     def __init__(self, output_file=sys.stdout):
#         super(Listener,self).__init__()
#         self.output_file = output_file
#     def on_status(self, status):
#         print(status.text, file=self.output_file)
#     def on_error(self, status_code):
#         print(status_code)
#         return False

# output = open('stream_output.txt', 'w')
# listener = Listener(output_file=output)

# stream = tweepy.Stream(auth=api.auth, listener=listener)
# try:
#     print('Start streaming.')
#     stream.sample(languages=['en'])
# except KeyboardInterrupt:
#     print("Stopped.")
# finally:
#     print('Done.')
#     stream.disconnect()
#     output.close()



# class MyListener(tweepy.Stream):
#     def on_data(self, data):
#         try:
#             with open('python.json', 'a') as f:
#                 f.write(data)
#                 return True
#         except BaseException as e:
#             print("Error on_data: %s" % str(e))
#         return True
 
#     def on_error(self, status):
#         print(status)
#         return True
 
# twitter_stream = Listener(
#   consumer_key, consumer_secret,
#   access_token, access_token_secret
# )

# twitter_stream.filter(track=['#python'])

