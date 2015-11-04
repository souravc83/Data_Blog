import usertweet as usertweet

def main():
    #metaphorminute is a bot that tweets every 2 min
    #this is useful to test whether the tweets
    #are being added properly
    bieber = usertweet.usertweet('metaphorminute')
    bieber.get_user_tweets()
    
    tweetlist = bieber.load_user_tweets()
    
    first_tweet = tweetlist[0]
    #for tweet in tweetlist:
    #    print tweet["created_at"]

if __name__ == '__main__':
    main()
    