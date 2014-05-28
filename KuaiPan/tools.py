#-*- coding:utf8 -*-

def genTimeStamp():
    '''
    timestamp
    '''
    import time
    t = time.time()
    return str(int(t))

def genRandom():
    import random
    i = random.randint(1000,1000000)
    return str(i)
    
    
def genSignature(method,baseUri,consumers,tokens,params):
    result = str(method).upper() + '&' + urlencode(baseUri) + '&'
    p_string = ''
    keys = params.keys()
    keys.sort()
    first = True
    for key in keys:
        if first:
            p_string = p_string + urlencode(key) + '=' +urlencode(params[key])
            first = False
        else:
            p_string = p_string + '&' + urlencode(key) + '=' +urlencode(params[key])
    result = result + urlencode(p_string)
    key = consumers['consumer_secret'] + '&'
    if(tokens.has_key('oauth_token_secret')):
        key = key + tokens['oauth_token_secret']
    #print result
    return urlencode(HmacSha1(key,result))
    
    
def HmacSha1(key,data):
    import hmac
    import hashlib
    import base64
    return hmac.new(key,data,hashlib.sha1).digest().encode('base64').rstrip()

def urlencode(str) :
    import urllib
    url =  urllib.urlencode({'':str})[1:]
    url = url.replace('%7E','~')
    return url





