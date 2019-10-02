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

# my private classes & methods
from ajb_bootstrap import ajb_bootstrap

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

####################### main ###########################
def main():
    parser = argparse.ArgumentParser()
    # Mandatory args
    parser.add_argument('-p','--password', help='password for accessing website', required=True, default='nopassword')
    parser.add_argument('-u','--username', help='username for accessing website', required=True, default='iamnobody')

    # optional args
    parser.add_argument('-d','--dbload', help='save JSON data into mongodb', action='store_true', dest='bool_dbload', required=False, default=False)
    parser.add_argument('-g','--gameweek', help='game weeks to analyze', required=False, default=False)
    parser.add_argument('-l','--league', help='league entry id', required=False, default=False)
    parser.add_argument('-q','--query', help='squad player id', required=False, default=False)
    parser.add_argument('-r','--recleague', help='recursive league details', action='store_true', dest='bool_recleague', required=False, default=False)
    parser.add_argument('-s','--studentid', help='student id', required=False, default='noplayerid')

    # info and help args
    parser.add_argument('-v','--verbose', help='verbose error logging', action='store_true', dest='bool_verbose', required=False, default=False)
    parser.add_argument('-x','--xray', help='enable all test vars/functions', action='store_true', dest='bool_xray', required=False, default=False)


    args = vars(parser.parse_args())
    print ( " " )
    print ( "########## bootstraping ##########" )
    print ( " " )

# ARGS[] pre-processing - set-ip logging before anything else
    if args['bool_verbose'] is True:
        print ( "Enabeling verbose info logging..." )
        logging.disable(0)     # Log level = NOTSET
        print ( "Command line args passed from shell..." )
        print ( parser.parse_args() )
        print ( " " )
    else:
        logging.disable(20)    # Log lvel = INFO

    # now process remainder of cmdline args[]
    username = args['username']
    password = args['password']
    xray_testing = args['bool_xray']

    print ( "XRAY TEST: ", xray_testing )
    bootstrap = ajb_bootstrap(100, username, password)         # create an instance of main player database
    # i_am = player_entry(this_player)                      # create instance of players basic ENTRY data-set (publically viewable stuff)

#    print ( "My name is:", i_am.entry['player_first_name'], i_am.entry['player_last_name'] )
#    print ( "My name is:", i_am.my_name() )
#    print ( "My teams name is:", i_am.my_teamname() )
#    print ( "My team ID is:", i_am.my_id() )
#    print ( "My Username:", username )
#    print ( "My Passowrd:", password )

print ( " " )
print ( "### main() - DONE ###" )

if __name__ == '__main__':
    main()
