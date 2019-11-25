# Copyright (c) 2019 Deere & Company
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.


import sys
sys.path.insert(0, './python_modules')
from requests_oauthlib.oauth1_session import OAuth1Session
import requests
import datetime
import os
import pprint
import json
import logging

#############################################################################
# Email
# Email
SEND_TO = ['']  # list of email addresses
SEND_FROM = ''  # must be SES verified in Hutch's AWS admin account
EMAIL_SUBJECT = 'Field Operation Event Notification'
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'  # 'mail.dx.deere.com'
EMAIL_PORT = 587  # port 25, 587, or 2587 for aws
EMAIL_USER = 'git from the usual place'
EMAIL_PW = 'git from the usual place'

# OAuth Constants
CLIENT_KEY = ''
CLIENT_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
