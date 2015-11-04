from __future__ import division
from twython import Twython,TwythonError
import Tconfig
import pickle
import os
import time

#import datetime
#import seaborn as sns
#import matplotlib.pyplot as plt
#import numpy as np
#from pytz import timezone
#import pytz
#from matplotlib.ticker import FuncFormatter


class usertweet:
    def __init__(self,username='justinbieber',realname=''):
        self._username=username
        self._twitter = None
        self._tweetlist = None
        self._filename = self._username+'.pickle'
        if realname == '':
            self._realname = self._username
        else:
            self._realname = realname

        
    def get_user_tweets(self):
        APP_KEY=Tconfig.account['APP_KEY']
        APP_SECRET=Tconfig.account['APP_SECRET']
        ACCESS_TOKEN =Tconfig.account['ACCESS_TOKEN']
        ACCESS_SECRET = Tconfig.account['ACCESS_SECRET']
        
        #first check if previously loaded tweets exist
        previously_loaded = False
        if os.path.isfile(self._filename):
            self._tweetlist = pickle.load( open(self._filename,'rb') )
            since_id = self._tweetlist[0]["id"]
            previously_loaded = True
            print "Found tweet file"
        
        try:
            self._twitter = Twython(APP_KEY,APP_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
            if previously_loaded == True:
                new_tweets = self._twitter.get_user_timeline(screen_name=self._username,\
                                                        since_id = since_id, count=200)
                if(len(new_tweets)>0):
                    print "Added ", len(new_tweets), " new tweets"
                    self._tweetlist = new_tweets + self._tweetlist
                else:
                    print "No new tweets since previous run"
            else:
                self.first_time_setup(APP_KEY,APP_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
                print "New user added"
                
            print "Tweet query successful"
            print "Total tweets in file:", len(self._tweetlist)
            print "Latest tweet:", self._tweetlist[0]["created_at"]
            print "Oldest tweet:", self._tweetlist[-1]["created_at"]

            pickle.dump( self._tweetlist, open(self._filename, 'wb') )
            
        except TwythonError as e:
            print e
    
    #repeatedly call to get all 3200 previous tweets
    def first_time_setup(self, APP_KEY,APP_SECRET, ACCESS_TOKEN, ACCESS_SECRET):
        try:
            self._twitter = Twython(APP_KEY,APP_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
            
            #first time
            self._tweetlist = self._twitter.get_user_timeline(screen_name=self._username,\
                                                                    count= 200)
            while(len(self._tweetlist)<3199):
                max_id = self._tweetlist[-1]["id"]
                try:
                    older_tweets = self._twitter.get_user_timeline(screen_name=self._username,\
                                                            max_id = max_id, count=200)
                    
                except TwythonError as e:
                    print "One of the repeat queries went wrong"
                    print e
                    
                if len(older_tweets)>1:
                 
                    
                    assert (older_tweets[1]["id"]<max_id)
                    self._tweetlist = self._tweetlist + older_tweets[1:len(older_tweets)]
                    print "Looping through old tweets, now size:", len(self._tweetlist)
                else:
                    print "Latest query did not yield new tweets, quitting loop"
                    break
                time.sleep(3)
            
            
        except TwythonError as e:
            print e
    
    def load_user_tweets(self):
        try:
            self._tweetlist = pickle.load( open(self._filename,'rb') )
            return self._tweetlist
        except:
            print "Could not load pickle file for user"
            return None


#bieber = usertweet(
#bieber.get_user_tweets()
##bieber.load_user_tweets()
#bieber.process_createdate()
#bieber.plot_hourhist()
#bieber.tweet_interval()

