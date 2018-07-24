#Twitter API Searching

### Author

oBreak ([email](mailto:obreakemail@gmail.com))

### Version 

0.2

### First time setup

First, create an application at apps.twitter.com. This is required to get a valid ID
and secret in order to authenticate via OAuth to the Twitter API. Note, this requires
that you have valid twitter credentials. A real or throwaway account is fine.

Also requires Python 3.x installed with modules `configparser` and `requests` installed.

##### Starting at the [Twitter App Creation Page](https://apps.twitter.com/app/new).

|Details            |Value          |
|:------------------|---------------|
Name of the app | Determine your own!
Description | For twitter research.
Website | https://placeholder.com
Callback URLs | <blank\>

##### Application Settings

|Object                 |                       Value|
|-----------------------|----------------------------|
|Consumer Key (API Key) |NEEDED FOR THIS TO WORK     |
|Consumer Secret        |NEEDED FOR THIS TO WORK     |

##### Created access token:

|Object                 |                       Value|
|-----------------------|----------------------------|
|Access Token	        |Example                     |
|Access Token Secret    |Example                     |

Real keys and tokens will be found in the `/conf/`
directory after adding them to the appropriate `key-conf.ini` file.

After creating the `key-conf.ini` modeled after the `key-conf-example.ini` included in
this repository with the appropriate data, the program should automatically
extract the keys and request a bearer token. This bearer token will be saved
as `bearer.token` in the `/conf/` directory and will be passed for future requests.

### Usage

Currently the app is set to search based on the terms in the `/conf/search.ini`. Edit 
the `/conf/public-search-terms.ini` and save as `/conf/search.ini` to whatever you would 
prefer to search for. Search parameter selection code (this can be edited to provide
other search terms as desired):

    search_params = {
        'q':            terms['q']['value'],
        'result_type':  terms['result_type']['value'],
        'count':        terms['count']['value']
    }

Where value will be stored in the config as something like 'Legos' or 'Popcorn'. 
The app will then return the relevant data for those tweets as specified
in the below section (both are found within the search() function). This
section subject to change but will be preserved in the readme (for now).

    tweet_data = search_resp.json()
    for x in tweet_data['statuses']:
        print('User screenname is: ' + x['user']['screen_name'])
        print('Text is: ' + x['text'] + '\n')
        print('Source is: ' + x['source'] + '\n')
        print('---------------------------------------')
