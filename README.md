#Twitter API Searching


### Author

oBreak ([email](mailto:obreakemail@gmail.com))

### Version

0.3

### First time setup

First, create an application at apps.twitter.com. This is required to get a valid ID
and secret in order to authenticate via OAuth to the Twitter API. Note, this requires
that you have valid twitter credentials. A real or throwaway account is fine.

Also requires Python 3.x installed with modules `configparser`, `requests_oauthlib` and `requests` installed.

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
The app will then return the relevant data for those tweets.
 
Output will be dropped in the `/out/` folder and logs of the application
working (to include OAuth, searching, variable values, etc.) will
go to the `/debug/` folder with a timestamp.

##### Example debug log

```main() function start.
keyImport() function start.
	Loaded key-conf.ini
searchConfigImport() function start.
bearerExists() function start.
	Bearer token exists in /conf/ directory. Importing...
setBearer() function start.
	Using bearer infile, conf/bearer.token
	Bearer token imported successfully.
oauthFlow() function start.
app_only_auth_search() function start.
	Executing search using Application-only (OAUTH2) Authentication...
	---------------------------------------
	No errors in app_only_auth_search().
returnDataNotLabeled() function start.
debugOut() function start.
```

##### Example out log

```
tesla_bruh	|	🇬🇭Rakim Jnr🇧🇪	|	447078017
@Bc_blackchrome I choose both, if there's ever a fight, I sit them down and tell them that though I love them deepl… https://t.co/kkpN0xDKLX

https://twitter.com/tesla_bruh/status/1034813682981715968
<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>

---------------------------------------
FettGeo	|	Elric the Damned	|	763507025556934656
RT @temp_worker: Must read regarding $TSLA part shortage @Trumpery45.
Rear ended Model S waiting 5.5 months and counting for parts while ow…

https://twitter.com/FettGeo/status/1034813673049489408
<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>

---------------------------------------

```

##### Preserved output (no longer relevant)
 
...as specified in the below section (both are found within the search() 
function). This section subject to change but will be preserved in the 
readme (for now).

    tweet_data = search_resp.json()
    for x in tweet_data['statuses']:
        print('User screenname is: ' + x['user']['screen_name'])
        print('Text is: ' + x['text'] + '\n')
        print('Source is: ' + x['source'] + '\n')
        print('---------------------------------------')
