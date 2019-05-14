#!/usr/bin/env python
# _*_coding:utf-8_*_
''' 
    * @author: Xwl_Yu.
'''

import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACCOUNT_DATABASE = {
    'engine':'file_storage',
    'name':'account',
    'username':None,
    'password':None,
    'path':'%s/db'%BASE_DIR
}

BASE_DATABASE = {
    'engine':'file_storage',
    'name':'base',
    'username':None,
    'password':None,
    'path':'%s/db'%BASE_DIR
}

DEFAULT_ADMIN_ACCOUNT = 'admin'
DEFAULT_ADMIN_PASSWORD = 'admin'

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'access':'access.log',
}

