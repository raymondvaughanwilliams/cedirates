from unittest import removeResult
from wsgiref.handlers import read_environ
from flask import Flask, render_template, request,redirect,url_for,flash,jsonify
from structure import db,app,api,logger,photos,basedir,consumer_key,consumer_secret,access_token, access_token_secret
from flask import send_from_directory,send_file
import tweepy
import secrets
import requests
import datetime
import urllib.request, json
import logging
from models import Meme,Mention,DirectMessage
import os  
from whoosh.index import create_in
from whoosh.fields import *
from flask_msearch import Search
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

# stream from tweepy 


stream = tweepy.Stream(
   consumer_key, consumer_secret,
  access_token, access_token_secret
)

class IDPrinter(tweepy.Stream):

    def on_status(self, status):
        # mentions =stream.filter(track=['python'])
        statustext = status.text
        new_id = status.id
        screen_name = status.user.screen_name
        if " " in statustext:
            text = statustext.replace(" ","-")
                    
        ntxt=[]
        txt = []
        for x in text.split("-"):
            if x.startswith("@"):
                ntxt.append(x)
            else:
                txt.append(x)
        tags = '-'.join(txt)
        themention = Mention(mention_id=new_id,full_text=statustext,tags=tags)
        db.session.add(themention)
        db.session.commit()
        domain = "https://imgworld.herokuapp.com/home/" + tags 
        url = domain + text
        api.update_status('@' + screen_name + " Here's your Search results. Click the link below: " + domain)
        return True


    def on_direct_message( self, direct_message ):    
            
        print(direct_message)

        author = direct_message.author.screen_name
        print(direct_message.text)
        api.send_direct_message(screen_name=author, text='response') ['message_data']['text']

        return True

    def on_data( self, data ):
        # print(dms)
        print("This is the message received: ", data)


printer = IDPrinter(
  consumer_key, consumer_secret,
  access_token, access_token_secret
)
printer.filter(track=['@imgworldbot'],threaded=True)

__searchable__ = '__searchable__'
# DEFAULT_WHOOSH_INDEX_NAME = 'whoosh_index'



@app.route('/cedirates')
def cedirates():
    date = datetime.datetime.now()
    daysoftheweek = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    day = datetime.datetime.today().weekday()
    day = daysoftheweek[day]
    print("day")
    print(day)
    datestr = day + " "+date.strftime("%b %m %Y, %I:%M %p")
    print(datestr)
    url = "https://api.apilayer.com/fixer/convert?to=GHS&from=USD&amount=1"
    urlgbp = "https://api.apilayer.com/fixer/convert?to=GHS&from=GBP&amount=1"
    urleur = "https://api.apilayer.com/fixer/convert?to=GHS&from=EUR&amount=1"
    urlbtc = "https://api.apilayer.com/fixer/convert?to=GHS&from=BTC&amount=1"
    payload = {}
    headers= {
    "apikey": "Fxsdl1cJnRdNiTxjMLCnnHJQfEdJgB1x"
    }
    # usd rate 
    response = requests.request("GET", url, headers=headers, data = payload)
    print("response:")
    print(response.text)
    data = response.text
    parse =json.loads(data)
    rate = parse["info"]["rate"]
    rate = round(rate,2)
 
    
    responseeur = requests.request("GET", urleur, headers=headers, data = payload)
    print("response:")
    print(responseeur.text)
    dataeur = responseeur.text
    parseeur =json.loads(dataeur)
    rateeur = parseeur["info"]["rate"]
    rateeur = round(rateeur,2)
    
    
    responsegpb = requests.request("GET", urlgbp, headers=headers, data = payload)
    print("response:")
    print(responsegpb.text)
    datagbp = responsegpb.text
    parsegbp =json.loads(datagbp)
    rategbp = parsegbp["info"]["rate"]
    rategbp = round(rategbp,2)
    
    
    responsebtc = requests.request("GET", urlbtc, headers=headers, data = payload)
    print("response:")
    print(responsebtc.text)
    databtc = responsebtc.text
    parsebtc =json.loads(databtc)
    ratebtc = parsebtc["info"]["rate"]
    ratebtc = round(ratebtc,2)
    
    
    image_path =  os.path.join(basedir, 'static/cedirates.gif')
    thetweet = datestr + "\n 💵 1 USD ➔ ₵ " + str(rate) + "\n 💶 1 EUR ➔ ₵ " + str(rateeur) + "\n 💷 1 GBP ➔ ₵ "+ str(rategbp) + "\n₿   1 BTC ➔ ₵ "+str(ratebtc)
    print(thetweet)
    print(image_path)
    # api.update_status(status=thetweet)
    media = api.media_upload(image_path)
    api.update_status(status=thetweet, media_ids=[media.media_id])

    return "something"


# scheduler = BackgroundScheduler()
# scheduler.add_job(func=cedirates,trigger="interval",seconds=86400)
# scheduler.start()
# atexit.register(lambda: scheduler.shutdown())


  






if __name__=='__main__':
	app.run(debug=True)

  
# issues 
# 1. findtag when there is no giphy found causes an error