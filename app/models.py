from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), index = True)
    email = db.Column(db.String(255),unique = True, index = True)
    bio = db.Column(db.String(1000))
    profile_pic_path = db.Column(db.String)
    password_secure = db.Column(db.String(255))
    blogs = db.relationship('Blog',backref = 'user', lazy = 'dynamic')
    comments = db.relationship('Comment', backref = 'user', lazy = 'dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.password_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_secure,password)

    def __repr__(self):
        return f'User{self.username},{self.email}'

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer,primary_key = True)
    blog_title = db.Column(db.String)
    blog_content = db.Column(db.String(1000))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    comments = db.relationship('Comment',backref =  'blog_id',lazy = "dynamic")


    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_blog(cls,id):
        blog = Blog.query.filter_by(id = id).first()

        return blog

    @classmethod
    def count_blogs(cls,uname):
        user = User.query.filter_by(username = uname).first()
        blogs = Blog.query.filter_by(user_id = user.id).all()

        blog_count = 0
        for blog in blogs:
            blog_count += 1

        return blog_count

    def __repr__(self):
        return f'Blog {self.blog_title}'


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(1000))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    blog = db.Column(db.Integer,db.ForeignKey("blogs.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,blog):
        comments = Comment.query.filter_by(blog_id = blog).all()
        return comments

    def __repr__(self):
        return f'Comment{self.comment}'

class Subscription(UserMixin, db.Model):
    __tablename__ = 'subs'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)

    def __repr__(self):
        return f'{self.email}'


class Quotes():
    def __init__(self, id, author, quote):
        self.id = id
        self.author = author
        self.quote = quote
