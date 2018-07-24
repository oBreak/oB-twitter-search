import configparser
import requests
import base64

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
    encodedkey              = '{}:{}'.format(twconsumer_key, twconsumer_secret).encode('ascii')
    b64_encoded_key         = base64.b64encode(encodedkey)
    b64_encoded_key         = b64_encoded_key.decode('ascii')

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





main()