import usertweet as usertweet

def main():
    
    trump = usertweet.usertweet('realDonaldTrump')
    trump.get_user_tweets()
    #democrat
    hillary = usertweet.usertweet('HillaryClinton')
    hillary.get_user_tweets()
    
    sanders = usertweet.usertweet('BernieSanders')
    sanders.get_user_tweets()
    
    jeb = usertweet.usertweet('JebBush')
    jeb.get_user_tweets()
    
    rubio = usertweet.usertweet('marcorubio')
    rubio.get_user_tweets()
    
    fiorina = usertweet.usertweet('CarlyFiorina')
    fiorina.get_user_tweets()
    
    huckabee = usertweet.usertweet('GovMikeHuckabee')
    huckabee.get_user_tweets()
    
    cruz = usertweet.usertweet('tedcruz')
    cruz.get_user_tweets()
    
    paul = usertweet.usertweet('RandPaul')
    paul.get_user_tweets()

if __name__ == '__main__':
    main()
    