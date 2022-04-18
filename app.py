from flask import Flask, render_template, request
from structure import db,app,api,logger
import tweepy
import requests
import logging
from models import Meme



# api key = RLYya4IiZvpFkLfn5pItSqPhW
# api secret= UaAjhhNYTmSB6FwCqEc5RDTkSB0dT2Y81jxCUFaqVGKht156Xd
# bearer_token = AAAAAAAAAAAAAAAAAAAAAOqEbgEAAAAABLp1X6nGWW2nXjYjgBjQ5VYCqSQ%3DpVZpzJVo4Bvy8GNQYeJA0fHcFEfkOlWSQUntNCncRmRC1BgF92
# access_token = 944709207038754816-pOXaIltIHr7rrORJiEOdcehpi6xUmZV
# access_token_secret = MhECXNlbr4F4ZfxMHz4iXgbpmhMcFWWMeEQYcsFxR1PwM



@app.route('/')
def home():
    # last_id = get_last_tweet(file)
    last_id = "1"
    mentions = api.mentions_timeline( tweet_mode='extended')
    if len(mentions) == 0:
        return
    else:
        for mention in mentions:
            mention_check = Meme.query.filter_by(mention_id=mention.id).first()
            if mention_check is None and "qqq" in mention.full_text:
                tweet= []
                new_id = mention.id
                text = mention.full_text
                meme = Meme(description=text,mention_id=new_id)
                db.session.add(meme)
                db.session.commit()
                # meme = Meme.query.filter_by(tags=text).first()
                memes = Meme.query.filter(Meme.tags.contains(text))
                domain = "localhost/home"
                url = domain + text
                # console.log(text)
            

                api.update_status('@' + mention.user.screen_name + " Here's your Search results. Click the link below: " + "/n" + url)
    return render_template('home.html')


    

	
	# search = request.args.get('q')
	
	# public_tweets = api.user_timeline(search)


# def get_url():
#     URL = "https://api.quotable.io/random"
#    url = "domain"+ 
#     try:
#         response = requests.get(URL)
#     except:
#         print("Error while calling API...")

# def respondToTweet(file):
#     last_id = get_last_tweet(file)
#     mentions = api.mentions_timeline(last_id, tweet_mode='extended')
#     if len(mentions) == 0:
#         return

#     for mention in reversed(mentions):
#         tweet= []
#         new_id = mention.id
#         text = mention.full_text
#         # meme = Meme.query.filter_by(tags=text).first()
#         memes = Meme.query.filter(Meme.tags.contains(text))
#         domain = "localhost/home"
#         url = domain + text
#         if mention.full_text.lower():
#             try:
#                 # tweet = get_quote()
#                 # Wallpaper.get_wallpaper(tweet)
#                 # media = api.media_upload("created_image.png")
#                 api.create_favorite(mention.id)
#                 query = request.args.get(text, None)
#                 meme = Meme(tags=text)
#                 db.session.add(meme)
#                 db.session.commit()

#                 api.update_status('@' + mention.user.screen_name + " Here's your Search results. Click the link below: " + "/n" + url, mention.id)
#             except:
#                 logger.info("Already replied to {}".format(mention.id))

#     put_last_tweet(file, new_id)


def get_last_tweet(file):
    f = open(file, 'r')
    lastId = int(f.read().strip())
    f.close()
    return lastId

def put_last_tweet(file, Id):
    f = open(file, 'w')
    f.write(str(Id))
    f.close()
    logger.info("Updated the file with the latest tweet Id")
    return










# api.update_status('@<username> My status update', tweetId)

# twts = api.search(q="Hello World!")

#list of specific strings we want to check for in Tweets
# t = ['Hello world!',
#     'Hello World!',
#     'Hello World!!!',
#     'Hello world!!!',
#     'Hello, world!',
#     'Hello, World!']

# for s in twt:
#     for i in t:
#         if i == s.text:
#             sn = s.user.screen_name
#             m = "@%s Hello!" % (sn)
#             s = api.update_status(m, s.id)


# mention_id = 1


# # The actual bot
# while True:
#     mentions = tweepy.Client.get_users_mentions(mention_id) 

#     for mention in mentions:
#         print("Mention tweet found")
#         print(f"{mention.author.screen_name} - {mention.text}")
#         mention_id = mention.id

#         if mention.in_reply_to_status_id is True:
#                 try:
#                     print("Attempting to reply...")
#                     response = client.create_tweet(text='tweet response text here', 
#                     in_reply_to_tweet_id=mention_id)
#                     print(response)
#                     print("Successfully replied :)")
#                 except Exception as exc:
#                     print(exc)
#     time.sleep(90) 


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

def respondToTweet(file):
    last_id = get_last_tweet(file)
    mentions = api.mentions_timeline(last_id, tweet_mode='extended')
    if len(mentions) == 0:
        return
    else:
        for mention in reversed(mentions):
            tweet= []
            new_id = mention.id
            text = mention.full_text
            meme = Meme(tags=text)
            db.session.add(meme)
            db.session.commit()
            # meme = Meme.query.filter_by(tags=text).first()
            memes = Meme.query.filter(Meme.tags.contains(text))
            domain = "localhost/home"
            url = domain + text
            console.log(text)
        

            api.update_status('@' + mention.user.screen_name + " Here's your Search results. Click the link below: " + "/n" + url, mention.id)

if __name__=='__main__':
	app.run(debug=True)




        # except:
        #     logger.info("Already replied to {}".format(mention.id))