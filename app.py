from unittest import removeResult
from wsgiref.handlers import read_environ
from flask import Flask, render_template, request,redirect,url_for,flash,jsonify
from structure import app,api,logger,photos,basedir,consumer_key,consumer_secret,access_token, access_token_secret
from flask import send_from_directory,send_file
import tweepy
import secrets
import requests
import datetime
import urllib.request, json
import time
# import logging
# from models import Meme,Mention,DirectMessage
import os  
# from whoosh.index import create_in
# from whoosh.fields import *
# from flask_msearch import Search
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

# stream from tweepy 


# stream = tweepy.Stream(
#    consumer_key, consumer_secret,
#   access_token, access_token_secret
# )

# class BOGReplies(tweepy.Stream):

#     def on_status(self, status):
#         statustext = status.text
#         handle = status.user.screen_name 
#         # print("response")
#         # print(status)
#         print("response")
#         print(handle)
#         new_id = status.id
#         if handle == "nosize71":
#             print("working")
#             tweet = cedirates()
#             api.update_status(status = tweet, in_reply_to_status_id = new_id , auto_populate_reply_metadata=True)
            
#     def on_limit(self,status):
#             print ("Rate Limit Exceeded, Sleep for 15 Mins")
#             time.sleep(10 * 60)
#             return True
    
    
#     def on_request_error(self, status):
#         print(status)
        
#     def on_disconnect(self,status):
#         print("Disconnected . Restarting stream")
#         print(status)
#         bogreplies.filter(track=['Bank of Ghana Exchange Rates'],threaded=True)
#         print("restarted")
        
        
#     def on_connection_error(self, status):
#         print("stream connection on_conn error")
#         bogreplies.filter(track=['Bank of Ghana Exchange Rates'],threaded=True)
#         print("restarted")
        
# bogreplies = BOGReplies(
#   consumer_key, consumer_secret,
#   access_token, access_token_secret
# )
# # bogreplies.filter(track=['Bank of Ghana Exchange Rates'],threaded=True)
# bogreplies.filter(track=['Bank of Ghana Exchange Rates'],threaded=True)





@app.route('/cedirates')
def cedirates():
    date = datetime.datetime.now()
    daysoftheweek = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    day = datetime.datetime.today().weekday()
    day = daysoftheweek[day]
    datestr = day + " "+date.strftime("%b %m %Y, %I:%M %p")
    url = "https://api.apilayer.com/exchangerates_data/convert?to=GHS&from=USD&amount=1"
    urlgbp = "https://api.apilayer.com/exchangerates_data/convert?to=GHS&from=GBP&amount=1"
    urleur = "https://api.apilayer.com/exchangerates_data/convert?to=GHS&from=EUR&amount=1"
    urlbtc = "https://api.apilayer.com/exchangerates_data/convert?to=GHS&from=BTC&amount=1"
    payload = {}
    headers= {
    "apikey": "mEt34QnraazOZ10YzUmUnWxsYqwNLnvb"
    }
    # usd rate 
    response = requests.request("GET", url, headers=headers, data = payload)
    # print("response:")
    # print(response.text)
    data = response.text
    parse =json.loads(data)
    rate = parse["info"]["rate"]
    rate = round(rate,2)
 
    
    responseeur = requests.request("GET", urleur, headers=headers, data = payload)
    # print("response:")
    # print(responseeur.text)
    dataeur = responseeur.text
    parseeur =json.loads(dataeur)
    rateeur = parseeur["info"]["rate"]
    rateeur = round(rateeur,2)
    
    
    responsegpb = requests.request("GET", urlgbp, headers=headers, data = payload)
    # print("response:")
    # print(responsegpb.text)
    datagbp = responsegpb.text
    parsegbp =json.loads(datagbp)
    rategbp = parsegbp["info"]["rate"]
    rategbp = round(rategbp,2)
    
    
    responsebtc = requests.request("GET", urlbtc, headers=headers, data = payload)
    # print("response:")
    # print(responsebtc.text)
    databtc = responsebtc.text
    parsebtc =json.loads(databtc)
    ratebtc = parsebtc["info"]["rate"]
    ratebtc = round(ratebtc)
    
    
    # image_path =  os.path.join(basedir, 'static/cedirates.gif')
    thetweet = datestr + "\n 💵 1 USD ➔ ₵ " + str(rate) + "\n 💶 1 EUR ➔ ₵ " + str(rateeur) + "\n 💷 1 GBP ➔ ₵ "+ str(rategbp) + "\n₿   1 BTC ➔ ₵ "+str(ratebtc)
    # print(thetweet)
    # print(image_path)
    # api.update_status(status=thetweet)
    # media = api.media_upload(image_path)
    print("Successful tweet")
    return thetweet



@app.route('/sendtweet')
def sendtweet():
    thetweet = cedirates()
    image_path =  os.path.join(basedir, 'static/cedirates.gif')
    media = api.media_upload(image_path)
    api.update_status(status=thetweet, media_ids=[media.media_id])
    return thetweet


    


scheduler = BackgroundScheduler()
scheduler.add_job(func=sendtweet,trigger="interval",seconds=1000)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())








if __name__=='__main__':
	app.run(debug=True)

  
# issues 
# 1. findtag when there is no giphy found causes an error