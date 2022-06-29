from structure import db
from datetime import datetime
from functools import wraps


class Meme(db.Model):
    __searchable__ = ['tags', 'description'] 
    id = db.Column(db.Integer, primary_key=True)
    mention_id = db.Column(db.String, nullable=True)
    tags = db.Column(db.Text, nullable=True)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    description = db.Column(db.String(255), nullable= True)
    type = db.Column(db.String(255), nullable= True)
    image = db.Column(db.String(150), nullable=False, default='image1.jpg')
    views = db.Column(db.Integer, nullable=True, default=0)
 

    def __repr__(self):
        return '<Meme %r>' % self.tags

    @property
    def serialize(self):

        return {"id": self.id,"tags": self.tags,"many2many": self.serialize_many2many}

    @property
    def serialize_many2many(self):
        return [item.serialize for item in self.many2many]




class Mention(db.Model):
    __seachbale__ = ['name','description']
    id = db.Column(db.Integer, primary_key=True)
    mention_id = db.Column(db.String, nullable=True)
    tags = db.Column(db.Text, nullable=True)
    full_text = db.Column(db.Text, nullable=True)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return '<Mention %r>' % self.tags


class DirectMessage(db.Model):
    __seachbale__ = ['name','description']
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.String, nullable=True)
    text = db.Column(db.Text, nullable=True)
    sender_id = db.Column(db.String, nullable=True)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)




# db.create_all()



