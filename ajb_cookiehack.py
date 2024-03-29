#!/usr/bin/python3
import requests
from requests import Request, Session
from requests_html import HTMLSession
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

# ajab_global_urls
SLOOP_URL = "https://www.schoolloop.com/"
SLOOP_MY_SCHOOL = "https://ois-orinda-ca.schoolloop.com/"
LOGIN_URL = "portal/login/"

# Portal main URL home pages
PARENT_HOME = "portal/parent_home/"
MAIL = "loopmail/inbox?d=x"
CALENDAR = "calendar/month/"

####################################################
# Fixure analytics was a poorly managed & messy JSON dataset
# in the game model. As of 2019/2020 season, they game architects
# seem to have started addressing this and moved all STANDINGS and
# FGIXTURES related data into a less cryptic JSON dataset

class cookiebakery:
    """Class to identify a user via userid passed in cmdline args"""
    """and then locate the correct cookie to set for this user"""
    """Known cookies are held in-line in a dict. Not in an editible file"""
    """Instance INIT does **NOT** install the cookie."""

    # Class Global attributes
    user = ""
    password = ""
    api_get_status = ""
    bootstrap = ""
    my_cookie = ""
    request = ""

    def __init__(self, username, password, request_session):
        """Instantiation does **NOT** install a cookie"""
        """It just locates the correct cookie to use based on the username credentials."""
        """Do the physical install seperately via the set_cookie method"""

        self.user = username
        self.password = password
        cookiebakery.user = username

        logging.info('cookiebakery() - INIT cookiebakery instance for user: %s' % self.user )

        userid_cookies = { \
                'dbrace': '__cfduid=d6ac2f7b9bd1249d750303b3bde6874311569895002; slid=1569895054259; __cfruid=fb7287adbd466aff340d6825af9aa20289886e13-1570157743; JSESSIONID=q45szp7owg2iaavyj66xxdh;', \
                'cynthia': 'eyJzIjogIld6SXNNalUyTkRBM01USmQ6MWh5aE9BOmdLcXg0S3RkSGR5UVRXRjUwVjhxZHR4RVNTayIsICJ1IjogeyJpZCI6IDI1NjQwNzEyLCAiZm4iOiAiRHJvaWQiLCAibG4iOiAiQWxwaGEiLCAiZmMiOiA1N319', \
                'naruto': 'eyJzIjogIld6SXNOVGc0T0RnM05WMDoxaHlpdU46MlhhRDZlbkx3YU03WFdtb0tBWEhsYXlESlBnIiwgInUiOiB7ImlkIjogNTg4ODg3NSwgImZuIjogIkRhdmlkIiwgImxuIjogIkJyYWNlIiwgImZjIjogOH19', \
                'family@usakiwi.com': 'eyJzIjogIld6VXNOVGc0T0RnM05WMDoxZnYzYWo6WGkxd1lMMnpLeW1pbThFTTVFeGEzVFdUaWtBIiwgInUiOiB7ImxuIjogIkJyYWNlIiwgImZjIjogOCwgImlkIjogNTg4ODg3NSwgImZuIjogIkRhdmlkIn19' }

        for userid, cookie_hack in userid_cookies.items():
            if userid == self.user:
                #s.cookies.update({'????_cookie_to_set_hack_????': cookie_hack})
                logging.info('cookiebakery() - FOUND - cookie for userid: %s' % self.user )
                logging.info('cookiebakery() - SETUP - cookie to: %s' % cookie_hack )
                cookiebakery.my_cookie = cookie_hack      # INSTALL users cookie as instance accessor
                cookiebakery.request = request_session    # INSTALL request session used for this cookie hack as instance accessor
                break    # found this players cookie
            else:
                logging.info('cookiebakery() - NO MATCH - cookie/userid: %s' % userid )
                cookiebakery.my_cookie = "FAILED"

        if cookiebakery.my_cookie == "FAILED":
            logging.info('cookiebakery() - ABORT - No cookie found for userid: %s EXITING...' % self.user )
        else:
            logging.info('cookiebakery() - SUCCESS - Good cookie & stored inside instance for userid: %s EXITING...' % self.user )
            return

        return    # catchall

# Class methods
    def set_cookie(self, request_session):
        """Set and install a cookie for this userid into the Session structure"""
        """You *should* only do this before executing the HTTP req GET on the wire"""
        self.s = request_session
        logging.info('cookiebakery::set_cookie - EXTRACTed saved cookie from bootstrap for userid: %s' % cookiebakery.user )
        logging.info('cookiebakery::set_cookie - SET cookie: %s' % cookiebakery.my_cookie )
        self.s.cookies.update({'COOKIE': cookiebakery.my_cookie})
        return


    def my_cookie(self):
        """Small helper method to output this users cookie that must be used"""
        """for any authentication operations"""

        logging.info('cookiebakery::my_cookie - cookie: %s' % cookiebakery.my_cookie )
        return cookiebakery.my_cookie


    def response_cookie(self, request_session):
        """Output the RESPONSE cookie info returned from a request session"""
        """This does not print the entire cookiejar array. Just 1 specific cookie"""

        self.s = request_session
        r_auth_cookie = requests.utils.dict_from_cookiejar(self.s.cookies)
        logging.info('cookiebakery::response_cookie AUTH login resp cookie: %s' % r_auth_cookie['COOKIE'] )
        return r_auth_cookie['COOKIE']


    def cookie_url(self):
        """Output the URL and status associated with the session request for setting this cookie"""
        """This method assumes the **original** session request that you used on class INIT"""

        self.url = cookiebakery.request.url
        self.status = cookiebakery.request.status_code
        logging.info('cookiebakery::cookie_url - url: %s' % self.url )
        logging.info('cookiebakery::cookie_url - url get status: %s' % self.status )
        return self.url
