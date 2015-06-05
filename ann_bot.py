import requests
import re
import random
import tweepy
import json
from tweepy.streaming import StreamListener
from tweepy import Stream

def getXML():
    url = 'http://www.animenewsnetwork.com/encyclopedia/reports.xml?id=172&nlist=100&nskip=0'
    request = requests.get(url)
    if request.status_code == 200:
        #print "Successfully downloaded XML"
        #print request.text
        return request.text

def pick_random():
    anime_xml = getXML()
    match = re.findall('>([^"<"]+)</anime>', anime_xml)
    match = [s.encode('ascii','ignore') for s in match]
    match = [s.replace('&amp;', '&') for s in match]
    return random.choice(match)
    

def auth_twitter():
    consumer_key = ""
    with open("consumer_key.txt", "r") as cons_key_file:
        consumer_key = cons_key_file.read()
    comsumer_key = consumer_key.strip()
    consumer_key = consumer_key.rstrip()

    consumer_secret = ""
    with open("consumer_secret.txt", "r") as cons_secret_file:
        consumer_secret = cons_secret_file.read()
    consumer_secret = consumer_secret.strip()
    consumer_secret = consumer_secret.strip()
    
    access_token = ""
    with open("access_token.txt", "r") as access_token_file:
        access_token = access_token_file.read()
    access_token = access_token.strip()
    access_token = access_token.strip()
    
    access_token_secret = ""
    with open("access_token_secret.txt", "r") as access_secret_file:
        access_token_secret = access_secret_file.read()
    access_token_secret = access_token_secret.strip()
    access_token_secret = access_token_secret.strip()
    

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

def post_bot():
    auth = auth_twitter()
    api = tweepy.API(auth)
    api.update_status(status=pick_random())


auth = auth_twitter()

class ReplyToTweet(StreamListener):

    def on_data(self, data):
        api = tweepy.API(auth)
        print data
        tweet = json.loads(data.strip())

        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user',{}).get('id_str','') == "3290086726"

        if retweeted is not None and not retweeted and not from_self:
            tweetId = tweet.get('id_str')
            screenName = tweet.get('user',{}).get('screen_name')
            tweetText = tweet.get('text')
            
            replyText = '@' + screenName + ' go watch ' +  pick_random()
            
            print('Tweet ID: ' + tweetId)
            print('From: ' + screenName)
            print('Tweet Text: ' + tweetText)
            print('Reply Text: ' + replyText)
            api.update_status(status=replyText)

    def on_error(self, status):
        print status

if __name__ == '__main__':
        streamListener = ReplyToTweet()
        twitterStream = Stream(auth, streamListener)
        twitterStream.userstream(_with='user')

#pick_random()
#post_bot()
