import configparser
import requests
import base64
from requests_oauthlib import OAuth1

def oauthFlow():
    conf = configparser.ConfigParser()
    conf.read('../conf/key-conf.ini')
    if conf:
        print('Loaded conf.ini')
    else:
        print('Did not load configuration.')

    twconsumer_key          = conf['twitter-consumer-api-key']['value']
    twconsumer_secret       = conf['twitter-consumer-secret']['value']
    twaccesstoken           = conf['twitter-access-token']['value']
    twaccesstokensecret     = conf['twitter-access-token-secret']['value']

    '''
    
    Contents of OAUTH1 request:
    
        oauth_consumer_key
        oauth_signature_method
        oauth_signature
        oauth_timestamp
        oauth_nonce
        oauth_version (optional)
        oauth_callback
        
    '''
    '''Steps:

    A.) Consumer requests REQUEST TOKEN
    B.) Service provider grants REQUEST TOKEN
    C.) Consumer directs user to service provider
    D.) Service provider directs user to consumer
    E.) Consumer requests ACCESS TOKEN
    F.) Service provider grants ACCESS TOKEN
    G.) Consumer Accesses Protected Resources

    '''
    searchconf = configparser.ConfigParser()
    searchconf.read('../conf/search.ini')
    if conf:
        print('Loaded search.ini')
    else:
        print('Did not load search configuration.')

    # The easy way.
    search_param            = searchconf['param']['value']
    oauth1_auth = OAuth1(twconsumer_key,twconsumer_secret,twaccesstoken,twaccesstokensecret)

    r = requests.get('https://api.twitter.com/1.1/statuses/user_timeline.json'+ search_param, auth=oauth1_auth)

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


def main():
    oauthFlow()
    return



main()