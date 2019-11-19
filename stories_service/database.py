# encoding: utf8
import datetime as dt

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()




class Story(db.Model):
    __tablename__ = 'story'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    text = db.Column(db.Text(1000))  # around 200 (English) words
    dicenumber = db.Column(db.Integer)
    # textual representation (labels) of dice faces {dice:[...]}
    roll = db.Column(db.JSON)

    date = db.Column(db.DateTime)
    # will store the number of likes, periodically updated in background
    likes = db.Column(db.Integer)
    # will store the number of likes, periodically updated in background
    dislikes = db.Column(db.Integer)
    # define foreign key
    author_id = db.Column(db.Integer)



    def __init__(self, *args, **kw):
        super(Story, self).__init__(*args, **kw)
        self.date = dt.datetime.now()

