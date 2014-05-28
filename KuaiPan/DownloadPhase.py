#-*- coding:utf8 -*-
'''
Created on 2014年5月16日

@author: Administrator
'''
import httplib
import json
import cPickle
import tools
import sys



def download(path_ori,to_path = 'none',root_ori = 'app_folder'):
    try:
        file_p = open('config')
        oauth_token = cPickle.load(file_p)
        oauth_token_secret = cPickle.load(file_p)
        file_p.close()
    except IOError,e:
        print 'Not logged in'
        exit()
    
    '''
            取得上传的URL
    '''
    global upload_url
    
    #http://api-content.dfs.kuaipan.cn/1/fileops/download_file
    
    url = 'api-content.dfs.kuaipan.cn'
    base = '/1/fileops/download_file?'
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
    path = 'path='+path_ori+'&'
    root = 'root='+root_ori+'&'
    
    
    method = 'GET'
    baseUri = 'http://' + url + base[:-1]
    params = {
            'oauth_version': v_ori, 
            'oauth_signature_method': sm_ori, 
            'oauth_nonce': nonce_ori, 
            'oauth_timestamp': ts_ori, 
            'oauth_consumer_key': ck_ori, 
            'oauth_token' : oauth_token,
            'path': path_ori,
            'root': root_ori
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
    param = base + nonce + timestamp + consumer_key + signature_method + version + token + path + root + signature
    #print 'http://' + url + param
    #读取
    '''
    conn = httplib.HTTPConnection(url)
    conn.request('GET', param)
    rs = conn.getresponse()
    return_code = str(rs.status).upper()
    #if(return_code != '200'):
      #  raise NameError('error return code  ' + return_code)
    headers = rs.getheader('set-cookie')
    print headers
    
    body = rs.read()
    #解析JSON
    print body
    '''
    import requests
    r = requests.get("http://" + url + param)
    #if len(sys.argv) < 2:
    file = open(to_path,'wb')
    file.write(r.content)
    file.close()
    '''
    else:
        import os
        path = to_path
        if(not os.path.exists(os.path.dirname(path))):
            os.makedirs(path)
        try:
            file = open(sys.argv[1],'wb')
            file.write(r.content)
            file.close()
        except Exception,e:
            print e
    '''
    
#download('abf.txt','tttt.txt')

