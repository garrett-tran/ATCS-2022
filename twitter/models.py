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

    def __repr__(self):
        return "@" + self.username


class Follower(Base):
    __tablename__ = "followers"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    follower_id = Column('follower_id', INTEGER, ForeignKey('users.username'))
    following_id = Column('following_id', INTEGER, ForeignKey('users.username'))

class Tweet(Base):
    __tablename__ = "tweets"
    id = Column("id", INTEGER, primary_key=True)
    content = Column("content", TEXT, nullable = False)
    username = Column("username", TEXT, ForeignKey("users.username"))
    timestamp = Column("timestamp", TEXT, nullable = False)
    tags = relationship("Tag", secondary = "tweettags", back_populates = "tweets")
    def __repr__(self):
        tags = ""
        for tag in self.tags:
            tags += str(tag) + " "
        return "@" + self.username + "\n" + self.content + "\n" + self.timestamp + "\n" + tags

        

class Tag(Base):
    __tablename__ = "tags"
    id = Column("id", INTEGER, primary_key=True)
    content = Column("content", TEXT, nullable = False)
    tweets = relationship("Tweet", secondary = "tweettags", back_populates = "tags")
    def __init__(self, content):
        self.content = content
    def __repr__(self):
        return self.content

class TweetTag(Base):
    __tablename__ = "tweettags"
    id = Column("id", INTEGER, primary_key=True)
    tag_id = Column("tag_id", INTEGER, ForeignKey('tags.id'))
    tweet_id = Column("tweet_id", INTEGER, ForeignKey('tweets.id'))

