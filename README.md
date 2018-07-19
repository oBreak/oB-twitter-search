#Twitter API Searching

### First time setup

First, create an application at apps.twitter.com. This is required to get a valid ID
and secret in order to authenticate via OAuth to the Twitter API.

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
directory after adding them to the appropriate conf.ini file.

After creating the conf.ini modeled after the conf-example.ini included in
this repository with the appropriate data, the program should automatically
extract the keys and request a bearer token. This bearer token will be saved
as bearer.token in the /conf/ directory and will be passed for future requests.

### Usage

Currently the app is set to search based on the terms below. Edit these
to whatever you would prefer to search for:

    search_params = {
        'q': 'Taylor Swift',
        'result_type': 'recent',
        'count': 2
    }

The app will then return the relevant data for those tweets as specified
in the below section (both are found within the search() function).

    tweet_data = search_resp.json()
    for x in tweet_data['statuses']:
        print('User is: ' + 'sample')
        print('Text is: ' + x['text'] + '\n')
        print('Source is: ' + x['source'] + '\n')
        print('---------------------------------------')
