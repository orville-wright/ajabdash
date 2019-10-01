# AJABDash
School Dashboard for Amelia

# ajabdash
- (this doc is formatted as Github Markup lang)
- NOTE: The dataset structures & API of the SchooLoop app at https://www.schoolloop.com and https://ois-orinda-ca.schoolloop.com aree proprietary and closed.

- The are not publicly documented and not open to public consumption.

- No subscription/consumption license is available or offered by https://www.schoolloop.com. Subsequently, NO license to those services is provided, inherited or inferred via the use of this code.


# Primary use case:
A companion dashboard for Schooloop.com (wbeapp and mobile app).

v1.0 of the project is focused on the following priorities...

1. decode login semantics
2. Native data feed data extracted
3. Understanding API I/O. No scraping raw data from JavaScript pages @ https://www.schoolloop.com
4. Understanding all available REST API's used by website & mobile app (i.e. a private API not publicly exposed/documented).
5. Prototyping & validating the API data I/O interface & technology, toolset & overall private game data structures & accessors.
6. Processing API extracted JSON datasets in memory (live) for speed. (avoid flat file ETL/data import at all costs)
7. Push data into MongoDB database where/when needed.
8. Augmenting dashbaord status dataset with additional data/info where key data/fields/structures are not present/provided in native datasets.
9. Apply State-of-Art Datascience logic to extrapolate observations and inferences. e.g. analysis, statistics & probably A/B Hypothesis testing against (via Datasciecne tools such as: Numpy, Pandas, Matplotlib, Scikit-Learn, Scipy & the Berkley Datascience module). Goal is to provide this capability via a Web/GUI experience, not force users interact with shell & write python code.

- Not all of these capabilities are available in v1.0


How to run
=================================
## usage:
   epldecoder.py [-h] [-d] [-l LEAGUE] [-p PLAYER] [-q QUERY] [-r] [-v] [-x] -u USERNAME -c PASSWORD [-g GAMEWEEK]

**optional arguments:**
- -c PASSWORD, --password PASSWORD  password for accessing EPL website
- -d, --dbload                      save JSON data into mongodb
- -g GAMEWEEK, --gameweek GAMEWEEK  game week to analyze
- -h, --help                        show this help message and exit
- -l LEAGUE, --league LEAGUE        league entry id - (a league that you want to evaluate)
- -p PLAYER, --player PLAYER        team player id - (a valid user ID registered in the EPL websit)
- -q QUERY, --query QUERY           squad player id - (a valid selectable squad player...eg. Harry Kane's player code)
- -r, --recleague                   recursive league details - (scan every league you are registered in)
- -u USERNAME, --username USERNAME  a valid username for accessing EPL website
- -v, --verbose                     verbose error logging
- -x, --xray                        dump out some raw JSON data dicts & structures


#

**REQUIRED**
- Username & Password



Notes:
=================================
The goal is to augment the game decision making process with additional analytical data sets that are sources from other locations. These will be created & stored within a MongoDB and cross-referenced with the basic game data-set. Today, this is not easy to do via the current game website: http://www.premierleague.com/en-gb.html. Doing this makes deeper team & player analysis more possible (but more complex). and therefore, better team/player decisions are possible. Many of these data sets come from non EPL websites. e.g. FIFA, gambling sites, football stats sites etc.

Also, the MongoDB data source will be used to drive richer analytical charts that are not available on http://www.premierleague.com/en-gb.html, never were available and are very much needed by the 5,000,000+ users of the Barclays EPL website & App.

These charts can graph info based on the standard dataset from the EPL website as well as graph additional advance charts.

That EPL website used to provided a set of charts to users but this service was removed and discontinued. Fantasy Football players no longer have any charts/graphing service to support their team decisions

A ML/AI engine will also be built and offered to individual players. A player will be able to teach the ML/AI (via a web app/mobile app) to emulate his/her individual analytical team decision making style. Thereby automating the mundane process of choosing a squad by churning through pages of weekly data & relying too much on fuzzy personal logic, gut-feel, intuition, rumors and voodoo on what squad to pick & set-up. This will also allow EPL Fantasy Football players to run 1000's of possible permutations against potential squads (e.g., who to captain, who to vice-captain, when to play a wild card, what to play special options etc...all before the game day cut-off time.
The ML/AI engine will operate under a set of personalize-able & tunable rules that "you" can define and control and do things like ...

- Scan for injury rumors, news and info then compute player not-starting probabilities
- Scan for hot & cold trends
- Extrapolate scoring runs and trends and predict possible 'Black Swan' events
- Compute best captain probabilities
- Compute best & worst games to play/avoid.
- Compute highest scoring probability of each game and player scoring probabilities
- Propose possible teams, transfers and team configs

...etc, etc

#
**Data Science**

As of 2019/2020 season, the code will implement & leverage Data Science code & functions provided by NUMPY & PANDAS.

This was always the long term strategy.

These python Data Science modules work well in a LINUX env & are easy to install, but can be tricky/problematic to get installed & running in a local Windows OS env. My Windows Dev environment uses Anaconda Python because it's the only way I can get a working Matplotlib for Windows Python module that works).

#
More to come. ~Orville
