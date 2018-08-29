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
PistachiosUK	|	Pistachios_UK	|	266500563
100g of Wonderful Almonds is a healthy snack full of nutrients including Vitamin E, contributing to the protection… https://t.co/vQuTeaKCZ6

https://twitter.com/PistachiosUK/status/1034813926133907456
<a href="https://about.twitter.com/products/tweetdeck" rel="nofollow">TweetDeck</a>

---------------------------------------
Seahawk1994	|	Seahawk Not Down	|	721631865866711040
@WozzieWasEre @discordspies For being "activated", their almonds look like they're past their expiration date.

https://twitter.com/Seahawk1994/status/1034813900045393920
<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>

---------------------------------------
Bryson_Dowler	|	Bryclops @DragonCon	|	567777024
RT @thedad: God: what are they doing down there?
Angel: they are making milk from almonds
God: what?! I gave them, like, 8 animals to get m…

https://twitter.com/Bryson_Dowler/status/1034813854449127425
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
