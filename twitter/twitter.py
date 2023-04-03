from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    """
    The menu to print once a user has logged in
    """

    def __init__(self, current_user = None):
        self.current_user = current_user


    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    #Method loops until valid user (name not taken) is entered
    def register_user(self):
        while True:
            handle = input("What will your twitter handle be? ")
            pw = input("Enter a password: ")
            reenter = input("Re-enter your password: ")
            check = db_session.query(User).where(User.username == handle).first()
                
            
            if check == None:
                if pw == reenter:
                    user = User(username = handle, password = pw)
                    db_session.add(user)
                    db_session.commit()
                    self.logged_in = True
                    self.current_user = user
                    break
                else:
                    print("The passwords don't match. Try again.")
            else:
                print("That username is already taken. Try again.")

    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    #Method continually asks for username and password until combination matches a record listed in the users table
    def login(self):
        while self.current_user == None:
            name = input("Username: ")
            pw = input("Password: ")
            user = db_session.query(User).where((User.username == name) & (User.password == pw)).first()
            while user == None:
                print("Invalid username or password")
                name = input("Username: ")
                pw = input("Password: ")
                user = db_session.query(User).where((User.username == name) & (User.password == pw)).first()
            else:
                print("you are succesfully logged in")
                self.current_user = user
                #sets the user found in the query to the current user so that it can be refered to in other methods as the user logged in to twitter

    #sets the current user to none allowing a new user to log in
    def logout(self):
        self.current_user = None
        self.startup()

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        choice = int(input("Welcome to ATCS Twitter! \n Please select a Menu Option \n 1. Login \n 2. Register User \n 0. Exit"))
        if choice == 1:
            self.login()
            
        if choice == 2:
            self.register_user()
        if choice == 0:
            exit(0)

    #If the current user does not already follow the user given, the method hads an entry into follower which keeps track of who follows who
    def follow(self):
        follow = input("Who would you like to follow? ")
        user = db_session.query(User).where(User.username == follow).first()
        check = db_session.query(Follower).where((Follower.follower_id == self.current_user.username) and (Follower.following_id == user.id)).first()
        if(check == None):
            follower = Follower(follower_id = self.current_user.username, following_id = user.username)
            db_session.add(follower)
            db_session.commit()
            print("You are now following @" + user.username)
        else:
            print("You already follow @" + user.username)
        
    #Removes the follower following entry in the following table given that it exists
    def unfollow(self):
        unfollow = input("Who would you like to unfollow? ")
        user = db_session.query(Follower).where((Follower.follower_id == self.current_user.username) and (Follower.following_id == unfollow)).first()
        if(user == None):
            print("You don't follow " + user.username)
        else:
            db_session.delete(user)
            db_session.commit()
            print("You are no longer following @" + unfollow)
    #Creates a tweet by requesting content and tags. Saves it into tweets table; entries can then be printed when needed. 
    def tweet(self):
        tweetContent = input("Create Tweet: ")
        tags = input("Enter your tags seperated by spaces: ")
        newTweet = Tweet(content = tweetContent, username = self.current_user.username, timestamp = datetime.now())
        db_session.add(newTweet)
        db_session.commit()
        tweet = db_session.query(Tweet).where(Tweet.content == tweetContent).first()
        tweetid = tweet.id
        tags = tags.split()
        for t in tags:
            if db_session.query(Tag).where(Tag.content == t).first() == None:
                tag = Tag(t)
                db_session.add(tag)
                db_session.commit()
            else:
                tag = db_session.query(Tag).where(Tag.content == t).first()
            tweetTag = TweetTag(tag_id = tag.id, tweet_id = tweetid)
            db_session.add(tweetTag)
            db_session.commit()
    #Queries for all tweets that are authored by the current user and lists them out using the print_tweets method
    def view_my_tweets(self):
        tweets = db_session.query(Tweet).where(Tweet.username == self.current_user.username)
        self.print_tweets(tweets)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    
    #iterates through the usernames that the current user is following. This is used to query for tweets made by these users. The first five tweets are then printed in order of timestamp.
    def view_feed(self):
        for following in self.current_user.following:
            user_tweets = db_session.query(Tweet).where(Tweet.username == following.username).order_by(Tweet.timestamp.desc()).limit(5)
            self.print_tweets(user_tweets)

        
    #Allows the user to search for tweets by a specific user using a query for tweets authored by a specific username
    def search_by_user(self):
        username = input("Whose tweets would you like to see? ")
        if db_session.query(User).where(User.username == username).first() != None:
            tweets = db_session.query(Tweet).where(Tweet.username == username)
            self.print_tweets(tweets)
        else:
            print("There is no user by that name")
    #Allows for the user to instead search for tweets given a tag using a similar query as search by user. Also checks to see if the tag exists
    def search_by_tag(self):
        t = input("What tag would you like to see? ")
        tag = db_session.query(Tag).where(Tag.content == t).first()
        if  tag != None:
            tweets = db_session.query(TweetTag, Tweet).join(Tweet, Tweet.id == TweetTag.tweet_id).where(TweetTag.tag_id == tag.id)
            self.print_tweets(tweets)
        else:
            print("There is no tag by that name")

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()
        #Runs while current user exists which means someone is logged in
        while self.current_user != None:
            self.print_menu()
            option = int(input(""))
        
            if option == 1:
                self.view_feed()
            elif option == 2:
                self.view_my_tweets()
            elif option == 3:
                self.search_by_tag()
            elif option == 4:
                self.search_by_user()
            elif option == 5:
                self.tweet()
            elif option == 6:
                self.follow()
            elif option == 7:
                self.unfollow()
            else:
                self.logout()
        
        self.end()

