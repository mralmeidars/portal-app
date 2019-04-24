from portal.services import mongoDatabase as db
from portal.services import cleanData

from json import load as json_load

import tweepy as tw
import time
import re

_dtTwitter = {}
_lastMaxId = -1
_twitter_limit_search = 0

def getCredentials():
    with open('portal/static/twitter_credentials.json') as twitter_cred:
        __credentialsAuth = json_load(twitter_cred)
    try:
        auth = tw.OAuthHandler( __credentialsAuth['CONSUMER_KEY'],
                                __credentialsAuth['CONSUMER_SECRET'] )
        auth.set_access_token(  __credentialsAuth['ACCESS_TOKEN_KEY'],
                                __credentialsAuth['ACCESS_TOKEN_SECRET'] )

    except tw.TweepError as e:
        print(f'Error: Twitter Authentication Failed - \n{str(e)}')

    return tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def getTweets(_query, _maxId, _tweetsMaxLimit = 1000): 
    __sinceId          = None
    __sleepTime        = 300 # seconds - 5 minutes - if necessary
    __tweetsCount      = 0
    __tweetsQueryLimit = 100
    __retry            = True

    __api = getCredentials()

    while __tweetsCount < _tweetsMaxLimit:
        try:
            if (_maxId <= 0):
                if (not __sinceId):
                    __apiTweets = __api.search(q=_query, count=__tweetsQueryLimit, lang='pt')
                else:
                    __apiTweets = __api.search(q=_query, count=__tweetsQueryLimit, since_id=__sinceId, lang='pt')
            else:
                if (not __sinceId):
                    __apiTweets = __api.search(q=_query, count=__tweetsQueryLimit, max_id=str(_maxId-1), lang='pt')
                else:
                    __apiTweets = __api.search(q=_query, count=__tweetsQueryLimit, max_id=str(_maxId-1), since_id=__sinceId, lang='pt')

            if (not __apiTweets):
                break

            for tweet in __apiTweets:
                __verifyTweet = {}
                __verifyTweet['tweets'] = tweet.text

                __textContent = cleanData.cleanEmoji(tweet.text.lower())
                __textContent = cleanData.cleanText(__textContent)

                # Create Data Dictionary
                __appendTweets = {
                                'user': tweet.user.screen_name,
                                'datetime': tweet.created_at,
                                'content': __textContent
                                }

                # Retweets - Appended only once
                if tweet.retweet_count > 0:
                    if __verifyTweet['tweets'] not in _dtTwitter['twitter']:
                        _dtTwitter['twitter'].append(__appendTweets)
                else:
                    # Tweet Id - Appended only once
                    if str(tweet.id) not in _dtTwitter['twitter']:
                        _dtTwitter['twitter'].append(__appendTweets)

                _lastMaxId = tweet.id

                if len(_dtTwitter['twitter']) == _tweetsMaxLimit:
                    __retry = False
                    break

            __tweetsCount = len(_dtTwitter['twitter'])
            _maxId = _lastMaxId

            return __retry

        except tw.RateLimitError:
            time.sleep(__sleepTime)
            pass

        except tw.TweepError:
            __retry = False
            break


class twitterClient(object):

    def __init__(self):
        _lastMaxId = -1

    def getData(self):
        with open('portal/static/parameters.json') as params:
            __params = json_load(params)

        _dtTwitter[__params['TWITTER_DB_COLLECTION']] = []
        _dbData = db.mongoData()

        try:
            while getTweets(_query=__params['TRACKING_TERM'], _maxId=_lastMaxId):
                __none = ' '

            # Storage Data
            _dbData.addManyData(    __params['MONGO_DB'],
                                    __params['TWITTER_DB_COLLECTION'],
                                    _dtTwitter[__params['TWITTER_DB_COLLECTION']])

        except Exception:
            pass
