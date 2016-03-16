#!/usr/bin/python

import os
import Cookie
import time
import random

def create_cookies():
    try:
        cookieDict = Cookie.SimpleCookie(os.environ['HTTP_COOKIE'])
    except KeyError:
        cookieDict = Cookie.SimpleCookie()

    try:
        oldSession = cookieDict['session'].value
    except KeyError:
        oldSession = None

    expireTimestamp = time.time() + 1 * 24 * 60 * 60
    expireTime = time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(expireTimestamp))

    if (oldSession == None):
        sessionValue = str(random.randint(0, 100000))
    else:
        sessionValue = oldSession

    cookieDict['session'] = sessionValue
    cookieDict['session']['expires'] = expireTime

    return cookieDict

def find_cookie():
    try:
        cookieDict = Cookie.SimpleCookie(os.environ['HTTP_COOKIE'])
    except KeyError:
        cookieDict = Cookie.SimpleCookie()
    try:
        oldSession = cookieDict['session'].value
    except KeyError:
        oldSession = None

    return oldSession

def remove_cookie():

    cookieDict = Cookie.SimpleCookie()
    expireTimestamp = time.time() + 0.1
    expireTime = time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(expireTimestamp))
    cookieDict['session'] = None
    cookieDict['session']['expires'] = expireTime

    return cookieDict