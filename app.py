from unittest import removeResult
from flask import Flask, render_template, request,redirect,url_for,flash 
from structure import db,app,api,logger,photos
import tweepy
import secrets
import requests
import urllib.request, json
import logging
from models import Meme,Mention,DirectMessage
from forms import Addmeme



# api key = RLYya4IiZvpFkLfn5pItSqPhW
# api secret= UaAjhhNYTmSB6FwCqEc5RDTkSB0dT2Y81jxCUFaqVGKht156Xd
# bearer_token = AAAAAAAAAAAAAAAAAAAAAOqEbgEAAAAABLp1X6nGWW2nXjYjgBjQ5VYCqSQ%3DpVZpzJVo4Bvy8GNQYeJA0fHcFEfkOlWSQUntNCncRmRC1BgF92
# access_token = 944709207038754816-pOXaIltIHr7rrORJiEOdcehpi6xUmZV
# access_token_secret = MhECXNlbr4F4ZfxMHz4iXgbpmhMcFWWMeEQYcsFxR1PwM

@app.route('/home/<string:tag>')
def findtag(tag):
    # memes = Meme.query.filter_by(tags=tag).all()
    memes = Meme.query.filter(Meme.tags.like('%'+tag+'%')).all()
    mentions = Mention.query.filter_by(tags=tag).all()
    # print (tag)
    # print (memes)
    payload = {'s': tag, 'api_key': 'BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et'}
    r = requests.get('http://api.giphy.com/v1/gifs/search?api_key=BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et&q='+tag)
    r = r.json()
    # https://api.giphy.com/v1/gifs/search?api_key=BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et&q=man&limit=25&offset=0&rating=g&lang=en
    url= 'http://api.giphy.com/v1/gifs/search?api_key=BeeDE4AMUc1K32Ii6Bi8TM2yc3aMy7Et&q='+tag
    response = urllib.request.urlopen(url)
    mdata = response.read()
    dict = json.loads(mdata)
    length = len(dict)
    print (length)
    print('start')
    # print(dict.data.images.original.url)
    for i in range(0, len(dict)):

        title = dict['data'][i]['title']
        url = dict['data'][i]['images']['original']['url']
        print (title)
        print (url)
        print('start')
        # print(r)
    return render_template('indexnew.html',memes=memes,mentions=mentions,tags=tag,giphys=r,dict=dict,len=length)


@app.route('/home/view/<string:id>')
def view(id):
    # memes = Meme.query.filter_by(tags=tag).all()
    meme = Meme.query.filter_by(id=id).first()
    tags= meme.tags
    similar = Meme.query.filter(Meme.tags.like('%'+tags+'%')).all()
    return render_template('viewmeme.html',meme=meme,similar=similar)

@app.route('/home')
def home():
    # last_id = get_last_tweet(file)
    last_id = "1"
    mentions = api.mentions_timeline( tweet_mode='extended')
    if len(mentions) == 0:
        return
    else:
        for mention in mentions:
            # print(mention)
            mention_check = Mention.query.filter_by(mention_id=mention.id).first()
            if mention_check is None and "qqq" in mention.full_text:
                tweet= []
                new_id = mention.id
                text = mention.full_text
                # meme = Meme(description=text,mention_id=new_id)
                # db.session.add(meme)
                # db.session.commit()
                # mention = Mention(mention_id=new_id,full_text=text)
                #process full_text to get tags to search for
                ntxt=[]
                txt = []
                # There is a faster way to do this
                for x in text.split():
                    if x.startswith("@"):
                        ntxt.append(x)
                    elif x.startswith("qqq"):
                        ntxt.append(x)
                    else:
                        txt.append(x)
                for tex in txt:
                    tags= ''.join(tex)
                    # print(tags)
                themention = Mention(mention_id=new_id,full_text=text,tags=tags)
                db.session.add(themention)
                db.session.commit()

                # meme = Meme.query.filter_by(tags=text).first()
                memes = Meme.query.filter(Meme.tags.like('%'+tags+'%')).all()
                domain = "localhost:5000/home/" + tags 
                url = domain + text
                # console.log(text)
                api.update_status('@' + mention.user.screen_name + " Here's your Search results. Click the link below: " + domain)
                return render_template("indexnew.html", memes=memes,title="IMG World")
        since_id = "1520898332213850118"
        count = "10"
        # print("Start")
        direct_messages = api.get_direct_messages(count=10)
        # print(len(direct_messages))
        count == 0
        for message in direct_messages:
            message_check = DirectMessage.query.filter_by(message_id=message.id).first()
            if message_check is None and "qqq" in message.message_create['message_data']['text']:
            # if message.id > since_id:
                dm_id= message.id
                text = message.message_create['message_data']['text']
                sender_id = message.message_create['sender_id']
                # print(message)
                # print(message.id)
                print(message.message_create['message_data']['text'])
                #process full_text to get tags to search for
                ntxt=[]
                txt = []
                # There is a faster way to do this
                for x in text.split():
                    if x.startswith("qqq"):
                        ntxt.append(x)
                    else:
                        txt.append(x)
                for tex in txt:
                    tags= ''.join(tex)
                    # print(tags)
                themessage= DirectMessage(message_id=dm_id,text=tags,sender_id=sender_id)
                print(themessage)
                print(message)
                db.session.add(themessage)
                db.session.commit()

                memes = Meme.query.filter(Meme.tags.like('%'+tags+'%')).all()
                domain = "https://www.localhost:5000/home/" + tags 
                reply =  " Here's your Search results. Click the link below: " + domain
                api.send_direct_message(sender_id, reply)
                return render_template("indexnew.html", memes=memes,title="IMG World")



    return render_template('indexnew.html',title="IMG World")

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

