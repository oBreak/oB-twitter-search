#!/usr/bin/env python
'''
Helpful reference: http://benalexkeen.com/interacting-with-the-twitter-api-using-python/
'''

import os
import configparser
import requests
import base64
import time
from requests_oauthlib import OAuth1

payload                     = {'key': 'val'}
builtheader                 = ''
bearertokenfile             = 'conf/bearer.token'
bearertoken                 = ''
base_url                    = 'https://api.twitter.com/'
tweets                      = []
debug                       = []

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
        debug.append('Error, bearer token not found.')
        x = False
        pass
    if x == True:
        debug.append('Bearer token exists in /conf/ directory. Importing...')
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
        debug.append('403 code response!')
        debug.append('Operation failed.')
    if auth_resp.status_code == 200:
        debug.append('200 code response!')
        debug.append('Operation successful retrieval of bearer token.')
        bearer_token = auth_resp.json()['access_token']
        try:
            f = open(bearertokenfile, 'w')
            debug.append('')
            debug.append('\tSetting output file,', bearertokenfile)
            debug.append('')
        except:
            debug.append("\tFailed to open output file!")
            f.close()
        f.write(bearer_token)
    return

def setBearer():
    global bearertoken
    g = open('conf/bearer.token')
    bearertoken = g.readline()
    debug.append('Bearer token imported successfully.')
    return

'''
Searching for the tweets.
http://benalexkeen.com/interacting-with-the-twitter-api-using-python/
https://dev.twitter.com/rest/reference/get/search/tweets
'''
def appOnlyAuthSearch(): # Uses OAuth2
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
    debug.append('Executing search using Application-only (OAUTH2) Authentication...')
    debug.append('---------------------------------------')
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
            tweets.append('User (screen_name, name, id): ' + x['user']['screen_name'] + '\t|\t' + x['user']['name'] + '\t|\t' + x['user']['id_str'])
            tweets.append('\nText is: ' + x['text'] + '\n')
            tweets.append('https://twitter.com/' + x['user']['screen_name']+'/status/'+x['id_str'])
            tweets.append('Source is: ' + x['source'] + '\n')
        except TypeError:
            debug.append('Type error.')
        except KeyError:
            debug.append('Key error.')
        tweets.append('---------------------------------------')
    return

def returnDataNotLabeled(tweet_data):
    for x in tweet_data['statuses']:
        try:
            tweets.append(x['user']['screen_name'] + '\t|\t' + x['user']['name'] + '\t|\t' + x['user']['id_str'])
            tweets.append(x['text'] + '\n')
            tweets.append('https://twitter.com/' + x['user']['screen_name']+'/status/'+x['id_str'])
            tweets.append(x['source'] + '\n')
        except TypeError:
            debug.append('Type error.')
        except KeyError:
            debug.append('Key error.')
        tweets.append('---------------------------------------')
    return

# Created to set keys as global variables to pass between functions. Should run at the beginning of the program.
def keyImport():
    global twconsumer_key
    global twconsumer_secret
    global twaccesstoken
    global twaccesstokensecret

    keyconf = configparser.ConfigParser()
    keyconf.read('conf/key-conf.ini')
    if keyconf:
        debug.append('Loaded key-conf.ini')
    else:
        debug.append('Did not load configuration from key-conf.ini.')

    twconsumer_key = keyconf['twitter-consumer-api-key']['value']
    twconsumer_secret = keyconf['twitter-consumer-secret']['value']
    twaccesstoken = keyconf['twitter-access-token']['value']
    twaccesstokensecret = keyconf['twitter-access-token-secret']['value']

def searchConfigImport():
    global searchconf
    searchconf = configparser.ConfigParser()
    searchconf.read('conf/search.ini')
    search_param = searchconf['param']['value']
    return

def oauthFlow():
    global oauth1_auth
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

    # keyconf = configparser.ConfigParser()
    # keyconf.read('conf/key-conf.ini')
    # if keyconf:
    #     print('Loaded key-conf.ini')
    # else:
    #     print('Did not load configuration.')

    searchconf = configparser.ConfigParser()
    searchconf.read('conf/search.ini')

    # The easy way.
    oauth1_auth = OAuth1(twconsumer_key, twconsumer_secret, twaccesstoken, twaccesstokensecret)

    # destroy_status_id = searchconf['destroy_status_id']['value']
    # destroyurl = 'https://api.twitter.com/1.1/statuses/destroy/' + destroy_status_id + '.json'
    # r = requests.post(destroyurl, auth=oauth1_auth)
    # if r.json():
    #     for thing in r.json():
    #         print(thing)

    # The hard way.

    # A.) Consumer requests REQUEST TOKEN - documented here: https://developer.twitter.com/en/docs/basics/authentication/api-reference/authenticate

    # requestTokenURL = 'https://api.twitter.com/oauth/authenticate'

    # B.) Service provider grants REQUEST TOKEN
    # C.) Consumer directs user to service provider
    # D.) Service provider directs user to consumer
    # E.) Consumer requests ACCESS TOKEN
    # F.) Service provider grants ACCESS TOKEN
    # G.) Consumer Accesses Protected Resources
    return

def oauth1search():
    search_param = searchconf['param']['value']
    searchurl = 'https://api.twitter.com/1.1/statuses/user_timeline.json' + search_param
    debug.append(searchurl)
    r = requests.get(searchurl, auth=oauth1_auth)

    if r.json():
        for tweet in r.json():
            tweets.append('-'*60)
            tweets.append(tweet['text'])
            tweets.append('\nid_str: ' + tweet['id_str'])
    return

def debugOut():
    n = int(0)
    lineBreaks = str('\n')
    timestr = time.strftime("%Y%m%d-%H%M%S")
    debugfile = 'debug/debug-' + timestr + '.log'
    print(debugfile + ' created.')
    try:
        f = open(debugfile, 'w')
        print('')
        print('\tSetting debug file,', debugfile)
        print('')
    except:
        print("\tFailed to open debug file!")
        f.close()
    for j in debug:
        f.write(str(j))
        f.write(lineBreaks)  # This is to add a new line at the end of each line of the log or text file.
        n = n + 1
        if n % 100 == 0:
            print('\tWriting outputs: ' + str(n) + ' lines complete.')
        else:
            pass
    else:
        pass
    print('\tOutput complete: ' + str(n) + ' lines written.')
    print('\n')
    return

def tweetsOutPrint():
    for i in tweets:
        print(i)
    return

def tweetsOutFile():
    n = int(0)
    lineBreaks = str('\n')
    timestr = time.strftime("%Y%m%d-%H%M%S")
    outfile = 'out/out-' + timestr + '.log'
    print(outfile + ' created.')
    try:
        f = open(outfile, 'w')
        print('')
        print('\tSetting outfile,', outfile)
        print('')
    except:
        print("\tFailed to open out file!")
        f.close()
    for j in tweets:
        f.write(str(j))
        f.write(lineBreaks)  # This is to add a new line at the end of each line of the log or text file.
        n = n + 1
        if n % 100 == 0:
            print('\tWriting outputs: ' + str(n) + ' lines complete.')
        else:
            pass
    else:
        pass
    print('\tOutput complete: ' + str(n) + ' lines written.')
    print('\n')
    return

def main():
    # Set up OAuth1 and OAuth2 flows.
    keyImport()
    searchConfigImport()
    if bearerExists() == False:
        b64key = readConf()
        generateBearer(b64key)
    setBearer()
    oauthFlow()

    # Search functions

    appOnlyAuthSearch()
    #oauth1search()

    # Writing Results

    debugOut()
    #tweetsOutPrint()
    tweetsOutFile()

    return

main()

