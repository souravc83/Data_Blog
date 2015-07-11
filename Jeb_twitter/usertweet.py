from __future__ import division
from twython import Twython,TwythonError
import Tconfig
import pickle
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pytz import timezone
import pytz
from matplotlib.ticker import FuncFormatter


class usertweet:
    def __init__(self,username='justinbieber',realname=''):
        self._username=username
        self._twitter = None
        self._tweetlist = None
        self._filename = self._username+'.pickle'
        self._datetimelist = None
        self._tweetinterval = None
        self._tzone_str=t_zone
        self._tzinfo = None
        if realname == '':
            self._realname = self._username
        else:
            self._realname = realname

        
    def get_user_tweets(self):
        APP_KEY=Tconfig.account['APP_KEY']
        APP_SECRET=Tconfig.account['APP_SECRET']
        ACCESS_TOKEN =Tconfig.account['ACCESS_TOKEN']
        ACCESS_SECRET = Tconfig.account['ACCESS_SECRET']
        try:
            self._twitter = Twython(APP_KEY,APP_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
            self._tweetlist = self._twitter.get_user_timeline(screen_name=self._username,\
                                                        count=500)
            print "Tweet query successful"
            pickle.dump( self._tweetlist, open(self._filename, 'wb') )
            
        except TwythonError as e:
            print e
    
    def load_user_tweets(self):
        try:
            self._tweetlist = pickle.load( open(self._filename,'rb') )
        except:
            print "Could not load pickle file for user"
    

bieber = usertweet('oliviataters','EST','Olivia Taters')
bieber.get_user_tweets()
#bieber.load_user_tweets()
bieber.process_createdate()
bieber.plot_hourhist()
#bieber.tweet_interval()

