'''
@author: Souvik Das
Institute: University at Buffalo
'''

import json
import datetime
import pandas as pd
from twitter import Twitter
from tweet_preprocessor import TWPreprocessor
from indexer import Indexer

reply_collection_knob = True

def read_records():
    with open("records.json") as json_file:
        data = json.load(json_file)

    return data

def write_records(data):
    with open("records.json", 'w') as json_file:
        json.dump(data, json_file)

def read_config():
    with open("config.json") as json_file:
        data = json.load(json_file)

    return data


def write_config(data):
    with open("config.json", 'w') as json_file:
        json.dump(data, json_file,ensure_ascii=False)


def save_file(data, filename):
    df = pd.DataFrame(data)
    df.to_pickle("data/" + filename)


def read_file(type, id):
    return pd.read_pickle(f"data/{type}_{id}.pkl")

def _update_records(records, lang, country):
    records[lang] = records[lang] + 1
    records[country] = records[country] + 1
    records["Total_tweets"] = records["Total_tweets"] + 1

    return records

def main():
    config = read_config()
    indexer = Indexer()
    twitter = Twitter()

    records = read_records()
    counter = records["counter"]
    pois = config["pois"]
    keywords = config["keywords"]
    kw_rply_finished = config["keywords_reply_finished"]

    for i in range(len(pois)):
        if pois[i]["finished"] == 0:
            print(f"---------- collecting tweets for poi: {pois[i]['screen_name']}")

            raw_tweets = twitter.get_tweets_by_poi_screen_name(
                screen_name1 = pois[i]["screen_name"],count1 = pois[i]["count"],poi_id = pois[i]["id"])  # pass args as needed

            processed_tweets = []
            for tw in raw_tweets:
                processed = TWPreprocessor.preprocess_poi(tweet= tw,poi=pois[i],isReply = False)
                if processed != {}:
                    processed_tweets.append(processed)
                    records = _update_records(counter, processed['tweet_lang'], processed['country'])
            #print(processed_tweets)
            indexer.create_documents(processed_tweets)
            print('DONE>>>>>>>>>>>>>')
            pois[i]["finished"] = 1
            pois[i]["collected"] = len(processed_tweets)

            write_config({
                    "pois": pois, "keywords": keywords, "keywords_reply_finished" : kw_rply_finished
                })

            write_records({
                "counter" : counter
            })            

            save_file(processed_tweets, f"poi_{pois[i]['id']}.pkl")
            print("------------ process complete -----------------------------------")
    
    for i in range(len(keywords)):
        if keywords[i]["finished"] == 0:
            print(f"---------- collecting tweets for keyword: {keywords[i]['name']}")

            raw_tweets = twitter.get_tweets_by_lang_and_keyword(
                kw = keywords[i]["name"],count1 = keywords[i]["count"],lang1 = keywords[i]["lang"]
            )  # pass args as needed

            processed_tweets = []
            for tw in raw_tweets:
                processed = TWPreprocessor.preprocess_kw(tweet= tw,isReply = False)
                if processed != {}:
                    processed_tweets.append(processed)
                    records = _update_records(counter, processed['tweet_lang'], processed['country'])

            indexer.create_documents(processed_tweets)

            keywords[i]["finished"] = 1
            keywords[i]["collected"] = len(processed_tweets)
            #keywords[i]["name"] = print(keywords[i]["name"])

            write_config({
                    "pois": pois, "keywords": keywords, "keywords_reply_finished" : kw_rply_finished
                })

            write_records({
                "counter" : counter
            })

            save_file(processed_tweets, f"keywords_{keywords[i]['id']}.pkl")

            print("------------ process complete -----------------------------------")

    if reply_collection_knob:
        poi_reply_counter = 0
        # Write a driver logic for reply collection, use the tweets from the data files for which the replies are to collected.
        if kw_rply_finished == "False":
            print("---------------collecting replies for keywords------------")
            kw_reply_counter = 0
            tweets = twitter.get_replies_kw()  # pass args as needed
            processed_tweets = []
            for tw in tweets:
                processed = TWPreprocessor.preprocess_kw(tweet= tw,isReply = True)
                if processed != {}:
                    processed_tweets.append(processed)
                    records = _update_records(counter, processed['tweet_lang'], processed['country'])
                kw_reply_counter = kw_reply_counter + 1
            #print(processed_tweets)
            indexer.create_documents(processed_tweets)
            kw_rply_finished = "True"
            write_config({
                    "pois": pois, "keywords": keywords, "keywords_reply_finished" : kw_rply_finished
                })
            counter['Total_reply_tweets'] = counter['Total_reply_tweets'] + kw_reply_counter
            print('DONE>>>>>>>>>>>>>')
            

            write_records({
                "counter" : counter
            })            

            save_file(processed_tweets, f"reply_kw.pkl")
            print("------------ process complete -----------------------------------") 


        for i in range(len(pois)):
            if pois[i]["reply_finished"] == 0:
                print(f"---------- collecting replies for tweets of poi: {pois[i]['screen_name']}")

                raw_tweets = twitter.get_replies(reply_id = pois[i]['id'],screen_name = pois[i]['screen_name'])  # pass args as needed

                processed_tweets = []
                for tw in raw_tweets:
                    processed = TWPreprocessor.preprocess_poi(tweet= tw,poi=pois[i],isReply = True)
                    if processed != {}:
                        processed_tweets.append(processed)
                        records = _update_records(counter, processed['tweet_lang'], processed['country'])
                        counter['Total_reply_tweets'] = counter['Total_reply_tweets'] + 1
                        poi_reply_counter = poi_reply_counter + 1
                        counter['Total_poi_replies'] = counter['Total_poi_replies'] + 1
                #print(processed_tweets)
                #indexer.create_documents(processed_tweets)
                print('DONE>>>>>>>>>>>>>')
                pois[i]["reply_finished"] = 1

                write_config({
                    "pois": pois, "keywords": keywords, "keywords_reply_finished" : kw_rply_finished
                })
                counter['Total_poi_replies'] =  poi_reply_counter
                counter['Total_reply_tweets'] = counter['Total_reply_tweets'] + poi_reply_counter
                write_records({
                    "counter" : counter
                })            

                save_file(processed_tweets, f"reply_poi_{pois[i]['id']}.pkl")
                print("------------ process reply poi tweets complete -----------------------------------")

            if poi_reply_counter > 4000:
                break
    
    print("---------------ALl processsing completed ---------------")


if __name__ == "__main__":
    main()
