#!/usr/bin/python3
import requests
from requests import Request, Session
import json
import sys
import unicodedata
import logging
import http.client

from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
from six import iteritems
from six import itervalues

# logging setup
logging.basicConfig(level=logging.INFO)

############################################
# note: Must be authourized by credentials
#
class ajb_bootstrap:
    """Base class for extracting the core game ENTRY dataset"""
    """This class requires valid credentials"""
    """but does not contain the full player private ENTRY dataset"""

    # Class Global attributes
    username = ""
    password = ""
    current_week = ""
    api_get_status = ""
    epl_team_names = {}
    my_cookie = ""

    def __init__(self, studentidnum, username, password):
        self.studentidnum = str(studentidnum)
        self.username = username
        self.password = password
        ajb_bootstrap.username = username    # make USERNAME global accessor to class instance
        ajb_bootstrap.password = password    # make PASSWORD global accessor to class instance

        logging.info('ajb_bootstrap:: - bootstrap ENTRY class instance for student: %s' % self.studentidnum )

        self.epl_team_names = {}    # global PRIVATE helper dict accessible from within this base class
        s = requests.Session()
        user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}
        API_URL0 = 'https://fantasy.premierleague.com/a/login'
        API_URL1 = FPL_API_URL + BSS

        pl_profile_cookies = { \
                '1212166': 'eyJzIjogIld6VXNNalUyTkRBM01USmQ6MWZpdE1COjZsNkJ4bngwaGNUQjFwa3hMMnhvN2h0OGJZTSIsICJ1IjogeyJsbiI6ICJBbHBoYSIsICJmYyI6IDM5LCAiaWQiOiAyNTY0MDcxMiwgImZuIjogIkRyb2lkIn19', \
                '1995215': 'eyJzIjogIld6SXNNalUyTkRBM01USmQ6MWh5aE9BOmdLcXg0S3RkSGR5UVRXRjUwVjhxZHR4RVNTayIsICJ1IjogeyJpZCI6IDI1NjQwNzEyLCAiZm4iOiAiRHJvaWQiLCAibG4iOiAiQWxwaGEiLCAiZmMiOiA1N319', \
                '1994221': 'eyJzIjogIld6SXNOVGc0T0RnM05WMDoxaHlpdU46MlhhRDZlbkx3YU03WFdtb0tBWEhsYXlESlBnIiwgInUiOiB7ImlkIjogNTg4ODg3NSwgImZuIjogIkRhdmlkIiwgImxuIjogIkJyYWNlIiwgImZjIjogOH19', \
                '1136396': 'eyJzIjogIld6VXNOVGc0T0RnM05WMDoxZnYzYWo6WGkxd1lMMnpLeW1pbThFTTVFeGEzVFdUaWtBIiwgInUiOiB7ImxuIjogIkJyYWNlIiwgImZjIjogOCwgImlkIjogNTg4ODg3NSwgImZuIjogIkRhdmlkIn19' }

        for pl, cookie_hack in pl_profile_cookies.items():
            if pl == self.studentidnum:
                s.cookies.update({'pl_profile': cookie_hack})
                logging.info('fpl_bootstrap:: FOUND - cookie for playerid: %s' % pl )
                logging.info('fpl_bootstrap:: SET - cookie to: %s' % cookie_hack )
                fpl_bootstrap.api_get_status = "GOODCOOKIE"
                fpl_bootstrap.my_cookie = cookie_hack    # save cookie as instance accessor
                break    # found this players cookie
            else:
                logging.info('fpl_bootstrap:: NO MATCH - cookie/playerid: %s' % pl )
                fpl_bootstrap.api_get_status = "FAILED"

        if fpl_bootstrap.api_get_status == "FAILED":
            logging.info('fpl_bootstrap:: ABORT - No cookie for player: %s EXITING... %s' % pl )
            Return

# Do REST API I/O now...
# 1st get authenticates, but must use critical cookie (i.e. "pl_profile")
# 2nd get does the data extraction if auth succeeds - failure = all JSON dicts/fields are empty
        rx0 = s.get( API_URL0, headers=user_agent, auth=HTTPBasicAuth(self.username, self.password) )
        rx1 = s.get( API_URL1, headers=user_agent, auth=HTTPDigestAuth(self.username, self.password) )
        self.auth_status = rx0.status_code
        self.gotdata_status = rx1.status_code
        logging.info('fpl_bootstrap:: - init - Logon AUTH url: %s' % rx0.url )
        logging.info('fpl_bootstrat:: - init - API data get url: %s' % rx1.url )

        rx0_auth_cookie = requests.utils.dict_from_cookiejar(s.cookies)
        logging.info('fpl_bootstrap:: AUTH login resp cookie: %s' % rx0_auth_cookie['pl_profile'] )

        if rx0.status_code != 200:    # failed to authenticate
            logging.info('fpl_bootstrap:: - init ERROR login AUTH failed with resp %s' % self.auth_status )
            return

        if rx1.status_code != 200:    # 404 API get failed
            logging.info('fpl_bootstrap:: - init ERROR API get failed with resp %s' % self.gotdata_status )
            return
        else:
            logging.info('fpl_bootstrap:: - Login AUTH success resp: %s' % self.auth_status )
            logging.info('fpl_bootstrap:: - API data GET resp is   : %s  ' % self.gotdata_status )
            # create JSON dict with players ENTRY data, plus other data thats now available
            # WARNING: This is a very large JSON data structure with stats on every squad/player in the league
            #          Dont load into memory multiple times. Best to insert into mongodb & access from there
            # EXTRACT JSON data/fields...
            # note: entry[] and player[] are not auto loaded when dataset lands (not sure why)
            t0 = json.loads(rx1.text)
            self.events = t0['events']
            self.game_settings = t0['game_settings']
            self.phases = t0['phases']
            self.teams = t0['teams']                    # All details of EPL teams in Premieership league this year
            self.elements = t0['elements']              # big data-set for every EPL squad player full details/stats
            self.stats = t0['element_stats']              # big data-set for every EPL squad player full details/stats
            self.element_types = t0['element_types']
            fpl_bootstrap.current_event = self.current_event    # set class global var so current week is easily accessible
        return

    def my_cookie(self):
        """Small helper method to output this users cookie that must be used"""
        """for any authentication operations"""

        logging.info('fpl_bootstrap.my_cookie() - cookie pl_profile: %s' % fpl_bootstrap.my_cookie )
        return fpl_bootstrap.my_cookie