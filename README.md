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
mariamoralescr	|	Maria Morales 🇨🇷	|	710994290
RT @EveningStandard: K-pop boyband BTS have broken Taylor Swift's record for the biggest music video debut on YouTube https://t.co/S0YK2eah…

https://twitter.com/mariamoralescr/status/1034813006260170752
<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>

---------------------------------------
jeddddddi	|	jedi	|	952475242676436992
RT @brando_swift: Must Protect Taylor Swift At All Costs™ Squad

https://twitter.com/jeddddddi/status/1034813001935740928
<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>

---------------------------------------
liamchxnel	|	sebastian	|	742716541704245248
RT @iknowplacesmp3: 🗣| UPDATE|| My sources say that Taylor Swift was recently in Nashville, filming. Is it for Gorgeous? Getaway Car? I Did…

https://twitter.com/liamchxnel/status/1034812974958108672
<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>

---------------------------------------
HaleyRatica	|	Haley Ratica wants to meet Taylor	|	589534481
RT @mashleighh: Taylor Swift deserves to feel &amp; be safe like every other person. Her fame shouldn’t change that. Please speak up if you see…

https://twitter.com/HaleyRatica/status/1034812973401948160
<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>

---------------------------------------
NUDi4RizKb0Zjjo	|	💜보라해💜	|	871247419635245056
RT @EveningStandard: K-pop boyband BTS have broken Taylor Swift's record for the biggest music video debut on YouTube https://t.co/S0YK2eah…

https://twitter.com/NUDi4RizKb0Zjjo/status/1034812953982251008
<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>

---------------------------------------
empireofmovies	|	marie 🌷	|	310729533
RT @musicnewsfact: Taylor Swift held a moment of silence for Aretha Franklin last night at her Detroit show at Ford Field. 😭❤ https://t.co/…

https://twitter.com/empireofmovies/status/1034812929420533760
<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>

---------------------------------------
sevenwhalien52	|	☆*🌙💜BTS 💜🌙*☆	|	892198596359200769
RT @wmag: #BTS reportedly set a new YouTube record for the highest number of views in 24 hours. https://t.co/upxf69vJnu #Idol

https://twitter.com/sevenwhalien52/status/1034812927675645953
<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>

---------------------------------------
JosefaQuiroz16	|	Josefa Quiroz	|	891849946189750277
RT @CNN: Korean pop group BTS beats Taylor Swift's record for biggest YouTube debut with the music video for its song "Idol" https://t.co/G…

https://twitter.com/JosefaQuiroz16/status/1034812916791500806
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
