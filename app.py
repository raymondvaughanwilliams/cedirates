from unittest import removeResult
from flask import Flask, render_template, request,redirect,url_for,flash 
from structure import db,app,api,logger,photos
import tweepy
import secrets
import requests
import logging
from models import Meme,Mention
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
    print (tag)
    print (memes)
    return render_template('indexnew.html',memes=memes,mentions=mentions,tags=tag)

@app.route('/home')
def home():
    # last_id = get_last_tweet(file)
    last_id = "1"
    mentions = api.mentions_timeline( tweet_mode='extended')
    if len(mentions) == 0:
        return
    else:
        for mention in mentions:
            print(mention)
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
                    print(tags)
                themention = Mention(mention_id=new_id,full_text=text,tags=tags)
                db.session.add(themention)
                db.session.commit()

                # meme = Meme.query.filter_by(tags=text).first()
                memes = Meme.query.filter(Meme.tags.like('%'+tags+'%')).all()
                domain = "localhost:5000/home/" + tags 
                url = domain + text
                # console.log(text)
                api.update_status('@' + mention.user.screen_name + " Here's your Search results. Click the link below: " + domain)
                return render_template("indexnew.html", memes=memes)

    return render_template('indexnew.html')



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




        # except:
        #     logger.info("Already replied to {}".format(mention.id))


# def get_last_tweet(file):
#     f = open(file, 'r')
#     lastId = int(f.read().strip())
#     f.close()
#     return lastId

# def put_last_tweet(file, Id):
#     f = open(file, 'w')
#     f.write(str(Id))
#     f.close()
#     logger.info("Updated the file with the latest tweet Id")
#     return