import configparser
import requests
import base64
import os
import sys



conf = configparser.ConfigParser()
conf.read('../conf/key-conf.ini')

twconsumer_key = keyconf['oauth_keys']['twitter-consumer-api-key']
twconsumer_secret = keyconf['oauth_keys']['twitter-consumer-secret']
twaccesstoken = keyconf['oauth_keys']['twitter-access-token']
twaccesstokensecret = keyconf['oauth_keys']['twitter-access-token-secret']

print(twconsumer_key)
print(twconsumer_secret)
print(twaccesstoken)
print(twaccesstokensecret)

# base64 encode the consumer key:secret pair
key_secret          = base64.urlsafe_b64encode('{}:{}'.format(twconsumer_key, twconsumer_secret).encode('UTF-8')).decode('UTF-8')

# set the url
base_url            = 'https://api.twitter.com/'
auth_url            = '{}oauth2/token'.format(base_url)

# set auth headers
auth_headers = {
    'Authorization': 'Basic {}'.format(key_secret),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {
    'grant_type': 'client_credentials'
}

auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
# print(auth_resp.status_code)




# os.sys('curl -H "Authorization: token OAUTH-TOKEN" https://api.github.com')

# r = requests.get('https://api.github.com/timeline.json')
# print(r.status_code)

# curl -i -X POST -H "Authorization: Basic Encoded-TOKEN" -d "grant_type=client_credentials" "https://api.twitter.com/oauth2/token"