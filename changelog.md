# Change Log

0.2 - 07/24/18 - New branch opened. The goal of this branch is to incorporate better
ways to search for data that is relevant to the user and to allow for twitter interactions,
where this could be defined pretty broadly. This does signal a change from research to
i/o, but the intent is to build up the research side (specificity, automation) while
enabling some automation for the interaction side as well.

Changes:

- Readme and changelog updated to contain new changes and relevant data.
- 

0.1 - 07/24/18 - Completion of minimum viable script. There were a lot of changes so let's just
call this the start version. Current features:
- Checks for stored bearer token (`/conf/bearer.token`)
- Requests bearer token using stored consumer key and secret from the `/conf/key-conf.ini` file
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
