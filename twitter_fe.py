import tweepy
from time import sleep
from generador import get_tweet

class TwitterFrontend():
    def __init__(self, db, ck, cs, ct, cts):
        print("[*] Iniciando bot de Twitter con Consumer Key = ",ck)# Authenticate to Twitter

        auth = tweepy.OAuthHandler(ck, cs)
        auth.set_access_token(ct, cts)
        self.db = db
        self.twitter = tweepy.API(auth)

    #Tuitear
    def tweet_bot(self, sleep_time):
        while(True):
            tweet = get_tweet(self.db)
            sleep(sleep_time)
            self.twitter.update_status(tweet, source="SentenceBot")
        