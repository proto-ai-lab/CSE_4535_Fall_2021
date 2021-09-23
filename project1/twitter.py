'''
@author: Souvik Das
Institute: University at Buffalo
'''

import tweepy
import json
poi_tweet_ids = {}
tweet_ids = {}

def read_tweet_ids():
    with open("tweet_ids.json") as json_file:
        data = json.load(json_file)

    return data

def write_tweet_ids(data):
    with open("tweet_ids.json", 'w') as json_file:
        json.dump(data, json_file)

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

    def get_tweets_by_poi_screen_name(self,screen_name1,count1,poi_id):
        '''
        Use user_timeline api to fetch POI related tweets, some postprocessing may be required.
        :return: List
        '''
        tweets = []
        keywords = ["quarentena",
      "hospital",
      "वैश्विकमहामारी",
      "oxygen",
      "सुरक्षित रहें",
      "stayhomestaysafe",
      "covid19",
      "quarantine",
      "face mask",
      "corona virus",
      "cierredeemergencia",
      "autoaislamiento",
      "sintomas",
      "covid positive",
      "कोविड मृत्यु",
      "स्वयं चुना एकांत",
      "stay safe",
      "#deltavariant",
      "covid symptoms",
      "sarscov2",
      "covidappropriatebehaviour",
      "pandemia de covid-19",
      "wearamask",
      "oxígeno",
      "coronawarriors",
      "quedate en casa",
      "mascaras",
      "trabajar desde casa",
      "संगरोध",
      "immunity",
      "स्वयं संगरोध",
      "dogajkidoori",
      "travelban",
      "covid",
      "variant",
      "yomequedoencasa",
      "doctor",
      "distancia social",
      "अस्पताल",
      "covid deaths",
      "कोविड19",
      "muvariant",
      "susanadistancia",
      "personal protective equipment",
      "quedateencasa",
      "social distancing",
      "distanciamiento social",
      "transmission",
      "epidemic",
      "social distance",
      "herd immunity",
      "transmisión",
      "सैनिटाइज़र",
      "indiafightscorona",
      "symptoms",
      "covid cases",
      "stayhomesavelives",
      "coronavirusupdates",
      "sanitize",
      "कोरोना",
      "sanitizer",
      "distanciamientosocial",
      "variante",
      "कोविड 19",
      "कोविड-19",
      "कोविड",
      "pandemic",
      "stayhome",
      "lavadodemanos",
      "maskmandate",
      "डेल्टा",
      "कोविड महामारी",
      "epidemia",
      "fiebre",
      "मौत",
      "travel ban",
      "फ़्लू",
      "स्वच्छ",
      "self-quarantine",
      "delta variant",
      "wuhan virus",
      "लक्षण",
      "corona",
      "maskup",
      "socialdistance",
      "stayathome",
      "positive",
      "lockdown",
      "propagación en la comunidad",
      "तीसरी लहर",
      "aislamiento",
      "coronavirus",
      "variante delta",
      "distanciasocial",
      "cubrebocas",
      "घर पर रहें",
      "socialdistancing",
      "covidwarriors",
      "प्रकोप",
      "covid-19",
      "stay home",
      "distanciamiento",
      "cuarentena",
      "indiafightscovid19",
      "healthcare",
      "मास्क पहनें",
      "delta",
      "wearmask",
      "fightagainstcovid19",
      "महामारी",
      "नियंत्रण क्षेत्र",
      "who",
      "mask",
      "pandemia",
      "deltavariant",
      "वैश्विक महामारी",
      "síntomas",
      "masks",
      "confinamiento",
      "flattening the curve",
      "cierre de emergencia",
      "स्वास्थ्य सेवा",
      "सोशल डिस्टन्सिंग",
      "covid vaccine",
        "vaccine mandate",
        "vaccines",
        "vaccination",
        "moderna",
        "covidvaccine",
        "shots",
        "covidvaccination",
        "vaccination drive",
        "vaccine passports",
        "teeka",
        "unvaccinated",
        "jab",
        "doses",
        "कोविशील्ड",
        "टीके",
        "टीकाकरण",
        "वैक्सीनेशन",
        "वैक्सीन पासपोर्ट",
        "टीकाकरण अभियान",
        "पहली खुराक",
        "एंटीबॉडी",
        "टीका",
        "वैक्सीन जनादेश",
        "anticuerpos",
        "eficacia de la vacuna",
        "dosis de vacuna",
        "vacunar",
        "vacunacovid19",
        "vacunado",
        "pinchazo",
        "vacunación",
        "vacuna",
        "primera dosis",
        "eficacia"]
        keyword_counter = 0
        keyword_index = 0
        tweet_id_index = []
        max_id = 0
        poi_tweet_ids[poi_id] = []
        tweet_ids[poi_id] = []
        read_tweet_id = read_tweet_ids()
        poi_tweet_ids_json = read_tweet_id["poi_tweet_ids"]
        kw_tw_id_json = read_tweet_id["kw_tweet_ids"]
        #data = self.api.user_timeline(screen_name = screen_name1, count = count1, include_rts = False,tweet_mode='extended')
        #data = self.api.user_timeline(screen_name = screen_name1, count = count1,tweet_mode='extended')
        """
        while keyword_counter < 10:
            query = "from:" + screen_name1 + " " + keywords[keyword_index]
            for data in tweepy.Cursor(self.api.search,q = query).items(5000):
                tweets.append(data)
                keyword_counter = keyword_counter+1
                rcvd_json = data._json
                tweet_id = rcvd_json["id_str"]
                tweet_id_index.append(tweet_id)
                poi_tweet_ids[poi_id].append(tweet_id)
                max_id = rcvd_json["id"]
                print("Keyword tweeetss **** for keyword = {}",keywords[keyword_index])
                print(data)
            keyword_index = keyword_index + 1
            if keyword_index == len(keywords):
                print("keywords related POI tweets collected = {}",keyword_counter)
                break
        
        for data in tweepy.Cursor(self.api.user_timeline,screen_name = screen_name1, count = count1,tweet_mode='extended',include_rts=False).items(count1):
            rcvd_json = data._json
            if rcvd_json["id_str"] in tweet_id_index:
                continue
            tweets.append(data)
        """
        retry_count = 0
        while  len(tweet_ids[poi_id]) < 500 or len(poi_tweet_ids[poi_id]) < 50:
            print("Let's go>>>>>>>") 
            retry_count = retry_count + 1
            if retry_count > 5:
                break
            for data in tweepy.Cursor(self.api.user_timeline, screen_name = screen_name1, count = count1,tweet_mode='extended',include_rts=False).items(count1):
                if data._json['id'] not in poi_tweet_ids[poi_id] and any(keyword in data._json['full_text'] for keyword in keywords) and len(poi_tweet_ids[poi_id]) < 50:
                    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<NEW>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>');
                    matching = [keyword for keyword in keywords if keyword in data._json['full_text']]
                    print(matching)
                    # any(word in 'some one long two phrase three' for word in list_)
                    print('tweet added')
                    tweets.append(data)
                    data._json['full_text']
                    if poi_id not in poi_tweet_ids[poi_id]:
                        poi_tweet_ids[poi_id].append(data._json['id'])
                        tweet_ids[poi_id].append(data._json['id'])
                        max_id = data._json['id']
                elif data._json['id'] not in tweet_ids:    
                    tweets.append(data)
                    tweet_ids[poi_id].append(data._json['id'])

        print('Total tweets collected>>>>')
        print(len(tweet_ids[poi_id]))
        print('Total KEYWORD tweets collected>>>>')
        print(len(poi_tweet_ids[poi_id]))    
        #print("Tweets_id for keywords are: *************\n")
        #print(tweet_id_index)
        poi_tweet_ids_json[poi_id] = poi_tweet_ids[poi_id]
        write_tweet_ids({
                "poi_tweet_ids" : poi_tweet_ids_json,
                "kw_tweet_ids" : kw_tw_id_json
            })
        return tweets

    def get_tweets_by_lang_and_keyword(self,kw,count1,lang1):
        '''
        Use search api to fetch keywords and language related tweets, use tweepy Cursor.
        :return: List
        '''
        read_tweet_id = read_tweet_ids()
        poi_tweet_ids_json = read_tweet_id["poi_tweet_ids"]
        kw_tw_id_json = read_tweet_id["kw_tweet_ids"]
        query = kw + "-filter:retweets"
        tweets = []
        for data in tweepy.Cursor(self.api.search,q = query,lang = lang1,count = count1,tweet_mode='extended').items(count1):
            tweets.append(data)
            kw_tw_id_json.append({"id": data.id,"user":data.user.screen_name})
        print("Number of tweets for the kw:"+kw+" is:",len(tweets))
        write_tweet_ids({
                "poi_tweet_ids" : poi_tweet_ids_json,
                "kw_tweet_ids" : kw_tw_id_json
            })
        return tweets

    def get_replies(self,reply_id,screen_name):
        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        
        replies=[]
        reply_counter = 0
        retry_count = 0
        poi_tweet_id_list = []
        index = 0
        loop_count = 0
        if reply_id != 100:
            poi_tweet_id_list = poi_tweet_ids[reply_id]
            print("POI tweet id list is : ",poi_tweet_id_list)
            for tweet_id in poi_tweet_id_list:
                index = poi_tweet_id_list.index(tweet_id)
                max_id = poi_tweet_id_list[index + 1]
                print("Collecting reply for tweet id: ",tweet_id)
                #print(str(tweet_id))
                while reply_counter < 10 or retry_count < 5:
                    if loop_count == 0:
                        tweet_list = tweepy.Cursor(self.api.search,q='to:'+screen_name, since_id=tweet_id,result_type = 'recent',tweet_mode='extended').items(100)
                    else:
                        tweet_list = tweepy.Cursor(self.api.search,q='to:'+screen_name, since_id=tweet_id,max_id = max_id,tweet_mode='extended').items(100)
                    loop_count = 1
                    for tweet in tweet_list:
                        if max_id < tweet._json['id']:
                            max_id = tweet._json['id']
                        #tw = tweet._json
                        print('1>>')
                        if hasattr(tweet, 'in_reply_to_status_id_str'):
                            print('2>>>')
                            if (tweet['in_reply_to_status_id_str']==str(tweet_id)):
                                print('3>>>>>')
                                print("reply found for tweet id:",tweet_id,"reply count:",reply_counter)
                                replies.append(tweet)
                                reply_counter = reply_counter + 1
                    print("Number of replies for tweet id:",tweet_id)
                    retry_count = retry_count + 1
                            #print(tweet)
        return replies
        '''

        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        '''
        print('---------------------------REPLIES STARTED')
        replies= []

        #tweet_ids = poi_tweet_ids[reply_id]
        read_tweet_id = read_tweet_ids()
        poi_tweet_ids_json = read_tweet_id["poi_tweet_ids"]
        kw_tw_id_json = read_tweet_id["kw_tweet_ids"]
        tweet_ids = poi_tweet_ids_json[str(reply_id)]
        for tid in tweet_ids:
            counter = 0
            max_id = 9999999999999999999
            for tweet in tweepy.Cursor(self.api.search,q='to:'+screen_name, result_type='recent', max_id = max_id, since_id=tid, tweet_mode='extended').items(1000):
                max_id = min(tweet.id,max_id)
                if max_id <= tid:
                    break
                print("max_id:",max_id)
                if hasattr(tweet, 'in_reply_to_status_id_str'):
                    if (tweet.in_reply_to_status_id_str==str(tid)):
                        replies.append(tweet)
                        print('Reply found')
                        counter = counter+1
                        print(counter)
                    if(counter >= 10):
                        #print(replies)
                        print('Going to next!!!!!!!!!!!!!!!!!!!!!')
                        break;    


        print('Replies found for all tweets')
        return replies

    def get_replies_kw(self):
        replies = []
        read_tweet_id = read_tweet_ids()
        poi_tweet_ids_json = read_tweet_id["poi_tweet_ids"]
        # kw_tw_id_json = { "fdjd" : "dfd"}
        tweet_ids = read_tweet_id["kw_tweet_ids"]
        #print(tweet_ids)
        counter = 0
        for tid in tweet_ids:
            counter_per_tw = 0
            max_id = 9999999999999999999
            for tweet in tweepy.Cursor(self.api.search,q=''+tid['user'], result_type='recent', since_id=tid['id'], max_id = max_id,tweet_mode='extended').items(1000):
                max_id = min(tweet.id,max_id)
                if max_id <= tid['id']:
                    break
                #print("max_id:",max_id)
                if hasattr(tweet, 'in_reply_to_status_id_str'):
                    if (tweet.in_reply_to_status_id_str==str(tid['id'])):
                        replies.append(tweet)
                        counter_per_tw = counter_per_tw + 1
                        counter = counter + 1
                        print('Reply found:',counter_per_tw)
                        print("********************reply**********")
                        #print(tweet)
                if counter_per_tw >= 3:
                    break
            print("************************Total keyword reply count****************",counter)
            if(counter >= 10000):
                print("reached 10000 kw replies!!")
                return replies
            print("Go to next tweet id from:",str(tid['id']))
        return replies
