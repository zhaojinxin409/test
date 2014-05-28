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
upload_url = ''

def getAddress():
    '''
            取得上传的URL
    '''
    global oauth_token
    global oauth_token_secret
    global upload_url
    
    
    url = 'api-content.dfs.kuaipan.cn'
    base = '/1/fileops/upload_locate?'
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
    #print 'http://' + url + param
    #读取
    conn = httplib.HTTPConnection(url)
    conn.request('GET', param)
    rs = conn.getresponse()
    return_code = str(rs.status).upper()
    if(return_code != '200'):
        raise NameError('error return code' + return_code)
    body = rs.read()
    #解析JSON
    request_obj = json.loads(str(body))
    upload_url = request_obj['url']


def Upload(filename,filepath,path_ori='/',overwrite_ori='True',root_ori='app_folder'):
    from poster.encode import multipart_encode
    from poster.streaminghttp import register_openers
    import urllib2
    
    global oauth_token
    global oauth_token_secret
    global upload_url
    
    
    url = upload_url
    base = '/1/fileops/upload_file?'
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
    
    path_ori = path_ori + filename
    path = 'path=' + path_ori  + '&'
    overwrite = 'overwrite=' + overwrite_ori + '&'
    root = 'root=' + root_ori + '&'
    
    
    method = 'POST'
    baseUri = url + base[:-1]
    params = {
            'oauth_version': v_ori, 
            'oauth_signature_method': sm_ori, 
            'oauth_nonce': nonce_ori, 
            'oauth_timestamp': ts_ori, 
            'oauth_consumer_key': ck_ori, 
            'oauth_token' : oauth_token,
            'path' : path_ori,
            'root' : root_ori,
            'overwrite' : overwrite_ori
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
    param = base + nonce + timestamp + consumer_key + signature_method + version + token + path + root + overwrite + signature
    #print url + param
       
    
    #register
    register_openers()
    
    datagen, headers = multipart_encode({filename: open(filepath, "rb")})

    # Create the Request object
    request = urllib2.Request(url + param, datagen, headers)
    # Actually do the request, and get the response
    try:
        rs = urllib2.urlopen(request).read()
        print 'Upload done.'
    except urllib2.HTTPError,e:
        print 'Error uploading file'
        print e
    

