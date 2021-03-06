#!/usr/bin/env python
'''
Helpful reference: http://benalexkeen.com/interacting-with-the-twitter-api-using-python/
which spawned some of this.
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


def bearerExists():
    debug.append('bearerExists() function start.')
    x = False
    try:
        # Open bearer file
        g = open(bearertokenfile)
        x = True
        for y in g.readlines():
            if y == '':
                x = False
                debug.append('\tError, bearer token is empty, regenerating.')
    except FileNotFoundError:
        # Send error
        debug.append('\tError, bearer token file not found during bearerExists() verification.')
        x = False
    if x == True:
        debug.append('\tBearer token exists in /conf/ directory. Importing...')
    return x

'''
readConf() is established to read the configuration file for the relevant keys and secrets in order to 
retrieve the bearer token (This is needed for application-only requests).

Returns the b64_encoded_key that needs to be sent with the request for the bearer token.

The bearer token should be STORED, not requested with each request.
'''

def readConf():
    debug.append('readConf() function start.')
    global conf
    global consumerapikey
    global consumersecret
    global accesstoken
    global accesstokensecret
    global builtheader
    global encodedkey

    conf = configparser.ConfigParser()
    conf.read('conf/key-conf.ini')

    twconsumer_key          = conf['oauth_keys']['twitter-consumer-api-key']
    twconsumer_secret       = conf['oauth_keys']['twitter-consumer-secret']
    twaccesstoken           = conf['oauth_keys']['twitter-access-token']
    twaccesstokensecret     = conf['oauth_keys']['twitter-access-token-secret']
    encodedkey              = '{}:{}'.format(twconsumer_key, twconsumer_secret).encode('ascii')
    b64_encoded_key         = base64.b64encode(encodedkey)
    b64_encoded_key         = b64_encoded_key.decode('ascii')
    print('b64_encoded_key is: ' + b64_encoded_key)
    return b64_encoded_key

# Gets the bearer token, if it's not already stored. Note there are rate limitations on how often this can be done.
# This following the Oauth2 authentication flow.
def generateBearer(x):
    debug.append('generateBearer() function start.')
    import configparser
    import requests
    import base64

    conf = configparser.ConfigParser()
    conf.read('conf/key-conf.ini')

    # # import relevant keys and secrets
    # twconsumer_key          = conf['oauth_keys']['twitter-consumer-api-key']
    # twconsumer_secret       = conf['oauth_keys']['twitter-consumer-secret']
    # twaccesstoken           = conf['oauth_keys']['twitter-access-token']
    # twaccesstokensecret     = conf['oauth_keys']['twitter-access-token-secret']
    #
    # # base64 encode the consumer key:secret pair
    # key_secret = base64.urlsafe_b64encode('{}:{}'.format(twconsumer_key, twconsumer_secret).encode('UTF-8')).decode(
    #     'UTF-8')

    # set the url
    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    # set auth headers
    auth_headers = {
        'Authorization': 'Basic {}'.format(x),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    debug.append('\t'+auth_headers)
    debug.append('\t'+str(auth_resp.status_code))

    if auth_resp.status_code == 403:
        debug.append('403 code response!')
        debug.append('Operation failed.')
    if auth_resp.status_code == 200:
        debug.append('200 code response!')
        debug.append('Operation successful, retrieval of bearer token complete.')
        bearer_token = auth_resp.json()['access_token']
        #print(bearer_token)
        try:
            f = open(bearertokenfile, 'w')
            debug.append('\tSetting output file,' + bearertokenfile)
        except:
            debug.append("\tFailed to open output file!")
            f.close()
        try:
            f.write(bearertoken)
        except ValueError:
            debug.append('\tCould not write to bearer.token file.')
    return

def setBearer():
    debug.append('setBearer() function start.')
    global bearertoken
    try:
        g = open(bearertokenfile, 'r')
        debug.append('\tUsing bearer infile, ' + bearertokenfile)
        bearertoken = g.readline()
        g.close()
        debug.append('\tBearer token imported successfully.')
    except:
        print("Failed to open infile!")
    return

'''
Searching for the tweets.
http://benalexkeen.com/interacting-with-the-twitter-api-using-python/
https://dev.twitter.com/rest/reference/get/search/tweets
'''
def app_only_auth_search(): # Uses OAuth2
    debug.append('app_only_auth_search() function start.')
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
        'q':            terms['oauth2_params']['q'],
        'result_type':  terms['oauth2_params']['result_type'],
        'count':        terms['oauth2_params']['count'],
        'lang': 'en' # Only returns English results. This can be removed.
    }

    search_url = '{}1.1/search/tweets.json'.format(base_url)
    debug.append('\tExecuting search using Application-only (OAUTH2) Authentication...')
    debug.append('\t---------------------------------------')
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
    try:
        print(tweet_data['errors'])
    except:
        debug.append('\tNo errors in app_only_auth_search().')
    # for key in tweet_data['statuses']:
    #     print (key)
    returnDataNotLabeled(tweet_data)
    return


def app_only_auth_fulldata(x):  # Uses OAuth2
    debug.append('app_only_auth_fulldata() function start.')
    status_id = x
    '''
    Pull search terms in from search.ini
    '''
    terms = configparser.ConfigParser()
    terms.read('conf/search.ini')

    search_headers = {
        'Authorization': 'Bearer {}'.format(bearertoken)
    }
    debug.append(search_headers)
    search_url = ('https://api.twitter.com/1.1/statuses/show.json?id=' + status_id)
    debug.append('\t' + search_url)
    debug.append('\tExecuting search using Application-only (OAUTH2) Authentication...')
    debug.append('\t---------------------------------------')
    search_resp = requests.get(search_url, headers=search_headers)
    debug.append('\tResponse code ' + str(search_resp.status_code))
    tweet_data = search_resp.json()
    keys = []
    for thing in tweet_data:
        keys.append(thing)
    for key in keys:
        key = str(key)
        try:
            tweets.append('-'*60)
            tweets.append(key)
            tweets.append(tweet_data[key])
        except KeyError:
            print('Did not work, key error in function app_only_auth_fulldata()')
    return


def morning_coffee():  # Uses OAuth2
    debug.append('morning_coffee() function start.')
    '''
    Pull search terms in from morning-filter.ini
        [q1]
        [q1]
        [q3]
        [q4]
        [q5]
        [result-type]
        [count]
    '''
    terms = configparser.ConfigParser()
    try:
        terms.read('conf/morning-filter.ini')
    except:
        debug.append('Failed to load morning-filter.ini to terms.')
    search_headers = {
        'Authorization': 'Bearer {}'.format(bearertoken)
    }
    for i in range(1,4): # Where 4 is ONE MORE than how many items you want to search on.
        search_params = {
            'q': terms['oauth2_params']['q'+str(i)],
            'result_type': terms['oauth2_params']['result_type'],
            'count': terms['oauth2_params']['count'],
            'lang': 'en'  # Only returns English results. This can be removed.
        }

        search_url = '{}1.1/search/tweets.json'.format(base_url)
        debug.append('\tExecuting search using Application-only (OAUTH2) Authentication...')
        debug.append('\t---------------------------------------')
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
        try:
            print(tweet_data['errors'])
        except:
            debug.append('\tNo errors in app_only_auth_search(). for term ' + str(i))
        # for key in tweet_data['statuses']:
        #     print (key)
        returnDataNotLabeled(tweet_data)
        # print(str(i))
        tweets.append('\n' + '*' * 40)
        tweets.append('End of search on criteria set in q'+str(i))
        tweets.append('*' * 40 + '\n')
    return

def returnDataLabeled(tweet_data):
    debug.append('\treturnDataLabeled() function start.')
    for x in tweet_data['statuses']:
        try:
            tweets.append('User (screen_name, name, id): ' + x['user']['screen_name'] + '\t|\t' + x['user']['name'] + '\t|\t' + x['user']['id_str'])
            tweets.append('\nText is: ' + x['text'] + '\n')
            tweets.append('https://twitter.com/' + x['user']['screen_name']+'/status/'+x['id_str'])
            tweets.append('Source is: ' + x['source'] + '\n')
        except TypeError:
            debug.append('\tType error.')
        except KeyError:
            debug.append('\tKey error.')
        tweets.append('---------------------------------------')
    return

def returnDataNotLabeled(tweet_data):
    debug.append('\treturnDataNotLabeled() function start.')
    for x in tweet_data['statuses']:
        try:
            tweets.append(x['user']['screen_name'] + '\t|\t' + x['user']['name'] + '\t|\t' + x['user']['id_str'])
            tweets.append(x['text'] + '\n')
            tweets.append('https://twitter.com/' + x['user']['screen_name']+'/status/'+x['id_str'])
            tweets.append(x['source'] + '\n')
        except TypeError:
            debug.append('\tType error.')
        except KeyError:
            debug.append('\tKey error.')
        tweets.append('---------------------------------------')
    return

# Created to set keys as global variables to pass between functions. Should run at the beginning of the program.
def keyImport():
    debug.append('keyImport() function start.')
    global twconsumer_key
    global twconsumer_secret
    global twaccesstoken
    global twaccesstokensecret

    keyconf = configparser.ConfigParser()
    keyconf.read('conf/key-conf.ini')
    if keyconf:
        debug.append('\tLoaded key-conf.ini')
    else:
        debug.append('\tDid not load configuration from key-conf.ini.')

    twconsumer_key          = keyconf['oauth_keys']['twitter-consumer-api-key']
    twconsumer_secret       = keyconf['oauth_keys']['twitter-consumer-secret']
    twaccesstoken           = keyconf['oauth_keys']['twitter-access-token']
    twaccesstokensecret     = keyconf['oauth_keys']['twitter-access-token-secret']

def searchConfigImport():
    debug.append('searchConfigImport() function start.')
    global searchconf
    searchconf = configparser.ConfigParser()
    searchconf.read('conf/search.ini')
    search_param = searchconf['oauth_params']['param']
    return

def oauthFlow():
    debug.append('oauthFlow() function start.')
    global oauth1_auth
    '''
    Steps:

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

    searchconf = configparser.ConfigParser()
    searchconf.read('conf/search.ini')

    # The easy way.
    oauth1_auth = OAuth1(twconsumer_key, twconsumer_secret, twaccesstoken, twaccesstokensecret)

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

