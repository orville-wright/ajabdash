#!/usr/bin/python3
import requests
from requests import Request, Session
import json
import sys
import unicodedata
import logging
import argparse
import http.client

from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
from six import iteritems
from six import itervalues

# my private classes & methods
from ajb_cookiehack import cookiebakery
import ajab_global_urls

# ajab_global_urls
SLOOP_URL = "https://www.schoolloop.com/"
SLOOP_MY_SCHOOL = "https://ois-orinda-ca.schoolloop.com/"
LOGIN_URL = "portal/login/"

# Portal main URL home pages
PARENT_HOME = "portal/parent_home/"
MAIL = "loopmail/inbox?d=x"
CALENDAR = "calendar/month/"

# logging setup
logging.basicConfig(level=logging.INFO)

############################################
# note: Must be authourized by credentials
#
class ajb_bootstrap:
    """Base class for intial dashboard connection, credentials & data set access"""
    """This class requires valid credentials"""

    # Class Global attributes
    username = ""
    password = ""
    current_week = ""
    api_get_status = ""
    epl_team_names = {}
    my_cookie = ""
    rx0 = ""
    rx1 = ""
    all_auth_cookies = ""

    def __init__(self, studentidnum, username, password, args):
        self.studentidnum = str(studentidnum)
        self.username = username
        self.password = password
        ajb_bootstrap.username = username    # make USERNAME global accessor to class instance
        ajb_bootstrap.password = password    # make PASSWORD global accessor to class instance

        logging.info('ajb_bootstrap() - INIT bootstrap inst for student: %s' % self.studentidnum )

        s = requests.Session()
        user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}
        #API_URL0 = 'https://fantasy.premierleague.com/a/login'
        # API_URL1 = FPL_API_URL + BSS
        URL0 = SLOOP_MY_SCHOOL + LOGIN_URL
        URL1 = SLOOP_MY_SCHOOL + PARENT_HOME

        if args['bool_xray'] is False:
            bootstrap_cookie = cookiebakery(self.username, self.password, s)
        else:
            logging.info('ajb_bootstrap() - INIT quick exit for XRAY testing' )
            return

        if bootstrap_cookie.my_cookie == "FAILED":
            logging.info('ajb_bootstrap() - INIT Error cookiebakery() failed to find/set cookie' )
            return
        else:
            # executing the real HTTP GET on the wire now...
            bootstrap_cookie.set_cookie(s)
            rx0 = s.get( URL0, headers=user_agent, auth=HTTPBasicAuth(self.username, self.password) )
            rx1 = s.get( URL1, headers=user_agent, auth=HTTPDigestAuth(self.username, self.password) )
            self.auth_status = rx0.status_code
            self.gotdata_status = rx1.status_code
            ajb_bootstrap.rx0 = rx0    # response to a session GET
            ajb_bootstrap.rx1 = rx1    # response to a session GET

            logging.info('ajb_bootstrap() - INIT : Logon AUTH url: %s' % rx0.url )
            logging.info('ajb_bootstrat() - INIT : API data get url: %s' % rx1.url )

            rx0_auth_cookies = requests.utils.dict_from_cookiejar(s.cookies)
            ajb_bootstrap.all_auth_cookies = rx0_auth_cookies
            logging.info('ajb_bootstrap() - AUTH login resp cookie: %s' % rx0_auth_cookies['????_cookie_to_set_hack_????'] )    # just 1 cookie

            if rx0.status_code != 200:    # failed to authenticate
                logging.info('ajb_bootstrap() - INIT Error login AUTH failed with resp %s' % self.auth_status )
                return

            if rx1.status_code != 200:    # 404 API get failed
                logging.info('ajb_bootstrap() - INIT Error API get failed with resp %s' % self.gotdata_status )
                return
            else:
                logging.info('ajb_bootstrap() - Login AUTH success resp: %s' % self.auth_status )
                logging.info('ajb_bootstrap() - API data GET resp is   : %s  ' % self.gotdata_status )

                # create JSON dict with players ENTRY data, plus other data thats now available
                # WARNING: This is a very large JSON data structure with stats on every squad/player in the league
                #          Dont load into memory multiple times. Best to insert into mongodb & access from there
                # EXTRACT JSON data/fields...
                # note: entry[] and player[] are not auto loaded when dataset lands (not sure why)
                #t0 = json.loads(rx1.text)
                #self.events = t0['events']
                #self.game_settings = t0['game_settings']
                #self.phases = t0['phases']
                #self.teams = t0['teams']                    # All details of EPL teams in Premieership league this year
                #self.elements = t0['elements']              # big data-set for every EPL squad player full details/stats
                #self.stats = t0['element_stats']              # big data-set for every EPL squad player full details/stats
                #self.element_types = t0['element_types']
                #fpl_bootstrap.current_event = self.current_event    # set class global var so current week is easily accessible
            return

        return     # catchall


    def my_cookie(self):
        """Small helper method to output this users cookie that must be used"""
        """for any authentication operations"""

        logging.info('ajb_bootstrap::my_cookie - cookie ????_cookie_to_set_hack_????: %s' % ajb_bootstrap.my_cookie )
        return ajb_bootstrap.my_cookie


    def my_responses(self, resp_x):
        """Must be either '0' for RX0 or '1' for RX1"""

        logging.info('ajb_bootstrap::my_responses - Dumping data for *RESPONSE*: %s' % resp_x )
        if resp_x == 0:
            print ( " " )
            print ( "=========== RX0 URL ===========" )
            print ( ajb_bootstrap.rx0.request.url )
            print ( " " )
            print ( "=========== RX0 body ===========" )
            print ( ajb_bootstrap.rx0.request.body )
            print ( " " )
            print ( "=========== RX0 Headers ===========" )
            for k, v in ajb_bootstrap.rx0.request.headers.items():
                print ("Key: ", k, " - ", "Data: ", v)
            print ( " " )
            print ( "=========== RX0 ALL Cookies ===========" )
            print ( json.dumps(ajb_bootstrap.all_auth_cookies, indent=0) )
        elif resp_x == 1:
            print ( " " )
            print ( "=========== RX1 URL ===========" )
            print ( ajb_bootstrap.rx1.request.url )
            print ( " " )
            print ( "=========== RX1 body ===========" )
            print ( ajb_bootstrap.rx1.request.body )
            print ( " " )
            print ( "=========== RX1 Headers ===========" )
            for k, v in ajb_bootstrap.rx1.request.headers.items():
                print ("Key: ", k, " - ", "Data: ", v)
            print ( " " )
            print ( "=========== RX1 ALL Cookies ===========" )
            print ( json.dumps(ajb_bootstrap.all_auth_cookies, indent=0) )
        else:
            print ( "ajb_bootstrap::my_responses - BAD response given on call - no data to dump")

        return
