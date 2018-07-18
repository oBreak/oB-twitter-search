import configparser
import requests
import base64
import os
import sys

conf = configparser.ConfigParser()
conf.read('conf/conf.ini')

# import relevant keys and secrets
twconsumer_key        = conf['twitter-consumer-api-key']['value']
twconsumer_secret     = conf['twitter-consumer-secret']['value']
twaccesstoken         = conf['twitter-access-token']['value']
twaccesstokensecret   = conf['twitter-access-token-secret']['value']

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

# auth_headers = {
#     'Authorization: Basic ' + key_secret,
#     'Content-Type: application/x-www-form-urlencoded;charset=UTF-8'
# }

auth_data = {
    'grant_type': 'client_credentials'
}

print(auth_url)
print(auth_headers)
print(auth_data)

# auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
# print(auth_resp.status_code)

# os.sys('curl -H "Authorization: token OAUTH-TOKEN" https://api.github.com')

# r = requests.get('https://api.github.com/timeline.json')
# print(r.status_code)

# curl -i -X POST -H "Authorization: Basic Encoded-TOKEN" -d "grant_type=client_credentials" "https://api.twitter.com/oauth2/token"