def oauth1selfsearch():
    debug.append('oauth1selfsearch() function start.')
    search_param = searchconf['oauth_params']['param']
    searchurl = 'https://api.twitter.com/1.1/statuses/user_timeline.json' + search_param
    debug.append('\t' + searchurl)
    r = requests.get(searchurl, auth=oauth1_auth)
    for thing in r:
        print (thing)
    debug.append(oauth1_auth)
    # tweet_data = r.json()
    # if tweet_data:
    #     for tweet in tweet_data:
    #         try:
    #             tweets.append('-'*60)
    #             tweets.append(tweet['text'])
    #             tweets.append('\nid_str: ' + tweet['id_str'])
    #         except TypeError:
    #             debug.append('Type error received in oauth1selfsearch(); this may be caused by searching for a '
    #                          'username that does not exist or because authentication failed.')
    return

'''
Note you cannot post more than 300 per user or 300 per app. Combined limit for POST statuses/update
endpoint. Can only post 300 tweets or retweets during a 3 hour period.

Creates tweet based on searchconf['oauth_params']['statusPost']
'''
def oauth1createtweet():
    debug.append('oauth1createtweet() function start.')
    statusPost = searchconf['oauth_params']['statusPost']
    posturl = 'https://api.twitter.com/1.1/statuses/update.json?status=' + statusPost
    r = requests.post(posturl, auth=oauth1_auth)
    debug.append('\tStatus code for posting tweet was code: ' + str(r.status_code))
    return

