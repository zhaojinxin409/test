#-*- coding:utf8 -*-
import tools
import httplib
import json
import cPickle


#oauth_token = '03e16fd258182fd83848777f'
#oauth_token_secret = 'f0eb2fe53e5e419fa10753064dcae101'
try:
    file_p = open('config')
    oauth_token = cPickle.load(file_p)
    oauth_token_secret = cPickle.load(file_p)
    file_p.close()
except IOError,e:
    print 'Not logged in'
    exit()

def clear():
    import os
    os.remove('config')
def who():
    global oauth_token
    global oauth_token_secret
    
    url = 'openapi.kuaipan.cn'
    base = '/1/account_info?'
    nonce_ori = tools.genRandom()
    nonce = 'oauth_nonce='+ nonce_ori +'&'
    ts_ori = tools.genTimeStamp()
    timestamp = 'oauth_timestamp='+ ts_ori +'&'
    ck_ori = 'xc0R4bpv0Y5ZtIjS'
    consumer_key = 'oauth_consumer_key=' + ck_ori + '&'
    consumer_secret = 'CrHgPlcLwd3GXucV'
    sm_ori = 'HMAC-SHA1'
    signature_method = 'oauth_signature_method=' + sm_ori + '&'
    v_ori = '1.0'
    version = 'oauth_version='+v_ori+'&'
    token = 'oauth_token='+oauth_token+'&'
    
    method = 'GET'
    baseUri = 'http://' + url + base[:-1]
    params = {
            'oauth_version': v_ori, 
            'oauth_signature_method': sm_ori, 
            'oauth_nonce': nonce_ori, 
            'oauth_timestamp': ts_ori, 
            'oauth_consumer_key': ck_ori, 
            'oauth_token' : oauth_token
    }
    
    consumers = {
            'consumer_key':  ck_ori,
            'consumer_secret': consumer_secret
    }
    
    tokens = {
            'oauth_token':oauth_token,
            'oauth_token_secret':oauth_token_secret
    }
    signature = 'oauth_signature=' + tools.genSignature(method, baseUri, consumers, tokens, params)
    param = base + nonce + timestamp + consumer_key + signature_method + version + token + signature
    #print consumers
    #print tokens
    #print 'http://' + url + param
    #读取
    conn = httplib.HTTPConnection(url)
    conn.request('GET', param)
    rs = conn.getresponse()
    return_code = str(rs.status).upper()
    if(return_code != '200'):
        print rs.read()
        raise NameError('error return code' + return_code)
    body = rs.read()
    #解析JSON
    request_obj = json.loads(str(body))
    print 'user\t\ttotal\t\tused\t\t'
    print '%s\t%s\t%s\t'%(request_obj['user_name'],request_obj['quota_total'],request_obj['quota_used'])
    