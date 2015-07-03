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
    def __init__(self,username='justinbieber',t_zone='EST',realname=''):
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
    
    def _convert_datetime(self, create_dt_str):
        [day_abbr,month_abbr,datestr,timestr,zonestr,year] = create_dt_str.split(' ')
        date_string = day_abbr + '_' + month_abbr + '_' + datestr + '_' +\
                      timestr + '_' +year
        this_date = datetime.datetime.strptime(date_string, '%a_%b_%d_%H:%M:%S_%Y')
        this_date = pytz.utc.localize(this_date)
        this_date = this_date.astimezone(self._tzinfo)
        return this_date 
    
    def process_createdate(self):
        self._datetimelist=[]
        self._process_timezone()
        for tweet in self._tweetlist:
            this_date = self._convert_datetime(tweet['created_at'])
            self._datetimelist.append(this_date)
            
    def _process_timezone(self):
        if self._tzone_str =='EST':
            self._tzinfo = timezone('US/Eastern')
        elif self._tzone_str == 'CST':
            self._tzinfo = timezone('US/Pacific')        
            
    def plot_hourhist(self):
        hourhist = np.zeros((24,1))
        for dt_val in self._datetimelist:
            hr_val=dt_val.hour
            hourhist[hr_val]= hourhist[hr_val]+1
        hourhist = self._hourhist_ampm(hourhist)
        (sleep_L, sleep_R, night_tweet) = self._min_interval(hourhist)
        self._construct_plot(range(24),hourhist,sleep_L,sleep_R)
        print self._username,": %age of tweets in sleeping time: ",night_tweet
    
    def _construct_plot(self,x_vals,y_vals,sleep_L,sleep_R):
        ax = plt.gca()
        ax.xaxis.set_major_formatter( FuncFormatter(self._fmt_ampm_tick) )
        plt.tick_params(axis='both', which='major', labelsize=14)
        plt.xlim(0,24)
        plt.xlabel("Time of Day",fontsize =16)
        plt.ylabel("No. of tweets",fontsize = 16)
        plt.bar(x_vals,y_vals)
        plt.axvline(sleep_L,color='r',linestyle='solid')
        plt.axvline(sleep_R,color='r',linestyle='solid')
        plt.title(self._realname, fontsize = 20)
        plt.gcf().tight_layout()
        
        filename = 'Figures/'+self._username
        plt.savefig(filename)
        plt.show()
        
        
    def _hourhist_ampm(self,hourhist):
        hr_am = hourhist[0:12]
        hr_pm = hourhist[12:24]
        new_hrhist = np.concatenate( (hr_pm ,hr_am),axis =0 )
        return new_hrhist 
        
    def _fmt_ampm_tick(self,when,pos=None):
        if when ==0:
            hourstr = '12P.M'
        elif when<12:
            hourstr = str(int(when))+'P.M'
        elif when == 12:
            hourstr = '12A.M'
        else:
            hourstr = str(int(when-12))+'A.M'
        return hourstr    
    
    def _min_interval(self,hourhist):
        range_R = 24 - 8+1
        sleep_L = 0
        sleep_R = 0
        min_tweets = 200
        
        for i in range(range_R):
            slice_arr = hourhist[i:i+8]
            slice_tweets = np.sum(slice_arr)
            if slice_tweets<min_tweets:
                min_tweets = slice_tweets
                sleep_L = i
                sleep_R = i+8
        
        min_perc = ( min_tweets/np.sum(hourhist) )*100
        return sleep_L,sleep_R, min_perc
        
        
        
        
    def _calc_interval(self):
        if self._datetimelist is None:
            print "datetimelist is not defined"
            return
        self._tweetinterval =[]
        interval = datetime.timedelta()
        
        for i in range( 1,len(self._datetimelist) ):
            interval = self._datetimelist[i-1] - self._datetimelist[i]
            self._tweetinterval.append( interval.total_seconds()/60 )
         
    def tweet_interval(self):
        if self._datetimelist is None:
            self.process_createdate()
        self._calc_interval()
        plt.hist(self._tweetinterval,bins=40)
        plt.show()
        
        

bieber = usertweet('oliviataters','EST','Olivia Taters')
bieber.get_user_tweets()
#bieber.load_user_tweets()
bieber.process_createdate()
bieber.plot_hourhist()
#bieber.tweet_interval()

