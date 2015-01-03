#encoding:utf8

from datetime import datetime

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import etc
db_info = etc.db_info

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@127.0.0.1/pos_mkw'
app.config['SQLALCHEMY_DATABASE_URI'] = '%s://%s:%s@%s:%s/%s' % (db_info['driver'], db_info['user'],  \
                                                                 db_info['pawd'], db_info['host'], \
                                                                 db_info['port'], db_info['name'])
app.config['SQLALCHEMY_ECHO'] = db_info['echo']
db = SQLAlchemy(app)

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32) )
    email    = db.Column(db.String(120), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, default=datetime.now())

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
        backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category_id):
        self.title = title
        self.body = body
        self.category_id = category_id

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.String(1024))
    slot = db.Column(db.String(100), unique=True)
    ord  = db.Column(db.Integer)
    flag = db.Column(db.Integer)
    def __init__(self, name, desc, slot, cord=1, flag=1):
        self.name = name
        self.desc = desc
        self.slot = slot
        self.ord  = cord
        self.flag = flag

    def __repr__(self):
        return '<Category %r>' % self.name
    

class Setting(db.Model):
    id    = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(100), unique = True)
    value = db.Column(db.Text)
    remark= db.Column(db.String(1024))
    def __init__(self, f,v,r):
        self.field   = f
        self.value = v
        self.remark= r
    
    def __repr__ (self):
        return "<Setting %r>" % self.field
    
