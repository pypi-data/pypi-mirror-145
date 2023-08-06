from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

post_recipients = db.Table('post_recipient',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')))

group_recipients = db.Table('group_recipient',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')))

group_posts = db.Table('group_post',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    online = db.Column(db.Boolean)
    posts = db.relationship('Post', backref='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_online(self, status):
        self.online = status

    def is_online(self):
       return self.online

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipients = db.relationship('User', secondary=post_recipients, backref='recipients')

    def __repr__(self):
        return '<{}: {}>'.format(self.author.username, self.body)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participants = db.relationship('User', secondary=group_recipients, backref='participants')
    messages = db.relationship('Post', secondary=group_posts, backref='posts')
    name = db.Column(db.String(140))