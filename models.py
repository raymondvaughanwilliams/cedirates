from structure import db
from datetime import datetime
from functools import wraps


class Meme(db.Model):
    __seachbale__ = ['name','description']
    id = db.Column(db.Integer, primary_key=True)
    mention_id = db.Column(db.String, nullable=True)
    tags = db.Column(db.Text, nullable=True)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    description = db.Column(db.String(255), nullable= True)
    type = db.Column(db.String(255), nullable= True)
    image = db.Column(db.String(150), nullable=False, default='image1.jpg')
 

    def __repr__(self):
        return '<Addproduct %r>' % self.tags




class Mention(db.Model):
    __seachbale__ = ['name','description']
    id = db.Column(db.Integer, primary_key=True)
    mention_id = db.Column(db.String, nullable=True)
    tags = db.Column(db.Text, nullable=True)
    full_text = db.Column(db.Text, nullable=True)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return '<Mention %r>' % self.tags







