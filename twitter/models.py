"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT, DATETIME
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    # Columns
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)

    following = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.follower_id",
                             secondaryjoin="User.username==Follower.following_id")
    
    followers = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.following_id",
                             secondaryjoin="User.username==Follower.follower_id",
                             overlaps="following")
    tweets = relationship("Tweet", back_populates="user")
    
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Follower(Base):
    __tablename__ = "followers"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    follower_id = Column('follower_id', TEXT, ForeignKey('users.username'))
    following_id = Column('following_id', TEXT, ForeignKey('users.username'))

    def __init__(self, id, follower_id, following_id):
        self.id = id
        self.follower_id = follower_id
        self.following_id = following_id

class Tweet(Base):
    __tablename__ = "tweets"


    id = Column("id", INTEGER, primary_key=True)
    content = Column('content', TEXT, nullable=False)
    timestamp = Column('timestamp', TEXT, nullable=False)
    username = Column('username',TEXT, ForeignKey('users.username'))

    def __init__(self, id, content, timestamp, username):
        self.id = id
        self.content = content
        self.timestamp = timestamp
        self.username = username

    user = relationship("User", back_populates="tweet")

class Tag(Base):
    __tablename__ = "tags"

    id = Column("id", INTEGER, primary_key=True)
    content = Column('content', TEXT, nullable=False)
    
    def __init__(self, id, content):
        self.id = id
        self.content = content

class TweetTag(Base):
    __tablename__ = "tweettags"

    id = Column("id", INTEGER, primary_key=True)
    tweet_id = ("tweet_id", INTEGER, ForeignKey('tweets.id'))
    tag_id = ("tag_id", INTEGER, ForeignKey('tags.id'))

    def __init__(self, id, tweet_id, tag_id):
        self.id = id
        self.tweet_id = tweet_id
        self.tag_id = tag_id