'''
Creates tweet based on searchconf['oauth_params']['destroy_status_id']
'''
def oauth1deletetweet():
    debug.append('oauth1deletetweet() function start.')
    destroy_status_id = searchconf['oauth_params']['destroy_status_id']
    destroyurl = 'https://api.twitter.com/1.1/statuses/destroy/' + destroy_status_id + '.json'
    r = requests.post(destroyurl, auth=oauth1_auth)
    debug.append('\tStatus code for deleting tweet with id ' + destroy_status_id + ' was code: ' + str(r.status_code))
    return

def debugOut():
    debug.append('debugOut() function start.')
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
    debug.append('tweetsOutPrint() function start.')
    for i in tweets:
        print(i)
    return

def tweetsOutFile():
    debug.append('tweetsOutFile() function start.')
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
        try:
            f.write(str(j))
            f.write(lineBreaks)  # This is to add a new line at the end of each line of the log or text file.
            n = n + 1
            if n % 100 == 0:
                print('\tWriting outputs: ' + str(n) + ' lines complete.')
            else:
                pass
        except UnicodeEncodeError:
            debug.append("Unicode Encoding Error in tweet.\n")
            f.write("Unicode Encoding Error, cannot display result.\n")
    else:
        pass
    print('\tOutput complete: ' + str(n) + ' lines written.')
    print('\n')
    return

def main():
    debug.append('main() function start.')
    global bearertoken
    # Set up OAuth1 and OAuth2 flows.
    keyImport()
    searchConfigImport()
    if bearerExists() == False:
        debug.append('\tBearer does not exist, entering bearer generation workflow.')
        b64key = readConf()
        generateBearer(b64key)
    setBearer()
    oauthFlow()

    # Interaction functions
    # app_only_auth_search()
    # app_only_auth_fulldata(searchconf['oauth2_params']['tweet_id_fulldata'])   # x is the tweet status
    # oauth1selfsearch()
    # oauth1createtweet()
    # oauth1deletetweet()
    morning_coffee()

    # Writing Results
    debugOut()
    # tweetsOutPrint()
    tweetsOutFile()
    return

main()

