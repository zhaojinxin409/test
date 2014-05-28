#-*- coding:utf8 -*-
'''
Created on this night

@author: Administrator
'''

import httplib
import tools
import json
import webbrowser


oauth_token = ''
oauth_token_secret = ''


def request():
    global oauth_token
    global oauth_token_secret
    url = 'openapi.kuaipan.cn'
    base = '/open/requestToken?'
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
    method = 'GET'
    baseUri = 'https://' + url + base[:-1]
    params = {
            'oauth_version': v_ori, 
            'oauth_signature_method': sm_ori, 
            'oauth_nonce': nonce_ori, 
            'oauth_timestamp': ts_ori, 
            'oauth_consumer_key': ck_ori, 
    }
    
    consumers = {
            'consumer_key':  ck_ori,
            'consumer_secret': consumer_secret
    }
    
    tokens = {
    }
    signature = 'oauth_signature=' + tools.genSignature(method, baseUri, consumers, tokens, params)
    param = base + nonce + timestamp + consumer_key + signature_method + version + signature
    #print 'https://' + url + param
    #读取
    conn = httplib.HTTPSConnection(url)
    conn.request('GET', param)
    rs = conn.getresponse()
    return_code = str(rs.reason).upper()
    if(return_code != 'OK'):
        raise NameError('error return code' + return_code)
    body = rs.read()
    #解析JSON
    request_obj = json.loads(str(body))
    oauth_token = request_obj['oauth_token']
    oauth_token_secret = request_obj['oauth_token_secret']
    
def authorize():
    
    #登陆授权
    au_url = 'https://www.kuaipan.cn/api.php?ac=open&op=authorise&oauth_token=' + oauth_token
    print 'The url is :  %s'%(au_url)
    webbrowser.open_new_tab(au_url)
    
    
def swapToken():
    
    global oauth_token
    global oauth_token_secret
    temp = raw_input('Have you allowed the program to enter your NetDisk?  Y/N :').upper()
    if not(temp == 'Y'):
        return
    url = 'openapi.kuaipan.cn'
    base = '/open/accessToken?'
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
    baseUri = 'https://' + url + base[:-1]
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
    #print 'https://' + url + param
    #读取
    conn = httplib.HTTPSConnection(url)
    conn.request('GET', param)
    rs = conn.getresponse()
    return_code = str(rs.status).upper()
    if(return_code != '200'):
        raise NameError('error return code' + return_code)
    body = rs.read()
    #解析JSON
    request_obj = json.loads(str(body))
    #print request_obj
    oauth_token = request_obj['oauth_token']
    oauth_token_secret = request_obj['oauth_token_secret']
    
def save():
    '''
    保存token和token_secret到config文件中
    '''
    import cPickle as pkl
    import os
    global oauth_token
    global oauth_token_secret
    
    if os.path.exists('config'):
        os.remove('config')
    file_p = open('config','w')
    
    pkl.dump(oauth_token, file_p, protocol=0)
    pkl.dump(oauth_token_secret,file_p,protocol=0)
    file_p.close()
    


try:
    request()
    authorize()
    swapToken()
    #write the token to the file
    save()
        
except NameError , e:
    print 'Binding failure.'    
    print e
    
    
