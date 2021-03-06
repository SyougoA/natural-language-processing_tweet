from requests_oauthlib import OAuth1
from sqlite_twitter import SqliteTweet
import requests
import json
import re


class TwitterStreamingDate(object):
    """
    statuses/filter...followID,keyword,location指定ができる
    statuses/sample...広く浅く全tweetの1%を無作為に取得

    """
    def __init__(self):
        self.consumer_key = ""
        self.consumer_secret = ""
        self.access_token = ""
        self.access_secret = ""
        self.auth = OAuth1(self.consumer_key, self.consumer_secret, self.access_token, self.access_secret)

        self.sql_tweet = SqliteTweet("location_streaming")

        self.filter_api = "https://stream.twitter.com/1.1/statuses/filter.json"
        japan = "122.87,24.84,153.01,46.80"
        self.req = requests.post(self.filter_api,
                                 auth=self.auth,
                                 stream=True,
                                 data={"location": japan})

    def tweets_data(self):
        for tweet in self.req.iter_lines():
            tweet = json.loads(tweet.decode("utf-8"))
            if "retweeted_status" in tweet:
                pass
            else:
                name = tweet["user"]["screen_name"]
                comment = tweet["text"]
                reply_name = tweet["in_reply_to_screen_name"]
                comment = self.erase(comment)

                tweet_data = (name, comment, reply_name)
                print(tweet_data)
                self.sql_tweet.insert_tweet(tweet_data)

    @staticmethod
    def erase(txt):
        # re_data -> 空行、改行、url、(半角記号,数字,英字)、(全角記号)
        txt = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", txt)
        txt = re.sub(r'[!-~]', "", txt)
        txt = re.sub(r'[︰-＠]', "", txt)
        txt = re.sub(' ', "", txt)
        txt = re.sub('\n', "", txt)

        return txt


if __name__ == "__main__":
    tw = TwitterStreamingDate()
    tw.tweets_data()