@app.route('/search')
def search():
    tags = request.args.get('tags')




@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        text = request.form['text']



@app.route('/addmeme', methods=['GET','POST'])
def addmeme():
    form = Addmeme()
    # form.genre.choices = [(g.id, g.name) for g in Genre.query.filter_by(id='1').all()]
    if request.method == 'POST' and 'image_1' in request.files:
        tags = form.tags.data
        type = form.type.data
        image_1 = photos.save(request.files['image_1'], name=secrets.token_hex(10) + ".")
        img= "/static/images/"+image_1
        meme = Meme(tags=tags,type=type,image=img)
        db.session.add(meme)
        db.session.commit()
        flash(f'Ticket added successfully','success')
        return redirect(url_for('home'))
    return render_template('addmeme.html',title ="Add Meme",form=form)



# @app.route('/', methods=['GET'])
# @app.route('/search', methods=['GET'])
# def index():
#     form = SearchForm(request.args)
#     query = request.args.get(text, None)
#     table = None
#     if query is not None:
#         items = Meme.query.filter(Meme.tags.like('%'+query+'%')).all()
#         table = ItemTable(items)
#     return render_template('index.html', form=form, query=query, table=table)

# def respondToTweet(file):
#     last_id = get_last_tweet(file)
#     mentions = api.mentions_timeline(last_id, tweet_mode='extended')
#     if len(mentions) == 0:
#         return
#     else:
#         for mention in reversed(mentions):
#             tweet= []
#             new_id = mention.id
#             text = mention.full_text
#             meme = Meme(tags=text)
#             db.session.add(meme)
#             db.session.commit()
#             # meme = Meme.query.filter_by(tags=text).first()
#             memes = Meme.query.filter(Meme.tags.contains(text))
#             domain = "localhost/home"
#             url = domain + text
#             console.log(text)
        

#             api.update_status('@' + mention.user.screen_name + " Here's your Search results. Click the link below: " + "/n" + url, mention.id)

if __name__=='__main__':
	app.run(debug=True)







# direct_messages = tweepy.Cursor(api.direct_messages, since_id=since_id).items()

# for dm in direct_messages:
#         print dm.text


        # <!-- row -->
        # <!--gihys-
        # <div class="row tm-mb-90 tm-gallery">
        #     {% for giphy in dict %}
        #     {% if giphy %}
        #     <div class="col-xl-3 col-lg-4 col-md-6 col-sm-6 col-12 mb-5">
        #         <figure class="effect-ming tm-video-item">
        #             <img src="{{giphy.url}}" alt="Image" class="img-fluid">
        #             <figcaption class="d-flex align-items-center justify-content-center">
        #                 <h2>Clocks</h2>
        #                 <a href="{{giphy.url}}">View more</a>
        #             </figcaption>                    
        #         </figure>
        #         <div class="d-flex justify-content-between tm-text-gray">
        #             <span class="tm-text-gray-light">{{giphy.data[giphy]['images']['original']['url']}}</span>
        #             <span>{{giphy['title']}}</span>
        #         </div>
        #     </div>
        #         {% endif %}
        #     {% endfor %}
        # </div>-->