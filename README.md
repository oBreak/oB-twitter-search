#Twitter API Searching

### First time setup

First, create an application at apps.twitter.com. This is required to get a valid ID
and secret in order to authenticate via OAuth to the Twitter API.

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

Real keys and tokens will be found in the /conf/ 
directory after adding them to the appropriate key-conf.ini file.

After creating the conf.ini modeled after the conf-example.ini included in
this repository with the appropriate data, the program should automatically
extract the keys and request a bearer token. This bearer token will be saved
as `bearer.token` in the `/conf/` directory and will be passed for future requests.

### Usage

Currently the app is set to search based on the terms in the `/conf/search.ini`. Edit 
the `/conf/search-terms.ini` and save as `/conf/search.ini` to whatever you would 
prefer to search for. Search parameter selection code (this can be edited to provide
other search terms as desired):

    search_params = {
        'q':            terms['q']['value'],
        'result_type':  terms['result_type']['value'],
        'count':        terms['count']['value']
    }

The app will then return the relevant data for those tweets as specified
in the below section (both are found within the search() function). This
section subject to change but will be preserved in the readme (for now).

    tweet_data = search_resp.json()
    for x in tweet_data['statuses']:
        print('User is: ' + 'sample')
        print('Text is: ' + x['text'] + '\n')
        print('Source is: ' + x['source'] + '\n')
        print('---------------------------------------')



##### Notes to self:

Add additional programmatic support for searching for other relevant tweet_data 
components, or at least documentation on how to do it.

##### Roadmap:

- Add livestream for specific tweet types. Maybe add in an email of top 10 hits per day or something.
- Add filter support for things that I'd want to see, something like "mentions me" or "damages my company's brand"
- Add username to returned results
- Add userID to returned results
- Add user PICTURE to returned results... not sure if I want to do this yet.
- etc.
