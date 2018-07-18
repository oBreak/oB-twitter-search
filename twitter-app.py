#!/usr/bin/env python
'''
Helpful reference: http://benalexkeen.com/interacting-with-the-twitter-api-using-python/


'''

import os
import configparser
import requests
import base64

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
    conf.read('conf/conf.ini')

    twconsumer_key          = conf['twitter-consumer-api-key']['value']
    twconsumer_secret       = conf['twitter-consumer-secret']['value']
    twaccesstoken           = conf['twitter-access-token']['value']
    twaccesstokensecret     = conf['twitter-access-token-secret']['value']
    encodedkey              = '{}:{}'.format(twconsumer_key, twconsumer_secret).encode('ascii')
    b64_encoded_key         = base64.b64encode(encodedkey)
    b64_encoded_key         = b64_encoded_key.decode('ascii')
    return b64_encoded_key

# Gets the bearer token, if it's not already stored. Note there are rate limitations on how often this can be done.
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

    print(twconsumer_key)
    print(twconsumer_secret)
    print(twaccesstoken)
    print(twaccesstokensecret)

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
    search_headers = {
        'Authorization': 'Bearer {}'.format(bearertoken)
    }

    search_params = {
        'q': 'Taylor Swift',
        'result_type': 'recent',
        'count': 2
    }

    search_url = '{}1.1/search/tweets.json'.format(base_url)
    print('Executing search...')
    print('---------------------------------------')
    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    tweet_data = search_resp.json()
    for x in tweet_data['statuses']:
        print('User is: ' + 'sample')
        print('Text is: ' + x['text'] + '\n')
        print('Source is: ' + x['source'] + '\n')
#        print(x['user'] + '\n')
        print('---------------------------------------')
    return

def main():
    if bearerExists() == False:
        b64key = readConf()
        generateBearer(b64key)
    setBearer()
    search()
    return

main()

