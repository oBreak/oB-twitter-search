# Change Log

0.3 - TBD

- Created `oauth1selfsearch()` to do a list of last ten tweets of the user timeline. This is
for the user named in `search.ini` under `param=`.
- Created `oauth1createtweet()` to create tweets based on criteria in config file.
- Created `oauth1deletetweet()` to delete specified tweets.
- Edited configuration file to support new functions.
- Created `delete_ids.ini` file in the `/conf/` directory. This can store a collection of 
tweets to destroy. For example, run a filter on posted tweets and delete all tweets
that mention Taylor Swift because her people are coming after you. Intent is to have this
dynamically updated by the program based on some search criteria.
- Changelog, roadmap, and readme updated
- Renamed function to `app_only_auth_search()`
- Created `app_only_auth_fulldata()` to pull all data for a single tweet, integration with
the config files.
- Fixed errors in pulling the correct filename for the config file.
- Cleaned up output of debug file. Functions are now top level and messages within the
function are now tabbed in for easier reading. All functions now announce that they have
started within the debug output.


0.2 - 07/25/18 - The goal of this branch is to incorporate better
ways to search for data that is relevant to the user and to allow for twitter interactions,
where this could be defined pretty broadly. This does signal a change from research to
i/o, but the intent is to build up the research side (specificity, automation) while
enabling some automation for the interaction side as well. Changes:

- Readme and changelog updated to contain new changes and relevant data.
- Added prerequisite to download the requests_oauthlib module. This handles the Oauth1 
interaction.
- Added `oauthFlow()` function. This handles the Oauth1 interaction in passing the consumer
key and secret + the user key and secret.
- Added a small search to bring back a user timeline based on the parameters set in 
search.ini in the `param` value.
- Added `interaction-testing.py` in the `/resources/` folder used for testing the oauth1 
functionality outside of the context of the greater program. I think I will use this 
method for testing future features when I don't want to comment out a great deal of 
the program.
- Added `keyconf()` function to import the keys as global variables that can be passed 
around within the program.
- Removed some unused global variables.
- Split out the output into tweets list. This can then be printed with the `tweetsOut()` 
function. This will clear up the 'print' to just be app function stuff. This
might be followed by moving the app stuff to a debug log.
- Renamed `search()` to be more descriptive as `appOnlyAuthSearch()`
- Moved `[destroy_status_id]` into example search configuration
- Moved search configuration import to a separate function. This means that the 
oauth flow, the search config, and the searching itself are all now separately
callable.
- Created `filter.ini` file for relevant topics that I would want 
to call. This is not integrated into the main program yet.
- Added import for `time` module to timestamp files.
- Now debug and out files are created rather than printing to IDE
- Created example debug and out logs for github purposes.
- Successfully tested removing a tweet with destroy status id code.


0.1 - 07/24/18 - Completion of minimum viable script. There were a lot of changes so 
let's just call this the start version. Current features:
- Checks for stored bearer token (`/conf/bearer.token`)
- Requests bearer token using stored consumer key and secret from the 
`/conf/key-conf.ini` file
- Performs searches according to the config in the `conf/search.ini` file
- Returns data by print based on the search() function (and nested calls)
- Example raw output from twitter API responses added to the `/resources/` directory
- Example of building the key testing in the `/resources/` directory
- .gitignore added so the REAL search terms, keys, and secrets are not uploaded to github.
(Don't give away your secrets!)
- Readme explains first time use and setting up the pre-requisites.
- Added a changelog (this document)



#### Style

Version - Date version complete - Description

- Change 1
- Change 2
