#!/usr/bin/env python
'''
Helpful reference: http://benalexkeen.com/interacting-with-the-twitter-api-using-python/
'''

import os
import configparser
import requests
import base64
from requests_oauthlib import OAuth1

url2                        = 'https://api.twitter.com/1.1/search/tweets.json?q=nasa&result_type=popular'
url                         = 'https://api.twitter.com/oauth2/token'
payload                     = {'key': 'val'}
builtheader                 = ''
bearertokenfile             = 'conf/bearer.token'
bearertoken                 = ''
base_url                    = 'https://api.twitter.com/'

'''
readConf() is established to read the configuration file for the relevant keys and secrets in order to 
retrieve the bearer token (This is needed for application-only requests).

Returns the b64_encoded_key that needs to be sent with the request for the bearer token.

The bearer token should be STORED, not requested with each request.
'''

def bearerExists():
    try:
        # Open bearer file
        pass
        g = open('conf/bearer.token')
        x = True
    except FileNotFoundError:
        # Send error
        print('Error, bearer token not found.')
        x = False
        pass
    if x == True:
        print('Bearer token exists in /conf/ directory. Importing...')
    return x

def readConf():
    global conf
    global consumerapikey
    global consumersecret
    global accesstoken
    global accesstokensecret
    global builtheader
    global encodedkey

    conf = configparser.ConfigParser()
    conf.read('conf/key_conf.ini')

    twconsumer_key          = conf['twitter-consumer-api-key']['value']
    twconsumer_secret       = conf['twitter-consumer-secret']['value']
    twaccesstoken           = conf['twitter-access-token']['value']
    twaccesstokensecret     = conf['twitter-access-token-secret']['value']
    encodedkey              = '{}:{}'.format(twconsumer_key, twconsumer_secret).encode('ascii')
    b64_encoded_key         = base64.b64encode(encodedkey)
    b64_encoded_key         = b64_encoded_key.decode('ascii')
    return b64_encoded_key

