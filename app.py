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
from forms import Addmeme,Searchform
import os  
from whoosh.index import create_in
from whoosh.fields import *
from flask_msearch import Search


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

    #     return True

    # def on_data( self, data ):
    #     # print(dms)
    #     print("This is the message received: ", data)



printer = IDPrinter(
  consumer_key, consumer_secret,
  access_token, access_token_secret
)
printer.filter(track=['@rv__williams'],threaded=True)
# mention = printer.filter(track=['@rv__williams'])

# printer.filter(follow=['@rv__williams'])
# print("mention:")
# print(mention)



__searchable__ = '__searchable__'
# DEFAULT_WHOOSH_INDEX_NAME = 'whoosh_index'

#download image route
@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    if 'static/images' in filename:
        uploads =  os.path.join(basedir, 'static/images')
        path = filename
        return send_file(path, as_attachment=True)
    else:
        url= 'http://api.giphy.com/v1/gifs/'+filename+'?api_key=BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et'
        response = urllib.request.urlopen(url)
        mdata = response.read()
        dict = json.loads(mdata)
        image= dict['data']['images']['original']['url']
        uploads =  os.path.join(basedir, 'static/images/')
        # print(image+'imageofgiphy')
        with open(filename +'.gif', 'w') as f:
            f.write(image)
        urllib.request.urlretrieve(image, uploads + filename +'.gif')
        url = image
        response = requests.get(url)
        data = response.content
        return send_file(uploads + filename +'.gif', as_attachment=True)
 



#find the image in the database using tags from search or url
@app.route('/home/<string:tag>')
def findtag(tag):
    searchform = Searchform()

    #check for spaces in the tag from url
    if " " or "%" in tag:
        giphytag = tag.replace(" ","-")
    #from search find tag
    if request.method == 'POST':

        #check for spaces in the tag from search
        tag = request.form['search']
        if " " or "%" in tag:
            giphytag = tag.replace(" ","-")

        # memes = whoosh_search(tag) #search for the tag in the database using whoosh
        memes = Meme.query.filter(Meme.tags.like('%'+tag+'%')).all()
        # memes = Meme.query.msearch(tag,fields=['tags'],limit=20).all() #search for the tag in the database using msearch

        #search for meme using giphy api
        payload = {'s': tag, 'api_key': 'BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et'}
        r = requests.get('http://api.giphy.com/v1/gifs/search?api_key=BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et&q='+giphytag)
        r = r.json()
        # https://api.giphy.com/v1/gifs/search?api_key=BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et&q=man&limit=25&offset=0&rating=g&lang=en
        url= 'http://api.giphy.com/v1/gifs/search?api_key=BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et&q='+giphytag
        response = urllib.request.urlopen(url)
        mdata = response.read()
        dict = json.loads(mdata)
        dictdata = dict['data']
        dictdatalen = len(dict['data'])

        #if giphy api returns results save the title and image url for no reason
        if dictdatalen > 0:
        # print(dict.data.images.original.url)
            for i in range(0, len(dict)):
                title = dict['data'][i]['title']
                url = dict['data'][i]['images']['original']['url']
   
        return render_template('indexnew.html',memes=memes,tags=tag,giphys=r,dict=dict,search='yes',searchform=searchform,dictdata=dictdata,dictdatalen=dictdatalen,page=page,)



    ROWS_PER_PAGE = 10
    page = request.args.get('page', 1, type=int)


    memes = Meme.query.filter(Meme.tags.like('%'+tag+'%')).paginate(page, 4, False)

    #from url find meme
    # memes = Meme.query.filter(Meme.tags.like('%'+tag+'%')).all()
    # mentions = Mention.query.filter_by(tags=tag).all()
    # search for meme with giphy api
    payload = {'s': tag, 'api_key': 'BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et'}
    r = requests.get('http://api.giphy.com/v1/gifs/search?api_key=BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et&q='+giphytag)
    r = r.json()
    # https://api.giphy.com/v1/gifs/search?api_key=BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et&q=man&limit=25&offset=0&rating=g&lang=en
    url= 'http://api.giphy.com/v1/gifs/search?api_key=BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et&q='+giphytag
    response = urllib.request.urlopen(url)
    mdata = response.read()
    dict = json.loads(mdata)
    length = len(dict)
    dictdata = dict['data']
    dictdatalen = len(dict['data'])
    #if giphy api returns results save the title and image url for no reason
    if dictdatalen > 0:
        results="yes"
    # print(dict.data.images.original.url)
        for i in range(0, len(dict)):
            title = dict['data'][i]['title']
            url = dict['data'][i]['images']['original']['url']
    else:
        results="no"

    return render_template('indexnew.html',memes=memes,tags=tag,giphys=r,dict=dict,len=length,search='yes',searchform=searchform,dictdata=dictdata,dictdatalen=dictdatalen,results=results,page=page)





