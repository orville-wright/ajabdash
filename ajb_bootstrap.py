#!/usr/bin/python3
import requests
from requests import Request, Session
import json
import sys
import unicodedata
import logging
import argparse
import http.client

from urllib import request, parse
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
LOGIN_URL = "portal/login"
LOGIN_FORM = "?etarget=login_form"
# https://ois-orinda-ca.schoolloop.com/portal/login?etarget=login_form

# Portal main URL home pages
PARENT_HOME = "portal/parent_home/"
MAIL = "loopmail/inbox?d=x"
CALENDAR = "calendar/month/"

# SLOOP_MY_SCHOOL + PARENT_HOME
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
    rx2_resp = ""
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
        s.auth = (self.username, self.password)
        #s.headers.update({'x-test': 'true'})


        #API_URL0 = 'https://fantasy.premierleague.com/a/login'
        # API_URL1 = FPL_API_URL + BSS
        URL0 = SLOOP_MY_SCHOOL + LOGIN_URL
        URL1 = SLOOP_MY_SCHOOL + PARENT_HOME
        URL2 = SLOOP_MY_SCHOOL + LOGIN_URL + LOGIN_FORM
        url2_data = { 'login_name': 'dbrace', 'password': 'Am3li@++', 'form_data_id': '11454190760382967', 'event_override': 'login' }
        #url2_data = parse.urlencode(url2_data).encode()
        url2_post_data = bytes(json.dumps(url2_data), encoding='utf-8')
        url2_headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36', 'content-type': 'application/json' }

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
            rx0 = s.get( URL1, headers=user_agent, auth=HTTPBasicAuth(self.username, self.password) )
            #rx1 = s.get( URL1, headers=user_agent, auth=HTTPDigestAuth(self.username, self.password) )
            rx1 = s.get( URL2, headers=user_agent, auth=HTTPDigestAuth(self.username, self.password) )

            # rx2 = requests.post(URL2, data=url2_data)    # explicit post
            rx2 = request.Request(URL2, data=url2_post_data, headers=url2_headers)    # implied POST because data != None
            rx2_resp = request.urlopen(rx2)

            with request.urlopen(rx2) as mem_file:
                #x = print(mem_file.read(1000).decode('utf-8'))
                x = mem_file.read().decode('utf-8')
                with open('dump_file.html', 'w', encoding="utf-8") as dump_file:
                    # dump_file.write(r.text)
                    dump_file.write( x )

            #rx2 = request.urlopen(URL1)    # GET method
            #dump_url = SLOOP_MY_SCHOOL + PARENT_HOME
            #rx2.request.urlretrieve(dump_url, "test_dump.txt")

            self.auth_status = rx0.status_code
            self.gotdata_status = rx1.status_code
            ajb_bootstrap.rx0 = rx0    # response to a session GET
            ajb_bootstrap.rx1 = rx1    # response to a session GET
            ajb_bootstrap.rx2_resp = rx2_resp    # response to a urlopen(rx2)

            logging.info('ajb_bootstrap() - INIT : GET AUTH rx0 request URL: %s' % rx0.request.url )        # respponse
            logging.info('ajb_bootstrap() - INIT : GET AUTH rx0 response URL: %s' % rx0.url )        # respponse
            logging.info('ajb_bootstrap() - INIT : GET AUTH rx1 request URL: %s' % rx1.request.url )        # respponse
            logging.info('ajb_bootstrat() - INIT : GET AUTH rx1 response URL: %s' % rx1.url )        # respponse
            logging.info('ajb_bootstrat() - INIT : URLOPEN  rx2 request URL: %s' % rx2.get_full_url() )   # respponse
            logging.info('ajb_bootstrat() - INIT : URLOPEN  rx2 rx2.full_url: %s' % rx2.full_url )   # respponse
            logging.info('ajb_bootstrat() - INIT : URLOPEN  rx2 rx2.get_method(): %s' % rx2.get_method() )   # respponse

            logging.info('ajb_bootstrat() - INIT : URLOPEN  rx2 response URL: %s' % rx2_resp.url )   # respponse


            rx0_auth_cookies = requests.utils.dict_from_cookiejar(s.cookies)
            ajb_bootstrap.all_auth_cookies = rx0_auth_cookies
            logging.info('ajb_bootstrap() - AUTH login resp cookie: %s' % rx0_auth_cookies['COOKIE'] )    # just 1 cookie

            if rx0.status_code != 200:    # failed to authenticate
                logging.info('ajb_bootstrap() - INIT Error login AUTH failed with resp %s' % self.auth_status )
                return

            if rx1.status_code != 200:    # 404 API get failed
                logging.info('ajb_bootstrap() - INIT Error API get failed with resp %s' % self.gotdata_status )
                return
            else:
                logging.info('ajb_bootstrap() - Login AUTH success resp: %s' % self.auth_status )
                logging.info('ajb_bootstrap() - API data GET resp is   : %s  ' % self.gotdata_status )
            return
        return     # catch-all


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


    def my_post_resp(self):
            #ajb_bootstrap.rx2_resp = request.urlopen(ajb_bootstrap.rx2)
            print ( "=========== RX2 HEADERS ===========" )
            print ( "** DEBUG : rx2_resp > headers : **", ajb_bootstrap.rx2_resp.headers )
            print ( "=========== RX2 STATUS ===========" )
            print ( "** DEBUG : rx2_resp > status : **", ajb_bootstrap.rx2_resp.status )
            print ( "=========== RX2 BODY ===========" )
            print ( "** DEBUG : rx2_resp > URL : **", ajb_bootstrap.rx2_resp.url )
            print ( "=========== RX2 READ ===========" )
            #print ( "** DEBUG : rx2_resp > read : **", ajb_bootstrap.rx2_resp.read() )
            return
