from . import db
from sqlalchemy import ForeignKey, DateTime, func
from flask_login import UserMixin
from sqlalchemy.orm import relationship

# TODO - CONFIGURE TABLES

# Users table
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship('Comments', back_populates='commenter')

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        # return self.email
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def add_user(user_name,user_email, user_password):
        new_user = User(
            name=user_name,
            email=user_email,
            password=user_password
        )
        db.session.add(new_user)
        db.session.commit()

# Blog table
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey("user.id"))
    author = relationship("User", back_populates="posts")
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    # author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    # # one-to-many relationship with comments
    # comment_id = db.Column(db.Integer,ForeignKey("comments.id"))
    comments = relationship('Comments', back_populates='post')

    def get_all_blogs(self):
        all_posts = db.session.execute(db.select(self.__class__).order_by(self.title)).scalars().all()
        return all_posts

# Comments table
class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    post_id = db.Column(db.Integer, ForeignKey("blog_posts.id"))
    text = db.Column(db.String(250),nullable=False)
    posted_at = db.Column(DateTime(), nullable=False, server_default=func.CURRENT_TIMESTAMP())
    commenter = relationship('User',back_populates='comments')
    post = relationship('BlogPost',back_populates='comments')

    def get_all_comments(self,blog_id):
        all_comments = db.session.execute(
            db.select(self.__class__).join(BlogPost.comments).where(BlogPost.id==self.__class__.post_id).where(BlogPost.id==blog_id)).scalars().all()
        return all_comments