#view meme by id
@app.route('/home/view/<string:id>')
def view(id):
    # memes = Meme.query.filter_by(tags=tag).all()
    meme = Meme.query.filter_by(id=id).first()
    print(meme)
    #using lenth of id to check if id is from giphy api or from database
    if len(id) > 10:
        url = id 
        url= 'http://api.giphy.com/v1/gifs/'+id+'?api_key=BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et'
        response = urllib.request.urlopen(url)
        mdata = response.read()
        dict = json.loads(mdata)
    #if there is a meme found split the tag and add a view to views counter and also search for similar memes
    if meme:
        tags= meme.tags
        tag = tags.split(',')
        meme.views = meme.views + 1
        db.session.commit()
        for t in tag:
            similar = Meme.query.filter(Meme.tags.like('%'+t+'%')).order_by(Meme.views.desc()).all()
        return render_template('viewmeme.html',meme=meme,similar=similar)
    
    return render_template('viewmeme.html',meme=meme,url=url,dict=dict)



#Home route
@app.route('/home')
def home():
    searchform = Searchform()
    # use tweepy mention api to get mentions
    # mentions = api.mentions_timeline( tweet_mode='extended')
    # if len(mentions) == 0:
    #     return
    # else:
    #     #if mention is found look through all mentions and if 'qqq' is found save the tweet id and the tweet text
    #     for mention in mentions:
    #         # print(mention)
    #         mention_check = Mention.query.filter_by(mention_id=mention.id).first()
    #         if mention_check is None and "qqq" in mention.full_text:
    #             tweet= []
    #             new_id = mention.id
    #             text = mention.full_text

    #             ntxt=[]
    #             txt = []
    #             # Process text from mention and save it to db.There is a faster way to do this.
    #             for x in text.split():
    #                 if x.startswith("@"):
    #                     ntxt.append(x)
    #                 elif x.startswith("qqq"):
    #                     ntxt.append(x)
    #                 else:
    #                     txt.append(x)
    #             for tex in txt:
    #                 tags= ''.join(tex)
    #             themention = Mention(mention_id=new_id,full_text=text,tags=tags)
    #             db.session.add(themention)
    #             db.session.commit()
    #             # meme = Meme.query.filter_by(tags=text).first()
    #             memes = Meme.query.filter(Meme.tags.like('%'+tags+'%')).all()
    #             # memes = whoosh_search(tags)
    #             # process reply and use tweepy to send reply
    #             domain = "localhost:5000/home/" + tags 
    #             url = domain + text
    #             # console.log(text)
    #             api.update_status('@' + mention.user.screen_name + " Here's your Search results. Click the link below: " + domain)
    #             return render_template("indexnew.html", memes=memes,title="IMG World",searchform=searchform)
    #     since_id = "1520898332213850118"
    #     count = "10"
    #     # print("Start")
    #     # if direct message is found look through all dms and if 'qqq' is found save the tweet id and the tweet text   
    #     direct_messages = api.get_direct_messages(count=10)
    #     # print(len(direct_messages))
    #     count == 0
    #     for message in direct_messages:
    #         message_check = DirectMessage.query.filter_by(message_id=message.id).first()
    #         if message_check is None and "qqq" in message.message_create['message_data']['text']:
    #         # if message.id > since_id:
    #             dm_id= message.id
    #             text = message.message_create['message_data']['text']
    #             sender_id = message.message_create['sender_id']
    #             # print(message)
    #             # print(message.id)
    #             print(message.message_create['message_data']['text'])
    #             #process full_text to get tags to search for
    #             ntxt=[]
    #             txt = []
    #             # Process tags and save to db. There is a faster way to do this
    #             for x in text.split():
    #                 if x.startswith("qqq"):
    #                     ntxt.append(x)
    #                 else:
    #                     txt.append(x)
    #             for tex in txt:
    #                 tags= ''.join(tex)
    #                 # print(tags)
    #             themessage= DirectMessage(message_id=dm_id,text=tags,sender_id=sender_id)
    #             db.session.add(themessage)
    #             db.session.commit()

                # # pagination
                # ROWS_PER_PAGE = 10
                # page = request.args.get('page', 1, type=int)


                # memes = Meme.query.filter(Meme.tags.like('%'+tags+'%')).paginate(page, 4, False)
    trending = Meme.query.order_by(Meme.views.desc()).all()

                # #process and send reply with tweepy
                # domain = "https://www.localhost:5000/home/" + tags 
                # reply =  " Here's your Search results. Click the link below: " + domain
                # api.send_direct_message(sender_id, reply)
                # return render_template("index.html", memes=memes,title="IMG World",page=page,trending=trending)

    ROWS_PER_PAGE = 5
    page = request.args.get('page', 1, type=int)
    trending = Meme.query.order_by(Meme.views.desc()).paginate(page, ROWS_PER_PAGE, False)

  
    return render_template('index.html',title="IMG World",asearchh='no',trending=trending,searchform=searchform)








