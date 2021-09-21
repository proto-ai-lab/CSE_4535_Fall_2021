'''
@author: Souvik Das
Institute: University at Buffalo
'''

import tweepy


class Twitter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler("zDYimvTNMu88qvb8UZ48RhIH6", "lrtMbRpMQySzIPJvidvHjqEuBWzwq4wlblFXfh7iU5YBGDvF3A")
        self.auth.set_access_token("1434993801223884804-ajixj7ntSNzK74ViDdJCHzoqbICzmO", "uMkhDXd28lIZmMhi8GjlLCMvgcklXrn1bowfkZz3hzrRS")
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def _meet_basic_tweet_requirements(self):
        '''
        Add basic tweet requirements logic, like language, country, covid type etc.
        :return: boolean
        '''
        raise NotImplementedError

    def get_tweets_by_poi_screen_name(self,screen_name1,count1):
        '''
        Use user_timeline api to fetch POI related tweets, some postprocessing may be required.
        :return: List
        '''
        tweets = []
        #data = self.api.user_timeline(screen_name = screen_name1, count = count1, include_rts = False,tweet_mode='extended')
        #data = self.api.user_timeline(screen_name = screen_name1, count = count1,tweet_mode='extended')
        for data in tweepy.Cursor(self.api.user_timeline,screen_name = screen_name1, count = count1,tweet_mode='extended').items(count1):
            tweets.append(data)
        return tweets

    def get_tweets_by_lang_and_keyword(self,kw,count1,lang1):
        '''
        Use search api to fetch keywords and language related tweets, use tweepy Cursor.
        :return: List
        '''
        query = kw + "-filter:retweets"
        tweets = []
        for data in tweepy.Cursor(self.api.search,q = query,lang = lang1,count = count1).items(count1):
            tweets.append(data)
        return tweets

    def get_replies(self):
        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        '''
        raise NotImplementedError
