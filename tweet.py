import tweepy
class Tweet:
    def __init__(self, cfg):
        auth = tweepy.OAuthHandler(cfg.CONSUMER_KEY, cfg.CONSUMER_SECRET)
        auth.set_access_token(cfg.ACCESS_TOKEN, cfg.ACCESS_SECRET)
        self.api = tweepy.API(auth)

    def tweet(self, msg):
        self.api.update_status(msg)