# Gets the bearer token, if it's not already stored. Note there are rate limitations on how often this can be done.
# This following the Oauth2 authentication flow.
def generateBearer(x):
    import configparser
    import requests
    import base64

    conf = configparser.ConfigParser()
    conf.read('conf/conf.ini')

    # import relevant keys and secrets
    twconsumer_key = conf['twitter-consumer-api-key']['value']
    twconsumer_secret = conf['twitter-consumer-secret']['value']
    twaccesstoken = conf['twitter-access-token']['value']
    twaccesstokensecret = conf['twitter-access-token-secret']['value']

    # base64 encode the consumer key:secret pair
    key_secret = base64.urlsafe_b64encode('{}:{}'.format(twconsumer_key, twconsumer_secret).encode('UTF-8')).decode(
        'UTF-8')

    # set the url
    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    # set auth headers
    auth_headers = {
        'Authorization': 'Basic {}'.format(key_secret),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    #print(auth_resp.status_code)

    if auth_resp.status_code == 403:
        print('403 code response!')
        print('Operation failed.')
    if auth_resp.status_code == 200:
        print('200 code response!')
        print('Operation successful retrieval of bearer token.')
        bearer_token = auth_resp.json()['access_token']
        try:
            f = open(bearertokenfile, 'w')
            print('')
            print('\tSetting output file,', bearertokenfile)
            print('')
        except:
            print("\tFailed to open output file!")
            f.close()
        f.write(bearer_token)
    return

def setBearer():
    global bearertoken
    g = open('conf/bearer.token')
    bearertoken = g.readline()
    print('Bearer token imported successfully.')
    return

'''
Searching for the tweets.
http://benalexkeen.com/interacting-with-the-twitter-api-using-python/
https://dev.twitter.com/rest/reference/get/search/tweets
'''
def search():
    '''
    Pull search terms in from search-terms.ini
        [q]
        [result-type]
        [count]
    '''
    terms = configparser.ConfigParser()
    terms.read('conf/search.ini')

    search_headers = {
        'Authorization': 'Bearer {}'.format(bearertoken)
    }

    search_params = {
        'q':            terms['q']['value'],
        'result_type':  terms['result_type']['value'],
        'count':        terms['count']['value'],
        'lang': 'en' # Only returns English results. This can be removed.
    }

    search_url = '{}1.1/search/tweets.json'.format(base_url)
    print('Executing search...')
    print('---------------------------------------')
    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    tweet_data = search_resp.json()
    '''
    Prints all relevant data for keys and values. This can help inform the data you want to return. Examples are:
        created_at
        id_str
        text
        entities: hashtags, indices, symbols, user_mentions, etc
        user: id, id_str, name, screen_name, location, description, url, followers_count, friends_count, listed_count, created_at, favourites_count, etc.
        source
        geo_enabled
        lang
        profile_image_url_https
        profile_banner_url
        possibly_sensitive
        
    For multi-part (nested dictionary values, in python-speak) attributes, usage is print(x['top level']['next level']) like x['user']['id_str']
    Careful of using id as it is type int, not str
    '''
    # for key in tweet_data['statuses']:
    #     print (key)
    returnDataNotLabeled(tweet_data)
    return

def returnDataLabeled(tweet_data):
    for x in tweet_data['statuses']:
        try:
            print('User (screen_name, name, id): ' + x['user']['screen_name'] + '\t|\t' + x['user']['name'] + '\t|\t' + x['user']['id_str'])
            print('\nText is: ' + x['text'] + '\n')
            print('Source is: ' + x['source'] + '\n')
        except TypeError:
            print('Type error.')
        except KeyError:
            print('Key error.')
        print('---------------------------------------')
    return

def returnDataNotLabeled(tweet_data):
    for x in tweet_data['statuses']:
        try:
            print(x['user']['screen_name'] + '\t|\t' + x['user']['name'] + '\t|\t' + x['user']['id_str'])
            print(x['text'] + '\n')
            print(x['source'] + '\n')
        except TypeError:
            print('Type error.')
        except KeyError:
            print('Key error.')
        print('---------------------------------------')
    return

def oauthFlow():

    '''Steps:

    A.) Consumer requests REQUEST TOKEN
    B.) Service provider grants REQUEST TOKEN
    C.) Consumer directs user to service provider
    D.) Service provider directs user to consumer
    E.) Consumer requests ACCESS TOKEN
    F.) Service provider grants ACCESS TOKEN
    G.) Consumer Accesses Protected Resources

    Contents of OAUTH1 request:

        oauth_consumer_key
        oauth_signature_method
        oauth_signature
        oauth_timestamp
        oauth_nonce
        oauth_version (optional)
        oauth_callback
    '''

    conf = configparser.ConfigParser()
    conf.read('conf/key-conf.ini')
    if conf:
        print('Loaded conf.ini')
    else:
        print('Did not load configuration.')

    twconsumer_key = conf['twitter-consumer-api-key']['value']
    twconsumer_secret = conf['twitter-consumer-secret']['value']
    twaccesstoken = conf['twitter-access-token']['value']
    twaccesstokensecret = conf['twitter-access-token-secret']['value']

    searchconf = configparser.ConfigParser()
    searchconf.read('conf/search.ini')
    if conf:
        print('Loaded search.ini')
    else:
        print('Did not load search configuration.')

    # The easy way.
    search_param = searchconf['param']['value']
    oauth1_auth = OAuth1(twconsumer_key, twconsumer_secret, twaccesstoken, twaccesstokensecret)
    searchurl = 'https://api.twitter.com/1.1/statuses/user_timeline.json' + search_param
    print (searchurl)
    r = requests.get(searchurl, auth=oauth1_auth)

    if r.json():
        for tweet in r.json():
            print('------------------')
            print(tweet['text'])

    # The hard way.

    # A.) Consumer requests REQUEST TOKEN - documented here: https://developer.twitter.com/en/docs/basics/authentication/api-reference/authenticate

    requestTokenURL = 'https://api.twitter.com/oauth/authenticate'

    # B.) Service provider grants REQUEST TOKEN
    # C.) Consumer directs user to service provider
    # D.) Service provider directs user to consumer
    # E.) Consumer requests ACCESS TOKEN
    # F.) Service provider grants ACCESS TOKEN
    # G.) Consumer Accesses Protected Resources

    return

def main():
    if bearerExists() == False:
        b64key = readConf()
        generateBearer(b64key)
    setBearer()
    #search() #Search is based on search() which will return data as specified in returnDataLabeled or returnDataNotLabeled as selected.
    oauthFlow()

    return

main()

