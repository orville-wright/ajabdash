#!/usr/bin/python3
import requests
from requests import Request, Session
import json
import sys
import unicodedata
import logging
import argparse
from random import randint
#import pandas as pd

from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
from six import iteritems
from six import itervalues

####################################################
# Fixure analytics was a poorly managed & messy JSON dataset
# in the game model. As of 2019/2020 season, they game architects
# seem to have started addressing this and moved all STANDINGS and
# FGIXTURES related data into a less cryptic JSON dataset

class cookiebakery:
    """Base class to manage fixtires related info"""
    """This JSON dataset may be publically accessible."""
    """So it doesn't require any auth"""

    # Class Global attributes
    this_event = ""
    api_get_status = ""
    standings_t = ""
    bootstrap = ""
    ds_df0 = ""        # Data science DATA FRAME 0  (fixtures)

    def __init__(self, playerid, bootstrapdb, eventnum):
        self.eventnum = str(eventnum)
        self.playeridnum = playerid
        logging.info('allfixtures:: - create fixtures class instance for gameweek: %s' % self.eventnum )
# new v3.0 cookie hack
        s = requests.Session()
        user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}
        API_URL0 = 'https://fantasy.premierleague.com/a/login'
        API_URL1 = FPL_API_URL + 'fixtures/?event=' + self.eventnum

        logging.info('get_opponents_squad:: EXTRACT saved cookie from bootstrap for playerid: %s' % self.playeridnum )
        logging.info('get_opponents_squad:: SET cookie: %s' % self.bootstrap.my_cookie )
        s.cookies.update({'pl_profile': self.bootstrap.my_cookie})

## Do REST API I/O now...
# 1st get authenticates, but must use critical cookie (i.e. "pl_profile")
# 2nd get does the data extraction if auth succeeds - failure = all JSON dicts/fields are empty
        rx0 = s.get( API_URL0, headers=user_agent )
        rx1 = s.get( API_URL1, headers=user_agent )
        self.auth_status = rx0.status_code
        self.gotdata_status = rx1.status_code
        logging.info('allfixtures:: init - Logon AUTH url: %s' % rx0.url )
        logging.info('allfixtures:: init - API data get url: %s' % rx1.url )

        rx0_auth_cookie = requests.utils.dict_from_cookiejar(s.cookies)
        logging.info('allfixtures:: AUTH login resp cookie: %s' % rx0_auth_cookie['pl_profile'] )

        return
