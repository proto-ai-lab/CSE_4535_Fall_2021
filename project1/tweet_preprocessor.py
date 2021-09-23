'''
@author: Souvik Das
Institute: University at Buffalo
'''

import demoji, re, datetime
import preprocessor
from datetime import datetime,timedelta


# demoji.download_codes()


class TWPreprocessor:
    @classmethod
    def preprocess_poi(cls, tweet,poi = None,isReply = False):
        '''
        Do tweet pre-processing before indexing, make sure all the field data types are in the format as asked in the project doc.
        :param tweet:
        :return: dict
        '''
        rcvd_json = tweet._json
        valid_languages = ["en", "es", "hi"]
        if rcvd_json['lang'] not in valid_languages:
            return {}
        #print(tweet._json)
        data = { 
                 'poi_name' : rcvd_json["user"]["screen_name"],
                 'poi_id' : rcvd_json["user"]["id"],
                 'verified': rcvd_json["user"]["verified"],
                 'id' : rcvd_json["id_str"],
                 'country' : poi['country'],
                 #'tweet_text' : rcvd_json["full_text"],
                 'tweet_lang' : rcvd_json["lang"]
                }
        if isReply == False:
            data["poi_name"] =  rcvd_json["user"]["screen_name"]
            data["poi_id"] = rcvd_json["user"]["id"]
        else:
            data["replied_to_tweet_id"] = rcvd_json["replied_to_tweet_id"]
            data["replied_to_user_id"] = rcvd_json["replied_to_user_id"]
            data["reply_text"] = rcvd_json["reply_text"]
        text_xx = 'text_' + rcvd_json["lang"]
        if "full_text" in rcvd_json:
            data['tweet_text'] = rcvd_json["full_text"]
            text_cleaner = _text_cleaner(rcvd_json["full_text"])
        else:
            data['tweet_text'] = rcvd_json["text"]
            text_cleaner = _text_cleaner(rcvd_json["text"])
        data[text_xx] = text_cleaner[0]
        if len(text_cleaner[1]) > 0:
            data['tweet_emoticons'] = text_cleaner[1]
        hashtags = _get_entities(rcvd_json,'hashtags')
        mentions = _get_entities(rcvd_json,'mentions')
        tw_url = _get_entities(rcvd_json,'urls')
        if len(hashtags) > 0:
            data['hashtags'] = hashtags
        if len(mentions) > 0:
            data['mentions'] = mentions
        if len(tw_url) > 0:
            data['tweet_urls'] = tw_url
        if rcvd_json['geo'] != None:
            data['geolocation'] = rcvd_json['geo']['coordinates']
        date = rcvd_json['created_at']
        data['tweet_date'] = str(_get_tweet_date(date))
        #print("********************* formatted data ***************")
        #print(data)
        return data

    @classmethod
    def preprocess_kw(cls, tweet):
        '''
        Do tweet pre-processing before indexing, make sure all the field data types are in the format as asked in the project doc.
        :param tweet:
        :return: dict
        '''
        rcvd_json = tweet._json
        valid_languages = ["en", "es", "hi"]
        if rcvd_json['lang'] not in valid_languages:
            return {}
        #print(tweet._json)
        data = {
                 'verified': rcvd_json["user"]["verified"],
                 'id' : rcvd_json["id_str"],
                 'tweet_text' : rcvd_json["full_text"],
                 'tweet_lang' : rcvd_json["lang"]
                }
        if rcvd_json["lang"] == "en":
            data['country'] = "USA"
        elif rcvd_json["lang"] == "hi":
            data['country'] = "India"
        else:
            data['country'] = "Mexico"
        text_xx = 'text_' + rcvd_json["lang"]
        text_cleaner = _text_cleaner(rcvd_json["full_text"])
        data[text_xx] = text_cleaner[0]
        if len(text_cleaner[1]) > 0:
            data['tweet_emoticons'] = text_cleaner[1]
        hashtags = _get_entities(rcvd_json,'hashtags')
        mentions = _get_entities(rcvd_json,'mentions')
        tw_url = _get_entities(rcvd_json,'urls')
        if len(hashtags) > 0:
            data['hashtags'] = hashtags
        if len(mentions) > 0:
            data['mentions'] = mentions
        if len(tw_url) > 0:
            data['tweet_urls'] = tw_url
        if rcvd_json['geo'] != None:
            data['geolocation'] = rcvd_json['geo']['coordinates']
        date = rcvd_json['created_at']
        data['tweet_date'] = str(_get_tweet_date(date))
        #print("********************* formatted data ***************")
        #print(data)
        return data


def _get_entities(tweet, type=None):
    result = []
    if type == 'hashtags':
        hashtags = tweet['entities']['hashtags']

        for hashtag in hashtags:
            result.append(hashtag['text'])
    elif type == 'mentions':
        mentions = tweet['entities']['user_mentions']

        for mention in mentions:
            result.append(mention['screen_name'])
    elif type == 'urls':
        urls = tweet['entities']['urls']

        for url in urls:
            result.append(url['url'])

    return result


def _text_cleaner(text):
    emoticons_happy = list([
        ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
        ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
        '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
        'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
        '<3'
    ])
    emoticons_sad = list([
        ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
        ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
        ':c', ':{', '>:\\', ';('
    ])
    all_emoticons = emoticons_happy + emoticons_sad

    emojis = list(demoji.findall(text).keys())
    clean_text = demoji.replace(text, '')

    for emo in all_emoticons:
        if (emo in clean_text):
            clean_text = clean_text.replace(emo, '')
            emojis.append(emo)

    clean_text = preprocessor.clean(text)
    # preprocessor.set_options(preprocessor.OPT.EMOJI, preprocessor.OPT.SMILEY)
    # emojis= preprocessor.parse(text)

    return clean_text, emojis


def _get_tweet_date(tweet_date):
    return _hour_rounder(datetime.strptime(tweet_date, '%a %b %d %H:%M:%S +0000 %Y'))


def _hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
            + timedelta(hours=t.minute // 30))
