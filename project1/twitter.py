import tweepy


class Twitter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler("", "")
        self.auth.set_access_token("", "")
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def _meet_basic_tweet_requirements(self):
        raise NotImplementedError

    def get_tweets_by_poi_screen_name(self):
        raise NotImplementedError

    def get_tweets_by_lang_and_keyword(self):
        raise NotImplementedError

    def get_replies(self):
        raise NotImplementedError