#earch gif route. Unused
@app.route('/home/gifs/<string:tags>')  
def search_gif(tags):
    #get a GIF that is similar to text sent
    payload = {'s': tags, 'api_key': 'BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et'}
    r = requests.get('http://api.giphy.com/v1/gifs/search?api_key=BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et&q=man')
    # https://api.giphy.com/v1/gifs/search?api_key=BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et&q=man&limit=25&offset=0&rating=g&lang=en
    r = r.json()
    # print(r)
    # url = r['data']['images']['original']['url']
    # print(url)
    return r





#search route. From search bar
@app.route('/search', methods=['GET', 'POST'])
def search():

    form = Searchform()
    if request.method == 'POST':
        tag = request.form['search']
        #replace spaces with - for giphy search
        if " " or "%" in tag:
            giphytag = tag.replace(" ","-")
        # memes = Meme.query.msearch(tag,fields=['tags'],limit=20).all()
        #search for memes in giphy db 
        memes = Meme.query.filter(Meme.tags.like('%'+tag+'%')).all()
        payload = {'s': tag, 'api_key': 'BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et'}
        r = requests.get('http://api.giphy.com/v1/gifs/search?api_key=BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et&q='+giphytag)
        r = r.json()
        # https://api.giphy.com/v1/gifs/search?api_key=BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et&q=man&limit=25&offset=0&rating=g&lang=en
        url= 'http://api.giphy.com/v1/gifs/search?api_key=BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et&q='+giphytag
        response = urllib.request.urlopen(url)
        mdata = response.read()
        dict = json.loads(mdata)
        length = len(dict)
        dictdata = dict['data']
        dictdatalen = len(dict['data'])
        # if result found savee the title and url for no reason
        if dictdata:
            for i in range(0, dictdatalen):
                title = dict['data'][i]['title']
                url = dict['data'][i]['images']['original']['url']
        else:
            print("empty")
        return redirect(url_for('findtag',tag=tag))




#unused
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        text = request.form['text']


#check if file format is allowed
allowed_extensions = ['png', 'jpg', 'jpeg', 'gif']
def check_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower() in allowed_extensions



@app.route('/addmeme', methods=['GET','POST'])
def addmeme():
    form = Addmeme()
    # form.genre.choices = [(g.id, g.name) for g in Genre.query.filter_by(id='1').all()]
    #process data and save it to db 
    if request.method == 'POST' and 'image_1' in request.files:
        tags = form.tags.data
        type = form.type.data
        image_1 = photos.save(request.files['image_1'], name=secrets.token_hex(10) + ".")
        img= "/static/images/"+image_1
        #check file format
        if check_file_extension(image_1):
            meme = Meme(tags=tags,type=type,image=img)
            db.session.add(meme)
            db.session.commit()
        flash(f'Meme added successfully','success')
        return redirect(url_for('home'))
    return render_template('addmeme.html',title ="Add Meme",form=form)


#livesearch route. To display related memes via ajax when adding a new meme
@app.route("/livesearch",methods=["POST","GET"])
def livesearch():
    form = Addmeme()
    search_word = request.form.get("text")
    related_memes = Meme.query.filter(Meme.tags.like('%'+search_word+'%')).all()
    for m in related_memes:
        rm=[]  
        rm.append(m.image)
    fmemes = related_memes[0].__dict__
    if len(related_memes) > 0:
        found="yes"
    else:
        found="no"
    final_memes = []
    allimg = []
    for rel in related_memes:

        rel.pub_date = rel.pub_date.strftime("%d-%m-%Y")
 
        final_memes.append(rel)
        final_memes = final_memes
        allimg.append(rel.image)
        allimg = allimg[0:6]
        memeimg= rel.image
    return jsonify({'allimg':allimg})

  






if __name__=='__main__':
	app.run(debug=True)

  
# issues 
# 1. findtag when there is no giphy found causes an error